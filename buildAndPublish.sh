#!/usr/bin/env bash

# Sync resources from AWS
aws s3 sync s3://nparisi-bucket/resources resources/

# Build docker image
docker build -t howiebot .
docker tag howiebot nickparisi/howiebot

# Publish to docker hub
docker login docker.io
docker push nickparisi/howiebot