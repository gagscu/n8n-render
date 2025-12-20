FROM jrottenberg/ffmpeg:4.4-alpine

WORKDIR /app
COPY . .

CMD ["sh","start.sh"]

