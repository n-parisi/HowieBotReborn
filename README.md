# HowieBotReborn

[![Build Status](https://travis-ci.com/n-parisi/HowieBotReborn.svg?branch=master)](https://travis-ci.com/n-parisi/HowieBotReborn)

A configurable Discord bot that serves images and sound clips. Resources can be synced from a provided
AWS S3 bucket. This bot is used in a personal Discord server and hosted on AWS. More features will be added.

The goal was to create something easily configurable and extensible. Just provide a bot token and resource files! 

### Commands

HowieBot responds to the following commands in chat:
- `!help` - Prints a help message.
- `!pic` - Display a random picture.
- `!sounds`- Prints list of all sound clips.
- `!play <clip>` - Play the specified clip. If none provided, play a random one.
- `!newclip <youtube-link> <start-time> <duration>` - Create a new sound clip from a youtube link.
- `!savefile` - Save a new clip from an attached .wav or .mp3 file.
- `!playlist <clip1> <clipN> <delaySec>` - Play a list of clips in sequence, with a delay between each.
- `!delay <clip1> <clipN> <delayMs>` - Create a new clip by playing clips in sequence, each clip starting after a delay in ms.
### Configuration

`config.yml`
-  `use_aws_resources` - If set to true, HowieBot will download resources at startup
-  `bucket_name` - The name of the S3 bucket to download resources from
-  `pics_prefix` - Location in the bucket where pic resources are located
-  `sounds_prefix` Location in the bucket where sound resources are located

Currently, resources are downloaded from S3 at startup if they don't exist locally. Future functionality could 
involve saving new resources to S3, or resyncing if new content is added to the bucket.

If you don't want HowieBot to retrieve content from AWS S3, set `use_aws_resources: false` and provide resources
locally at `resources/sounds` and `resources/pics`.

### Running

All required dependencies are provided in the [gorialis/discord.py](https://hub.docker.com/r/gorialis/discord.py/) image. This is the 
simplest way to run the bot.

```
docker run -it --rm \
   -e DISCORD_BOT_TOKEN=<your token> \
   -v "$PWD":/home/app \
   gorialis/discord.py /bin/bash -c "pip install -r requirements.txt; python -u main.py"
```

Please note you will need to configure AWS credentials if using AWS resources. For running locally, you can add 
`-e AWS_ACCESS_KEY_ID= -e AWS_SECRET_ACCESS_KEY=` with the appropriate values provided to the `docker run` command.
