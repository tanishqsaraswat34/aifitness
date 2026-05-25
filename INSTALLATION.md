# AI Fitness Assistant - Installation Guide

## Complete Setup Instructions

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Storage**: 500MB
- **Microphone**: For voice features (optional)

---

## Step-by-Step Installation

### Step 1: Install Python
1. Download from https://www.python.org/downloads/
2. During installation, **check "Add Python to PATH"**
3. Verify installation:
```bash
python --version
```

### Step 2: Download/Clone Project
- Extract the project folder to your desired location
- Navigate to the project folder in terminal

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: Installation may take 2-5 minutes depending on internet speed.

### Step 5: Initialize Database
The database will be created automatically when you run the app for the first time.

### Step 6: Run the Application
```bash
python app.py
```

You should see:
```
WARNING in app.run_simple
 * Running on http://127.0.0.1:5000
```

### Step 7: Open in Browser
Visit: **http://localhost:5000**

---

## Troubleshooting

### Issue 1: "command not found: python"
**Solution**:
- Install Python from python.org
- Add to PATH during installation
- Use `python3` instead of `python`

### Issue 2: "No module named 'flask'"
**Solution**:
```bash
pip install -r requirements.txt
```

### Issue 3: Port 5000 already in use
**Solution**: Edit app.py, change last line to:
```python
app.run(debug=True, port=5001)
```

### Issue 4: Microphone errors
**Solution**:
```bash
# Windows
pip install pipwin
pipwin install pyaudio

# macOS
brew install portaudio
pip install pyaudio

# Linux
sudo apt-get install python3-pyaudio
```

### Issue 5: Database locked
**Solution**: Delete `database.db` and restart app

---

## Accessing the Application

### Local Access
- **URL**: http://localhost:5000
- **Default Port**: 5000

### Network Access (Optional)
To access from other devices on the network:
1. Find your IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. Use: http://YOUR_IP:5000

---

## First Time Setup

### 1. Create Test Account
1. Click "Register"
2. Fill in details:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `Test@123`
   - Age: `25`
   - Gender: `Male`
   - Height: `180` cm
   - Weight: `75` kg
   - Goal: `Maintenance`
3. Click "Create Account"

### 2. Login
1. Use credentials from step 1
2. You'll see the dashboard

### 3. Explore Features
- Go to "Workouts" for recommendations
- Go to "Diet" for meal plans
- Go to "Tracker" to log activities
- View progress on Dashboard

---

## Deactivating Virtual Environment

When done working on the project:

**Windows:**
```bash
venv\Scripts\deactivate
```

**macOS/Linux:**
```bash
deactivate
```

---

## Common Commands

```bash
# Activate virtual environment
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate

# Install all requirements
pip install -r requirements.txt

# Run the app
python app.py

# Deactivate virtual environment
deactivate

# Reinstall all packages
pip install -r requirements.txt --upgrade
```

---

## File Locations

After running the app, you'll see:
- `database.db` - SQLite database (auto-created)
- `*.log` - Log files (if enabled)
- `static/` - CSS, JS, images

---

## Testing the Application

### Manual Testing Checklist
- [ ] Registration works
- [ ] Login works
- [ ] Dashboard loads
- [ ] Recommendations work
- [ ] Tracking features work
- [ ] Charts display correctly
- [ ] Logout works

### Test Scenarios
1. **Registration**: Create account with valid data
2. **Login**: Login with correct credentials
3. **Workout**: Get workout recommendation
4. **Diet**: View diet plan
5. **Tracker**: Log workout and food
6. **Profile**: Update profile information

---

## Performance Tips

1. **Clear cache** if app seems slow:
   - Delete `*.pyc` files
   - Clear browser cache

2. **Database optimization**:
   - Periodically backup `database.db`
   - Clear old logs if space is limited

3. **Memory usage**:
   - App uses ~200MB RAM
   - Ensure minimum 2GB available

---

## Security Notes

1. Change default secret key in production:
   ```python
   app.secret_key = 'your-unique-secret-key'
   ```

2. Update password hashing if needed

3. Enable HTTPS for public deployment

---

## Support Resources

- **Python Docs**: https://docs.python.org/3/
- **Flask Docs**: https://flask.palletsprojects.com/
- **Bootstrap Docs**: https://getbootstrap.com/docs/
- **SQLite Docs**: https://www.sqlite.org/docs.html

---

## Next Steps

1. ✅ Install and run the app
2. ✅ Create test account
3. ✅ Explore features
4. ✅ Read the README.md
5. ✅ Review the code
6. ✅ Customize as needed

---

**Installation completed! Enjoy your AI Fitness Assistant!** 💪
