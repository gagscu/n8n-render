#!/bin/sh
set -e

echo "FFmpeg version:"
ffmpeg -version

echo "Running video creation..."
python main.py

