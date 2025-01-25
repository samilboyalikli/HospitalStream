FROM python:3.12-slim

WORKDIR /hospitals

COPY requirements.txt /hospitals/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /hospitals/
