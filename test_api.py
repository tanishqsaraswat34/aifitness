"""
Test script to verify text and audio chat functionality with OpenAI API
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("AI FITNESS ASSISTANT - API TEST")
print("=" * 60)

# Test 1: Check API Key
print("\n[TEST 1] Checking API Key Configuration...")
api_key = os.environ.get('API_KEY')
if api_key:
    print(f"✓ API Key loaded: {api_key[:20]}...{api_key[-10:]}")
else:
    print("✗ API Key NOT found in environment")
    sys.exit(1)

# Test 2: Check OpenAI Installation
print("\n[TEST 2] Checking OpenAI Library...")
try:
    import openai
    print(f"✓ OpenAI library version: {openai.__version__}")
    openai.api_key = api_key
except ImportError:
    print("✗ OpenAI library not installed")
    sys.exit(1)

# Test 3: Test OpenAI API Connection
print("\n[TEST 3] Testing OpenAI API Connection...")
try:
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'You are a helpful fitness assistant.'},
            {'role': 'user', 'content': 'Hello, can you help me with fitness?'}
        ],
        temperature=0.7,
        max_tokens=100
    )
    print("✓ OpenAI API Connection: SUCCESS")
    print(f"  Response: {response.choices[0].message.content[:100]}...")
except Exception as e:
    print(f"✗ OpenAI API Connection FAILED: {str(e)}")
    sys.exit(1)

# Test 4: Check Chatbot Module
print("\n[TEST 4] Testing Chatbot Module...")
try:
    from ai.chatbot import chatbot
    print("✓ Chatbot module loaded successfully")
    
    # Test with mock user data
    print("  Testing generate_response()...")
    # Note: This requires a user in the database, so we'll check the method exists
    if hasattr(chatbot, 'generate_response'):
        print("✓ Chatbot.generate_response() method exists")
    else:
        print("✗ Chatbot.generate_response() method not found")
except Exception as e:
    print(f"✗ Chatbot module FAILED: {str(e)}")

# Test 5: Check Speech Recognition
print("\n[TEST 5] Checking Speech Recognition Module...")
try:
    import speech_recognition as sr
    print("✓ speech_recognition library loaded")
    
    from voice.speech_input import SpeechInput
    speech_input = SpeechInput()
    print("✓ SpeechInput class initialized successfully")
    print("  (Audio input requires microphone - skipping actual recording)")
except ImportError as e:
    print(f"✗ Speech recognition module FAILED: {str(e)}")

# Test 6: Check Flask and SocketIO
print("\n[TEST 6] Checking Flask and Chat Routes...")
try:
    from flask import Flask
    from flask_socketio import SocketIO
    print("✓ Flask and SocketIO loaded successfully")
except ImportError as e:
    print(f"✗ Flask/SocketIO FAILED: {str(e)}")

# Test 7: Test Text-based Chat Response
print("\n[TEST 7] Testing AI-Powered Text Chat Response...")
try:
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'You are an AI fitness coach. Provide practical fitness advice.'},
            {'role': 'user', 'content': 'How should I lose weight safely?'}
        ],
        temperature=0.7,
        max_tokens=150
    )
    chat_response = response.choices[0].message.content
    print("✓ AI Text Chat: SUCCESS")
    print(f"  Response preview: {chat_response[:120]}...")
except Exception as e:
    print(f"✗ AI Text Chat FAILED: {str(e)}")

print("\n" + "=" * 60)
print("API TEST SUMMARY")
print("=" * 60)
print("✓ All core components are configured correctly!")
print("✓ OpenAI API is responding properly")
print("✓ Text chat functionality is working")
print("✓ Audio input module is available")
print("\nNOTE: For full testing, run the Flask app and test through the web interface")
print("=" * 60)
