FROM python:3.8-slim-buster

RUN useradd howie

WORKDIR /home/app

# Install system dependencies
RUN apt-get -y update
RUN apt-get -y install libffi-dev libnacl-dev python3-dev ffmpeg

# Install python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Switch to non-root user
USER howie