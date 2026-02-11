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

# CSS with animations and dashboard styling
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
    
    .stApp {
        background: linear-gradient(135deg, #00695c 0%, #004d40 50%, #00352c 100%);
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
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        animation: float-particle 15s infinite;
    }
    
    @keyframes float-particle {
        0%, 100% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
    }
    
    /* Dashboard Container */
    .dashboard-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        position: relative;
        z-index: 1;
    }
    
    /* Top Navigation Bar */
    .top-nav {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 15px 25px;
        margin-bottom: 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .nav-logo {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .nav-logo-text {
        color: white;
        font-size: 1.5em;
        font-weight: 700;
    }
    
    .nav-links {
        display: flex;
        gap: 10px;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 40px 20px;
        margin-bottom: 40px;
    }
    
    .animated-title {
        font-size: 3.5em;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff, #80cbc4, #ffffff, #80cbc4);
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
    
    .hero-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.3em;
        font-weight: 300;
        margin-bottom: 10px;
    }
    
    .hero-tagline {
        color: rgba(255,255,255,0.7);
        font-size: 1em;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Dashboard Grid */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 25px;
        margin-bottom: 40px;
    }
    
    /* Feature Cards */
    .feature-card {
        background: rgba(255,255,255,0.95);
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        cursor: pointer;
        border: 3px solid transparent;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 30px 60px rgba(0,0,0,0.3);
        border-color: #00897b;
    }
    
    .feature-icon {
        width: 80px;
        height: 80px;
        margin: 0 auto 20px;
        background: linear-gradient(135deg, #00897b, #00695c);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        box-shadow: 0 10px 30px rgba(0,137,123,0.3);
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
    
    .feature-btn {
        background: linear-gradient(135deg, #00897b, #00695c);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s;
        display: inline-block;
        text-decoration: none;
    }
    
    .feature-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(0,137,123,0.4);
    }
    
    /* Stats Section */
    .stats-bar {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 40px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 2.5em;
        font-weight: 800;
        color: white;
        display: block;
    }
    
    .stat-label {
        color: rgba(255,255,255,0.7);
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Quick Access Section */
    .quick-section {
        background: rgba(255,255,255,0.95);
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 30px;
    }
    
    .section-title {
        font-size: 1.5em;
        font-weight: 700;
        color: #263238;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Contact Cards */
    .contact-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
    }
    
    .contact-card {
        background: #f5f5f5;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        transition: all 0.3s;
    }
    
    .contact-card:hover {
        background: #e0f2f1;
        transform: translateY(-5px);
    }
    
    .contact-icon {
        font-size: 30px;
        margin-bottom: 10px;
    }
    
    .contact-name {
        font-weight: 600;
        color: #263238;
        margin-bottom: 5px;
    }
    
    .contact-info {
        font-size: 0.85em;
        color: #78909c;
    }
    
    /* Footer */
    .dashboard-footer {
        text-align: center;
        padding: 30px;
        color: rgba(255,255,255,0.6);
        font-size: 0.9em;
    }
    
    /* Admin Link */
    .admin-access {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(255,255,255,0.2);
        padding: 10px 20px;
        border-radius: 30px;
        color: white;
        text-decoration: none;
        font-size: 0.85em;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s;
        z-index: 100;
    }
    
    .admin-access:hover {
        background: rgba(255,255,255,0.3);
        transform: scale(1.05);
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .animated-title { font-size: 2.5em; }
        .stats-bar { grid-template-columns: repeat(2, 1fr); }
        .dashboard-grid { grid-template-columns: 1fr; }
        .nav-links { display: none; }
    }
    
    /* Form Styling */
    .form-label {
        color: #37474f;
        font-weight: 600;
        font-size: 0.9em;
        margin-bottom: 8px;
        display: block;
    }
    
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 12px !important;
        border: 2px solid #e0e2e5 !important;
        padding: 14px !important;
        font-size: 16px !important;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00897b, #00695c) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    
    /* Assessment Styles */
    .progress-container {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .question-card {
        background: white;
        border-radius: 25px;
        padding: 35px 30px;
        margin-bottom: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .option-btn-modern {
        width: 100%;
        padding: 20px 25px;
        margin-bottom: 15px;
        background: white;
        border: 3px solid #e0f2f1;
        border-radius: 18px;
        text-align: left;
        font-size: 16px;
        color: #37474f;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .option-btn-modern:hover {
        border-color: #00897b;
        background: #f1f8f6;
        transform: translateX(10px);
    }
    
    .option-letter {
        width: 45px;
        height: 45px;
        background: linear-gradient(135deg, #00897b, #00bfa5);
        color: white;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 18px;
        flex-shrink: 0;
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
        return False, 0
    
    try:
        df = pd.read_csv(csv_path)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM questions")
        
        imported_count = 0
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
            imported_count += 1
        
        conn.commit()
        conn.close()
        return True, imported_count
        
    except Exception as e:
        st.error(f"Import error: {e}")
        return False, 0

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_question_count():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM questions")
    count = c.fetchone()[0]
    conn.close()
    return count

def get_stats():
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

# Initialize
init_db()

# Import questions on startup
if 'questions_imported' not in st.session_state:
    success, count = import_questions_from_csv()
    if success:
        st.session_state.questions_imported = True
        st.session_state.question_count = count
    else:
        # Add sample if no CSV
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM questions")
        if c.fetchone()[0] == 0:
            sample = [("Sample Question", json.dumps(["A", "B", "C", "D"]), 0, "General", 1)]
            c.executemany("INSERT INTO questions (question, options, correct_answer, category, marks) VALUES (?, ?, ?, ?, ?)", sample)
            conn.commit()
        c.execute("SELECT COUNT(*) FROM questions")
        st.session_state.question_count = c.fetchone()[0]
        conn.close()

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
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

def show_logo():
    try:
        logo_path = "Medanta Lucknow Logo.jpg"
        if os.path.exists(logo_path):
            image = Image.open(logo_path)
            return image
        else:
            github_url = "https://raw.githubusercontent.com/pspallavisingh349-ai/medanta-induction/main/Medanta%20Lucknow%20Logo.jpg"
            response = requests.get(github_url, timeout=5)
            if response.status_code == 200:
                return Image.open(BytesIO(response.content))
    except:
        pass
    return None

# ==================== DASHBOARD PAGE ====================
def show_dashboard():
    total_users, completed, avg_score, total_q = get_stats()
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # Top Navigation
    st.markdown("""
        <div class="top-nav">
            <div class="nav-logo">
                <span style="font-size: 40px;">🏥</span>
                <span class="nav-logo-text">Medanta Induction</span>
            </div>
            <div class="nav-links">
                <span style="color: rgba(255,255,255,0.8); font-size: 0.9em;">New Employee Portal</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <h1 class="animated-title">Namaste! 🙏</h1>
            <div class="hero-subtitle">Welcome to Medanta</div>
            <div class="hero-tagline">
                Your journey to excellence in healthcare begins here. 
                Access your handbook, complete assessments, and track your learning progress.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats Bar
    st.markdown(f"""
        <div class="stats-bar">
            <div class="stat-item">
                <span class="stat-value">{total_q}</span>
                <span class="stat-label">Questions</span>
            </div>
            <div class="stat-item">
                <span class="stat-value">{total_users}</span>
                <span class="stat-label">Employees</span>
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
    st.markdown("""
        <div class="dashboard-grid">
            <div class="feature-card" onclick="window.location.href='?page=handbook'">
                <div class="feature-icon">📚</div>
                <div class="feature-title">Employee Handbook</div>
                <div class="feature-desc">Access digital handbook, policies, and guidelines for new employees</div>
                <button class="feature-btn">View Handbook</button>
            </div>
            
            <div class="feature-card" onclick="window.location.href='?page=assessment_login'">
                <div class="feature-icon">📝</div>
                <div class="feature-title">Assessment</div>
                <div class="feature-desc">Complete your induction assessment with {} questions</div>
                <button class="feature-btn">Start Assessment</button>
            </div>
            
            <div class="feature-card" onclick="window.location.href='?page=journey'">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Learning Journey</div>
                <div class="feature-desc">Track your progress, milestones, and learning path</div>
                <button class="feature-btn">View Journey</button>
            </div>
            
            <div class="feature-card" onclick="window.location.href='?page=contacts'">
                <div class="feature-icon">📞</div>
                <div class="feature-title">Key Contacts</div>
                <div class="feature-desc">Important contacts for HR, IT, and department heads</div>
                <button class="feature-btn">View Contacts</button>
            </div>
        </div>
    """.format(total_q), unsafe_allow_html=True)
    
    # Quick Access / Recent Activity
    st.markdown("""
        <div class="quick-section">
            <div class="section-title">
                <span>⚡</span>
                <span>Quick Access</span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
                <div style="background: linear-gradient(135deg, #e3f2fd, #bbdefb); padding: 20px; border-radius: 15px;">
                    <div style="font-weight: 700; color: #1565c0; margin-bottom: 5px;">🆕 New Joiner?</div>
                    <div style="font-size: 0.9em; color: #546e7a;">Register and start your assessment</div>
                </div>
                <div style="background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 20px; border-radius: 15px;">
                    <div style="font-weight: 700; color: #2e7d32; margin-bottom: 5px;">🔑 Returning User?</div>
                    <div style="font-size: 0.9em; color: #546e7a;">Continue where you left off</div>
                </div>
                <div style="background: linear-gradient(135deg, #fff3e0, #ffe0b2); padding: 20px; border-radius: 15px;">
                    <div style="font-weight: 700; color: #ef6c00; margin-bottom: 5px;">📊 View Results</div>
                    <div style="font-size: 0.9em; color: #546e7a;">Check your assessment scores</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Key Contacts Preview
    st.markdown("""
        <div class="quick-section">
            <div class="section-title">
                <span>📞</span>
                <span>Emergency Contacts</span>
            </div>
            <div class="contact-grid">
                <div class="contact-card">
                    <div class="contact-icon">👨‍💼</div>
                    <div class="contact-name">HR Department</div>
                    <div class="contact-info">hr@medanta.org<br>Ext: 1001</div>
                </div>
                <div class="contact-card">
                    <div class="contact-icon">🖥️</div>
                    <div class="contact-name">IT Support</div>
                    <div class="contact-info">it@medanta.org<br>Ext: 2001</div>
                </div>
                <div class="contact-card">
                    <div class="contact-icon">🏥</div>
                    <div class="contact-name">Medical Affairs</div>
                    <div class="contact-info">medical@medanta.org<br>Ext: 3001</div>
                </div>
                <div class="contact-card">
                    <div class="contact-icon">🚨</div>
                    <div class="contact-name">Emergency</div>
                    <div class="contact-info">Emergency Line<br>Ext: 9999</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="dashboard-footer">
            <p>© 2025 Medanta Hospital. All rights reserved.</p>
            <p style="font-size: 0.85em; margin-top: 10px;">Building a healthier tomorrow, together.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Admin Access Button
    st.markdown('<a href="?page=admin_login" class="admin-access">🔐 Admin Portal</a>', unsafe_allow_html=True)
    
    # Handle card clicks with buttons (since HTML onclick doesn't work in Streamlit)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📚 Handbook", key="btn_handbook", use_container_width=True):
            st.session_state.page = 'handbook'
            st.rerun()
    with col2:
        if st.button("📝 Assessment", key="btn_assessment", use_container_width=True):
            st.session_state.page = 'assessment_login'
            st.rerun()
    with col3:
        if st.button("🎯 Journey", key="btn_journey", use_container_width=True):
            st.session_state.page = 'journey'
            st.rerun()
    with col4:
        if st.button("📞 Contacts", key="btn_contacts", use_container_width=True):
            st.session_state.page = 'contacts'
            st.rerun()

# ==================== ASSESSMENT LOGIN PAGE ====================
def show_assessment_login():
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # Back button
    if st.button("← Back to Dashboard", key="back_dash"):
        st.session_state.page = 'dashboard'
        st.rerun()
    
    st.markdown("""
        <div class="hero-section" style="padding: 20px;">
            <h1 style="color: white; font-size: 2.5em; margin-bottom: 10px;">📝 Assessment</h1>
            <p style="color: rgba(255,255,255,0.8);">Complete your induction assessment</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<div class="quick-section">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["✨ New Registration", "🔑 Continue"])
        
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
                
                submitted = st.form_submit_button("🚀 Start Assessment", use_container_width=True, type="primary")
                
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
                            st.session_state.page = 'assessment'
                            st.session_state.questions = []
                            st.session_state.current_question = 0
                            st.session_state.answers = []
                            st.session_state.start_time = time.time()
                            st.rerun()
                        conn.close()
        
        with tab2:
            st.markdown('<p class="form-label">Email Address</p>', unsafe_allow_html=True)
            login_email = st.text_input("", placeholder="Enter registered email", key="login_email", label_visibility="collapsed")
            
            if st.button("▶️ Continue Assessment", use_container_width=True, type="primary"):
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
                    st.error("Email not found")
                conn.close()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== ASSESSMENT PAGE ====================
def show_assessment():
    # Load questions if not loaded
    if not st.session_state.questions:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM questions")
        rows = c.fetchall()
        st.session_state.questions = [dict(row) for row in rows]
        conn.close()
    
    questions = st.session_state.questions
    current = st.session_state.current_question
    
    if current >= len(questions):
        submit_assessment()
        return
    
    total_questions = len(questions)
    progress = ((current) / total_questions) * 100
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    # Progress Header
    st.markdown(f"""
        <div class="progress-container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <span style="font-weight: 700; color: #37474f; font-size: 18px;">
                    Question {current + 1} of {total_questions}
                </span>
                <span style="background: linear-gradient(135deg, #00897b, #00695c); color: white; 
                             padding: 10px 20px; border-radius: 25px; font-weight: 600;">
                    ⏱️ {int((time.time() - st.session_state.start_time) // 60):02d}:{int((time.time() - st.session_state.start_time) % 60):02d}
                </span>
            </div>
            <div style="background: #e0f2f1; height: 12px; border-radius: 6px; overflow: hidden;">
                <div style="width: {progress}%; height: 100%; background: linear-gradient(90deg, #00897b, #00bfa5); 
                            border-radius: 6px; transition: width 0.5s ease;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Question Card
    q = questions[current]
    options = json.loads(q['options'])
    
    st.markdown(f"""
        <div class="question-card">
            <div style="color: #00897b; font-size: 13px; font-weight: 700; text-transform: uppercase; 
                        letter-spacing: 1.5px; margin-bottom: 15px;">{q['category']}</div>
            <div style="font-size: 22px; font-weight: 600; color: #263238; line-height: 1.5;">{q['question']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Options
    for i, opt in enumerate(options):
        cols = st.columns([1, 12])
        with cols[0]:
            st.markdown(f"""
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #00897b, #00bfa5); 
                            border-radius: 15px; display: flex; align-items: center; justify-content: center;
                            color: white; font-weight: 700; font-size: 20px; margin-top: 5px;
                            box-shadow: 0 8px 20px rgba(0,137,123,0.3);">{chr(65+i)}</div>
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
    
    correct = sum(1 for i, ans in enumerate(answers) 
                  if i < len(questions) and ans == questions[i]['correct_answer'])
    total = len(questions)
    score = (correct / total * 100) if total > 0 else 0
    
    conn = get_db()
    c = conn.cursor()
    c.execute("""INSERT INTO assessments (user_id, title, score, total_questions, correct_answers, 
                                          status, time_taken, completed_at, answers)
                 VALUES (?, ?, ?, ?, ?, 'completed', ?, datetime('now'), ?)""",
        (st.session_state.user_id, "Induction Assessment", score, total, correct, time_taken, json.dumps(answers)))
    c.execute("UPDATE users SET status = 'completed', completion_percentage = ? WHERE id = ?", 
              (score, st.session_state.user_id))
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
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(f"""
            <div style="background: white; border-radius: 30px; padding: 50px 40px; text-align: center; 
                        margin-top: 30px; box-shadow: 0 30px 60px rgba(0,0,0,0.3);">
                <div style="font-size: 80px; margin-bottom: 20px; animation: bounce 2s infinite;">{'🎉' if passed else '👏'}</div>
                <h2 style="color: {'#00897b' if passed else '#ff7043'}; margin: 0; font-size: 36px; font-weight: 800;">
                    {'Congratulations!' if passed else 'Great Effort!'}
                </h2>
                <p style="color: #78909c; margin: 15px 0 40px 0; font-size: 18px;">
                    {'You successfully passed the induction!' if passed else 'Thank you for completing the assessment.'}
                </p>
                
                <div style="width: 200px; height: 200px; margin: 0 auto 40px auto; border-radius: 50%; 
                            background: {'linear-gradient(135deg, #00897b, #00bfa5)' if passed else 'linear-gradient(135deg, #ff7043, #f4511e)'};
                            display: flex; align-items: center; justify-content: center; 
                            box-shadow: 0 20px 50px rgba(0,0,0,0.2); animation: pulse 2s infinite;">
                    <span style="color: white; font-size: 56px; font-weight: 800;">{result['score']:.0f}%</span>
                </div>
                
                <div style="display: flex; justify-content: space-around; margin-bottom: 30px;">
                    <div style="text-align: center;">
                        <div style="font-size: 32px; font-weight: 800; color: #37474f;">{result['correct_answers']}</div>
                        <div style="font-size: 14px; color: #90a4ae; text-transform: uppercase; letter-spacing: 1px;">Correct</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 32px; font-weight: 800; color: #37474f;">{result['total_questions']}</div>
                        <div style="font-size: 14px; color: #90a4ae; text-transform: uppercase; letter-spacing: 1px;">Total</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 32px; font-weight: 800; color: #37474f;">{result['time_taken']//60}m</div>
                        <div style="font-size: 14px; color: #90a4ae; text-transform: uppercase; letter-spacing: 1px;">Time</div>
                    </div>
                </div>
                
                <div style="background: {'#e8f5e9' if passed else '#fff3e0'}; padding: 25px; border-radius: 20px; margin-bottom: 30px;">
                    <p style="margin: 0; color: {'#2e7d32' if passed else '#ef6c00'}; font-size: 16px; font-weight: 600;">
                        {'✓ Certificate unlocked! Check your email for details.' if passed else '⚠ Review materials and retake if needed.'}
                    </p>
                </div>
                
                <button onclick="window.location.href='?page=dashboard'" style="background: linear-gradient(135deg, #00897b, #00695c); 
                        color: white; border: none; padding: 18px 40px; border-radius: 30px; font-size: 18px; 
                        font-weight: 600; cursor: pointer; width: 100%;">🏠 Back to Dashboard</button>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 Back to Dashboard", use_container_width=True, type="primary"):
            st.session_state.page = 'dashboard'
            st.session_state.user_id = None
            st.session_state.user_name = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== HANDBOOK PAGE ====================
def show_handbook():
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()
    
    st.markdown("""
        <div class="hero-section">
            <h1 style="color: white; font-size: 2.5em;">📚 Employee Handbook</h1>
            <p style="color: rgba(255,255,255,0.8);">Your guide to Medanta policies and procedures</p>
        </div>
    """, unsafe_allow_html=True)
    
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
            st.info("Detailed content will be loaded from your handbook document.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== LEARNING JOURNEY PAGE ====================
def show_journey():
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()
    
    st.markdown("""
        <div class="hero-section">
            <h1 style="color: white; font-size: 2.5em;">🎯 Learning Journey</h1>
            <p style="color: rgba(255,255,255,0.8);">Track your induction progress</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Progress tracker
    steps = [
        ("📋", "Registration", "Complete your profile", True),
        ("📖", "Handbook Review", "Read employee handbook", False),
        ("📝", "Assessment", "Complete induction test", False),
        ("🎓", "Certification", "Download certificate", False)
    ]
    
    for i, (icon, title, desc, completed) in enumerate(steps):
        col1, col2 = st.columns([1, 10])
        with col1:
            color = "#00897b" if completed else "#e0e0e0"
            st.markdown(f"""
                <div style="width: 50px; height: 50px; background: {color}; border-radius: 50%; 
                            display: flex; align-items: center; justify-content: center; color: white; 
                            font-size: 24px; margin: 0 auto;">{icon}</div>
                {'' if i == len(steps)-1 else '<div style="width: 4px; height: 40px; background: #e0e0e0; margin: 5px auto;"></div>'}
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style="background: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
                    <div style="font-weight: 700; color: #263238; font-size: 18px;">{title}</div>
                    <div style="color: #78909c;">{desc}</div>
                    {'<div style="color: #00897b; font-weight: 600; margin-top: 10px;">✓ Completed</div>' if completed else ''}
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== CONTACTS PAGE ====================
def show_contacts():
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()
    
    st.markdown("""
        <div class="hero-section">
            <h1 style="color: white; font-size: 2.5em;">📞 Key Contacts</h1>
            <p style="color: rgba(255,255,255,0.8);">Important contacts for your support</p>
        </div>
    """, unsafe_allow_html=True)
    
    contacts = [
        ("👨‍💼", "HR Department", "hr@medanta.org", "Ext: 1001", "Mon-Fri 9AM-6PM"),
        ("🖥️", "IT Support", "it@medanta.org", "Ext: 2001", "24/7 Support"),
        ("🏥", "Medical Affairs", "medical@medanta.org", "Ext: 3001", "Mon-Fri 8AM-8PM"),
        ("🚨", "Emergency", "emergency@medanta.org", "Ext: 9999", "24/7 Emergency"),
        ("🔧", "Facilities", "facilities@medanta.org", "Ext: 4001", "Mon-Sat 8AM-8PM"),
        ("📚", "Training", "training@medanta.org", "Ext: 5001", "Mon-Fri 9AM-5PM")
    ]
    
    cols = st.columns(2)
    for i, (icon, dept, email, ext, hours) in enumerate(contacts):
        with cols[i % 2]:
            st.markdown(f"""
                <div style="background: white; padding: 25px; border-radius: 20px; margin-bottom: 20px; 
                            box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                        <div style="font-size: 40px;">{icon}</div>
                        <div style="font-weight: 700; color: #263238; font-size: 18px;">{dept}</div>
                    </div>
                    <div style="color: #546e7a; line-height: 1.8;">
                        📧 {email}<br>
                        📞 {ext}<br>
                        🕐 {hours}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== ADMIN PAGES ====================
def show_admin_login():
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background: rgba(255,255,255,0.95); padding: 50px; border-radius: 30px; 
                        text-align: center; margin-top: 60px; box-shadow: 0 30px 60px rgba(0,0,0,0.3);">
                <div style="font-size: 60px; margin-bottom: 20px;">🔐</div>
                <h2 style="color: #00897b; margin-bottom: 30px; font-size: 28px;">Admin Portal</h2>
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
    
    total_users, completed, avg_score, total_q = get_stats()
    
    st.sidebar.title("🏥 Medanta Admin")
    admin_page = st.sidebar.radio("Menu", [
        "📊 Dashboard", "👥 Participants", "📝 Results", 
        "❓ Questions", "📁 Import CSV", "🚪 Logout"
    ])
    
    if admin_page == "🚪 Logout":
        st.session_state.admin_authenticated = False
        st.session_state.page = 'dashboard'
        st.rerun()
    
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    if admin_page == "📊 Dashboard":
        st.title("Admin Dashboard")
        
        # Stats
        cols = st.columns(4)
        cols[0].metric("Total Questions", total_q)
        cols[1].metric("Total Users", total_users)
        cols[2].metric("Completed", completed)
        cols[3].metric("Avg Score", f"{avg_score:.1f}%")
        
        # Charts
        if completed > 0:
            st.bar_chart({"Completed": [completed], "Pending": [total_users - completed]})
        
        # Recent activity
        st.subheader("Recent Activity")
        conn = get_db()
        c = conn.cursor()
        c.execute("""SELECT u.name, u.department, a.score, a.completed_at 
                     FROM assessments a JOIN users u ON a.user_id = u.id 
                     WHERE a.status = 'completed' ORDER BY a.completed_at DESC LIMIT 5""")
        recent = c.fetchall()
        conn.close()
        
        if recent:
            for r in recent:
                st.write(f"✓ {r['name']} ({r['department']}) - Score: {r['score']:.0f}%")
    
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
        
        uploaded = st.file_uploader("Upload CSV (with columns: Question, Option A, Option B, Option C, Option D, Answer, Category)", type="csv")
        
        if uploaded:
            df = pd.read_csv(uploaded)
            st.write(f"Found {len(df)} questions in CSV")
            st.write("Preview:", df.head())
            
            if st.button("Import to Database", use_container_width=True, type="primary"):
                df.to_csv("questions.csv", index=False)
                success, count = import_questions_from_csv()
                if success:
                    st.success(f"✅ Successfully imported {count} questions!")
                    st.session_state.question_count = count
                    st.balloons()
                else:
                    st.error("❌ Import failed")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== MAIN ====================
def main():
    query = st.query_params
    
    # Handle URL parameters
    if query.get("page") == "admin":
        if 'admin_authenticated' in st.session_state and st.session_state.admin_authenticated:
            st.session_state.page = 'admin_dashboard'
        else:
            st.session_state.page = 'admin_login'
    
    page = st.session_state.page
    
    if page == 'dashboard':
        show_dashboard()
    elif page == 'assessment_login':
        show_assessment_login()
    elif page == 'assessment':
        show_assessment()
    elif page == 'result':
        show_result()
    elif page == 'handbook':
        show_handbook()
    elif page == 'journey':
        show_journey()
    elif page == 'contacts':
        show_contacts()
    elif page == 'admin_login':
        show_admin_login()
    elif page == 'admin_dashboard':
        show_admin_dashboard()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
