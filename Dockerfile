FROM gorialis/discord.py:3.8.5-buster-master-minimal

# Copy source code
COPY pkg/ pkg/
COPY main.py main.py
COPY requirements.txt requirements.txt
COPY config.yml config.yml

# Install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Start bot
CMD python -u main.py
