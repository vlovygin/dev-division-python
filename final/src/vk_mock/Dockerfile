FROM python:3.10.4-slim-bullseye

RUN apt-get update && apt-get install -y net-tools

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app
