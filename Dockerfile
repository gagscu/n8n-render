FROM n8nio/n8n:latest

USER root

# Install ffmpeg (Alpine package)
RUN apk update && apk add --no-cache \
    ffmpeg \
    imagemagick \
    curl \
    bash \
    git

USER node

ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=https

EXPOSE 5678

CMD ["n8n"]
