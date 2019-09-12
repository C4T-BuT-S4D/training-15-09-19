FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1

RUN apk add gcc musl-dev
RUN apk add mariadb-dev build-base
RUN pip install gunicorn gevent

ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ADD ./ /app

CMD ["/entrypoint.sh"]