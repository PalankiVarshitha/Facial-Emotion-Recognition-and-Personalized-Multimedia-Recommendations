import torch
import timm
import cv2
import numpy as np
from torchvision import transforms as T
from PIL import Image
from config import MODEL_PATH, EMOTION_MAPPING, IMAGE_SIZE, MEAN, STD

class EmotionDetector:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"[MODEL] Loading model on device: {self.device}")
        
        self.model = timm.create_model('rexnet_150', pretrained=False, num_classes=len(EMOTION_MAPPING))
        self.model.load_state_dict(torch.load(MODEL_PATH, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        print("[MODEL] Model loaded successfully")
        
        self.transform = T.Compose([
            T.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            T.Grayscale(num_output_channels=3),
            T.ToTensor(),
            T.Normalize(mean=MEAN, std=STD)
        ])
        
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        print("[FACE DETECTION] Haar Cascade loaded")
    
    def detect_and_crop_face(self, image_path):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
        
        print(f"[FACE DETECTION] Detected {len(faces)} face(s)")
        
        if len(faces) == 0:
            return None, "No face detected"
        
        largest_face = max(faces, key=lambda face: face[2] * face[3])
        x, y, w, h = largest_face
        
        print(f"[FACE DETECTION] Using largest face: position=({x},{y}), size=({w}x{h})")
        
        padding = int(0.2 * max(w, h))
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(img.shape[1], x + w + padding)
        y2 = min(img.shape[0], y + h + padding)
        
        face_img = img[y1:y2, x1:x2]
        
        if face_img.size == 0:
            return None, "Face crop failed"
        
        face_pil = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))
        return face_pil, None
    
    def predict(self, image_path):
        print(f"\n[PREDICTION START] Processing image: {image_path}")
        
        face_img, error = self.detect_and_crop_face(image_path)
        
        if error:
            print(f"[ERROR] {error}")
            return None, 0.0, error
        
        print("[PREPROCESSING] Face cropped and extracted (matching training data)")
        image_tensor = self.transform(face_img).unsqueeze(0).to(self.device)
        print(f"[PREPROCESSING] Image tensor shape: {image_tensor.shape}")
        
        with torch.no_grad():
            output = self.model(image_tensor)
            probabilities = torch.softmax(output, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
            
            print(f"[PREDICTION] Raw output: {output.cpu().numpy()}")
            print(f"[PREDICTION] Probabilities: {probabilities.cpu().numpy()}")
            
            all_emotions = {}
            for idx, prob in enumerate(probabilities[0].cpu().numpy()):
                emotion_name = EMOTION_MAPPING[idx]
                all_emotions[emotion_name] = float(prob * 100)
            
            print("[PREDICTION] All emotion probabilities:")
            for emotion, prob in sorted(all_emotions.items(), key=lambda x: x[1], reverse=True):
                print(f"  {emotion}: {prob:.2f}%")
        
        emotion = EMOTION_MAPPING[predicted.item()]
        confidence_score = confidence.item()
        
        print(f"[RESULT] Detected emotion: {emotion.upper()}")
        print(f"[RESULT] Confidence: {confidence_score * 100:.2f}%")
        print("[PREDICTION END]\n")
        
        return emotion, confidence_score, None

detector = None

def get_detector():
    global detector
    if detector is None:
        detector = EmotionDetector()
    return detector