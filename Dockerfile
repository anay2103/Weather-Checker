FROM python:3.9-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

ARG PIPENV_FLAGS

EXPOSE 80
WORKDIR /app

RUN set -ex &&  apt update && apt upgrade -y \
    && apt -y install libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/* 

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv

RUN pipenv install --system ${PIPENV_FLAGS}

COPY . /app/