FROM openjdk:8-jdk-alpine

RUN apk add --no-cache bash python3 py3-pip

COPY . .

# non-volume installer commands:
    # BUG | "=> ERROR [senior 4/8] RUN wget"
    #RUN wget -P /opt https://dlcdn.apache.org/spark/spark-3.5.4/spark-3.5.4-bin-hadoop3.tgz

RUN wget -P /opt https://archive.apache.org/dist/spark/spark-3.5.4/spark-3.5.4-bin-hadoop3.tgz
RUN tar -xvzf /opt/spark-3.5.4-bin-hadoop3.tgz -C /opt/

# this command was for volume version:
    #RUN ln -s /opt/spark-modules/spark-3.5.4-bin-hadoop3 /opt/spark

RUN ln -s /opt/spark-3.5.4-bin-hadoop3 /opt/spark

RUN pip3 install kafka-python

RUN export PATH=$PATH:/opt/spark/bin

ENV PATH="/opt/spark/bin:${PATH}"

ENTRYPOINT ["/entrypoint.sh"]