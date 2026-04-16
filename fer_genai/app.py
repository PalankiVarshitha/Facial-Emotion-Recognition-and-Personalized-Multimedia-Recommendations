from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import base64
from datetime import datetime
from io import BytesIO
from PIL import Image
from utils.database import init_db, create_user, verify_user, add_history, get_user_history
from utils.model_loader import get_detector
from utils.gemini_helper import get_recommendations, format_recommendations
from config import SECRET_KEY, UPLOAD_FOLDER

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_id = create_user(username, email, password)
        
        if user_id:
            return redirect(url_for('login'))
        else:
            return render_template('signup.html', error='User already exists')
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = verify_user(email, password)
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('upload'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/upload')
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('upload.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    image_data = data.get('image')
    
    if not image_data:
        return jsonify({'error': 'No image data'}), 400
    
    image_data = image_data.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    
    filename = f"{session['user_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(filepath)
    
    print(f"\n{'='*80}")
    print(f"[REQUEST] User ID: {session['user_id']}")
    print(f"[REQUEST] Image saved: {filename}")
    print(f"{'='*80}")
    
    detector = get_detector()
    emotion, confidence, error = detector.predict(filepath)
    
    if error:
        print(f"[ERROR] Prediction failed: {error}")
        return jsonify({'error': error}), 400
    
    session['last_emotion'] = emotion
    session['last_confidence'] = confidence
    session['last_filepath'] = filepath
    
    print(f"[SUCCESS] Prediction completed - emotion detected")
    print(f"{'='*80}\n")
    
    return jsonify({
        'success': True,
        'emotion': emotion,
        'confidence': round(confidence * 100, 2),
        'redirect': url_for('category_select')
    })

@app.route('/category_select')
def category_select():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    emotion = session.get('last_emotion')
    confidence = session.get('last_confidence')
    
    if not emotion:
        return redirect(url_for('upload'))
    
    return render_template('category_select.html', emotion=emotion, confidence=confidence)

@app.route('/get_category_recommendations', methods=['POST'])
def get_category_recommendations():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    selected_category = data.get('category')
    
    emotion = session.get('last_emotion')
    
    if not emotion or not selected_category:
        return jsonify({'error': 'Missing emotion or category'}), 400
    
    # Generate recommendations for all three categories in a single API call
    all_recommendations = {
        'songs': [],
        'movies': [],
        'books': []
    }
    
    # Single API call to get all recommendations
    recommendations_text = get_recommendations(emotion)
    formatted = format_recommendations(recommendations_text)
    all_recommendations = formatted
    
    # detect quota or generation errors
    recommendation_error = False
    if (not recommendations_text) or "Unable to generate" in recommendations_text or "RESOURCE_EXHAUSTED" in recommendations_text:
        recommendation_error = True
    session['recommendation_error'] = recommendation_error
    
    # Debug logging
    print(f"\n[DEBUG] Emotion: {emotion}")
    print(f"[DEBUG] API Response (first 300 chars): {recommendations_text[:300]}")
    print(f"[DEBUG] Extracted songs: {len(all_recommendations['songs'])} items")
    print(f"[DEBUG] Extracted movies: {len(all_recommendations['movies'])} items")
    print(f"[DEBUG] Extracted books: {len(all_recommendations['books'])} items")
    
    filepath = session.get('last_filepath')
    # Save the recommendations text to history (reuse the already generated text)
    add_history(session['user_id'], emotion, session.get('last_confidence'), filepath, recommendations_text)
    
    session['last_recommendations'] = all_recommendations
    session['last_category'] = selected_category
    
    print(f"[SUCCESS] All recommendations generated")
    print(f"{'='*80}\n")
    
    return jsonify({
        'success': True,
        'redirect': url_for('results')
    })

@app.route('/results')
def results():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    emotion = session.get('last_emotion')
    confidence = session.get('last_confidence')
    recommendations = session.get('last_recommendations')
    
    return render_template('results.html', emotion=emotion, confidence=confidence, recommendations=recommendations)

@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_history = get_user_history(session['user_id'])
    return render_template('history.html', history=user_history)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)