from app import app
from keklib.rendering import render_template
from flask import request
import pickle
import base64


@app.errorhandler(400)
def bad_request(e):
    dumped_cookies = pickle.dumps(request.cookies)
    return render_template(
        '400.html',
        referer=request.headers.get('Referer'),
        page=request.url,
        cookies=base64.b64encode(dumped_cookies).decode(),
        error=e,
    ), 400


@app.errorhandler(401)
def not_authorized(_e):
    dumped_cookies = pickle.dumps(request.cookies)
    return render_template(
        '401.html',
        referer=request.headers.get('Referer'),
        page=request.url,
        cookies=base64.b64encode(dumped_cookies).decode(),
    ), 401


@app.errorhandler(403)
def access_denied(_e):
    dumped_cookies = pickle.dumps(request.cookies)
    return render_template(
        '403.html',
        referer=request.headers.get('Referer'),
        page=request.url,
        cookies=base64.b64encode(dumped_cookies).decode(),
    ), 403


@app.errorhandler(404)
def page_not_found(_e):
    dumped_cookies = pickle.dumps(request.cookies)
    return render_template(
        '404.html',
        referer=request.headers.get('Referer'),
        page=request.url,
        cookies=base64.b64encode(dumped_cookies).decode(),
    ), 404


@app.errorhandler(405)
def method_not_allowed(_e):
    dumped_cookies = pickle.dumps(request.cookies)
    return render_template(
        '405.html',
        referer=request.headers.get('Referer'),
        page=request.url,
        cookies=base64.b64encode(dumped_cookies).decode(),
        method=request.method,
    ), 405


@app.errorhandler(500)
def bad_request(e):
    dumped_cookies = pickle.dumps(request.cookies)
    return render_template(
        '500.html',
        referer=request.headers.get('Referer'),
        page=request.url,
        cookies=base64.b64encode(dumped_cookies).decode(),
        error=e,
    ), 500