docker run -it --rm \
   -e DISCORD_BOT_TOKEN=$DISCORD_BOT_TOKEN \
   -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
   -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
   -e BUILD_ID=local-docker \
   -v "$PWD":/app \
   howiebot