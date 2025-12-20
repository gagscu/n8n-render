FROM jrottenberg/ffmpeg:4.4-alpine

WORKDIR /app

RUN apk add --no-cache python3 py3-pip

COPY . .

RUN chmod +x start.sh

CMD ["./start.sh"]

