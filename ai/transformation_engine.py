"""
AI Fitness Assistant - Transformation Engine
Predicts body transformation based on current stats and time duration
"""

import math
from datetime import datetime, timedelta

class TransformationEngine:
    """
    AI engine for predicting body transformations
    Uses scientifically-backed formulas for realistic predictions
    """
    
    def __init__(self):
        self.body_types = {
            'ectomorph': {
                'muscle_gain_potential': 0.5,  # kg per month
                'fat_loss_rate': 0.3,  # kg per month
                'metabolism_factor': 1.2
            },
            'mesomorph': {
                'muscle_gain_potential': 0.8,
                'fat_loss_rate': 0.4,
                'metabolism_factor': 1.0
            },
            'endomorph': {
                'muscle_gain_potential': 0.6,
                'fat_loss_rate': 0.35,
                'metabolism_factor': 0.8
            }
        }
    
    def determine_body_type(self, height, weight, fitness_goal):
        """
        Determine body type based on height, weight, and goal
        
        Args:
            height (float): Height in cm
            weight (float): Weight in kg
            fitness_goal (str): 'weight_loss', 'muscle_gain', 'maintenance'
        
        Returns:
            str: Body type (ectomorph, mesomorph, endomorph)
        """
        bmi = weight / ((height / 100) ** 2)
        
        if fitness_goal == 'muscle_gain':
            if bmi < 20:
                return 'ectomorph'
            elif bmi < 25:
                return 'mesomorph'
            else:
                return 'endomorph'
        elif fitness_goal == 'weight_loss':
            if bmi > 30:
                return 'endomorph'
            elif bmi > 25:
                return 'mesomorph'
            else:
                return 'ectomorph'
        else:
            return 'mesomorph'
    
    def predict_weight_change(self, current_weight, fitness_goal, duration_months, body_type):
        """
        Predict weight change based on goal and duration
        
        Args:
            current_weight (float): Current weight in kg
            fitness_goal (str): 'weight_loss', 'muscle_gain', 'maintenance'
            duration_months (int): Duration in months
            body_type (str): Body type
        
        Returns:
            dict: Predicted weight and breakdown
        """
        stats = self.body_types.get(body_type, self.body_types['mesomorph'])
        
        if fitness_goal == 'weight_loss':
            # Monthly fat loss with minimum muscle loss
            monthly_loss = stats['fat_loss_rate'] * 1.1
            total_weight_loss = monthly_loss * duration_months
            
            # Realistic loss (losing some muscle too)
            fat_lost = total_weight_loss * 0.9
            muscle_lost = total_weight_loss * 0.1
            
            predicted_weight = current_weight - fat_lost - muscle_lost
            return {
                'predicted_weight': max(predicted_weight, 35),
                'weight_change': -(fat_lost + muscle_lost),
                'fat_lost': fat_lost,
                'muscle_lost': muscle_lost,
                'body_fat_reduction': fat_lost
            }
        
        elif fitness_goal == 'muscle_gain':
            # Monthly muscle gain with some fat gain
            monthly_gain = stats['muscle_gain_potential']
            total_muscle_gain = monthly_gain * duration_months
            
            # Realistic gain (gaining some fat too)
            muscle_gained = total_muscle_gain * 0.85
            fat_gained = total_muscle_gain * 0.15
            
            predicted_weight = current_weight + muscle_gained + fat_gained
            return {
                'predicted_weight': predicted_weight,
                'weight_change': muscle_gained + fat_gained,
                'muscle_gained': muscle_gained,
                'fat_gained': fat_gained,
                'body_fat_increase': fat_gained
            }
        
        else:  # maintenance
            return {
                'predicted_weight': current_weight,
                'weight_change': 0,
                'muscle_gained': 0,
                'fat_lost': 0,
                'status': 'Maintaining current weight'
            }
    
    def predict_body_measurements(self, current_measurements, fitness_goal, duration_months, body_type):
        """
        Predict body measurements change
        
        Args:
            current_measurements (dict): Current measurements (chest, waist, arms, legs)
            fitness_goal (str): Fitness goal
            duration_months (int): Duration in months
            body_type (str): Body type
        
        Returns:
            dict: Predicted measurements
        """
        predicted = current_measurements.copy()
        stats = self.body_types.get(body_type, self.body_types['mesomorph'])
        
        if fitness_goal == 'weight_loss':
            # Reduce measurements proportionally
            reduction_factor = 0.01 * duration_months  # 1% per month
            for key in ['chest', 'waist', 'arms', 'legs']:
                if key in predicted:
                    predicted[key] = predicted[key] * (1 - reduction_factor)
        
        elif fitness_goal == 'muscle_gain':
            # Increase measurements, especially arms and chest
            growth_factor = 0.015 * duration_months  # 1.5% per month
            predicted['chest'] = predicted.get('chest', 0) * (1 + growth_factor)
            predicted['arms'] = predicted.get('arms', 0) * (1 + growth_factor * 1.2)
            predicted['legs'] = predicted.get('legs', 0) * (1 + growth_factor * 0.8)
            predicted['waist'] = predicted.get('waist', 0) * (1 + growth_factor * 0.3)
        
        return predicted
    
    def predict_transformation(self, age, gender, height, weight, fitness_goal, 
                              duration_months, current_measurements=None):
        """
        Generate complete transformation prediction
        
        Args:
            age (int): Age
            gender (str): 'male' or 'female'
            height (float): Height in cm
            weight (float): Weight in kg
            fitness_goal (str): Fitness goal
            duration_months (int): Duration in months
            current_measurements (dict): Optional current measurements
        
        Returns:
            dict: Complete transformation prediction
        """
        body_type = self.determine_body_type(height, weight, fitness_goal)
        
        weight_prediction = self.predict_weight_change(
            weight, fitness_goal, duration_months, body_type
        )
        
        measurements_prediction = {}
        if current_measurements:
            measurements_prediction = self.predict_body_measurements(
                current_measurements, fitness_goal, duration_months, body_type
            )
        
        # Calculate difficulty and recommendation
        difficulty = 'Moderate'
        if duration_months <= 3:
            difficulty = 'Challenging'
        elif duration_months >= 12:
            difficulty = 'Achievable'
        
        recommendation = self._get_recommendation(
            fitness_goal, duration_months, weight, weight_prediction
        )
        
        # Generate before/after description
        before_description = self._generate_body_description(
            weight, height, gender, current_measurements, 'before'
        )
        after_description = self._generate_body_description(
            weight_prediction.get('predicted_weight', weight), height, gender, 
            measurements_prediction or current_measurements, 'after'
        )
        
        return {
            'success': True,
            'body_type': body_type,
            'duration_months': duration_months,
            'difficulty': difficulty,
            'before': {
                'weight': weight,
                'description': before_description,
                'measurements': current_measurements
            },
            'after': {
                'weight': weight_prediction.get('predicted_weight', weight),
                'weight_change': weight_prediction.get('weight_change', 0),
                'description': after_description,
                'measurements': measurements_prediction,
                'details': {
                    'muscle_gained': weight_prediction.get('muscle_gained', 
                                   weight_prediction.get('muscle_lost', 0)),
                    'fat_lost': weight_prediction.get('fat_lost', 0),
                    'fat_gained': weight_prediction.get('fat_gained', 0)
                }
            },
            'recommendation': recommendation,
            'tips': self._get_transformation_tips(fitness_goal, duration_months)
        }
    
    def _generate_body_description(self, weight, height, gender, measurements=None, phase='after'):
        """Generate descriptive text about body physique"""
        bmi = weight / ((height / 100) ** 2)
        
        descriptions = {
            'underweight': {
                'before': 'Thin build with minimal muscle definition',
                'after': 'Lean physique with visible muscle tone'
            },
            'normal': {
                'before': 'Average build with balanced proportions',
                'after': 'Fit and toned physique with good muscle definition'
            },
            'overweight': {
                'before': 'Soft build with excess body fat',
                'after': 'Athletic build with reduced body fat and better definition'
            },
            'obese': {
                'before': 'Heavy build with significant body fat',
                'after': 'Healthier weight with improved muscle tone'
            }
        }
        
        if bmi < 18.5:
            category = 'underweight'
        elif bmi < 25:
            category = 'normal'
        elif bmi < 30:
            category = 'overweight'
        else:
            category = 'obese'
        
        return descriptions.get(category, {}).get(phase, 'Transformed physique')
    
    def _get_recommendation(self, fitness_goal, duration_months, current_weight, weight_prediction):
        """Get recommendation based on prediction"""
        recommendations = {
            'weight_loss': {
                'calorie_deficit': '500-750 kcal/day',
                'workout_frequency': '4-5 times/week',
                'workout_type': 'Cardio + Light Strength Training',
                'diet_focus': 'High protein, low carb',
                'expected_result': f"Lose ~{abs(weight_prediction.get('weight_change', 0)):.1f}kg in {duration_months} months"
            },
            'muscle_gain': {
                'calorie_surplus': '250-500 kcal/day',
                'workout_frequency': '4-5 times/week',
                'workout_type': 'Heavy Strength Training',
                'diet_focus': 'High protein, moderate carb and fat',
                'expected_result': f"Gain ~{weight_prediction.get('muscle_gained', 0):.1f}kg muscle in {duration_months} months"
            },
            'maintenance': {
                'calories': 'Maintenance level',
                'workout_frequency': '3-4 times/week',
                'workout_type': 'Balanced Training',
                'diet_focus': 'Balanced macronutrients',
                'expected_result': 'Maintain current weight and improve fitness'
            }
        }
        
        return recommendations.get(fitness_goal, {})
    
    def _get_transformation_tips(self, fitness_goal, duration_months):
        """Get tips for successful transformation"""
        tips = {
            'weight_loss': [
                '🥗 Create a consistent calorie deficit',
                '💪 Incorporate strength training to preserve muscle',
                '🏃 Do cardio 3-4 times per week',
                '💧 Drink 3-4 liters of water daily',
                '😴 Get 7-8 hours of quality sleep',
                '⏰ Be patient - sustainable loss is 0.5-1kg per week'
            ],
            'muscle_gain': [
                '🏋️ Focus on compound exercises',
                '🥚 Eat 1.6-2.2g protein per kg body weight',
                '💪 Progressive overload - increase weight/reps regularly',
                '😴 Get 8+ hours of sleep for muscle recovery',
                '💧 Stay hydrated throughout the day',
                '⏰ Expect 0.5-1kg muscle gain per month'
            ],
            'maintenance': [
                '⚖️ Maintain consistent workout routine',
                '🥗 Eat at maintenance calorie level',
                '🏃 Mix cardio and strength training',
                '💪 Focus on improving strength and endurance',
                '😴 Prioritize sleep and recovery',
                '🎯 Set new fitness goals to stay motivated'
            ]
        }
        
        return tips.get(fitness_goal, tips['maintenance'])


# Create global instance
transformation_engine = TransformationEngine()

# Utility functions
def predict_transformation(age, gender, height, weight, fitness_goal, duration_months, 
                          current_measurements=None):
    """
    Predict body transformation
    
    Args:
        age, gender, height, weight, fitness_goal, duration_months, current_measurements
    
    Returns:
        Transformation prediction dict
    """
    return transformation_engine.predict_transformation(
        age, gender, height, weight, fitness_goal, 
        duration_months, current_measurements
    )
