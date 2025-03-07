FROM openjdk:8-jdk-alpine

RUN apk add --no-cache bash python3 py3-pip

COPY . .

# RUN wget -P /opt https://dlcdn.apache.org/spark/spark-3.5.4/spark-3.5.4-bin-hadoop3.tgz

# RUN tar -xvzf /opt/spark-3.5.4-bin-hadoop3.tgz -C /opt/

RUN ln -s /opt/spark-modules/spark-3.5.4-bin-hadoop3 /opt/spark

RUN pip3 install kafka-python

RUN export PATH=$PATH:/opt/spark/bin

ENV PATH="/opt/spark/bin:${PATH}"

ENTRYPOINT ["/entrypoint.sh"]