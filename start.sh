#!/usr/bin/env bash

aws s3 sync s3://nparisi-bucket/resources resources/
export DISCORD_BOT_TOKEN="NzQ1NDU4ODkxMjM5NzE4OTU0.XzyEsQ.HImP1b6cKLjrE_4-CEFcapkBrb8"
python bot.py