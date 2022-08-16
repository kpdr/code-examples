import re
from functools import wraps
from typing import Dict, Tuple

import flask
from google.auth.transport import requests
from google.oauth2 import id_token

from example_backend.exc.bad_request import BadRequest
from example_backend.users import dao
from example_backend.users.dao import User

AUTH_HEADER_PAT = re.compile(r"^Bearer (?P<token>.*)$")
CLIENT_ID = "362134854545-t9ni0g6vtl1igvv2gmk8ehjk5tr315p4.apps.googleusercontent.com"
MISSING_MESSAGE = "Authorization header is required"
MALFORMED_MESSAGE = "Authorization header malformed, value must be 'Bearer <jwt token>`"


def verify_token(token: str) -> Dict:
    request = requests.Request()
    return id_token.verify_oauth2_token(token, request, CLIENT_ID)


def _resolve_user(token: str) -> Tuple[User, Dict]:
    id_info = verify_token(token)
    user = dao.find_by_email(id_info["email"])
    if not user:
        user = dao.insert(id_info["email"], id_info["name"])
    return user, id_info


def resolve_user() -> Tuple[User, Dict]:
    """
    Resolve a User from the request, if the User is new it is persisted as well
    """
    if "Authorization" not in flask.request.headers:
        raise BadRequest(MISSING_MESSAGE)

    auth_header = flask.request.headers["Authorization"]
    m = AUTH_HEADER_PAT.match(auth_header)
    if not m:
        raise BadRequest(MALFORMED_MESSAGE)

    try:
        return _resolve_user(m.group("token"))
    except ValueError as e:
        raise BadRequest(str(e))


def auth_required(inject_user=False, inject_id_info=False):
    """
    A decorator that resolves a User and optionally injects it into the decorated function
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user, id_info = resolve_user()
            if inject_user:
                kwargs["user"] = user
            if inject_id_info:
                kwargs["id_info"] = id_info
            return f(*args, **kwargs)

        return decorated_function

    return decorator
