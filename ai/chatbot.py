"""
AI Fitness Assistant - Chatbot Module
Provides AI-backed responses for fitness, physique, diet, and transformation queries.
Uses Gemini API for AI-powered responses.
"""
import os
import random
import re
import requests
import json
from models.database import get_db_connection
from ai.recommendation_engine import recommendation_engine
from ai.transformation_engine import transformation_engine

class ChatBot:
    """AI Fitness Chatbot with Gemini API integration."""

    def __init__(self):
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY")
        self.gemini_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    def get_user(self, user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return user

    def _extract_duration(self, text):
        match = re.search(r"(\d+)\s*(month|months|week|weeks)", text)
        if match:
            value = int(match.group(1))
            unit = match.group(2)
            if 'week' in unit:
                return max(1, value // 4)
            return max(1, value)
        return None

    def _normalize_text(self, text):
        return text.lower().strip()

    def _classify_intent(self, text):
        intent_keywords = {
            'bmi': ['bmi', 'body mass index'],
            'calories': ['calorie', 'maintenance', 'macros', 'protein', 'carbs', 'fat'],
            'weight_loss': ['lose weight', 'weight loss', 'fat loss'],
            'muscle_gain': ['gain muscle', 'build muscle', 'muscle gain'],
            'workout': ['workout', 'exercise', 'training', 'routine'],
            'diet': ['diet', 'meal', 'food', 'nutrition'],
            'transformation': ['physique', 'transformation', 'progress', 'duration'],
            'greeting': ['hello', 'hi', 'hey', 'greetings'],
            'help': ['help', 'advice', 'suggest', 'tips']
        }
        for intent, tokens in intent_keywords.items():
            if any(token in text for token in tokens):
                return intent
        return 'general'

    def _build_profile_context(self, user):
        goal_map = {
            'weight_loss': 'weight loss',
            'muscle_gain': 'muscle gain',
            'general_fitness': 'general fitness'
        }
        return (
            f"Profile: {user['name']}, {user['age']} years old, {user['gender']}, "
            f"{user['height']} cm, {user['weight']} kg, goal: {goal_map.get(user['fitness_goal'], user['fitness_goal'])}."
        )

    def _gemini_available(self):
        return bool(self.gemini_api_key)

    def _gemini_response(self, user, text, duration):
        system_message = (
            "You are an AI fitness coach. Use the user's profile and goals to answer questions clearly, practically, and professionally. "
            "If the user asks for transformation advice, mention realistic expectations and emphasize consistency. "
            "Keep responses concise and actionable, between 100-200 words."
        )
        prompt = (
            f"{self._build_profile_context(user)} "
            f"User asks: '{text}'. "
            f"The user is asking about fitness, diet, workouts, or physique transformation. "
            f"Provide a helpful response without referring to the API or system internals. "
            f"If the user asks for a transformation estimate, use {duration} month(s) as the expected timeframe."
        )

        try:
            headers = {
                'Content-Type': 'application/json'
            }
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"{system_message}\n\n{prompt}"
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 280,
                    "topK": 40,
                    "topP": 0.95
                }
            }
            
            url = f"{self.gemini_endpoint}?key={self.gemini_api_key}"
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                print(f"Unexpected Gemini response format: {result}")
                return None
        except Exception as e:
            print(f'Gemini API request failed: {e}')
            return None

    def _compose_response(self, intent, user, duration):
        bmi_info = recommendation_engine.calculate_bmi(user['height'], user['weight'])
        calories = recommendation_engine.get_daily_calorie_requirement(
            user['age'], user['gender'], user['height'], user['weight'], user['fitness_goal']
        )
        macros = recommendation_engine.get_macronutrients(calories, user['fitness_goal'])
        prediction = transformation_engine.predict_transformation(
            user['age'], user['gender'], user['height'], user['weight'],
            user['fitness_goal'], duration, None
        )

        if intent == 'bmi':
            return (
                f"Your BMI is {bmi_info['bmi']} ({bmi_info['category']}). "
                f"That means {bmi_info['message']} Focus on gradual progress and consistent training."
            )

        if intent == 'calories':
            return (
                f"For your current profile, a daily target of around {calories} kcal is a good starting point. "
                f"Aiming for {macros['protein_g']}g protein, {macros['carbs_g']}g carbs, and {macros['fat_g']}g fat can support your goal."
            )

        if intent == 'weight_loss':
            return (
                "To lose weight successfully, focus on a moderate calorie deficit and strength training 3-4 times a week. "
                "Keep protein high, include cardio, and prioritize recovery for steady progress."
            )

        if intent == 'muscle_gain':
            return (
                "For muscle gain, follow a progressive strength program and eat a slight calorie surplus. "
                "Aim for enough protein, rest well, and track your lifts so you can increase load gradually."
            )

        if intent == 'workout':
            return (
                f"A balanced routine for your goal would include strength training and targeted conditioning. "
                f"Train 4-5 times a week with compound lifts plus recovery work for best results."
            )

        if intent == 'diet':
            return (
                "A well-rounded diet should prioritize lean protein, vegetables, whole grains, and healthy fats. "
                "Keep meals consistent and avoid large fluctuations in calories day-to-day."
            )

        if intent == 'transformation':
            return (
                f"In about {duration} months, you can realistically move toward a {prediction['after']['description'].lower()} physique. "
                f"Your predicted weight would be around {prediction['after']['weight']:.1f} kg with steady progress. "
                "Use the transformation page to compare your current shape with a visual preview."
            )

        if intent == 'greeting':
            return 'Hello! I am your AI fitness coach. Ask me anything about physique, diet, workouts, or transformation goals.'

        if intent == 'help':
            return (
                "I can help you with BMI, calorie targets, workout strategies, diet guidance, and physique transformation planning. "
                "Ask me about any of those topics and I will give you a helpful answer."
            )

        return (
            "That is a great question. Based on your profile, consistency and balanced nutrition are the most powerful tools. "
            "Stay consistent with your training, track your progress, and adjust your program every few weeks."
        )

    def generate_response(self, user_id, message):
        user = self.get_user(user_id)
        if not user:
            return 'I could not find your profile. Please log in again.'

        text = self._normalize_text(message)
        if not text:
            return 'Please type a question so I can help you.'

        duration = self._extract_duration(text) or 3
        intent = self._classify_intent(text)

        # Try Gemini API first
        if self._gemini_available():
            ai_response = self._gemini_response(user, text, duration)
            if ai_response:
                return ai_response

        # Fallback to rule-based responses
        return self._compose_response(intent, user, duration)


chatbot = ChatBot()
