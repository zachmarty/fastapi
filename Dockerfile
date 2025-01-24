FROM python:3.11-slim

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt

