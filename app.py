from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
import os
import json
import cv2
import numpy as np
import tensorflow as tf
import speech_recognition as sr
import spacy

app = FastAPI()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")
ALLOWED_POS = {"NOUN", "PRON", "ADJ", "VERB"}

# Load trained model
model = tf.keras.models.load_model("sign_language_model.h5")

# Load word-to-video mapping
mapping_file = "gesture_mapping.json"
word_to_video = json.load(open(mapping_file, "r")) if os.path.exists(mapping_file) else {}

# WebSocket Endpoint
@app.websocket("/ws/speech")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            
            # Tokenization
            tokens = [token.text for token in nlp(data) if token.pos_ in ALLOWED_POS]

            # Send recognized text and tokens back to frontend
            await websocket.send_json({"text": data, "tokens": tokens})
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()

# Speech-to-Sign Video Endpoint
@app.post("/speech-to-sign/")
@app.post("/speech-to-sign/")
async def speech_to_sign(audio: UploadFile = File(...)):
    try:
        print(f"Received file: {audio.filename}")  # Debugging

        with open("temp_audio.wav", "wb") as f:
            f.write(await audio.read())

        recognizer = sr.Recognizer()
        with sr.AudioFile("temp_audio.wav") as source:
            audio_data = recognizer.record(source)
        
        # Perform Speech Recognition
        text = recognizer.recognize_google(audio_data).lower()
        print(f"Recognized Text: {text}")  # Debugging

        # Tokenize the Text
        tokens = [token.text for token in nlp(text) if token.pos_ in ALLOWED_POS]
        print(f"Tokens: {tokens}")  # Debugging

        return {"text": text, "tokens": tokens}

    except sr.UnknownValueError:
        return JSONResponse({"error": "Speech not understood"}, status_code=400)
    except sr.RequestError:
        return JSONResponse({"error": "Speech recognition failed"}, status_code=500)