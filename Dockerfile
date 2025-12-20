FROM jrottenberg/ffmpeg:4.4-alpine

WORKDIR /app
COPY . .

RUN chmod +x start.sh

CMD ["sh", "start.sh"]

