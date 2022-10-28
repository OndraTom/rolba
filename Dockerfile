FROM python:3.11.0-slim

MAINTAINER Ondrej Tom <info@ondratom.cz>

COPY ./requirements.txt /requirements.txt

RUN pip3 install --upgrade -r /requirements.txt

COPY . /app

WORKDIR /app

CMD ["python3", "run.py"]