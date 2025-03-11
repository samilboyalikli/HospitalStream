FROM python:3.12-slim
WORKDIR /consumer
COPY requirements.txt /consumer/
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py /consumer/
ENTRYPOINT ["sh", "-c", "sleep 10 && python3 main.py"]
