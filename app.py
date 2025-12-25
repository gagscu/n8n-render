import os
import threading
import uuid
import requests
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- BACKGROUND WORKER ---
def process_video(data):
    job_id = data.get('job_id')
    webhook_url = data.get('webhook_url')
    image_url = data.get('image_url')
    audio_url = data.get('audio_url')

    # Unique filenames taaki overwrite na ho
    input_image = f"img_{job_id}.jpg"
    input_audio = f"aud_{job_id}.mp3"
    output_video = f"out_{job_id}.mp4"

    try:
        print(f"[{job_id}] Downloading assets...")
        # 1. Download Files
        with open(input_image, 'wb') as f:
            f.write(requests.get(image_url).content)
        with open(input_audio, 'wb') as f:
            f.write(requests.get(audio_url).content)

        print(f"[{job_id}] Rendering video...")
        # 2. Run FFmpeg (Using subprocess is safer than os.system)
        # Note: -shortest ensure video ends when audio ends
        command = [
            'ffmpeg', '-y', '-loop', '1', '-i', input_image, '-i', input_audio,
            '-c:v', 'libx264', '-tune', 'stillimage', '-c:a', 'aac', '-b:a', '192k',
            '-pix_fmt', 'yuv420p', '-shortest', output_video
        ]
        subprocess.run(command, check=True)

        print(f"[{job_id}] Video created. Uploading...")
        
        # 3. YAHAN TERA UPLOAD LOGIC AAYEGA
        # Render Free tier file store nahi karta. Tujhe ise kahin upload karna HOGA.
        # Temporary Solution: Hum file.io (free temp storage) use kar rahe hain demo ke liye.
        with open(output_video, 'rb') as f:
            response = requests.post('https://file.io', files={'file': f})
        
        download_link = response.json().get('link')
        
        # 4. Send Success Webhook to n8n
        requests.post(webhook_url, json={
            "status": "success",
            "job_id": job_id,
            "video_link": download_link
        })

    except Exception as e:
        print(f"Error: {e}")
        # Send Failure Webhook
        if webhook_url:
            requests.post(webhook_url, json={"status": "error", "message": str(e)})

    finally:
        # 5. CLEANUP (Bahut Zaruri hai)
        for f in [input_image, input_audio, output_video]:
            if os.path.exists(f):
                os.remove(f)

# --- API ENDPOINT ---
@app.route("/render", methods=['POST'])
def start_render():
    data = request.json
    
    # Validation
    if not data or 'image_url' not in data or 'audio_url' not in data or 'webhook_url' not in data:
        return jsonify({"error": "Missing image_url, audio_url, or webhook_url"}), 400

    job_id = str(uuid.uuid4())[:8]
    data['job_id'] = job_id
    
    # Thread start kar (Non-blocking)
    thread = threading.Thread(target=process_video, args=(data,))
    thread.start()
    
    return jsonify({"message": "Processing started", "job_id": job_id}), 200

@app.route("/")
def home():
    return "Render Service is Alive"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
