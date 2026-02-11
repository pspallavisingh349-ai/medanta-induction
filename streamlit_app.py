import streamlit as st
import pandas as pd
import sqlite3
import json
import time
import os
from datetime import datetime

# Page config - Mobile optimized
st.set_page_config(
    page_title="Medanta Induction",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Mobile-first CSS with modern interactions
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        -webkit-tap-highlight-color: transparent;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(180deg, #00695c 0%, #004d40 100%);
        min-height: 100vh;
    }
    
    /* Mobile-optimized container */
    .main-container {
        max-width: 100%;
        padding: 0;
        margin: 0 auto;
    }
    
    @media (min-width: 768px) {
        .main-container {
            max-width: 600px;
            padding: 20px;
        }
    }
    
    /* Floating medical icons background */
    .bg-icons {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
        opacity: 0.03;
    }
    
    .bg-icon {
        position: absolute;
        font-size: 40px;
        animation: float 20s infinite ease-in-out;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(100vh) rotate(0deg); }
        50% { transform: translateY(-10vh) rotate(180deg); }
    }
    
    /* Compact glass card */
    .glass-card {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 24px 20px;
        margin: 10px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    @media (min-width: 768px) {
        .glass-card {
            padding: 40px;
            margin: 20px auto;
        }
    }
    
    /* Animated logo with pulse */
    .logo-wrapper {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .logo-ring {
        width: 100px;
        height: 100px;
        margin: 0 auto;
        background: linear-gradient(135deg, #00897b 0%, #00695c 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        box-shadow: 0 10px 30px rgba(0,137,123,0.4);
    }
    
    .logo-ring::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: inherit;
        animation: pulse-ring 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
        z-index: -1;
    }
    
    @keyframes pulse-ring {
        0% { transform: scale(0.95); opacity: 0.8; }
        50% { transform: scale(1.2); opacity: 0; }
        100% { transform: scale(0.95); opacity: 0; }
    }
    
    .logo-icon {
        font-size: 50px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
    }
    
    /* Typography */
    .greeting {
        text-align: center;
        margin-bottom: 8px;
    }
    
    .greeting h1 {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(90deg, #00897b, #00bfa5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    
    .subtitle {
        text-align: center;
        color: #546e7a;
        font-size: 14px;
        margin-bottom: 24px;
        line-height: 1.5;
    }
    
    /* Segmented control for tabs */
    .segmented-control {
        display: flex;
        background: #f5f5f5;
        border-radius: 12px;
        padding: 4px;
        margin-bottom: 24px;
    }
    
    .segment-btn {
        flex: 1;
        padding: 12px 8px;
        border: none;
        background: transparent;
        border-radius: 10px;
        font-size: 14px;
        font-weight: 600;
        color: #78909c;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .segment-btn.active {
        background: white;
        color: #00897b;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Form styling - Mobile optimized */
    .form-group {
        margin-bottom: 16px;
    }
    
    .form-label {
        display: block;
        font-size: 13px;
        font-weight: 600;
        color: #37474f;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .required::after {
        content: ' *';
        color: #e53935;
    }
    
    /* Custom inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextInput > div > div > input:focus {
        border: 2px solid #e0f2f1 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-size: 16px !important;
        background: #fafafa !important;
        transition: all 0.2s !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #00897b !important;
        background: white !important;
        box-shadow: 0 0 0 4px rgba(0,137,123,0.1) !important;
    }
    
    /* Primary button - Full width mobile */
    .btn-primary {
        width: 100%;
        padding: 16px;
        background: linear-gradient(135deg, #00897b 0%, #00695c 100%);
        color: white;
        border: none;
        border-radius: 14px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,137,123,0.3);
        transition: all 0.2s;
        margin-top: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    
    .btn-primary:active {
        transform: scale(0.98);
        box-shadow: 0 2px 8px rgba(0,137,123,0.3);
    }
    
    /* Secondary button */
    .btn-secondary {
        width: 100%;
        padding: 14px;
        background: transparent;
        color: #00897b;
        border: 2px solid #00897b;
        border-radius: 14px;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        margin-top: 12px;
    }
    
    .btn-secondary:active {
        background: rgba(0,137,123,0.05);
    }
    
    /* Quick login options */
    .quick-login {
        margin-top: 24px;
        padding-top: 24px;
        border-top: 1px solid #e0e0e0;
    }
    
    .quick-login-title {
        text-align: center;
        font-size: 13px;
        color: #90a4ae;
        margin-bottom: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .id-input-wrapper {
        display: flex;
        gap: 12px;
        align-items: center;
    }
    
    .id-input-wrapper .stTextInput {
        flex: 1;
    }
    
    /* Assessment page styles */
    .assessment-header {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .progress-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    
    .progress-text {
        font-size: 14px;
        font-weight: 600;
        color: #37474f;
    }
    
    .timer-badge {
        background: linear-gradient(135deg, #00897b, #00695c);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .progress-bar-bg {
        height: 8px;
        background: #e0f2f1;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #00897b, #00bfa5);
        border-radius: 4px;
        transition: width 0.5s ease;
    }
    
    /* Question card */
    .question-card {
        background: white;
        border-radius: 20px;
        padding: 24px 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .question-number {
        font-size: 12px;
        font-weight: 700;
        color: #00897b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }
    
    .question-text {
        font-size: 18px;
        font-weight: 600;
        color: #263238;
        line-height: 1.5;
        margin-bottom: 24px;
    }
    
    /* Option buttons - Large touch targets */
    .option-btn {
        width: 100%;
        padding: 18px 20px;
        margin-bottom: 12px;
        background: white;
        border: 2px solid #e0f2f1;
        border-radius: 16px;
        text-align: left;
        font-size: 16px;
        color: #37474f;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .option-btn:hover {
        border-color: #00897b;
        background: #f1f8f6;
    }
    
    .option-btn:active {
        transform: scale(0.99);
        background: #e0f2f1;
    }
    
    .option-letter {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #00897b, #00bfa5);
        color: white;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 14px;
        flex-shrink: 0;
    }
    
    /* Bottom navigation */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 16px 20px;
        box-shadow: 0 -10px 30px rgba(0,0,0,0.1);
        display: flex;
        gap: 12px;
        z-index: 100;
    }
    
    @media (min-width: 768px) {
        .nav-bar {
            position: relative;
            background: transparent;
            box-shadow: none;
            padding: 0;
            margin-top: 20px;
        }
    }
    
    .nav-btn {
        flex: 1;
        padding: 16px;
        border-radius: 14px;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        border: none;
    }
    
    .nav-btn-secondary {
        background: #f5f5f5;
        color: #546e7a;
    }
    
    .nav-btn-primary {
        background: linear-gradient(135deg, #00897b, #00695c);
        color: white;
    }
    
    /* Results page */
    .result-card {
        text-align: center;
        padding: 40px 24px;
    }
    
    .result-emoji {
        font-size: 80px;
        margin-bottom: 16px;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .score-circle {
        width: 160px;
        height: 160px;
        margin: 24px auto;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .score-circle::before {
        content: '';
        position: absolute;
        inset: 4px;
        border-radius: 50%;
        background: white;
    }
    
    .score-value {
        position: relative;
        font-size: 42px;
        font-weight: 800;
        color: #00897b;
    }
    
    .score-label {
        font-size: 14px;
        color: #78909c;
        margin-top: 8px;
    }
    
    /* Admin compact */
    .admin-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-bottom: 24px;
    }
    
    .stat-box {
        background: white;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .stat-value {
        font-size: 32px;
        font-weight: 800;
        color: #00897b;
    }
    
    .stat-label {
        font-size: 12px;
        color: #78909c;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
    
    /* Hide Streamlit elements */
    .stButton > button {
        width: 100%;
    }
    
    /* Smooth transitions */
    div[data-testid="stVerticalBlock"] > div {
        animation: fadeIn 0.4s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>

<!-- Background animation -->
<div class="bg-icons">
    <div class="bg-icon" style="left: 10%; animation-delay: 0s;">🏥</div>
    <div class="bg-icon" style="left: 30%; animation-delay: 5s;">💊</div>
    <div class="bg-icon" style="left: 50%; animation-delay: 10s;">❤️</div>
    <div class="bg-icon" style="left: 70%; animation-delay: 15s;">🩺</div>
    <div class="bg-icon" style="left: 90%; animation-delay: 8s;">⚕️</div>
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
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'register'

# ==================== HOME PAGE ====================
def show_home():
    st.markdown('<div class="main-container"><div class="glass-card">', unsafe_allow_html=True)
    
    # Logo
    st.markdown("""
        <div class="logo-wrapper">
            <div class="logo-ring">
                <span class="logo-icon">🏥</span>
            </div>
        </div>
        <div class="greeting">
            <h1>Namaste <span style="font-size: 0.8em;">🙏</span></h1>
        </div>
        <p class="subtitle">Welcome to Medanta<br>Begin your journey with excellence in healthcare</p>
    """, unsafe_allow_html=True)
    
    # Segmented control for tabs
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✨ New Joiner", use_container_width=True, 
                    type="primary" if st.session_state.active_tab == 'register' else "secondary"):
            st.session_state.active_tab = 'register'
            st.rerun()
    with col2:
        if st.button("🔑 Returning", use_container_width=True,
                    type="primary" if st.session_state.active_tab == 'login' else "secondary"):
            st.session_state.active_tab = 'login'
            st.rerun()
    
    # Registration Form
    if st.session_state.active_tab == 'register':
        with st.form("reg_form", clear_on_submit=False):
            st.markdown('<p class="form-label required">Full Name</p>', unsafe_allow_html=True)
            name = st.text_input("", placeholder="Your full name", label_visibility="collapsed")
            
            st.markdown('<p class="form-label required">Email</p>', unsafe_allow_html=True)
            email = st.text_input("", placeholder="you@medanta.org", label_visibility="collapsed")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<p class="form-label required">Department</p>', unsafe_allow_html=True)
                department = st.selectbox("", ["Select", "Nursing", "Medical", "Administration", 
                                              "HR", "Finance", "IT", "Operations"], label_visibility="collapsed")
            with col2:
                st.markdown('<p class="form-label required">Designation</p>', unsafe_allow_html=True)
                role = st.text_input("", placeholder="e.g. Staff Nurse", label_visibility="collapsed")
            
            st.markdown('<p class="form-label">Employee ID (if available)</p>', unsafe_allow_html=True)
            employee_id = st.text_input("", placeholder="Optional", label_visibility="collapsed")
            
            submitted = st.form_submit_button("🚀 Start Assessment")
            
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
    
    # Login Form
    else:
        st.markdown('<div style="margin-top: 24px;">', unsafe_allow_html=True)
        
        st.markdown('<p class="form-label">Email Address</p>', unsafe_allow_html=True)
        login_email = st.text_input("", placeholder="Enter registered email", key="login_email", label_visibility="collapsed")
        
        if st.button("▶️ Continue Assessment", type="primary"):
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
        
        # Quick ID login
        st.markdown("""
            <div class="quick-login">
                <p class="quick-login-title">Quick Access</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            login_id = st.text_input("", placeholder="Enter Participant ID", key="login_id", label_visibility="collapsed")
        with col2:
            if st.button("Go", use_container_width=True):
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
                        else:
                            st.error("Invalid ID")
                    except:
                        st.error("Invalid ID")
    
    # Admin link
    st.markdown("""
        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0;">
            <a href="?page=admin" style="color: #00897b; text-decoration: none; font-size: 14px; font-weight: 600;">
                🔐 Admin Portal
            </a>
        </div>
        </div></div>
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
    progress = (current / len(questions)) * 100
    
    st.markdown(f"""
        <div class="assessment-header">
            <div class="progress-info">
                <span class="progress-text">Question {current + 1} of {len(questions)}</span>
                <span class="timer-badge">⏱️ {int((time.time() - st.session_state.start_time) // 60):02d}:{int((time.time() - st.session_state.start_time) % 60):02d}</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {progress}%"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Question card
    q = questions[current]
    options = json.loads(q['options'])
    
    st.markdown(f"""
        <div class="question-card">
            <div class="question-number">{q['category']}</div>
            <div class="question-text">{q['question']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Options with large touch targets
    for i, opt in enumerate(options):
        if st.button(f"{opt}", key=f"opt_{i}", use_container_width=True):
            st.session_state.answers.append(i)
            st.session_state.current_question += 1
            st.rerun()
    
    # Bottom navigation
    st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if current > 0:
            if st.button("⬅️ Back", use_container_width=True):
                st.session_state.current_question -= 1
                st.session_state.answers.pop()
                st.rerun()
        else:
            st.button("⬅️ Back", use_container_width=True, disabled=True)
    with col2:
        if st.button("Skip ⏭️", use_container_width=True):
            st.session_state.answers.append(-1)
            st.session_state.current_question += 1
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

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
        <div class="main-container">
            <div class="glass-card result-card">
                <div class="result-emoji">{'🎉' if passed else '👏'}</div>
                <h2 style="color: {'#00897b' if passed else '#ff7043'}; margin: 0; font-size: 28px;">
                    {'Excellent!' if passed else 'Good Effort!'}
                </h2>
                <p style="color: #78909c; margin: 8px 0 24px 0; font-size: 16px;">
                    {'You passed the induction' if passed else 'Keep learning and growing'}
                </p>
                
                <div class="score-circle" style="background: {'linear-gradient(135deg, #00897b, #00bfa5)' if passed else 'linear-gradient(135deg, #ff7043, #f4511e)'};">
                    <div class="score-value">{result['score']:.0f}%</div>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 24px 0;">
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: 700; color: #37474f;">{result['correct_answers']}</div>
                        <div style="font-size: 12px; color: #90a4ae; text-transform: uppercase;">Correct</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: 700; color: #37474f;">{result['total_questions']}</div>
                        <div style="font-size: 12px; color: #90a4ae; text-transform: uppercase;">Total</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: 700; color: #37474f;">{result['time_taken']//60}m</div>
                        <div style="font-size: 12px; color: #90a4ae; text-transform: uppercase;">Time</div>
                    </div>
                </div>
                
                <div style="background: {'#e8f5e9' if passed else '#fff3e0'}; padding: 16px; border-radius: 12px; margin-bottom: 24px;">
                    <p style="margin: 0; color: {'#2e7d32' if passed else '#ef6c00'}; font-size: 14px; font-weight: 500; text-align: center;">
                        {'✓ Certificate unlocked! Check your email.' if passed else '⚠ Review required materials and retake if needed.'}
                    </p>
                </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏠 Back to Home", use_container_width=True, type="primary"):
        st.session_state.page = 'home'
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ==================== ADMIN PAGE ====================
def show_admin():
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        st.markdown("""
            <div class="main-container" style="margin-top: 60px;">
                <div class="glass-card" style="text-align: center; padding: 40px 24px;">
                    <div style="font-size: 60px; margin-bottom: 16px;">🔐</div>
                    <h2 style="color: #00897b; margin-bottom: 24px;">Admin Access</h2>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("", type="password", placeholder="Enter password", label_visibility="collapsed")
        
        if st.button("Unlock", use_container_width=True, type="primary"):
            if pwd == "medanta123":
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Invalid password")
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        return
    
    # Admin sidebar
    with st.sidebar:
        st.markdown("### 🏥 Medanta Admin")
        page = st.radio("", ["📊 Dashboard", "👥 Participants", "📝 Results", "❓ Questions", "📁 Import", "🚪 Logout"])
    
    if page == "🚪 Logout":
        st.session_state.admin_authenticated = False
        st.session_state.page = 'home'
        st.rerun()
    
    elif page == "📊 Dashboard":
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.title("Dashboard")
        
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
        
        st.markdown(f"""
            <div class="stat-grid">
                <div class="stat-box">
                    <div class="stat-value">{total}</div>
                    <div class="stat-label">Participants</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{completed}</div>
                    <div class="stat-label">Completed</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{avg_score:.0f}%</div>
                    <div class="stat-label">Avg Score</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{total_q}</div>
                    <div class="stat-label">Questions</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if completed > 0:
            chart_data = pd.DataFrame({
                'Status': ['Completed', 'Pending'],
                'Count': [completed, total - completed]
            })
            st.bar_chart(chart_data.set_index('Status'))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif page == "👥 Participants":
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.title("Participants")
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users ORDER BY created_at DESC")
        users = c.fetchall()
        conn.close()
        
        if users:
            df = pd.DataFrame([dict(row) for row in users])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button("⬇️ Export CSV", df.to_csv(index=False), "participants.csv", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif page == "📝 Results":
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.title("Results")
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
            st.download_button("⬇️ Export CSV", df.to_csv(index=False), "results.csv", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif page == "❓ Questions":
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.title("Question Bank")
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM questions")
        questions = c.fetchall()
        conn.close()
        
        st.info(f"Total questions: {len(questions)}")
        
        for q in questions:
            opts = json.loads(q['options'])
            with st.expander(f"{q['category']}: {q['question'][:40]}..."):
                for i, opt in enumerate(opts):
                    if i == q['correct_answer']:
                        st.success(f"**{chr(65+i)}.** {opt}")
                    else:
                        st.write(f"{chr(65+i)}. {opt}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif page == "📁 Import":
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.title("Import Questions")
        uploaded = st.file_uploader("Upload CSV", type="csv")
        
        if uploaded:
            df = pd.read_csv(uploaded)
            st.write("Preview:", df.head(3))
            
            if st.button("Import to Database", use_container_width=True, type="primary"):
                df.to_csv("questions.csv", index=False)
                if import_questions_from_csv():
                    st.success("✅ Imported!")
                    st.balloons()
                else:
                    st.error("❌ Failed")
        st.markdown('</div>', unsafe_allow_html=True)

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
