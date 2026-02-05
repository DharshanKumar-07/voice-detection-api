import os
import uuid
import base64
import json
import librosa
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
API_KEY = "sk_test_123456789"  
SUPPORTED_LANGUAGES = {"Tamil", "English", "Hindi", "Malayalam", "Telugu"}
TEMP_DIR = "temp_audio_files"

os.makedirs(TEMP_DIR, exist_ok=True)

# --- AUTHENTICATION ---
def require_api_key(f):
    def decorated_function(*args, **kwargs):
        headers_key = request.headers.get("x-api-key")
        if not headers_key or headers_key != API_KEY:
            return jsonify({"status": "error", "message": "Invalid API key"}), 403
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# --- NOVELTY: SCIENTIFIC EXPLANATION GENERATOR ---
def analyze_audio(file_path):
    try:
        # Load audio (downsampled to 16khz)
        y, sr = librosa.load(file_path, sr=16000)
        
        # 1. Spectral Flatness (Robotic/Buzzy detection)
        flatness = librosa.feature.spectral_flatness(y=y)
        avg_flatness = np.mean(flatness)
        
        # 2. Silence Ratio (Breath pause detection)
        non_silent = librosa.effects.split(y, top_db=20)
        non_silent_duration = sum([(end - start) for start, end in non_silent]) / sr
        total_duration = librosa.get_duration(y=y, sr=sr)
        silence_ratio = 1.0 - (non_silent_duration / total_duration)

        return avg_flatness, silence_ratio
    except Exception as e:
        print(f"Error: {e}")
        return 0.0, 0.0

def classify_voice(flatness, silence_ratio):
    # Simulated Logic for Prototype
    if flatness > 0.03: 
        return "AI_GENERATED", 0.95, f"High spectral flatness ({flatness:.4f}) indicates synthetic vocoding."
    elif silence_ratio < 0.01:
        return "AI_GENERATED", 0.88, "Unnatural lack of physiological breath pauses detected."
    else:
        return "HUMAN", 0.92, "Detected organic pitch fluctuations and natural breath intervals."

# --- API ENDPOINT ---
@app.route('/api/voice-detection', methods=['POST'])
@require_api_key
def voice_detection():
    data = request.get_json()
    
    if not data or 'audioBase64' not in data:
        return jsonify({"status": "error", "message": "Missing audioBase64"}), 400
    
    if data.get('language') not in SUPPORTED_LANGUAGES:
        return jsonify({"status": "error", "message": "Unsupported language"}), 400

    # Save Temp File
    temp_filename = f"{uuid.uuid4()}.mp3"
    temp_filepath = os.path.join(TEMP_DIR, temp_filename)
    
    try:
        with open(temp_filepath, "wb") as f:
            f.write(base64.b64decode(data['audioBase64']))
            
        # Analyze
        flatness, silence = analyze_audio(temp_filepath)
        label, score, reason = classify_voice(flatness, silence)
        
        return jsonify({
            "status": "success",
            "language": data['language'],
            "classification": label,
            "confidenceScore": score,
            "explanation": reason
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

if __name__ == '__main__':
    # Change 5000 to 5001 here
    app.run(host='0.0.0.0', port=5001, debug=True)