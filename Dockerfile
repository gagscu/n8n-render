FROM jrottenberg/ffmpeg:4.4-alpine

WORKDIR /app
COPY . .

CMD ["python", "main.py"]
