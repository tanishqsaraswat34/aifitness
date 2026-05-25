"""
AI Fitness Assistant - Analytics Module
Generates charts and analytics for fitness tracking
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64
from datetime import datetime, timedelta
from models.database import get_db_connection

class Analytics:
    """
    Class for generating analytics and charts
    """
    
    @staticmethod
    def get_weight_trend(user_id, days=30):
        """
        Get weight trend data
        
        Args:
            user_id (int): User ID
            days (int): Number of days to show
        
        Returns:
            dict: Dates and weights
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        start_date = datetime.now() - timedelta(days=days)
        
        cursor.execute('''
            SELECT date, weight FROM progress_logs
            WHERE user_id = ? AND date >= ?
            ORDER BY date
        ''', (user_id, start_date.isoformat()))
        
        data = cursor.fetchall()
        conn.close()
        
        dates = [row[0] for row in data]
        weights = [row[1] for row in data]
        
        return {'dates': dates, 'weights': weights}
    
    @staticmethod
    def get_calorie_trend(user_id, days=30):
        """
        Get calorie trend data
        
        Args:
            user_id (int): User ID
            days (int): Number of days to show
        
        Returns:
            dict: Dates, consumed, and burned calories
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        start_date = datetime.now() - timedelta(days=days)
        
        # Get consumed calories
        cursor.execute('''
            SELECT DATE(date), SUM(calories) FROM diet_logs
            WHERE user_id = ? AND date >= ?
            GROUP BY DATE(date)
            ORDER BY DATE(date)
        ''', (user_id, start_date.isoformat()))
        
        consumed_data = cursor.fetchall()
        
        # Get burned calories
        cursor.execute('''
            SELECT DATE(date), SUM(calories_burned) FROM workouts
            WHERE user_id = ? AND date >= ? AND completed = 1
            GROUP BY DATE(date)
            ORDER BY DATE(date)
        ''', (user_id, start_date.isoformat()))
        
        burned_data = cursor.fetchall()
        conn.close()
        
        dates = [row[0] for row in consumed_data] if consumed_data else []
        consumed = [row[1] or 0 for row in consumed_data] if consumed_data else []
        burned = [row[1] or 0 for row in burned_data] if burned_data else []
        
        return {
            'dates': dates,
            'consumed': consumed,
            'burned': burned
        }
    
    @staticmethod
    def get_workout_stats(user_id, days=30):
        """
        Get workout statistics
        
        Args:
            user_id (int): User ID
            days (int): Number of days to show
        
        Returns:
            dict: Workout statistics
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        start_date = datetime.now() - timedelta(days=days)
        
        # Total workouts
        cursor.execute('''
            SELECT COUNT(*) FROM workouts
            WHERE user_id = ? AND date >= ? AND completed = 1
        ''', (user_id, start_date.isoformat()))
        total_workouts = cursor.fetchone()[0]
        
        # Total calories burned
        cursor.execute('''
            SELECT SUM(calories_burned) FROM workouts
            WHERE user_id = ? AND date >= ? AND completed = 1
        ''', (user_id, start_date.isoformat()))
        total_calories = cursor.fetchone()[0] or 0
        
        # Workouts by type
        cursor.execute('''
            SELECT workout_type, COUNT(*) FROM workouts
            WHERE user_id = ? AND date >= ? AND completed = 1
            GROUP BY workout_type
        ''', (user_id, start_date.isoformat()))
        
        type_data = cursor.fetchall()
        conn.close()
        
        return {
            'total_workouts': total_workouts,
            'total_calories': total_calories,
            'by_type': dict(type_data) if type_data else {}
        }
    
    @staticmethod
    def create_weight_chart(user_id, days=30):
        """
        Create weight trend chart
        
        Args:
            user_id (int): User ID
            days (int): Number of days
        
        Returns:
            str: Base64 encoded chart image
        """
        data = Analytics.get_weight_trend(user_id, days)
        
        if not data['dates']:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(data['dates'], data['weights'], marker='o', color='#2196F3', linewidth=2)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Weight (kg)', fontsize=12)
        ax.set_title('Weight Trend', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Convert to base64
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        chart_data = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return chart_data
    
    @staticmethod
    def create_calorie_chart(user_id, days=30):
        """
        Create calorie comparison chart
        
        Args:
            user_id (int): User ID
            days (int): Number of days
        
        Returns:
            str: Base64 encoded chart image
        """
        data = Analytics.get_calorie_trend(user_id, days)
        
        if not data['dates']:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        x = range(len(data['dates']))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], data['consumed'], width, label='Consumed', color='#FF6B6B')
        ax.bar([i + width/2 for i in x], data['burned'], width, label='Burned', color='#51CF66')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Calories', fontsize=12)
        ax.set_title('Daily Calories: Consumed vs Burned', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(data['dates'], rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        # Convert to base64
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        chart_data = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return chart_data
    
    @staticmethod
    def create_workout_type_chart(user_id, days=30):
        """
        Create workout type distribution chart
        
        Args:
            user_id (int): User ID
            days (int): Number of days
        
        Returns:
            str: Base64 encoded chart image
        """
        stats = Analytics.get_workout_stats(user_id, days)
        
        if not stats['by_type']:
            return None
        
        fig, ax = plt.subplots(figsize=(8, 8))
        types = list(stats['by_type'].keys())
        counts = list(stats['by_type'].values())
        colors = ['#2196F3', '#FF9800', '#4CAF50', '#F44336', '#9C27B0']
        
        ax.pie(counts, labels=types, autopct='%1.1f%%', colors=colors[:len(types)], startangle=90)
        ax.set_title('Workout Type Distribution', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        # Convert to base64
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        chart_data = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return chart_data
    
    @staticmethod
    def get_summary_stats(user_id, days=30):
        """
        Get summary statistics
        
        Args:
            user_id (int): User ID
            days (int): Number of days
        
        Returns:
            dict: Summary statistics
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        start_date = datetime.now() - timedelta(days=days)
        
        # Current weight
        cursor.execute('''
            SELECT weight FROM progress_logs
            WHERE user_id = ?
            ORDER BY date DESC LIMIT 1
        ''', (user_id,))
        current_weight = cursor.fetchone()[0] if cursor.fetchone() else 0
        
        # Total workouts
        cursor.execute('''
            SELECT COUNT(*) FROM workouts
            WHERE user_id = ? AND date >= ? AND completed = 1
        ''', (user_id, start_date.isoformat()))
        total_workouts = cursor.fetchone()[0]
        
        # Total calories burned
        cursor.execute('''
            SELECT SUM(calories_burned) FROM workouts
            WHERE user_id = ? AND date >= ? AND completed = 1
        ''', (user_id, start_date.isoformat()))
        total_calories_burned = cursor.fetchone()[0] or 0
        
        # Average daily calories
        cursor.execute('''
            SELECT AVG(daily_calories) FROM (
                SELECT SUM(calories_burned) as daily_calories
                FROM workouts
                WHERE user_id = ? AND date >= ? AND completed = 1
                GROUP BY DATE(date)
            )
        ''', (user_id, start_date.isoformat()))
        avg_daily_calories = int(cursor.fetchone()[0]) if cursor.fetchone()[0] else 0
        
        conn.close()
        
        return {
            'current_weight': current_weight,
            'total_workouts': total_workouts,
            'total_calories_burned': total_calories_burned,
            'avg_daily_calories': avg_daily_calories
        }

# Create global instance
analytics = Analytics()
