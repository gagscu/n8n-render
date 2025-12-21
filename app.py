import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Server alive"

@app.route("/render")
def render():
    os.system(
        "ffmpeg -y -loop 1 -i image.jpg -i audio.mp3 "
        "-c:v libx264 -tune stillimage "
        "-c:a aac -shortest -pix_fmt yuv420p output.mp4"
    )
    return "Video created"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
  
