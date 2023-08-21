FROM python:3.9-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip==21.0.0

RUN pip install --no-cache-dir --upgrade --upgrade-strategy=eager -r requirements.txt

COPY . /app
WORKDIR /app

ENV PATH /app:$PATH

USER root

RUN chmod -R 777 .