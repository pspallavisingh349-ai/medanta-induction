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

# Custom CSS - EXACT match to your HTML
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;500;600;700&display=swap');
    
    /* Remove default Streamlit padding */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Hide Streamlit header */
    header {
        visibility: hidden;
    }
    
    /* Hide Streamlit footer */
    footer {
        visibility: hidden;
    }
    
    /* Main background - gradient like your HTML */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Remove default background */
    .main {
        background: transparent !important;
    }
    
    /* Container - white box with shadow */
    .main-container {
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        overflow: hidden;
        max-width: 1000px;
        margin: 40px auto;
    }
    
    /* Left panel - red gradient */
    .left-panel {
        background: linear-gradient(135deg, #e53935 0%, #c62828 100%);
        padding: 40px;
        color: white;
        text-align: center;
        min-height: 600px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .logo-circle {
        width: 120px;
        height: 120px;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .welcome-title {
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 15px;
        color: white;
    }
    
    .welcome-text {
        font-size: 1.1em;
        opacity: 0.9;
        line-height: 1.6;
        color: white;
    }
    
    /* Right panel - white background */
    .right-panel {
        padding: 40px;
        background: white;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 2px solid #eee;
        margin-bottom: 30px;
    }
    
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        padding: 15px;
        text-align: center;
        font-weight: 600;
        color: #666;
        background: transparent;
        border: none;
        font-size: 16px;
    }
    
    .stTabs [aria-selected="true"] {
        color: #e53935 !important;
        border-bottom: 3px solid #e53935 !important;
        background: transparent !important;
    }
    
    /* Form inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        width: 100%;
        padding: 12px 15px;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        font-size: 16px;
        background: white;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #e53935;
        box-shadow: 0 0 0 2px rgba(229, 57, 53, 0.2);
        outline: none;
    }
    
    /* Labels */
    .stTextInput label,
    .stSelectbox label {
        color: #333;
        font-weight: 500;
        margin-bottom: 8px;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        padding: 15px;
        background: linear-gradient(135deg, #e53935 0%, #c62828 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        cursor: pointer;
        transition: transform 0.3s, box-shadow 0.3s;
        margin-top: 10px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(229, 57, 53, 0.3);
    }
    
    .stButton > button:disabled {
        background: #ccc !important;
        cursor: not-allowed;
        transform: none;
    }
    
    /* Admin link */
    .admin-link {
        text-align: center;
        margin-top: 20px;
    }
    
    .admin-link a {
        color: #e53935;
        text-decoration: none;
        font-weight: 500;
    }
    
    /* Form container spacing */
    .element-container {
        margin-bottom: 0 !important;
    }
    
    /* Reduce gap between form elements */
    .row-widget.stTextInput,
    .row-widget.stSelectbox {
        margin-bottom: 20px !important;
    }
    
    /* Assessment styling */
    .question-card {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    
    .timer {
        font-size: 24px;
        font-weight: bold;
        background: rgba(229, 57, 53, 0.1);
        color: #e53935;
        padding: 10px 20px;
        border-radius: 10px;
        text-align: center;
    }
    
    .progress-bar {
        height: 10px;
        background: #e0e0e0;
        border-radius: 5px;
        margin-bottom: 30px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #e53935, #ff6b6b);
        transition: width 0.5s;
    }
    
    .result-card {
        background: white;
        border-radius: 20px;
        padding: 60px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    /* Sidebar for admin */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    div[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Remove extra padding */
    .css-1d391kg {
        padding: 0 !important;
    }
    
    /* Center content */
    .css-1y4p8pa {
        max-width: 100% !important;
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Database path
DB_PATH = "medanta.db"

def init_db():
    """Initialize database"""
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
    """Import questions from questions.csv if exists"""
    csv_path = "questions.csv"
    
    if not os.path.exists(csv_path):
        return False
    
    try:
        df = pd.read_csv(csv_path)
        
        required_cols = ['Question', 'Option A', 'Option B', 'Option C', 'Option D', 'Answer']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            return False
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM questions")
        
        imported = 0
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
            imported += 1
        
        conn.commit()
        conn.close()
        return imported > 0
        
    except Exception as e:
        return False

def add_sample_questions():
    """Add sample questions if none exist"""
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
            ("What is the standard hand hygiene protocol?", 
             json.dumps(["Water only", "Soap and water", "Sanitizer only", "Soap and water or sanitizer"]), 
             3, "Clinical", 1),
            ("Who is the founder of Medanta?", 
             json.dumps(["Dr. Naresh Trehan", "Dr. Devi Shetty", "Dr. Prathap Reddy", "Dr. Ashok Seth"]), 
             0, "HR", 1),
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

# Try to import CSV questions on startup
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

# ==================== HOME PAGE (REGISTRATION) ====================
def show_home():
    # Create two columns with exact same ratio as HTML
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Left panel with red gradient
        st.markdown("""
        <div style="background: linear-gradient(135deg, #e53935 0%, #c62828 100%); 
                    padding: 40px; color: white; text-align: center; 
                    min-height: 600px; display: flex; flex-direction: column; 
                    justify-content: center; align-items: center; border-radius: 0;">
            <div style="width: 120px; height: 120px; background: white; 
                        border-radius: 50%; display: flex; align-items: center; 
                        justify-content: center; margin-bottom: 30px; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
                <h1 style="color: #e53935; font-size: 60px; margin: 0;">🏥</h1>
            </div>
            <h1 style="font-size: 2.5em; font-weight: bold; margin-bottom: 15px; color: white;">
                Welcome to Medanta
            </h1>
            <p style="font-size: 1.1em; opacity: 0.9; line-height: 1.6; color: white;">
                Begin your journey with us. Complete your induction to become part 
                of our family dedicated to delivering exceptional healthcare.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Right panel with white background
        st.markdown("""
        <div style="background: white; padding: 40px; min-height: 600px;">
        """, unsafe_allow_html=True)
        
        # Tabs
        tab1, tab2 = st.tabs(["New Registration", "Continue Assessment"])
        
        with tab1:
            st.markdown("<h3 style='color: #333; margin-bottom: 20px;'>New Registration</h3>", unsafe_allow_html=True)
            
            with st.form("registration_form", clear_on_submit=False):
                name = st.text_input("Full Name *", placeholder="Enter your full name")
                email = st.text_input("Email Address *", placeholder="your.email@medanta.org")
                department = st.selectbox("Department *", 
                    ["", "Nursing", "Medical", "Administration", "HR", "Finance", "IT", "Operations"])
                role = st.text_input("Designation *", placeholder="e.g., Staff Nurse, Doctor, Manager")
                employee_id = st.text_input("Employee ID", placeholder="If available")
                
                submitted = st.form_submit_button("Register & Start Assessment")
                
                if submitted:
                    if not name or not email or not department or not role:
                        st.error("Please fill all required fields")
                    else:
                        conn = get_db()
                        c = conn.cursor()
                        c.execute("SELECT id FROM users WHERE email = ?", (email,))
                        if c.fetchone():
                            st.error("Email already registered. Use 'Continue Assessment' tab.")
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
            st.markdown("<h3 style='color: #333; margin-bottom: 20px;'>Continue Assessment</h3>", unsafe_allow_html=True)
            
            login_email = st.text_input("Email Address", key="login_email", placeholder="Enter your registered email")
            
            if st.button("Continue My Assessment"):
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
                    st.error("Email not found. Please register first.")
                conn.close()
            
            st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
            st.markdown("<p style='color: #666; text-align: center;'>Or enter your Participant ID:</p>", unsafe_allow_html=True)
            login_id = st.text_input("Participant ID", key="login_id")
            
            if st.button("Continue with ID"):
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
                            st.error("ID not found")
                    except:
                        st.error("Invalid ID")
        
        # Admin link
        st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <a href="?page=admin" style="color: #e53935; text-decoration: none; font-weight: 500;">
                🔐 Administrator Portal
            </a>
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
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"<h3>Welcome, {st.session_state.user_name}!</h3>", unsafe_allow_html=True)
    with col2:
        elapsed = int(time.time() - st.session_state.start_time)
        mins = elapsed // 60
        secs = elapsed % 60
        st.markdown(f"""
            <div style="font-size: 24px; font-weight: bold; background: rgba(229, 57, 53, 0.1); 
                        color: #e53935; padding: 10px 20px; border-radius: 10px; text-align: center;">
                {mins:02d}:{secs:02d}
            </div>
        """, unsafe_allow_html=True)
    
    # Progress bar
    progress = (current + 1) / len(questions) * 100
    st.markdown(f"""
        <div style="height: 10px; background: #e0e0e0; border-radius: 5px; margin-bottom: 10px; overflow: hidden;">
            <div style="height: 100%; width: {progress}%; background: linear-gradient(90deg, #e53935, #ff6b6b);"></div>
        </div>
        <p style="text-align: center; color: #e53935; font-weight: 600; margin-bottom: 30px;">
            Question {current + 1} of {len(questions)}
        </p>
    """, unsafe_allow_html=True)
    
    # Question card
    q = questions[current]
    st.markdown(f"""
        <div style="background: white; border-radius: 20px; padding: 40px; 
                    box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin-bottom: 30px;">
            <h3 style="margin-bottom: 30px; color: #333;">{q['question']}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Options
    options = json.loads(q['options'])
    for i, opt in enumerate(options):
        if st.button(f"{chr(65+i)}. {opt}", key=f"opt_{i}", use_container_width=True):
            st.session_state.answers.append(i)
            st.session_state.current_question += 1
            st.rerun()
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if current > 0:
            if st.button("← Previous"):
                st.session_state.current_question -= 1
                st.session_state.answers.pop()
                st.rerun()
    with col3:
        if st.button("Skip →"):
            st.session_state.answers.append(-1)
            st.session_state.current_question += 1
            st.rerun()

def submit_assessment():
    questions = st.session_state.questions
    answers = st.session_state.answers
    time_taken = int(time.time() - st.session_state.start_time)
    
    correct = 0
    for i, ans in enumerate(answers):
        if i < len(questions) and ans == questions[i]['correct_answer']:
            correct += 1
    
    total = len(questions)
    score = (correct / total * 100) if total > 0 else 0
    
    conn = get_db()
    c = conn.cursor()
    c.execute("""INSERT INTO assessments (user_id, title, score, total_questions, correct_answers, status, time_taken, completed_at, answers)
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
    
    st.markdown(f"""
        <div style="background: white; border-radius: 20px; padding: 60px; 
                    text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
            <div style="font-size: 80px; margin-bottom: 20px;">{'🎉' if passed else '📋'}</div>
            <h1 style="font-size: 32px; margin-bottom: 20px; color: #333;">
                {'Congratulations!' if passed else 'Assessment Completed'}
            </h1>
            <div style="font-size: 48px; font-weight: bold; color: #e53935; margin-bottom: 10px;">
                {result['score']:.0f}%
            </div>
            <p style="font-size: 18px; color: #666; margin-bottom: 10px;">
                {result['correct_answers']} out of {result['total_questions']} correct
            </p>
            <p style="font-size: 18px; color: #666; margin-bottom: 30px;">
                {'You have successfully passed!' if passed else 'Thank you for completing.'}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Back to Home", use_container_width=True):
        st.session_state.page = 'home'
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.rerun()

# ==================== ADMIN PAGE ====================
def show_admin():
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        st.markdown("<h3>🔐 Administrator Login</h3>", unsafe_allow_html=True)
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if password == "medanta123":
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password")
        return
    
    st.sidebar.title("🏥 Admin Portal")
    admin_page = st.sidebar.radio("Navigation", ["Dashboard", "Participants", "Results", "Questions", "Import CSV", "Logout"])
    
    if admin_page == "Logout":
        st.session_state.admin_authenticated = False
        st.session_state.page = 'home'
        st.rerun()
    
    elif admin_page == "Dashboard":
        st.title("📊 Dashboard")
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
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Participants", total)
        col2.metric("Completed", completed)
        col3.metric("Average Score", f"{avg_score:.1f}%")
        col4.metric("Total Questions", total_q)
    
    elif admin_page == "Participants":
        st.title("👥 Participants")
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users ORDER BY created_at DESC")
        users = c.fetchall()
        conn.close()
        
        if users:
            df = pd.DataFrame([dict(row) for row in users])
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "participants.csv", "text/csv")
    
    elif admin_page == "Results":
        st.title("📝 Results")
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
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "results.csv", "text/csv")
    
    elif admin_page == "Questions":
        st.title("❓ Questions")
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT * FROM questions")
        questions = c.fetchall()
        conn.close()
        
        st.info(f"Total questions: {len(questions)}")
        
        for q in questions:
            with st.expander(f"{q['category']}: {q['question'][:60]}..."):
                opts = json.loads(q['options'])
                for i, opt in enumerate(opts):
                    if i == q['correct_answer']:
                        st.success(f"**{chr(65+i)}. {opt}** ✓")
                    else:
                        st.write(f"{chr(65+i)}. {opt}")
    
    elif admin_page == "Import CSV":
        st.title("📁 Import Questions from CSV")
        uploaded_file = st.file_uploader("Choose CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.write("Preview:", df.head())
                
                if st.button("Import to Database"):
                    df.to_csv("questions.csv", index=False)
                    imported = import_questions_from_csv()
                    
                    if imported:
                        st.success("✅ Questions imported!")
                        st.balloons()
                    else:
                        st.error("❌ Failed to import")
            except Exception as e:
                st.error(f"Error: {e}")

# ==================== MAIN ROUTING ====================
def main():
    query_params = st.query_params
    if query_params.get("page") == "admin":
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
