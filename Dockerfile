FROM python:3.9-alpine3.13
LABEL maintainer='Irina'

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000
