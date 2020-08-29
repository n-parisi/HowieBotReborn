#!/usr/bin/env bash

# Sync resources from AWS
# Will likely remove this
aws s3 sync s3://nparisi-bucket/resources resources/

# Build docker image
docker build -t nickparisi/howiebot -f ~/dev/HowieBotReborn/Dockerfile .

# Publish to docker hub
docker login docker.io
docker push nickparisi/howiebot