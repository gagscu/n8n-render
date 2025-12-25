import os
import threading
import uuid
import requests
import subprocess
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_audio_duration(audio_path):
    """Audio ki length second mein nikalta hai"""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

def process_video_slideshow(data):
    job_id = data.get('job_id')
    webhook_url = data.get('webhook_url')
    image_urls = data.get('image_urls') # Note: Ye ab List hai, single URL nahi
    audio_url = data.get('audio_url')

    work_dir = f"job_{job_id}"
    os.makedirs(work_dir, exist_ok=True)
    
    input_audio = os.path.join(work_dir, "audio.mp3")
    output_video = f"out_{job_id}.mp4"
    concat_file = os.path.join(work_dir, "inputs.txt")

    try:
        print(f"[{job_id}] Downloading assets...")
        
        # 1. Download Audio
        with open(input_audio, 'wb') as f:
            f.write(requests.get(audio_url).content)
        
        # 2. Get Duration & Calculate Time Per Image
        audio_duration = get_audio_duration(input_audio)
        num_images = len(image_urls)
        duration_per_image = audio_duration / num_images
        print(f"[{job_id}] Audio: {audio_duration}s, Images: {num_images}, Each Image: {duration_per_image}s")

        # 3. Download Images & Create Concat File
        # Format:
        # file 'img1.jpg'
        # duration 5.0
        # file 'img2.jpg'
        # duration 5.0
        
        image_files = []
        with open(concat_file, 'w') as f:
            for i, url in enumerate(image_urls):
                img_name = os.path.join(work_dir, f"img_{i}.jpg")
                with open(img_name, 'wb') as img_file:
                    img_file.write(requests.get(url).content)
                image_files.append(img_name)
                
                # Write to concat list
                # Note: File path must be safe inside txt
                f.write(f"file 'img_{i}.jpg'\n")
                f.write(f"duration {duration_per_image}\n")
            
            # Last image ko repeat karna padta hai FFmpeg bug fix ke liye
            f.write(f"file 'img_{num_images-1}.jpg'\n")

        print(f"[{job_id}] Rendering Slideshow...")
        
        # 4. Run FFmpeg with Concat Demuxer
        # -f concat: Text file se list padhega
        # -vsync vfr: Video sync issues rokne ke liye
        command = [
            'ffmpeg', '-y', 
            '-f', 'concat', '-safe', '0', '-i', concat_file, 
            '-i', input_audio,
            '-c:v', 'libx264', '-r', '30', '-pix_fmt', 'yuv420p', 
            '-c:a', 'aac', '-b:a', '192k', 
            '-shortest', # Video audio ke saath khatam hogi
            output_video
        ]
        
        subprocess.run(command, check=True, cwd=work_dir) # cwd is important here

        print(f"[{job_id}] Uploading...")
        
        # 5. Upload to file.io (Temp Storage)
        with open(output_video, 'rb') as f:
            response = requests.post('https://file.io', files={'file': f})
        
        download_link = response.json().get('link')
        
        # 6. Notify n8n
        requests.post(webhook_url, json={
            "status": "success",
            "job_id": job_id,
            "video_link": download_link
        })

    except Exception as e:
        print(f"Error: {e}")
        if webhook_url:
            requests.post(webhook_url, json={"status": "error", "message": str(e)})

    finally:
        # 7. CLEANUP (Folder uda do)
        import shutil
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)
        if os.path.exists(output_video):
            os.remove(output_video)

@app.route("/render", methods=['POST'])
def start_render():
    data = request.json
    # Basic Validation
    if not data or 'image_urls' not in data or 'audio_url' not in data:
        return jsonify({"error": "Missing image_urls (list) or audio_url"}), 400

    job_id = str(uuid.uuid4())[:8]
    data['job_id'] = job_id
    
    thread = threading.Thread(target=process_video_slideshow, args=(data,))
    thread.start()
    
    return jsonify({"message": "Slideshow processing started", "job_id": job_id}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
