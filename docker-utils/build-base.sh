#!/bin/sh

docker build --pull -f base.Dockerfile -t rentme-py-base .

docker image pull postgres
docker image pull rabbitmq:management
