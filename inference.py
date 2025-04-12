import os
import json
import numpy as np
import cv2
import tensorflow as tf
import speech_recognition as sr
import spacy
import subprocess
import platform  # To detect OS

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Allowed POS tags: Nouns, Pronouns, Adjectives, Verbs
ALLOWED_POS = {"NOUN", "PRON", "ADJ", "VERB"}

# Set GPU for Mac M3
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

# Load trained model
model = tf.keras.models.load_model("sign_language_model.h5")

# Set dataset folder
video_folder = "/Users/sujana/Documents/Sujana_personal/dl_proj/DL_Dataset"

# Load video mappings
mapping_file = "mapping.json"  # Define the mapping file path

if os.path.exists(mapping_file):
    with open(mapping_file, "r") as f:
        word_to_video = json.load(f)
else:
    # Auto-map videos based on filenames (if no predefined mapping)
    video_files = [f for f in os.listdir(video_folder) if f.endswith((".mp4", ".MOV"))]
    word_to_video = {}
    
    for vid in video_files:
        base_name = os.path.splitext(vid)[0].lower()
        base_name = base_name.lstrip("0123456789.-_ ")  # Remove numbering
        base_name = base_name.replace("(", "").replace(")", "").strip()
        word_to_video[base_name] = os.path.join(video_folder, vid)

# Speech recognition function
def recognize_speech(audio_file=None):
    recognizer = sr.Recognizer()
    
    if audio_file:
        # Handle file-based recognition
        with sr.AudioFile(audio_file) as source:
            print(f"🎵 Recognizing speech from file: {audio_file}")
            audio = recognizer.record(source)
    else:
        # Handle microphone-based recognition
        with sr.Microphone() as source:
            print("🎤 Speak now...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ Recognized: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return ""
    except sr.RequestError:
        print("❌ Could not request results, check internet.")
        return ""

# Tokenization function: Extract only nouns, pronouns, adjectives, and verbs
def tokenize_text(text):
    doc = nlp(text)
    return [token.text for token in doc if token.pos_ in ALLOWED_POS]

# Extract gesture clips using OpenCV
def extract_gesture_clip(video_path, duration=2):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"⚠️ Error opening {video_path}")
        return None

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(duration * fps)
    frames = []

    for _ in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()
    return frames if frames else None

# Generate video output using OpenCV
def generate_output_video(words):
    frames_list = []
    phrase = " ".join(words)  # Convert tokens to phrase for mapping

    if phrase in word_to_video:
        print(f"✅ Found matching video for: {phrase}")
        frames = extract_gesture_clip(word_to_video[phrase])
        if frames:
            frames_list.extend(frames)
    else:
        print(f"❌ No matching video for: {phrase}")
        
        # Check individual words if no exact phrase match
        for word in words:
            if word in word_to_video:
                print(f"✅ Found matching video for: {word}")
                frames = extract_gesture_clip(word_to_video[word])
                if frames:
                    frames_list.extend(frames)

    if not frames_list:
        print("❌ No matching gestures found.")
        return

    height, width, layers = frames_list[0].shape
    out = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

    for frame in frames_list:
        out.write(frame)

    out.release()
    print("✅ Video saved as output.mp4")
    play_video("output.mp4")

# Play the generated video immediately
def play_video(video_path):
    if platform.system() == "Darwin":  
        os.system(f"open {video_path}")
    elif platform.system() == "Windows":  
        os.startfile(video_path)
    else:  # Linux or other OS
        subprocess.run(["xdg-open", video_path], check=True)

# Main loop
while True:
    spoken_text = recognize_speech()
    if spoken_text:
        tokens = tokenize_text(spoken_text)
        print(f"🔹 Tokenized Words (Filtered): {tokens}")
        generate_output_video(tokens)
