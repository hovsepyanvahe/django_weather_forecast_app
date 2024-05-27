FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/share/man/man1 \
    && apt-get update \
    && apt-get -y dist-upgrade \
    && apt-get -y install --no-install-recommends \
        python3 \
        python3-dev \
        python3-pip \
        python3-setuptools \
        python3-wheel \
        build-essential \
        curl \
        swig \
        libmariadb3 \
        libmariadb-dev-compat \
        libssl1.1 \
        libssl-dev \
        libcairo2 \
        libpango1.0 \
        libmagic1 \
        libxml2 \
        libxml2-dev \
        libxmlsec1 \
        libxmlsec1-openssl \
        libxmlsec1-dev \
        openjdk-11-jre-headless \
        git \
        xmlsec1 \
        zlib1g-dev \
        libncurses5-dev\
        libgdbm-dev \
        libnss3-dev \
        libssl-dev \
        libsqlite3-dev \
        libreadline-dev \
        libffi-dev \
        curl \
        libbz2-dev \
        libpq-dev \
    && apt-get -y autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt requirements.txt
RUN /usr/local/bin/python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

COPY . /app
COPY ./docker /docker

RUN chmod +x /docker/start.sh

CMD ["/docker/start.sh"]
