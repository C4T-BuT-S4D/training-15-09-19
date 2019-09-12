#!/bin/sh

set +e

cd /app || exit

sleep 5

gunicorn -b 0.0.0.0 --worker-class gevent --worker-connections 1024 app:app
#python app.py