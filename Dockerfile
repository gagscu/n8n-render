FROM n8nio/n8n:latest

# Switch to root to install dependencies
USER root

# Install full FFmpeg + ImageMagick + essential tools
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    sox \
    python3 \
    python3-pip \
    curl \
    git \
    wget \
    nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to n8n user
USER node

# Timezone
ENV GENERIC_TIMEZONE="Asia/Kolkata"

# Required for storage
VOLUME /home/node/.n8n
