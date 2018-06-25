import hashlib
import time

def generate_token(device_hash):
    if len(device_hash) != 128:
        raise AttributeError(
            "The device hash is not a valid sha-512 hash")
    h = hashlib.sha512()
    h.update(str(time.time()).encode('utf-8'))
    h.update(device_hash.encode('utf-8'))
    return h.hexdigest()