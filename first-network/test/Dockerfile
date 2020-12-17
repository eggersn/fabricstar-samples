FROM gradle:5.3.0-jdk-alpine
COPY kafka-star-java-consumer /usr/local/kafka-star-java-consumer
WORKDIR /usr/local/kafka-star-java-consumer
ENTRYPOINT ["gradle", "run"]
