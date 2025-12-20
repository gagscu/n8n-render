import os

cmd = """
ffmpeg -y \
-loop 1 -i image.jpg \
-i audio.mp3 \
-c:v libx264 \
-tune stillimage \
-c:a aac \
-b:a 128k \
-pix_fmt yuv420p \
-shortest \
output.mp4
"""

os.system(cmd)
print("Video created: output.mp4")
