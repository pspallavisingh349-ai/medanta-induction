import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os
import base64

# ============== PAGE CONFIGURATION ==============
st.set_page_config(
    page_title="Medanta New Hire Induction Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============== CUSTOM CSS ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* White Background with Golden Confetti Animation */
    .stApp {
        background: #FFFFFF;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Animated Golden Confetti/Dots Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle, #D4AF37 2px, transparent 2px),
            radial-gradient(circle, #D4AF37 1.5px, transparent 1.5px),
            radial-gradient(circle, #D4AF37 1px, transparent 1px);
        background-size: 50px 50px, 30px 30px, 70px 70px;
        background-position: 0 0, 25px 25px, 15px 60px;
        animation: confettiMove 20s linear infinite;
        pointer-events: none;
        z-index: 0;
        opacity: 0.3;
    }
    
    @keyframes confettiMove {
        0% { transform: translateY(0) rotate(0deg); }
        100% { transform: translateY(-100px) rotate(360deg); }
    }
    
    /* Main Content Container */
    .main-container {
        position: relative;
        z-index: 1;
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Logo Styling */
    .logo-container {
        text-align: center;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .logo-text {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        color: #8B1538;
        font-weight: 700;
        letter-spacing: 3px;
    }
    
    .logo-tagline {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #D4AF37;
        letter-spacing: 2px;
        margin-top: 0.2rem;
    }
    
    /* Headings - Maroon */
    h1, h2, h3, h4, h5, h6 {
        color: #8B1538 !important;
        font-family: 'Playfair Display', serif;
    }
    
    /* Body Text - Black */
    p, span, div, label {
        color: #000000;
        font-family: 'Inter', sans-serif;
    }
    
    /* Compact Cards */
    .compact-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(139, 21, 56, 0.1);
        border: 2px solid #D4AF37;
        margin: 0.5rem 0;
    }
    
    /* Choice Cards */
    .choice-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid #D4AF37;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem;
        transition: all 0.3s;
        cursor: pointer;
    }
    
    .choice-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(139, 21, 56, 0.15);
        border-color: #8B1538;
    }
    
    /* Buttons - Maroon with Gold */
    .stButton>button {
        background: #8B1538;
        color: #FFFFFF;
        border: 2px solid #D4AF37;
        border-radius: 25px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: #A91D3A;
        box-shadow: 0 4px 15px rgba(139, 21, 56, 0.3);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 8px;
        border: 2px solid #D4AF37;
        background: #FFFFFF;
        color: #000000;
        padding: 0.6rem;
        font-size: 0.9rem;
    }
    
    /* Dashboard Grid */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .dashboard-item {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 1.2rem;
        border: 2px solid #D4AF37;
        text-align: center;
        transition: all 0.3s;
    }
    
    .dashboard-item:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(139, 21, 56, 0.15);
    }
    
    .dashboard-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-title {
        color: #8B1538;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.3rem;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(212, 175, 55, 0.1);
        padding: 8px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 8px 16px;
        border: 2px solid transparent;
        color: #000000;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: #8B1538 !important;
        color: #FFFFFF !important;
        border: 2px solid #D4AF37 !important;
    }
    
    /* Progress Circle */
    .progress-circle {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: conic-gradient(#8B1538 var(--progress), #E5E7EB 0deg);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
    }
    
    .progress-inner {
        width: 65px;
        height: 65px;
        border-radius: 50%;
        background: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #8B1538;
        font-size: 0.9rem;
    }
    
    /* Compact Layout Utilities */
    .compact-section {
        margin: 0.5rem 0;
    }
    
    .compact-row {
        display: flex;
        gap: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .logo-text { font-size: 1.8rem; }
        .dashboard-grid { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

# ============== DATA STORAGE ==============
DATA_FILE = "user_data.json"
RESULTS_FILE = "assessment_results.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"users": [], "assessments": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_results(results):
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=4)

def add_user(user_info):
    data = load_data()
    user_info['registration_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_info['user_id'] = f"MED{datetime.now().strftime('%Y%m%d%H%M%S')}"
    data['users'].append(user_info)
    save_data(data)
    return user_info['user_id']

def get_user_by_email(email):
    data = load_data()
    for user in data['users']:
        if user['email'].lower() == email.lower():
            return user
    return None

def get_user_by_employee_id(emp_id):
    data = load_data()
    for user in data['users']:
        if user.get('employee_id') == emp_id:
            return user
    return None

# ============== SESSION STATE ==============
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = 'handbook'

# ============== DEPARTMENT DATA ==============
DEPARTMENT_CATEGORIES = ["Administrative", "Paramedical", "Nursing", "Clinical"]

# ============== QUESTIONS (175) ==============
QUESTIONS = [
    {"id": 1, "category": "Patient Safety", "question": "What is the primary goal of Patient Safety at Medanta?", 
     "options": ["Prevent harm to patients", "Increase revenue", "Reduce staff", "Expand facilities"]},
    {"id": 2, "category": "Patient Safety", "question": "What does SBAR stand for?",
     "options": ["Situation, Background, Assessment, Recommendation", "Standard, Basic, Advanced, Review", "Safety, Benefits, Assessment, Results", "System, Background, Analysis, Report"]},
    {"id": 3, "category": "Patient Safety", "question": "What is the correct hand hygiene duration?",
     "options": ["40-60 seconds", "10-15 seconds", "20-30 seconds", "5-10 seconds"]},
    {"id": 4, "category": "Patient Safety", "question": "What color code indicates a fire emergency?",
     "options": ["Code Red", "Code Blue", "Code Pink", "Code Yellow"]},
    {"id": 5, "category": "Patient Safety", "question": "What is the most common cause of medication errors?",
     "options": ["Communication failure", "Equipment malfunction", "Staff shortage", "Patient non-compliance"]},
]

while len(QUESTIONS) < 175:
    idx = len(QUESTIONS) + 1
    cat = "Department Specific" if idx > 140 else "General"
    QUESTIONS.append({
        "id": idx,
        "category": cat,
        "question": f"Question {idx}: Standard Medanta protocol compliance?",
        "options": ["Follow standard protocol", "Ignore protocol", "Modify as needed", "Ask colleague"]
    })

CORRECT_ANSWERS = {1: "Prevent harm to patients", 2: "Situation, Background, Assessment, Recommendation", 
                   3: "40-60 seconds", 4: "Code Red", 5: "Communication failure"}
for i in range(6, 176):
    if i not in CORRECT_ANSWERS:
        CORRECT_ANSWERS[i] = "Follow standard protocol"

# ============== FUNCTIONS ==============
def calculate_score():
    correct = 0
    total = len(QUESTIONS)
    for q in QUESTIONS:
        q_id = q['id']
        user_answer = st.session_state.answers.get(q_id, "")
        if user_answer == CORRECT_ANSWERS.get(q_id, ""):
            correct += 1
    return correct, total, (correct/total)*100

def save_assessment_result(user_info):
    correct, total, percentage = calculate_score()
    result_data = {
        "result_id": f"RES{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "user_id": user_info.get('user_id', 'Unknown'),
        "employee_id": user_info.get('employee_id', 'N/A'),
        "name": user_info.get('name', 'Unknown'),
        "email": user_info.get('email', 'Unknown'),
        "department_category": user_info.get('department_category', 'Unknown'),
        "sub_department": user_info.get('sub_department', 'Unknown'),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": correct,
        "total": total,
        "percentage": round(percentage, 2),
        "answers": st.session_state.answers,
        "status": "Passed" if percentage >= 70 else "Failed"
    }
    
    all_results = load_results()
    all_results.append(result_data)
    save_results(all_results)
    
    data = load_data()
    for user in data['users']:
        if user.get('email') == user_info.get('email'):
            if 'assessments' not in user:
                user['assessments'] = []
            user['assessments'].append(result_data)
            break
    save_data(data)
    
    return result_data

def get_user_progress(user_email):
    data = load_data()
    for user in data['users']:
        if user.get('email') == user_email:
            assessments = user.get('assessments', [])
            if assessments:
                latest = assessments[-1]
                return latest['percentage'], len(assessments)
    return 0, 0

# ============== PAGES ==============
def show_logo():
    st.markdown("""
    <div class="logo-container">
        <div class="logo-text">🏥 MEDANTA</div>
        <div class="logo-tagline">THE MEDICITY</div>
    </div>
    """, unsafe_allow_html=True)

def show_landing():
    show_logo()
    
    st.markdown("""
    <h1 style="text-align: center; color: #8B1538; font-family: Playfair Display, serif; font-size: 2rem; margin-bottom: 0.5rem;">
        🙏 Namaste
    </h1>
    <p style="text-align: center; color: #000000; font-size: 1rem; margin-bottom: 1.5rem;">
        Welcome to New Hire Induction Portal
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="choice-card">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🆕</div>
            <div style="color: #8B1538; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.3rem;">New Hire</div>
            <div style="color: #000000; font-size: 0.85rem;">First time here? Register now</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Register", key="new_hire_btn", use_container_width=True):
            st.session_state.user_type = 'new'
            st.session_state.page = 'registration'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="choice-card">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">👤</div>
            <div style="color: #8B1538; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.3rem;">Returning Employee</div>
            <div style="color: #000000; font-size: 0.85rem;">Already registered? Login</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Login", key="returning_btn", use_container_width=True):
            st.session_state.user_type = 'returning'
            st.session_state.page = 'returning_login'
            st.rerun()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔐 Admin Portal", use_container_width=True):
            st.session_state.page = 'admin_login'
            st.rerun()

def show_registration():
    show_logo()
    st.markdown('<h2 style="color: #8B1538; text-align: center; font-size: 1.5rem; margin-bottom: 1rem;">📝 New Hire Registration</h2>', unsafe_allow_html=True)
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name *", placeholder="Full Name")
            mobile = st.text_input("Mobile No *", placeholder="+91-XXXXXXXXXX")
        with col2:
            email = st.text_input("Email Address *", placeholder="email@example.com")
            employee_id = st.text_input("Employee ID (if allotted)", placeholder="MED2024001")
        
        col1, col2 = st.columns(2)
        with col1:
            dept_category = st.selectbox("Department Category *", ["Select"] + DEPARTMENT_CATEGORIES)
        with col2:
            sub_department = st.text_input("Sub Department *", placeholder="e.g., Cardiology, HR, etc.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.form_submit_button("← Back"):
                st.session_state.page = 'landing'
                st.rerun()
        with col3:
            submitted = st.form_submit_button("Register →")
            if submitted:
                if name and email and mobile and dept_category != "Select" and sub_department:
                    existing_user = get_user_by_email(email)
                    if existing_user:
                        st.error("Email already registered!")
                    else:
                        user_info = {
                            'name': name,
                            'email': email,
                            'mobile': mobile,
                            'employee_id': employee_id if employee_id else "Pending",
                            'department_category': dept_category,
                            'sub_department': sub_department,
                        }
                        user_id = add_user(user_info)
                        user_info['user_id'] = user_id
                        st.session_state.user = user_info
                        st.session_state.page = 'employee_dashboard'
                        st.rerun()
                else:
                    st.error("Fill all required fields!")

def show_returning_login():
    show_logo()
    st.markdown('<h2 style="color: #8B1538; text-align: center; font-size: 1.5rem; margin-bottom: 1rem;">👤 Returning Employee Login</h2>', unsafe_allow_html=True)
    
    login_method = st.radio("Login using:", ["Email Address", "Employee ID"], horizontal=True)
    
    if login_method == "Email Address":
        email = st.text_input("Email Address", placeholder="your.email@example.com")
    else:
        emp_id = st.text_input("Employee ID", placeholder="MED2024001")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()
    with col3:
        if st.button("Login →", use_container_width=True):
            if login_method == "Email Address":
                user = get_user_by_email(email) if email else None
            else:
                user = get_user_by_employee_id(emp_id) if emp_id else None
            
            if user:
                st.session_state.user = user
                st.session_state.page = 'employee_dashboard'
                st.rerun()
            else:
                st.error("User not found!")

def show_employee_dashboard():
    user = st.session_state.user
    progress, attempts = get_user_progress(user.get('email', ''))
    
    show_logo()
    
    # Welcome & Progress
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f'<h2 style="color: #8B1538; font-size: 1.3rem; margin: 0;">👋 Welcome, {user["name"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #000000; font-size: 0.85rem; margin: 0;">{user.get("sub_department", "N/A")} | {user.get("department_category", "N/A")}</p>', unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="text-align: right;">
            <div style="display: inline-block; text-align: center;">
                <div style="width: 60px; height: 60px; border-radius: 50%; background: conic-gradient(#8B1538 {progress*3.6}deg, #E5E7EB 0deg); display: flex; align-items: center; justify-content: center; margin: 0 auto;">
                    <div style="width: 50px; height: 50px; border-radius: 50%; background: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #8B1538; font-size: 0.8rem;">
                        {progress:.0f}%
                    </div>
                </div>
                <p style="font-size: 0.7rem; color: #000000; margin: 0.2rem 0 0 0;">Progress</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Dashboard Grid
    st.markdown('<h3 style="color: #8B1538; font-size: 1.1rem; margin-bottom: 0.8rem;">📚 Learning Resources</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="dashboard-item" style="cursor: pointer;">
            <div class="dashboard-icon">📖</div>
            <div class="dashboard-title">Employee Handbook</div>
            <div style="color: #000000; font-size: 0.8rem;">View digital handbook</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Handbook", key="handbook_btn", use_container_width=True):
            st.session_state.current_tab = 'handbook'
            st.session_state.page = 'resources'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="dashboard-item" style="cursor: pointer;">
            <div class="dashboard-icon">🏥</div>
            <div class="dashboard-title">JCI Handbook</div>
            <div style="color: #000000; font-size: 0.8rem;">Joint Commission standards</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open JCI Handbook", key="jci_btn", use_container_width=True):
            st.session_state.current_tab = 'jci'
            st.session_state.page = 'resources'
            st.rerun()
    
    st.markdown('<h3 style="color: #8B1538; font-size: 1.1rem; margin: 1rem 0 0.8rem 0;">🎯 Assessment</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="dashboard-item" style="cursor: pointer;">
            <div class="dashboard-icon">📝</div>
            <div class="dashboard-title">Take Assessment</div>
            <div style="color: #000000; font-size: 0.8rem;">175 questions | 70% to pass</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Assessment", key="assessment_btn", use_container_width=True):
            st.session_state.answers = {}
            st.session_state.current_question = 0
            st.session_state.submitted = False
            st.session_state.page = 'assessment'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="dashboard-item" style="cursor: pointer;">
            <div class="dashboard-icon">📊</div>
            <div class="dashboard-title">Report Card</div>
            <div style="color: #000000; font-size: 0.8rem;">View results & certificate</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Report", key="report_btn", use_container_width=True):
            st.session_state.page = 'report_card'
            st.rerun()
    
    # Progress Report Section
    st.markdown('<h3 style="color: #8B1538; font-size: 1.1rem; margin: 1rem 0 0.8rem 0;">📈 Progress Report</h3>', unsafe_allow_html=True)
    
    data = load_data()
    user_assessments = []
    for u in data['users']:
        if u.get('email') == user.get('email'):
            user_assessments = u.get('assessments', [])
            break
    
    if user_assessments:
        latest = user_assessments[-1]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Attempts", len(user_assessments))
        with col2:
            st.metric("Latest Score", f"{latest['percentage']:.1f}%")
        with col3:
            st.metric("Status", latest['status'])
        with col4:
            st.metric("Best Score", f"{max(a['percentage'] for a in user_assessments):.1f}%")
    else:
        st.info("No assessments taken yet. Start your first assessment!")
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.page = 'landing'
        st.rerun()

def show_resources():
    user = st.session_state.user
    
    show_logo()
    
    # Back button
    if st.button("← Back to Dashboard", use_container_width=True):
        st.session_state.page = 'employee_dashboard'
        st.rerun()
    
    # Tabs for different handbooks
    tabs = st.tabs(["📖 Employee Handbook", "🏥 JCI Handbook"])
    
    with tabs[0]:
        st.markdown('<h2 style="color: #8B1538; font-size: 1.3rem;">Employee Handbook</h2>', unsafe_allow_html=True)
        
        # Flipping Book Embed
        flipping_book_url = "https://online.flippingbook.com/view/652486186/"
        
        st.markdown(f"""
        <div style="border: 3px solid #D4AF37; border-radius: 10px; overflow: hidden; margin: 1rem 0;">
            <iframe src="{flipping_book_url}" 
                    style="width: 100%; height: 600px; border: none;" 
                    allowfullscreen>
            </iframe>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("💡 **Tip:** Use the arrow buttons in the book viewer to navigate pages. You can also zoom and search within the document.")
        
        # Quick Links
        st.markdown('<h4 style="color: #8B1538; font-size: 1rem; margin-top: 1rem;">Quick Links</h4>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("[📋 Policies](#)")
        with col2:
            st.markdown("[👔 Dress Code](#)")
        with col3:
            st.markdown("[⚠️ Safety](#)")
    
    with tabs[1]:
        st.markdown('<h2 style="color: #8B1538; font-size: 1.3rem;">JCI Handbook</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: #FFFFFF; padding: 2rem; border-radius: 10px; border: 2px solid #D4AF37; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🏥</div>
            <h3 style="color: #8B1538;">Joint Commission International Standards</h3>
            <p style="color: #000000;">JCI accreditation standards for patient safety and quality of care.</p>
            <p style="color: #6B7280; font-size: 0.9rem;">Content loading... Please contact HR for the JCI handbook.</p>
        </div>
        """, unsafe_allow_html=True)

def show_assessment():
    if st.session_state.submitted:
        show_report_card()
        return
    
    user = st.session_state.user
    show_logo()
    
    total_questions = len(QUESTIONS)
    current = st.session_state.current_question + 1
    progress_percent = (current / total_questions) * 100
    
    # Progress Bar
    st.progress(progress_percent / 100)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f'<p style="color: #000000; font-size: 0.9rem; margin: 0;">Question {current} of {total_questions}</p>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<p style="color: #8B1538; font-size: 0.9rem; margin: 0; text-align: right;">{progress_percent:.1f}% Complete</p>', unsafe_allow_html=True)
    
    q = QUESTIONS[st.session_state.current_question]
    
    st.markdown(f'<p style="color: #D4AF37; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin: 0.5rem 0 0.2rem 0;">{q["category"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color: #000000; font-size: 1.1rem; margin-bottom: 1rem;">{q["id"]}. {q["question"]}</h3>', unsafe_allow_html=True)
    
    selected_option = st.radio("Select your answer:", q['options'], key=f"q_{q['id']}", index=None)
    
    if selected_option:
        st.session_state.answers[q['id']] = selected_option
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.current_question > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    with col2:
        if st.button("Save & Exit", use_container_width=True):
            st.session_state.page = 'employee_dashboard'
            st.rerun()
    with col3:
        if st.session_state.current_question < total_questions - 1:
            if st.button("Next →", use_container_width=True):
                if q['id'] in st.session_state.answers:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    st.warning("Select an answer!")
        else:
            if st.button("Submit ✓", use_container_width=True):
                if q['id'] in st.session_state.answers:
                    st.session_state.submitted = True
                    save_assessment_result(st.session_state.user)
                    st.rerun()
                else:
                    st.warning("Select an answer!")

def show_report_card():
    correct, total, percentage = calculate_score()
    user = st.session_state.user
    
    show_logo()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        status_color = "#10B981" if percentage >= 70 else "#EF4444"
        status_text = "PASSED" if percentage >= 70 else "FAILED"
        
        st.markdown(f"""
        <div style="background: #FFFFFF; padding: 1.5rem; border-radius: 15px; border: 3px solid #D4AF37; text-align: center; margin-bottom: 1rem;">
            <div style="width: 100px; height: 100px; border-radius: 50%; background: conic-gradient(#8B1538 {percentage*3.6}deg, #E5E7EB 0deg); margin: 0 auto; display: flex; align-items: center; justify-content: center;">
                <div style="width: 85px; height: 85px; border-radius: 50%; background: #FFFFFF; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 1.5rem; font-weight: bold; color: #8B1538;">{percentage:.0f}%</span>
                </div>
            </div>
            <h2 style="color: #8B1538; margin: 0.5rem 0; font-size: 1.3rem;">{user['name']}</h2>
            <p style="color: #000000; margin: 0; font-size: 0.9rem;">{user.get('sub_department', 'N/A')}</p>
            <div style="margin-top: 0.8rem; padding: 0.5rem; background: {status_color}20; border-radius: 8px; border: 2px solid {status_color};">
                <span style="color: {status_color}; font-weight: 700; font-size: 1.1rem;">{status_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total", total)
    with col2:
        st.metric("Correct", correct)
    with col3:
        st.metric("Wrong", total - correct)
    with col4:
        st.metric("Score", f"{percentage:.1f}%")
    
    if percentage >= 70:
        st.success("🎉 Congratulations! Download your certificate below.")
        
        cert_text = f"""
CERTIFICATE OF COMPLETION
----------------------------
This certifies that

{user['name']}

has successfully completed the
Medanta New Hire Induction Program

Employee ID: {user.get('employee_id', 'N/A')}
Department: {user.get('sub_department', 'N/A')}
Score: {percentage:.1f}%
Date: {datetime.now().strftime("%B %d, %Y")}
Certificate ID: CERT{datetime.now().strftime('%Y%m%d%H%M%S')}
"""
        st.download_button("📥 Download Certificate", cert_text, 
                          f"Medanta_Certificate_{user.get('employee_id', 'User')}.txt", 
                          use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.page = 'employee_dashboard'
            st.session_state.submitted = False
            st.session_state.current_question = 0
            st.rerun()
    with col2:
        if percentage < 70:
            if st.button("🔄 Retake Assessment", use_container_width=True):
                st.session_state.answers = {}
                st.session_state.submitted = False
                st.session_state.current_question = 0
                st.session_state.page = 'assessment'
                st.rerun()

def show_admin_login():
    show_logo()
    st.markdown('<h2 style="color: #8B1538; text-align: center; font-size: 1.5rem; margin-bottom: 1rem;">🔐 Admin Portal</h2>', unsafe_allow_html=True)
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()
    with col3:
        if st.button("Login", use_container_width=True):
            if username == "admin" and password == "medanta2024":
                st.session_state.admin_authenticated = True
                st.session_state.page = 'admin_dashboard'
                st.rerun()
            else:
                st.error("Invalid credentials!")

def show_admin_dashboard():
    if not st.session_state.admin_authenticated:
        st.session_state.page = 'admin_login'
        st.rerun()
        return
    
    show_logo()
    st.markdown('<h2 style="color: #8B1538; text-align: center; font-size: 1.5rem; margin-bottom: 1rem;">📊 Admin Dashboard</h2>', unsafe_allow_html=True)
    
    data = load_data()
    results = load_results()
    
    total_users = len(data['users'])
    total_assessments = len(results)
    passed = sum(1 for r in results if r['status'] == "Passed")
    avg_score = sum(r['percentage'] for r in results) / total_assessments if total_assessments > 0 else 0
    
    # Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("Total Users", total_users, "👥"),
        ("Assessments", total_assessments, "📝"),
        ("Pass Rate", f"{(passed/total_assessments*100):.0f}%" if total_assessments > 0 else "0%", "✅"),
        ("Avg Score", f"{avg_score:.1f}%", "📊")
    ]
    for i, (label, value, icon) in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div style="background: #FFFFFF; padding: 1rem; border-radius: 10px; border: 2px solid #D4AF37; text-align: center;">
                <div style="font-size: 1.5rem; margin-bottom: 0.2rem;">{icon}</div>
                <div style="color: #8B1538; font-weight: 700; font-size: 1.1rem;">{value}</div>
                <div style="color: #000000; font-size: 0.75rem;">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tabs
    tabs = st.tabs(["📋 Employees", "📊 Reports", "📈 Analytics"])
    
    with tabs[0]:
        if data['users']:
            users_df = pd.DataFrame(data['users'])
            st.dataframe(users_df[['user_id', 'name', 'email', 'employee_id', 'department_category', 'sub_department', 'registration_date']], use_container_width=True)
            csv = users_df.to_csv(index=False)
            st.download_button("📥 Export CSV", csv, f"employees_{datetime.now().strftime('%Y%m%d')}.csv")
        else:
            st.info("No employees registered.")
    
    with tabs[1]:
        if results:
            results_df = pd.DataFrame(results)
            st.dataframe(results_df[['date', 'name', 'employee_id', 'department_category', 'score', 'total', 'percentage', 'status']], use_container_width=True)
            csv = results_df.to_csv(index=False)
            st.download_button("📥 Export Results", csv, f"results_{datetime.now().strftime('%Y%m%d')}.csv")
        else:
            st.info("No assessment results.")
    
    with tabs[2]:
        if results:
            results_df = pd.DataFrame(results)
            dept_stats = results_df.groupby('department_category')['percentage'].mean().reset_index()
            st.bar_chart(dept_stats.set_index('department_category'))
            
            st.markdown("### Department Performance")
            for _, row in dept_stats.iterrows():
                st.markdown(f"**{row['department_category']}:** {row['percentage']:.1f}%")
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.session_state.page = 'landing'
        st.rerun()

# ============== MAIN ==============
def main():
    pages = {
        'landing': show_landing,
        'registration': show_registration,
        'returning_login': show_returning_login,
        'employee_dashboard': show_employee_dashboard,
        'resources': show_resources,
        'assessment': show_assessment,
        'report_card': show_report_card,
        'admin_login': show_admin_login,
        'admin_dashboard': show_admin_dashboard
    }
    
    current_page = st.session_state.get('page', 'landing')
    pages.get(current_page, show_landing)()

if __name__ == "__main__":
    main()
