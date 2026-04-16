import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, 'models', 'raf_best_model.pth')

GEMINI_API_KEY = 'AIzaSyDBlTlnij3HsmbkSsQRTw_86PqdJXcLuYA'
GEMINI_MODEL = 'gemini-2.5-flash-lite'

DATABASE_PATH = os.path.join(BASE_DIR, 'emotion_detection.db')

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

EMOTION_MAPPING = {
    0: 'surprise',
    1: 'fear',
    2: 'disgust',
    3: 'happy',
    4: 'sad',
    5: 'angry',
    6: 'neutral'
}

IMAGE_SIZE = 224
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]

SECRET_KEY = 'your_secret_key_here_change_in_production'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS