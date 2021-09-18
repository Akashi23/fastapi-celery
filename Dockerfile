FROM python:3.7-slim

LABEL maintainer="Daniar <dan.zh.1999@gmail.com>"

ENV DOCKER=true

COPY pyproject.toml .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry install

EXPOSE 8000