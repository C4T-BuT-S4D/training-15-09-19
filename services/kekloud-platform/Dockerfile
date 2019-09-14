FROM ubuntu:18.04

MAINTAINER @keltecc

RUN apt update && \
    apt install -y socat

RUN mkdir -p /var/kpl/

WORKDIR /var/kpl/

COPY kpl vm.so ./

ENTRYPOINT ["socat", "TCP-LISTEN:31337,reuseaddr,fork", "EXEC:./kpl"]
