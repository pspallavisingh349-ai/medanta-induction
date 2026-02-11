import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Medanta Induction Portal",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for aesthetic design and mobile responsiveness
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main container */
    .main-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Header Section */
    .header-section {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .header-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        opacity: 0.3;
    }
    
    .logo-container {
        position: relative;
        z-index: 1;
        margin-bottom: 20px;
    }
    
    .logo-img {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: white;
        padding: 10px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        border: 4px solid rgba(255,255,255,0.3);
        animation: float 3s ease-in-out infinite;
    }
    
    .welcome-text {
        color: white;
        font-size: 2.5em;
        font-weight: 700;
        margin: 10px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2em;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    /* Portal Cards */
    .portal-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin: 30px 0;
    }
    
    .portal-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 2px solid transparent;
        cursor: pointer;
    }
    
    .portal-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.12);
        border-color: #667eea;
    }
    
    .portal-icon {
        font-size: 3em;
        margin-bottom: 15px;
    }
    
    .portal-title {
        font-size: 1.4em;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 8px;
    }
    
    .portal-desc {
        color: #718096;
        font-size: 0.95em;
    }
    
    /* Contact Section */
    .contact-section {
        background: white;
        border-radius: 20px;
        padding: 30px;
        margin-top: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    }
    
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.3em;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .section-icon {
        color: #e53e3e;
        font-size: 1.2em;
    }
    
    .contact-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
    }
    
    .contact-card {
        background: #f7fafc;
        border-radius: 15px;
        padding: 20px;
        border-left: 4px solid;
        transition: all 0.3s ease;
    }
    
    .contact-card:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    
    .contact-card.emr { border-left-color: #e53e3e; }
    .contact-card.it { border-left-color: #3182ce; }
    .contact-card.salary { border-left-color: #d69e2e; }
    .contact-card.onboarding { border-left-color: #38a169; }
    .contact-card.training { 
        border-left-color: #805ad5; 
        background: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%);
        grid-column: 1 / -1;
    }
    
    .contact-label {
        font-size: 0.85em;
        font-weight: 600;
        color: #4a5568;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }
    
    .contact-person {
        font-size: 1.1em;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 8px;
    }
    
    .contact-number {
        font-size: 1.3em;
        font-weight: 700;
        color: #e53e3e;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .contact-number.green {
        color: #38a169;
    }
    
    .contact-number.blue {
        color: #3182ce;
    }
    
    .phone-icon {
        font-size: 0.9em;
    }
    
    .hrbp-text {
        color: #38a169;
        font-weight: 600;
        font-size: 1.1em;
    }
    
    /* Animations */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255,255,255,0.8);
        padding: 10px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102,126,234,0.4);
    }
    
    /* Form styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 12px 16px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        padding: 14px 24px;
        font-size: 16px;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102,126,234,0.4);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .welcome-text { font-size: 1.8em; }
        .subtitle { font-size: 1em; }
        .header-section { padding: 30px 15px; }
        .portal-grid { grid-template-columns: 1fr; }
        .contact-grid { grid-template-columns: 1fr; }
        .main-container { padding: 10px; }
        .stTabs [data-baseweb="tab-list"] { flex-direction: column; }
    }
    
    /* Success message */
    .success-box {
        background: linear-gradient(135deg, #48bb78, #38a169);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(72,187,120,0.3);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: #f7fafc;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stRadio > div:hover {
        border-color: #667eea;
        background: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Data files
DATA_FILE = "induction_data.json"
QUESTIONS_FILE = "questions.json"

# Default questions
DEFAULT_QUESTIONS = [
    {
        "id": 1,
        "question": "What is the primary mission of Medanta?",
        "options": [
            "To provide affordable healthcare to all",
            "To deliver world-class healthcare with a patient-first approach",
            "To maximize profits while providing care",
            "To focus only on research and development"
        ],
        "correct": 1
    },
    {
        "id": 2,
        "question": "Which of the following is a core value at Medanta?",
        "options": [
            "Profit maximization",
            "Patient centricity and clinical excellence",
            "Cost cutting at all costs",
            "Rapid expansion over quality"
        ],
        "correct": 1
    },
    {
        "id": 3,
        "question": "What does 'Samvaad' represent in Medanta's culture?",
        "options": [
            "A type of medical procedure",
            "Open communication and dialogue",
            "A billing system",
            "A patient discharge process"
        ],
        "correct": 1
    }
]

def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, 'r') as f:
            return json.load(f)
    else:
        with open(QUESTIONS_FILE, 'w') as f:
            json.dump(DEFAULT_QUESTIONS, f, indent=2)
        return DEFAULT_QUESTIONS

def save_user_data(data):
    all_data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            all_data = json.load(f)
    
    data['timestamp'] = datetime.now().isoformat()
    data['score'] = calculate_score(data.get('answers', {}))
    all_data.append(data)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(all_data, f, indent=2)

def calculate_score(answers):
    questions = load_questions()
    score = 0
    for q in questions:
        if answers.get(str(q['id'])) == q['correct']:
            score += 1
    return score

def show_header():
    st.markdown("""
    <div class="header-section animate-in">
        <div class="logo-container">
            <img src="https://www.medanta.org/images/medanta-logo.png" 
                 onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI0NSIgZmlsbD0id2hpdGUiLz48dGV4dCB4PSI1MCIgeT0iNTUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxMiIgZmlsbD0iIzY2N2VlYSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+TWVkYW50YTwvdGV4dD48L3N2Zz4='"
                 class="logo-img" alt="Medanta Logo">
        </div>
        <h1 class="welcome-text">Namaste! 🙏</h1>
        <p class="subtitle">Welcome to Medanta Induction Portal</p>
    </div>
    """, unsafe_allow_html=True)

def show_portal_cards():
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👤 New Joinee", use_container_width=True, key="new_joinee_btn"):
            st.session_state.page = 'new_joinee'
            st.rerun()
        st.markdown("""
        <div class="portal-card" style="margin-top: -60px; pointer-events: none;">
            <div class="portal-icon">✨</div>
            <div class="portal-title">Participant Portal</div>
            <div class="portal-desc">For new employees joining Medanta</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🔐 Returning User", use_container_width=True, key="returning_btn"):
            st.session_state.page = 'returning'
            st.rerun()
        st.markdown("""
        <div class="portal-card" style="margin-top: -60px; pointer-events: none;">
            <div class="portal-icon">🎯</div>
            <div class="portal-title">Administrator Portal</div>
            <div class="portal-desc">For HR, Trainers & Management</div>
        </div>
        """, unsafe_allow_html=True)

def show_contact_section():
    st.markdown("""
    <div class="contact-section animate-in">
        <div class="section-title">
            <span class="section-icon">📞</span>
            Key Contacts
        </div>
        <div class="contact-grid">
            <div class="contact-card emr">
                <div class="contact-label">EMR/HIS Query</div>
                <div class="contact-person">Mr. Surjendra</div>
                <div class="contact-number">
                    <span class="phone-icon">📱</span>
                    9883111600
                </div>
            </div>
            
            <div class="contact-card it">
                <div class="contact-label">IT Helpdesk</div>
                <div class="contact-person">Internal Extension</div>
                <div class="contact-number blue">
                    <span class="phone-icon">☎️</span>
                    1010
                </div>
            </div>
            
            <div class="contact-card salary">
                <div class="contact-label">Salary Related</div>
                <div class="contact-person">HR Department</div>
                <div class="contact-number">
                    <span class="phone-icon">📱</span>
                    9560719167
                </div>
            </div>
            
            <div class="contact-card onboarding">
                <div class="contact-label">Onboarding Query</div>
                <div class="contact-person">HR Business Partner</div>
                <div class="hrbp-text">Contact your HRBP</div>
            </div>
            
            <div class="contact-card training">
                <div class="contact-label">Training Related</div>
                <div class="contact-person">Dr. Pallavi & Mr. Rohit</div>
                <div style="display: flex; gap: 20px; margin-top: 10px;">
                    <div class="contact-number green">
                        <span class="phone-icon">📞</span>
                        7860955988
                    </div>
                    <div class="contact-number green">
                        <span class="phone-icon">📞</span>
                        7275181822
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_new_joinee_form():
    st.markdown('<div class="animate-in">', unsafe_allow_html=True)
    
    with st.form("registration_form"):
        st.subheader("📝 New Joinee Registration")
        
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name *", placeholder="Enter your full name")
            emp_id = st.text_input("Employee ID *", placeholder="e.g., MED12345")
            dept = st.selectbox("Department *", 
                ["Select", "Nursing", "Medical Services", "Administration", 
                 "HR", "Finance", "Operations", "IT", "Others"])
        
        with col2:
            email = st.text_input("Email *", placeholder="your.email@medanta.org")
            phone = st.text_input("Phone *", placeholder="+91 XXXXX XXXXX")
            desig = st.selectbox("Designation *",
                ["Select", "Consultant", "Nurse", "Resident", "Intern",
                 "Manager", "Executive", "Technician", "Others"])
        
        st.markdown("---")
        st.subheader("🎯 Assessment")
        
        questions = load_questions()
        answers = {}
        
        for i, q in enumerate(questions, 1):
            st.markdown(f"**Q{i}. {q['question']}**")
            ans = st.radio(
                f"q_{q['id']}",
                options=q['options'],
                index=None,
                key=f"question_{q['id']}",
                label_visibility="collapsed"
            )
            if ans:
                answers[str(q['id'])] = q['options'].index(ans)
            st.markdown("---")
        
        col_back, col_submit = st.columns([1, 2])
        with col_back:
            if st.form_submit_button("← Back", type="secondary"):
                st.session_state.page = 'home'
                st.rerun()
        
        with col_submit:
            submitted = st.form_submit_button("Complete Registration", type="primary")
        
        if submitted:
            if not all([full_name, emp_id, dept != "Select", email, phone, desig != "Select"]):
                st.error("Please fill all required fields!")
            elif len(answers) < len(questions):
                st.error("Please answer all questions!")
            else:
                user_data = {
                    "name": full_name,
                    "employee_id": emp_id,
                    "department": dept,
                    "email": email,
                    "phone": phone,
                    "designation": desig,
                    "answers": answers,
                    "type": "new_joinee"
                }
                save_user_data(user_data)
                score = calculate_score(answers)
                
                st.balloons()
                st.markdown(f"""
                <div class="success-box">
                    <h3>🎉 Welcome to Medanta, {full_name}!</h3>
                    <p>Your Score: {score}/{len(questions)}</p>
                    <p>We wish you a wonderful journey ahead! 🚀</p>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.page = 'home'
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_returning_user():
    st.markdown('<div class="animate-in">', unsafe_allow_html=True)
    
    st.subheader("🔍 Check Your Status")
    
    emp_id = st.text_input("Enter Employee ID", placeholder="e.g., MED12345")
    
    col_back, col_search = st.columns([1, 2])
    
    with col_back:
        if st.button("← Back", key="back_btn"):
            st.session_state.page = 'home'
            st.rerun()
    
    with col_search:
        if st.button("Search", key="search_btn"):
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                
                records = [u for u in data if u.get('employee_id') == emp_id]
                
                if records:
                    latest = records[-1]
                    score = latest.get('score', 0)
                    total = len(load_questions())
                    
                    st.success(f"Found: **{latest['name']}**")
                    
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Department", latest['department'])
                    c2.metric("Designation", latest['designation'])
                    c3.metric("Score", f"{score}/{total}")
                    
                    st.progress(score/total if total > 0 else 0)
                    st.caption(f"Last updated: {latest['timestamp'][:10]}")
                else:
                    st.error("No records found. Please register first.")
            else:
                st.error("No data available.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    show_header()
    
    if st.session_state.page == 'home':
        show_portal_cards()
        show_contact_section()
    elif st.session_state.page == 'new_joinee':
        show_new_joinee_form()
    elif st.session_state.page == 'returning':
        show_returning_user()

if __name__ == "__main__":
    main()
