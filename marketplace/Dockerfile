FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY ./req.txt /usr/src/app/req.txt
RUN pip install -r /usr/src/app/req.txt

COPY . /usr/src/app

EXPOSE 8000
