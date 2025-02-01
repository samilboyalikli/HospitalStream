FROM python:3.12-slim
WORKDIR /consumer
COPY requirements.txt /consumer/
RUN pip install --no-cache-dir -r requirements.txt
COPY consumer.py /consumer/
CMD ["python3", "consumer.py"]
