#!/bin/sh
set -e

echo "Starting video render..."

# create video (ONE TIME)
ffmpeg -y \
-loop 1 -i image.jpg \
-i audio.mp3 \
-c:v libx264 -tune stillimage \
-c:a aac -b:a 192k \
-shortest \
-pix_fmt yuv420p \
output.mp4

echo "Video created. Keeping container alive..."

# keep Render alive
python3 -m http.server 10000
