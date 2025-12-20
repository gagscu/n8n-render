#!/bin/sh
set -e

echo "Checking FFmpeg..."
ffmpeg -version

echo "Creating video..."
python main.py

echo "Done"
