FROM parrotsec/core

ARG DEBIAN_FRONTEND=noninteractive

# parrot is SUPER jank. 404s, somehow reruning it works sometimes. who knows. it's shit.
RUN apt update && parrot-upgrade && \
    apt install -y python3 python3-pip python3-venv && \
    python3 -m pip install -U setuptools pip && \
    useradd -m -s /bin/bash stegoveritas && \
    mkdir -p /opt

COPY --chown=stegoveritas:stegoveritas . /opt/stegoveritas/

RUN cd /opt/stegoveritas && pip3 install -e .[dev] && \
    stegoveritas_install_deps

WORKDIR /home/stegoveritas
USER stegoveritas
