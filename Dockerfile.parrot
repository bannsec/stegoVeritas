FROM parrotsec/core

ARG DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]

# parrot is SUPER jank. 404s, somehow reruning it works sometimes. who knows. it's shit.
RUN apt update && apt full-upgrade && \
    apt install -y python3 python3-pip python3-venv && \
    python3 -m venv /opt/stegoveritas_venv && \
    source /opt/stegoveritas_venv/bin/activate && \
    python3 -m pip install -U setuptools pip && \
    useradd -m -s /bin/bash stegoveritas && \
    mkdir -p /opt

COPY --chown=stegoveritas:stegoveritas . /opt/stegoveritas/

RUN source /opt/stegoveritas_venv/bin/activate && \
    cd /opt/stegoveritas && pip3 install -e .[dev] && \
    stegoveritas_install_deps && \
    echo "source /opt/stegoveritas_venv/bin/activate" >> /home/stegoveritas/.bashrc && \
    chown -R stegoveritas:stegoveritas /opt/stegoveritas_venv

WORKDIR /home/stegoveritas
USER stegoveritas
