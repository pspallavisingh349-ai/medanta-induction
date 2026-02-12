import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

# ============== PAGE CONFIGURATION ==============
st.set_page_config(
    page_title="Medanta New Hire Induction Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============== CUSTOM CSS - CREAM, WHITE, GOLD, MAROON, GREY THEME ==============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Main Background - Cream to White Gradient */
    .main {
        background: linear-gradient(135deg, #FAF7F0 0%, #FFFFFF 50%, #FDF8E8 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #FAF7F0 0%, #FFFFFF 50%, #FDF8E8 100%);
    }
    
    /* Header Styling - Gold and Maroon */
    .welcome-text {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        color: #8B1538;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 700;
        letter-spacing: 2px;
    }
    
    .namaste-text {
        font-family: 'Cinzel', serif;
        font-size: 4.5rem;
        color: #D4AF37;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 600;
        text-shadow: 2px 2px 4px rgba(139, 21, 56, 0.2);
    }
    
    .subtitle-text {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
        letter-spacing: 1px;
    }
    
    /* Logo Styling */
    .logo-container {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #FFFFFF 0%, #FDF8E8 100%);
        border-radius: 20px;
        border: 3px solid #D4AF37;
        margin: 2rem auto;
        max-width: 400px;
        box-shadow: 0 10px 40px rgba(139, 21, 56, 0.15);
    }
    
    .logo-icon {
        font-size: 4rem;
        margin-bottom: 0.5rem;
    }
    
    .logo-text {
        font-family: 'Cinzel', serif;
        font-size: 3rem;
        color: #8B1538;
        font-weight: 700;
        letter-spacing: 4px;
        margin: 0;
    }
    
    .logo-tagline {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #D4AF37;
        letter-spacing: 3px;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    /* Card Styling - White with Gold Border */
    .info-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(139, 21, 56, 0.08);
        border: 2px solid #D4AF37;
        margin: 1rem 0;
    }
    
    .login-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 10px 40px rgba(139, 21, 56, 0.1);
        border: 3px solid #D4AF37;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Button Styling - Maroon with Gold Border */
    .stButton>button {
        background: linear-gradient(135deg, #8B1538 0%, #A91D3A 100%);
        color: #FFFFFF;
        border: 2px solid #D4AF37;
        border-radius: 30px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 21, 56, 0.3);
        background: linear-gradient(135deg, #A91D3A 0%, #8B1538 100%);
    }
    
    /* Secondary Button - Gold with Maroon Text */
    .secondary-btn {
        background: linear-gradient(135deg, #FDF8E8 0%, #FFFFFF 100%) !important;
        color: #8B1538 !important;
        border: 2px solid #D4AF37 !important;
    }
    
    /* Input Styling - Cream Background with Gold Border */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 2px solid #D4AF37;
        background: #FAF7F0;
        color: #374151;
        padding: 0.8rem;
        font-size: 1rem;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div>select:focus {
        border-color: #8B1538;
        box-shadow: 0 0 0 3px rgba(139, 21, 56, 0.1);
    }
    
    /* Labels - Grey Color */
    .stTextInput label, .stSelectbox label {
        color: #6B7280 !important;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    /* Progress Bar - Gold to Maroon */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #D4AF37 0%, #8B1538 100%);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(212, 175, 55, 0.1);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #FFFFFF;
        border-radius: 10px;
        padding: 10px 20px;
        border: 2px solid transparent;
        color: #6B7280;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8B1538 0%, #A91D3A 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #D4AF37 !important;
    }
    
    /* Choice Cards */
    .choice-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        border: 3px solid #D4AF37;
        box-shadow: 0 8px 25px rgba(139, 21, 56, 0.1);
        margin: 1rem;
        transition: all 0.3s;
    }
    
    .choice-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(139, 21, 56, 0.2);
        border-color: #8B1538;
    }
    
    .choice-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
    }
    
    .choice-title {
        color: #8B1538;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-family: 'Playfair Display', serif;
    }
    
    .choice-desc {
        color: #6B7280;
        font-size: 1rem;
    }
    
    /* Section Headers */
    .section-header {
        color: #8B1538;
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #D4AF37;
        padding-bottom: 1rem;
        display: inline-block;
        width: 100%;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .welcome-text { font-size: 2rem; }
        .namaste-text { font-size: 2.5rem; }
        .logo-text { font-size: 2rem; }
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

# ============== DEPARTMENT DATA ==============
DEPARTMENT_CATEGORIES = {
    "Administrative": [
        "HR Department", "Finance & Accounts", "Administration", 
        "Legal & Compliance", "Marketing", "IT Support", 
        "Procurement", "Front Office"
    ],
    "Paramedical": [
        "Laboratory Services", "Radiology & Imaging", "Physiotherapy",
        "Respiratory Therapy", "Dialysis Unit", "Blood Bank", 
        "Pharmacy", "Biomedical Engineering"
    ],
    "Clinical": [
        "Cardiology", "Neurology", "Orthopedics", "Gastroenterology",
        "Oncology", "Nephrology", "Pulmonology", "Endocrinology",
        "Rheumatology", "Dermatology", "ENT", "Ophthalmology",
        "Dental", "Emergency Medicine", "Critical Care", "Anesthesiology"
    ],
    "Nursing": [
        "General Ward Nursing", "ICU Nursing", "OT Nursing",
        "Emergency Nursing", "Pediatric Nursing", "Oncology Nursing",
        "Cardiac Nursing", "Neuro Nursing", "Nursing Administration"
    ]
}

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

CONTACTS = [
    {"name": "HR Department", "phone": "+91-124-4141414", "email": "hr@medanta.org", "icon": "👥"},
    {"name": "IT Helpdesk", "phone": "+91-124-4141415", "email": "it.support@medanta.org", "icon": "💻"},
    {"name": "Emergency", "phone": "108", "email": "emergency@medanta.org", "icon": "🚨"},
    {"name": "Admin Office", "phone": "+91-124-4141416", "email": "admin@medanta.org", "icon": "🏢"},
]

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

# ============== PAGES ==============
def show_logo():
    """Display Medanta Logo"""
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; margin: 1rem auto; max-width: 350px;">
        <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🏥</div>
        <h1 style="font-family: 'Cinzel', serif; font-size: 2.8rem; color: #8B1538; font-weight: 700; letter-spacing: 4px; margin: 0;">MEDANTA</h1>
        <p style="font-family: 'Inter', sans-serif; font-size: 0.85rem; color: #D4AF37; letter-spacing: 3px; margin-top: 0.3rem; font-weight: 500;">THE MEDICITY</p>
    </div>
    """, unsafe_allow_html=True)

def show_landing():
    show_logo()
    
    st.markdown('<h1 class="namaste-text">🙏 Namaste</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="welcome-text">Welcome to Medanta</h2>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">New Hire Induction Portal</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="choice-card">
            <div class="choice-icon">🆕</div>
            <div class="choice-title">New Hire</div>
            <div class="choice-desc">First time here? Register and start your induction journey.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("I'm a New Hire", key="new_hire_btn", use_container_width=True):
            st.session_state.user_type = 'new'
            st.session_state.page = 'registration'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="choice-card">
            <div class="choice-icon">👤</div>
            <div class="choice-title">Returning User</div>
            <div class="choice-desc">Already registered? Login to continue or view results.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("I'm a Returning User", key="returning_btn", use_container_width=True):
            st.session_state.user_type = 'returning'
            st.session_state.page = 'returning_login'
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔐 Admin Login", use_container_width=True):
            st.session_state.page = 'admin_login'
            st.rerun()

def show_registration():
    show_logo()
    st.markdown('<h2 class="section-header">📝 New Hire Registration</h2>', unsafe_allow_html=True)
    
    with st.container():
        with st.form("registration_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name *", placeholder="Enter your full name")
                mobile = st.text_input("Mobile Number *", placeholder="+91-XXXXXXXXXX")
            with col2:
                email = st.text_input("Email Address *", placeholder="your.email@example.com")
                employee_id = st.text_input("Employee ID (if allotted)", placeholder="e.g., MED2024001")
            
            col1, col2 = st.columns(2)
            with col1:
                dept_category = st.selectbox("Department Category *", 
                                             ["Select"] + list(DEPARTMENT_CATEGORIES.keys()))
            with col2:
                sub_department = st.selectbox("Sub Department *", 
                                              ["Select"] + (DEPARTMENT_CATEGORIES.get(dept_category, []) if dept_category != "Select" else []))
            
            submitted = st.form_submit_button("Register & Continue →", use_container_width=True)
            
            if submitted:
                if name and email and mobile and dept_category != "Select" and sub_department != "Select":
                    existing_user = get_user_by_email(email)
                    if existing_user:
                        st.error("⚠️ This email is already registered! Use Returning User login.")
                    else:
                        user_info = {
                            'name': name,
                            'email': email,
                            'mobile': mobile,
                            'employee_id': employee_id if employee_id else "Pending",
                            'department_category': dept_category,
                            'sub_department': sub_department,
                            'user_type': 'new_hire'
                        }
                        user_id = add_user(user_info)
                        user_info['user_id'] = user_id
                        st.session_state.user = user_info
                        st.session_state.page = 'handbook'
                        st.rerun()
                else:
                    st.error("⚠️ Please fill all required fields!")
    
    if st.button("← Back", use_container_width=True):
        st.session_state.page = 'landing'
        st.rerun()

def show_returning_login():
    show_logo()
    st.markdown('<h2 class="section-header">👤 Returning User Login</h2>', unsafe_allow_html=True)
    
    with st.container():
        login_method = st.radio("Login using:", ["Email Address", "Employee ID"])
        
        if login_method == "Email Address":
            email = st.text_input("📧 Enter your registered email", placeholder="your.email@example.com")
        else:
            emp_id = st.text_input("🆔 Enter your Employee ID", placeholder="e.g., MED2024001")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.page = 'landing'
                st.rerun()
        
        with col3:
            if st.button("Login →", use_container_width=True):
                if login_method == "Email Address":
                    if email:
                        user = get_user_by_email(email)
                        if user:
                            st.session_state.user = user
                            st.session_state.page = 'user_dashboard'
                            st.rerun()
                        else:
                            st.error("⚠️ Email not found! Please register as New Hire.")
                else:
                    if emp_id:
                        user = get_user_by_employee_id(emp_id)
                        if user:
                            st.session_state.user = user
                            st.session_state.page = 'user_dashboard'
                            st.rerun()
                        else:
                            st.error("⚠️ Employee ID not found! Please register as New Hire.")

def show_user_dashboard():
    user = st.session_state.user
    show_logo()
    st.markdown(f'<h2 style="text-align: center; color: #8B1538; font-family: Playfair Display, serif; font-size: 2rem; margin-bottom: 1rem;">👋 Welcome back, {user["name"]}!</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; border: 2px solid #D4AF37; margin-bottom: 1rem;">
            <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">Employee ID</p>
            <p style="color: #8B1538; font-weight: 600; margin: 0; font-size: 1.1rem;">{user.get('employee_id', 'N/A')}</p>
            <p style="color: #6B7280; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Department</p>
            <p style="color: #8B1538; font-weight: 600; margin: 0; font-size: 1.1rem;">{user.get('sub_department', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; border: 2px solid #D4AF37; margin-bottom: 1rem;">
            <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">Category</p>
            <p style="color: #8B1538; font-weight: 600; margin: 0; font-size: 1.1rem;">{user.get('department_category', 'N/A')}</p>
            <p style="color: #6B7280; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Email</p>
            <p style="color: #8B1538; font-weight: 600; margin: 0; font-size: 1.1rem;">{user.get('email', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    data = load_data()
    user_assessments = []
    for u in data['users']:
        if u.get('email') == user.get('email'):
            user_assessments = u.get('assessments', [])
            break
    
    if user_assessments:
        st.markdown('<h3 style="color: #8B1538; font-family: Playfair Display, serif; margin-top: 1.5rem;">📊 Assessment History</h3>', unsafe_allow_html=True)
        for assessment in reversed(user_assessments[-5:]):
            status_color = "#10B981" if assessment['status'] == "Passed" else "#EF4444"
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {status_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color: #6B7280; font-size: 0.9rem;">{assessment['date']}</span><br>
                        <span style="color: #374151; font-weight: 500;">Score: {assessment['score']}/{assessment['total']} ({assessment['percentage']:.1f}%)</span>
                    </div>
                    <span style="color: {status_color}; font-weight: 700; font-size: 1.1rem;">{assessment['status']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if user_assessments[-1]['percentage'] >= 70:
            st.success("🎉 You have already passed the induction program!")
        else:
            st.warning("⚠️ You need to pass the assessment (70% or higher).")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("📚 Review Handbook", use_container_width=True):
            st.session_state.page = 'handbook'
            st.rerun()
    with col2:
        if st.button("📝 Take Assessment", use_container_width=True):
            st.session_state.answers = {}
            st.session_state.current_question = 0
            st.session_state.submitted = False
            st.session_state.page = 'assessment'
            st.rerun()
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = 'landing'
            st.rerun()

def show_handbook():
    show_logo()
    st.markdown('<h2 class="section-header">📚 Employee Handbook</h2>', unsafe_allow_html=True)
    
    tabs = st.tabs(["🏥 About Medanta", "📖 Policies", "🎥 Video Tour", "📞 Contacts"])
    
    with tabs[0]:
        st.header("About Medanta - The Medicity")
        st.write("Medanta is one of India's largest multi-super specialty medical institutes located in Gurgaon. Founded by Dr. Naresh Trehan, Medanta brings together outstanding doctors, scientists, and technologists to provide world-class healthcare.")
        
        st.subheader("Our Vision")
        st.write("To create an integrated healthcare system that provides high-quality, affordable care to all sections of society.")
        
        st.subheader("Our Mission")
        st.write("To deliver international standard healthcare through innovative, ethical, and patient-centric services.")
        
        st.subheader("Core Values")
        st.markdown("""
        - **Patient First:** Every decision prioritizes patient welfare
        - **Integrity:** Uncompromising ethical standards
        - **Excellence:** Continuous pursuit of medical excellence
        - **Compassion:** Treating every patient with empathy
        - **Innovation:** Embracing cutting-edge technology
        """)
    
    with tabs[1]:
        st.header("Key Policies")
        st.subheader("🔒 Confidentiality Policy")
        st.write("All patient information is strictly confidential. Never discuss patient details in public areas or share on social media.")
        st.subheader("⏰ Attendance Policy")
        st.write("Standard working hours are 9 AM to 6 PM. Inform your supervisor 24 hours in advance for planned leaves.")
        st.subheader("👔 Dress Code")
        st.write("Professional attire is mandatory. Clinical staff must wear clean uniforms and ID badges at all times.")
        st.subheader("⚠️ Safety Policy")
        st.write("Report all incidents immediately. Your safety and patient safety are our top priorities.")
    
    with tabs[2]:
        st.header("Virtual Tour of Medanta")
        st.info("🎬 Virtual Tour Video - In production. Contact HR for physical facility tour.")
        st.subheader("Key Facilities")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("🏥 Main Hospital")
            st.write("🫀 Heart Institute")
        with col2:
            st.write("🧠 Neurosciences")
            st.write("🦴 Orthopedics")
        with col3:
            st.write("🧪 Advanced Labs")
            st.write("🍽️ Staff Cafeteria")
    
    with tabs[3]:
        st.header("Emergency & Key Contacts")
        cols = st.columns(2)
        for idx, contact in enumerate(CONTACTS):
            with cols[idx % 2]:
                st.subheader(f"{contact['icon']} {contact['name']}")
                st.write(f"📞 **Phone:** {contact['phone']}")
                st.write(f"✉️ **Email:** {contact['email']}")
                st.markdown("---")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back", use_container_width=True):
            if st.session_state.user_type == 'returning':
                st.session_state.page = 'user_dashboard'
            else:
                st.session_state.page = 'registration'
            st.rerun()
    with col3:
        if st.button("Start Assessment →", use_container_width=True):
            st.session_state.page = 'assessment'
            st.rerun()

def show_assessment():
    if st.session_state.submitted:
        show_report_card()
        return
    
    show_logo()
    st.markdown('<h2 class="section-header">📝 Knowledge Assessment</h2>', unsafe_allow_html=True)
    
    total_questions = len(QUESTIONS)
    current = st.session_state.current_question + 1
    progress = current / total_questions
    
    st.progress(progress)
    st.write(f"**Question {current} of {total_questions}**")
    
    q = QUESTIONS[st.session_state.current_question]
    
    st.markdown(f'<p style="color: #D4AF37; font-weight: 600; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">{q["category"]}</p>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color: #374151; margin-bottom: 1.5rem;">{q["id"]}. {q["question"]}</h3>', unsafe_allow_html=True)
    
    selected_option = st.radio("Select your answer:", q['options'], key=f"q_{q['id']}", index=None)
    
    if selected_option:
        st.session_state.answers[q['id']] = selected_option
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.session_state.current_question > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    with col3:
        if st.session_state.current_question < total_questions - 1:
            if st.button("Next →", use_container_width=True):
                if q['id'] in st.session_state.answers:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    st.warning("⚠️ Please select an answer!")
        else:
            if st.button("Submit Assessment ✓", use_container_width=True):
                if q['id'] in st.session_state.answers:
                    st.session_state.submitted = True
                    save_assessment_result(st.session_state.user)
                    st.rerun()
                else:
                    st.warning("⚠️ Please select an answer!")

def show_report_card():
    correct, total, percentage = calculate_score()
    show_logo()
    st.markdown('<h2 class="section-header">📊 Your Report Card</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        score_color = "#10B981" if percentage >= 70 else "#EF4444"
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: white; border-radius: 20px; border: 3px solid #D4AF37; margin-bottom: 1rem;">
            <div style="width: 150px; height: 150px; border-radius: 50%; background: conic-gradient(#8B1538 {percentage*3.6}deg, #F3F4F6 0deg); margin: 0 auto; display: flex; align-items: center; justify-content: center;">
                <div style="width: 120px; height: 120px; border-radius: 50%; background: white; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 2.5rem; font-weight: bold; color: #8B1538;">{percentage:.0f}%</span>
                </div>
            </div>
            <h3 style="color: #8B1538; margin-top: 1rem; font-family: Playfair Display, serif;">{st.session_state.user['name']}</h3>
            <p style="color: #6B7280; margin: 0;">{st.session_state.user.get('sub_department', 'N/A')}</p>
            <div style="margin-top: 1rem; padding: 0.8rem; background: {'#D1FAE5' if percentage >= 70 else '#FEE2E2'}; border-radius: 10px;">
                <span style="color: {'#059669' if percentage >= 70 else '#DC2626'}; font-weight: 700; font-size: 1.1rem;">
                    {'🎉 Passed' if percentage >= 70 else '❌ Failed'}
                </span>
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
        st.success("🎉 Congratulations! You have successfully completed the Medanta Induction Program!")
        cert_text = f"""
CERTIFICATE OF COMPLETION
----------------------------
This certifies that
{st.session_state.user['name']}
has successfully completed the
Medanta New Hire Induction Program

Employee ID: {st.session_state.user.get('employee_id', 'N/A')}
Department: {st.session_state.user.get('sub_department', 'N/A')}
Score: {percentage:.1f}%
Date: {datetime.now().strftime("%B %d, %Y")}
Certificate ID: CERT{datetime.now().strftime('%Y%m%d%H%M%S')}
"""
        st.download_button(label="📥 Download Certificate", data=cert_text, 
                          file_name=f"Medanta_Certificate_{st.session_state.user.get('employee_id', 'User')}.txt", 
                          mime="text/plain", use_container_width=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back to Dashboard", use_container_width=True):
            st.session_state.page = 'user_dashboard'
            st.session_state.submitted = False
            st.session_state.current_question = 0
            st.rerun()
    with col3:
        if st.button("🏠 Return to Home", use_container_width=True):
            st.session_state.page = 'landing'
            st.session_state.user = None
            st.session_state.answers = {}
            st.session_state.current_question = 0
            st.session_state.submitted = False
            st.rerun()

def show_admin_login():
    show_logo()
    st.markdown('<h2 class="section-header">🔐 Admin Login</h2>', unsafe_allow_html=True)
    username = st.text_input("👤 Admin Username")
    password = st.text_input("🔑 Password", type="password")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = 'landing'
            st.rerun()
    with col3:
        if st.button("Login →", use_container_width=True):
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
    st.markdown('<h2 class="section-header">📊 Admin Dashboard</h2>', unsafe_allow_html=True)
    
    data = load_data()
    results = load_results()
    
    total_users = len(data['users'])
    total_assessments = len(results)
    passed = sum(1 for r in results if r['status'] == "Passed")
    avg_score = sum(r['percentage'] for r in results) / total_assessments if total_assessments > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", total_users)
    with col2:
        st.metric("Assessments", total_assessments)
    with col3:
        st.metric("Avg Score", f"{avg_score:.1f}%")
    with col4:
        st.metric("Pass Rate", f"{(passed/total_assessments*100):.1f}%" if total_assessments > 0 else "0%")
    
    tabs = st.tabs(["📋 All Users", "📊 Results", "📈 Analytics"])
    
    with tabs[0]:
        if data['users']:
            users_df = pd.DataFrame(data['users'])
            st.dataframe(users_df[['user_id', 'name', 'email', 'employee_id', 'department_category', 'sub_department']], use_container_width=True)
            csv = users_df.to_csv(index=False)
            st.download_button("📥 Download Users CSV", csv, f"medanta_users_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
        else:
            st.info("No users registered yet.")
    
    with tabs[1]:
        if results:
            results_df = pd.DataFrame(results)
            st.dataframe(results_df[['date', 'name', 'employee_id', 'department_category', 'score', 'total', 'percentage', 'status']], use_container_width=True)
            csv = results_df.to_csv(index=False)
            st.download_button("📥 Download Results CSV", csv, f"medanta_results_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
        else:
            st.info("No results yet.")
    
    with tabs[2]:
        if results:
            results_df = pd.DataFrame(results)
            dept_stats = results_df.groupby('department_category')['percentage'].mean().reset_index()
            st.bar_chart(dept_stats.set_index('department_category'))
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.session_state.page = 'landing'
        st.rerun()

# ============== MAIN ==============
def main():
    if st.session_state.page == 'landing':
        show_landing()
    elif st.session_state.page == 'registration':
        show_registration()
    elif st.session_state.page == 'returning_login':
        show_returning_login()
    elif st.session_state.page == 'user_dashboard':
        show_user_dashboard()
    elif st.session_state.page == 'handbook':
        show_handbook()
    elif st.session_state.page == 'assessment':
        show_assessment()
    elif st.session_state.page == 'admin_login':
        show_admin_login()
    elif st.session_state.page == 'admin_dashboard':
        show_admin_dashboard()
    else:
        show_landing()

if __name__ == "__main__":
    main()
