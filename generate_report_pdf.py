"""
Generate Project Report as PDF
"""

from fpdf import FPDF
from datetime import datetime

class ProjectReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_font("Arial", size=11)

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_title(self, title):
        self.set_font("Arial", "B", 16)
        self.set_text_color(25, 118, 210)
        self.ln(5)
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def add_section(self, section_title):
        self.set_font("Arial", "B", 13)
        self.set_text_color(25, 118, 210)
        self.ln(8)
        self.cell(0, 10, section_title, ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", size=11)
        self.ln(2)

    def add_text(self, text):
        self.set_font("Arial", size=11)
        self.multi_cell(0, 5, text)

    def add_bullet_points(self, points):
        self.set_font("Arial", size=10)
        for point in points:
            self.ln(1)
            self.cell(5, 5, "•", ln=False)
            self.multi_cell(0, 5, point, 10)

pdf = ProjectReportPDF()
pdf.add_page()

# Title
pdf.set_font("Arial", "B", 20)
pdf.set_text_color(25, 118, 210)
pdf.cell(0, 15, "AI FITNESS ASSISTANT", ln=True, align="C")
pdf.set_font("Arial", "B", 12)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, "Complete Project Report", ln=True, align="C")
pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%B %d, %Y')}", ln=True, align="C")
pdf.set_text_color(0, 0, 0)
pdf.ln(5)

# 1. PROJECT OVERVIEW
pdf.add_section("1. PROJECT OVERVIEW")
pdf.add_text(
    "Title: AI Fitness Assistant\n"
    "Type: Full-Stack Web Application\n"
    "Purpose: A comprehensive fitness platform providing personalized workout recommendations, "
    "diet plans, voice interaction, and progress tracking using artificial intelligence.\n"
)

pdf.add_text("\nKey Statistics:")
pdf.add_bullet_points([
    "Backend: 600+ lines (Flask, Python)",
    "Database Layer: 400+ lines",
    "AI Engine: 600+ lines (recommendation & analytics)",
    "Frontend: 1000+ lines (HTML/CSS/JavaScript)",
    "Voice Module: 350+ lines"
])

# 2. TECHNOLOGY STACK
pdf.add_section("2. TECHNOLOGY STACK")
pdf.add_text("Backend:")
pdf.add_bullet_points(["Python 3.8+", "Flask 2.3.2 (Web Framework)", "SQLite (Database)"])

pdf.add_text("\nFrontend:")
pdf.add_bullet_points(["HTML5, CSS3, Bootstrap 5", "JavaScript (Vanilla)", "Chart.js & Matplotlib (Visualization)"])

pdf.add_text("\nAI & Voice:")
pdf.add_bullet_points(["SpeechRecognition (Speech-to-text)", "pyttsx3 (Text-to-speech)"])

pdf.add_text("\nKey Libraries: Werkzeug, Jinja2, Pillow, python-dotenv")

# 3. CORE FEATURES
pdf.add_section("3. CORE FEATURES IMPLEMENTED")
pdf.add_bullet_points([
    "User Authentication: Secure login/registration, password hashing",
    "BMI Calculator: Real-time calculation with health categories",
    "Workout Recommendations: 15+ personalized workouts across 3 difficulty levels",
    "Diet Plans: Indian food options, macronutrient calculations",
    "Voice Assistant: Speech commands for dashboard, workouts, BMI, diet plans",
    "Progress Tracking: Weight history, calorie logging, workout logging",
    "Analytics & Charts: Weight trends, calorie comparisons, workout statistics",
    "Dashboard: Real-time stats, visualizations, recent workouts",
    "Data Persistence: SQLite database with 6 optimized tables"
])

# 4. PROJECT STRUCTURE
pdf.add_section("4. PROJECT STRUCTURE")
pdf.add_text(
    "AI-Fitness-Assistant/\n"
    "├── app.py (Main Flask application - 600+ lines)\n"
    "├── requirements.txt (13 dependencies)\n"
    "├── models/database.py (Database operations - 400+ lines)\n"
    "├── ai/ (recommendation_engine, image_processor, chatbot)\n"
    "├── voice/ (speech_input, speech_output)\n"
    "├── charts/analytics.py (Chart generation - 400+ lines)\n"
    "└── templates/ (8 HTML files: login, register, dashboard, etc.)"
)

pdf.add_page()

# 5. KEY MODULES
pdf.add_section("5. KEY MODULES & FUNCTIONALITY")

pdf.add_text("A. Database Layer (models/database.py):")
pdf.add_bullet_points([
    "6 optimized database tables",
    "CRUD operations",
    "Password hashing",
    "Data retrieval functions"
])

pdf.add_text("\nB. AI Recommendation Engine (ai/recommendation_engine.py):")
pdf.add_bullet_points([
    "BMI calculation",
    "Calorie requirements using Harris-Benedict formula",
    "Macronutrient distribution",
    "15 different workouts (3 difficulty levels each)",
    "3 complete diet plans with Indian food options",
    "Fitness tips generation"
])

pdf.add_text("\nC. Voice Module (voice/):")
pdf.add_bullet_points([
    "10+ command types recognized",
    "Microphone input handling",
    "Text-to-speech with rate/volume control",
    "15 motivational quotes database",
    "Error handling"
])

pdf.add_text("\nD. Analytics Module (charts/analytics.py):")
pdf.add_bullet_points([
    "Weight trend analysis",
    "Calorie comparison",
    "Workout statistics",
    "Base64 image encoding for web display"
])

# 6. DATABASE SCHEMA
pdf.add_section("6. DATABASE SCHEMA")
pdf.add_text("The project uses 6 interconnected SQLite tables:")
pdf.add_bullet_points([
    "users: User profiles and authentication",
    "workouts: Workout history and details",
    "diet_logs: Food intake records",
    "calorie_logs: Calorie tracking",
    "progress_logs: Weight and body measurements",
    "recommendations: AI-generated plans"
])

# 7. INSTALLATION
pdf.add_section("7. INSTALLATION & DEPLOYMENT")
pdf.add_text("System Requirements:")
pdf.add_bullet_points([
    "OS: Windows 10+, macOS 10.14+, Ubuntu 18.04+",
    "Python: 3.8 or higher",
    "RAM: 2GB minimum",
    "Storage: 500MB",
    "Microphone: For voice features (optional)"
])

pdf.add_text("\nInstallation Steps:")
pdf.add_bullet_points([
    "Create virtual environment: python -m venv venv",
    "Activate: venv\\Scripts\\activate (Windows)",
    "Install dependencies: pip install -r requirements.txt",
    "Run application: python app.py",
    "Access: http://localhost:5000"
])

pdf.add_page()

# 8. USER WORKFLOWS
pdf.add_section("8. USER WORKFLOWS")

pdf.add_text("Workflow 1: New User Registration")
pdf.add_bullet_points([
    "User registers with fitness profile",
    "Provides height, weight, fitness goal",
    "Receives personalized recommendations"
])

pdf.add_text("\nWorkflow 2: Existing User")
pdf.add_bullet_points([
    "Login to dashboard",
    "View BMI, calories, recent workouts",
    "Track progress with analytics",
    "View weight trends and statistics"
])

pdf.add_text("\nWorkflow 3: Voice Interaction")
pdf.add_bullet_points([
    "Use voice commands (e.g., 'Show dashboard')",
    "Receive AI recommendations",
    "Get motivational feedback",
    "Track workouts via voice"
])

# 9. API ENDPOINTS
pdf.add_section("9. KEY API ENDPOINTS")
pdf.add_text(
    "/login (POST): User authentication\n"
    "/register (POST): User registration\n"
    "/dashboard (GET): Main dashboard display\n"
    "/workout (GET): Personalized workouts\n"
    "/diet (GET): Diet recommendations\n"
    "/tracker (GET): Progress tracking\n"
    "/api/add-workout (POST): Log workout\n"
    "/api/add-diet (POST): Log food\n"
    "/api/analytics (GET): Generate charts"
)

# 10. LEARNING OUTCOMES
pdf.add_section("10. LEARNING OUTCOMES & SKILLS DEMONSTRATED")
pdf.add_bullet_points([
    "Full-stack web development (Frontend + Backend)",
    "Database design and management (SQLite)",
    "RESTful API design",
    "AI/ML concepts (Recommendation engine, calorie calculations)",
    "Voice processing (Speech recognition & synthesis)",
    "Data visualization (Matplotlib, Chart.js)",
    "Authentication & security (Password hashing, sessions)",
    "Responsive UI design (Bootstrap, CSS)",
    "JavaScript async operations",
    "Software engineering best practices"
])

# 11. CHALLENGES & SOLUTIONS
pdf.add_section("11. CHALLENGES & SOLUTIONS")
pdf.add_text("Cross-browser voice compatibility:")
pdf.add_bullet_points(["Used SpeechRecognition API with fallbacks"])

pdf.add_text("Real-time chart updates:")
pdf.add_bullet_points(["Implemented AJAX for dynamic refreshing"])

pdf.add_text("Large file uploads:")
pdf.add_bullet_points(["Set MAX_CONTENT_LENGTH limit"])

pdf.add_text("Database optimization:")
pdf.add_bullet_points(["Indexed user_id and created_at fields"])

pdf.add_text("Security:")
pdf.add_bullet_points(["SHA256 password hashing, session management"])

# 12. FUTURE ENHANCEMENTS
pdf.add_section("12. FUTURE ENHANCEMENTS")
pdf.add_bullet_points([
    "Machine learning for better recommendations",
    "Mobile app (React Native/Flutter)",
    "Social features (friend groups, challenges)",
    "Wearable device integration",
    "Advanced nutrition analysis",
    "Video tutorials for workouts",
    "Payment integration for premium features"
])

# Save PDF
pdf_path = "AI_Fitness_Assistant_Project_Report.pdf"
pdf.output(pdf_path)
print(f"✅ PDF Report generated successfully: {pdf_path}")
