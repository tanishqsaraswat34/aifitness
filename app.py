"""
AI Fitness Assistant - Main Flask Application
Complete backend with authentication, recommendations, and tracking
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from datetime import datetime, timedelta
import os
import sys
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import custom modules
from models.database import (
    init_db, create_user, get_user, verify_password, update_user_profile,
    add_workout, add_diet_log, add_calorie_log, add_progress_log,
    get_user_workouts, get_user_diet_logs, get_user_progress_logs,
    get_daily_calorie_summary, get_db_connection
)
from flask_socketio import SocketIO, emit
from ai.recommendation_engine import recommendation_engine
from ai.transformation_engine import transformation_engine
from ai.image_processor import image_processor
from ai.chatbot import chatbot
from charts.analytics import analytics
from voice.speech_output import get_random_quote

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')

# Initialize database
init_db()

# ===================== AUTHENTICATION ROUTES =====================

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.json
        
        # Validate input
        if not all([data.get('username'), data.get('email'), data.get('password'), 
                   data.get('name'), data.get('age'), data.get('gender'),
                   data.get('height'), data.get('weight'), data.get('fitness_goal')]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Create user
        if create_user(
            data['username'],
            data['email'],
            data['password'],
            data['name'],
            int(data['age']),
            data['gender'],
            float(data['height']),
            float(data['weight']),
            data['fitness_goal']
        ):
            return jsonify({'success': True, 'message': 'Registration successful! Please login.'})
        else:
            return jsonify({'success': False, 'message': 'Username or email already exists'}), 400
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'}), 400
        
        user = get_user(username)
        if user and verify_password(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 400
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('login'))

# ===================== DASHBOARD ROUTES =====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/dashboard-data')
@login_required
def get_dashboard_data():
    """Get dashboard statistics"""
    user_id = session['user_id']
    
    # Get user info
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    # Calculate BMI
    bmi_info = recommendation_engine.calculate_bmi(user['height'], user['weight'])
    
    # Get summary stats
    summary = analytics.get_summary_stats(user_id)
    
    # Get charts
    weight_chart = analytics.create_weight_chart(user_id)
    calorie_chart = analytics.create_calorie_chart(user_id)
    workout_chart = analytics.create_workout_type_chart(user_id)
    
    # Get recent workouts
    workouts = get_user_workouts(user_id, 5)
    workouts_list = [dict(w) for w in workouts] if workouts else []
    
    return jsonify({
        'success': True,
        'user': {
            'name': user['name'],
            'age': user['age'],
            'height': user['height'],
            'weight': user['weight'],
            'fitness_goal': user['fitness_goal']
        },
        'bmi': bmi_info,
        'summary': summary,
        'charts': {
            'weight': weight_chart,
            'calorie': calorie_chart,
            'workout': workout_chart
        },
        'recent_workouts': workouts_list
    })

# ===================== RECOMMENDATION ROUTES =====================

@app.route('/api/recommendations')
@login_required
def get_recommendations():
    """Get personalized recommendations"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    # Determine difficulty
    bmi_info = recommendation_engine.calculate_bmi(user['height'], user['weight'])
    if bmi_info['category'] == 'Underweight' or bmi_info['category'] == 'Normal':
        difficulty = 'beginner'
    elif bmi_info['category'] == 'Overweight':
        difficulty = 'intermediate'
    else:
        difficulty = 'beginner'
    
    # Get complete plan
    plan = recommendation_engine.get_weekly_plan(
        user['age'],
        user['gender'],
        user['height'],
        user['weight'],
        user['fitness_goal'],
        difficulty
    )
    
    return jsonify({'success': True, 'plan': plan})

@app.route('/workout')
@login_required
def workout():
    """Workout recommendation page"""
    return render_template('workout.html')

@app.route('/diet')
@login_required
def diet():
    """Diet recommendation page"""
    return render_template('diet.html')

@app.route('/api/diet-plan')
@login_required
def get_diet_plan():
    """Get diet plan"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT fitness_goal FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    diet_plan = recommendation_engine.get_diet_recommendation(user['fitness_goal'])
    
    return jsonify({'success': True, 'diet_plan': diet_plan})

# ===================== TRACKING ROUTES =====================

@app.route('/tracker')
@login_required
def tracker():
    """Tracking page"""
    return render_template('tracker.html')

@app.route('/api/track-workout', methods=['POST'])
@login_required
def track_workout():
    """Track a workout"""
    data = request.json
    user_id = session['user_id']
    
    try:
        add_workout(
            user_id,
            data.get('workout_type', 'General'),
            data.get('name'),
            int(data.get('duration', 0)),
            data.get('difficulty', 'Beginner'),
            int(data.get('calories_burned', 0))
        )
        return jsonify({'success': True, 'message': 'Workout tracked successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/track-diet', methods=['POST'])
@login_required
def track_diet():
    """Track diet"""
    data = request.json
    user_id = session['user_id']
    
    try:
        add_diet_log(
            user_id,
            data.get('meal_type', 'Other'),
            data.get('food_item'),
            float(data.get('quantity', 0)),
            int(data.get('calories', 0)),
            float(data.get('protein', 0)),
            float(data.get('carbs', 0)),
            float(data.get('fat', 0))
        )
        return jsonify({'success': True, 'message': 'Diet logged successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/track-weight', methods=['POST'])
@login_required
def track_weight():
    """Track weight"""
    data = request.json
    user_id = session['user_id']
    
    try:
        add_progress_log(
            user_id,
            float(data.get('weight')),
            float(data.get('body_fat', 0)) if data.get('body_fat') else None,
            float(data.get('chest', 0)) if data.get('chest') else None,
            float(data.get('waist', 0)) if data.get('waist') else None,
            float(data.get('arms', 0)) if data.get('arms') else None,
            float(data.get('legs', 0)) if data.get('legs') else None
        )
        return jsonify({'success': True, 'message': 'Weight tracked successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/daily-summary')
@login_required
def daily_summary():
    """Get daily calorie summary"""
    user_id = session['user_id']
    date = request.args.get('date', datetime.now().date().isoformat())
    
    summary = get_daily_calorie_summary(user_id, date)
    
    return jsonify({
        'success': True,
        'date': date,
        'summary': summary
    })

# ===================== PROFILE ROUTES =====================

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('profile.html')

@app.route('/api/profile')
@login_required
def get_profile():
    """Get user profile"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'name': user['name'],
            'age': user['age'],
            'gender': user['gender'],
            'height': user['height'],
            'weight': user['weight'],
            'fitness_goal': user['fitness_goal'],
            'created_at': user['created_at']
        }
    })

@app.route('/api/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Update user profile"""
    data = request.json
    user_id = session['user_id']
    
    try:
        update_user_profile(
            user_id,
            int(data.get('age')),
            float(data.get('height')),
            float(data.get('weight')),
            data.get('fitness_goal')
        )
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# ===================== UTILITY ROUTES =====================

@app.route('/api/quote')
def get_quote():
    """Get a motivational quote"""
    quote = get_random_quote()
    return jsonify({'success': True, 'quote': quote})

@app.route('/api/calculate-bmi', methods=['POST'])
def calculate_bmi():
    """Calculate BMI"""
    data = request.json
    height = float(data.get('height', 0))
    weight = float(data.get('weight', 0))
    
    if height <= 0 or weight <= 0:
        return jsonify({'success': False, 'message': 'Invalid height or weight'}), 400
    
    bmi_info = recommendation_engine.calculate_bmi(height, weight)
    return jsonify({'success': True, 'bmi': bmi_info})

# ===================== AI SMART INSIGHTS =====================

@app.route('/api/ai-insights')
@login_required
def get_ai_insights():
    """Get AI-powered personalized insights and recommendations"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    # Calculate BMI
    bmi_info = recommendation_engine.calculate_bmi(user['height'], user['weight'])
    
    # Get user activity
    workouts = get_user_workouts(user_id, 30)
    diet_logs = get_user_diet_logs(user_id, 30)
    progress_logs = get_user_progress_logs(user_id, 30)
    
    # AI Logic: Generate insights based on activity
    insights = []
    
    # Insight 1: Activity level analysis
    if workouts:
        workout_count = len([w for w in workouts if w['completed']])
        days_active = len(set([w['date'] for w in workouts if w['completed']]))
        avg_workouts_per_week = (workout_count / 4.3) if workout_count > 0 else 0
        
        if avg_workouts_per_week >= 4:
            insights.append({
                'title': '💪 Excellent Consistency!',
                'message': f'You\'ve completed {workout_count} workouts this month! Keep up this amazing momentum.',
                'type': 'positive'
            })
        elif avg_workouts_per_week >= 2:
            insights.append({
                'title': '🎯 Good Progress!',
                'message': f'You\'ve been working out {days_active} days per week. Try to add one more day for even better results.',
                'type': 'info'
            })
        else:
            insights.append({
                'title': '📈 Increase Activity',
                'message': 'You\'ve logged few workouts. Try to exercise at least 3 times per week for optimal fitness goals.',
                'type': 'suggestion'
            })
    else:
        insights.append({
            'title': '🚀 Start Your Journey!',
            'message': 'Begin logging your workouts to get personalized AI insights and track your progress!',
            'type': 'motivation'
        })
    
    # Insight 2: Weight trend analysis
    if len(progress_logs) >= 2:
        recent_weight = progress_logs[0]['weight']
        previous_weight = progress_logs[-1]['weight']
        weight_change = recent_weight - previous_weight
        
        if weight_change < -1:
            insights.append({
                'title': '⬇️ Weight Loss Progress!',
                'message': f'Great job! You\'ve lost {abs(weight_change):.1f}kg this month. Continue your efforts!',
                'type': 'positive'
            })
        elif weight_change > 1:
            insights.append({
                'title': '⬆️ Muscle Gain!',
                'message': f'You\'ve gained {weight_change:.1f}kg. Combined with workouts, this might be muscle gain!',
                'type': 'info'
            })
    
    # Insight 3: Diet consistency
    if diet_logs:
        diet_days = len(set([d['date'] for d in diet_logs]))
        if diet_days >= 20:
            insights.append({
                'title': '🥗 Excellent Tracking!',
                'message': f'You\'ve tracked food {diet_days} days this month. This consistency helps your success!',
                'type': 'positive'
            })
        elif diet_days < 10:
            insights.append({
                'title': '📋 Improve Tracking',
                'message': 'Logging your meals helps optimize your fitness plan. Try to log daily!',
                'type': 'suggestion'
            })
    
    # Insight 4: Goal-based recommendation
    if user['fitness_goal'] == 'weight_loss':
        insights.append({
            'title': '💪 Weight Loss Strategy',
            'message': 'Focus on cardio (running, cycling) 4x/week and maintain a calorie deficit. Consistency is key!',
            'type': 'tip'
        })
    elif user['fitness_goal'] == 'muscle_gain':
        insights.append({
            'title': '🏋️ Muscle Building Strategy',
            'message': 'Prioritize strength training 4-5x/week with high protein intake. Progressive overload wins!',
            'type': 'tip'
        })
    elif user['fitness_goal'] == 'general_fitness':
        insights.append({
            'title': '⚖️ Balanced Fitness',
            'message': 'Mix cardio (3x/week) and strength (2x/week) training for overall health and fitness.',
            'type': 'tip'
        })
    
    return jsonify({
        'success': True,
        'insights': insights,
        'bmi': bmi_info
    })

@app.route('/api/ai-meal-suggestions')
@login_required
def get_ai_meal_suggestions():
    """Get AI-powered meal suggestions based on user preferences and goals"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT fitness_goal, age, gender FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    # AI meal suggestions based on goal and time
    suggestions = {
        'breakfast': [],
        'lunch': [],
        'dinner': [],
        'snack': []
    }
    
    goal = user['fitness_goal']
    
    # High protein options
    if goal == 'muscle_gain':
        suggestions['breakfast'] = [
            {'item': 'Oatmeal with eggs and almonds', 'calories': 450, 'protein': 25, 'carbs': 45, 'fat': 15},
            {'item': 'Greek yogurt with granola and berries', 'calories': 350, 'protein': 20, 'carbs': 40, 'fat': 8},
            {'item': 'Protein pancakes with honey', 'calories': 400, 'protein': 30, 'carbs': 45, 'fat': 8}
        ]
        suggestions['lunch'] = [
            {'item': 'Grilled chicken breast with rice and broccoli', 'calories': 600, 'protein': 45, 'carbs': 55, 'fat': 10},
            {'item': 'Salmon with quinoa and vegetables', 'calories': 650, 'protein': 40, 'carbs': 50, 'fat': 20},
            {'item': 'Lean beef with sweet potato and greens', 'calories': 700, 'protein': 50, 'carbs': 60, 'fat': 15}
        ]
        suggestions['dinner'] = [
            {'item': 'Turkey meatballs with whole wheat pasta', 'calories': 550, 'protein': 40, 'carbs': 55, 'fat': 12},
            {'item': 'Baked tilapia with potatoes and asparagus', 'calories': 500, 'protein': 35, 'carbs': 50, 'fat': 10},
            {'item': 'Lean chicken curry with basmati rice', 'calories': 600, 'protein': 38, 'carbs': 65, 'fat': 12}
        ]
        suggestions['snack'] = [
            {'item': 'Protein shake with banana', 'calories': 250, 'protein': 25, 'carbs': 25, 'fat': 3},
            {'item': 'Greek yogurt with nuts', 'calories': 200, 'protein': 15, 'carbs': 15, 'fat': 8},
            {'item': 'Peanut butter and whole wheat bread', 'calories': 300, 'protein': 12, 'carbs': 30, 'fat': 14}
        ]
    
    elif goal == 'weight_loss':
        suggestions['breakfast'] = [
            {'item': 'Egg white omelet with vegetables', 'calories': 200, 'protein': 15, 'carbs': 10, 'fat': 8},
            {'item': 'Oatmeal with berries and cinnamon', 'calories': 250, 'protein': 8, 'carbs': 45, 'fat': 3},
            {'item': 'Smoothie bowl with greens and fruits', 'calories': 280, 'protein': 12, 'carbs': 45, 'fat': 3}
        ]
        suggestions['lunch'] = [
            {'item': 'Grilled chicken salad with olive oil dressing', 'calories': 350, 'protein': 30, 'carbs': 20, 'fat': 12},
            {'item': 'Turkey and vegetables wrap', 'calories': 320, 'protein': 25, 'carbs': 35, 'fat': 8},
            {'item': 'Zucchini noodles with lean ground turkey', 'calories': 280, 'protein': 28, 'carbs': 15, 'fat': 9}
        ]
        suggestions['dinner'] = [
            {'item': 'Baked cod with broccoli and carrots', 'calories': 280, 'protein': 32, 'carbs': 20, 'fat': 6},
            {'item': 'Grilled turkey breast with cauliflower rice', 'calories': 250, 'protein': 35, 'carbs': 12, 'fat': 5},
            {'item': 'Vegetable stir-fry with tofu', 'calories': 300, 'protein': 20, 'carbs': 30, 'fat': 8}
        ]
        suggestions['snack'] = [
            {'item': 'Apple with almond butter', 'calories': 180, 'protein': 6, 'carbs': 20, 'fat': 8},
            {'item': 'Rice cakes with hummus', 'calories': 150, 'protein': 5, 'carbs': 18, 'fat': 5},
            {'item': 'Plain Greek yogurt with berries', 'calories': 120, 'protein': 12, 'carbs': 15, 'fat': 2}
        ]
    
    else:  # General fitness
        suggestions['breakfast'] = [
            {'item': 'Whole grain toast with avocado and egg', 'calories': 350, 'protein': 15, 'carbs': 35, 'fat': 14},
            {'item': 'Smoothie with banana, oats, and milk', 'calories': 300, 'protein': 12, 'carbs': 50, 'fat': 5},
            {'item': 'Pancakes with fresh fruits', 'calories': 380, 'protein': 10, 'carbs': 60, 'fat': 8}
        ]
        suggestions['lunch'] = [
            {'item': 'Balanced bowl: chicken, rice, and vegetables', 'calories': 500, 'protein': 30, 'carbs': 50, 'fat': 12},
            {'item': 'Sandwich with turkey and vegetables', 'calories': 420, 'protein': 22, 'carbs': 48, 'fat': 12},
            {'item': 'Fish with sweet potato and greens', 'calories': 480, 'protein': 32, 'carbs': 45, 'fat': 13}
        ]
        suggestions['dinner'] = [
            {'item': 'Pasta with lean meat sauce and salad', 'calories': 520, 'protein': 28, 'carbs': 55, 'fat': 14},
            {'item': 'Stir-fried beef with brown rice', 'calories': 550, 'protein': 32, 'carbs': 52, 'fat': 16},
            {'item': 'Grilled chicken with roasted vegetables', 'calories': 480, 'protein': 35, 'carbs': 40, 'fat': 14}
        ]
        suggestions['snack'] = [
            {'item': 'Trail mix and banana', 'calories': 250, 'protein': 8, 'carbs': 35, 'fat': 10},
            {'item': 'String cheese and apple', 'calories': 180, 'protein': 8, 'carbs': 20, 'fat': 8},
            {'item': 'Yogurt with granola', 'calories': 220, 'protein': 10, 'carbs': 32, 'fat': 5}
        ]
    
    return jsonify({
        'success': True,
        'suggestions': suggestions,
        'goal': goal
    })

@app.route('/api/ai-workout-plan')
@login_required
def get_ai_workout_plan():
    """Get AI-powered personalized workout plan based on activity history"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    # Get workout history
    workouts = get_user_workouts(user_id, 30)
    
    # AI Logic: Determine current fitness level and adjust plan
    workout_count = len([w for w in workouts if w['completed']]) if workouts else 0
    avg_duration = sum([w['duration'] for w in workouts if w['completed']]) / max(len([w for w in workouts if w['completed']]), 1) if workouts else 0
    
    plan = recommendation_engine.get_weekly_plan(
        user['age'],
        user['gender'],
        user['height'],
        user['weight'],
        user['fitness_goal'],
        'beginner' if workout_count < 5 else 'intermediate' if workout_count < 15 else 'advanced'
    )
    
    # AI Adjustments based on history
    ai_notes = []
    
    if workout_count == 0:
        ai_notes.append('🎯 Starting your fitness journey? Begin with 3 workouts per week and gradually increase intensity.')
    elif workout_count < 10:
        ai_notes.append('📈 Good start! You\'re building consistency. Try to maintain 4 workouts per week.')
    elif avg_duration < 30:
        ai_notes.append('⏱️ Increase workout duration. Aim for 30-45 minutes per session for better results.')
    else:
        ai_notes.append('🏆 Excellent consistency! You\'re ready for advanced workouts and higher intensity.')
    
    plan['ai_notes'] = ai_notes
    
    return jsonify({
        'success': True,
        'plan': plan,
        'fitness_level': 'beginner' if workout_count < 5 else 'intermediate' if workout_count < 15 else 'advanced',
        'workouts_completed': workout_count
    })

# ===================== ERROR HANDLING =====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'success': False, 'message': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'success': False, 'message': 'Internal server error'}), 500

# ===================== TRANSFORMATION PREDICTION =====================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/transformation')
@login_required
def transformation():
    """Transformation prediction page"""
    return render_template('transformation.html')

@app.route('/chat')
@login_required
def chat():
    """AI chat page"""
    return render_template('chat.html')

@socketio.on('connect')
def handle_connect():
    if 'user_id' in session:
        emit('chat_response', {
            'sender': 'bot',
            'message': 'Hello! I am your AI physique coach. Ask me anything about your fitness, diet, workouts, or transformation goals.'
        })
    else:
        emit('chat_response', {
            'sender': 'bot',
            'message': 'Please login to chat with your AI coach.'
        })

@socketio.on('user_message')
def handle_user_message(data):
    user_id = session.get('user_id')
    message = data.get('message', '').strip()
    if not message:
        emit('chat_response', {'sender': 'bot', 'message': 'Please type a question before sending.'})
        return
    if not user_id:
        emit('chat_response', {'sender': 'bot', 'message': 'Please login to use the chat.'})
        return

    response = chatbot.generate_response(user_id, message)
    emit('chat_response', {'sender': 'bot', 'message': response})

@app.route('/api/predict-transformation', methods=['POST'])
@login_required
def predict_transformation():
    """
    Predict body transformation
    Accepts either photo upload or body dimensions
    """
    user_id = session['user_id']
    
    try:
        # Get user data
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        duration_months = int(request.form.get('duration_months', 3))
        
        # Get current measurements if available
        current_measurements = None
        if request.form.get('chest'):
            current_measurements = {
                'chest': float(request.form.get('chest', 90)),
                'waist': float(request.form.get('waist', 75)),
                'arms': float(request.form.get('arms', 30)),
                'legs': float(request.form.get('legs', 55))
            }
        
        # Predict transformation
        prediction = transformation_engine.predict_transformation(
            user['age'],
            user['gender'],
            user['height'],
            user['weight'],
            user['fitness_goal'],
            duration_months,
            current_measurements
        )
        
        # Handle image generation
        image_data = None
        uploaded_image_base64 = None
        fallback_measurements = {
            'chest': float(request.form.get('chest', 96)),
            'waist': float(request.form.get('waist', 80)),
            'arms': float(request.form.get('arms', 32)),
            'legs': float(request.form.get('legs', 56))
        }

        if request.form.get('chest') or request.form.get('waist') or request.form.get('arms') or request.form.get('legs'):
            current_measurements = {
                'chest': float(request.form.get('chest', fallback_measurements['chest'])),
                'waist': float(request.form.get('waist', fallback_measurements['waist'])),
                'arms': float(request.form.get('arms', fallback_measurements['arms'])),
                'legs': float(request.form.get('legs', fallback_measurements['legs']))
            }
        else:
            current_measurements = fallback_measurements

        if 'photo' in request.files and request.files['photo'].filename != '':
            file = request.files['photo']
            if file and allowed_file(file.filename):
                result = image_processor.process_uploaded_image(file)
                if result['success']:
                    uploaded_image_base64 = result['image_base64']
                    before_image = result['image_base64']
                    after_image = image_processor.generate_transformation_from_photo(
                        result['filepath'], prediction['duration_months'], prediction['after']['weight'], prediction['body_type']
                    )
                    if not after_image:
                        after_image = image_processor.generate_physique_image(
                            prediction['after']['weight'], user['height'], prediction['after'].get('measurements') or current_measurements,
                            user['gender'], phase='after'
                        )
                    image_data = {
                        'before': before_image,
                        'after': after_image
                    }

        if not image_data:
            before_image = image_processor.generate_physique_image(
                user['weight'], user['height'], current_measurements, user['gender'], phase='before'
            )
            after_image = image_processor.generate_physique_image(
                prediction['after']['weight'], user['height'], prediction['after'].get('measurements') or current_measurements,
                user['gender'], phase='after'
            )
            if before_image and after_image:
                image_data = {
                    'before': before_image,
                    'after': after_image
                }
            else:
                sample_image = image_processor.get_sample_image(
                    user['fitness_goal'], prediction['body_type']
                )
                image_data = {
                    'sample': sample_image
                }
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'images': image_data,
            'uploaded_photo': uploaded_image_base64
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

# ===================== VOICE & SPEECH ROUTES =====================

@app.route('/api/voice/quote')
def voice_get_quote():
    """Get a motivational quote with voice synthesis"""
    from voice.speech_output import get_random_quote, speak_random_quote
    
    try:
        quote = get_random_quote()
        # Optionally speak it out (can be async)
        return jsonify({
            'success': True,
            'quote': quote,
            'message': 'Quote retrieved successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/voice/speak', methods=['POST'])
def voice_speak():
    """Speak custom text using text-to-speech"""
    from voice.speech_output import speak_custom
    
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({'success': False, 'message': 'Text is required'}), 400
    
    try:
        speak_custom(text)
        return jsonify({
            'success': True,
            'message': f'Speaking: {text}'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/api/voice/listen')
def voice_listen():
    """Listen to voice input from user"""
    from voice.speech_input import speech_input
    
    try:
        # Listen for speech
        recognized_text = speech_input.listen()
        
        if recognized_text:
            # Process the command
            command = speech_input.process_command(recognized_text)
            return jsonify({
                'success': True,
                'text': recognized_text,
                'command': command
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Could not understand audio'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 400

@app.route('/api/voice/command', methods=['POST'])
def voice_command():
    """Process a voice command"""
    from voice.speech_input import speech_input
    from voice.speech_output import speak_response
    
    data = request.json
    command_text = data.get('text', '')
    
    if not command_text:
        return jsonify({'success': False, 'message': 'Command text is required'}), 400
    
    try:
        # Process the command
        command = speech_input.process_command(command_text)
        
        if command and command['success']:
            intent = command['intent']
            
            # Provide voice response
            if intent in ['dashboard', 'workout', 'diet', 'bmi', 'calories', 'progress', 'weight', 'water', 'quote']:
                speak_response(intent)
            
            return jsonify({
                'success': True,
                'command': command,
                'action': f'Executing command: {intent}'
            })
        else:
            speak_response('error')
            return jsonify({
                'success': False,
                'message': 'Command not recognized'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/voice/settings', methods=['GET', 'POST'])
def voice_settings():
    """Get or update voice settings"""
    from voice.speech_output import speech_output
    
    if request.method == 'POST':
        data = request.json
        
        try:
            if 'rate' in data:
                speech_output.set_rate(int(data['rate']))
            
            if 'volume' in data:
                speech_output.set_volume(float(data['volume']))
            
            if 'voice' in data:
                speech_output.set_voice(int(data['voice']))
            
            return jsonify({
                'success': True,
                'message': 'Voice settings updated successfully'
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400
    
    else:  # GET request
        try:
            settings = {
                'rate': 150,  # Default rate
                'volume': 0.9,  # Default volume
                'voices': ['Male', 'Female']  # Available voices
            }
            return jsonify({
                'success': True,
                'settings': settings
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 400

# ===================== CONTEXT PROCESSORS =====================

@app.context_processor
def inject_user():
    """Inject user data into templates"""
    user_id = session.get('user_id')
    username = session.get('username')
    name = session.get('name')
    return {'user_id': user_id, 'username': username, 'name': name}

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
