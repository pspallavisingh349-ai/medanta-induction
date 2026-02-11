import streamlit as st
import pandas as pd
import sqlite3
import json
import time
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Medanta - Employee Induction Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit defaults
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background: linear-gradient(135deg, #00897b 0%, #00695c 50%, #004d40 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Database setup
DB_PATH = "medanta.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        department TEXT NOT NULL,
        role TEXT NOT NULL,
        employee_id TEXT,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completion_percentage REAL DEFAULT 0
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        options TEXT NOT NULL,
        correct_answer INTEGER NOT NULL,
        category TEXT DEFAULT 'General',
        marks INTEGER DEFAULT 1
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        score INTEGER,
        total_questions INTEGER DEFAULT 0,
        correct_answers INTEGER DEFAULT 0,
        status TEXT DEFAULT 'pending',
        time_taken INTEGER DEFAULT 0,
        completed_at TIMESTAMP,
        answers TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )""")
    
    conn.commit()
    conn.close()

def import_questions_from_csv():
    csv_path = "questions.csv"
    if not os.path.exists(csv_path):
        return False
    
    try:
        df = pd.read_csv(csv_path)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM questions")
        
        for _, row in df.iterrows():
            question = str(row.get('Question', '')).strip()
            if not question or pd.isna(question):
                continue
            
            opt_a = str(row.get('Option A', '')).strip()
            opt_b = str(row.get('Option B', '')).strip()
            opt_c = str(row.get('Option C', '')).strip()
            opt_d = str(row.get('Option D', '')).strip()
            answer = str(row.get('Answer', 'A')).strip().upper()
            
            ans_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            correct_idx = ans_map.get(answer, 0)
            
            options = json.dumps([opt_a, opt_b, opt_c, opt_d])
            topic = str(row.get('Topic', row.get('Category', 'General'))).strip()
            if not topic or topic == 'nan':
                topic = 'General'
            
            c.execute("""
                INSERT INTO questions (question, options, correct_answer, category, marks)
                VALUES (?, ?, ?, ?, ?)
            """, (question, options, correct_idx, topic, 1))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        return False

def add_sample_questions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM questions")
    count = c.fetchone()[0]
    
    if count == 0:
        sample_questions = [
            ("What is Medanta's core value regarding patient care?", 
             json.dumps(["Profit first", "Patient first", "Technology first", "Speed first"]), 
             1, "HR", 1),
            ("What should you do in case of a fire emergency?", 
             json.dumps(["Use elevator", "Run immediately", "Follow evacuation protocol", "Call security only"]), 
             2, "Safety", 1),
            ("Which document is mandatory for all new employees?", 
             json.dumps(["PAN Card", "Aadhar Card", "Both", "None"]), 
             2, "Compliance", 1),
        ]
        c.executemany("""INSERT INTO questions (question, options, correct_answer, category, marks) 
                        VALUES (?, ?, ?, ?, ?)""", sample_questions)
        conn.commit()
    
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize
init_db()

if 'csv_imported' not in st.session_state:
    imported = import_questions_from_csv()
    if not imported:
        add_sample_questions()
    st.session_state.csv_imported = True

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'questions' not in st.session_state:
    st.session_state.questions = []

# ==================== ANIMATED HOME PAGE ====================
def show_home():
    # CSS with animations
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Animated background particles */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
    }
    
    .particle {
        position: absolute;
        width: 10px;
        height: 10px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        animation: float 15s infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
    }
    
    /* Glass card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        padding: 50px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(0,137,123,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* Logo animation */
    .logo-container {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .logo-circle {
        width: 150px;
        height: 150px;
        background: linear-gradient(135deg, #00897b 0%, #00695c 100%);
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 20px 40px rgba(0,137,123,0.4);
        animation: pulse 2s infinite, glow 2s infinite alternate;
        position: relative;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes glow {
        from { box-shadow: 0 20px 40px rgba(0,137,123,0.4); }
        to { box-shadow: 0 20px 60px rgba(0,137,123,0.6), 0 0 30px rgba(0,137,123,0.3); }
    }
    
    .logo-icon {
        font-size: 80px;
        animation: heartbeat 1.5s infinite;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        14% { transform: scale(1.1); }
        28% { transform: scale(1); }
        42% { transform: scale(1.1); }
        70% { transform: scale(1); }
    }
    
    /* Animated text */
    .animated-text {
        text-align: center;
        margin-bottom: 40px;
    }
    
    .namaste {
        font-size: 3em;
        font-weight: 700;
        background: linear-gradient(90deg, #00897b, #00bfa5, #00897b);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s linear infinite;
        margin-bottom: 10px;
    }
    
    @keyframes gradient {
        to { background-position: 200% center; }
    }
    
    .welcome-text {
        font-size: 2em;
        color: #00695c;
        font-weight: 300;
        animation: slideIn 1s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .tagline {
        text-align: center;
        color: #546e7a;
        font-size: 1.2em;
        margin-top: 20px;
        line-height: 1.6;
    }
    
    /* Form styling */
    .form-container {
        margin-top: 40px;
    }
    
    .form-title {
        text-align: center;
        color: #00695c;
        font-size: 1.8em;
        font-weight: 600;
        margin-bottom: 30px;
    }
    
    .input-field {
        margin-bottom: 20px;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 15px !important;
        border: 2px solid #e0f2f1 !important;
        padding: 15px !important;
        font-size: 16px !important;
        transition: all 0.3s !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #00897b !important;
        box-shadow: 0 0 0 3px rgba(0,137,123,0.2) !important;
    }
    
    .submit-btn {
        background: linear-gradient(135deg, #00897b 0%, #00695c 100%) !important;
        color: white !important;
        border: none !important;
        padding: 18px 40px !important;
        border-radius: 50px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        width: 100% !important;
        margin-top: 20px !important;
        box-shadow: 0 10px 30px rgba(0,137,123,0.3) !important;
        transition: all 0.3s !important;
    }
    
    .submit-btn:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(0,137,123,0.4) !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        margin-bottom: 30px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(0,137,123,0.1);
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
        color: #00897b;
        border: 2px solid transparent;
        transition: all 0.3s;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00897b 0%, #00695c 100%) !important;
        color: white !important;
        border-color: #00897b !important;
    }
    
    /* Admin link */
    .admin-link {
        text-align: center;
        margin-top: 30px;
    }
    
    .admin-link a {
        color: #00897b;
        text-decoration: none;
        font-weight: 600;
        padding: 10px 20px;
        border: 2px solid #00897b;
        border-radius: 25px;
        transition: all 0.3s;
    }
    
    .admin-link a:hover {
        background: #00897b;
        color: white;
    }
    
    /* Floating shapes */
    .shape {
        position: absolute;
        opacity: 0.1;
        animation: float-shape 20s infinite;
    }
    
    @keyframes float-shape {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(30px, -30px) rotate(120deg); }
        66% { transform: translate(-20px, 20px) rotate(240deg); }
    }
    </style>
    
    <!-- Floating particles -->
    <div class="particles">
        <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
        <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
        <div class="particle" style="left: 40%; animation-delay: 6s;"></div>
        <div class="particle" style="left: 50%; animation-delay: 8s;"></div>
        <div class="particle" style="left: 60%; animation-delay: 10s;"></div>
        <div class="particle" style="left: 70%; animation-delay: 12s;"></div>
        <div class="particle" style="left: 80%; animation-delay: 14s;"></div>
        <div class="particle" style="left: 90%; animation-delay: 16s;"></div>
    </div>
    
    <div class="main-container">
        <div class="glass-card">
    """, unsafe_allow_html=True)
    
    # Animated logo and text
    st.markdown("""
        <div class="logo-container">
            <div class="logo-circle">
                <span class="logo-icon">🏥</span>
            </div>
        </div>
        
        <div class="animated-text">
            <div class="namaste">Namaste! 🙏</div>
            <div class="welcome-text">Welcome to Medanta</div>
            <div class="tagline">
                Begin your journey with us. Complete your induction to become part 
                of our family dedicated to delivering exceptional healthcare with compassion and excellence.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs for registration/login
    tab1, tab2 = st.tabs(["✨ New Registration", "🔑 Continue Assessment"])
    
    with tab1:
        st.markdown('<div class="form-title">Create Your Account</div>', unsafe_allow_html=True)
        
        with st.form("reg_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name *", placeholder="Enter your full name")
                email = st.text_input("Email Address *", placeholder="your.email@medanta.org")
            with col2:
                department = st.selectbox("Department *", 
                    ["", "Nursing", "Medical", "Administration", "HR", "Finance", "IT", "Operations"])
                role = st.text_input("Designation *", placeholder="e.g., Staff Nurse, Doctor")
            
            employee_id = st.text_input("Employee ID (Optional)", placeholder="If available")
            
            submitted = st.form_submit_button("🚀 Register & Start Assessment")
            
            if submitted:
                if not name or not email or not department or not role:
                    st.error("⚠️ Please fill all required fields")
                else:
                    conn = get_db()
                    c = conn.cursor()
                    c.execute("SELECT id FROM users WHERE email = ?", (email,))
                    if c.fetchone():
                        st.error("📧 Email already registered")
                    else:
                        c.execute("""INSERT INTO users (name, email, department, role, employee_id) 
                                     VALUES (?, ?, ?, ?, ?)""",
                            (name, email, department, role, employee_id or None))
                        user_id = c.lastrowid
                        conn.commit()
                        conn.close()
                        
                        st.session_state.user_id = user_id
                        st.session_state.user_name = name
                        st.session_state.page = 'assessment'
                        st.session_state.questions = []
                        st.session_state.current_question = 0
                        st.session_state.answers = []
                        st.session_state.start_time = time.time()
                        st.rerun()
                    conn.close()
    
    with tab2:
        st.markdown('<div class="form-title">Welcome Back!</div>', unsafe_allow_html=True)
        
        login_email = st.text_input("📧 Email Address", key="login_email", placeholder="Enter registered email")
        
        if st.button("Continue My Assessment", key="login_btn"):
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ?", (login_email,))
            user = c.fetchone()
            
            if user:
                st.session_state.user_id = user['id']
                st.session_state.user_name = user['name']
                c.execute("SELECT * FROM assessments WHERE user_id = ? AND status = 'completed'", (user['id'],))
                completed = c.fetchone()
                conn.close()
                
                if completed:
                    st.session_state.page = 'result'
                else:
                    st.session_state.page = 'assessment'
                    st.session_state.questions = []
                    st.session_state.current_question = 0
                    st.session_state.answers = []
                    st.session_state.start_time = time.time()
                st.rerun()
            else:
                st.error("❌ Email not found")
            conn.close()
        
        st.markdown("<hr style='margin: 30px 0; opacity: 0.3;'>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<p style='text-align: center; color: #78909c;'>Or enter Participant ID</p>", unsafe_allow_html=True)
            login_id = st.text_input("🆔 Participant ID", key="login_id", label_visibility="collapsed")
            
            if st.button("Continue with ID", key="id_btn"):
                if login_id:
                    try:
                        conn = get_db()
                        c = conn.cursor()
                        c.execute("SELECT * FROM users WHERE id = ?", (int(login_id),))
                        user = c.fetchone()
                        conn.close()
                        
                        if user:
                            st.session_state.user_id = user['id']
                            st.session_state.user_name = user['name']
                            st.session_state.page = 'assessment'
                            st.session_state.questions = []
                            st.session_state.current_question = 0
                            st.session_state.answers = []
                            st.session_state.start_time = time.time()
                            st.rerun()
                    except:
                        st.error("Invalid ID")
    
    # Admin link
    st.markdown("""
        <div class="admin-link">
            <a href="?page=admin">🔐 Administrator Portal</a>
        </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== ASSESSMENT PAGE ====================
def show_assessment():
    if not st.session_state.questions:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM questions")
        st.session_state.questions = [dict(row) for row in c.fetchall()]
        conn.close()
    
    questions = st.session_state.questions
    current = st.session_state.current_question
    
    if current >= len(questions):
        submit_assessment()
        return
    
    # Progress header
    progress = (current) / len(questions) * 100
    
    st.markdown(f"""
    <style>
    .assessment-header {{
        background: rgba(255,255,255,0.95);
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}
    .progress-container {{
        background: #e0f2f1;
        height: 12px;
        border-radius: 10px;
        overflow: hidden;
        margin: 15px 0;
    }}
    .progress-bar {{
        height: 100%;
        background: linear-gradient(90deg, #00897b, #00bfa5);
        width: {progress}%;
        transition: width 0.5s;
        border-radius: 10px;
    }}
    .timer-box {{
        background: linear-gradient(135deg, #00897b, #00695c);
        color: white;
        padding: 15px 25px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 10px 30px rgba(0,137,123,0.3);
    }}
    .question-box {{
        background: rgba(255,255,255,0.95);
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        margin-bottom: 30px;
    }}
    .option-btn {{
        background: white;
        border: 3px solid #e0f2f1;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        cursor: pointer;
        transition: all 0.3s;
        text-align: left;
        font-size: 16px;
    }}
    .option-btn:hover {{
        border-color: #00897b;
        background: #e0f2f1;
        transform: translateX(10px);
    }}
    </style>
    
    <div class="assessment-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="color: #00695c; margin: 0;">Question {current + 1} of {len(questions)}</h2>
                <p style="color: #78909c; margin: 5px 0 0 0;">Keep going! You're doing great! 🌟</p>
            </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        elapsed = int(time.time() - st.session_state.start_time)
        mins, secs = divmod(elapsed, 60)
        st.markdown(f'<div class="timer-box">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        </div>
        <div class="progress-container">
            <div class="progress-bar"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Question
    q = questions[current]
    st.markdown(f"""
        <div class="question-box">
            <h3 style="color: #37474f; line-height: 1.6; font-size: 1.4em;">{q['question']}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Options
    options = json.loads(q['options'])
    for i, opt in enumerate(options):
        cols = st.columns([1, 12])
        with cols[0]:
            st.markdown(f"""
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #00897b, #00bfa5); 
                            border-radius: 50%; display: flex; align-items: center; justify-content: center;
                            color: white; font-weight: bold; font-size: 20px; box-shadow: 0 5px 15px rgba(0,137,123,0.3);">
                    {chr(65+i)}
                </div>
            """, unsafe_allow_html=True)
        with cols[1]:
            if st.button(opt, key=f"opt_{i}", use_container_width=True):
                st.session_state.answers.append(i)
                st.session_state.current_question += 1
                st.rerun()
    
    # Navigation
    cols = st.columns([1, 2, 1])
    with cols[0]:
        if current > 0 and st.button("⬅️ Previous", use_container_width=True):
            st.session_state.current_question -= 1
            st.session_state.answers.pop()
            st.rerun()
    with cols[2]:
        if st.button("⏭️ Skip", use_container_width=True):
            st.session_state.answers.append(-1)
            st.session_state.current_question += 1
            st.rerun()

def submit_assessment():
    questions = st.session_state.questions
    answers = st.session_state.answers
    time_taken = int(time.time() - st.session_state.start_time)
    
    correct = sum(1 for i, ans in enumerate(answers) if i < len(questions) and ans == questions[i]['correct_answer'])
    total = len(questions)
    score = (correct / total * 100) if total > 0 else 0
    
    conn = get_db()
    c = conn.cursor()
    c.execute("""INSERT INTO assessments (user_id, title, score, total_questions, correct_answers, status, time_taken, completed_at, answers)
                 VALUES (?, ?, ?, ?, ?, 'completed', ?, datetime('now'), ?)""",
        (st.session_state.user_id, "Induction Assessment", score, total, correct, time_taken, json.dumps(answers)))
    c.execute("UPDATE users SET status = 'completed', completion_percentage = ? WHERE id = ?", (score, st.session_state.user_id))
    conn.commit()
    conn.close()
    
    st.session_state.page = 'result'
    st.rerun()

# ==================== RESULT PAGE ====================
def show_result():
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT * FROM assessments WHERE user_id = ? AND status = 'completed' 
                 ORDER BY completed_at DESC LIMIT 1""", (st.session_state.user_id,))
    result = c.fetchone()
    conn.close()
    
    if not result:
        st.error("No assessment found")
        return
    
    passed = result['score'] >= 70
    
    st.markdown(f"""
    <style>
    .result-container {{
        text-align: center;
        padding: 60px 40px;
        background: rgba(255,255,255,0.95);
        border-radius: 30px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        max-width: 700px;
        margin: 40px auto;
    }}
    .result-icon {{
        font-size: 100px;
        margin-bottom: 20px;
        animation: bounce 1s infinite;
    }}
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-20px); }}
    }}
    .score-circle {{
        width: 200px;
        height: 200px;
        border-radius: 50%;
        background: linear-gradient(135deg, {'#00897b, #00bfa5' if passed else '#ff7043, #f4511e'});
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 30px auto;
        box-shadow: 0 20px 40px rgba({'0,137,123' if passed else '244,81,30'},0.3);
    }}
    .score-text {{
        color: white;
        font-size: 48px;
        font-weight: bold;
    }}
    </style>
    
    <div class="result-container">
        <div class="result-icon">{'🎉' if passed else '👏'}</div>
        <h1 style="color: {'#00897b' if passed else '#ff7043'}; font-size: 2.5em; margin-bottom: 10px;">
            {'Congratulations!' if passed else 'Great Effort!'}
        </h1>
        <p style="color: #78909c; font-size: 1.2em; margin-bottom: 30px;">
            {'You have successfully passed the induction!' if passed else 'Thank you for completing the assessment.'}
        </p>
        
        <div class="score-circle">
            <div class="score-text">{result['score']:.0f}%</div>
        </div>
        
        <p style="color: #546e7a; font-size: 1.3em; margin: 20px 0;">
            {result['correct_answers']} correct out of {result['total_questions']} questions
        </p>
        
        <p style="color: #90a4ae; font-size: 1em;">
            Time taken: {result['time_taken']//60}m {result['time_taken']%60}s
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.page = 'home'
            st.session_state.user_id = None
            st.session_state.user_name = None
            st.rerun()

# ==================== ADMIN PAGE ====================
def show_admin():
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        st.markdown("""
        <style>
        .login-box {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: rgba(255,255,255,0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            text-align: center;
        }
        </style>
        <div class="login-box">
            <h2 style="color: #00897b;">🔐 Admin Login</h2>
        </div>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("Password", type="password", label_visibility="collapsed")
        if st.button("Login", use_container_width=True):
            if pwd == "medanta123":
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Wrong password")
        return
    
    st.sidebar.title("🏥 Medanta Admin")
    page = st.sidebar.radio("Menu", ["📊 Dashboard", "👥 Participants", "📝 Results", "❓ Questions", "📁 Import CSV", "🚪 Logout"])
    
    if page == "🚪 Logout":
        st.session_state.admin_authenticated = False
        st.session_state.page = 'home'
        st.rerun()
    
    elif page == "📊 Dashboard":
        st.title("📊 Dashboard Overview")
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        total = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM assessments WHERE status = 'completed'")
        completed = c.fetchone()[0]
        c.execute("SELECT AVG(score) FROM assessments WHERE status = 'completed'")
        avg_score = c.fetchone()[0] or 0
        c.execute("SELECT COUNT(*) FROM questions")
        total_q = c.fetchone()[0]
        conn.close()
        
        cols = st.columns(4)
        cols[0].metric("👥 Total Participants", total)
        cols[1].metric("✅ Completed", completed)
        cols[2].metric("📊 Average Score", f"{avg_score:.1f}%")
        cols[3].metric("❓ Questions", total_q)
        
        # Chart
        if completed > 0:
            st.bar_chart({"Completed": [completed], "Pending": [total - completed]})
    
    elif page == "👥 Participants":
        st.title("👥 All Participants")
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users ORDER BY created_at DESC")
        users = c.fetchall()
        conn.close()
        
        if users:
            df = pd.DataFrame([dict(row) for row in users])
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇️ Download CSV", df.to_csv(index=False), "participants.csv")
    
    elif page == "📝 Results":
        st.title("📝 Assessment Results")
        conn = get_db()
        c = conn.cursor()
        c.execute("""SELECT a.*, u.name, u.email, u.department 
                     FROM assessments a JOIN users u ON a.user_id = u.id 
                     WHERE a.status = 'completed' ORDER BY a.completed_at DESC""")
        results = c.fetchall()
        conn.close()
        
        if results:
            df = pd.DataFrame([dict(row) for row in results])
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇️ Download CSV", df.to_csv(index=False), "results.csv")
    
    elif page == "❓ Questions":
        st.title("❓ Question Bank")
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM questions")
        questions = c.fetchall()
        conn.close()
        
        st.success(f"Total questions in database: {len(questions)}")
        
        for q in questions:
            with st.expander(f"{q['category']}: {q['question'][:50]}..."):
                opts = json.loads(q['options'])
                for i, opt in enumerate(opts):
                    if i == q['correct_answer']:
                        st.success(f"**{chr(65+i)}. {opt}** ✅")
                    else:
                        st.write(f"{chr(65+i)}. {opt}")
    
    elif page == "📁 Import CSV":
        st.title("📁 Import Questions from CSV")
        uploaded = st.file_uploader("Upload CSV file", type="csv")
        
        if uploaded:
            df = pd.read_csv(uploaded)
            st.write("Preview:", df.head())
            
            if st.button("Import to Database", use_container_width=True):
                df.to_csv("questions.csv", index=False)
                if import_questions_from_csv():
                    st.success("✅ Imported successfully!")
                    st.balloons()
                else:
                    st.error("❌ Import failed")

# ==================== MAIN ====================
def main():
    query = st.query_params
    if query.get("page") == "admin":
        show_admin()
        return
    
    if st.session_state.page == 'home':
        show_home()
    elif st.session_state.page == 'assessment':
        show_assessment()
    elif st.session_state.page == 'result':
        show_result()
    elif st.session_state.page == 'admin':
        show_admin()

if __name__ == "__main__":
    main()
