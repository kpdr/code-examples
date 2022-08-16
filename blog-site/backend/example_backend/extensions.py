import functools

from flask import jsonify
from flask_alchemydumps import AlchemyDumps
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
alchemydumps = AlchemyDumps()


def serialize(obj):
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    return obj


def as_json(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        obj = func(*args, **kwargs)
        if type(obj) == list:
            return jsonify([serialize(o) for o in obj])
        elif type(obj) == dict:
            for k, v in obj.items():
                obj[k] = serialize(v)
            return jsonify(obj)
        return jsonify(serialize(obj))

    return wrapper
