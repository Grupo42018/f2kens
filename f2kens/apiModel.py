# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.utils import encoding
import http.client as http
import json
import socket
import base64
import itertools
import inspect

conn = http.HTTPConnection(settings.ASISTENCIA['API'])
baseroute = settings.ASISTENCIA['baseroute']

try:
    conn.request('HEAD', baseroute)
except socket.gaierror:
    raise socket.error("The API url is wrong or the server is not responding")

res = conn.getresponse()
if res.status == 404:
    raise AttributeError("The API route set hasn't been found in the selected API host")

class ApiModel(object):
    def __init__(self, _parent=None, **kwargs):
        #check if the _url attribute was set and its type
        if not isinstance(self._url, str):
            raise TypeError("The _url variable should be set and has to be a string")

        self._heigh= 0 if not _parent else _parent._heigh+1 
        self._parent=_parent

        if self.__class__.__base__ is ApiModel:
            self._api_id = kwargs['id']


        #add the attributes to get from the api. These shoud have been added as variables when this class is inherited
        self._attributes = []
        for attr in self.__class__.__dict__.keys():
            if attr[0] != '_' and attr:
                self._attributes.append(attr)
                try:
                    setattr(self, attr, 
                        getattr(self, attr)._do_field(
                            kwargs[attr], parent=self))
                except KeyError:
                    raise AttributeError(
                        "The attribute \'{attr}\' is not present in the given parameters \'{url}\'".format(
                            attr=attr, url=self._url))

    def _check_copy(self, copy_id, cls):
        if not self._heigh:
            return False
        if copy_id == self._api_id and cls == self.__class__:
            return self
        else:
            return self._parent._check_copy(copy_id, cls)

    @classmethod
    def getAll(cls):
        for obj in json.load(cls._request()):
            new = cls(**obj)
            new._api_id = obj['id']
            yield new

    @classmethod
    def filter(cls, **kwargs):
        urlattr = "?"
        for x in kwargs.keys():
            urlattr += "{}={}&".format(x, kwargs[x])

        for obj in json.load(cls._request(urlattr=urlattr[:-1])):
            new = cls(**obj)
            new._api_id = obj['id']
            yield new

    @classmethod
    def _request(cls, method="GET", urlattr="", body="", headers={}):
        global conn
        global baseroute

        #try to get the json, if it fails, reconnect and try again, if it fails again return error
        try:
            conn.request(method, "{}{}{}".format(baseroute, cls._url, urlattr), body=body, headers=headers)
        except ConnectionRefusedError:
            conn.close()
            conn = http.HTTPConnection(ASISTENCIA['API'])
            try:
                conn.request(method, "{}{}{}".format(baseroute, cls._url, urlattr), body=body, headers=headers)
            except:
                raise socket.error("The API a host was found but is not responding to the requests")
        except socket.gaierror:
            raise socket.error("The API url is wrong or the server is not responding")

        response = conn.getresponse()
        if response.status == 404:
            raise AttributeError("The url with the requested attributes could not be found")
        #return response
        return response



class ApiModelSaveable(ApiModel):
    def __init__(self, **kwargs):
        if 'id' in kwargs.keys():
            self._api_id=kwargs['id']
        super().__init__(**kwargs)

    @classmethod
    def get(cls, rid=""):
        #get the response and then load it to return the requested object 
        info = json.load(cls._request(urlattr=""+rid))

        if isinstance(info, dict):
            return cls(**info)
        else:
            def model_iter(info):
                for obj in info:
                    yield cls(**obj)
            return model_iter(info)

    def save(self):
        global conn

        if self._api_id is None:
            method="POST"
            attr=""
        else:
            method="PUT"
            attr=str(self._api_id)

        body = {attr: getattr(self, attr) for attr in self._attributes}
        
        res = self.__class__._request(method=method, 
            urlattr=attr,
            body=json.dumps(body), 
            headers={'Content-Type':'application/json',
            'Authorization': "Basic {}".format(
                base64.urlsafe_b64encode(
                    encoding.force_bytes(
                        "{}:{}".format(settings.ASISTENCIA['user'], settings.ASISTENCIA['password']))).decode())})

        di = json.load(res)
        self._api_id = di['id']


class Field(object):
    def __init__(self, cls, is_array=False, *args):
        self.cls = cls
        self.is_array = is_array
        self.args = args

    def _do_field(self, data, parent):
        if inspect.isclass(self.cls):
            if self.is_array:
                if isinstance(data[0], self.cls):
                    return data
            else:
                if isinstance(data, self.cls):
                    return data
            if issubclass(self.cls, ApiModel):
                if self.is_array:
                    a=[]
                    for obj in data:
                        copy = parent._check_copy(obj['id'], self.cls)
                        if copy:
                            a.append(copy)
                        a.append(self.cls(_parent=parent, **obj))
                    return a
                else:
                    copy = parent._check_copy(data['id'], self.cls)
                    if copy:
                        return copy
                    return self.cls(_parent=parent, **data)
        else:
            if self.is_array:
                a=[]
                for obj in data:
                    a.append(self.cls(obj, *self.args))
                return attr
            else:
                return self.cls(data, *self.args)