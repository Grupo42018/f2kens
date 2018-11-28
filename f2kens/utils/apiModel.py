import http.client as http
import json
import socket
import base64
import itertools
import inspect
import time

from django.conf import settings
from django.utils import encoding
from django.db import models
from django import forms
from django.utils.translation import gettext_lazy as _

class APIModel(object):
    """API Model Manager

    This class takes the attributes with a Field object inside and replaces
    it with the returned value from the `_do_field`function.
    This class won't work by itself, it needs to be inhereted.
    """

    def __init__(self, _parent=None, **kwargs):
        # check if the _url attribute was set and its type
        if (not isinstance(self._url, str)):
            raise TypeError(
                "The _url variable should be set and has to be a string")

        # Set the parent and how deep is this instance to later check for copy
        # of parents and not generate duplicates of the same classes
        self._height = 0 if not _parent else _parent._height + 1
        self._parent = _parent

        # This code only runs if the inhereted class is a direct child from this
        # class. If it has another class in between it wont run
        if (self.__class__.__base__ is APIModel):
            self._api_id = kwargs['id']

        # Add the attributes to get from the api. These shoud have been added as
        # variables when this class is inherited.
        self._attributes = []
        for attr in self.__class__.__dict__.keys():
            # Any attribute that has an underscore at the beggining of its name
            # won't be modified
            if (not attr.startswith('_')
                    and attr is not None):
                self._attributes.append(attr)
                try:
                    # Replace the attributes with their values to make them directly 
                    # accesable unless they are not ApiField
                    if (isinstance(getattr(self, attr), Field)):
                        setattr(self, attr,
                                getattr(self, attr)._do_field(
                                    kwargs[attr], parent=self))
                except KeyError:
                    raise AttributeError(
                        "The attribute \'{attr}\' is not present in the given \
                        parameters \'{url}\'".format(
                            attr=attr, url=self._url))

    def _check_copy(self, copy_id, cls):
        # If the id of the requested object is the same as this instance and the
        # instance is the same as the class then its a match
        if (copy_id == self._api_id
                and cls == self.__class__):
            return self
        # If the height is 0 then there is no copy of the requested object
        if (self._height == 0):
            return False
        # Else try this instances parent
        else:
            return self._parent._check_copy(copy_id, cls)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            print(f"{other.__class__} {self.__class__}")
            return False
        return self._api_id == other._api_id

    def __str__(self):
        return str(self._api_id)

    @property
    def id(self):
        return self._api_id

    @classmethod
    def get_all(cls):
        """get_all
        This method will return a generator with all the objects in the API.
        """
        for obj in json.load(cls._request()):
            new = cls(**obj)
            new._api_id = obj['id']
            yield new

    @classmethod
    def get(cls, **kwargs):
        """get
        This function will search the api and return the first object that
        compells with the given arguments.

        Keyword Arguments:
        `**kwargs` -- The filter variables and its values
        """

        for obj in json.load(cls._request(urlattr=cls.__url_gen(kwargs))):
            new = cls(**obj)
            new._api_id = obj['id']
            return new
        raise AttributeError("The request returned None")

    @classmethod
    def filter(cls, **kwargs):
        """filter
        Used to filter the objects and return a generator with all objects that
        compel with the given arguments

        Keyword arguments:
        `**kwargs` -- The filter variables and its values
        """
        # If the id of the requested object is the same as this instance and

        for obj in json.load(
            cls._request(
                urlattr=cls.__url_gen(kwargs))):
            new = cls(**obj)
            yield new

    @classmethod
    def _request(cls, method="GET",
                 urlattr="", body="",
                 headers={}):
        """_request

        bootsraper for the request method of the HTTPConnection from the
        standard library http.client
        """

        # Create the connection
        conn = http.HTTPConnection(
            ADDR,
            port=PORT,
            timeout=TIMEOUT)

        # Make the request
        try:
            conn.request(method, "{}{}{}".format(
                         BASEPATH, cls._url, urlattr),
                         body=body, headers=headers)

        except socket.timeout as exc:
            # If the connection times out raise timeout TimeoutError
            raise TimeoutError(
                "The server {ip}:{port} is not responding".format(
                    ip=ADDR, 
                    port=PORT)) from exc
        except ConnectionRefusedError:
            # if the connection is refused try again
            conn.close()
            conn = http.HTTPConnection(ADDR, port=PORT, timeout=TIMEOUT)
            try:
                conn.request(method, "{}{}{}".format(
                             baseroute, cls._url, urlattr),
                             body=body, headers=headers)
            except ConnectionRefusedError as cre:
                # If it falils again raise a socket.error
                raise NotAHTTPServerError(
                    "A host was found but is not responding to the \
                     HTTP requests") from cre

        response = conn.getresponse()
        if response.status == 404:
            raise NotFoundError(
                "The url with the requested attributes could not be found")

        conn.close()  # Close the connection
        return response  # return response

    @staticmethod
    def __url_gen(kwargs):
        urlattr = "?"
        for x in kwargs.keys():
            if isinstance(kwargs[x], APIModel):
                urlattr += "{}={}&".format(x, kwargs[x]._api_id)
                continue
            urlattr += "{}={}&".format(x, kwargs[x])

        return urlattr[:-1]


class APIModelSaveable(APIModel):
    """API Model Manager for savable objects
    
    This class inherits from APIModel. It implements methods to save
    objects rather than just get them.
    """

    def __init__(self, **kwargs):
        # set the api_id if it was given
        self._api_id = None
        if ('id' in kwargs.keys()):
            self._api_id = kwargs['id']
        super().__init__(**kwargs)

    def save(self):
        """save
        
        This method gets the attributes and saves or updates them in the API.
        """

        # Set the method to create or update the row
        if self._api_id is None:
            method = "POST"
            attr = ""
        else:
            method = "PUT"
            attr = str(self._api_id)

        # Set the body to send and update.
        body = {attr: getattr(self, attr) for attr in self._attributes}

        # Do the request and get the response
        res = self.__class__._request(
            method=method,
            urlattr=attr,
            body=json.dumps(body),
            headers={
                'Content-Type': 'application/json',
                'Authorization': "Basic {}".format(
                    base64.urlsafe_b64encode(
                        encoding.force_bytes(
                            "{}:{}".format(
                                APICONF['user'],
                                APICONF['password']))).decode())
            }
            )

        # Read the response and set the api_id
        di = json.load(res)
        self._api_id = di['id']


class Field(object):
    """Field

    This class is used to generate the information for relations
    or other types of information. You should create instances for 
    each attribute in a APIModel class.

    Keyword arguments:
    `class_` -- the type to be created
    `is_array` -- if it should create a list or a single instance
    """
    def __init__(self, class_, is_array=False, choices={}, *args):
        self.class_ = class_
        self.is_array = is_array
        self.choices = choices
        self.args = args

    def _do_field(self, data, parent):
        if inspect.isclass(self.class_):
            if self.is_array:
                if isinstance(data[0], self.class_):
                    for i in range(len(data)):
                        data[i] = self._check_choices(data[i])
                    return data
            else:
                if isinstance(data, self.class_):
                    return self._check_choices(data)
            if issubclass(self.class_, APIModel):
                if self.is_array:
                    a = []
                    for obj in data:
                        copy = parent._check_copy(obj['id'], self.class_)
                        if copy:
                            a.append(copy)
                        a.append(self._check_choices(self.class_(_parent=parent, **obj)))
                    return a
                else:
                    copy = parent._check_copy(data['id'], self.class_)
                    if copy:
                        return copy
                    return self._check_choices(self.class_(_parent=parent, **data))
        else:
            if self.is_array:
                a = []
                for obj in data:
                    a.append(self._check_choices(self.class_(obj, *self.args)))
                return attr
            else:
                return self._check_choices(self.class_(data, *self.args))

    def _check_choices(self, value):
        try:
            return self.choices[value]
        except:
            return value


class ApiField(models.Field):
    """ApiField

    Custom Django Field to load the objects in the models and to save them
    in the database
    """
    description = _("ApiIdentifier")

    def __init__(self, class_, *args, **kwargs):
        self.class_ = class_
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.class_.get(id=value)

    def to_python(self, value):
        if isinstance(value, APIModel):
            return value

        if value is None:
            return value

        return self.class_.get(id=value)

    def get_internal_type(self):
        return "IntegerField"

    def get_prep_value(self, value):
        if not isinstance(value, self.class_):
            raise AttributeError(
                "The value passed is a {type} instead of {need}".format(
                    type=value.__class__, need=self.class_))
        return value._api_id

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['class_'] = self.class_
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': forms.IntegerField,
            **kwargs,
        })

    def db_type(self, connection):
        return 'INTEGER'



# Exceptions

# TODO: Create more expetion for more specific error handling
class NotFoundError(Exception):
    pass

class TimeoutError(Exception):
    pass

class NotAHTTPServerError(Exception):
    pass


# Set the required configuration
try:
    APICONF = settings.ASISTENCIA
    ADDR = APICONF['API']
    USER = APICONF['USER']
    PASS = APICONF['PASS']
except AttributeError as exc:
    raise AttributeError(
        "Please set the API configuration in settings") from exc
except KeyError as exc:
    attr = str(exc).split("'")[1]
    raise AttributeError(
        "Please set the attribute {attr} in the configuration".format(
            attr=attr)) from exc

# Set the defaultable configuration
if (':' in ADDR):
    PORT = None
elif ('PORT' in APICONF.keys()):
    PORT = APICONF['PORT']
else:
    PORT = 80                     # Default to 80 if no config is found

if ('TIMEOUT' in APICONF.keys()):
    TIMEOUT = APICONF['TIMEOUT']
else:
    TIMEOUT = 10                  # Default to 10s 

if ('BASEPATH' in APICONF.keys()):
    BASEPATH = APICONF['BASEPATH']
else:
    BASEPATH = '/'               # Defaults to the root of the url

# check if the connection works. I do this by checking the base route
# of the api with a HEAD method
conn = http.HTTPConnection(ADDR, port=PORT, timeout=TIMEOUT)

try:
    conn.request("HEAD", BASEPATH)
except socket.timeout as exc:
    # If the connection times out raise timeout TimeoutError
    raise TimeoutError(
        "The server {ip}:{port} is not responding".format(
            ip=ADDR, 
            port=PORT)) from exc
except ConnectionRefusedError:
    # if the connection is refused try again
    conn.close()
    conn = http.HTTPConnection(ADDR, port=PORT, timeout=TIMEOUT)
    try:
        conn.request("HEAD", BASEPATH)
    except ConnectionRefusedError as cre:
        # If it fails again the server is not HTTP
        raise NotAHTTPServerError(
            "A host was found but is not responding to the HTTP requests") from cre

# If the connection gives a 404 back then its not the server or the
# path we are looking for
res = conn.getresponse()
if res.status == 404:
    raise NotFoundError(
        "The API route set hasn't been found in the selected API host")

