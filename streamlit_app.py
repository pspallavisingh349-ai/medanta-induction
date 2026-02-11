import streamlit as st
import pandas as pd
import sqlite3
import json
import time
import os
import base64
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO

# Page config
st.set_page_config(
    page_title="Medanta - Employee Induction Portal",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS with powder blue background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
        -webkit-tap-highlight-color: transparent;
    }
    
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
        max-width: 100% !important;
    }
    
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    
    /* POWDER BLUE BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
        margin-top: 0 !important;
        min-height: 100vh;
    }
    
    /* Floating particles */
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
        background: rgba(255,255,255,0.4);
        border-radius: 50%;
        animation: float-particle 15s infinite;
    }
    
    @keyframes float-particle {
        0%, 100% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
    }
    
    /* Login Container */
    .login-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 20px;
        position: relative;
        z-index: 1;
    }
    
    .login-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 40px 30px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.5);
        text-align: center;
    }
    
    /* Logo styling */
    .logo-circle {
        width: 120px;
        height: 120px;
        margin: 0 auto 30px;
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 20px 40px rgba(25,118,210,0.3);
        animation: pulse-blue 2s infinite;
    }
    
    @keyframes pulse-blue {
        0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(25,118,210,0.4); }
        50% { transform: scale(1.05); box-shadow: 0 0 0 20px rgba(25,118,210,0); }
    }
    
    .logo-icon {
        font-size: 60px;
    }
    
    /* Animated title - BLUE theme */
    .animated-title {
        font-size: 2.8em;
        font-weight: 800;
        background: linear-gradient(90deg, #1565c0, #42a5f5, #1565c0, #42a5f5);
        background-size: 300% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-flow 3s ease infinite;
        margin-bottom: 10px;
    }
    
    @keyframes gradient-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .login-subtitle {
        color: #546e7a;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    
    /* Form styling */
    .form-label {
        color: #37474f;
        font-weight: 600;
        font-size: 0.9em;
        margin-bottom: 8px;
        display: block;
        text-align: left;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 12px !important;
        border: 2px solid #e3f2fd !important;
        padding: 14px !important;
        font-size: 16px !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #1976d2 !important;
        box-shadow: 0 0 0 4px rgba(25,118,210,0.1) !important;
    }
    
    /* Buttons - BLUE theme */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-weight: 600 !important;
        width: 100% !important;
        box-shadow: 0 10px 30px rgba(25,118,210,0.3) !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: white !important;
        color: #1976d2 !important;
        border: 2px solid #1976d2 !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-weight: 600 !important;
    }
    
    /* Dashboard Container */
    .dashboard-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        position: relative;
        z-index: 1;
    }
    
    /* Top Navigation - WHITE */
    .top-nav {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 20px 25px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .nav-logo {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .nav-logo-text {
        color: #1565c0;
        font-size: 1.5em;
        font-weight: 700;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 40px 20px;
        margin-bottom: 40px;
    }
    
    .hero-title {
        color: #1565c0;
        font-size: 2.5em;
        font-weight: 800;
        margin-bottom: 15px;
    }
    
    .hero-subtitle {
        color: #546e7a;
        font-size: 1.2em;
        margin-bottom: 10px;
    }
    
    .hero-tagline {
        color: #78909c;
        font-size: 1em;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Stats Bar - WHITE */
    .stats-bar {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 2.5em;
        font-weight: 800;
        color: #1565c0;
        display: block;
    }
    
    .stat-label {
        color: #78909c;
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Feature Cards */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 25px;
        margin-bottom: 40px;
    }
    
    .feature-card {
        background: white;
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        border-color: #1976d2;
    }
    
    .feature-icon {
        width: 80px;
        height: 80px;
        margin: 0 auto 20px;
        background: linear-gradient(135deg, #1976d2, #42a5f5);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        box-shadow: 0 10px 30px rgba(25,118,210,0.3);
    }
    
    .feature-title {
        font-size: 1.4em;
        font-weight: 700;
        color: #263238;
        margin-bottom: 10px;
    }
    
    .feature-desc {
        color: #78909c;
        font-size: 0.95em;
        line-height: 1.5;
        margin-bottom: 20px;
    }
    
    /* Topic Cards for Assessment */
    .topic-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-bottom: 40px;
    }
    
    .topic-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border-left: 5px solid #1976d2;
        transition: all 0.3s;
    }
    
    .topic-card:hover {
        transform: translateX(10px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.12);
    }
    
    .topic-name {
        font-size: 1.2em;
        font-weight: 700;
        color: #263238;
        margin-bottom: 10px;
    }
    
    .topic-count {
        color: #78909c;
        font-size: 0.9em;
        margin-bottom: 15px;
    }
    
    .topic-status {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
    }
    
    .status-pending {
        background: #fff3e0;
        color: #ef6c00;
    }
    
    .status-passed {
        background: #e8f5e9;
        color: #2e7d32;
    }
    
    .status-failed {
        background: #ffebee;
        color: #c62828;
    }
    
    /* Report Card */
    .report-card {
        background: white;
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.08);
    }
    
    .report-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
        padding-bottom: 20px;
        border-bottom: 2px solid #e3f2fd;
    }
    
    .report-title {
        font-size: 1.5em;
        font-weight: 700;
        color: #1565c0;
    }
    
    .report-grade {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: 800;
        color: white;
    }
    
    .grade-a { background: linear-gradient(135deg, #4caf50, #388e3c); }
    .grade-b { background: linear-gradient(135deg, #2196f3, #1976d2); }
    .grade-c { background: linear-gradient(135deg, #ff9800, #f57c00); }
    .grade-f { background: linear-gradient(135deg, #f44336, #d32f2f); }
    
    /* Contacts Section */
    .contacts-section {
        background: white;
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.08);
    }
    
    .section-title {
        font-size: 1.5em;
        font-weight: 700;
        color: #1565c0;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .contact-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
    }
    
    .contact-card {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 15px;
        border-left: 4px solid #1976d2;
        transition: all 0.3s;
    }
    
    .contact-card:hover {
        background: #e3f2fd;
        transform: translateX(5px);
    }
    
    .contact-title {
        font-weight: 700;
        color: #263238;
        font-size: 1.1em;
        margin-bottom: 5px;
    }
    
    .contact-person {
        color: #546e7a;
        font-size: 0.9em;
        margin-bottom: 10px;
    }
    
    .contact-number {
        color: #d32f2f;
        font-weight: 700;
        font-size: 1.2em;
    }
    
    .contact-number-green {
        color: #388e3c;
        font-weight: 700;
        font-size: 1.1em;
    }
    
    /* Progress bars */
    .progress-container {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .question-card {
        background: white;
        border-radius: 25px;
        padding: 35px 30px;
        margin-bottom: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .animated-title { font-size: 2em; }
        .stats-bar { grid-template-columns: repeat(2, 1fr); }
        .dashboard-grid { grid-template-columns: 1fr; }
        .hero-title { font-size: 1.8em; }
        .topic-grid { grid-template-columns: 1fr; }
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
        topic TEXT,
        title TEXT NOT NULL,
        score REAL,
        total_questions INTEGER DEFAULT 0,
        correct_answers INTEGER DEFAULT 0,
        status TEXT DEFAULT 'pending',
        time_taken INTEGER DEFAULT 0,
        completed_at TIMESTAMP,
        answers TEXT,
        attempt_number INTEGER DEFAULT 1,
        passed BOOLEAN DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )""")
    
    conn.commit()
    conn.close()

def import_questions_from_csv():
    csv_path = "questions.csv"
    if not os.path.exists(csv_path):
        return False, 0, []
    
    try:
        df = pd.read_csv(csv_path)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM questions")
        
        imported_count = 0
        topics = set()
        
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
            
            topics.add(topic)
            
            c.execute("""
                INSERT INTO questions (question, options, correct_answer, category, marks)
                VALUES (?, ?, ?, ?, ?)
            """, (question, options, correct_idx, topic, 1))
            imported_count += 1
        
        conn.commit()
        conn.close()
        return True, imported_count, list(topics)
        
    except Exception as e:
        st.error(f"Import error: {e}")
        return False, 0, []

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_stats():
    """FIXED: Get dashboard statistics"""
    try:
        conn = get_db()
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM users")
        total_users = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM assessments WHERE status = 'completed'")
        completed = c.fetchone()[0]
        
        c.execute("SELECT AVG(score) FROM assessments WHERE status = 'completed'")
        avg_score = c.fetchone()[0] or 0
        
        c.execute("SELECT COUNT(*) FROM questions")
        total_q = c.fetchone()[0]
        
        conn.close()
        return total_users, completed, avg_score, total_q
    except Exception as e:
        st.error(f"Stats error: {e}")
        return 0, 0, 0, 0

def get_topics():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT DISTINCT category FROM questions ORDER BY category")
    topics = [row[0] for row in c.fetchall()]
    conn.close()
    return topics

def get_questions_by_topic(topic):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE category = ?", (topic,))
    questions = [dict(row) for row in c.fetchall()]
    conn.close()
    return questions

def get_topic_stats(user_id, topic):
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT * FROM assessments 
                 WHERE user_id = ? AND topic = ? 
                 ORDER BY attempt_number DESC LIMIT 1""", (user_id, topic))
    result = c.fetchone()
    conn.close()
    return dict(result) if result else None

def get_all_attempts(user_id, topic):
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT * FROM assessments 
                 WHERE user_id = ? AND topic = ? 
                 ORDER BY attempt_number ASC""", (user_id, topic))
    results = [dict(row) for row in c.fetchall()]
    conn.close()
    return results

def get_user_report_card(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT topic, score, passed, attempt_number, completed_at 
                 FROM assessments 
                 WHERE user_id = ? AND status = 'completed'
                 ORDER BY topic""", (user_id,))
    results = [dict(row) for row in c.fetchall()]
    
    c.execute("SELECT DISTINCT category FROM questions")
    all_topics = [row[0] for row in c.fetchall()]
    conn.close()
    
    return results, all_topics

# Initialize
init_db()

# Import questions on startup
if 'questions_imported' not in st.session_state:
    success, count, topics = import_questions_from_csv()
    st.session_state.questions_imported = True
    st.session_state.question_count = count
    st.session_state.available_topics = topics if topics else get_topics()

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'attempt_number' not in st.session_state:
    st.session_state.attempt_number = 1

# ==================== LOGIN PAGE ====================
def show_login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="login-card">
            <div class="logo-circle">
                <span class="logo-icon">🏥</span>
            </div>
            <h1 class="animated-title">Namaste! 🙏</h1>
            <p class="login-subtitle">Welcome to Medanta Induction Portal</p>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["✨ New Joiner", "🔑 Returning User"])
    
    with tab1:
        with st.form("reg_form"):
            st.markdown('<p class="form-label">Full Name *</p>', unsafe_allow_html=True)
            name = st.text_input("", placeholder="Your full name", label_visibility="collapsed")
            
            st.markdown('<p class="form-label">Email *</p>', unsafe_allow_html=True)
            email = st.text_input("", placeholder="you@medanta.org", label_visibility="collapsed")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<p class="form-label">Department *</p>', unsafe_allow_html=True)
                department = st.selectbox("", ["Select", "Nursing", "Medical", "Administration", 
                                              "HR", "Finance", "IT", "Operations"], label_visibility="collapsed")
            with col2:
                st.markdown('<p class="form-label">Designation *</p>', unsafe_allow_html=True)
                role = st.text_input("", placeholder="e.g. Staff Nurse", label_visibility="collapsed")
            
            submitted = st.form_submit_button("🚀 Get Started", use_container_width=True, type="primary")
            
            if submitted:
                if not name or not email or department == "Select" or not role:
                    st.error("Please fill all required fields")
                else:
                    conn = get_db()
                    c = conn.cursor()
                    c.execute("SELECT id FROM users WHERE email = ?", (email,))
                    if c.fetchone():
                        st.error("Email already registered")
                    else:
                        c.execute("""INSERT INTO users (name, email, department, role, employee_id) 
                                     VALUES (?, ?, ?, ?, ?)""",
                            (name, email, department, role, None))
                        user_id = c.lastrowid
                        conn.commit()
                        conn.close()
                        
                        st.session_state.user_id = user_id
                        st.session_state.user_name = name
                        st.session_state.page = 'dashboard'
                        st.rerun()
                    conn.close()
    
    with tab2:
        st.markdown('<p class="form-label">Email Address</p>', unsafe_allow_html=True)
        login_email = st.text_input("", placeholder="Enter registered email", key="login_email", label_visibility="collapsed")
        
        if st.button("▶️ Continue to Dashboard", use_container_width=True, type="primary"):
            conn = get_db()
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ?", (login_email,))
            user = c.fetchone()
            
            if user:
                st.session_state.user_id = user['id']
                st.session_state.user_name = user['name']
                conn.close()
                st.session_state.page = 'dashboard'
                st.rerun()
            else:
                st.error("Email not found. Please register first.")
            conn.close()
    
    st.markdown("""
        </div>
        <div style="text-align: center; margin-top: 30px; color: #78909c; font-size: 0.9em;">
            <p>© 2025 Medanta Hospital. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Admin access
    if st.button("🔐 Admin Portal", key="admin_btn"):
        st.session_state.page = 'admin_login'
        st.rerun()

# ==================== DASHBOARD PAGE ====================
def show_dashboard():
    if not st.session_state.user_id:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    # FIXED: Get stats with error handling
    try:
        total_users, completed, avg_score, total_q = get_stats()
    except:
        total_users, completed, avg_score, total_q = 0, 0, 0, 0
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # Top Navigation
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 35px;">🏥</span>
                <span style="color: #1565c0; font-weight: 700; font-size: 1.3em;">Medanta</span>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div style="text-align: center; color: #546e7a;">
                Welcome, <strong>{st.session_state.user_name}</strong>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        if st.button("Logout", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.user_name = None
            st.session_state.page = 'login'
            st.rerun()
    
    st.markdown("<hr style='margin: 20px 0; opacity: 0.2;'>", unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">Your Induction Dashboard</h1>
            <p class="hero-tagline">
                Access your handbook, complete topic-wise assessments, track your learning journey, 
                and connect with key contacts.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats Bar
    num_topics = len(st.session_state.get('available_topics', []))
    
    st.markdown(f"""
        <div class="stats-bar">
            <div class="stat-item">
                <span class="stat-value">{total_q}</span>
                <span class="stat-label">Questions</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{num_topics}</span>
                <span class="stat-label">Topics</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{completed}</span>
                <span class="stat-label">Completed</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{avg_score:.0f}%</span>
                <span class="stat-label">Avg Score</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Grid
    st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📚</div>
                <div class="feature-title">Employee Handbook</div>
                <div class="feature-desc">Access digital handbook with policies and guidelines</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("View Handbook", key="btn_handbook", use_container_width=True):
            st.session_state.page = 'handbook'
            st.rerun()
    
    with col2:
        st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">📝</div>
                <div class="feature-title">Assessment</div>
                <div class="feature-desc">Topic-wise assessments ({num_topics} topics)</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Start Assessment", key="btn_assessment", use_container_width=True):
            st.session_state.page = 'topics'
            st.rerun()
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Learning Journey</div>
                <div class="feature-desc">Track progress with report card</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("View Journey", key="btn_journey", use_container_width=True):
            st.session_state.page = 'journey'
            st.rerun()
    
    with col4:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📞</div>
                <div class="feature-title">Key Contacts</div>
                <div class="feature-desc">Important contacts for support</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("View Contacts", key="btn_contacts", use_container_width=True):
            st.session_state.page = 'contacts'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Key Contacts Preview
    st.markdown("""
        <div class="contacts-section">
            <div class="section-title">
                <span>📞</span>
                <span>Quick Contacts</span>
            </div>
            <div class="contact-grid">
                <div class="contact-card">
                    <div class="contact-title">EMR/HIS Query</div>
                    <div class="contact-person">Mr. Surjendra</div>
                    <div class="contact-number">📱 9883111600</div>
                </div>
                <div class="contact-card">
                    <div class="contact-title">IT Helpdesk</div>
                    <div class="contact-person">Internal Extension</div>
                    <div class="contact-number">📞 1010</div>
                </div>
                <div class="contact-card">
                    <div class="contact-title">Training</div>
                    <div class="contact-person">Dr. Pallavi & Mr. Rohit</div>
                    <div class="contact-number-green">📱 7860955988</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== HANDBOOK PAGE ====================
def show_handbook():
    if not st.session_state.user_id:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard", key="back_dash"):
        st.session_state.page = 'dashboard'
        st.rerun()
    
    st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">📚 Employee Handbook</h1>
            <p class="hero-tagline">Your complete guide to Medanta policies and procedures</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Embedded Handbook Link
    st.markdown("""
        <div style="background: white; border-radius: 20px; padding: 30px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); text-align: center;">
            <div style="font-size: 60px; margin-bottom: 20px;">📖</div>
            <h3 style="color: #1565c0; margin-bottom: 15px;">Digital Employee Handbook</h3>
            <p style="color: #78909c; margin-bottom: 25px;">Access the complete handbook with all policies, procedures, and guidelines</p>
            <a href="https://online.flippingbook.com/view/652486186/" target="_blank" 
               style="display: inline-block; background: linear-gradient(135deg, #1976d2, #1565c0); color: white; 
                      padding: 16px 40px; border-radius: 30px; text-decoration: none; font-weight: 600; 
                      font-size: 16px; box-shadow: 0 10px 30px rgba(25,118,210,0.3);">
                📖 Open Handbook
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick sections
    sections = [
        ("🏥", "About Medanta", "Our history, mission, vision, and values"),
        ("👔", "Code of Conduct", "Professional standards and behavior guidelines"),
        ("⏰", "Attendance Policy", "Working hours, leaves, and attendance tracking"),
        ("🔒", "Data Security", "HIPAA compliance and patient data protection"),
        ("🚨", "Emergency Procedures", "Fire safety, evacuation, and emergency contacts"),
        ("💼", "Benefits", "Health insurance, leaves, and employee perks")
    ]
    
    for icon, title, desc in sections:
        with st.expander(f"{icon} {title}"):
            st.write(desc)
            st.info("For detailed information, please refer to the Digital Handbook above.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== TOPICS PAGE ====================
def show_topics():
    if not st.session_state.user_id:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard", key="back_dash"):
        st.session_state.page = 'dashboard'
        st.rerun()
    
    st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">📝 Topic-wise Assessment</h1>
            <p class="hero-tagline">Complete assessments for each topic. You need 70% to pass. Unlimited attempts allowed!</p>
        </div>
    """, unsafe_allow_html=True)
    
    topics = st.session_state.get('available_topics', [])
    
    if not topics:
        st.warning("No topics found. Please check your questions.csv file.")
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    for topic in topics:
        # Get stats for this topic
        stats = get_topic_stats(st.session_state.user_id, topic)
        questions = get_questions_by_topic(topic)
        q_count = len(questions)
        
        # Determine status
        if stats:
            if stats['passed']:
                status_class = "status-passed"
                status_text = f"✓ Passed ({stats['score']:.0f}%)"
                btn_text = "Retake (Optional)"
                btn_type = "secondary"
            else:
                status_class = "status-failed"
                status_text = f"✗ Failed ({stats['score']:.0f}%) - Attempt {stats['attempt_number']}"
                btn_text = "Retake Assessment"
                btn_type = "primary"
        else:
            status_class = "status-pending"
            status_text = "Not Started"
            btn_text = "Start Assessment"
            btn_type = "primary"
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
                <div class="topic-card">
                    <div class="topic-name">{topic}</div>
                    <div class="topic-count">{q_count} questions • Passing: 70%</div>
                    <span class="topic-status {status_class}">{status_text}</span>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button(btn_text, key=f"topic_{topic}", use_container_width=True, type=btn_type):
                st.session_state.current_topic = topic
                st.session_state.questions = questions
                st.session_state.current_question = 0
                st.session_state.answers = []
                st.session_state.start_time = time.time()
                # Get attempt number
                if stats:
                    st.session_state.attempt_number = stats['attempt_number'] + 1
                else:
                    st.session_state.attempt_number = 1
                st.session_state.page = 'assessment'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== ASSESSMENT PAGE ====================
def show_assessment():
    if not st.session_state.user_id or not st.session_state.current_topic:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    questions = st.session_state.questions
    current = st.session_state.current_question
    topic = st.session_state.current_topic
    
    if current >= len(questions):
        submit_assessment()
        return
    
    total_questions = len(questions)
    progress = ((current) / total_questions) * 100
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # Header
    if st.button("← Exit Assessment", key="exit_assessment"):
        st.session_state.page = 'topics'
        st.rerun()
    
    st.markdown(f"""
        <div class="progress-container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <span style="font-weight: 700; color: #37474f; font-size: 18px;">
                    {topic} • Question {current + 1} of {total_questions}
                </span>
                <span style="background: linear-gradient(135deg, #1976d2, #42a5f5); color: white; 
                             padding: 10px 20px; border-radius: 25px; font-weight: 600;">
                    ⏱️ {int((time.time() - st.session_state.start_time) // 60):02d}:{int((time.time() - st.session_state.start_time) % 60):02d}
                </span>
            </div>
            <div style="background: #e3f2fd; height: 12px; border-radius: 6px; overflow: hidden;">
                <div style="width: {progress}%; height: 100%; background: linear-gradient(90deg, #1976d2, #42a5f5); 
                            border-radius: 6px; transition: width 0.5s ease;"></div>
            </div>
            <div style="margin-top: 10px; text-align: center; color: #78909c; font-size: 0.9em;">
                Attempt #{st.session_state.attempt_number} • Need 70% to pass
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Question
    q = questions[current]
    options = json.loads(q['options'])
    
    st.markdown(f"""
        <div class="question-card">
            <div style="color: #1976d2; font-size: 13px; font-weight: 700; text-transform: uppercase; 
                        letter-spacing: 1.5px; margin-bottom: 15px;">{topic}</div>
            <div style="font-size: 22px; font-weight: 600; color: #263238; line-height: 1.5;">{q['question']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Options
    for i, opt in enumerate(options):
        cols = st.columns([1, 12])
        with cols[0]:
            st.markdown(f"""
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #1976d2, #42a5f5); 
                            border-radius: 15px; display: flex; align-items: center; justify-content: center;
                            color: white; font-weight: 700; font-size: 20px; margin-top: 5px;
                            box-shadow: 0 8px 20px rgba(25,118,210,0.3);">{chr(65+i)}</div>
            """, unsafe_allow_html=True)
        with cols[1]:
            if st.button(opt, key=f"opt_{i}", use_container_width=True):
                st.session_state.answers.append(i)
                st.session_state.current_question += 1
                st.rerun()
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if current > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                st.session_state.current_question -= 1
                st.session_state.answers.pop()
                st.rerun()
    with col2:
        if st.button("Skip Question ⏭️", use_container_width=True):
            st.session_state.answers.append(-1)
            st.session_state.current_question += 1
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def submit_assessment():
    questions = st.session_state.questions
    answers = st.session_state.answers
    time_taken = int(time.time() - st.session_state.start_time)
    topic = st.session_state.current_topic
    
    correct = sum(1 for i, ans in enumerate(answers) 
                  if i < len(questions) and ans == questions[i]['correct_answer'])
    total = len(questions)
    score = (correct / total * 100) if total > 0 else 0
    passed = score >= 70
    
    conn = get_db()
    c = conn.cursor()
    c.execute("""INSERT INTO assessments (user_id, topic, title, score, total_questions, correct_answers, 
                                          status, time_taken, completed_at, answers, attempt_number, passed)
                 VALUES (?, ?, ?, ?, ?, ?, 'completed', ?, datetime('now'), ?, ?, ?)""",
        (st.session_state.user_id, topic, f"{topic} Assessment", score, total, correct, 
         time_taken, json.dumps(answers), st.session_state.attempt_number, passed))
    conn.commit()
    conn.close()
    
    st.session_state.page = 'result'
    st.rerun()

# ==================== RESULT PAGE ====================
def show_result():
    if not st.session_state.user_id:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT * FROM assessments 
                 WHERE user_id = ? AND topic = ? 
                 ORDER BY completed_at DESC LIMIT 1""", 
              (st.session_state.user_id, st.session_state.current_topic))
    result = c.fetchone()
    conn.close()
    
    if not result:
        st.error("No assessment found")
        return
    
    passed = result['passed']
    score = result['score']
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(f"""
            <div style="background: white; border-radius: 30px; padding: 50px 40px; text-align: center; 
                        margin-top: 30px; box-shadow: 0 30px 60px rgba(0,0,0,0.15);">
                <div style="font-size: 80px; margin-bottom: 20px;">{'🎉' if passed else '⚠️'}</div>
                <h2 style="color: {'#1976d2' if passed else '#ff7043'}; margin: 0; font-size: 36px; font-weight: 800;">
                    {'Congratulations!' if passed else 'Keep Trying!'}
                </h2>
                <p style="color: #78909c; margin: 15px 0 30px 0; font-size: 18px;">
                    {'You passed the assessment!' if passed else 'You need 70% to pass. Try again!'}
                </p>
                
                <div style="width: 180px; height: 180px; margin: 0 auto 30px auto; border-radius: 50%; 
                            background: {'linear-gradient(135deg, #4caf50, #388e3c)' if passed else 'linear-gradient(135deg, #ff9800, #f57c00)'};
                            display: flex; align-items: center; justify-content: center; 
                            box-shadow: 0 20px 50px rgba(0,0,0,0.15);">
                    <span style="color: white; font-size: 48px; font-weight: 800;">{score:.0f}%</span>
                </div>
                
                <div style="background: {'#e8f5e9' if passed else '#fff3e0'}; padding: 20px; border-radius: 15px; margin-bottom: 30px;">
                    <p style="margin: 0; color: {'#2e7d32' if passed else '#ef6c00'}; font-size: 16px; font-weight: 600;">
                        {'✓ Topic Completed! Move to next topic.' if passed else f'⚠ Attempt #{result["attempt_number"]} • Try again to score 70%+'}
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
        with col2:
            if st.button("📋 Back to Topics", use_container_width=True, type="primary"):
                st.session_state.page = 'topics'
                st.rerun()
        
        if not passed:
            if st.button("🔄 Retake Assessment", use_container_width=True, type="primary"):
                st.session_state.current_question = 0
                st.session_state.answers = []
                st.session_state.start_time = time.time()
                st.session_state.attempt_number = result['attempt_number'] + 1
                st.session_state.page = 'assessment'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== JOURNEY PAGE WITH REPORT CARD ====================
def show_journey():
    if not st.session_state.user_id:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    reports, all_topics = get_user_report_card(st.session_state.user_id)
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()
    
    st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">🎯 Learning Journey</h1>
            <p class="hero-tagline">Track your progress and view your report card</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Calculate overall stats
    passed_topics = sum(1 for r in reports if r['passed'])
    total_attempts = len(reports)
    avg_score = sum(r['score'] for r in reports) / len(reports) if reports else 0
    
    # Overall Progress
    st.markdown(f"""
        <div class="stats-bar" style="margin-bottom: 30px;">
            <div class="stat-item">
                <span class="stat-value">{passed_topics}/{len(all_topics)}</span>
                <span class="stat-label">Topics Passed</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{total_attempts}</span>
                <span class="stat-label">Total Attempts</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{avg_score:.0f}%</span>
                <span class="stat-label">Avg Score</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{len(all_topics) - passed_topics}</span>
                <span class="stat-label">Remaining</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Report Card
    st.markdown("""
        <div class="report-card">
            <div class="report-header">
                <div>
                    <div class="report-title">📊 Report Card</div>
                    <div style="color: #78909c; font-size: 0.9em;">{st.session_state.user_name}</div>
                </div>
    """, unsafe_allow_html=True)
    
    # Calculate grade
    if avg_score >= 90:
        grade, grade_class = "A", "grade-a"
    elif avg_score >= 80:
        grade, grade_class = "B", "grade-b"
    elif avg_score >= 70:
        grade, grade_class = "C", "grade-c"
    else:
        grade, grade_class = "F", "grade-f"
    
    st.markdown(f"""
                <div class="report-grade {grade_class}">{grade}</div>
            </div>
    """, unsafe_allow_html=True)
    
    # Topic-wise results table
    if reports:
        st.markdown("""
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: #e3f2fd;">
                        <th style="padding: 15px; text-align: left; color: #1565c0; font-weight: 600;">Topic</th>
                        <th style="padding: 15px; text-align: center; color: #1565c0; font-weight: 600;">Score</th>
                        <th style="padding: 15px; text-align: center; color: #1565c0; font-weight: 600;">Status</th>
                        <th style="padding: 15px; text-align: center; color: #1565c0; font-weight: 600;">Attempts</th>
                    </tr>
                </thead>
                <tbody>
        """, unsafe_allow_html=True)
        
        for report in reports:
            status_color = "#4caf50" if report['passed'] else "#f44336"
            status_icon = "✓" if report['passed'] else "✗"
            st.markdown(f"""
                <tr style="border-bottom: 1px solid #e0e0e0;">
                    <td style="padding: 15px; font-weight: 500;">{report['topic']}</td>
                    <td style="padding: 15px; text-align: center; font-weight: 700;">{report['score']:.0f}%</td>
                    <td style="padding: 15px; text-align: center; color: {status_color}; font-weight: 600;">{status_icon} {'Passed' if report['passed'] else 'Failed'}</td>
                    <td style="padding: 15px; text-align: center;">#{report['attempt_number']}</td>
                </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("</tbody></table>", unsafe_allow_html=True)
    else:
        st.info("No assessments completed yet. Start your learning journey!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Progress Tracker
    st.markdown("""
        <div class="report-card">
            <div class="report-title" style="margin-bottom: 25px;">🗺️ Progress Tracker</div>
    """, unsafe_allow_html=True)
    
    for topic in all_topics:
        # Find best score for this topic
        topic_reports = [r for r in reports if r['topic'] == topic]
        if topic_reports:
            best = max(topic_reports, key=lambda x: x['score'])
            passed = best['passed']
            score = best['score']
            status_icon = "✅" if passed else "⚠️"
            color = "#4caf50" if passed else "#ff9800"
        else:
            passed = False
            score = 0
            status_icon = "⭕"
            color = "#e0e0e0"
        
        st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 12px;">
                <div style="font-size: 30px; margin-right: 20px;">{status_icon}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #263238;">{topic}</div>
                    <div style="color: #78909c; font-size: 0.9em;">{'Best: ' + f'{score:.0f}%' if score > 0 else 'Not started'}</div>
                </div>
                <div style="width: 100px; height: 10px; background: #e0e0e0; border-radius: 5px; overflow: hidden;">
                    <div style="width: {score}%; height: 100%; background: {color}; border-radius: 5px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== CONTACTS PAGE ====================
def show_contacts():
    if not st.session_state.user_id:
        st.session_state.page = 'login'
        st.rerun()
        return
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()
    
    st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">📞 Key Contacts</h1>
            <p class="hero-tagline">Important contacts for your support</p>
        </div>
    """, unsafe_allow_html=True)
    
    contacts = [
        ("EMR/HIS Query", "Mr. Surjendra", "9883111600", "red"),
        ("IT Helpdesk", "Internal Extension", "1010", "red"),
        ("Salary Related", "HR Department", "9560719167", "red"),
        ("Onboarding Query", "HR Business Partner", "Contact your HRBP", "green"),
    ]
    
    cols = st.columns(2)
    for i, (title, person, number, color) in enumerate(contacts):
        with cols[i % 2]:
            num_color = "#d32f2f" if color == "red" else "#388e3c"
            st.markdown(f"""
                <div style="background: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; 
                            box-shadow: 0 5px 15px rgba(0,0,0,0.08); border-left: 4px solid #1976d2;">
                    <div style="font-weight: 700; color: #263238; font-size: 1.1em; margin-bottom: 5px;">{title}</div>
                    <div style="color: #546e7a; font-size: 0.9em; margin-bottom: 10px;">{person}</div>
                    <div style="color: {num_color}; font-weight: 700; font-size: 1.2em;">{number}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # Training contact
    st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 25px; border-radius: 15px; 
                    margin-bottom: 20px; border-left: 4px solid #388e3c;">
            <div style="font-weight: 700; color: #263238; font-size: 1.1em; margin-bottom: 5px;">Training Related</div>
            <div style="color: #546e7a; font-size: 0.9em; margin-bottom: 10px;">Dr. Pallavi & Mr. Rohit</div>
            <div style="display: flex; gap: 20px;">
                <div style="color: #388e3c; font-weight: 700; font-size: 1.1em;">📱 7860955988</div>
                <div style="color: #388e3c; font-weight: 700; font-size: 1.1em;">📱 7275181822</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== ADMIN PAGES ====================
def show_admin_login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    if st.button("← Back to Login"):
        st.session_state.page = 'login'
        st.rerun()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class="login-card" style="margin-top: 40px;">
                <div style="font-size: 60px; margin-bottom: 20px;">🔐</div>
                <h2 style="color: #1565c0; margin-bottom: 30px; font-size: 28px;">Admin Portal</h2>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("", type="password", placeholder="Enter password", label_visibility="collapsed")
        
        if st.button("Login", use_container_width=True, type="primary"):
            if pwd == "medanta123":
                st.session_state.admin_authenticated = True
                st.session_state.page = 'admin_dashboard'
                st.rerun()
            else:
                st.error("Invalid password")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_admin_dashboard():
    if 'admin_authenticated' not in st.session_state or not st.session_state.admin_authenticated:
        st.session_state.page = 'admin_login'
        st.rerun()
        return
    
    try:
        total_users, completed, avg_score, total_q = get_stats()
    except:
        total_users, completed, avg_score, total_q = 0, 0, 0, 0
    
    st.sidebar.title("🏥 Medanta Admin")
    admin_page = st.sidebar.radio("Menu", [
        "📊 Dashboard", "👥 Participants", "📝 Results", 
        "❓ Questions", "📁 Import CSV", "🚪 Logout"
    ])
    
    if admin_page == "🚪 Logout":
        st.session_state.admin_authenticated = False
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    if admin_page == "📊 Dashboard":
        st.title("Admin Dashboard")
        
        cols = st.columns(4)
        cols[0].metric("Total Questions", total_q)
        cols[1].metric("Total Users", total_users)
        cols[2].metric("Completed", completed)
        cols[3].metric("Avg Score", f"{avg_score:.1f}%")
        
        if completed > 0:
            st.bar_chart({"Completed": [completed], "Pending": [total_users - completed]})
        
        st.info(f"Topics: {len(st.session_state.get('available_topics', []))}")
    
    elif admin_page == "👥 Participants":
        st.title("All Participants")
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users ORDER BY created_at DESC")
        users = c.fetchall()
        conn.close()
        
        if users:
            df = pd.DataFrame([dict(row) for row in users])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button("⬇️ Export CSV", df.to_csv(index=False), "participants.csv")
    
    elif admin_page == "📝 Results":
        st.title("Assessment Results")
        conn = get_db()
        c = conn.cursor()
        c.execute("""SELECT a.*, u.name, u.email, u.department 
                     FROM assessments a JOIN users u ON a.user_id = u.id 
                     WHERE a.status = 'completed' ORDER BY a.completed_at DESC""")
        results = c.fetchall()
        conn.close()
        
        if results:
            df = pd.DataFrame([dict(row) for row in results])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button("⬇️ Export CSV", df.to_csv(index=False), "results.csv")
    
    elif admin_page == "❓ Questions":
        st.title(f"Question Bank ({total_q} questions)")
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM questions LIMIT 10")
        questions = c.fetchall()
        conn.close()
        
        for q in questions:
            opts = json.loads(q['options'])
            with st.expander(f"{q['category']}: {q['question'][:50]}..."):
                for i, opt in enumerate(opts):
                    if i == q['correct_answer']:
                        st.success(f"**{chr(65+i)}. {opt}** ✅")
                    else:
                        st.write(f"{chr(65+i)}. {opt}")
    
    elif admin_page == "📁 Import CSV":
        st.title("Import Questions")
        st.info(f"Current question count: {total_q}")
        st.info(f"Topics: {len(st.session_state.get('available_topics', []))}")
        
        uploaded = st.file_uploader("Upload CSV with columns: Question, Option A, Option B, Option C, Option D, Answer, Topic", type="csv")
        
        if uploaded:
            df = pd.read_csv(uploaded)
            st.write(f"Found {len(df)} questions")
            st.write("Preview:", df.head())
            
            if st.button("Import to Database", use_container_width=True, type="primary"):
                df.to_csv("questions.csv", index=False)
                success, count, topics = import_questions_from_csv()
                if success:
                    st.success(f"✅ Imported {count} questions!")
                    st.success(f"Topics found: {', '.join(topics)}")
                    st.session_state.question_count = count
                    st.session_state.available_topics = topics
                    st.balloons()
                else:
                    st.error("❌ Import failed")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== MAIN ====================
def main():
    page = st.session_state.page
    
    if page == 'login':
        show_login()
    elif page == 'dashboard':
        show_dashboard()
    elif page == 'handbook':
        show_handbook()
    elif page == 'topics':
        show_topics()
    elif page == 'assessment':
        show_assessment()
    elif page == 'result':
        show_result()
    elif page == 'journey':
        show_journey()
    elif page == 'contacts':
        show_contacts()
    elif page == 'admin_login':
        show_admin_login()
    elif page == 'admin_dashboard':
        show_admin_dashboard()
    else:
        show_login()

if __name__ == "__main__":
    main()
