#!/bin/bash

set -ex

docker build -f base.Dockerfile -t rentme-py-base .

# cd ..; docker-compose pull; docker-compose build

cd ..; docker-compose build django-init; docker-compose up django-init
