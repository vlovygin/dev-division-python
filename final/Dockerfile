FROM python:3.10.4-slim-bullseye

WORKDIR /main

ENV PYTHONPATH="/main"

COPY requirements.txt /main
RUN python3 -m pip install -r requirements.txt
