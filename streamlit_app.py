import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import base64
from pathlib import Path
import time

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

# DARK THEME CSS - Borrowed from HTML
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --medanta-teal: #008B8B;
    --medanta-gold: #D4AF37;
    --medanta-dark: #0f172a;
}

* {
    font-family: 'Inter', sans-serif;
}

/* Main dark background */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    color: white;
    min-height: 100vh;
}

/* Hide Streamlit elements */
#MainMenu, footer, header, .stDeployButton {display: none;}

/* Glassmorphism cards */
.glass-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 40px;
    margin: 20px 0;
    transition: all 0.3s ease;
}

.glass-card:hover {
    border-color: rgba(0, 139, 139, 0.5);
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

/* Gradient text */
.gradient-text {
    background: linear-gradient(135deg, #fff 0%, #008B8B 50%, #D4AF37 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-family: 'Playfair Display', serif;
}

/* Teal buttons */
.teal-btn {
    background: linear-gradient(135deg, #008B8B 0%, #006666 100%);
    color: white;
    border: none;
    padding: 16px 32px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0, 139, 139, 0.3);
    width: 100%;
}

.teal-btn:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 15px 40px rgba(0, 139, 139, 0.4);
}

/* Gold accent button */
.gold-btn {
    background: linear-gradient(135deg, #D4AF37 0%, #B8941F 100%);
    color: #0f172a;
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

/* Outline button */
.outline-btn {
    background: transparent;
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.2);
    padding: 16px 32px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 1.1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
}

.outline-btn:hover {
    border-color: #008B8B;
    background: rgba(0, 139, 139, 0.1);
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
    box-shadow: 0 20px 60px rgba(0, 139, 139, 0.3);
    border: 4px solid rgba(255, 255, 255, 0.1);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); box-shadow: 0 20px 60px rgba(0, 139, 139, 0.3); }
    50% { transform: scale(1.05); box-shadow: 0 30px 80px rgba(0, 139, 139, 0.5); }
}

/* 3D Seal */
.seal-3d {
    width: 200px;
    height: 200px;
    margin: 0 auto;
    background: linear-gradient(135deg, #ffd700 0%, #D4AF37 50%, #B8941F 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 6px solid #0f172a;
    box-shadow: 0 20px 60px rgba(212, 175, 55, 0.4), inset 0 -10px 30px rgba(0,0,0,0.2);
    animation: rotate-seal 10s linear infinite;
    position: relative;
}

@keyframes rotate-seal {
    0% { transform: rotateY(0deg); }
    100% { transform: rotateY(360deg); }
}

/* Progress bar */
.progress-container {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    overflow: hidden;
    height: 12px;
}

.progress-bar {
    background: linear-gradient(90deg, #008B8B, #D4AF37);
    height: 100%;
    border-radius: 20px;
    transition: width 0.5s ease;
}

/* Question cards */
.question-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
    transition: all 0.3s ease;
    border-left: 4px solid #008B8B;
}

.question-card:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateX(10px);
    border-color: rgba(0, 139, 139, 0.5);
}

/* Radio buttons styling */
div[role="radiogroup"] > label {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 12px;
}

div[role="radiogroup"] > label:hover {
    background: rgba(0, 139, 139, 0.1);
    border-color: #008B8B;
    transform: translateX(5px);
}

/* Stats cards */
.stat-card {
    background: rgba(0, 139, 139, 0.1);
    border: 1px solid rgba(0, 139, 139, 0.3);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
    background: rgba(0, 139, 139, 0.15);
}

/* Typography */
h1, h2, h3 {
    color: white !important;
    font-family: 'Playfair Display', serif;
}

p, span, div {
    color: #94a3b8;
}

/* Success/Error messages */
.success-msg {
    background: rgba(0, 139, 139, 0.2);
    border: 1px solid #008B8B;
    border-radius: 12px;
    padding: 20px;
    color: #008B8B;
}

.error-msg {
    background: rgba(239, 68, 68, 0.2);
    border: 1px solid #ef4444;
    border-radius: 12px;
    padding: 20px;
    color: #ef4444;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: #0f172a;
}
::-webkit-scrollbar-thumb {
    background: #008B8B;
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
    background: rgba(255, 255, 255, 0.05);
    padding: 10px;
    border-radius: 16px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 12px;
    padding: 12px 24px;
    color: #94a3b8;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #008B8B 0%, #006666 100%) !important;
    color: white !important;
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

# LANDING PAGE - Dark theme with glassmorphism
if st.session_state.page == 'landing':
    # Background effects
    st.markdown("""
    <div style="position: fixed; top: 20%; left: 10%; width: 400px; height: 400px; 
         background: radial-gradient(circle, rgba(0,139,139,0.15) 0%, transparent 70%); 
         border-radius: 50%; pointer-events: none; z-index: 0;"></div>
    <div style="position: fixed; bottom: 20%; right: 10%; width: 300px; height: 300px; 
         background: radial-gradient(circle, rgba(212,175,55,0.1) 0%, transparent 70%); 
         border-radius: 50%; pointer-events: none; z-index: 0;"></div>
    """, unsafe_allow_html=True)
    
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        if logo_src:
            st.markdown(f'<img src="{logo_src}" class="logo-img" alt="Medanta Logo">', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size: 80px; text-align: center;">🏥</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<h1 class="gradient-text" style="text-align: center; font-size: 4rem; margin-bottom: 10px;">Welcome to Medanta</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #94a3b8; font-size: 1.3rem; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 40px;">The Medicity</p>', unsafe_allow_html=True)
        
        # 3D Seal
        st.markdown("""
        <div style="text-align: center; margin: 40px 0;">
            <div class="seal-3d">
                <div style="text-align: center; color: #0f172a;">
                    <div style="font-size: 12px; letter-spacing: 2px; font-weight: 700;">JCI ACCREDITED</div>
                    <div style="font-size: 48px; font-weight: bold; margin: 5px 0;">GOLD</div>
                    <div style="font-size: 10px; letter-spacing: 2px;">SEAL OF APPROVAL</div>
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
                    <div style="font-size: 2rem; font-weight: 700; color: #008B8B;">{num}</div>
                    <div style="font-size: 0.9rem; color: #64748b;">{label}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # CTA Buttons
        if st.button("🚀 Begin Your Journey", key="start_btn"):
            st.session_state.page = 'employee_login'
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔐 Admin Portal", key="admin_btn"):
            st.session_state.page = 'admin_login'
            st.rerun()
        
        st.markdown("""
        <p style="text-align: center; color: #64748b; margin-top: 30px; font-style: italic; font-family: 'Playfair Display', serif;">
            "Where Healing Meets Innovation"
        </p>
        """, unsafe_allow_html=True)

# EMPLOYEE LOGIN - Dark glassmorphism
elif st.session_state.page == 'employee_login':
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="margin-top: 50px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <div style="font-size: 4rem; margin-bottom: 15px; animation: float 3s ease-in-out infinite;">🙏</div>
                <h2 style="font-family: 'Playfair Display', serif; font-size: 2.5rem; margin-bottom: 10px;">Join the Medanta Family</h2>
                <p style="color: #64748b;">Your personalized induction journey awaits</p>
            </div>
        """, unsafe_allow_html=True)
        
        # New Joinee
        with st.form("employee_reg"):
            st.markdown('<p style="color: #008B8B; font-weight: 600; margin-bottom: 15px;">🆕 New Joinee</p>', unsafe_allow_html=True)
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
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
        st.markdown('<p style="color: #D4AF37; font-weight: 600; margin-bottom: 15px;">🔙 Returning User</p>', unsafe_allow_html=True)
        
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

# EMPLOYEE DASHBOARD - Dark theme
elif st.session_state.page == 'employee_dashboard':
    user = st.session_state.user
    
    st.markdown(f"""
    <div style="text-align: center; padding: 30px 0;">
        <div style="font-size: 3.5rem; margin-bottom: 15px; animation: pulse 2s infinite; display: inline-block;">🙏</div>
        <h1 style="font-family: 'Playfair Display', serif; font-size: 3rem; margin-bottom: 10px;">
            Namaste, {user['name']}
        </h1>
        <p style="color: #64748b; font-size: 1.1rem;">{user['department']} | {user['category']}</p>
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
            <span style="color: white; font-weight: 600;">Your Progress</span>
            <span style="color: #008B8B; font-weight: 700;">{progress}%</span>
        </div>
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Modules
    st.markdown('<h2 style="margin-bottom: 20px;">🎯 Learning Modules</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card" style="padding: 25px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 2.5rem; margin-bottom: 15px;">📚</div>', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 10px;">Employee Handbook</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #64748b; margin-bottom: 20px;">Learn about Medanta\'s policies and culture</p>', unsafe_allow_html=True)
        if st.button("Open Handbook", key="handbook"):
            data = load_data()
            for u in data:
                if u['email'] == user['email']:
                    u['handbook_viewed'] = True
                    st.session_state.user = u
                    break
            save_data(data)
            st.session_state.page = 'handbook'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card" style="padding: 25px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 2.5rem; margin-bottom: 15px;">📝</div>', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 10px;">Assessments</h3>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #64748b; margin-bottom: 20px;">{len(questions_data)} modules • 80% to pass</p>', unsafe_allow_html=True)
        if st.button("Start Assessment", key="assessment"):
            st.session_state.current_module_idx = user.get('current_module', 0)
            st.session_state.page = 'assessment'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card" style="padding: 25px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 2.5rem; margin-bottom: 15px;">🏅</div>', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 10px;">JCI Handbook</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #64748b; margin-bottom: 20px;">International Patient Safety Goals</p>', unsafe_allow_html=True)
        if st.button("Open JCI Guide", key="jci"):
            st.session_state.page = 'jci_handbook'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card" style="padding: 25px;">', unsafe_allow_html=True)
        st.markdown('<div style="font-size: 2.5rem; margin-bottom: 15px;">🎓</div>', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-bottom: 10px;">Report Card</h3>', unsafe_allow_html=True)
        if user.get('assessment_passed'):
            st.markdown('<p style="color: #008B8B; margin-bottom: 20px;">✅ Certification Complete!</p>', unsafe_allow_html=True)
            if st.button("View Certificate", key="cert"):
                st.session_state.page = 'report_card'
                st.rerun()
        else:
            st.markdown('<p style="color: #64748b; margin-bottom: 20px;">⏳ Complete assessment first</p>', unsafe_allow_html=True)
            st.button("View Certificate", disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.user = None
        st.session_state.page = 'landing'
        st.rerun()

# HANDBOOK
elif st.session_state.page == 'handbook':
    st.markdown('<h2 style="margin-bottom: 20px;">📚 Employee Handbook</h2>', unsafe_allow_html=True)
    st.components.v1.iframe("https://online.flippingbook.com/view/652486186/ ", height=700)
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# JCI HANDBOOK
elif st.session_state.page == 'jci_handbook':
    st.markdown('<h2 style="margin-bottom: 20px;">🏅 JCI Accreditation Standards</h2>', unsafe_allow_html=True)
    st.components.v1.iframe("https://online.flippingbook.com/view/389334287/ ", height=700)
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# ASSESSMENT - With tabs for each topic
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
            if u['email'] == user['email']:
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
    
    # Progress
    st.markdown(f"""
    <div style="margin-bottom: 30px;">
        <h2 style="color: #008B8B; margin-bottom: 10px;">{current_module['name']}</h2>
        <p style="color: #64748b;">Module {current_idx + 1} of {len(module_ids)} • {len(questions)} Questions</p>
        <div class="progress-container" style="margin-top: 15px;">
            <div class="progress-bar" style="width: {(current_idx/len(module_ids))*100}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for each question
    tabs = st.tabs([f"Q{i+1}" for i in range(len(questions))])
    
    answers = {}
    
    for i, (tab, q) in enumerate(zip(tabs, questions)):
        with tab:
            st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
            st.markdown(f'<h3 style="color: white; margin-bottom: 20px;">{q["question"]}</h3>', unsafe_allow_html=True)
            
            answer = st.radio(
                "Select your answer:",
                q['options'],
                index=None,
                key=f"q_{current_idx}_{i}"
            )
            answers[i] = answer
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit button
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
    
    if st.button("Submit Module", type="primary", use_container_width=True):
        if None in answers.values():
            st.error("⚠️ Please answer all questions before submitting!")
            st.stop()
        
        correct_count = 0
        for i, q in enumerate(questions):
            if answers[i] == q['options'][q['correct']]:
                correct_count += 1
        
        percentage = (correct_count / len(questions)) * 100
        
        # Save result
        data = load_data()
        for u in data:
            if u['email'] == user['email']:
                u['attempts'] = u.get('attempts', 0) + 1
                if percentage >= 80:
                    u['current_module'] = current_idx + 1
                    if current_idx + 1 >= len(module_ids):
                        u['assessment_passed'] = True
                        u['assessment_score'] = percentage
                break
        save_data(data)
        
        # Show result
        if percentage >= 80:
            st.balloons()
            st.success(f"🎉 Congratulations! You passed with {percentage:.0f}%!")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➡️ Next Module"):
                    st.session_state.current_module_idx += 1
                    st.rerun()
            with col2:
                if st.button("← Back to Dashboard"):
                    st.session_state.page = 'employee_dashboard'
                    st.rerun()
        else:
            st.error(f"❌ You scored {percentage:.0f}%. You need 80% to pass.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Reattempt Module"):
                    st.rerun()
            with col2:
                if st.button("← Back to Dashboard"):
                    st.session_state.page = 'employee_dashboard'
                    st.rerun()

# REPORT CARD
elif st.session_state.page == 'report_card':
    user = st.session_state.user
    
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; max-width: 800px; margin: 0 auto; 
         border: 2px solid #D4AF37; background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.9));">
        <div style="font-size: 4rem; margin-bottom: 20px;">🎓</div>
        <h1 style="font-family: 'Playfair Display', serif; font-size: 2.5rem; margin-bottom: 10px; color: #D4AF37;">
            Certificate of Completion
        </h1>
        <p style="color: #64748b; margin-bottom: 30px;">Medanta New Hire Induction Program</p>
        
        <div style="background: rgba(0,139,139,0.1); padding: 30px; border-radius: 20px; margin: 30px 0; border: 1px solid rgba(0,139,139,0.3);">
            <h2 style="font-family: 'Playfair Display', serif; font-size: 2rem; margin-bottom: 10px; color: white;">
                {user['name']}
            </h2>
            <p style="color: #64748b;">{user['department']} Department</p>
            <p style="color: #64748b;">Employee ID: {user.get('emp_id', 'Pending')}</p>
        </div>
        
        <div style="background: linear-gradient(135deg, #008B8B, #006666); padding: 30px; border-radius: 20px; margin: 30px 0;">
            <p style="font-size: 1.2rem; margin-bottom: 10px; color: rgba(255,255,255,0.8);">Assessment Score</p>
            <h2 style="font-size: 3rem; margin: 0; font-family: 'Playfair Display', serif; color: white;">
                {user.get('assessment_score', 0):.0f}%
            </h2>
            <p style="margin-top: 10px; color: rgba(255,255,255,0.8);">Status: PASSED ✅</p>
        </div>
        
        <p style="color: #64748b; font-style: italic; margin-top: 30px;">
            This certifies that the above named employee has successfully completed<br>
            the mandatory induction program at <strong style="color: #008B8B;">Medanta - The Medicity</strong>
        </p>
        
        <p style="color: #D4AF37; margin-top: 20px; font-weight: 600;">
            Validated by: Dr. Pallavi & Mr. Rohit<br>
            <span style="font-size: 0.9rem; color: #64748b;">
                Date: {datetime.now().strftime("%B %d, %Y")}
            </span>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Download certificate
    cert_text = f"""MEDANTA INDUCTION CERTIFICATE

This certifies that
{user['name']}

has successfully completed the Medanta Induction Program.

Department: {user['department']}
Employee ID: {user.get('emp_id', 'Pending')}
Score: {user.get('assessment_score', 0):.0f}%
Status: PASSED

Date: {datetime.now().strftime("%B %d, %Y")}
Validated by: Dr. Pallavi & Mr. Rohit
Learning & Development Department
Medanta - The Medicity
"""
    
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        st.download_button("📜 Download Certificate", cert_text, 
                          f"Medanta_Certificate_{user['name']}.txt", "text/plain")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.page = 'employee_dashboard'
            st.rerun()

# ADMIN LOGIN
elif st.session_state.page == 'admin_login':
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="margin-top: 80px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <div style="font-size: 4rem; margin-bottom: 15px;">🔐</div>
                <h2 style="font-family: 'Playfair Display', serif; font-size: 2rem;">Admin Portal</h2>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("admin_login"):
            email = st.text_input("Admin Email")
            password = st.text_input("Password", type="password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("← Back"):
                    st.session_state.page = 'landing'
                    st.rerun()
            with col2:
                submitted = st.form_submit_button("Login")
            
            if submitted:
                if email in ADMIN_USERS and password == ADMIN_USERS[email]:
                    st.session_state.admin = email
                    st.session_state.page = 'admin_dashboard'
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ADMIN DASHBOARD
elif st.session_state.page == 'admin_dashboard':
    st.markdown('<h2 style="margin-bottom: 5px;">🔐 Admin Dashboard</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #64748b; margin-bottom: 30px;">{st.session_state.admin}</p>', unsafe_allow_html=True)
    
    data = load_data()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2rem; font-weight: 700; color: #008B8B;">{len(data)}</div>
            <div style="color: #64748b;">Total</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        passed = len([e for e in data if e.get('assessment_passed')])
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2rem; font-weight: 700; color: #008B8B;">{passed}</div>
            <div style="color: #64748b;">Passed</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        pending = len([e for e in data if not e.get('assessment_passed')])
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2rem; font-weight: 700; color: #D4AF37;">{pending}</div>
            <div style="color: #64748b;">Pending</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        avg = sum(e.get('assessment_score', 0) for e in data) / len(data) if data else 0
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2rem; font-weight: 700; color: #008B8B;">{avg:.1f}%</div>
            <div style="color: #64748b;">Avg Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Data table
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)
    st.markdown('<h3 style="margin-bottom: 20px;">📊 Employee Records</h3>', unsafe_allow_html=True)
    
    if data:
        df = pd.DataFrame(data)
        display_cols = ['name', 'email', 'department', 'category', 'assessment_score', 'assessment_passed', 'attempts']
        display_df = df[[col for col in display_cols if col in df.columns]].copy()
        
        if 'assessment_passed' in display_df.columns:
            display_df['assessment_passed'] = display_df['assessment_passed'].map({True: '✅', False: '❌'})
        if 'assessment_score' in display_df.columns:
            display_df['assessment_score'] = display_df['assessment_score'].fillna(0).apply(lambda x: f"{x:.0f}%" if x else "N/A")
        
        st.dataframe(display_df, use_container_width=True)
        
        csv = df.to_csv(index=False)
        st.download_button("📥 Download Report (CSV)", csv, 
                          f"medanta_report_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    else:
        st.info("No data yet.")
    
    if st.button("🚪 Logout"):
        st.session_state.admin = None
        st.session_state.page = 'landing'
        st.rerun()
