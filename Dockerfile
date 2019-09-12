FROM python:3.7
MAINTAINER ramon.rdm <ramon.rdm@ufsc.br>


RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y ffmpeg
RUN pip install --upgrade pip
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
#RUN python3 manage.py migrate && python3 manage.py collectstatic --noinput

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]