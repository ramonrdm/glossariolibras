# Builder
FROM python:3.8-slim-buster as builder
LABEL maintainer="ramon.rdm@ufsc.br"
ENV PYTHONUNBUFFERED 0

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg nano htop
RUN pip install --upgrade pip

WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt