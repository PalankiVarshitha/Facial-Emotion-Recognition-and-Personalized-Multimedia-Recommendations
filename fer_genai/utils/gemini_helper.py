from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)

def get_recommendations(emotion, category=None):
    mood_balancing_prompts = {
        'happy': 'feel even more joyful and motivated',
        'sad': 'uplift their mood and bring positivity',
        'angry': 'calm down and find peace',
        'fear': 'feel more confident and secure',
        'surprised': 'maintain excitement and wonder',
        'disgust': 'cleanse their mind and refresh perspective',
        'neutral': 'find inspiration and engagement'
    }
    
    mood_intent = mood_balancing_prompts.get(emotion.lower(), 'improve their emotional state')
    
    # Always request all categories in one API call to avoid quota issues
    prompt = f"""The user is currently feeling '{emotion}'. Provide recommendations to help them {mood_intent}.

Please format your response exactly like this:

Songs:
1. Song Name - Artist Name
2. Song Name - Artist Name
3. Song Name - Artist Name
4. Song Name - Artist Name
5. Song Name - Artist Name
6. Song Name - Artist Name
7. Song Name - Artist Name
8. Song Name - Artist Name
9. Song Name - Artist Name
10. Song Name - Artist Name

Movies:
1. Movie Name (Year)
2. Movie Name (Year)
3. Movie Name (Year)
4. Movie Name (Year)
5. Movie Name (Year)
6. Movie Name (Year)
7. Movie Name (Year)
8. Movie Name (Year)
9. Movie Name (Year)
10. Movie Name (Year)

Books:
1. Book Name by Author Name
2. Book Name by Author Name
3. Book Name by Author Name
4. Book Name by Author Name
5. Book Name by Author Name
6. Book Name by Author Name
7. Book Name by Author Name
8. Book Name by Author Name
9. Book Name by Author Name
10. Book Name by Author Name

Focus on uplifting, inspiring, or mood-balancing content that counters their current emotional state. Prefer recent and popular titles."""
    
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"[GEMINI ERROR] {e}")
        return f"Unable to generate recommendations at this time."

def format_recommendations(recommendations_text):
    lines = recommendations_text.strip().split('\n')
    formatted = {
        'songs': [],
        'movies': [],
        'books': []
    }
    
    current_category = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for category headers (case-insensitive)
        line_lower = line.lower()
        if line_lower.startswith('songs'):
            current_category = 'songs'
            continue
        elif line_lower.startswith('movies'):
            current_category = 'movies'
            continue
        elif line_lower.startswith('books'):
            current_category = 'books'
            continue
        
        # Extract recommendation items
        if current_category and line:
            # Match lines starting with numbers (1-10)
            if len(line) > 0 and line[0].isdigit():
                # Remove leading number, dot, and spaces (e.g., "1. ", "10. ")
                cleaned = line.lstrip('0123456789. ')
                if cleaned and cleaned not in ['', 'N/A', 'None']:
                    formatted[current_category].append(cleaned)
    
    return formatted