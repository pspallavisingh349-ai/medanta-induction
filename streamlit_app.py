import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Medanta Induction Portal",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    }
    #MainMenu, footer, header {visibility: hidden;}
    
    .header-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    
    .portal-btn {
        background: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px 0;
        cursor: pointer;
        transition: transform 0.3s;
    }
    
    .portal-btn:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .contact-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 4px solid #e53e3e;
    }
    
    .contact-box.it {border-left-color: #3182ce;}
    .contact-box.salary {border-left-color: #d69e2e;}
    .contact-box.onboard {border-left-color: #38a169;}
    .contact-box.training {
        border-left-color: #805ad5;
        background: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%);
    }
    
    .number {
        color: #e53e3e;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    .number.green {color: #38a169;}
    .number.blue {color: #3182ce;}
    
    @media (max-width: 768px) {
        .header-box {padding: 20px;}
        h1 {font-size: 1.5em !important;}
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

DATA_FILE = "induction_data.json"
QUESTIONS_FILE = "questions.json"

DEFAULT_QUESTIONS = [
    {
        "id": 1,
        "question": "What is the primary mission of Medanta?",
        "options": ["To provide affordable healthcare", "To deliver world-class healthcare", "To maximize profits", "Research only"],
        "correct": 1
    },
    {
        "id": 2,
        "question": "Which is a core value at Medanta?",
        "options": ["Profit first", "Patient centricity", "Cost cutting", "Rapid expansion"],
        "correct": 1
    },
    {
        "id": 3,
        "question": "What does 'Samvaad' represent?",
        "options": ["Medical procedure", "Open communication", "Billing system", "Discharge process"],
        "correct": 1
    }
]

def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, 'r') as f:
            return json.load(f)
    with open(QUESTIONS_FILE, 'w') as f:
        json.dump(DEFAULT_QUESTIONS, f)
    return DEFAULT_QUESTIONS

def save_data(data):
    all_data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            all_data = json.load(f)
    data['timestamp'] = datetime.now().isoformat()
    all_data.append(data)
    with open(DATA_FILE, 'w') as f:
        json.dump(all_data, f)

def calc_score(answers):
    questions = load_questions()
    return sum(1 for q in questions if answers.get(str(q['id'])) == q['correct'])

# Header
st.markdown("""
<div class="header-box">
    <h1>🏥 Namaste! 🙏</h1>
    <h3>Welcome to Medanta Induction Portal</h3>
</div>
""", unsafe_allow_html=True)

# Navigation
if st.session_state.page == 'home':
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✨ New Joinee", use_container_width=True):
            st.session_state.page = 'new'
            st.rerun()
        st.markdown('<div class="portal-btn"><h4>Participant Portal</h4><p>For new employees</p></div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🔐 Returning User", use_container_width=True):
            st.session_state.page = 'return'
            st.rerun()
        st.markdown('<div class="portal-btn"><h4>Administrator Portal</h4><p>For HR & Management</p></div>', unsafe_allow_html=True)
    
    # Contacts
    st.markdown("---")
    st.subheader("📞 Key Contacts")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="contact-box">
            <b>EMR/HIS Query</b><br>
            Mr. Surjendra<br>
            <span class="number">📱 9883111600</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="contact-box salary">
            <b>Salary Related</b><br>
            HR Department<br>
            <span class="number">📱 9560719167</span>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown("""
        <div class="contact-box it">
            <b>IT Helpdesk</b><br>
            Internal Extension<br>
            <span class="number blue">☎️ 1010</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="contact-box onboard">
            <b>Onboarding Query</b><br>
            HR Business Partner<br>
            <span style="color:#38a169;font-weight:600;">Contact your HRBP</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="contact-box training">
        <b>Training Related</b> - Dr. Pallavi & Mr. Rohit<br>
        <span class="number green">📞 7860955988</span> &nbsp;&nbsp;
        <span class="number green">📞 7275181822</span>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == 'new':
    with st.form("reg_form"):
        st.subheader("📝 New Joinee Registration")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *")
            emp_id = st.text_input("Employee ID *")
            dept = st.selectbox("Department *", ["Select", "Nursing", "Medical", "Admin", "HR", "Finance", "IT", "Others"])
        
        with col2:
            email = st.text_input("Email *")
            phone = st.text_input("Phone *")
            desig = st.selectbox("Designation *", ["Select", "Consultant", "Nurse", "Manager", "Executive", "Others"])
        
        st.markdown("---")
        st.subheader("🎯 Assessment")
        
        questions = load_questions()
        answers = {}
        
        for q in questions:
            st.write(f"**Q{q['id']}. {q['question']}**")
            ans = st.radio(f"q_{q['id']}", q['options'], key=f"q_{q['id']}", label_visibility="collapsed")
            if ans:
                answers[str(q['id'])] = q['options'].index(ans)
            st.write("")
        
        col_back, col_sub = st.columns([1, 2])
        with col_back:
            if st.form_submit_button("← Back"):
                st.session_state.page = 'home'
                st.rerun()
        with col_sub:
            submitted = st.form_submit_button("Complete Registration", type="primary")
        
        if submitted:
            if not all([name, emp_id, dept != "Select", email, phone, desig != "Select"]):
                st.error("Fill all required fields!")
            elif len(answers) < len(questions):
                st.error("Answer all questions!")
            else:
                save_data({
                    "name": name, "employee_id": emp_id, "department": dept,
                    "email": email, "phone": phone, "designation": desig,
                    "answers": answers, "score": calc_score(answers)
                })
                st.balloons()
                st.success(f"🎉 Welcome {name}! Score: {calc_score(answers)}/{len(questions)}")
                st.session_state.page = 'home'
                st.rerun()

elif st.session_state.page == 'return':
    st.subheader("🔍 Check Your Status")
    emp_id = st.text_input("Enter Employee ID")
    
    col_back, col_search = st.columns([1, 2])
    with col_back:
        if st.button("← Back"):
            st.session_state.page = 'home'
            st.rerun()
    with col_search:
        if st.button("Search"):
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                records = [u for u in data if u.get('employee_id') == emp_id]
                if records:
                    r = records[-1]
                    st.success(f"Found: {r['name']}")
                    st.write(f"Department: {r['department']} | Score: {r['score']}/3")
                else:
                    st.error("Not found. Register first.")
            else:
                st.error("No data yet.")
