import os
import json
import numpy as np
import cv2
import tensorflow as tf
import speech_recognition as sr
import spacy
import asyncio
import websockets
from fastapi import FastAPI, WebSocket, Response
from fastapi.responses import StreamingResponse
import subprocess
import platform

app = FastAPI()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")
ALLOWED_POS = {"NOUN", "PRON", "ADJ", "VERB"}

# Load trained model
model = tf.keras.models.load_model("sign_language_model.h5")

# Set dataset folder
video_folder = "/Users/sujana/Documents/Sujana_personal/dl_proj/DL_Dataset"

# Load video mappings
mapping_file = "mapping.json"
word_to_video = {}

if os.path.exists(mapping_file):
    with open(mapping_file, "r") as f:
        word_to_video = json.load(f)

# Speech Recognition WebSocket
@app.websocket("/ws/speech")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    recognizer = sr.Recognizer()
    
    while True:
        with sr.Microphone() as source:
            print("🎤 Speak now...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"🗣️ Recognized: {text}")
            tokens = tokenize_text(text)
            await websocket.send_json({"text": text, "tokens": tokens})
        except Exception as e:
            await websocket.send_json({"error": str(e)})

# Tokenization function
def tokenize_text(text):
    doc = nlp(text)
    return [token.text for token in doc if token.pos_ in ALLOWED_POS]

# Generate and Stream Video
def generate_video(words):
    frames_list = []
    phrase = " ".join(words)

    if phrase in word_to_video:
        frames = extract_gesture_clip(word_to_video[phrase])
        if frames:
            frames_list.extend(frames)
    
    for word in words:
        if word in word_to_video:
            frames = extract_gesture_clip(word_to_video[word])
            
            # Function to extract gesture clip from a video file
            def extract_gesture_clip(video_path):
                cap = cv2.VideoCapture(video_path)
                frames = []
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frames.append(frame)
                cap.release()
                return frames
            
            if frames:
                frames_list.extend(frames)
    
    if not frames_list:
        print("❌ No matching gestures found.")
        return None

    height, width, layers = frames_list[0].shape
    out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))
    
    for frame in frames_list:
        out.write(frame)
    
    out.release()
    return "output.mp4"

@app.get("/stream")
def stream_video():
    def generate():
        with open("output.mp4", "rb") as video_file:
            yield from video_file
    return StreamingResponse(generate(), media_type="video/mp4")
