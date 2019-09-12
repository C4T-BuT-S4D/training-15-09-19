from functools import wraps
from flask import request, abort, session
from keklib import processing


def with_allowed_methods(methods):
    def with_methods_wrapper(func):
        @wraps(func)
        def real_wrapper(*args, **kwargs):
            method = processing.decode_method(request)
            if method not in methods:
                abort(405)
            return func(*args, **kwargs)
        return real_wrapper

    return with_methods_wrapper


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('id') is None:
            abort(403)
        return func(*args, **kwargs)

    return wrapper
