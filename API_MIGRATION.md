# API Migration Summary

## Changes Made

This document outlines all the changes made to replace local libraries with API-based solutions and remove image generation.

### 1. **Chatbot Module** (`ai/chatbot.py`)
- **Removed**: OpenAI API dependency
- **Added**: Gemini API integration
- **Changes**:
  - Replaced `openai.ChatCompletion.create()` with Gemini API REST calls
  - Uses `generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent`
  - Requires: `GEMINI_API_KEY` environment variable
  - Maintains fallback to rule-based responses if API is unavailable

### 2. **Recommendation Engine** (`ai/recommendation_engine.py`)
- **Removed**: Hardcoded meal suggestion dictionaries with if-else cases
- **Added**: Gemini API-based meal suggestions
- **Changes**:
  - New method `_get_meals_from_api()` - generates meal suggestions dynamically via API
  - New method `_get_fallback_meals()` - provides backup hardcoded meals if API fails
  - Updated `get_diet_recommendation()` - now returns API-generated meals instead of hardcoded options
  - Fully API-driven: No more if-else logic for meal selection
  - Requires: `GEMINI_API_KEY` environment variable

### 3. **Image Processor** (`ai/image_processor.py`)
- **Removed**: All image generation functions
  - `generate_transformation_from_photo()` - Returns None
  - `generate_physique_image_from_dimensions()` - Returns None
  - `generate_before_after_comparison()` - Returns None
- **Kept**: Basic image upload and processing
  - `process_uploaded_image()` - Still handles file uploads

### 4. **Speech Input Module** (`voice/speech_input.py`)
- **Removed**: `SpeechRecognition` library (local speech-to-text)
- **Added**: Google Cloud Speech-to-Text API
- **Changes**:
  - New method `process_audio_from_file()` - Converts audio files to text via API
  - Supports: WAV, FLAC, MP3, OGG formats
  - Uses REST API instead of local microphone + Google's free service
  - Requires: `GOOGLE_CLOUD_API_KEY` environment variable
  - Note: Works with pre-recorded audio files (not real-time microphone input)

### 5. **Speech Output Module** (`voice/speech_output.py`)
- **Removed**: `pyttsx3` library (local text-to-speech)
- **Added**: Google Cloud Text-to-Speech API
- **Changes**:
  - New method `speak()` - Synthesizes speech from text via API
  - New method `save_speech_to_file()` - Saves audio to MP3 file
  - New method `set_voice()` - Change voice gender and language
  - New method `set_rate()` - Adjust speaking rate (0.25 to 4.0)
  - Returns audio bytes (MP3 format)
  - Requires: `GOOGLE_CLOUD_API_KEY` environment variable
  - Supports multiple voices (Neural2-A for male, Neural2-C for female)

### 6. **Requirements** (`requirements.txt`)
- **Removed**:
  - `openai>=0.27.0`
  - `SpeechRecognition==3.10.0`
  - `pyttsx3==2.90`
- **Kept**:
  - `requests==2.31.0` (for API calls)
  - `Pillow==10.0.0` (for image processing)
  - `python-dotenv==1.0.0` (for environment variables)
  - All Flask dependencies

### 7. **Environment Configuration** (`.env.example`)
- **New**: Added `.env.example` with required API keys
- **Required**:
  - `GEMINI_API_KEY` - For chat and meal suggestions
  - `GOOGLE_CLOUD_API_KEY` - For speech services
  - `FLASK_SECRET_KEY` - For session management

## API Keys Required

You now need TWO API keys:

### 1. Gemini API Key
- Source: https://makersuite.google.com/app/apikey
- Used for: Chat responses, meal suggestions
- Cost: Free tier available

### 2. Google Cloud API Key
- Source: https://console.cloud.google.com/
- Used for: Speech-to-text, text-to-speech
- Cost: Pay-as-you-go (free trial available)
- Services needed:
  - Cloud Speech-to-Text API
  - Cloud Text-to-Speech API

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file**:
   ```bash
   cp .env.example .env
   ```

3. **Add API keys to `.env`**:
   ```
   GEMINI_API_KEY=your_key_here
   GOOGLE_CLOUD_API_KEY=your_key_here
   FLASK_SECRET_KEY=your_secret_key
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

## API Call Examples

### Gemini API (Chat)
```python
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
payload = {
    "contents": [{"parts": [{"text": "Your prompt here"}]}],
    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 280}
}
response = requests.post(url, json=payload)
```

### Google Cloud Speech-to-Text API
```python
url = f"https://speech.googleapis.com/v1/speech:recognize?key={GOOGLE_CLOUD_API_KEY}"
payload = {
    "config": {
        "encoding": "LINEAR16",
        "languageCode": "en-US",
        "sampleRateHertz": 16000
    },
    "audio": {"content": base64_encoded_audio}
}
response = requests.post(url, json=payload)
```

### Google Cloud Text-to-Speech API
```python
url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={GOOGLE_CLOUD_API_KEY}"
payload = {
    "input": {"text": "Your text here"},
    "voice": {"languageCode": "en-US", "name": "en-US-Neural2-C"},
    "audioConfig": {"audioEncoding": "MP3"}
}
response = requests.post(url, json=payload)
```

## Fallback Behavior

- **Chat**: Falls back to rule-based responses if Gemini API fails
- **Meal Suggestions**: Falls back to hardcoded meals if Gemini API fails
- **Speech Services**: Returns None/error message if API keys not configured

## Benefits of Migration

✅ No local library dependencies for AI/speech  
✅ All AI using Gemini (single LLM provider)  
✅ Scalable REST API calls  
✅ No image generation overhead  
✅ Smaller application footprint  
✅ Cloud-based speech services (more accurate)  
✅ Fully API-driven meal suggestions (no hardcoding)  

## Notes

- Speech-to-text API works with pre-recorded audio files, not real-time microphone input
- For real-time voice: Consider using WebSocket connections for streaming audio
- All API responses are cached/handled gracefully with fallbacks
- Image upload still works; image generation has been removed
