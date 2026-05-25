# 🚀 QUICK START GUIDE

## Get Running in 5 Minutes

### Prerequisites
- Python 3.8+ installed
- Basic command line knowledge

---

## Step 1: Setup Environment
```bash
# Navigate to project folder
cd AI-Fitness-Assistant

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
```

## Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 3: Run Application
```bash
python app.py
```

## Step 4: Open Browser
```
http://localhost:5000
```

---

## First Time Setup

### Create Account
1. Click "Register"
2. Fill in details:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `test@123`
   - Age: `25`
   - Height: `180` cm
   - Weight: `75` kg
   - Goal: `Maintenance`

### Explore Features
1. **Dashboard** - View BMI and stats
2. **Workouts** - See personalized workout plan
3. **Diet** - Get customized meal plan
4. **Tracker** - Log your activities
5. **Profile** - Manage your information

---

## Key Features

### 💪 Get Workout Plan
```
1. Click "Workouts"
2. View personalized recommendations
3. Click "Log Today's Workout" to record
```

### 🥗 Get Diet Plan
```
1. Click "Diet Plan"
2. View macronutrients and meals
3. Log food items you consume
```

### 📊 Track Progress
```
1. Click "Tracker"
2. Log weight, workouts, food
3. View daily summary
```

### 📈 Monitor Stats
```
1. Dashboard shows:
   - BMI
   - Weight
   - Calories burned
   - Total workouts
2. Charts show trends
```

---

## Test Data

After registration, create some test data:

### Log a Workout
1. Go to "Tracker"
2. Click "Log Workout"
3. Enter: Running, 30 min, 400 cal
4. Click "Log Workout"

### Log Food
1. Go to "Tracker"
2. Click "Log Food"
3. Enter: Chicken, 200g, 500 cal
4. Click "Log Food"

### Update Weight
1. Go to "Tracker"
2. Enter weight: 73 kg
3. Click "Log Weight"

### View Progress
1. Go to "Dashboard"
2. See updated stats
3. Check charts for trends

---

## Common Commands

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows

# Run app
python app.py

# Deactivate virtual environment
deactivate

# Stop app
Ctrl + C
```

---

## Troubleshooting

### App won't start?
```bash
# Check Python is installed
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Port 5000 in use?
Edit `app.py`, last line:
```python
app.run(debug=True, port=5001)
```

### Microphone issues?
- Check microphone permissions
- Try without voice features first

---

## File Structure
```
AI-Fitness-Assistant/
├── app.py                    ← Run this
├── database.db               ← Auto-created
├── requirements.txt          ← Dependencies
├── models/                   ← Database
├── ai/                       ← AI logic
├── voice/                    ← Voice features
├── charts/                   ← Analytics
├── templates/                ← HTML files
├── static/
│   ├── css/                  ← Styling
│   └── js/                   ← JavaScript
└── README.md                 ← Full documentation
```

---

## Next Steps

1. ✅ Get app running
2. ✅ Create account
3. ✅ Add test data
4. ✅ Explore features
5. ✅ Read README.md
6. ✅ Check FEATURES.md
7. ✅ Customize colors/text
8. ✅ Add your own database entries

---

## Key Endpoints

| Page | URL |
|------|-----|
| Home | http://localhost:5000 |
| Login | http://localhost:5000/login |
| Register | http://localhost:5000/register |
| Dashboard | http://localhost:5000/dashboard |
| Workouts | http://localhost:5000/workout |
| Diet | http://localhost:5000/diet |
| Tracker | http://localhost:5000/tracker |
| Profile | http://localhost:5000/profile |

---

## Tips

1. **Data Entry**: Enter accurate height/weight for better recommendations
2. **Tracking**: Log workouts and food consistently for better analytics
3. **Goals**: Change fitness goal in profile to get new recommendations
4. **Charts**: Refresh dashboard to see updated charts
5. **Voice**: Click and allow microphone permission for voice features

---

## Support

### If stuck:
1. Check INSTALLATION.md for detailed setup
2. Read FEATURES.md for feature details
3. Review README.md for comprehensive guide
4. Check code comments in app.py

---

**Ready to get fit? Let's go! 💪**

```
python app.py → http://localhost:5000 → Start tracking! 🎉
```
