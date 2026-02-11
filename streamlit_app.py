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

# Page config - CENTERED to avoid wide layout issues
st.set_page_config(
    page_title="Medanta Induction",
    page_icon="🏥",
    layout="centered",  # Changed from wide to centered
    initial_sidebar_state="collapsed"
)

# CRITICAL: Remove top padding and white space
st.markdown("""
<style>
    /* Remove ALL default Streamlit spacing */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Hide all default elements */
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    
    /* Remove extra white space at top */
    .stApp {
        background: linear-gradient(135deg, #00695c 0%, #004d40 100%);
        margin-top: 0 !important;
    }
    
    /* Fix text colors for visibility */
    .big-title {
        color: #ffffff !important;
        text-align: center;
        font-size: 2.5em;
        font-weight: 700;
        margin: 10px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        color: #b2dfdb !important;
        text-align: center;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    
    /* Form labels - WHITE for visibility */
    .form-label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 0.9em;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Glass card with better contrast */
    .glass-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px 20px;
        margin: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(255,255,255,0.95) !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px !important;
        font-size: 16px !important;
    }
    
    /* Tab buttons - Medanta colors */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00897b, #00695c) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: rgba(255,255,255,0.2) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.5) !important;
        border-radius: 25px !important;
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .logo-img {
        max-width: 150px;
        height: auto;
        border-radius: 50%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
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
        st.error(f"Import error: {e}")
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

# Function to load and display logo
def show_logo():
    # Try to load local logo first, fallback to URL or emoji
    logo_path = "Medanta Lucknow Logo.jpg"
    
    try:
        if os.path.exists(logo_path):
            image = Image.open(logo_path)
            st.image(image, width=150, use_container_width=False)
        else:
            # Try GitHub raw URL
            github_logo_url = "https://raw.githubusercontent.com/pspallavisingh349-ai/medanta-induction/main/Medanta%20Lucknow%20Logo.jpg"
            response = requests.get(github_logo_url, timeout=5)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, width=150, use_container_width=False)
            else:
                st.markdown('<div style="font-size: 80px; text-align: center;">🏥</div>', unsafe_allow_html=True)
    except:
        st.markdown('<div style="font-size: 80px; text-align: center;">🏥</div>', unsafe_allow_html=True)

# ==================== HOME PAGE ====================
def show_home():
    # NO extra containers that create white space
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Logo
        show_logo()
        
        # Title - WHITE text for visibility
        st.markdown('<h1 class="big-title">Namaste 🙏</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Welcome to Medanta<br>Begin your journey with excellence in healthcare</p>', unsafe_allow_html=True)
        
        # Tabs
        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            if st.button("✨ New Joiner", use_container_width=True, 
                        type="primary" if st.session_state.active_tab == 'register' else "secondary"):
                st.session_state.active_tab = 'register'
                st.rerun()
        with tab_col2:
            if st.button("🔑 Returning", use_container_width=True,
                        type="primary" if st.session_state.active_tab == 'login' else "secondary"):
                st.session_state.active_tab = 'login'
                st.rerun()
        
        # Forms
        if st.session_state.active_tab == 'register':
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
                
                st.markdown('<p class="form-label">Employee ID</p>', unsafe_allow_html=True)
                employee_id = st.text_input("", placeholder="Optional", label_visibility="collapsed")
                
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
        else:
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
            
            # Quick ID login
            st.markdown("<hr style='margin: 20px 0; opacity: 0.3;'>", unsafe_allow_html=True)
            st.markdown('<p class="form-label" style="text-align: center;">Quick Access with ID</p>', unsafe_allow_html=True)
            
            id_col1, id_col2 = st.columns([3, 1])
            with id_col1:
                login_id = st.text_input("", placeholder="Participant ID", key="login_id", label_visibility="collapsed")
            with id_col2:
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
            <div style="text-align: center; margin-top: 20px;">
                <a href="?page=admin" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 13px;">
                    🔐 Admin Portal
                </a>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

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
    
    # Progress
    progress = (current / len(questions)) * 100
    
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.95); padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600; color: #37474f;">Question {current + 1} of {len(questions)}</span>
                <span style="background: #00897b; color: white; padding: 5px 15px; border-radius: 15px; font-size: 14px;">
                    ⏱️ {int((time.time() - st.session_state.start_time) // 60):02d}:{int((time.time() - st.session_state.start_time) % 60):02d}
                </span>
            </div>
            <div style="background: #e0f2f1; height: 8px; border-radius: 4px;">
                <div style="width: {progress}%; height: 100%; background: linear-gradient(90deg, #00897b, #00bfa5); border-radius: 4px; transition: 0.3s;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Question
    q = questions[current]
    options = json.loads(q['options'])
    
    st.markdown(f"""
        <div style="background: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="color: #00897b; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 10px;">{q['category']}</div>
            <div style="font-size: 18px; font-weight: 600; color: #263238; line-height: 1.5;">{q['question']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Options
    for i, opt in enumerate(options):
        cols = st.columns([1, 10])
        with cols[0]:
            st.markdown(f"""
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #00897b, #00bfa5); 
                            border-radius: 10px; display: flex; align-items: center; justify-content: center;
                            color: white; font-weight: 700; margin-top: 5px;">{chr(65+i)}</div>
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
        if st.button("Skip ⏭️", use_container_width=True):
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
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(f"""
            <div style="background: white; padding: 40px 30px; border-radius: 20px; text-align: center; margin-top: 20px;">
                <div style="font-size: 60px; margin-bottom: 10px;">{'🎉' if passed else '👏'}</div>
                <h2 style="color: {'#00897b' if passed else '#ff7043'}; margin: 0;">{'Excellent!' if passed else 'Good Effort!'}</h2>
                <p style="color: #78909c; margin: 10px 0 30px 0;">{'You passed!' if passed else 'Review & retry if needed'}</p>
                
                <div style="width: 150px; height: 150px; margin: 0 auto 30px auto; border-radius: 50%; 
                            background: {'linear-gradient(135deg, #00897b, #00bfa5)' if passed else 'linear-gradient(135deg, #ff7043, #f4511e)'};
                            display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                    <span style="color: white; font-size: 36px; font-weight: 800;">{result['score']:.0f}%</span>
                </div>
                
                <div style="display: flex; justify-content: space-around; margin-bottom: 30px;">
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: 700; color: #37474f;">{result['correct_answers']}</div>
                        <div style="font-size: 12px; color: #90a4ae;">Correct</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: 700; color: #37474f;">{result['total_questions']}</div>
                        <div style="font-size: 12px; color: #90a4ae;">Total</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 24px; font-weight: 700; color: #37474f;">{result['time_taken']//60}m</div>
                        <div style="font-size: 12px; color: #90a4ae;">Time</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 Back to Home", use_container_width=True, type="primary"):
            st.session_state.page = 'home'
            st.session_state.user_id = None
            st.session_state.user_name = None
            st.rerun()

# ==================== ADMIN PAGE ====================
def show_admin():
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <div style="background: rgba(255,255,255,0.95); padding: 40px; border-radius: 20px; text-align: center; margin-top: 60px;">
                    <div style="font-size: 50px; margin-bottom: 20px;">🔐</div>
                    <h2 style="color: #00897b; margin-bottom: 20px;">Admin Login</h2>
            """, unsafe_allow_html=True)
            
            pwd = st.text_input("", type="password", placeholder="Password", label_visibility="collapsed")
            
            if st.button("Login", use_container_width=True, type="primary"):
                if pwd == "medanta123":
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("Wrong password")
            
            st.markdown("</div>", unsafe_allow_html=True)
        return
    
    st.sidebar.title("🏥 Medanta Admin")
    page = st.sidebar.radio("Menu", ["📊 Dashboard", "👥 Participants", "📝 Results", "❓ Questions", "📁 Import CSV", "🚪 Logout"])
    
    if page == "🚪 Logout":
        st.session_state.admin_authenticated = False
        st.session_state.page = 'home'
        st.rerun()
    
    elif page == "📊 Dashboard":
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
        
        cols = st.columns(4)
        cols[0].metric("Total", total)
        cols[1].metric("Completed", completed)
        cols[2].metric("Avg Score", f"{avg_score:.1f}%")
        cols[3].metric("Questions", total_q)
        
        if completed > 0:
            st.bar_chart({"Completed": [completed], "Pending": [total - completed]})
    
    elif page == "👥 Participants":
        st.title("Participants")
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users ORDER BY created_at DESC")
        users = c.fetchall()
        conn.close()
        
        if users:
            df = pd.DataFrame([dict(row) for row in users])
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button("⬇️ Download CSV", df.to_csv(index=False), "participants.csv")
    
    elif page == "📝 Results":
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
            st.download_button("⬇️ Download CSV", df.to_csv(index=False), "results.csv")
    
    elif page == "❓ Questions":
        st.title(f"Questions ({len(st.session_state.questions) if st.session_state.questions else 'Loading...'})")
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM questions")
        questions = c.fetchall()
        conn.close()
        
        for q in questions[:10]:  # Show first 10 for performance
            opts = json.loads(q['options'])
            with st.expander(f"{q['category']}: {q['question'][:50]}..."):
                for i, opt in enumerate(opts):
                    if i == q['correct_answer']:
                        st.success(f"**{chr(65+i)}. {opt}** ✅")
                    else:
                        st.write(f"{chr(65+i)}. {opt}")
    
    elif page == "📁 Import CSV":
        st.title("Import Questions")
        uploaded = st.file_uploader("Upload CSV (175 questions)", type="csv")
        
        if uploaded:
            df = pd.read_csv(uploaded)
            st.write(f"Preview ({len(df)} questions):", df.head())
            
            if st.button("Import to Database", use_container_width=True, type="primary"):
                df.to_csv("questions.csv", index=False)
                if import_questions_from_csv():
                    st.success(f"✅ Imported {len(df)} questions!")
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
