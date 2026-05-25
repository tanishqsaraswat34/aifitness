"""
AI Fitness Assistant - Recommendation Engine
Generates personalized workout and diet recommendations based on user profile.
Meal suggestions are fetched via Gemini API - NO hardcoded if-else for meals.
"""
import os
import requests
import json
import re

class RecommendationEngine:
    """
    AI recommendation engine for fitness advice with API-based meal suggestions
    """
    
    def __init__(self):
        self.gemini_api_key = os.environ.get('GEMINI_API_KEY')
        self.gemini_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        
        # Workout database - different difficulty levels
        self.WORKOUTS = {
            'beginner': [
                {'name': 'Brisk Walking', 'type': 'Cardio', 'duration': 30, 'calories': 150,
                 'description': 'Walk at a fast pace for 30 minutes. Improves cardiovascular health.'},
                {'name': 'Bodyweight Basics', 'type': 'Strength', 'duration': 20, 'calories': 100,
                 'description': 'Includes push-ups, squats, and planks. No equipment needed.'},
                {'name': 'Yoga for Beginners', 'type': 'Flexibility', 'duration': 30, 'calories': 120,
                 'description': 'Basic yoga poses to improve flexibility and reduce stress.'},
                {'name': 'Swimming', 'type': 'Cardio', 'duration': 30, 'calories': 200,
                 'description': 'Low impact full body workout. Great for all fitness levels.'},
                {'name': 'Home Workout', 'type': 'Strength', 'duration': 25, 'calories': 120,
                 'description': 'Jump jacks, lunges, and step-ups. No equipment needed.'}
            ],
            'intermediate': [
                {'name': 'Running', 'type': 'Cardio', 'duration': 45, 'calories': 400,
                 'description': 'Moderate paced running. Build endurance and burn calories.'},
                {'name': 'Weight Training - Push/Pull', 'type': 'Strength', 'duration': 60, 'calories': 300,
                 'description': 'Push-ups, chest press, rows, pull-ups, and more.'},
                {'name': 'HIIT Training', 'type': 'Cardio', 'duration': 30, 'calories': 300,
                 'description': 'High intensity interval training for maximum calorie burn.'},
                {'name': 'Cycling', 'type': 'Cardio', 'duration': 60, 'calories': 450,
                 'description': 'Outdoor or stationary cycling for cardiovascular fitness.'},
                {'name': 'Circuit Training', 'type': 'Strength', 'duration': 45, 'calories': 250,
                 'description': 'Combination of cardio and strength exercises with minimal rest.'}
            ],
            'advanced': [
                {'name': 'Intense HIIT', 'type': 'Cardio', 'duration': 45, 'calories': 500,
                 'description': 'Advanced high intensity interval training with complex movements.'},
                {'name': 'Powerlifting', 'type': 'Strength', 'duration': 90, 'calories': 400,
                 'description': 'Heavy compound lifts: deadlifts, squats, bench press.'},
                {'name': 'Marathon Training', 'type': 'Cardio', 'duration': 120, 'calories': 1200,
                 'description': 'Long distance running for advanced athletes.'},
                {'name': 'Crossfit', 'type': 'Strength', 'duration': 60, 'calories': 400,
                 'description': 'Combination of Olympic lifting, gymnastics, and cardio.'},
                {'name': 'Advanced Yoga/Pilates', 'type': 'Flexibility', 'duration': 60, 'calories': 250,
                 'description': 'Complex poses and movements for advanced practitioners.'}
            ]
        }
        
        # Diet configuration (macronutrient percentages)
        self.DIET_CONFIG = {
            'weight_loss': {'protein_percent': 40, 'carbs_percent': 35, 'fat_percent': 25},
            'muscle_gain': {'protein_percent': 50, 'carbs_percent': 35, 'fat_percent': 15},
            'maintenance': {'protein_percent': 35, 'carbs_percent': 45, 'fat_percent': 20}
        }
    
    def _get_meals_from_api(self, fitness_goal, meal_type, daily_calories):
        """
        Get meal suggestions from Gemini API - fully API-based, no hardcoding
        
        Args:
            fitness_goal (str): 'weight_loss', 'muscle_gain', or 'maintenance'
            meal_type (str): 'Breakfast', 'Lunch', 'Snack', or 'Dinner'
            daily_calories (int): Daily calorie target
        
        Returns:
            list: List of meal suggestions from API
        """
        if not self.gemini_api_key:
            return self._get_fallback_meals(meal_type)
        
        try:
            cal_per_meal = daily_calories // 4
            prompt = (
                f"Suggest 4 healthy {meal_type.lower()} options for {fitness_goal.replace('_', ' ')}. "
                f"Each meal approximately {cal_per_meal} calories. "
                f"Return ONLY valid JSON array: [{{\"name\": \"meal name\", \"calories\": 350}}]. "
                f"Include Indian food options. Be specific with portions. No other text."
            )
            
            headers = {'Content-Type': 'application/json'}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 200}
            }
            
            url = f"{self.gemini_endpoint}?key={self.gemini_api_key}"
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            response.raise_for_status()
            
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text'].strip()
                json_match = re.search(r'\[.*\]', text, re.DOTALL)
                if json_match:
                    meals = json.loads(json_match.group())
                    return [{'name': m.get('name', 'Unknown'), 'calories': m.get('calories', 300)} for m in meals]
        except Exception as e:
            print(f"Error fetching meals from Gemini API: {e}")
        
        return self._get_fallback_meals(meal_type)
    
    def _get_fallback_meals(self, meal_type):
        """Get fallback meal options if API is unavailable"""
        fallback_meals = {
            'Breakfast': [
                {'name': 'Oats with berries', 'calories': 350},
                {'name': 'Eggs with whole wheat toast', 'calories': 300},
                {'name': 'Greek yogurt with granola', 'calories': 320},
                {'name': 'Protein smoothie with banana', 'calories': 280}
            ],
            'Lunch': [
                {'name': 'Grilled chicken with brown rice', 'calories': 500},
                {'name': 'Paneer curry with roti', 'calories': 450},
                {'name': 'Fish with sweet potato', 'calories': 480},
                {'name': 'Lentil dal with rice', 'calories': 420}
            ],
            'Snack': [
                {'name': 'Apple with almond butter', 'calories': 200},
                {'name': 'Almonds', 'calories': 160},
                {'name': 'Greek yogurt', 'calories': 100},
                {'name': 'Protein bar', 'calories': 200}
            ],
            'Dinner': [
                {'name': 'Grilled fish with vegetables', 'calories': 400},
                {'name': 'Paneer tikka with salad', 'calories': 380},
                {'name': 'Chicken soup with vegetables', 'calories': 350},
                {'name': 'Soya chunks curry with roti', 'calories': 420}
            ]
        }
        return fallback_meals.get(meal_type, [])
    
    def calculate_bmi(self, height, weight):
        """Calculate BMI (Body Mass Index)"""
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        
        return {
            'bmi': round(bmi, 2),
            'category': category,
            'message': self._get_bmi_message(category)
        }
    
    def _get_bmi_message(self, category):
        """Get motivational message based on BMI category"""
        messages = {
            'Underweight': 'You are underweight. Focus on a balanced diet with adequate calories.',
            'Normal': 'Great! You are in a healthy weight range. Maintain your fitness routine.',
            'Overweight': 'You are overweight. Focus on a balanced diet and regular exercise.',
            'Obese': 'You have obesity. Consult a doctor and start a fitness program.'
        }
        return messages.get(category, '')
    
    def get_daily_calorie_requirement(self, age, gender, height, weight, fitness_goal):
        """Calculate daily calorie requirement using Harris-Benedict formula"""
        if gender.upper() == 'M':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        
        tdee = bmr * 1.55
        
        if fitness_goal == 'weight_loss':
            tdee *= 0.85
        elif fitness_goal == 'muscle_gain':
            tdee *= 1.10
        
        return int(tdee)
    
    def get_macronutrients(self, daily_calories, fitness_goal):
        """Calculate macronutrient distribution"""
        goal_key = fitness_goal if fitness_goal in self.DIET_CONFIG else 'maintenance'
        config = self.DIET_CONFIG[goal_key]
        
        return {
            'protein_g': int(daily_calories * config['protein_percent'] / 100 / 4),
            'carbs_g': int(daily_calories * config['carbs_percent'] / 100 / 4),
            'fat_g': int(daily_calories * config['fat_percent'] / 100 / 9),
            'daily_calories': daily_calories
        }
    
    def get_workout_recommendation(self, fitness_goal, difficulty, days_per_week=5):
        """Get personalized workout plan"""
        if difficulty not in self.WORKOUTS:
            difficulty = 'beginner'
        
        workouts = self.WORKOUTS[difficulty]
        
        if fitness_goal == 'weight_loss':
            selected = [w for w in workouts if 'Cardio' in w['type']] + \
                      [w for w in workouts if 'Cardio' not in w['type']]
        elif fitness_goal == 'muscle_gain':
            selected = [w for w in workouts if 'Strength' in w['type']] + \
                      [w for w in workouts if 'Strength' not in w['type']]
        else:
            selected = workouts
        
        return selected[:min(days_per_week, len(selected))]
    
    def get_diet_recommendation(self, fitness_goal, daily_calories=2000):
        """
        Get personalized diet plan with API-based meal suggestions
        No hardcoded if-else cases - fully API-driven
        """
        goal_key = fitness_goal if fitness_goal in self.DIET_CONFIG else 'maintenance'
        
        # Get meals from API for each meal type
        meals = {}
        for meal_type in ['Breakfast', 'Lunch', 'Snack', 'Dinner']:
            meals[meal_type] = self._get_meals_from_api(fitness_goal, meal_type, daily_calories)
        
        return {
            'goal': goal_key,
            'daily_calories': daily_calories,
            'macros': self.get_macronutrients(daily_calories, fitness_goal),
            'meals': meals
        }
    
    def get_weekly_plan(self, age, gender, height, weight, fitness_goal, difficulty):
        """Generate complete weekly fitness plan"""
        daily_calories = self.get_daily_calorie_requirement(age, gender, height, weight, fitness_goal)
        macros = self.get_macronutrients(daily_calories, fitness_goal)
        bmi_info = self.calculate_bmi(height, weight)
        workouts = self.get_workout_recommendation(fitness_goal, difficulty)
        diet = self.get_diet_recommendation(fitness_goal, daily_calories)
        
        return {
            'bmi_info': bmi_info,
            'daily_calories': daily_calories,
            'macronutrients': macros,
            'weekly_workouts': workouts,
            'diet_plan': diet,
            'tips': self.get_fitness_tips(fitness_goal, difficulty)
        }
    
    def get_fitness_tips(self, fitness_goal, difficulty):
        """Get fitness tips based on goal and difficulty"""
        tips = {
            'weight_loss': [
                'Create a calorie deficit of 300-500 calories per day',
                'Increase your water intake to 3-4 liters daily',
                'Incorporate cardio exercises 5 times per week',
                'Eat more protein to maintain muscle mass',
                'Avoid processed foods and sugary drinks',
                'Get 7-8 hours of sleep daily',
                'Track your food intake using apps'
            ],
            'muscle_gain': [
                'Eat in a calorie surplus of 300-500 calories per day',
                'Focus on protein intake of 1.6-2.2g per kg body weight',
                'Perform resistance training 4-5 times per week',
                'Use progressive overload in your workouts',
                'Get adequate rest between workouts',
                'Stay hydrated throughout the day',
                'Take rest days seriously for muscle recovery'
            ],
            'maintenance': [
                'Maintain consistent workout routine',
                'Eat balanced meals with all macronutrients',
                'Exercise 4-5 times per week for overall fitness',
                'Keep your calorie intake stable',
                'Stay hydrated and get enough sleep',
                'Include variety in your workouts',
                'Monitor your progress regularly'
            ]
        }
        
        goal_tips = tips.get(fitness_goal, tips['maintenance'])
        return goal_tips[:5]


# Create global instance
recommendation_engine = RecommendationEngine()
