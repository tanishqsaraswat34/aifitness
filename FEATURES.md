# AI Fitness Assistant - Features Documentation

## Complete Feature List & Technical Details

---

## 1. USER AUTHENTICATION SYSTEM

### Registration Page
**Location**: `/register`
**File**: `templates/register.html`

**Features**:
- User input validation (client-side)
- Password strength indicators (can be added)
- Email verification (can be added)
- Unique username and email checking

**Form Fields**:
- Username (required, unique)
- Email (required, unique)
- Password (required, min 6 chars recommended)
- Full Name
- Age (13+)
- Gender (M/F/Other)
- Height (cm)
- Weight (kg)
- Fitness Goal

**Backend Route**: `/register` (POST)

---

### Login Page
**Location**: `/login`
**File**: `templates/login.html`

**Features**:
- Secure password verification
- Session management
- Remember session until logout

**Backend Route**: `/login` (GET/POST)

**Session Data Stored**:
- user_id
- username
- name

---

### Logout
**Route**: `/logout`
- Clears all session data
- Redirects to login

---

## 2. DASHBOARD

**Location**: `/dashboard`
**File**: `templates/dashboard.html`

### Components

#### BMI Card
```
Displays: BMI Value, Category (Underweight/Normal/Overweight/Obese)
Updates: Real-time from profile data
Formula: Weight(kg) / (Height(m))²
```

#### Weight Card
```
Shows: Current weight from latest progress log
Updates: When weight is tracked
```

#### Calorie Card
```
Shows: Total calories burned this month
Calculation: Sum of all workouts' calories_burned in current month
```

#### Workout Card
```
Shows: Total workouts completed this month
Calculation: Count of completed workouts in current month
```

#### Weight Progress Chart
```
Type: Line chart (Matplotlib)
X-axis: Dates (last 30 days)
Y-axis: Weight (kg)
Data: From progress_logs table
```

#### Calorie Comparison Chart
```
Type: Bar chart (Matplotlib)
Shows: Consumed vs Burned calories
Comparison: Daily breakdown
```

#### Recent Workouts Table
```
Columns: Date, Workout, Duration, Calories
Rows: Last 5 workouts
Sorting: By date (newest first)
```

---

## 3. WORKOUT RECOMMENDATIONS

**Location**: `/workout`
**File**: `templates/workout.html`

### Features

#### Personalization Logic
```python
1. Get user profile (age, gender, height, weight)
2. Calculate BMI
3. Determine difficulty:
   - Underweight/Normal → Beginner
   - Overweight → Intermediate
   - Obese → Beginner
4. Match goal with workouts
5. Generate weekly plan
```

#### Workout Categories

**Beginner** (5 workouts):
- Brisk Walking (30 min, 150 kcal)
- Bodyweight Basics (20 min, 100 kcal)
- Yoga (30 min, 120 kcal)
- Swimming (30 min, 200 kcal)
- Home Workout (25 min, 120 kcal)

**Intermediate** (5 workouts):
- Running (45 min, 400 kcal)
- Weight Training (60 min, 300 kcal)
- HIIT (30 min, 300 kcal)
- Cycling (60 min, 450 kcal)
- Circuit Training (45 min, 250 kcal)

**Advanced** (5 workouts):
- Intense HIIT (45 min, 500 kcal)
- Powerlifting (90 min, 400 kcal)
- Marathon Training (120 min, 1200 kcal)
- Crossfit (60 min, 400 kcal)
- Advanced Yoga (60 min, 250 kcal)

#### Goal-Based Filtering
```
Weight Loss: Prioritize Cardio workouts
Muscle Gain: Prioritize Strength workouts
Maintenance: Mix of both
```

#### Fitness Tips
- 5 customized tips based on goal
- Include recommendations for:
  - Calorie deficits/surplus
  - Frequency
  - Hydration
  - Recovery
  - Sleep

---

## 4. DIET RECOMMENDATIONS

**Location**: `/diet`
**File**: `templates/diet.html`

### Features

#### Macronutrient Calculation
```
Daily Calories = Calculated from Harris-Benedict formula

Weight Loss (40% Protein, 35% Carbs, 25% Fat):
- 15% calorie deficit
- Example: 1800 kcal → Protein 180g, Carbs 157g, Fat 50g

Muscle Gain (50% Protein, 35% Carbs, 15% Fat):
- 10% calorie surplus
- Example: 2400 kcal → Protein 300g, Carbs 210g, Fat 40g

Maintenance (35% Protein, 45% Carbs, 20% Fat):
- No deficit/surplus
- Example: 2000 kcal → Protein 175g, Carbs 225g, Fat 44g
```

#### Meal Plan Structure

**4 Meals Per Day**:

1. **Breakfast** - 350-550 kcal
   - Options for each goal
   - Indian options: Oats, Eggs, Paneer

2. **Lunch** - 500-700 kcal
   - Main meal
   - Indian options: Dal, Paneer, Chicken

3. **Snack** - 150-400 kcal
   - Quick options
   - Protein-rich suggestions

4. **Dinner** - 350-700 kcal
   - Light to moderate
   - Indian options: Soya chunks, Fish, Paneer

#### Indian Diet Examples
- Paneer (cottage cheese)
- Soya chunks
- Dal (lentils)
- Rice
- Roti (bread)
- Milk
- Peanut butter
- Fruits (Apple, Banana)
- Vegetables

---

## 5. PROGRESS TRACKING

**Location**: `/tracker`
**File**: `templates/tracker.html`

### Weight Tracking
```
Input: Current weight, Body Fat %, Chest, Waist, Arms, Legs
Storage: progress_logs table
History: All measurements stored with dates
Comparison: Can compare month-over-month
```

### Workout Logging
```
Input: Workout Name, Type, Duration, Calories
Types: Cardio, Strength, Flexibility, Sports
Storage: workouts table
Notes: Duration in minutes, calories_burned as integer
```

### Diet Logging
```
Input: Meal Type, Food Item, Quantity, Calories, Macros
Meal Types: Breakfast, Lunch, Snack, Dinner
Macros Tracked: Protein, Carbs, Fat
Storage: diet_logs table
```

### Water Intake
```
Input: Amount in liters
Tracking: Daily summary
Optional: Can be extended for more detailed tracking
```

### Daily Summary
```
Displays:
- Total Calories Consumed (from diet_logs)
- Total Calories Burned (from workouts, completed=1)
- Net Calories (Consumed - Burned)
- Updates: Real-time as data is logged
```

---

## 6. BMI CALCULATOR

**Location**: `/api/calculate-bmi` (POST)

```python
Inputs: Height (cm), Weight (kg)
Formula: BMI = weight / (height_in_meters)²

Output:
{
    "bmi": 24.5,
    "category": "Normal",
    "message": "You are in a healthy weight range..."
}

Categories:
- Underweight: < 18.5
- Normal: 18.5-24.9
- Overweight: 25-29.9
- Obese: ≥ 30
```

---

## 7. ANALYTICS & CHARTS

**Location**: `/charts/analytics.py`

### Chart Types

#### Weight Trend Chart
```
Type: Line Chart (Matplotlib)
Data: Last 30 days weight data
Visual: Blue line with circular markers
X-axis: Dates
Y-axis: Weight in kg
Format: PNG image (base64 encoded)
Display: In dashboard
```

#### Calorie Comparison Chart
```
Type: Bar Chart (Matplotlib)
Bars: Consumed (Red) vs Burned (Green)
X-axis: Dates
Y-axis: Calories
Legend: Shows which bar is which
```

#### Workout Distribution Chart
```
Type: Pie Chart (Matplotlib)
Shows: Percentage of each workout type
Colors: Multiple colors for distinction
Display: In dashboard
```

### Analytics Functions
```python
get_weight_trend(user_id, days=30)
- Returns list of dates and weights

get_calorie_trend(user_id, days=30)
- Returns consumed and burned calories

get_workout_stats(user_id, days=30)
- Total workouts, total calories, by type

get_summary_stats(user_id, days=30)
- Current weight, total workouts, calories burned, avg daily
```

---

## 8. PROFILE MANAGEMENT

**Location**: `/profile`
**File**: `templates/profile.html`

### Profile Information
```
View Only:
- Username
- Email
- Gender
- Date Created

Editable:
- Age
- Height
- Weight
- Fitness Goal
```

### Quick Stats
```
Display:
- Age
- Height
- Current Weight
- Fitness Goal
```

### Account Settings
- Change Password (coming soon)
- Delete Account (coming soon)

---

## 9. VOICE FEATURES

**Location**: `/voice/`

### Speech Input (`speech_input.py`)
```python
Features:
- Microphone listening
- Audio to text conversion (Google API)
- Command recognition
- Error handling

Commands Recognized:
- "dashboard" → Redirect to dashboard
- "workout" → Get workout recommendation
- "diet" → Get diet plan
- "bmi" → Calculate BMI
- "calories" → Track calories
- "progress" → Show progress
- "weight" → Log weight
- "water" → Log water intake
- "quote" → Get motivational quote
- "logout" → Logout
```

### Speech Output (`speech_output.py`)
```python
Features:
- Text to speech conversion (pyttsx3)
- Multiple voice options
- Adjustable speech rate
- Volume control

Pre-defined Responses:
- Greetings
- Feature confirmations
- Motivational quotes (15 different quotes)
- BMI results
- Calorie summaries
```

---

## 10. RECOMMENDATION ENGINE

**Location**: `/ai/recommendation_engine.py`

### Core Algorithm

```
1. Input: User profile (age, gender, height, weight, goal, difficulty)

2. Calculate BMI
   - Category determination
   - Health message

3. Calculate Daily Calorie Requirement
   - Harris-Benedict formula
   - Activity factor (1.55)
   - Goal adjustment (±10-15%)

4. Calculate Macronutrients
   - Based on goal
   - Protein/Carbs/Fat distribution

5. Select Workouts
   - Filter by goal
   - Filter by difficulty
   - Return 5 workouts

6. Select Diet Plan
   - Match to goal
   - Include meal options
   - Include macronutrients

7. Generate Tips
   - 5 specific tips for goal and difficulty
```

---

## 11. DATABASE OPERATIONS

**Location**: `/models/database.py`

### Tables

#### Users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT UNIQUE,
    password TEXT (SHA256 hashed),
    name TEXT,
    age INTEGER,
    gender TEXT,
    height REAL,
    weight REAL,
    fitness_goal TEXT,
    created_at TIMESTAMP,
    last_login TIMESTAMP
)
```

#### Workouts
```sql
CREATE TABLE workouts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER (FK),
    workout_type TEXT,
    name TEXT,
    duration INTEGER,
    difficulty TEXT,
    calories_burned INTEGER,
    date TIMESTAMP,
    completed INTEGER (0/1)
)
```

#### Diet Logs
```sql
CREATE TABLE diet_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER (FK),
    meal_type TEXT,
    food_item TEXT,
    quantity REAL,
    calories INTEGER,
    protein REAL,
    carbs REAL,
    fat REAL,
    date TIMESTAMP
)
```

#### Calorie Logs
```sql
CREATE TABLE calorie_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER (FK),
    calories_consumed INTEGER,
    calories_burned INTEGER,
    water_intake REAL,
    date TIMESTAMP
)
```

#### Progress Logs
```sql
CREATE TABLE progress_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER (FK),
    weight REAL,
    body_fat REAL,
    chest REAL,
    waist REAL,
    arms REAL,
    legs REAL,
    date TIMESTAMP
)
```

---

## 12. API ENDPOINTS

### Authentication
```
POST   /register      - Register new user
POST   /login         - User login
GET    /logout        - User logout
```

### Dashboard
```
GET    /dashboard     - Dashboard page
GET    /api/dashboard-data - Get dashboard statistics
```

### Recommendations
```
GET    /api/recommendations - Get personalized plan
GET    /workout        - Workout page
GET    /diet           - Diet page
GET    /api/diet-plan  - Get diet plan
```

### Tracking
```
POST   /api/track-workout - Log workout
POST   /api/track-diet    - Log food
POST   /api/track-weight  - Log weight
GET    /api/daily-summary - Get daily summary
```

### Profile
```
GET    /profile              - Profile page
GET    /api/profile          - Get profile data
POST   /api/update-profile   - Update profile
```

### Utilities
```
GET    /api/quote            - Get random quote
POST   /api/calculate-bmi    - Calculate BMI
```

---

## 13. ERROR HANDLING

### Validation
- Required field checking
- Data type validation
- Range validation (age, height, weight)
- Email format validation

### Error Messages
- User-friendly error messages
- Field-specific errors
- Database errors
- Network errors

### HTTP Status Codes
- 200 OK
- 400 Bad Request
- 404 Not Found
- 500 Internal Server Error

---

## 14. SECURITY FEATURES

### Password Security
- SHA256 hashing
- No plain text storage
- Verification on login

### Session Management
- Unique session IDs
- Timeout handling
- Secure cookies

### Input Validation
- SQL injection prevention
- XSS prevention
- CSRF tokens (can be added)

### Database Security
- Parameterized queries
- Foreign key constraints
- Data type validation

---

## 15. USER EXPERIENCE

### Loading States
- Spinner during data fetch
- Visual feedback on interactions
- Success/error messages

### Responsive Design
- Mobile-friendly
- Tablet optimized
- Desktop optimized
- Touch-friendly buttons

### Navigation
- Consistent sidebar
- Breadcrumb navigation (can be added)
- Active page highlighting
- Quick action buttons

---

## 16. PERFORMANCE FEATURES

### Caching
- Static file caching
- Database query optimization
- Chart generation (one-time)

### Optimization
- Lazy loading charts
- Database indexing
- Efficient queries

---

## 17. DATA FLOW

### Registration Flow
```
User Input → Validation → Hash Password → 
Check Uniqueness → Store in DB → Success Message
```

### Login Flow
```
Username/Password → Get User → Hash Input Password →
Compare → Create Session → Redirect to Dashboard
```

### Recommendation Flow
```
User Data → Get from DB → Run AI Algorithm →
Calculate BMI/Calories/Macros → Generate Recommendations →
Display to User
```

### Tracking Flow
```
User Input → Validation → Store in DB →
Update Dashboard → Show in Charts → Success Message
```

---

**Feature Documentation Complete!**

For implementation details, refer to the source code in respective files.
