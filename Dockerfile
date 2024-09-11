FROM python:3.9-alpine3.13
LABEL maintainer="Irina"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8001

ARG DEV=false
RUN apk update && \
    apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    cmake \
    flac \
    libstdc++ \
    build-base

# Экспортируем пути для компиляторов
ENV CC=/usr/bin/gcc \
    CXX=/usr/bin/g++

# Создаем виртуальное окружение и устанавливаем зависимости
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    /py/bin/pip install pocketsphinx && \
    if [ "$DEV" = 'true' ]; then /py/bin/pip install -r /tmp/requirements.dev.txt; fi && \
    rm -rf /tmp

ENV PATH="/py/bin:$PATH"
