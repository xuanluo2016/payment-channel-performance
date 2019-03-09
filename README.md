# Kafka Ethereum Transaction Time and Gas Cost Analyzer

[![Kafka](https://img.shields.io/badge/streaming_platform-kafka-black.svg?style=flat-square)](https://kafka.apache.org)
[![Docker Images](https://img.shields.io/badge/docker_images-confluent-orange.svg?style=flat-square)](https://github.com/confluentinc/cp-docker-images)
[![Python](https://img.shields.io/badge/python-3.5+-blue.svg?style=flat-square)](https://www.python.org)

## Install

This system is fully containerised. You will need [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/) to run it.

You simply need to create a Docker network called `kafka-network` to enable communication between the Kafka cluster and the apps:

```bash
$ docker network create kafka-network
```

All set!

## Quickstart

- Spin up the local single-node Kafka cluster (will run in the background):

```bash
$ docker-compose -f docker-compose.kafka.yml up -d
```

- Check the cluster is up and running (wait for "started" to show up):

```bash
$ docker-compose -f docker-compose.kafka.yml logs -f broker | grep "started"
```

- Start the transaction generator and detector (will run in the background):

```bash
$ docker-compose up -d
```

## Usage

Show a stream of transactions in the topic `T` (optionally add `--from-beginning`):

```bash
$ docker-compose -f docker-compose.kafka.yml exec kafka-console-consumer --bootstrap-server localhost:9092 --topic T
```

Topics:

- `queuing.transactions`: raw generated transactions
- `streaming.transactions.mined`: transactions have been mined in Ethereum
- `streaming.transactions.unmined`: pending transactions

Example transaction message:

```json
```

## Teardown

To stop the transaction generator and detector:

```bash
$ docker-compose down
```

To stop the Kafka cluster (use `down`  instead to also remove contents of the topics):

```bash
$ docker-compose -f docker-compose.kafka.yml stop
```

To remove the Docker network:

```bash
$ docker network rm kafka-network
```
