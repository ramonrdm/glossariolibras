FROM python:3.7
MAINTAINER ramon.rdm <ramon.rdm@ufsc.br>
RUN apt-get update 
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]