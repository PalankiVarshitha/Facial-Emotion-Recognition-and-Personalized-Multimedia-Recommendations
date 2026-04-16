# Facial Emotion Recognition Using Computer Vision with GenAI-Based Personalized Multimedia Recommendations

## Team Project

This project was developed as part of a 5-member final year team project.

## My Contributions

- Designed and implemented facial emotion detection pipeline using deep learning models (ResNet, Swin Transformer)
- Integrated GenAI-based personalized multimedia recommendation system
- Contributed to data preprocessing, model evaluation, and system integration
- Built an end-to-end system combining computer vision with intelligent recommendation workflows

## Project Context

This repository represents my implementation and understanding of the team project.

## Overview

An intelligent system that performs real-time facial emotion recognition using deep learning models and generates personalized multimedia recommendations through generative AI.

## 🚀 Features
- **Real-time Emotion Detection**: Detects 7 emotions (happy, sad, angry, surprised, fear, disgust, neutral)
- **Personalized Recommendations**: Suggests content based on your current mood
- **User Authentication**: Signup/Login system to track history
- **History Tracking**: Saves your emotion detection history
- **Web Interface**: Easy-to-use web application
- **Multiple Models**: Supports various deep learning models

## 🛠️ Technologies Used
- **Python 3.12**
- **PyTorch** - Deep learning framework
- **OpenCV** - Face detection and image processing
- **Flask** - Web framework
- **SQLite** - Database for user data
- **HTML/CSS/JavaScript** - Frontend
- **EfficientNet** - Model architecture
- **ResEmoNet** - Custom emotion recognition model

## 📋 Models Included
- `raf_efficientnet_best_model.pth` - EfficientNet model trained on RAF-DB dataset
- rab-emotion.ipynb - EfficientNet-B0 and RexNet_150 models
- ResEmoNet.ipynb - Custom emotion network
- SimCLR.ipynb - Self-supervised learning model
- SwinfaceViT.ipynb - Vision Transformer based model

## 🔧 Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- Git
- Webcam (for real-time detection)

## Steps

### 1. Clone the repository:
git clone https://github.com/PalankiVarshitha/Facial-Emotion-Recognition-and-Personalized-Multimedia-Recommendations.git
cd Facial-Emotion-Recognition-and-Personalized-Multimedia-Recommendations

### 2. Create a virtual environment:
python -m venv venv

On Windows:

venv\Scripts\activate

On Mac/Linux:

source venv/bin/activate

### 3. Install dependencies:

pip install -r fer_genai/requirements.txt

### 4. Run the application:
cd fer_genai

python app.py

Open your browser
Go to http://localhost:5000

## 🎯 How to Use

1. Sign Up / Login - Create a new account or login
2. Allow Camera Access- Grant permission when prompted
3. Show Your Emotion - Look at the camera naturally
4. Get Initial Recommendations - System detects your emotion and shows personalized multimedia recommendations to help balance your mood
5. Choose Your Content Type - After viewing recommendations, you can select what you want:
   - 🎵 Songs - Switch to music recommendations
   - 📚 Books - Switch to reading suggestions  
   - 🎬 Movies - Switch to film recommendations
6. Navigate Freely - Toggle between Songs, Books, and Movies anytime to see different recommendations - all tailored to balance your current mood

## 🎯 Mood-Balancing Recommendations

Based on your detected emotion, the system recommends content to help balance your mood:

| Emotion | 🎵 Songs | 📚 Books | 🎬 Movies | Goal |
|---------|----------|-----------|------------|------|
| 😊 Happy | Upbeat, cheerful music | Comedy, feel-good books | Comedy, adventure movies | Enhance positivity |
| 😢 Sad | Calming, uplifting songs | Inspirational, drama books | Feel-good, heartwarming films | Lift your spirits |
| 😠 Angry | Relaxing, calming music | Mystery, thriller books | Action, intense movies | Channel your energy |
| 😲 Surprised | Energetic, upbeat songs | Sci-fi, fantasy books | Sci-fi, mystery movies | Match your excitement |
| 😨 Fear | Peaceful, soothing music | Horror, suspense books | Horror, psychological films | Face your fears safely |
| 🤢 Disgust | Happy, cheerful songs | Light-hearted, comedy books | Comedy, parody movies | Shift your focus |
| 😐 Neutral | Varied recommendations | Mixed genres | Mixed recommendations | Explore new content |

## 📊 Dataset

The models are trained on:

RAF-DB (Real-world Affective Faces Database)

7 basic emotions: Happy, Sad, Surprise, Fear, Anger, Disgust, Neutral

## 🎨 Future Enhancements

Add more emotion categories

Integrate with music APIs (Spotify, YouTube)

Mobile app version

Multi-face detection

Real-time recommendation updates

Social sharing features
