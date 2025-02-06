FROM python:3.12-slim

WORKDIR /distributor

COPY requirements.txt /distributor/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /distributor/

CMD ["python3", "distributor.py"]
