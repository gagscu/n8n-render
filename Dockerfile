FROM jrottenberg/ffmpeg:4.4-alpine

WORKDIR /app

RUN apk add --no-cache python3 py3-pip
RUN pip install flask

COPY . .

ENTRYPOINT ["python3", "app.py"]

