FROM python:3.9.1

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libmagic-dev

RUN mkdir /app

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

