FROM python:3.8-slim-buster
WORKDIR app/

# Install dependencies
RUN apt-get -y update
RUN apt-get -y install libffi-dev libnacl-dev python3-dev ffmpeg

# Copy source / resources
COPY pkg/ pkg/
COPY resources/ resources/
COPY main.py main.py
COPY requirements.txt .

# Install python requirements
RUN pip3 install -r requirements.txt

# Start bot
ENTRYPOINT python3 -u main.py