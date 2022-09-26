import json

from redis import Redis


def save_dict(key, value):
    r = Redis(decode_responses=True)
    r.set(name=key, value=json.dumps(value))


def get_data(key):
    r = Redis(decode_responses=True)
    return r.get(name=key)


def delete_data(key):
    r = Redis(decode_responses=True)
    r.delete(key)
