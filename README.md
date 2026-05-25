# AI Fitness Assistant 💪

## Project Overview

**AI Fitness Assistant** is a comprehensive web-based fitness application that provides personalized workout recommendations, diet plans, and progress tracking using artificial intelligence. The system combines voice interaction with a modern web interface to help users achieve their fitness goals.

This project is designed for **B.Tech Computer Science final year submissions** and demonstrates full-stack development, AI/ML concepts, and professional web development practices.

---

## ✨ Features

### 1. **User Authentication & Profile Management**
- Secure user registration and login
- Password hashing using SHA256
- User profile management with fitness goals
- Personal statistics tracking

### 2. **AI-Powered Recommendations**
- **BMI Calculator** - Real-time body mass index calculation
- **Workout Recommendations** - Personalized workout plans based on:
  - Fitness goal (Weight Loss, Muscle Gain, Maintenance)
  - Difficulty level (Beginner, Intermediate, Advanced)
  - Body metrics
- **Diet Recommendations** - Customized meal plans with:
  - Macronutrient calculations
  - Daily calorie requirements
  - Indian diet examples (Paneer, Soya chunks, etc.)
  - Meal options for each meal type

### 3. **Voice Assistant**
- Speech-to-text command recognition
- Text-to-speech responses
- Voice commands for:
  - "Show my dashboard"
  - "Suggest workout"
  - "Track calories"
  - "What is my BMI"
  - "Give diet plan"

### 4. **Progress Tracking**
- Weight tracking with history
- Calorie intake logging
- Workout logging
- Body measurements (chest, waist, arms, legs)
- Daily activity monitoring
- Water intake tracking

### 5. **Analytics & Visualization**
- Weight trend charts (Matplotlib)
- Calorie comparison charts
- Workout type distribution
- Progress statistics
- Monthly summaries

### 6. **Dashboard**
- Real-time BMI display
- Daily calorie summary
- Recent workouts
- Weight progress visualization
- Motivational quotes
- Quick action buttons

### 7. **Database Integration**
- SQLite for data persistence
- Proper relational schema
- User data security
- Historical data tracking

---

## 🛠️ Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 2.3.2** - Web framework
- **SQLite** - Database
- **Werkzeug** - WSGI utilities

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with gradients and animations
- **JavaScript (Vanilla)** - Interactivity
- **Bootstrap 5** - Responsive design

### AI & Voice
- **SpeechRecognition** - Speech-to-text conversion
- **pyttsx3** - Text-to-speech synthesis

### Data Visualization
- **Matplotlib** - Chart generation
- **Chart.js** - Interactive charts

---

## 📁 Project Structure

```
AI-Fitness-Assistant/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── database.db                 # SQLite database (auto-created)
├── README.md                   # This file
│
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   └── script.js          # Frontend JavaScript
│   └── images/                # Image assets
│
├── templates/
│   ├── index.html             # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # Main dashboard
│   ├── workout.html           # Workout recommendations
│   ├── diet.html              # Diet plans
│   ├── tracker.html           # Progress tracking
│   └── profile.html           # User profile
│
├── models/
│   └── database.py            # Database schema and operations
│
├── voice/
│   ├── speech_input.py        # Speech recognition module
│   └── speech_output.py       # Text-to-speech module
│
├── ai/
│   └── recommendation_engine.py # AI logic for recommendations
│
└── charts/
    └── analytics.py           # Analytics and chart generation
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Microphone (for voice features)

### Step 1: Clone/Download Project
```bash
# Navigate to project directory
cd AI-Fitness-Assistant
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Open in Browser
```
Visit: http://localhost:5000
```

---

## 👤 Test Credentials

After running the application, you can register a new account or use test data:

```
Username: testuser
Password: Test@123
```

Or create your own account through the registration page.

---

## 📊 Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email
- `password` - Hashed password
- `name` - Full name
- `age` - Age
- `gender` - Gender (M/F/O)
- `height` - Height in cm
- `weight` - Weight in kg
- `fitness_goal` - Goal type
- `created_at` - Account creation timestamp

### Workouts Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `workout_type` - Type (Cardio/Strength/etc.)
- `name` - Workout name
- `duration` - Duration in minutes
- `calories_burned` - Calories burned
- `date` - Timestamp
- `completed` - Completion status

### Diet Logs Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `meal_type` - Meal type (Breakfast/Lunch/etc.)
- `food_item` - Food name
- `calories` - Calories value
- `protein/carbs/fat` - Macronutrients
- `date` - Timestamp

### Progress Logs Table
- Similar structure for tracking weight, body fat, measurements

---

## 🎯 How to Use

### 1. Registration
1. Click "Register" on login page
2. Fill in all required information
3. Select your fitness goal
4. Click "Create Account"

### 2. Get Personalized Plan
1. Go to Dashboard
2. View your BMI and stats
3. Click "Workouts" for personalized workout plan
4. Click "Diet Plan" for meal recommendations

### 3. Track Progress
1. Go to "Tracker"
2. Log your weight, workouts, and food
3. Use BMI calculator
4. Track water intake

### 4. Monitor Progress
1. Go to Dashboard
2. View weight trend chart
3. Check calorie statistics
4. See recent workouts

### 5. Voice Commands (Optional)
- Click microphone icon
- Speak commands like:
  - "Show my dashboard"
  - "Suggest a workout"
  - "Track calories"

---

## 💡 AI Recommendation Logic

### BMI Calculation
```
BMI = weight (kg) / (height (m))²

Categories:
- Underweight: BMI < 18.5
- Normal: 18.5 ≤ BMI < 25
- Overweight: 25 ≤ BMI < 30
- Obese: BMI ≥ 30
```

### Calorie Requirements (Harris-Benedict Formula)
```
Men: BMR = 88.362 + (13.397 × weight) + (4.799 × height) - (5.677 × age)
Women: BMR = 447.593 + (9.247 × weight) + (3.098 × height) - (4.330 × age)

TDEE = BMR × Activity Factor
Adjusted for goal (deficit for weight loss, surplus for muscle gain)
```

### Macronutrient Distribution
```
Weight Loss: 40% Protein, 35% Carbs, 25% Fat
Muscle Gain: 50% Protein, 35% Carbs, 15% Fat
Maintenance: 35% Protein, 45% Carbs, 20% Fat
```

---

## 📈 Sample Recommendations

### Weight Loss Plan (BMI 27, Intermediate)
- **Daily Calories**: ~1800 kcal (15% deficit)
- **Protein**: 180g | **Carbs**: 157g | **Fat**: 50g
- **Workouts**:
  - Running (45 min, 400 kcal)
  - HIIT Training (30 min, 300 kcal)
  - Cycling (60 min, 450 kcal)
- **Meals**:
  - Grilled chicken with vegetables
  - Lentil dal with roti
  - Greek yogurt
  - Paneer salad

---

## 🔐 Security Features

- Password hashing with SHA256
- Session management
- CSRF protection ready
- Input validation
- SQL injection prevention through parameterized queries
- Secure database operations

---

## 🎨 UI/UX Features

- Modern responsive design
- Gradient buttons and cards
- Mobile-friendly layout
- Dark/light color scheme compatible
- Smooth animations
- Loading states
- Error handling
- Toast notifications

---

## 📱 Responsive Breakpoints

- Desktop: 1200px+
- Tablet: 768px - 1199px
- Mobile: 576px - 767px
- Small Mobile: < 576px

---

## 🚀 Deployment Options

### Local Development
```bash
python app.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn app:app
```

### Cloud Deployment
- Heroku
- AWS
- Google Cloud
- Azure

---

## 🐛 Troubleshooting

### Issue: Module not found
**Solution**: Ensure all requirements are installed
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution**: Change port in app.py
```python
app.run(debug=True, port=5001)
```

### Issue: Microphone not working
**Solution**: 
- Check microphone permissions
- Test with system settings
- Install `pyaudio`: `pip install pyaudio`

### Issue: Database locked
**Solution**: Restart the application

---

## 📚 Learning Outcomes

### Technologies Demonstrated
✅ Full-stack web development
✅ Database design and SQL
✅ REST API development
✅ Frontend JavaScript and AJAX
✅ Voice processing
✅ Data visualization
✅ AI/ML algorithms
✅ Session management
✅ Authentication & security
✅ Responsive web design

### Software Engineering Concepts
✅ MVC architecture
✅ Modular code organization
✅ Error handling
✅ Code documentation
✅ Testing mindset
✅ Performance optimization
✅ Security best practices

---

## 🎓 Presentation Tips for Viva

1. **Project Overview** (2 min)
   - Explain what the project does
   - Real-world use cases
   - Who are the users

2. **Architecture** (3 min)
   - Show folder structure
   - Explain database design
   - Mention technology choices

3. **Demo** (5 min)
   - Registration and login
   - Get recommendations
   - Track workouts and diet
   - Show dashboard and charts

4. **Technical Implementation** (5 min)
   - BMI calculation logic
   - Calorie requirement formula
   - Database queries
   - Voice commands

5. **Challenges & Solutions** (2 min)
   - What was difficult
   - How you solved it
   - Lessons learned

6. **Future Enhancements** (1 min)
   - Mobile app
   - Machine learning
   - Social features
   - API integration

---

## 🔮 Future Enhancements

### Phase 2
- [ ] Mobile app (Flutter/React Native)
- [ ] Advanced ML models
- [ ] Social features (friend tracking)
- [ ] Gym integration
- [ ] Wearable device sync

### Phase 3
- [ ] Video tutorials
- [ ] Nutrition API integration
- [ ] PDF report generation
- [ ] Email notifications
- [ ] Telegram bot integration

### Phase 4
- [ ] AI chatbot (GPT integration)
- [ ] Exercise form detection (Computer Vision)
- [ ] Real-time form correction
- [ ] Multiplayer challenges
- [ ] Leaderboards

---

## 📄 License

This project is open source and available for educational purposes.

---

## 👨‍💻 Author

**Your Name**
- Email: your.email@example.com
- GitHub: @yourprofile
- College: Your College Name
- Roll Number: Your Roll Number

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review code comments
3. Check GitHub issues
4. Contact via email

---

## 🎉 Conclusion

This AI Fitness Assistant demonstrates a complete web application with authentication, AI recommendations, voice interaction, and data visualization. It's suitable for final year project submission and shows proficiency in multiple technologies and software engineering concepts.

**Happy Fitness Journey! 💪**

---

### Quick Links
- 🚀 [Getting Started](#installation--setup)
- 📊 [Features](#features)
- 🛠️ [Tech Stack](#-technology-stack)
- 📖 [How to Use](#-how-to-use)
- 🎓 [Learning Outcomes](#-learning-outcomes)

---

**Last Updated**: May 2024
**Version**: 1.0.0
