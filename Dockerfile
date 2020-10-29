FROM python:3.7
LABEL maintainer="ramon.rdm@ufsc.br"
ENV PYTHONUNBUFFERED 0

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg nano htop
RUN pip install --upgrade pip

WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt

EXPOSE 8000