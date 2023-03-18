FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sudo \
    curl \
    wget\
    git \
    vim \
    pbzip2 \
    ca-certificates

RUN ln -s /usr/bin/python3.8 /usr/bin/python
RUN ln -s /usr/bin/python3.8 /usr/bin/python3

WORKDIR /code

COPY python python
COPY docker_scripts docker_scripts

RUN ./docker_scripts/install_python.sh