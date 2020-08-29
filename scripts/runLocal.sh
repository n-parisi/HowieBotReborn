docker run -it --rm \
  -e DISCORD_BOT_TOKEN=NzQ1NDU4ODkxMjM5NzE4OTU0.XzyEsQ.1dWaIT_m9ZMgCNuqtFurQbnOwR8 \
  -v "$PWD":/home/app \
  nickparisi/howiebot:latest python3 -u main.py

