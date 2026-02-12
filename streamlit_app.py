import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from pathlib import Path

# Page config
st.set_page_config(page_title="Medanta Induction", layout="wide")

# Create data folder
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Load questions
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
                correct_idx = ord(correct_val[0].upper()) - ord('A')
                correct_idx = max(0, min(3, correct_idx))
                questions.append({
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
        st.error(f"Error loading questions: {e}")
        return {}

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'current_module' not in st.session_state:
    st.session_state.current_module = 0

DATA_FILE = DATA_DIR / "employees.json"
ADMIN_USERS = {"pallavi.singh@medanta.org": "Pallavi@2024", "rohit.singh@medanta.org": "Rohit@2024"}

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

questions_data = load_questions()

# Simple CSS
st.markdown("""
<style>
    .main { background: #FAF8F3; }
    h1, h2, h3 { color: #800020; }
    .stButton>button { 
        background: #800020; 
        color: white; 
        border-radius: 8px; 
        padding: 10px 24px;
    }
    .stButton>button:hover { background: #A00030; }
</style>
""", unsafe_allow_html=True)

# LANDING PAGE
if st.session_state.page == 'landing':
    st.markdown("<h1 style='text-align: center;'>🏥 Welcome to Medanta</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #D4AF37; font-size: 1.2rem;'>The Medicity - JCI Gold Accredited</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Begin Your Journey", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
        if st.button("🔐 Admin Portal", use_container_width=True):
            st.session_state.page = 'admin_login'
            st.rerun()

# LOGIN PAGE
elif st.session_state.page == 'login':
    st.markdown("<h2>New Joinee Registration</h2>", unsafe_allow_html=True)
    
    with st.form("reg_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        dept = st.text_input("Department")
        mobile = st.text_input("Mobile")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("← Back"):
                st.session_state.page = 'landing'
                st.rerun()
        with col2:
            if st.form_submit_button("Register"):
                if name and email and dept:
                    data = load_data()
                    new_user = {
                        "name": name, "email": email, "department": dept,
                        "mobile": mobile, "registered_at": datetime.now().isoformat(),
                        "assessment_passed": False, "current_module": 0
                    }
                    data.append(new_user)
                    save_data(data)
                    st.session_state.user = new_user
                    st.session_state.page = 'dashboard'
                    st.rerun()
                else:
                    st.error("Please fill required fields")

# DASHBOARD
elif st.session_state.page == 'dashboard':
    user = st.session_state.user
    st.markdown(f"<h2>Welcome, {user.get('name', 'User')}</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 Employee Handbook"):
            st.session_state.page = 'handbook'
            st.rerun()
        if st.button("📝 Take Assessment"):
            st.session_state.current_module = user.get('current_module', 0)
            st.session_state.current_q = 0
            st.session_state.answers = {}
            st.session_state.page = 'assessment'
            st.rerun()
    with col2:
        if st.button("🏅 JCI Handbook"):
            st.session_state.page = 'jci'
            st.rerun()
        if st.button("📊 Report Card"):
            st.session_state.page = 'report'
            st.rerun()
    
    if st.button("🚪 Logout"):
        st.session_state.user = None
        st.session_state.page = 'landing'
        st.rerun()

# HANDBOOK
elif st.session_state.page == 'handbook':
    st.markdown("<h2>Employee Handbook</h2>", unsafe_allow_html=True)
    st.components.v1.iframe("https://online.flippingbook.com/view/652486186/", height=600)
    if st.button("← Back"):
        st.session_state.page = 'dashboard'
        st.rerun()

# JCI HANDBOOK
elif st.session_state.page == 'jci':
    st.markdown("<h2>JCI Standards</h2>", unsafe_allow_html=True)
    st.components.v1.iframe("https://online.flippingbook.com/view/389334287/", height=600)
    if st.button("← Back"):
        st.session_state.page = 'dashboard'
        st.rerun()

# ASSESSMENT - SIMPLE VERSION
elif st.session_state.page == 'assessment':
    user = st.session_state.user
    
    if not questions_data:
        st.error("No questions loaded!")
        if st.button("← Back"):
            st.session_state.page = 'dashboard'
            st.rerun()
        st.stop()
    
    module_ids = list(questions_data.keys())
    mod_idx = st.session_state.current_module
    
    if mod_idx >= len(module_ids):
        st.success("🎉 All modules completed!")
        if st.button("View Report"):
            st.session_state.page = 'report'
            st.rerun()
        st.stop()
    
    module = questions_data[module_ids[mod_idx]]
    questions = module['questions']
    q_idx = st.session_state.current_q
    
    # Progress
    st.progress((q_idx + 1) / len(questions))
    st.markdown(f"**{module['name']}** - Question {q_idx + 1} of {len(questions)}")
    
    # Show ALL questions as numbered list on top
    cols = st.columns(len(questions))
    for i, col in enumerate(cols):
        with col:
            status = "🔴" if i == q_idx else "🟢" if i in st.session_state.answers else "⚪"
            if st.button(f"{status} {i+1}", key=f"q_{i}"):
                st.session_state.current_q = i
                st.rerun()
    
    # Current question
    q = questions[q_idx]
    st.markdown(f"### {q['question']}")
    
    # Options
    answer = st.radio("Select answer:", q['options'], key=f"opt_{mod_idx}_{q_idx}")
    
    if answer:
        st.session_state.answers[q_idx] = answer
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Prev", disabled=(q_idx == 0)):
            st.session_state.current_q = max(0, q_idx - 1)
            st.rerun()
    with col2:
        if q_idx < len(questions) - 1:
            if st.button("Next →"):
                st.session_state.current_q = q_idx + 1
                st.rerun()
        else:
            if st.button("✅ Submit"):
                # Calculate score
                correct = 0
                for i, q in enumerate(questions):
                    if i in st.session_state.answers:
                        if st.session_state.answers[i] == q['options'][q['correct']]:
                            correct += 1
                
                score = (correct / len(questions)) * 100
                passed = score >= 80
                
                # Save
                data = load_data()
                for u in data:
                    if u['email'] == user['email']:
                        u['attempts'] = u.get('attempts', 0) + 1
                        if passed:
                            u['current_module'] = mod_idx + 1
                            if mod_idx + 1 >= len(module_ids):
                                u['assessment_passed'] = True
                                u['score'] = score
                        break
                save_data(data)
                
                if passed:
                    st.success(f"Passed! {score:.0f}%")
                    st.session_state.current_module = mod_idx + 1
                    st.session_state.current_q = 0
                    st.session_state.answers = {}
                else:
                    st.error(f"Failed! {score:.0f}%")
                    st.session_state.answers = {}
                    st.session_state.current_q = 0
                
                if st.button("Continue"):
                    st.rerun()
    with col3:
        if st.button("Exit"):
            st.session_state.page = 'dashboard'
            st.rerun()

# REPORT CARD
elif st.session_state.page == 'report':
    user = st.session_state.user
    st.markdown("<h2>Report Card</h2>", unsafe_allow_html=True)
    
    if user.get('assessment_passed'):
        st.success(f"🏆 Certified! Score: {user.get('score', 0):.0f}%")
    else:
        st.info("Complete assessment to view certificate")
    
    if st.button("← Back"):
        st.session_state.page = 'dashboard'
        st.rerun()

# ADMIN LOGIN
elif st.session_state.page == 'admin_login':
    st.markdown("<h2>Admin Login</h2>", unsafe_allow_html=True)
    
    with st.form("admin_form"):
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
                    st.session_state.page = 'admin'
                    st.rerun()
                else:
                    st.error("Invalid credentials")

# ADMIN DASHBOARD
elif st.session_state.page == 'admin':
    st.markdown("<h2>Admin Dashboard</h2>", unsafe_allow_html=True)
    
    data = load_data()
    st.metric("Total Employees", len(data))
    
    if data:
        df = pd.DataFrame(data)
        st.dataframe(df[['name', 'email', 'department', 'assessment_passed']], hide_index=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "employees.csv", "text/csv")
    
    if st.button("Logout"):
        st.session_state.page = 'landing'
        st.rerun()
