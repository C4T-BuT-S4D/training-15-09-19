import base64
from flask import abort


def decode_method(request):
    try:
        encoded_method = request.method
        encoded_method += '=' * (-len(encoded_method) % 8)
        method = base64.b32decode(encoded_method).decode()
    except Exception as e:
        abort(400)
    else:
        return method
