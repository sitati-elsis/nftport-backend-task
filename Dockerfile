FROM python:3.9.7

RUN mkdir /app
COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENV FLASK_APP=app.py

ENV FLASK_ENV=development

EXPOSE 5001:5000