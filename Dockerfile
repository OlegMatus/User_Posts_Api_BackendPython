FROM python:3.13-alpine

MAINTAINER Some Dev

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.2 \
    POETRY_NO_INTERACTION=1 \
    DEBIAN_FRONTEND=noninteractive \
    COLUMNS=80

RUN apk update && apk add --no-cache \
    gcc musl-dev mariadb-dev curl ca-certificates \
    gdal gdal-dev python3-dev build-base bash libmagic geos geos-dev \
    && update-ca-certificates \

RUN pip install --no-cache-dir gdal

RUN mkdir /app
WORKDIR /app

ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV POETRY_HOME=/usr/local/poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$POETRY_HOME/bin:$PATH

COPY pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry lock
RUN poetry install