"""
AI Fitness Assistant - Speech Output Module
Uses Google Cloud Text-to-Speech API for voice synthesis
"""

import os
import requests
import base64
import io
from datetime import datetime

class SpeechOutput:
    """
    Handle speech output using Google Cloud Text-to-Speech API
    """
    
    def __init__(self):
        """Initialize the Text-to-Speech API client"""
        self.api_key = os.environ.get('GOOGLE_CLOUD_API_KEY')
        self.endpoint = "https://texttospeech.googleapis.com/v1/text:synthesize"
        self.language_code = "en-US"
        self.voice_name = "en-US-Neural2-C"  # Female voice
        self.speaking_rate = 1.0
    
    def speak(self, text):
        """
        Synthesize speech from text using Google Cloud API
        Returns audio bytes that can be played or saved
        
        Args:
            text (str): Text to speak
        
        Returns:
            bytes: Audio content or None if synthesis failed
        """
        if not self.api_key:
            print("Error: GOOGLE_CLOUD_API_KEY not set")
            return None
        
        try:
            payload = {
                "input": {
                    "text": text
                },
                "voice": {
                    "languageCode": self.language_code,
                    "name": self.voice_name
                },
                "audioConfig": {
                    "audioEncoding": "MP3",
                    "speakingRate": self.speaking_rate
                }
            }
            
            headers = {'Content-Type': 'application/json'}
            url = f"{self.endpoint}?key={self.api_key}"
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            
            if 'audioContent' in result:
                # Decode base64 audio
                audio_bytes = base64.b64decode(result['audioContent'])
                print(f"Speech synthesis successful. ({len(audio_bytes)} bytes)")
                return audio_bytes
            else:
                print("Error: No audio content in response")
                return None
                
        except Exception as e:
            print(f"Error during speech synthesis: {e}")
            return None
    
    def save_speech_to_file(self, text, output_path='output.mp3'):
        """
        Synthesize speech and save to file
        
        Args:
            text (str): Text to speak
            output_path (str): Path to save audio file
        
        Returns:
            bool: True if successful, False otherwise
        """
        audio_bytes = self.speak(text)
        if audio_bytes:
            try:
                with open(output_path, 'wb') as f:
                    f.write(audio_bytes)
                print(f"Audio saved to {output_path}")
                return True
            except Exception as e:
                print(f"Error saving audio: {e}")
                return False
        return False
    
    def set_voice(self, gender='female', language='en-US'):
        """
        Set the voice for speech output
        
        Args:
            gender (str): 'male' or 'female'
            language (str): Language code (e.g., 'en-US', 'en-GB')
        """
        self.language_code = language
        
        voice_map = {
            ('female', 'en-US'): 'en-US-Neural2-C',
            ('male', 'en-US'): 'en-US-Neural2-A',
            ('female', 'en-GB'): 'en-GB-Neural2-C',
            ('male', 'en-GB'): 'en-GB-Neural2-A',
        }
        
        self.voice_name = voice_map.get((gender, language), 'en-US-Neural2-C')
    
    def set_rate(self, rate):
        """
        Set the speech rate
        
        Args:
            rate (float): Speech rate (0.25 to 4.0, where 1.0 is normal)
        """
        self.speaking_rate = max(0.25, min(4.0, rate))


# Create global instance
speech_output = SpeechOutput()

# Define fitness-related responses
FITNESS_RESPONSES = {
    'greeting': "Welcome to AI Fitness Assistant. How can I help you today?",
    'goodbye': "Thank you for using AI Fitness Assistant. Stay fit and healthy!",
    'dashboard': "Opening your fitness dashboard.",
    'workout': "I'll suggest a personalized workout plan for you.",
    'diet': "I'll create a personalized diet plan for you.",
    'bmi': "Calculating your BMI score.",
    'calories': "Let me track your calories.",
    'progress': "Showing your fitness progress.",
    'weight': "Recording your weight.",
    'water': "Logging your water intake.",
    'quote': "Here's your motivation for today.",
    'error': "I'm sorry, I didn't understand that. Please try again."
}

# Motivational quotes collection
MOTIVATIONAL_QUOTES = [
    "The only way to define your limits is by going beyond them.",
    "Your body can stand almost anything. It's your mind you need to convince.",
    "The difference between who you are and who you want to be is what you do.",
    "Fitness is not about being better than someone else. It's about being better than you used to be.",
    "Success is the sum of small efforts repeated day in and day out.",
    "Don't watch the clock; do what it does. Keep going.",
    "The secret of getting ahead is getting started.",
    "Your limitations, it's only your imagination, remember that.",
    "Great things never come from comfort zones.",
    "Do something today that your future self will thank you for.",
    "Don't stop when you're tired. Stop when you're done.",
    "It's not about having time. It's about making time.",
    "Discipline is choosing between what you want now and what you want most.",
    "Progress is progress, no matter how small.",
    "Take care of your body. It's the only place you have to live.",
    "You are stronger than you think.",
]

def get_random_quote():
    """Get a random motivational quote"""
    import random
    return random.choice(MOTIVATIONAL_QUOTES)
