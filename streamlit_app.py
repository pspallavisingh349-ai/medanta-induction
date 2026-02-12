import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import base64
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Medanta Induction Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Create data folder
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Function to load logo
def get_logo_src():
    try:
        logo_files = ["Medanta Lucknow Logo.jpg", "medanta_logo.png", "logo.png"]
        for logo_file in logo_files:
            if os.path.exists(logo_file):
                with open(logo_file, "rb") as f:
                    return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
        return None
    except:
        return None

# Load questions from EXCEL
def load_questions():
    try:
        df = pd.read_excel("Question_bank.xlsx")
        df = df[df['Active'] == 'YES']
        
        assessments = {}
        for assessment_id in df['Assessment_ID'].unique():
            assessment_df = df[df['Assessment_ID'] == assessment_id]
            questions = []
            for _, row in assessment_df.iterrows():
                opts = []
                for opt in ['Option_A', 'Option_B', 'Option_C', 'Option_D']:
                    if pd.notna(row.get(opt)) and str(row.get(opt)).strip():
                        opts.append(str(row[opt]))
                
                correct_val = str(row.get('Correct_Option', 'A')).strip()
                correct_letter = correct_val[0].upper() if correct_val else 'A'
                correct_idx = ord(correct_letter) - ord('A')
                correct_idx = max(0, min(3, correct_idx))
                
                questions.append({
                    "id": str(row['Question_ID']),
                    "question": str(row['Question_Text']),
                    "options": opts,
                    "correct": correct_idx
                })
            
            assessments[str(assessment_id)] = {
                "name": str(assessment_df['Assessment_Name'].iloc[0]),
                "questions": questions
            }
        return assessments
    except Exception as e:
        st.error(f"Error loading questions: {str(e)}")
        return {}

# Get logo source
logo_src = get_logo_src()

# WHITE & GOLD THEME WITH MAROON/GREY TEXT
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --medanta-maroon: #800020;
    --medanta-gold: #D4AF37;
    --medanta-gold-light: #F4E8C1;
    --medanta-cream: #FAF8F3;
    --medanta-grey: #666666;
    --medanta-grey-light: #999999;
}

* {
    font-family: 'Inter', sans-serif;
}

/* Main white background with gold accents */
.stApp {
    background: linear-gradient(135deg, #FFFFFF 0%, #FAF8F3 50%, #F4E8C1 100%);
    color: #666666;
    min-height: 100vh;
}

/* Hide Streamlit elements */
#MainMenu, footer, header, .stDeployButton {display: none;}

/* Glassmorphism cards - white with gold border */
.glass-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border: 2px solid #D4AF37;
    border-radius: 24px;
    padding: 40px;
    margin: 20px 0;
    box-shadow: 0 10px 40px rgba(128, 0, 32, 0.1);
    transition: all 0.3s ease;
}

.glass-card:hover {
    border-color: #800020;
    transform: translateY(-5px);
    box-shadow: 0 20px 60px rgba(128, 0, 32, 0.15);
}

/* Maroon headings */
h1, h2, h3 {
    color: #800020 !important;
    font-family: 'Playfair Display', serif;
}

/* Gold accent text */
.gold-text {
    color: #D4AF37 !important;
    font-weight: 600;
}

/* Maroon buttons */
.maroon-btn {
    background: linear-gradient(135deg, #800020 0%, #A00030 100%);
    color: white;
    border: none;
    padding: 16px 32px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(128, 0, 32, 0.3);
    width: 100%;
}

.maroon-btn:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 15px 40px rgba(128, 0, 32, 0.4);
}

/* Gold buttons */
.gold-btn {
    background: linear-gradient(135deg, #D4AF37 0%, #B8941F 100%);
    color: #800020;
    border: none;
    padding: 16px 32px;
    border-radius: 50px;
    font-weight: 700;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3);
    width: 100%;
}

.gold-btn:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 15px 40px rgba(212, 175, 55, 0.4);
}

/* Outline button - maroon border */
.outline-btn {
    background: transparent;
    color: #800020;
    border: 2px solid #800020;
    padding: 16px 32px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
}

.outline-btn:hover {
    background: rgba(128, 0, 32, 0.05);
    border-color: #D4AF37;
    color: #D4AF37;
}

/* Logo styling */
.logo-container {
    text-align: center;
    margin-bottom: 30px;
}

.logo-img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: white;
    padding: 10px;
    box-shadow: 0 20px 60px rgba(128, 0, 32, 0.2);
    border: 4px solid #D4AF37;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); box-shadow: 0 20px 60px rgba(128, 0, 32, 0.2); }
    50% { transform: scale(1.05); box-shadow: 0 30px 80px rgba(128, 0, 32, 0.3); }
}

/* 3D Seal - Gold with maroon text */
.seal-3d {
    width: 200px;
    height: 200px;
    margin: 0 auto;
    background: linear-gradient(135deg, #F4E8C1 0%, #D4AF37 50%, #B8941F 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 6px solid #800020;
    box-shadow: 0 20px 60px rgba(212, 175, 55, 0.4), inset 0 -10px 30px rgba(0,0,0,0.1);
    animation: rotate-seal 10s linear infinite;
}

@keyframes rotate-seal {
    0% { transform: rotateY(0deg); }
    100% { transform: rotateY(360deg); }
}

/* Progress bar - gold to maroon */
.progress-container {
    background: rgba(212, 175, 55, 0.2);
    border-radius: 20px;
    overflow: hidden;
    height: 12px;
}

.progress-bar {
    background: linear-gradient(90deg, #D4AF37, #800020);
    height: 100%;
    border-radius: 20px;
    transition: width 0.5s ease;
}

/* Question cards - white with gold left border */
.question-card {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #E5E5E5;
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
    border-left: 4px solid #D4AF37;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}

.question-card:hover {
    border-left-color: #800020;
    transform: translateX(10px);
    box-shadow: 0 8px 25px rgba(128, 0, 32, 0.1);
}

/* Radio buttons styling */
div[role="radiogroup"] > label {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid #E5E5E5;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 12px;
    color: #666666;
}

div[role="radiogroup"] > label:hover {
    background: rgba(212, 175, 55, 0.1);
    border-color: #D4AF37;
    transform: translateX(5px);
}

/* Stats cards - white with gold border */
.stat-card {
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid #D4AF37;
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    border-color: #800020;
    box-shadow: 0 15px 40px rgba(128, 0, 32, 0.1);
}

/* Typography */
p, span, div {
    color: #666666;
}

/* Success/Error messages */
.success-msg {
    background: rgba(212, 175, 55, 0.15);
    border: 1px solid #D4AF37;
    border-radius: 12px;
    padding: 20px;
    color: #800020;
}

.error-msg {
    background: rgba(128, 0, 32, 0.1);
    border: 1px solid #800020;
    border-radius: 12px;
    padding: 20px;
    color: #800020;
}

/* Custom scrollbar - gold */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #FAF8F3;
}
::-webkit-scrollbar-thumb {
    background: #D4AF37;
    border-radius: 4px;
}

/* Floating animation */
.floating {
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255, 255, 255, 0.8);
    padding: 10px;
    border-radius: 16px;
    border: 1px solid #D4AF37;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 12px;
    padding: 12px 24px;
    color: #666666;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #800020 0%, #A00030 100%) !important;
    color: white !important;
}

/* Input fields */
input, textarea, select {
    background: white !important;
    border: 1px solid #D4AF37 !important;
    border-radius: 12px !important;
    color: #666666 !important;
}

input:focus, textarea:focus, select:focus {
    border-color: #800020 !important;
    box-shadow: 0 0 0 3px rgba(128, 0, 32, 0.1) !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.95);
    border: 2px solid #D4AF37;
    border-radius: 16px;
    padding: 20px;
}

[data-testid="stMetric"] label {
    color: #800020 !important;
    font-weight: 600;
}

[data-testid="stMetric"] div {
    color: #D4AF37 !important;
    font-size: 2rem;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'admin' not in st.session_state:
    st.session_state.admin = None
if 'current_module_idx' not in st.session_state:
    st.session_state.current_module_idx = 0
if 'current_question_idx' not in st.session_state:
    st.session_state.current_question_idx = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'module_scores' not in st.session_state:
    st.session_state.module_scores = {}

DATA_FILE = DATA_DIR / "employees.json"

ADMIN_USERS = {
    "pallavi.singh@medanta.org": "Pallavi@2024",
    "rohit.singh@medanta.org": "Rohit@2024"
}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Load questions
questions_data = load_questions()

# LANDING PAGE - White & Gold theme
if st.session_state.page == 'landing':
    # Reset question index when coming to landing
    st.session_state.current_question_idx = 0
    st.session_state.answers = {}
    
    # Background effects - subtle gold
    st.markdown("""
    <div style="position: fixed; top: 10%; right: 5%; width: 300px; height: 300px; 
         background: radial-gradient(circle, rgba(212,175,55,0.15) 0%, transparent 70%); 
         border-radius: 50%; pointer-events: none; z-index: 0;"></div>
    <div style="position: fixed; bottom: 10%; left: 5%; width: 400px; height: 400px; 
         background: radial-gradient(circle, rgba(128,0,32,0.08) 0%, transparent 70%); 
         border-radius: 50%; pointer-events: none; z-index: 0;"></div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        if logo_src:
            st.markdown(f'<img src="{logo_src}" class="logo-img" alt="Medanta Logo">', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size: 80px; text-align: center;">🏥</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<h1 style="text-align: center; font-size: 3.5rem; margin-bottom: 10px; color: #800020; font-family: Playfair Display, serif;">Welcome to Medanta</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #D4AF37; font-size: 1.3rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 40px; font-weight: 600;">The Medicity</p>', unsafe_allow_html=True)
        
        # 3D Seal
        st.markdown("""
        <div style="text-align: center; margin: 40px 0;">
            <div class="seal-3d">
                <div style="text-align: center; color: #800020;">
                    <div style="font-size: 11px; letter-spacing: 2px; font-weight: 700; color: #800020;">JCI ACCREDITED</div>
                    <div style="font-size: 48px; font-weight: bold; margin: 5px 0; color: #800020;">GOLD</div>
                    <div style="font-size: 10px; letter-spacing: 2px; color: #800020;">SEAL OF APPROVAL</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats
        cols = st.columns(4)
        stats = [("25+", "Years"), ("2M+", "Patients"), ("JCI", "Gold"), ("5000+", "Healers")]
        for col, (num, label) in zip(cols, stats):
            with col:
                st.markdown(f"""
                <div class="stat-card">
                    <div style="font-size: 2rem; font-weight: 700; color: #800020;">{num}</div>
                    <div style="font-size: 0.9rem; color: #666666;">{label}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # CTA Buttons - Maroon and Gold
        if st.button("🚀 Begin Your Journey", key="start_btn"):
            st.session_state.page = 'employee_login'
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔐 Admin Portal", key="admin_btn"):
            st.session_state.page = 'admin_login'
            st.rerun()
        
        st.markdown("""
        <p style="text-align: center; color: #800020; margin-top: 30px; font-style: italic; font-family: Playfair Display, serif; font-size: 1.2rem;">
            "Where Healing Meets Innovation"
        </p>
        """, unsafe_allow_html=True)

# EMPLOYEE LOGIN - White & Gold theme
elif st.session_state.page == 'employee_login':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="margin-top: 50px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <div style="font-size: 4rem; margin-bottom: 15px; animation: float 3s ease-in-out infinite;">🙏</div>
                <h2 style="font-family: Playfair Display, serif; font-size: 2.5rem; margin-bottom: 10px; color: #800020;">Join the Medanta Family</h2>
                <p style="color: #666666;">Your personalized induction journey awaits</p>
            </div>
        """, unsafe_allow_html=True)
        
        # New Joinee
        with st.form("employee_reg"):
            st.markdown('<p style="color: #800020; font-weight: 600; margin-bottom: 15px; font-size: 1.1rem;">🆕 New Joinee</p>', unsafe_allow_html=True)
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            email = st.text_input("Email Address *", placeholder="your.email@medanta.org")
            
            col_cat, col_dept = st.columns(2)
            with col_cat:
                category = st.selectbox("Category *", ["Select", "Clinical", "Administration", "Nursing", "Paramedical"])
            with col_dept:
                department = st.text_input("Department *", placeholder="e.g., Cardiology")
            
            mobile = st.text_input("Mobile Number *", placeholder="+91 XXXXX XXXXX")
            emp_id = st.text_input("Employee ID (if available)", placeholder="Optional")
            
            submitted = st.form_submit_button("✨ Create My Portal")
            
            if submitted:
                if not all([name, email, department, mobile]) or category == "Select":
                    st.error("Please fill all required fields!")
                else:
                    data = load_data()
                    existing = [e for e in data if e['email'] == email]
                    
                    if existing:
                        st.error("Email already registered! Use 'Returning User' option.")
                    else:
                        new_user = {
                            "id": len(data) + 1,
                            "name": name,
                            "email": email,
                            "category": category,
                            "department": department,
                            "mobile": mobile,
                            "emp_id": emp_id if emp_id else "Pending",
                            "registered_at": datetime.now().isoformat(),
                            "assessment_score": None,
                            "assessment_passed": False,
                            "attempts": 0,
                            "handbook_viewed": False,
                            "current_module": 0
                        }
                        data.append(new_user)
                        save_data(data)
                        st.session_state.user = new_user
                        st.session_state.page = 'employee_dashboard'
                        st.rerun()
        
        # Returning User
        st.markdown("<hr style='border-color: #D4AF37; margin: 30px 0;'>", unsafe_allow_html=True)
        st.markdown('<p style="color: #D4AF37; font-weight: 600; margin-bottom: 15px; font-size: 1.1rem;">🔙 Returning User</p>', unsafe_allow_html=True)
        
        with st.form("employee_login_form"):
            login_email = st.text_input("Email Address", placeholder="your.email@medanta.org", key="login_email")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("← Back"):
                    st.session_state.page = 'landing'
                    st.rerun()
            with col2:
                if st.form_submit_button("Login"):
                    if login_email:
                        data = load_data()
                        user = [e for e in data if e['email'] == login_email]
                        if user:
                            st.session_state.user = user[0]
                            st.success(f"Welcome back, {user[0]['name']}!")
                            st.session_state.page = 'employee_dashboard'
                            st.rerun()
                        else:
                            st.error("Email not found! Please register first.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# EMPLOYEE DASHBOARD - White & Gold theme
elif st.session_state.page == 'employee_dashboard':
    user = st.session_state.user
    
    # Reset question index when coming to dashboard
    st.session_state.current_question_idx = 0
    st.session_state.answers = {}
    
    # Fix: Check if keys exist
    user_dept = user.get('department', 'N/A')
    user_cat = user.get('category', 'N/A')
    user_name = user.get('name', 'User')
    
    st.markdown(f"""
    <div style="text-align: center; padding: 30px 0;">
        <div style="font-size: 3.5rem; margin-bottom: 15px; animation: pulse 2s infinite; display: inline-block;">🙏</div>
        <h1 style="font-family: Playfair Display, serif; font-size: 3rem; margin-bottom: 10px; color: #800020;">
            Namaste, {user_name}
        </h1>
        <p style="color: #666666; font-size: 1.1rem;">{user_dept} | {user_cat}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress
    progress = 0
    if user.get('handbook_viewed'): progress += 33
    if user.get('assessment_passed'): progress += 33
    if user.get('departmental_induction'): progress += 34
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 25px; margin-bottom: 30px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <span style="color: #800020; font-weight: 600;">Your Progress</span>
            <span style="color: #D4AF37; font-weight: 700;">{progress}%</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Modules
    st.markdown('<h2 style="margin-bottom: 20px; color: #800020;">🎯 Learning Modules</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card" style="padding: 25px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 2.5rem; margin-bottom: 15px;">📚</div>', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 10px; color: #800020;">Employee Handbook</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666666; margin-bottom: 20px;">Learn about Medanta\'s policies and culture</p>', unsafe_allow_html=True)
        if st.button("Open Handbook", key="handbook"):
            data = load_data()
            for u in data:
                if u['email'] == user.get('email'):
                    u['handbook_viewed'] = True
                    st.session_state.user = u
                    break
            save_data(data)
            st.session_state.page = 'handbook'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card" style="padding: 25px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 2.5rem; margin-bottom: 15px;">📝</div>', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 10px; color: #800020;">Assessments</h3>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #666666; margin-bottom: 20px;">{len(questions_data)} modules • 80% to pass</p>', unsafe_allow_html=True)
        if st.button("Start Assessment", key="assessment"):
            st.session_state.current_module_idx = user.get('current_module', 0)
            st.session_state.current_question_idx = 0
            st.session_state.answers = {}
            st.session_state.page = 'assessment'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card" style="padding: 25px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 2.5rem; margin-bottom: 15px;">🏅</div>', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 10px; color: #800020;">JCI Handbook</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #666666; margin-bottom: 20px;">International Patient Safety Goals</p>', unsafe_allow_html=True)
        if st.button("Open JCI Guide", key="jci"):
            st.session_state.page = 'jci_handbook'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card" style="padding: 25px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 2.5rem; margin-bottom: 15px;">🎓</div>', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 10px; color: #800020;">Report Card</h3>', unsafe_allow_html=True)
        if user.get('assessment_passed'):
            st.markdown('<p style="color: #D4AF37; margin-bottom: 20px; font-weight: 600;">✅ Certification Complete!</p>', unsafe_allow_html=True)
            if st.button("View Certificate", key="cert"):
                st.session_state.page = 'report_card'
                st.rerun()
        else:
            st.markdown('<p style="color: #666666; margin-bottom: 20px;">⏳ Complete assessment first</p>', unsafe_allow_html=True)
            st.button("View Certificate", disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.user = None
        st.session_state.page = 'landing'
        st.rerun()

# HANDBOOK
elif st.session_state.page == 'handbook':
    st.markdown('<h2 style="margin-bottom: 20px; color: #800020;">📚 Employee Handbook</h2>', unsafe_allow_html=True)
    st.components.v1.iframe("https://online.flippingbook.com/view/652486186/", height=700)
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# JCI HANDBOOK
elif st.session_state.page == 'jci_handbook':
    st.markdown('<h2 style="margin-bottom: 20px; color: #800020;">🏅 JCI Accreditation Standards</h2>', unsafe_allow_html=True)
    st.components.v1.iframe("https://online.flippingbook.com/view/389334287/", height=700)
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# ASSESSMENT - FIXED VERSION (One question at a time with navigation)
elif st.session_state.page == 'assessment':
    user = st.session_state.user
    
    if not questions_data:
        st.error("⚠️ Could not load questions. Please check Question_bank.xlsx file.")
        if st.button("← Back"):
            st.session_state.page = 'employee_dashboard'
            st.rerun()
        st.stop()
    
    module_ids = list(questions_data.keys())
    current_idx = st.session_state.current_module_idx
    
    if current_idx >= len(module_ids):
        st.balloons()
        st.success("🎉 Congratulations! You have completed all assessments!")
        
        data = load_data()
        for u in data:
            if u['email'] == user.get('email'):
                u['assessment_passed'] = True
                break
        save_data(data)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("View Report Card"):
                st.session_state.page = 'report_card'
                st.rerun()
        with col2:
            if st.button("← Back to Dashboard"):
                st.session_state.page = 'employee_dashboard'
                st.rerun()
        st.stop()
    
    current_module = questions_data[module_ids[current_idx]]
    questions = current_module['questions']
    total_questions = len(questions)
    
    # Safety check
    if st.session_state.current_question_idx >= total_questions:
        st.session_state.current_question_idx = 0
    
    current_q_idx = st.session_state.current_question_idx
    current_q = questions[current_q_idx]
    
    # Header
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <h2 style="color: #800020; margin-bottom: 5px;">{current_module['name']}</h2>
        <p style="color: #666666;">Module {current_idx + 1} of {len(module_ids)} • Question {current_q_idx + 1} of {total_questions}</p>
        <div class="progress-container" style="margin-top: 10px;">
            <div class="progress-bar" style="width: {((current_q_idx + 1) / total_questions) * 100}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Question boxes - ALL of them in rows of 10
    st.markdown("<p style='color: #800020; font-weight: 600; margin-bottom: 10px;'>Questions:</p>", unsafe_allow_html=True)
    
    # Calculate rows needed
    questions_per_row = 10
    num_rows = (total_questions + questions_per_row - 1) // questions_per_row
    
    for row in range(num_rows):
        start = row * questions_per_row
        end = min(start + questions_per_row, total_questions)
        cols = st.columns(end - start)
        
        for i in range(start, end):
            with cols[i - start]:
                # Style based on state
                if i == current_q_idx:
                    btn_type = "primary"  # Maroon
                    label = f"Q{i+1}"
                elif i in st.session_state.answers:
                    btn_type = "secondary"  # Will be gold via CSS
                    label = f"✓{i+1}"
                else:
                    btn_type = "secondary"  # White
                    label = f"{i+1}"
                
                if st.button(label, key=f"nav_{current_idx}_{i}", use_container_width=True, type=btn_type):
                    st.session_state.current_question_idx = i
                    st.rerun()
    
    # Question display
    st.markdown(f"""
    <div style="background: white; border: 3px solid #D4AF37; border-radius: 20px; padding: 35px; margin: 25px 0; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
        <h3 style="color: #800020; font-size: 1.5rem; margin-bottom: 25px; line-height: 1.6; font-weight: 600;">
            {current_q.get('question', 'Question not available')}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer options
    options = current_q.get('options', [])
    current_answer = st.session_state.answers.get(current_q_idx)
    
    try:
        current_index = options.index(current_answer) if current_answer in options else None
    except:
        current_index = None
    
    selected = st.radio(
        "Select your answer:",
        options,
        index=current_index,
        key=f"ans_{current_idx}_{current_q_idx}"
    )
    
    # Save answer
    if selected:
        st.session_state.answers[current_q_idx] = selected
    
    # Navigation buttons
    st.markdown("<hr style='border-color: #D4AF37; margin: 30px 0;'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Previous", disabled=(current_q_idx == 0), use_container_width=True):
            st.session_state.current_question_idx = max(0, current_q_idx - 1)
            st.rerun()
    
    with col2:
        # Show submit only when all answered
        if len(st.session_state.answers) == total_questions:
            if st.button("✅ Submit Module", type="primary", use_container_width=True):
                # Calculate score
                correct = 0
                for i in range(total_questions):
                    if i < len(questions):
                        q = questions[i]
                        correct_idx = q.get('correct', 0)
                        opts = q.get('options', [])
                        if i in st.session_state.answers and st.session_state.answers[i] == opts[correct_idx]:
                            correct += 1
                
                score = (correct / total_questions) * 100 if total_questions > 0 else 0
                
                # Save
                data = load_data()
                for u in data:
                    if u['email'] == user.get('email'):
                        u['attempts'] = u.get('attempts', 0) + 1
                        if score >= 80:
                            u['current_module'] = current_idx + 1
                            if current_idx + 1 >= len(module_ids):
                                u['assessment_passed'] = True
                                u['assessment_score'] = score
                        break
                save_data(data)
                
                # Store result
                st.session_state.last_score = score
                st.session_state.last_passed = score >= 80
                st.session_state.answers = {}
                st.session_state.current_question_idx = 0
                st.rerun()
        else:
            st.info(f"Answered: {len(st.session_state.answers)}/{total_questions}")
    
    with col3:
        if current_q_idx < total_questions - 1:
            if st.button("Next →", use_container_width=True):
                st.session_state.current_question_idx = min(total_questions - 1, current_q_idx + 1)
                st.rerun()
        else:
            st.button("Next →", disabled=True, use_container_width=True)
    
    # Show result if submitted
    if 'last_score' in st.session_state:
        score = st.session_state.last_score
        passed = st.session_state.last_passed
        
        if passed:
            st.balloons()
            st.success(f"🎉 Passed! Score: {score:.0f}%")
            if st.button("Next Module →"):
                del st.session_state.last_score
                del st.session_state.last_passed
                st.session_state.current_module_idx += 1
                st.rerun()
        else:
            st.error(f"❌ Failed! Score: {score:.0f}%")
            if st.button("🔄 Retry"):
                del st.session_state.last_score
                del st.session_state.last_passed
                st.session_state.answers = {}
                st.session_state.current_question_idx = 0
                st.rerun()
    
    if st.button("← Exit to Dashboard"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# REPORT CARD
elif st.session_state.page == 'report_card':
    user = st.session_state.user
    data = load_data()
    user_data = next((u for u in data if u['email'] == user.get('email')), None)
    
    st.markdown('<h2 style="margin-bottom: 20px; color: #800020;">📊 Assessment Report Card</h2>', unsafe_allow_html=True)
    
    if not user_data or not user_data.get('assessment_passed'):
        st.warning("⚠️ You haven't completed all assessments yet.")
        if st.button("← Back to Dashboard"):
            st.session_state.page = 'employee_dashboard'
            st.rerun()
    else:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%); 
                    border: 3px solid #D4AF37; border-radius: 15px; padding: 40px; 
                    text-align: center; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="color: #800020; font-size: 2.5em; margin-bottom: 10px;">🏆 Certificate of Completion</h1>
            <h2 style="color: #333; font-size: 2em; margin: 20px 0;">{user_data.get('name', 'Employee')}</h2>
            <div style="margin: 30px 0;">
                <span style="font-size: 3em; color: #D4AF37;">{'★' * 5}</span>
            </div>
            <p style="font-size: 1.1em; color: #800020; font-weight: bold;">
                Final Score: {user_data.get('assessment_score', 0):.0f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🖨️ Print Certificate"):
                st.info("Use Ctrl+P to save as PDF")
        with col2:
            if st.button("← Back to Dashboard"):
                st.session_state.page = 'employee_dashboard'
                st.rerun()

# ADMIN LOGIN
elif st.session_state.page == 'admin_login':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="margin-top: 50px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <div style="font-size: 4rem; margin-bottom: 15px;">🔐</div>
                <h2 style="font-family: Playfair Display, serif; font-size: 2.5rem; margin-bottom: 10px; color: #800020;">Admin Portal</h2>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("admin_login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("← Back"):
                    st.session_state.page = 'landing'
                    st.rerun()
            with col2:
                if st.form_submit_button("Login"):
                    if email in ADMIN_USERS and ADMIN_USERS[email] == password:
                        st.session_state.admin = email
                        st.session_state.page = 'admin_dashboard'
                        st.rerun()
                    else:
                        st.error("Invalid credentials!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ADMIN DASHBOARD
elif st.session_state.page == 'admin_dashboard':
    if not st.session_state.admin:
        st.session_state.page = 'admin_login'
        st.rerun()
    
    st.markdown('<h1 style="color: #800020; margin-bottom: 30px;">📊 Admin Dashboard</h1>', unsafe_allow_html=True)
    
    data = load_data()
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("Total", len(data))
    with cols[1]:
        st.metric("Passed", len([e for e in data if e.get('assessment_passed')]))
    with cols[2]:
        st.metric("Handbook", len([e for e in data if e.get('handbook_viewed')]))
    with cols[3]:
        st.metric("Pass Rate", f"{(len([e for e in data if e.get('assessment_passed')])/len(data)*100):.1f}%" if data else "0%")
    
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df[['name', 'email', 'department', 'assessment_passed']], hide_index=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv, "report.csv", "text/csv")
    
    if st.button("🚪 Logout"):
        st.session_state.admin = None
        st.session_state.page = 'landing'
        st.rerun()
