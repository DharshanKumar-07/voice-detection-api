import requests
import base64
import json

# Load local MP3 file
try:
    with open("test_audio.mp3", "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
except FileNotFoundError:
    print("Error: Please put a file named 'test_audio.mp3' in this folder!")
    exit()

# Send to API (Port 5001)
url = "http://127.0.0.1:5001/api/voice-detection"
payload = {
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": encoded_string
}
headers = {
    "Content-Type": "application/json",
    "x-api-key": "sk_test_123456789"
}

print("Sending audio to AI model...")
try:
    response = requests.post(url, json=payload, headers=headers)
    print("\n--- API RESPONSE ---")
    print(json.dumps(response.json(), indent=4))
except Exception as e:
    print(f"Failed to connect: {e}")