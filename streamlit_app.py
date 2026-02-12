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
    page_title="Medanta New Hire Portal",
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
        # Try multiple possible logo filenames
        logo_files = ["Medanta Lucknow Logo.jpg", "medanta_logo.png", "logo.png", "Medanta Logo.jpg"]
        for logo_file in logo_files:
            if os.path.exists(logo_file):
                with open(logo_file, "rb") as f:
                    return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
        return None
    except:
        return None

# Load questions from CSV or Excel
def load_questions():
    try:
        # Try Excel first (your original file)
        if os.path.exists("Question_bank.xlsx"):
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
                    
                    questions.append({
                        "id": str(row['Question_ID']),
                        "question": str(row['Question_Text']),
                        "options": opts,
                        "correct": ord(str(row['Correct_Option'])) - ord('A')
                    })
                
                assessments[str(assessment_id)] = {
                    "name": assessment_df['Assessment_Name'].iloc[0],
                    "questions": questions
                }
            return assessments
        
        # Fallback to CSV format
        elif os.path.exists("questions.csv"):
            df = pd.read_csv("questions.csv")
            df = df.dropna(subset=['Question'])
            
            assessments = {"A01": {"name": "General Assessment", "questions": []}}
            for idx, row in df.iterrows():
                opts = [
                    str(row['Option_A']),
                    str(row['Option_B']),
                    str(row['Option_C']),
                    str(row['Option_D'])
                ]
                opts = [o for o in opts if o and o != 'nan']
                
                correct_letter = str(row['Correct_Option']).strip().upper()
                correct_idx = ord(correct_letter) - ord('A') if correct_letter in ['A','B','C','D'] else 0
                
                assessments["A01"]["questions"].append({
                    "id": str(row.get('Q No', idx)),
                    "question": str(row['Question']),
                    "options": opts,
                    "correct": correct_idx
                })
            return assessments
        
        return {}
        
    except Exception as e:
        st.error(f"Error loading questions: {str(e)}")
        return {}

# Get logo source
logo_src = get_logo_src()

# MAGICAL CSS WITH ANIMATIONS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap');

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(2deg); }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.05); opacity: 0.9; }
}

@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

@keyframes rotate3D {
    0% { transform: rotateY(0deg); }
    100% { transform: rotateY(360deg); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(40px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-50px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(128,0,32,0.3); }
    50% { box-shadow: 0 0 40px rgba(128,0,32,0.6), 0 0 60px rgba(212,175,55,0.4); }
}

@keyframes namasteFloat {
    0%, 100% { transform: translateY(0) rotate(-5deg); }
    50% { transform: translateY(-15px) rotate(5deg); }
}

/* Main Background - Cream/Maroon/Gold soothing gradient */
.main-container {
    background: linear-gradient(-45deg, #faf8f3, #f5f5dc, #ebe5d8, #f0ebe0, #e8e0d5, #f5f0e8);
    background-size: 500% 500%;
    animation: gradientMove 20s ease infinite;
    min-height: 100vh;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: -2;
}

/* Floating Particles */
.particle {
    position: fixed;
    background: radial-gradient(circle, rgba(128,0,32,0.06) 0%, transparent 70%);
    border-radius: 50%;
    animation: float 12s ease-in-out infinite;
    z-index: -1;
    pointer-events: none;
}

/* Glassmorphism Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 30px;
    box-shadow: 0 8px 32px rgba(128, 0, 32, 0.08);
    padding: 40px;
    margin: 20px 0;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeInUp 0.8s ease-out;
}

.glass-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 60px rgba(128, 0, 32, 0.15);
    border-color: rgba(212, 175, 55, 0.4);
}

/* 3D JCI Seal Animation */
.seal-container {
    perspective: 1000px;
    width: 180px;
    height: 180px;
    margin: 0 auto;
}

.seal-3d {
    width: 100%;
    height: 100%;
    position: relative;
    transform-style: preserve-3d;
    animation: rotate3D 20s linear infinite;
}

.seal-face {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #ffd700, #d4af37, #b8941f);
    border: 6px solid #800020;
    box-shadow: 0 20px 60px rgba(212, 175, 55, 0.4),
                inset 0 -10px 30px rgba(0,0,0,0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    backface-visibility: hidden;
}

/* Logo Animation */
.logo-container {
    animation: pulse 3s ease-in-out infinite;
    filter: drop-shadow(0 10px 30px rgba(128,0,32,0.2));
    transition: all 0.4s ease;
}

.logo-container:hover {
    transform: scale(1.1);
    filter: drop-shadow(0 15px 40px rgba(128,0,32,0.4));
}

.logo-img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: white;
    padding: 8px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    border: 4px solid white;
    object-fit: contain;
    animation: pulse 2s infinite;
}

/* Magical Button */
.magic-btn {
    background: linear-gradient(135deg, #800020 0%, #a00030 50%, #800020 100%);
    background-size: 200% 200%;
    color: white;
    border: none;
    padding: 20px 50px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 1.1rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.4s ease;
    box-shadow: 0 10px 30px rgba(128, 0, 32, 0.3);
    position: relative;
    overflow: hidden;
    animation: glow 3s infinite;
}

.magic-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    transition: 0.6s;
}

.magic-btn:hover::before {
    left: 100%;
}

.magic-btn:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 20px 50px rgba(128, 0, 32, 0.5);
}

/* Achievement Cards */
.achievement-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(245,245,220,0.9) 100%);
    border: 2px solid rgba(212, 175, 55, 0.3);
    border-radius: 25px;
    padding: 35px 25px;
    text-align: center;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.6s ease-out;
}

.achievement-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #800020, #d4af37, #800020);
    background-size: 200% 100%;
    animation: shimmer 3s infinite;
    transform: scaleX(0);
    transition: transform 0.4s ease;
}

.achievement-card:hover {
    transform: translateY(-15px) scale(1.05);
    box-shadow: 0 25px 50px rgba(128, 0, 32, 0.12);
}

.achievement-card:hover::before {
    transform: scaleX(1);
}

/* Progress Bar */
.progress-container {
    background: rgba(128, 0, 32, 0.1);
    border-radius: 20px;
    overflow: hidden;
    height: 14px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}

.progress-bar {
    background: linear-gradient(90deg, #800020, #d4af37, #800020);
    background-size: 200% 100%;
    height: 100%;
    border-radius: 20px;
    transition: width 0.8s ease;
    animation: shimmer 3s infinite;
}

/* Title Styling */
.magic-title {
    font-family: 'Playfair Display', serif;
    font-size: 4rem;
    color: #800020;
    text-align: center;
    margin-bottom: 10px;
    text-shadow: 3px 3px 6px rgba(0,0,0,0.1);
    animation: fadeInUp 1s ease-out;
    letter-spacing: 2px;
}

.subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1.5rem;
    color: #666;
    text-align: center;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 40px;
    animation: fadeInUp 1s ease-out 0.3s both;
}

/* Namaste Animation */
.namaste {
    font-size: 4rem;
    animation: namasteFloat 3s ease-in-out infinite;
    display: inline-block;
    filter: drop-shadow(0 5px 15px rgba(0,0,0,0.1));
}

/* Hide Streamlit Elements */
#MainMenu, footer, header {visibility: hidden;}
.stDeployButton {display: none;}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: #f5f5dc;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #800020, #d4af37);
    border-radius: 6px;
}

/* Input Fields */
.magic-input {
    background: rgba(255, 255, 255, 0.9);
    border: 2px solid transparent;
    border-radius: 15px;
    padding: 15px 20px;
    font-size: 16px;
    transition: all 0.3s ease;
    width: 100%;
}

.magic-input:focus {
    border-color: #800020;
    box-shadow: 0 0 0 4px rgba(128, 0, 32, 0.1);
    outline: none;
    transform: translateY(-2px);
}

/* Question Cards */
.question-card {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 20px;
    border-left: 5px solid #800020;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    transition: all 0.3s ease;
    animation: slideIn 0.5s ease-out;
}

.question-card:hover {
    transform: translateX(10px);
    box-shadow: 0 8px 30px rgba(128, 0, 32, 0.1);
}

/* Affirmation Banner */
.affirmation-banner {
    background: linear-gradient(135deg, rgba(212,175,55,0.15) 0%, rgba(128,0,32,0.08) 100%);
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    margin-bottom: 30px;
    border: 1px solid rgba(212,175,55,0.3);
    animation: pulse 4s infinite;
}
</style>

<!-- Floating Particles -->
<div class="particle" style="width: 400px; height: 400px; top: 5%; left: 5%; animation-delay: 0s;"></div>
<div class="particle" style="width: 300px; height: 300px; top: 60%; right: 10%; animation-delay: 3s;"></div>
<div class="particle" style="width: 350px; height: 350px; bottom: 10%; left: 40%; animation-delay: 5s;"></div>
<div class="particle" style="width: 250px; height: 250px; top: 30%; right: 30%; animation-delay: 2s;"></div>
<div class="particle" style="width: 200px; height: 200px; bottom: 30%; left: 10%; animation-delay: 4s;"></div>
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
if 'assessment_submitted' not in st.session_state:
    st.session_state.assessment_submitted = False
if 'assessment_result' not in st.session_state:
    st.session_state.assessment_result = None

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

def save_csv_data(filename, data):
    """Save data to CSV for easy download"""
    filepath = DATA_DIR / filename
    df = pd.DataFrame([data])
    if filepath.exists():
        df.to_csv(filepath, mode='a', header=False, index=False)
    else:
        df.to_csv(filepath, index=False)

# Load questions
questions_data = load_questions()

# JCI Seal Component
def render_jci_seal():
    st.markdown("""
    <div style="text-align: center; padding: 30px;">
        <div class="seal-container">
            <div class="seal-3d">
                <div class="seal-face">
                    <div style="text-align: center; color: #800020;">
                        <div style="font-size: 10px; letter-spacing: 2px; font-weight: 600;">JCI ACCREDITED</div>
                        <div style="font-size: 42px; margin: 5px 0; font-weight: bold;">GOLD</div>
                        <div style="font-size: 9px; letter-spacing: 2px;">SEAL OF APPROVAL</div>
                        <div style="font-size: 18px; margin-top: 5px;">★★★</div>
                    </div>
                </div>
            </div>
        </div>
        <p style="color: #800020; margin-top: 20px; font-style: italic; font-family: Playfair Display; 
             font-size: 1.2rem; animation: pulse 3s infinite;">
            Excellence in Patient Safety
        </p>
    </div>
    """, unsafe_allow_html=True)

# LANDING PAGE
if st.session_state.page == 'landing':
    # Logo and Header
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align: center; padding: 20px 0;">', unsafe_allow_html=True)
        
        # Display logo
        if logo_src:
            st.markdown(f'<div class="logo-container"><img src="{logo_src}" class="logo-img" alt="Medanta Logo"></div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size: 80px; text-align: center; animation: pulse 2s infinite;">🏥</div>', 
                       unsafe_allow_html=True)
        
        st.markdown('<h1 class="magic-title">Welcome to Medanta</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">The Medicity</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # JCI Seal
    render_jci_seal()
    
    # Achievements
    st.markdown("<div style='padding: 30px 0;'>", unsafe_allow_html=True)
    
    achievements = [
        ("🏆", "JCI Gold Seal", "3rd Consecutive Accreditation"),
        ("🌍", "Global Recognition", "Among World's Best Hospitals"),
        ("❤️", "5000+ Lives", "Saved through Organ Transplants"),
        ("🔬", "Research Excellence", "1000+ Published Papers"),
        ("⭐", "NABH Accredited", "Highest Quality Standards"),
        ("🤖", "Robotic Surgery", "Pioneer in Da Vinci Surgery")
    ]
    
    for row in range(2):
        cols = st.columns(3)
        for idx in range(3):
            i = row * 3 + idx
            if i < len(achievements):
                icon, title, desc = achievements[i]
                with cols[idx]:
                    st.markdown(f"""
                    <div class="achievement-card" style="animation-delay: {i * 0.1}s;">
                        <div style="font-size: 3rem; margin-bottom: 15px; animation: float 4s ease-in-out infinite; 
                             animation-delay: {i * 0.5}s;">{icon}</div>
                        <h3 style="color: #800020; font-family: Playfair Display; margin-bottom: 8px; 
                             font-size: 1.2rem;">{title}</h3>
                        <p style="color: #666; font-size: 0.9rem;">{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # CTA Buttons
    st.markdown("<div style='text-align: center; padding: 40px 0;'>", unsafe_allow_html=True)
    col1, col2, col1 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Begin Your Journey", use_container_width=True):
            st.session_state.page = 'employee_login'
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔐 Admin Portal", use_container_width=True):
            st.session_state.page = 'admin_login'
            st.rerun()
    
    st.markdown("""
        <p style="text-align: center; color: #800020; margin-top: 30px; font-style: italic; 
             font-family: Playfair Display; font-size: 1.2rem; animation: pulse 3s infinite;">
            "Where Healing Meets Innovation"
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Contacts
    with st.expander("📞 Key Contacts"):
        col1, col2 = st.columns(2)
        with col1:
            st.info("**EMR/HIS** - Mr. Surjendra\n📱 9883111600")
            st.info("**Salary** - HR Dept\n📱 9560719167")
        with col2:
            st.info("**IT Helpdesk**\n☎️ 1010")
            st.info("**Training** - Dr. Pallavi & Mr. Rohit\n📞 7860955988 | 7275181822")

# EMPLOYEE LOGIN
elif st.session_state.page == 'employee_login':
    col1, col2, col1 = st.columns([1, 2.5, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="margin-top: 30px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <span class="namaste">🙏</span>
                <h2 style="color: #800020; font-family: Playfair Display; font-size: 2.5rem; 
                     margin-top: 15px;">Join the Medanta Family</h2>
                <p style="color: #666;">Your personalized induction journey awaits</p>
            </div>
        """, unsafe_allow_html=True)
        
        # New Joinee
        with st.form("employee_reg"):
            st.subheader("🆕 New Joinee")
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            email = st.text_input("Email Address *", placeholder="your.email@medanta.org")
            
            col_cat, col_dept = st.columns(2)
            with col_cat:
                category = st.selectbox("Category *", 
                                      ["Select", "Clinical", "Administration", "Nursing", "Paramedical"])
            with col_dept:
                department = st.text_input("Department *", placeholder="e.g., Cardiology")
            
            mobile = st.text_input("Mobile Number *", placeholder="+91 XXXXX XXXXX")
            emp_id = st.text_input("Employee ID (if available)", placeholder="Optional")
            
            submitted = st.form_submit_button("✨ Create My Portal", use_container_width=True)
            
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
                        save_csv_data("user_logins.csv", {
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'name': name, 'email': email, 'department': department,
                            'category': category, 'emp_id': emp_id if emp_id else "Pending"
                        })
                        st.session_state.user = new_user
                        st.session_state.page = 'employee_dashboard'
                        st.rerun()
        
        # Returning User
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("🔙 Returning User")
        
        with st.form("employee_login_form"):
            login_email = st.text_input("Email Address", placeholder="your.email@medanta.org")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("← Back to Home"):
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

# EMPLOYEE DASHBOARD
elif st.session_state.page == 'employee_dashboard':
    user = st.session_state.user
    
    st.markdown(f"""
    <div style="text-align: center; padding: 30px 0;">
        <span class="namaste">🙏</span>
        <h1 style="font-family: Playfair Display; color: #800020; font-size: 2.8rem; margin: 15px 0;">
            Namaste, {user['name']}
        </h1>
        <p style="color: #666; font-size: 1.1rem;">{user['department']} | {user['category']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress
    progress = 0
    if user.get('handbook_viewed'): progress += 33
    if user.get('assessment_passed'): progress += 33
    if user.get('departmental_induction'): progress += 34
    
    st.markdown(f"""
    <div class="glass-card" style="padding: 25px;">
        <h3 style="color: #800020; margin-bottom: 15px;">📊 Your Progress</h3>
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress}%;"></div>
        </div>
        <p style="text-align: center; margin-top: 10px; color: #666;">{progress}% Complete</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Modules
    st.subheader("🎯 Learning Modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card" style="padding: 25px;">', unsafe_allow_html=True)
        st.subheader("📚 Employee Handbook")
        st.write("Learn about Medanta's policies, culture, and benefits")
        if st.button("Open Handbook", use_container_width=True):
            # Mark as viewed
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
        st.subheader("📝 Assessments")
        st.write(f"Complete all {len(questions_data)} modules. Need 80% to pass!")
        if st.button("Start Assessment", use_container_width=True):
            st.session_state.assessment_submitted = False
            st.session_state.assessment_result = None
            st.session_state.current_module_idx = user.get('current_module', 0)
            st.session_state.page = 'assessment'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card" style="padding: 25px;">', unsafe_allow_html=True)
        st.subheader("🏅 JCI Handbook")
        st.write("International Patient Safety Goals and standards")
        if st.button("Open JCI Guide", use_container_width=True):
            st.session_state.page = 'jci_handbook'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card" style="padding: 25px;">', unsafe_allow_html=True)
        st.subheader("🎓 Report Card")
        if user.get('assessment_passed'):
            st.success("✅ Certification Complete!")
            if st.button("View Certificate", use_container_width=True):
                st.session_state.page = 'report_card'
                st.rerun()
        else:
            st.warning("⏳ Complete assessment first")
            st.button("View Certificate", use_container_width=True, disabled=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.user = None
        st.session_state.page = 'landing'
        st.rerun()

# HANDBOOK
elif st.session_state.page == 'handbook':
    st.subheader("📚 Employee Handbook")
    st.components.v1.iframe("https://online.flippingbook.com/view/652486186/", height=700)
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# JCI HANDBOOK
elif st.session_state.page == 'jci_handbook':
    st.subheader("🏅 JCI Accreditation Standards")
    st.components.v1.iframe("https://online.flippingbook.com/view/389334287/", height=700)
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# ASSESSMENT
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
        # All complete
        st.balloons()
        st.success("🎉 Congratulations! You have completed all assessments!")
        
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
    progress = (current_idx / len(module_ids)) * 100
    
    st.markdown(f"""
    <div style="margin-bottom: 30px;">
        <h2 style="color: #800020; font-family: Playfair Display;">{current_module['name']}</h2>
        <p>Module {current_idx + 1} of {len(module_ids)} | {len(questions)} Questions</p>
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Affirmation
    affirmations = [
        "🌟 You're doing amazing! Keep going!",
        "💪 Every question makes you stronger!",
        "🎯 Focus and precision - you've got this!",
        "🏥 Medanta believes in you!",
        "⭐ Excellence is your standard!"
    ]
    st.markdown(f"""
    <div class="affirmation-banner">
        <p style="color: #800020; font-weight: 600; margin: 0; font-size: 1.1rem;">
            {affirmations[current_idx % len(affirmations)]}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.assessment_submitted:
        with st.form("assessment_form"):
            correct_count = 0
            user_answers = {}
            
            for i, q in enumerate(questions):
                st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
                st.write(f"**Q{i+1}. {q['question']}**")
                
                answer = st.radio(
                    "Select your answer:",
                    q['options'],
                    index=None,
                    key=f"q_{current_idx}_{i}"
                )
                user_answers[i] = answer
                
                if answer == q['options'][q['correct']]:
                    correct_count += 1
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Submit Module", type="primary")
            
            if submitted:
                if None in user_answers.values():
                    st.error("⚠️ Please answer all questions before submitting!")
                    st.stop()
                
                score_pct = (correct_count / len(questions)) * 100
                
                st.session_state.assessment_result = {
                    'score': correct_count,
                    'total': len(questions),
                    'percentage': score_pct
                }
                st.session_state.assessment_submitted = True
                
                # Save to data
                data = load_data()
                for u in data:
                    if u['email'] == user['email']:
                        u['attempts'] = u.get('attempts', 0) + 1
                        if score_pct >= 80:
                            u['current_module'] = current_idx + 1
                            if current_idx + 1 >= len(module_ids):
                                u['assessment_passed'] = True
                                u['assessment_score'] = score_pct
                        st.session_state.user = u
                        break
                save_data(data)
                
                # Save to CSV
                save_csv_data("assessment_results.csv", {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'user': user['name'],
                    'email': user['email'],
                    'module': current_module['name'],
                    'score': score_pct,
                    'correct': correct_count,
                    'total': len(questions),
                    'status': 'PASSED' if score_pct >= 80 else 'FAILED'
                })
                
                st.rerun()
    
    else:
        # Show results
        result = st.session_state.assessment_result
        score_pct = result['percentage']
        
        st.markdown("---")
        st.subheader("📊 Module Result")
        
        if score_pct >= 80:
            st.balloons()
            st.success(f"🎉 Congratulations! You passed with {score_pct:.0f}%!")
            st.info("Click 'Next Module' to continue your journey.")
            
            if st.button("➡️ Next Module", type="primary"):
                st.session_state.assessment_submitted = False
                st.session_state.assessment_result = None
                st.session_state.current_module_idx += 1
                st.rerun()
        else:
            st.error(f"❌ You scored {score_pct:.0f}%. You need 80% to pass.")
            st.info("🔄 Don't worry! Review the material and try again.")
            
            if st.button("🔄 Reattempt Module"):
                st.session_state.assessment_submitted = False
                st.session_state.assessment_result = None
                st.rerun()
        
        if st.button("← Back to Dashboard"):
            st.session_state.assessment_submitted = False
            st.session_state.assessment_result = None
            st.session_state.page = 'employee_dashboard'
            st.rerun()

# REPORT CARD
elif st.session_state.page == 'report_card':
    user = st.session_state.user
    
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; max-width: 800px; margin: 0 auto; 
         border: 3px solid #d4af37; background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(245,245,220,0.9));">
        <div style="font-size: 4rem; margin-bottom: 20px;">🎓</div>
        <h1 style="color: #800020; font-family: Playfair Display; font-size: 2.5rem; margin-bottom: 10px;">
            Certificate of Completion
        </h1>
        <p style="color: #666; font-size: 1.1rem; margin-bottom: 30px;">
            Medanta New Hire Induction Program
        </p>
        
        <div style="background: rgba(128,0,32,0.05); padding: 30px; border-radius: 20px; margin: 30px 0;">
            <h2 style="color: #800020; font-family: Playfair Display; font-size: 2rem; margin-bottom: 10px;">
                {user['name']}
            </h2>
            <p style="color: #666; font-size: 1.1rem;">{user['department']} Department</p>
            <p style="color: #666; font-size: 1rem;">Employee ID: {user.get('emp_id', 'Pending')}</p>
        </div>
        
        <div style="background: linear-gradient(135deg, #800020, #a00030); color: white; 
             padding: 30px; border-radius: 20px; margin: 30px 0;">
            <p style="font-size: 1.2rem; margin-bottom: 10px;">Assessment Score</p>
            <h2 style="font-size: 3rem; margin: 0; font-family: Playfair Display;">
                {user.get('assessment_score', 0):.0f}%
            </h2>
            <p style="margin-top: 10px; opacity: 0.9;">Status: PASSED ✅</p>
        </div>
        
        <p style="color: #666; font-style: italic; margin-top: 30px;">
            This certifies that the above named employee has successfully completed<br>
            the mandatory induction program at <strong style="color: #800020;">Medanta - The Medicity</strong>
        </p>
        
        <p style="color: #800020; margin-top: 20px; font-weight: 600;">
            Validated by: Learning & Development Department<br>
            <span style="font-size: 0.9rem; color: #666; font-weight: 400;">
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
        <div class="glass-card" style="margin-top: 50px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <span style="font-size: 4rem;">🔐</span>
                <h2 style="color: #800020; font-family: Playfair Display; font-size: 2rem; 
                     margin-top: 15px;">Admin Portal</h2>
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
                if st.form_submit_button("Login"):
                    if email in ADMIN_USERS and password == ADMIN_USERS[email]:
                        st.session_state.admin = email
                        st.session_state.page = 'admin_dashboard'
                        st.rerun()
                    else:
                        st.error("Invalid credentials!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ADMIN DASHBOARD
elif st.session_state.page == 'admin_dashboard':
    st.subheader(f"🔐 Admin Dashboard")
    st.write(f"Logged in as: {st.session_state.admin}")
    
    data = load_data()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Employees", len(data))
    col2.metric("Passed", len([e for e in data if e.get('assessment_passed')]))
    col3.metric("In Progress", len([e for e in data if not e.get('assessment_passed') and e.get('attempts', 0) > 0]))
    col4.metric("Not Started", len([e for e in data if e.get('attempts', 0) == 0]))
    
    # Data table
    st.markdown("---")
    st.subheader("📊 Employee Records")
    
    if data:
        df = pd.DataFrame(data)
        display_cols = ['name', 'email', 'department', 'category', 'assessment_score', 'assessment_passed', 'attempts']
        display_df = df[[col for col in display_cols if col in df.columns]].copy()
        
        if 'assessment_passed' in display_df.columns:
            display_df['assessment_passed'] = display_df['assessment_passed'].map({True: '✅', False: '❌'})
        if 'assessment_score' in display_df.columns:
            display_df['assessment_score'] = display_df['assessment_score'].fillna(0).apply(lambda x: f"{x:.0f}%" if x else "N/A")
        
        st.dataframe(display_df, use_container_width=True)
        
        # Download buttons
        col1, col2 = st.columns(2)
        with col1:
            csv = df.to_csv(index=False)
            st.download_button("📥 Download Full Report (CSV)", csv, 
                              f"medanta_report_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
        
        with col2:
            # Download CSV data folder
            if os.path.exists(DATA_DIR / "user_logins.csv"):
                with open(DATA_DIR / "user_logins.csv", 'rb') as f:
                    st.download_button("📥 Download User Logins", f, "user_logins.csv", "text/csv")
    else:
        st.info("No employee data yet.")
    
    if st.button("🚪 Logout"):
        st.session_state.admin = None
        st.session_state.page = 'landing'
        st.rerun()
