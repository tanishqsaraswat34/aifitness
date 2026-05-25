"""
AI Fitness Assistant - Database Models
This module contains all database schema and operations using SQLite
"""

import sqlite3
import os
from datetime import datetime
import hashlib

# Database file location
DB_PATH = 'database.db'

def get_db_connection():
    """
    Create and return a database connection
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initialize the database with all required tables
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            height REAL,
            weight REAL,
            fitness_goal TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Create Workouts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            workout_type TEXT NOT NULL,
            name TEXT NOT NULL,
            duration INTEGER,
            difficulty TEXT,
            calories_burned INTEGER,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create Diet Logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diet_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            meal_type TEXT NOT NULL,
            food_item TEXT NOT NULL,
            quantity REAL,
            calories INTEGER,
            protein REAL,
            carbs REAL,
            fat REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create Calorie Logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calorie_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            calories_consumed INTEGER,
            calories_burned INTEGER,
            water_intake REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create Progress Logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            weight REAL,
            body_fat REAL,
            chest REAL,
            waist REAL,
            arms REAL,
            legs REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create Recommendations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            recommendation_type TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """
    Hash password using SHA256
    """
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password, name, age, gender, height, weight, fitness_goal):
    """
    Create a new user
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        hashed_password = hash_password(password)
        
        cursor.execute('''
            INSERT INTO users (username, email, password, name, age, gender, height, weight, fitness_goal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, email, hashed_password, name, age, gender, height, weight, fitness_goal))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user(username):
    """
    Get user by username
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_password(stored_password, provided_password):
    """
    Verify password
    """
    return stored_password == hash_password(provided_password)

def update_user_profile(user_id, age, height, weight, fitness_goal):
    """
    Update user profile information
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET age = ?, height = ?, weight = ?, fitness_goal = ?
        WHERE id = ?
    ''', (age, height, weight, fitness_goal, user_id))
    conn.commit()
    conn.close()

def add_workout(user_id, workout_type, name, duration, difficulty, calories_burned):
    """
    Add a workout log
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO workouts (user_id, workout_type, name, duration, difficulty, calories_burned)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, workout_type, name, duration, difficulty, calories_burned))
    conn.commit()
    conn.close()

def add_diet_log(user_id, meal_type, food_item, quantity, calories, protein, carbs, fat):
    """
    Add a diet log entry
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO diet_logs (user_id, meal_type, food_item, quantity, calories, protein, carbs, fat)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, meal_type, food_item, quantity, calories, protein, carbs, fat))
    conn.commit()
    conn.close()

def add_calorie_log(user_id, calories_consumed, calories_burned, water_intake):
    """
    Add a calorie log entry
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO calorie_logs (user_id, calories_consumed, calories_burned, water_intake)
        VALUES (?, ?, ?, ?)
    ''', (user_id, calories_consumed, calories_burned, water_intake))
    conn.commit()
    conn.close()

def add_progress_log(user_id, weight, body_fat=None, chest=None, waist=None, arms=None, legs=None):
    """
    Add a progress log entry
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO progress_logs (user_id, weight, body_fat, chest, waist, arms, legs)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, weight, body_fat, chest, waist, arms, legs))
    conn.commit()
    conn.close()

def get_user_workouts(user_id, limit=10):
    """
    Get recent workouts for a user
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM workouts WHERE user_id = ?
        ORDER BY date DESC LIMIT ?
    ''', (user_id, limit))
    workouts = cursor.fetchall()
    conn.close()
    return workouts

def get_user_diet_logs(user_id, limit=10):
    """
    Get recent diet logs for a user
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM diet_logs WHERE user_id = ?
        ORDER BY date DESC LIMIT ?
    ''', (user_id, limit))
    logs = cursor.fetchall()
    conn.close()
    return logs

def get_user_progress_logs(user_id, limit=10):
    """
    Get recent progress logs for a user
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM progress_logs WHERE user_id = ?
        ORDER BY date DESC LIMIT ?
    ''', (user_id, limit))
    logs = cursor.fetchall()
    conn.close()
    return logs

def get_daily_calorie_summary(user_id, date):
    """
    Get calorie summary for a specific date
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get total calories consumed
    cursor.execute('''
        SELECT SUM(calories) FROM diet_logs 
        WHERE user_id = ? AND DATE(date) = ?
    ''', (user_id, date))
    consumed = cursor.fetchone()[0] or 0
    
    # Get total calories burned from workouts
    cursor.execute('''
        SELECT SUM(calories_burned) FROM workouts 
        WHERE user_id = ? AND DATE(date) = ? AND completed = 1
    ''', (user_id, date))
    burned = cursor.fetchone()[0] or 0
    
    conn.close()
    return {'consumed': consumed, 'burned': burned}

# Initialize database when module is imported
if not os.path.exists(DB_PATH):
    init_db()
