FROM python:3.12.3-slim-bookworm

WORKDIR /

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONBUFFERED 1 

RUN apt-get update \ 
    && apt-get -y install netcat-openbsd gcc postgresql \ 
    && apt-get clean 

RUN pip install --upgrade pip 
COPY ./requirements.txt /requirements.txt 

RUN pip install -r requirements.txt 

COPY . /
