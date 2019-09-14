FROM golang:1.12-alpine

MAINTAINER tg: @kekov

RUN apk update && apk add git gcc musl-dev

ADD ./go.mod /app/go.mod
ADD ./go.sum /app/go.sum

WORKDIR /app

RUN go get

ADD . /app

RUN go build .

ENTRYPOINT ["./kekustotal"]