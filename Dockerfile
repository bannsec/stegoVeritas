FROM ubuntu:bionic

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt dist-upgrade -y && \
    apt install -y python3 python3-pip python3-venv && \
    useradd -m -s /bin/bash stegoveritas && \
    mkdir -p /opt

COPY --chown=stegoveritas:stegoveritas . /opt/stegoveritas/

RUN cd /opt/stegoveritas && pip3 install -e .[dev] && \
    stegoveritas_install_deps

WORKDIR /home/stegoveritas
USER stegoveritas
