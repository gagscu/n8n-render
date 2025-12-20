#!/bin/sh
set -e

echo "FFmpeg check"
ffmpeg -version

echo "Running python script"
python main.py

