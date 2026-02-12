import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

# ============== PAGE CONFIGURATION ==============
st.set_page_config(
    page_title="Medanta - New Hire Induction",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============== PROFESSIONAL CSS ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Montserrat:wght@300;400;500;600&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Clean White Background with Subtle Gold Pattern */
    .stApp {
        background-color: #FAFAFA;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(212, 175, 55, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(139, 21, 56, 0.02) 0%, transparent 50%);
    }
    
    /* Main Container */
    .main .block-container {
        max-width: 800px;
        padding: 2rem;
        background: #FFFFFF;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border-radius: 0;
        margin: 2rem auto;
        border-top: 4px solid #8B1538;
    }
    
    /* Professional Logo */
    .logo-container {
        text-align: center;
        padding: 1.5rem 0;
        border-bottom: 1px solid #E5E5E5;
        margin-bottom: 2rem;
    }
    
    .logo-main {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #8B1538;
        letter-spacing: 8px;
        text-transform: uppercase;
        margin: 0;
        line-height: 1;
    }
    
    .logo-sub {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.65rem;
        color: #D4AF37;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-top: 0.3rem;
        font-weight: 500;
    }
    
    /* Elegant Headings */
    h1 {
        font-family: 'Cormorant Garamond', serif !important;
        font-size: 2rem !important;
        color: #1A1A1A !important;
        font-weight: 600 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        letter-spacing: 1px;
    }
    
    h2, h3 {
        font-family: 'Cormorant Garamond', serif !important;
        color: #8B1538 !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem !important;
    }
    
    /* Body Text */
    p, div, span, label {
        font-family: 'Montserrat', sans-serif;
        color: #333333;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #666666;
        font-size: 0.85rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Divider */
    .elegant-divider {
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, #8B1538, #D4AF37);
        margin: 1.5rem auto;
    }
    
    /* Cards - Professional */
    .portal-card {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .portal-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: #8B1538;
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .portal-card:hover::before {
        transform: scaleX(1);
    }
    
    .portal-card:hover {
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
        border-color: #D4AF37;
    }
    
    .card-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
        color: #8B1538;
    }
    
    .card-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.3rem;
        color: #1A1A1A;
        font-weight: 600;
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
    }
    
    .card-desc {
        color: #666666;
        font-size: 0.8rem;
        font-weight: 400;
    }
    
    /* Buttons - Professional */
    .stButton>button {
        background: #8B1538;
        color: #FFFFFF;
        border: none;
        border-radius: 0;
        padding: 0.9rem 2rem;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: #6B1029;
        box-shadow: 0 4px 15px rgba(139, 21, 56, 0.3);
    }
    
    /* Secondary Button */
    .secondary-btn {
        background: transparent !important;
        color: #8B1538 !important;
        border: 1px solid #8B1538 !important;
    }
    
    .secondary-btn:hover {
        background: #8B1538 !important;
        color: #FFFFFF !important;
    }
    
    /* Form Inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 0;
        border: 1px solid #CCCCCC;
        background: #FFFFFF;
        color: #333333;
        padding: 0.8rem;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.85rem;
        transition: border-color 0.3s;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #8B1538;
        box-shadow: none;
    }
    
    /* Labels */
    .stTextInput label, .stSelectbox label {
        font-family: 'Montserrat', sans-serif !important;
        color: #555555 !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Dashboard Items */
    .dashboard-item {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .dashboard-item:hover {
        border-color: #8B1538;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    
    .dashboard-icon {
        font-size: 1.8rem;
        color: #8B1538;
        margin-bottom: 0.8rem;
    }
    
    .dashboard-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
        color: #1A1A1A;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    
    .dashboard-desc {
        color: #888888;
        font-size: 0.75rem;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #8B1538, #D4AF37);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid #E0E0E0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 0;
        padding: 1rem 1.5rem;
        border: none;
        border-bottom: 2px solid transparent;
        color: #666666;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.8rem;
        font-weight: 500;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #8B1538 !important;
        border-bottom: 2px solid #8B1538 !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        padding: 1.2rem;
        text-align: center;
    }
    
    .metric-value {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2rem;
        color: #8B1538;
        font-weight: 700;
    }
    
    .metric-label {
        color: #888888;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.3rem;
    }
    
    /* Report Card */
    .score-display {
        text-align: center;
        padding: 2rem;
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        margin-bottom: 1.5rem;
    }
    
    .score-value {
        font-family: 'Cormorant Garamond', serif;
        font-size: 4rem;
        color: #8B1538;
        font-weight: 700;
        line-height: 1;
    }
    
    .score-label {
        color: #888888;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5rem;
    }
    
    /* Status Badge */
    .status-pass {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: #E8F5E9;
        color: #2E7D32;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        border: 1px solid #2E7D32;
    }
    
    .status-fail {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: #FFEBEE;
        color: #C62828;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        border: 1px solid #C62828;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Responsive */
    @media (max-width: 768px) {
        .main .block-container {
            margin: 0;
            border-radius: 0;
        }
        .logo-main { font-size: 1.8rem; letter-spacing: 4px; }
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

DEPARTMENT_CATEGORIES = ["Administrative", "Paramedical", "Nursing", "Clinical"]

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

# ============== PAGES ==============
def show_logo():
    st.markdown("""
    <div class="logo-container">
        <div class="logo-main">🏥 MEDANTA</div>
        <div class="logo-sub">The Medicity</div>
    </div>
    """, unsafe_allow_html=True)

def show_landing():
    show_logo()
    
    st.markdown('<h1>Namaste</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">New Hire Induction Portal</p>', unsafe_allow_html=True)
    st.markdown('<div class="elegant-divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="portal-card">
            <div class="card-icon">◆</div>
            <div class="card-title">New Hire</div>
            <div class="card-desc">First time here? Register now</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Register", key="new_btn"):
            st.session_state.user_type = 'new'
            st.session_state.page = 'registration'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="portal-card">
            <div class="card-icon">◈</div>
            <div class="card-title">Returning Employee</div>
            <div class="card-desc">Already registered? Login</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Login", key="return_btn"):
            st.session_state.user_type = 'returning'
            st.session_state.page = 'returning_login'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        if st.button("ADMIN PORTAL", key="admin_btn"):
            st.session_state.page = 'admin_login'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def show_registration():
    show_logo()
    st.markdown('<h2>New Hire Registration</h2>', unsafe_allow_html=True)
    st.markdown('<div class="elegant-divider"></div>', unsafe_allow_html=True)
    
    with st.form("reg_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter full name")
            mobile = st.text_input("Mobile Number *", placeholder="+91-XXXXXXXXXX")
        with col2:
            email = st.text_input("Email Address *", placeholder="email@example.com")
            employee_id = st.text_input("Employee ID (if allotted)", placeholder="MED2024001")
        
        col1, col2 = st.columns(2)
        with col1:
            dept_category = st.selectbox("Department Category *", ["Select"] + DEPARTMENT_CATEGORIES)
        with col2:
            sub_department = st.text_input("Sub Department *", placeholder="e.g., Cardiology, HR")
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.form_submit_button("← BACK"):
                st.session_state.page = 'landing'
                st.rerun()
        with col3:
            if st.form_submit_button("REGISTER →"):
                if name and email and mobile and dept_category != "Select" and sub_department:
                    existing_user = get_user_by_email(email)
                    if existing_user:
                        st.error("Email already registered")
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
                    st.error("Please fill all required fields")

def show_returning_login():
    show_logo()
    st.markdown('<h2>Employee Login</h2>', unsafe_allow_html=True)
    st.markdown('<div class="elegant-divider"></div>', unsafe_allow_html=True)
    
    login_method = st.radio("", ["Email Address", "Employee ID"], horizontal=True)
    
    if login_method == "Email Address":
        email = st.text_input("", placeholder="your.email@example.com")
    else:
        emp_id = st.text_input("", placeholder="MED2024001")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← BACK"):
            st.session_state.page = 'landing'
            st.rerun()
    with col3:
        if st.button("LOGIN →"):
            if login_method == "Email Address":
                user = get_user_by_email(email) if email else None
            else:
                user = get_user_by_employee_id(emp_id) if emp_id else None
            
            if user:
                st.session_state.user = user
                st.session_state.page = 'employee_dashboard'
                st.rerun()
            else:
                st.error("User not found")

def show_employee_dashboard():
    user = st.session_state.user
    
    show_logo()
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f'<h1 style="text-align: left; font-size: 1.5rem;">Welcome, {user["name"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #666; font-size: 0.8rem;">{user.get("sub_department", "N/A")} | {user.get("department_category", "N/A")}</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown('<h2>Learning Resources</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="dashboard-item">
            <div class="dashboard-icon">📖</div>
            <div class="dashboard-title">Employee Handbook</div>
            <div class="dashboard-desc">Digital handbook & policies</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("ACCESS", key="handbook_btn"):
            st.session_state.page = 'handbook'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="dashboard-item">
            <div class="dashboard-icon">🏥</div>
            <div class="dashboard-title">JCI Handbook</div>
            <div class="dashboard-desc">Joint Commission standards</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("ACCESS", key="jci_btn"):
            st.session_state.page = 'jci_handbook'
            st.rerun()
    
    st.markdown('<h2>Assessment</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="dashboard-item">
            <div class="dashboard-icon">📝</div>
            <div class="dashboard-title">Take Assessment</div>
            <div class="dashboard-desc">175 questions | 70% to pass</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("START", key="assess_btn"):
            st.session_state.answers = {}
            st.session_state.current_question = 0
            st.session_state.submitted = False
            st.session_state.page = 'assessment'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="dashboard-item">
            <div class="dashboard-icon">📊</div>
            <div class="dashboard-title">Report Card</div>
            <div class="dashboard-desc">View results & certificate</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("VIEW", key="report_btn"):
            st.session_state.page = 'report_card'
            st.rerun()
    
    st.markdown('<h2>Progress Report</h2>', unsafe_allow_html=True)
    
    data = load_data()
    user_assessments = []
    for u in data['users']:
        if u.get('email') == user.get('email'):
            user_assessments = u.get('assessments', [])
            break
    
    if user_assessments:
        latest = user_assessments[-1]
        col1, col2, col3, col4 = st.columns(4)
        metrics = [
            (str(len(user_assessments)), "Attempts"),
            (f"{latest['percentage']:.0f}%", "Latest Score"),
            (latest['status'], "Status"),
            (f"{max(a['percentage'] for a in user_assessments):.0f}%", "Best Score")
        ]
        for i, (val, label) in enumerate(metrics):
            with [col1, col2, col3, col4][i]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{val}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No assessments taken yet")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("LOGOUT", use_container_width=True):
        st.session_state.user = None
        st.session_state.page = 'landing'
        st.rerun()

def show_handbook():
    user = st.session_state.user
    show_logo()
    st.markdown('<h2>Employee Handbook</h2>', unsafe_allow_html=True)
    
    if st.button("← BACK TO DASHBOARD"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()
    
    flipping_book_url = "https://online.flippingbook.com/view/652486186/"
    
    st.markdown(f"""
    <div style="border: 1px solid #E0E0E0; margin-top: 1rem;">
        <iframe src="{flipping_book_url}" 
                style="width: 100%; height: 500px; border: none;" 
                allowfullscreen>
        </iframe>
    </div>
    """, unsafe_allow_html=True)

def show_jci_handbook():
    show_logo()
    st.markdown('<h2>JCI Handbook</h2>', unsafe_allow_html=True)
    
    if st.button("← BACK TO DASHBOARD"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()
    
    st.info("JCI Handbook content loading...")

def show_assessment():
    if st.session_state.submitted:
        show_report_card()
        return
    
    user = st.session_state.user
    show_logo()
    
    total_questions = len(QUESTIONS)
    current = st.session_state.current_question + 1
    progress_percent = (current / total_questions) * 100
    
    st.progress(progress_percent / 100)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write(f"Question {current} of {total_questions}")
    with col2:
        st.write(f"{progress_percent:.1f}% Complete")
    
    q = QUESTIONS[st.session_state.current_question]
    
    st.markdown(f'<p style="color: #8B1538; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px;">{q["category"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="border: none; font-size: 1.2rem;">{q["id"]}. {q["question"]}</h3>', unsafe_allow_html=True)
    
    selected_option = st.radio("", q['options'], key=f"q_{q['id']}", index=None)
    
    if selected_option:
        st.session_state.answers[q['id']] = selected_option
    
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.session_state.current_question > 0:
            if st.button("← PREVIOUS"):
                st.session_state.current_question -= 1
                st.rerun()
    with col2:
        if st.button("SAVE & EXIT"):
            st.session_state.page = 'employee_dashboard'
            st.rerun()
    with col3:
        if st.session_state.current_question < total_questions - 1:
            if st.button("NEXT →"):
                if q['id'] in st.session_state.answers:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    st.warning("Select an answer")
        else:
            if st.button("SUBMIT ✓"):
                if q['id'] in st.session_state.answers:
                    st.session_state.submitted = True
                    save_assessment_result(st.session_state.user)
                    st.rerun()
                else:
                    st.warning("Select an answer")

def show_report_card():
    correct, total, percentage = calculate_score()
    user = st.session_state.user
    
    show_logo()
    st.markdown('<h2>Assessment Report</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        status_class = "status-pass" if percentage >= 70 else "status-fail"
        status_text = "PASSED" if percentage >= 70 else "FAILED"
        
        st.markdown(f"""
        <div class="score-display">
            <div class="score-value">{percentage:.0f}%</div>
            <div class="score-label">Overall Score</div>
            <div style="margin-top: 1rem;">
                <span class="{status_class}">{status_text}</span>
            </div>
            <p style="margin-top: 1rem; color: #666; font-size: 0.9rem;">{user['name']}<br>{user.get('sub_department', 'N/A')}</p>
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
        st.metric("Accuracy", f"{percentage:.1f}%")
    
    if percentage >= 70:
        st.success("Congratulations! You have successfully completed the induction program.")
        cert_text = f"""CERTIFICATE OF COMPLETION
{'='*50}
This certifies that

{user['name']}

has successfully completed the
Medanta New Hire Induction Program

Employee ID: {user.get('employee_id', 'N/A')}
Department: {user.get('sub_department', 'N/A')}
Score: {percentage:.1f}%
Date: {datetime.now().strftime('%B %d, %Y')}
Certificate ID: CERT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"""
        
        st.download_button("DOWNLOAD CERTIFICATE", cert_text, 
                          f"Medanta_Certificate_{user['name'].replace(' ', '_')}.txt")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← BACK TO DASHBOARD"):
            st.session_state.page = 'employee_dashboard'
            st.session_state.submitted = False
            st.session_state.current_question = 0
            st.rerun()
    with col2:
        if percentage < 70:
            if st.button("RETAKE ASSESSMENT"):
                st.session_state.answers = {}
                st.session_state.submitted = False
                st.session_state.current_question = 0
                st.session_state.page = 'assessment'
                st.rerun()

def show_admin_login():
    show_logo()
    st.markdown('<h2>Admin Portal</h2>', unsafe_allow_html=True)
    st.markdown('<div class="elegant-divider"></div>', unsafe_allow_html=True)
    
    username = st.text_input("Username", placeholder="admin")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← BACK"):
            st.session_state.page = 'landing'
            st.rerun()
    with col3:
        if st.button("LOGIN →"):
            if username == "admin" and password == "medanta2024":
                st.session_state.admin_authenticated = True
                st.session_state.page = 'admin_dashboard'
                st.rerun()
            else:
                st.error("Invalid credentials")

def show_admin_dashboard():
    if not st.session_state.admin_authenticated:
        st.session_state.page = 'admin_login'
        st.rerun()
        return
    
    show_logo()
    st.markdown('<h2>Admin Dashboard</h2>', unsafe_allow_html=True)
    st.markdown('<div class="elegant-divider"></div>', unsafe_allow_html=True)
    
    data = load_data()
    results = load_results()
    
    total_users = len(data['users'])
    total_assessments = len(results)
    passed = sum(1 for r in results if r['status'] == "Passed")
    avg_score = sum(r['percentage'] for r in results) / total_assessments if total_assessments > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        (str(total_users), "Total Users"),
        (str(total_assessments), "Assessments"),
        (f"{(passed/total_assessments*100):.0f}%" if total_assessments > 0 else "0%", "Pass Rate"),
        (f"{avg_score:.1f}%", "Avg Score")
    ]
    for i, (val, label) in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    tabs = st.tabs(["Employees", "Reports", "Analytics"])
    
    with tabs[0]:
        if data['users']:
            users_df = pd.DataFrame(data['users'])
            st.dataframe(users_df[['user_id', 'name', 'email', 'employee_id', 'department_category', 'sub_department', 'registration_date']], use_container_width=True)
            csv = users_df.to_csv(index=False)
            st.download_button("EXPORT CSV", csv, f"employees_{datetime.now().strftime('%Y%m%d')}.csv")
        else:
            st.info("No employees registered")
    
    with tabs[1]:
        if results:
            results_df = pd.DataFrame(results)
            st.dataframe(results_df[['date', 'name', 'employee_id', 'department_category', 'score', 'total', 'percentage', 'status']], use_container_width=True)
            csv = results_df.to_csv(index=False)
            st.download_button("EXPORT RESULTS", csv, f"results_{datetime.now().strftime('%Y%m%d')}.csv")
        else:
            st.info("No assessment results")
    
    with tabs[2]:
        if results:
            results_df = pd.DataFrame(results)
            dept_stats = results_df.groupby('department_category')['percentage'].mean().reset_index()
            st.bar_chart(dept_stats.set_index('department_category'))
            
            st.markdown("### Department Performance")
            for _, row in dept_stats.iterrows():
                st.write(f"**{row['department_category']}:** {row['percentage']:.1f}%")
        else:
            st.info("No data available")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("LOGOUT"):
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
        'handbook': show_handbook,
        'jci_handbook': show_jci_handbook,
        'assessment': show_assessment,
        'report_card': show_report_card,
        'admin_login': show_admin_login,
        'admin_dashboard': show_admin_dashboard
    }
    
    current_page = st.session_state.get('page', 'landing')
    pages.get(current_page, show_landing)()

if __name__ == "__main__":
    main()
