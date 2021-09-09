docker run --rm -it \
  -v $(pwd):/config \
  linuxserver/ffmpeg -y \
  -i /config/resources/sounds/suspense.mp3  \
  -i /config/resources/sounds/imgonnasay.mp3  \
  -i /config/resources/sounds/tickleelmo.mp3 \
  -filter_complex "aevalsrc=0:d=15[s1];[1:a]adelay=delays=2000:all=1[1a];[2:a]adelay=delays=4000:all=1[2a];[s1][0:a][1a][2a]amix=inputs=4:duration=longest" \
  /config/output.mp3
