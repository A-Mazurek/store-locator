FROM python:3.8

COPY store_locator /app

WORKDIR /app

COPY store_locator/requirements.txt requirements.txt

RUN pip install -r requirements.txt
