import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load pre-trained ResNet50 model for feature extraction
resnet = ResNet50(weights='imagenet', include_top=False, pooling='avg')

# Set the path to the dataset folder
video_folder = "/Users/sujana/Documents/Sujana_personal/dl_proj/DL_Dataset"

all_files = os.listdir(video_folder)
print(f"📂 All files in dataset folder: {all_files}")  # Debugging line

video_files = [f for f in all_files if f.endswith((".mp4", ".MOV"))]

if len(video_files) == 0:
    raise ValueError(f"❌ No MP4 or MOV video files found in {video_folder}. Check file paths and formats!")

print(f"✅ Found {len(video_files)} videos: {video_files}")

def extract_features_from_video(video_path):
    """Extract frame-wise features from a given video file using ResNet50."""
    cap = cv2.VideoCapture(video_path)
    features = []
    
    if not cap.isOpened():
        print(f"❌ Error: Cannot open video file {video_path}")
        return np.array([])  # Return empty array to handle errors

    frame_count = 0  # Debug: Count processed frames
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        print(f"✅ Processing frame {frame_count} from {os.path.basename(video_path)}")  # Debug log
        frame = cv2.resize(frame, (224, 224))  # Resize to match ResNet50 input
        frame = np.expand_dims(frame, axis=0)
        frame = frame / 255.0  # Normalize
        feature = resnet.predict(frame, verbose=0)  # Extract feature vector
        features.append(feature.flatten())

    cap.release()
    
    if frame_count == 0:
        print(f"❌ No frames extracted from {os.path.basename(video_path)}. Check if the video is corrupted.")
    
    return np.array(features)

# Get all video files in the dataset folder
video_files = [f for f in os.listdir(video_folder) if f.endswith((".mp4", ".MOV"))]

if len(video_files) == 0:
    raise ValueError(f"❌ No MP4 or MOV video files found in {video_folder}. Check file paths!")

print(f"📂 Found {len(video_files)} videos for feature extraction.")

# Extract features from all videos
X = [extract_features_from_video(os.path.join(video_folder, file)) for file in video_files]

# 🚀 Ensure X is not empty before padding
if len(X) == 0 or all(len(x) == 0 for x in X):
    raise ValueError("❌ No valid feature vectors extracted. Ensure videos are loaded and preprocessed correctly.")

# Convert to padded sequences
X = pad_sequences(X, padding='post', dtype='float32')

print(f"✅ Feature extraction complete. X shape after padding: {X.shape}")

# Define and train a simple model (example)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Masking

# Ensure all extracted features have the same shape
max_timesteps = X.shape[1]  # Use the padded sequence length

model = Sequential([
    Masking(mask_value=0.0, input_shape=(max_timesteps, X.shape[2])),
    LSTM(128, return_sequences=True),
    LSTM(64),
    Dense(32, activation='relu'),
    Dense(len(video_files), activation='softmax')  # Number of unique gestures
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Dummy labels for now (replace with real labels)
y = np.arange(len(X))  # Example: Just assigning indices as labels
y = tf.keras.utils.to_categorical(y, num_classes=len(video_files))

# Train the model
model.fit(X, y, epochs=10, batch_size=4)

# Save the trained model
model.save("sign_language_model.h5")
print("✅ Model saved as sign_language_model.h5")

