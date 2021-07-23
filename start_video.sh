#!/bin/bash

# Runs the video stream, converting an rtsp stream into a virtual webcam

source .env

ffmpeg -i rtsp://$CAM_IP/live1.sdp -f v4l2 /dev/video2