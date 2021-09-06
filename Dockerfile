FROM gorialis/discord.py:3.8.5-buster-master-minimal

# Install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Start bot
CMD python -u main.py
