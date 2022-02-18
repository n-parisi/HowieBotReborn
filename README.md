# HowieBotReborn

A configurable Discord bot that serves images and sound clips. Resources can be synced from a provided
AWS S3 bucket. A .json file is used with the `TinyDB` library to create a small DB for tracking play stats and other simple data.
This bot is used in a personal Discord server. 

The goal was to create something easily configurable and extensible. Just provide a bot token and resource files! 

### Commands

HowieBot responds to the following commands in chat:
- `!help` - Prints a help message.
- `!pic` - Display a random picture.
- `!clips <search>`- Prints list of all sound clips, or just the ones that contain the optional search term.
- `!play <clip>` - Play the specified clip. If none provided, play a random one.
- `!newclip <youtube-link>, <start-time>, <duration>` - Create a new sound clip from a youtube link.
- `!playlist <clip1>, <clipN>, <delaySec>` - Play a list of clips in sequence, with a delay between each. **(Note: Currently broken)**
- `!player` - Creates a player that can be continually reacted to in order to keep playing random clips.
- `!stats <X>` - Displays the top X most played clips.
- `!stats <clip>` - Displays how many times a clip has been played.
- `!savefile` - Save a new clip from an attached .wav or .mp3 file.
- `!resync` - If using AWS resources, deletes all cips and redownloads from source.
- `!unstuck` - Disconnects all active voice clients. Can be useful for fixing a stuck bot, or stopping a clip early.
- `!exportAll` - Exports the db.json file into a CSV file for statistical analysis.

##### Delay

You can create a new clips by overlaying existing clips on top of each other. Then you can save those as new clips.
The possibilities are endless! Substitute any clip with the word `random` to get a random clip.

- `!delay <clip1>, <clipN>, <delayMs>` - Create a new clip by playing clips in sequence, each clip starting after a delay in ms.
- `!delay <clip1>, <delay1Ms>, <clip2>, <delay2Ms>, <clipN>` - Specify a different delay after each clip for more precision.
- `!newmacro <macroName>, <delayParams>` - Save a macro of any way you would use `!delay`. This is useful if you want to save a `!delay` sequence
with the `randoms` left unresolved until the macro is actually played.
- `!showmacro <macroName>` - Show what a macro resolves to
- `!macro <macroName>` - Play a macro.


##### Wagers

A system was created to allow placing 'wagers' on when a certain clip will play next, and to buy stock that rewards the user
whenever that clip plays. Everything is tracked through the local DB. This system is just for fun and all money is fake! 

The first time a user places a wager, an account will be created for that user with $100.

- `!wager <$X>, <clipName>, <attempts>` - Place a wager that given clip will play within some number of attempts. 
Less attempts means a higher payout!
- `!wagers <username>` - Show all active wagers, optionally filter by username.
- `!bucks` - Show how many HowieBucks all users have.
- `!winners <X>` - Show the last X number of winners.
- `!winners <username> <X>` - Show the last X wins for a user.
- `!tip <amount>` - Tip HowieBot some of your HowieBucks! This serves no purpose other than feeding superstition :)
- `!tip <amount> <user_mention>` - Tip another user, denoted by a Discord mention.
- '!tippers - Shows the amount each user has tipped HowieBot.
- `!freemoney <amount> <user>` - Give every user in the system some amount of money, or denote a specific user by their
unique discord id. Note: This command can only be used by the admin specified in the config file.
- `!buystock <clip>` - Buy a share of a clip for $200. When that clip plays, shareholders are paid $10 per share.
- `!portfolio <username>` - Show stocks owned by a user, or call with no username to show own portfolio.
- '!payout <clip> - Shows the amount a clip has paid out in wagers and stocks.

### Configuration

`config.yml`
- `use_aws_resources` - If set to true, HowieBot will download resources at startup
- `bucket_name` - The name of the S3 bucket to download resources from
- `pics_prefix` - Location in the bucket where pic resources are located
- `sounds_prefix` - Location in the bucket where sound resources are located
- `allow_savefile` - Allow the `!savefile` command. Will allow saving of any .mp3 or .wav. Be careful!
- `admin_id` - Unique discord id of the 'admin'. This is the person allowed to use the `!freemoney` command.

Resources are downloaded from S3 at startup if they don't exist locally. When new clips are created, they are saved to S3.

If you don't want HowieBot to retrieve content from AWS S3, set `use_aws_resources: false` and provide resources
locally at `resources/sounds` and `resources/pics`.

### Running

Many of the required dependencies are provided in the [gorialis/discord.py](https://hub.docker.com/r/gorialis/discord.py/) image.
The simplest way to run the bot is to create a base image with the included Dockerfile:

```
docker build -t howiebot .
```

Then use this image to run the bot (see `runLocal.sh`):

```
docker run -it --rm \
   -e DISCORD_BOT_TOKEN=$DISCORD_BOT_TOKEN \
   -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
   -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
   -e BUILD_ID=local-docker \
   -v "$PWD":/app \
   howiebot
```

Please note you will need to configure AWS credentials if using AWS resources. If not, you can remove the AWS
environment variables. 

Putting it all together, you can run the bot with docker-compose like this:

```
  howiebot:
    build: path/to/bot/repository
    container_name: howiebot
    volumes:
      - path/to/bot/repository:/app
    environment:
      - DISCORD_BOT_TOKEN=
      - AWS_ACCESS_KEY_ID=
      - AWS_SECRET_ACCESS_KEY=
      - BUILD_ID=remote-docker
```
