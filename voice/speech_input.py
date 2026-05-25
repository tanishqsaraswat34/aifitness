"""
AI Fitness Assistant - Speech Input Module
Uses Google Cloud Speech-to-Text API for voice recognition
"""

import os
import requests
import base64

class SpeechInput:
    """
    Handle speech input using Google Cloud Speech-to-Text API
    """
    
    def __init__(self):
        """Initialize the Speech-to-Text API client"""
        self.api_key = os.environ.get('GOOGLE_CLOUD_API_KEY')
        self.endpoint = "https://speech.googleapis.com/v1/speech:recognize"
    
    def process_audio_from_file(self, audio_file_path, language_code='en-US'):
        """
        Process audio file and convert to text using Google Cloud API
        
        Args:
            audio_file_path (str): Path to audio file (WAV, FLAC, MP3, OGG)
            language_code (str): Language code (default: en-US)
        
        Returns:
            str: Recognized text or None if recognition failed
        """
        if not self.api_key:
            print("Error: GOOGLE_CLOUD_API_KEY not set")
            return None
        
        try:
            # Read audio file and encode to base64
            with open(audio_file_path, 'rb') as audio_file:
                audio_content = base64.b64encode(audio_file.read()).decode('utf-8')
            
            # Determine audio encoding based on file extension
            file_ext = audio_file_path.split('.')[-1].lower()
            encoding_map = {
                'wav': 'LINEAR16',
                'flac': 'FLAC',
                'mp3': 'MP3',
                'ogg': 'OGG_OPUS'
            }
            audio_encoding = encoding_map.get(file_ext, 'LINEAR16')
            
            # Prepare request payload
            payload = {
                "config": {
                    "encoding": audio_encoding,
                    "languageCode": language_code,
                    "sampleRateHertz": 16000,
                    "enableAutomaticPunctuation": True
                },
                "audio": {
                    "content": audio_content
                }
            }
            
            # Make API request
            headers = {'Content-Type': 'application/json'}
            url = f"{self.endpoint}?key={self.api_key}"
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Extract recognized text
            if 'results' in result and len(result['results']) > 0:
                transcript = result['results'][0]['alternatives'][0]['transcript']
                print(f"You said: {transcript}")
                return transcript.lower()
            else:
                print("Sorry, I could not understand your speech.")
                return None
                
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            return None
    
    def process_command(self, text):
        """
        Process speech command and extract intent
        
        Args:
            text (str): Recognized text
        
        Returns:
            dict: Command details with intent and parameters
        """
        if text is None:
            return None
        
        text = text.lower().strip()
        
        # Define command patterns
        commands = {
            'dashboard': ['show dashboard', 'show my dashboard', 'dashboard', 'home'],
            'workout': ['suggest workout', 'workout plan', 'give me workout', 'what workout'],
            'diet': ['suggest diet', 'diet plan', 'give me diet', 'what diet'],
            'bmi': ['what is my bmi', 'calculate bmi', 'my bmi', 'bmi'],
            'calories': ['track calories', 'calories', 'calorie intake', 'my calories'],
            'progress': ['show progress', 'my progress', 'progress tracking'],
            'weight': ['track weight', 'log weight', 'update weight', 'my weight'],
            'water': ['water intake', 'log water', 'water'],
            'quote': ['motivational quote', 'quote', 'inspire me'],
            'logout': ['logout', 'exit', 'goodbye', 'bye']
        }
        
        for intent, keywords in commands.items():
            for keyword in keywords:
                if keyword in text:
                    return {
                        'intent': intent,
                        'text': text,
                        'success': True
                    }
        
        return {
            'intent': 'unknown',
            'text': text,
            'success': False
        }


# Create global instance
speech_input = SpeechInput()
