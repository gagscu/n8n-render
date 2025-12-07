FROM n8nio/n8n:latest

# Install FFmpeg
USER root
RUN apt-get update && apt-get install -y ffmpeg
USER node

ENV GENERIC_TIMEZONE="Asia/Kolkata"

VOLUME /home/node/.n8n
