# voice-detection-api


A machine learning API that detects whether an audio file is **Real Human Speech** or **AI-Generated**. Built for the Hackathon challenge.

## Features
* **Scientific Analysis:** Uses Spectral Flatness and Zero-Crossing Rate to detect synthetic audio signatures.
* **Instant Classification:** Returns `REAL` or `AI_GENERATED` with a confidence score.
* **Secure:** Protected by API Key authentication.
* **Cloud Hosted:** Fully deployed and publicly accessible.

## Tech Stack
* **Python 3.12**
* **Flask** (API Framework)
* **Librosa** (Audio Processing)
* **Gunicorn** (Production Server)
* **Render** (Cloud Deployment)

## API Endpoint
**POST** `https://voice-detection-api-66jd.onrender.com/api/voice-detection`

### Example Request
```json
{
  "language": "English",
  "audioFormat": "mp3",
  "audioBase64": "<BASE64_STRING>"
}
