import os

cmd = (
    "ffmpeg -y "
    "-loop 1 -i image.jpg "
    "-i audio.mp3 "
    "-c:v libx264 "
    "-tune stillimage "
    "-c:a aac "
    "-b:a 128k "
    "-pix_fmt yuv420p "
    "-shortest "
    "output.mp4"
)

print("Running FFmpeg...")
os.system(cmd)

if os.path.exists("output.mp4"):
    print("✅ Video created successfully")
else:
    print("❌ Video creation failed")
    
