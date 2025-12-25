# 1. Base Image: Python Slim (Stable & Fast)
FROM python:3.9-slim

# 2. System Level pe FFmpeg install kar (Ye sabse crucial step hai)
# 'rm -rf' karna zaruri hai taaki image ka size chhota rahe (Render Free tier loves small images)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# 3. Work Directory set kar
WORKDIR /app

# 4. Dependencies copy aur install kar
# Pehle requirements copy karte hain taaki Docker cache use kar sake
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Baaki code copy kar
COPY . .

# 6. Gunicorn use kar (Ye Production Server hai)
# -w 1: Sirf 1 Worker (Kyunki 512MB RAM hai, zyada worker = Crash)
# --timeout 120: Taaki FFmpeg agar time le toh server band na ho jaye
CMD ["gunicorn", "-w", "1", "--timeout", "120", "-b", "0.0.0.0:10000", "app:app"]

