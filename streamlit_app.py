import streamlit as st
import pandas as pd
import json
import base64
from datetime import datetime
import os

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
    
    .main {
        background: linear-gradient(135deg, #faf8f5 0%, #f5f0e8 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #faf8f5 0%, #f5f0e8 100%);
    }
    
    /* Header Styling */
    .medanta-header {
        background: linear-gradient(90deg, #8B1538 0%, #A91D3A 100%);
        padding: 1.5rem;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 4px 20px rgba(139, 21, 56, 0.2);
        margin-bottom: 2rem;
    }
    
    .welcome-text {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        color: #D4AF37;
        text-align: center;
        animation: fadeInUp 2s ease-out;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .namaste-text {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        color: #8B1538;
        text-align: center;
        animation: pulse 2s infinite;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Card Styling */
    .info-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(139, 21, 56, 0.1);
        border: 2px solid #D4AF37;
        margin: 1rem 0;
    }
    
    .login-card {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 10px 40px rgba(139, 21, 56, 0.15);
        border: 3px solid #D4AF37;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .question-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 5px solid #8B1538;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #8B1538 0%, #A91D3A 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
        border: 2px solid #D4AF37;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(139, 21, 56, 0.3);
    }
    
    .secondary-btn {
        background: white !important;
        color: #8B1538 !important;
        border: 2px solid #8B1538 !important;
    }
    
    /* Input Styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stNumberInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #D4AF37;
        background: white;
        padding: 0.8rem;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #8B1538 0%, #D4AF37 100%);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(139, 21, 56, 0.05);
        padding: 10px;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: 2px solid transparent;
        color: #8B1538;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8B1538 0%, #A91D3A 100%) !important;
        color: white !important;
        border: 2px solid #D4AF37 !important;
    }
    
    /* Report Card */
    .report-card {
        background: linear-gradient(135deg, #ffffff 0%, #faf8f5 100%);
        border: 3px solid #D4AF37;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
    }
    
    .score-circle {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        background: conic-gradient(#8B1538 var(--score-deg), #f0f0f0 0deg);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        position: relative;
    }
    
    .score-inner {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #8B1538;
    }
    
    /* Contact Cards */
    .contact-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        border: 2px solid #D4AF37;
        text-align: center;
        transition: transform 0.3s;
    }
    
    .contact-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(139, 21, 56, 0.15);
    }
    
    /* Choice Cards */
    .choice-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        border: 3px solid transparent;
        transition: all 0.3s;
        cursor: pointer;
        margin: 1rem;
    }
    
    .choice-card:hover {
        border-color: #D4AF37;
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(139, 21, 56, 0.2);
    }
    
    .choice-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
    }
    
    .choice-title {
        color: #8B1538;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .welcome-text { font-size: 2rem; }
        .namaste-text { font-size: 2.5rem; }
        .info-card { padding: 1rem; }
        .login-card { padding: 1.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# ============== DATA STORAGE SETUP ==============
DATA_FILE = "user_data.json"
RESULTS_FILE = "assessment_results.json"

def load_data():
    """Load all user data"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"users": [], "assessments": []}

def save_data(data):
    """Save all user data"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_results():
    """Load assessment results"""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_results(results):
    """Save assessment results"""
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=4)

def add_user(user_info):
    """Add new user to database"""
    data = load_data()
    user_info['registration_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_info['user_id'] = f"MED{datetime.now().strftime('%Y%m%d%H%M%S')}"
    data['users'].append(user_info)
    save_data(data)
    return user_info['user_id']

def get_user_by_email(email):
    """Get user by email"""
    data = load_data()
    for user in data['users']:
        if user['email'].lower() == email.lower():
            return user
    return None

def get_user_by_employee_id(emp_id):
    """Get user by employee ID"""
    data = load_data()
    for user in data['users']:
        if user.get('employee_id') == emp_id:
            return user
    return None

# ============== SESSION STATE INITIALIZATION ==============
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_type' not in st.session_state:
    st.session_state.user_type = None  # 'new' or 'returning'
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
        "HR Department",
        "Finance & Accounts",
        "Administration",
        "Legal & Compliance",
        "Marketing & Communications",
        "IT Support",
        "Procurement",
        "Front Office"
    ],
    "Paramedical": [
        "Laboratory Services",
        "Radiology & Imaging",
        "Physiotherapy",
        "Respiratory Therapy",
        "Dialysis Unit",
        "Blood Bank",
        "Pharmacy",
        "Biomedical Engineering"
    ],
    "Clinical": [
        "Cardiology",
        "Neurology",
        "Orthopedics",
        "Gastroenterology",
        "Oncology",
        "Nephrology",
        "Pulmonology",
        "Endocrinology",
        "Rheumatology",
        "Dermatology",
        "ENT",
        "Ophthalmology",
        "Dental",
        "Emergency Medicine",
        "Critical Care",
        "Anesthesiology"
    ],
    "Nursing": [
        "General Ward Nursing",
        "ICU Nursing",
        "OT Nursing",
        "Emergency Nursing",
        "Pediatric Nursing",
        "Oncology Nursing",
        "Cardiac Nursing",
        "Neuro Nursing",
        "Nursing Administration",
        "Nursing Education"
    ]
}

# ============== QUESTIONS DATA ==============
QUESTIONS = [
    # Patient Safety & Quality (Questions 1-25)
    {"id": 1, "category": "Patient Safety", "question": "What is the primary goal of Patient Safety at Medanta?", 
     "options": ["Prevent harm to patients", "Increase revenue", "Reduce staff", "Expand facilities"]},
    {"id": 2, "category": "Patient Safety", "question": "What does SBAR stand for in healthcare communication?",
     "options": ["Situation, Background, Assessment, Recommendation", "Standard, Basic, Advanced, Review", "Safety, Benefits, Assessment, Results", "System, Background, Analysis, Report"]},
    {"id": 3, "category": "Patient Safety", "question": "What is the correct hand hygiene duration using soap and water?",
     "options": ["40-60 seconds", "10-15 seconds", "20-30 seconds", "5-10 seconds"]},
    {"id": 4, "category": "Patient Safety", "question": "What color code indicates a fire emergency in hospital?",
     "options": ["Code Red", "Code Blue", "Code Pink", "Code Yellow"]},
    {"id": 5, "category": "Patient Safety", "question": "What is the most common cause of medication errors?",
     "options": ["Communication failure", "Equipment malfunction", "Staff shortage", "Patient non-compliance"]},
    {"id": 6, "category": "Patient Safety", "question": "What is the 'Universal Protocol' for preventing wrong site surgery?",
     "options": ["Sign in, Time out, Sign out", "Check in, Operate, Check out", "Verify, Cut, Confirm", "Prepare, Execute, Review"]},
    {"id": 7, "category": "Patient Safety", "question": "What does RACE stand for in fire safety?",
     "options": ["Rescue, Alarm, Contain, Extinguish", "Run, Alert, Call, Exit", "Remove, Avoid, Cover, Escape", "Report, Assess, Control, Evacuate"]},
    {"id": 8, "category": "Patient Safety", "question": "What is the proper way to verify patient identity?",
     "options": ["Two identifiers: Name and DOB/MRN", "Ask patient name only", "Check room number", "Verify with family member"]},
    {"id": 9, "category": "Patient Safety", "question": "What is a 'Never Event' in healthcare?",
     "options": ["Serious preventable error", "Minor incident", "Patient complaint", "Equipment failure"]},
    {"id": 10, "category": "Patient Safety", "question": "What is the purpose of Root Cause Analysis (RCA)?",
     "options": ["Identify underlying causes of errors", "Punish staff for mistakes", "Report to insurance", "Document incidents"]},
    
    # Clinical Excellence (Questions 11-35)
    {"id": 11, "category": "Clinical Excellence", "question": "What is the standard temperature for medication refrigerator?",
     "options": ["2-8°C", "0-5°C", "10-15°C", "Room temperature"]},
    {"id": 12, "category": "Clinical Excellence", "question": "What does NABH stand for?",
     "options": ["National Accreditation Board for Hospitals", "National Association of Better Healthcare", "National Accreditation for Better Hospitals", "National Advisory Board for Health"]},
    {"id": 13, "category": "Clinical Excellence", "question": "What is the correct technique for aseptic dressing change?",
     "options": ["Sterile to sterile, clean to clean", "Clean to sterile", "Sterile to clean", "No specific technique"]},
    {"id": 14, "category": "Clinical Excellence", "question": "What is the normal range for adult blood pressure?",
     "options": ["90/60 to 120/80 mmHg", "80/50 to 100/60 mmHg", "100/70 to 140/90 mmHg", "120/80 to 160/100 mmHg"]},
    {"id": 15, "category": "Clinical Excellence", "question": "What is the proper disposal method for sharps?",
     "options": ["Puncture-resistant yellow container", "Regular trash bin", "Recycling bin", "Biohazard bag"]},
    
    # Emergency Protocols (Questions 16-40)
    {"id": 16, "category": "Emergency Protocols", "question": "What is the first step in Basic Life Support (BLS)?",
     "options": ["Check scene safety", "Start chest compressions", "Call for help", "Check pulse"]},
    {"id": 17, "category": "Emergency Protocols", "question": "What is the compression-to-ventilation ratio for adult CPR?",
     "options": ["30:2", "15:2", "20:2", "40:2"]},
    {"id": 18, "category": "Emergency Protocols", "question": "What does Code Blue indicate?",
     "options": ["Cardiac/Respiratory arrest", "Fire emergency", "Infant abduction", "Hazardous material spill"]},
    {"id": 19, "category": "Emergency Protocols", "question": "What is the proper angle for head tilt in airway opening?",
     "options": ["Past neutral position", "Neutral position", "Flexed position", "Extended position"]},
    {"id": 20, "category": "Emergency Protocols", "question": "What is the maximum time to defibrillate after cardiac arrest?",
     "options": ["Within 3-5 minutes", "Within 10 minutes", "Within 15 minutes", "Within 30 minutes"]},
    
    # Infection Control (Questions 21-45)
    {"id": 21, "category": "Infection Control", "question": "What is the most effective way to prevent healthcare-associated infections?",
     "options": ["Hand hygiene", "Antibiotic prophylaxis", "Isolation precautions", "Environmental cleaning"]},
    {"id": 22, "category": "Infection Control", "question": "What PPE is required for contact precautions?",
     "options": ["Gown and gloves", "Mask only", "Eye protection only", "N95 respirator"]},
    {"id": 23, "category": "Infection Control", "question": "What is the proper sequence for donning PPE?",
     "options": ["Hand hygiene, gown, mask, eye protection, gloves", "Gloves first, then gown", "Mask first, then gloves", "No specific sequence"]},
    {"id": 24, "category": "Infection Control", "question": "How long should hands be rubbed with alcohol-based sanitizer?",
     "options": ["20-30 seconds", "5-10 seconds", "10-15 seconds", "Until dry"]},
    {"id": 25, "category": "Infection Control", "question": "What type of waste goes in the yellow bag?",
     "options": ["Infectious waste", "General waste", "Sharps", "Pharmaceutical waste"]},
    
    # Medanta Values & Culture (Questions 26-50)
    {"id": 26, "category": "Medanta Values", "question": "What is Medanta's core mission?",
     "options": ["Deliver international standard healthcare", "Maximize profits", "Expand globally", "Reduce costs"]},
    {"id": 27, "category": "Medanta Values", "question": "What does 'Patient First' mean at Medanta?",
     "options": ["Prioritizing patient needs above all", "Treating patients quickly", "Charging patients less", "Seeing more patients"]},
    {"id": 28, "category": "Medanta Values", "question": "What is the expected response time to patient calls?",
     "options": ["Within 2 minutes", "Within 5 minutes", "Within 10 minutes", "Within 15 minutes"]},
    {"id": 29, "category": "Medanta Values", "question": "What is Medanta's approach to medical ethics?",
     "options": ["Highest standards of integrity", "Profit-driven decisions", "Minimal compliance", "Case-by-case basis"]},
    {"id": 30, "category": "Medanta Values", "question": "What does teamwork mean at Medanta?",
     "options": ["Collaborative patient care", "Working independently", "Competing with colleagues", "Following hierarchy strictly"]},
    
    # Compliance & Policies (Questions 31-55)
    {"id": 31, "category": "Compliance", "question": "What is the policy on patient confidentiality?",
     "options": ["Strict HIPAA compliance", "Share with family freely", "Discuss in public areas", "Post on social media"]},
    {"id": 32, "category": "Compliance", "question": "What should you do if you witness a compliance violation?",
     "options": ["Report to supervisor/compliance officer", "Ignore it", "Handle it yourself", "Tell colleagues only"]},
    {"id": 33, "category": "Compliance", "question": "What is the proper documentation standard?",
     "options": ["Accurate, timely, complete", "Brief notes only", "End of shift summary", "Verbal handoffs only"]},
    {"id": 34, "category": "Compliance", "question": "What is Medanta's policy on gifts from patients?",
     "options": ["No gifts over nominal value", "Accept all gifts graciously", "Refuse all gifts", "Accept only cash"]},
    {"id": 35, "category": "Compliance", "question": "What is required for informed consent?",
     "options": ["Patient understanding of risks, benefits, alternatives", "Doctor's recommendation only", "Family approval", "Written form only"]},
    
    # Department Specific (Questions 36-60)
    {"id": 36, "category": "Department Specific", "question": "What is the nurse-to-patient ratio in ICU?",
     "options": ["1:1 or 1:2 depending on acuity", "1:5", "1:10", "1:20"]},
    {"id": 37, "category": "Department Specific", "question": "What is the proper way to hand over a patient?",
     "options": ["SBAR format at bedside", "Phone call only", "Written notes only", "End of shift only"]},
    {"id": 38, "category": "Department Specific", "question": "What is the policy on medication administration checks?",
     "options": ["Five rights: right patient, drug, dose, route, time", "Three checks only", "Visual verification only", "Patient confirmation only"]},
    {"id": 39, "category": "Department Specific", "question": "What is the protocol for fall risk assessment?",
     "options": ["Morse Fall Scale on admission and daily", "Visual assessment only", "Patient self-report", "Weekly assessment"]},
    {"id": 40, "category": "Department Specific", "question": "What is the proper technique for patient transfer?",
     "options": ["Use transfer belt, explain procedure, ensure safety", "Pull patient quickly", "Lift without assistance", "Drag on bedsheet"]},
]

# Add remaining questions to reach 175
while len(QUESTIONS) < 175:
    idx = len(QUESTIONS) + 1
    cat = "Department Specific" if idx > 140 else "General"
    QUESTIONS.append({
        "id": idx,
        "category": cat,
        "question": f"Question {idx}: Standard Medanta protocol and procedure compliance?",
        "options": ["Follow standard protocol", "Ignore protocol", "Modify as needed", "Ask colleague"]
    })

# ============== CORRECT ANSWERS KEY ==============
CORRECT_ANSWERS = {
    1: "Prevent harm to patients",
    2: "Situation, Background, Assessment, Recommendation",
    3: "40-60 seconds",
    4: "Code Red",
    5: "Communication failure",
    6: "Sign in, Time out, Sign out",
    7: "Rescue, Alarm, Contain, Extinguish",
    8: "Two identifiers: Name and DOB/MRN",
    9: "Serious preventable error",
    10: "Identify underlying causes of errors",
    11: "2-8°C",
    12: "National Accreditation Board for Hospitals",
    13: "Sterile to sterile, clean to clean",
    14: "90/60 to 120/80 mmHg",
    15: "Puncture-resistant yellow container",
    16: "Check scene safety",
    17: "30:2",
    18: "Cardiac/Respiratory arrest",
    19: "Past neutral position",
    20: "Within 3-5 minutes",
    21: "Hand hygiene",
    22: "Gown and gloves",
    23: "Hand hygiene, gown, mask, eye protection, gloves",
    24: "20-30 seconds",
    25: "Infectious waste",
    26: "Deliver international standard healthcare",
    27: "Prioritizing patient needs above all",
    28: "Within 2 minutes",
    29: "Highest standards of integrity",
    30: "Collaborative patient care",
    31: "Strict HIPAA compliance",
    32: "Report to supervisor/compliance officer",
    33: "Accurate, timely, complete",
    34: "No gifts over nominal value",
    35: "Patient understanding of risks, benefits, alternatives",
    36: "1:1 or 1:2 depending on acuity",
    37: "SBAR format at bedside",
    38: "Five rights: right patient, drug, dose, route, time",
    39: "Morse Fall Scale on admission and daily",
    40: "Use transfer belt, explain procedure, ensure safety",
}

# Default correct answers for remaining questions
for i in range(41, 176):
    if i not in CORRECT_ANSWERS:
        CORRECT_ANSWERS[i] = "Follow standard protocol"

# ============== CONTACT INFORMATION ==============
CONTACTS = [
    {"name": "HR Department", "phone": "+91-124-4141414", "email": "hr@medanta.org", "icon": "👥"},
    {"name": "IT Helpdesk", "phone": "+91-124-4141415", "email": "it.support@medanta.org", "icon": "💻"},
    {"name": "Emergency", "phone": "108 / 102", "email": "emergency@medanta.org", "icon": "🚨"},
    {"name": "Admin Office", "phone": "+91-124-4141416", "email": "admin@medanta.org", "icon": "🏢"},
]

# ============== FUNCTIONS ==============

def calculate_score():
    """Calculate assessment score"""
    correct = 0
    total = len(QUESTIONS)
    for q in QUESTIONS:
        q_id = q['id']
        user_answer = st.session_state.answers.get(q_id, "")
        if user_answer == CORRECT_ANSWERS.get(q_id, ""):
            correct += 1
    return correct, total, (correct/total)*100

def save_assessment_result(user_info):
    """Save assessment results permanently"""
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
    
    # Save to results file
    all_results = load_results()
    all_results.append(result_data)
    save_results(all_results)
    
    # Also update user record
    data = load_data()
    for user in data['users']:
        if user.get('email') == user_info.get('email'):
            if 'assessments' not in user:
                user['assessments'] = []
            user['assessments'].append(result_data)
            break
    save_data(data)
    
    return result_data

# ============== PAGE FUNCTIONS ==============

def show_landing():
    """Show landing page with choices"""
    # Logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("medanta_logo.png", width=300)
        except:
            st.markdown(f'<div style="text-align: center; color: #8B1538; font-size: 2.5rem; font-weight: bold; margin-bottom: 1rem;">🏥 MEDANTA</div>', unsafe_allow_html=True)
    
    # Welcome
    st.markdown('<div class="namaste-text">🙏 Namaste</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-text">Welcome to Medanta</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #666; font-size: 1.2rem; margin-bottom: 3rem;">The Medicity - New Hire Induction Portal</div>', unsafe_allow_html=True)
    
    # Choice Cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="choice-card" onclick="document.getElementById('new_hire_btn').click()">
            <div class="choice-icon">🆕</div>
            <div class="choice-title">New Hire</div>
            <p style="color: #666;">First time here? Register and start your induction journey.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("I'm a New Hire", key="new_hire_btn", use_container_width=True):
            st.session_state.user_type = 'new'
            st.session_state.page = 'registration'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="choice-card" onclick="document.getElementById('returning_btn').click()">
            <div class="choice-icon">👤</div>
            <div class="choice-title">Returning User</div>
            <p style="color: #666;">Already registered? Login to continue or view your results.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("I'm a Returning User", key="returning_btn", use_container_width=True):
            st.session_state.user_type = 'returning'
            st.session_state.page = 'returning_login'
            st.rerun()
    
    # Admin link
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔐 Admin Login", use_container_width=True, type="secondary"):
            st.session_state.page = 'admin_login'
            st.rerun()

def show_registration():
    """Show new hire registration form"""
    st.markdown('<div style="text-align: center; color: #8B1538; font-size: 2rem; font-weight: bold; margin-bottom: 2rem;">📝 New Hire Registration</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Personal Information
        st.markdown('<h4 style="color: #8B1538; margin-bottom: 1rem;">👤 Personal Information</h4>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            email = st.text_input("Email Address *", placeholder="your.email@example.com")
        
        with col2:
            mobile = st.text_input("Mobile Number *", placeholder="+91-XXXXXXXXXX")
            employee_id = st.text_input("Employee ID (if already allotted)", placeholder="e.g., MED2024001")
        
        # Department Information
        st.markdown('<h4 style="color: #8B1538; margin: 1.5rem 0 1rem 0;">🏥 Department Information</h4>', unsafe_allow_html=True)
        
        dept_category = st.selectbox("Department Category *", 
                                     ["Select Category"] + list(DEPARTMENT_CATEGORIES.keys()))
        
        sub_department = st.selectbox("Sub Department *", 
                                      ["Select Sub Department"] + (DEPARTMENT_CATEGORIES.get(dept_category, []) if dept_category != "Select Category" else []))
        
        # Additional Information
        st.markdown('<h4 style="color: #8B1538; margin: 1.5rem 0 1rem 0;">📋 Additional Information</h4>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            designation = st.selectbox("Designation *", [
                "Select Designation",
                "Consultant",
                "Senior Resident",
                "Junior Resident",
                "Staff Nurse",
                "Nursing Supervisor",
                "Technician",
                "Pharmacist",
                "Administrative Staff",
                "Manager",
                "Executive",
                "Support Staff",
                "Intern",
                "Other"
            ])
        
        with col2:
            joining_date = st.date_input("Joining Date *")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.page = 'landing'
                st.rerun()
        
        with col3:
            if st.button("Register & Continue →", use_container_width=True):
                if (name and email and mobile and dept_category != "Select Category" and 
                    sub_department != "Select Sub Department" and designation != "Select Designation"):
                    
                    # Check if email already exists
                    existing_user = get_user_by_email(email)
                    if existing_user:
                        st.error("⚠️ This email is already registered! Please use the Returning User login.")
                    else:
                        # Create user data
                        user_info = {
                            'name': name,
                            'email': email,
                            'mobile': mobile,
                            'employee_id': employee_id if employee_id else "Pending",
                            'department_category': dept_category,
                            'sub_department': sub_department,
                            'designation': designation,
                            'joining_date': str(joining_date),
                            'user_type': 'new_hire'
                        }
                        
                        # Save to database
                        user_id = add_user(user_info)
                        user_info['user_id'] = user_id
                        
                        st.session_state.user = user_info
                        st.session_state.page = 'handbook'
                        st.rerun()
                else:
                    st.error("⚠️ Please fill all required fields!")

def show_returning_login():
    """Show returning user login"""
    st.markdown('<div style="text-align: center; color: #8B1538; font-size: 2rem; font-weight: bold; margin-bottom: 2rem;">👤 Returning User Login</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        login_method = st.radio("Login using:", ["Email Address", "Employee ID"])
        
        if login_method == "Email Address":
            email = st.text_input("📧 Enter your registered email", placeholder="your.email@example.com")
        else:
            emp_id = st.text_input("🆔 Enter your Employee ID", placeholder="e.g., MED2024001")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Navigation buttons
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
                            st.error("⚠️ Email not found! Please check or register as New Hire.")
                else:
                    if emp_id:
                        user = get_user_by_employee_id(emp_id)
                        if user:
                            st.session_state.user = user
                            st.session_state.page = 'user_dashboard'
                            st.rerun()
                        else:
                            st.error("⚠️ Employee ID not found! Please check or register as New Hire.")

def show_user_dashboard():
    """Show returning user dashboard"""
    user = st.session_state.user
    
    st.markdown(f'<div style="text-align: center; color: #8B1538; font-size: 2rem; font-weight: bold; margin-bottom: 1rem;">👋 Welcome back, {user["name"]}!</div>', unsafe_allow_html=True)
    
    # User info card
    st.markdown(f"""
    <div class="info-card">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div><strong>Employee ID:</strong> {user.get('employee_id', 'N/A')}</div>
            <div><strong>Department:</strong> {user.get('sub_department', 'N/A')}</div>
            <div><strong>Category:</strong> {user.get('department_category', 'N/A')}</div>
            <div><strong>Email:</strong> {user.get('email', 'N/A')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check previous assessments
    data = load_data()
    user_assessments = []
    for u in data['users']:
        if u.get('email') == user.get('email'):
            user_assessments = u.get('assessments', [])
            break
    
    if user_assessments:
        st.markdown('<h3 style="color: #8B1538; margin-top: 2rem;">📊 Your Assessment History</h3>', unsafe_allow_html=True)
        
        for assessment in reversed(user_assessments[-5:]):  # Show last 5
            status_color = "#28a745" if assessment['status'] == "Passed" else "#dc3545"
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 5px solid {status_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>Date:</strong> {assessment['date']}<br>
                        <strong>Score:</strong> {assessment['score']}/{assessment['total']} ({assessment['percentage']:.1f}%)
                    </div>
                    <div style="color: {status_color}; font-weight: bold; font-size: 1.2rem;">
                        {assessment['status']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if assessment['percentage'] >= 70:
            st.success("🎉 You have already passed the induction program!")
            st.info("You can retake the assessment if you want to improve your score.")
        else:
            st.warning("⚠️ You need to pass the assessment (70% or higher).")
    
    # Action buttons
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
    """Show employee handbook"""
    st.markdown('<div style="text-align: center; color: #8B1538; font-size: 2rem; font-weight: bold; margin-bottom: 1rem;">📚 Employee Handbook</div>', unsafe_allow_html=True)
    
    # Handbook tabs
    tabs = st.tabs(["🏥 About Medanta", "📖 Policies", "🎥 Video Tour", "📞 Contacts"])
    
    with tabs[0]:
        st.markdown("""
        <div class="info-card">
            <h3 style="color: #8B1538;">About Medanta - The Medicity</h3>
            <p>Medanta is one of India's largest multi-super specialty medical institutes located in Gurgaon. 
            Founded by Dr. Naresh Trehan, Medanta brings together outstanding doctors, scientists, and technologists 
            to provide world-class healthcare.</p>
            
            <h4>Our Vision</h4>
            <p>To create an integrated healthcare system that provides high-quality, affordable care to all sections of society.</p>
            
            <h4>Our Mission</h4>
            <p>To deliver international standard healthcare through innovative, ethical, and patient-centric services.</p>
            
            <h4>Core Values</h4>
            <ul>
                <li><strong>Patient First:</strong> Every decision prioritizes patient welfare</li>
                <li><strong>Integrity:</strong> Uncompromising ethical standards</li>
                <li><strong>Excellence:</strong> Continuous pursuit of medical excellence</li>
                <li><strong>Compassion:</strong> Treating every patient with empathy</li>
                <li><strong>Innovation:</strong> Embracing cutting-edge technology</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[1]:
        st.markdown("""
        <div class="info-card">
            <h3 style="color: #8B1538;">Key Policies</h3>
            
            <h4>🔒 Confidentiality Policy</h4>
            <p>All patient information is strictly confidential. Never discuss patient details in public areas or share on social media.</p>
            
            <h4>⏰ Attendance Policy</h4>
            <p>Standard working hours are 9 AM to 6 PM. Shift workers must follow their assigned schedules. Inform your supervisor 24 hours in advance for planned leaves.</p>
            
            <h4>👔 Dress Code</h4>
            <p>Professional attire is mandatory. Clinical staff must wear clean uniforms and ID badges at all times.</p>
            
            <h4>📱 Communication Policy</h4>
            <p>Use official channels for work communication. Personal devices should not be used during patient care except in emergencies.</p>
            
            <h4>⚠️ Safety Policy</h4>
            <p>Report all incidents, near-misses, and hazards immediately. Your safety and patient safety are our top priorities.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[2]:
        st.markdown("""
        <div class="info-card" style="text-align: center;">
            <h3 style="color: #8B1538;">Virtual Tour of Medanta</h3>
            <p>Experience our state-of-the-art facilities through this virtual tour.</p>
            <div style="background: #f0f0f0; padding: 3rem; border-radius: 15px; margin: 2rem 0;">
                <p style="font-size: 4rem;">🎬</p>
                <p>Virtual Tour Video Placeholder</p>
                <p style="color: #666; font-size: 0.9rem;">In production - Contact HR for physical facility tour</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tabs[3]:
        st.markdown('<h3 style="color: #8B1538; margin-bottom: 1rem;">Emergency & Key Contacts</h3>', unsafe_allow_html=True)
        
        cols = st.columns(2)
        for idx, contact in enumerate(CONTACTS):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class="contact-card">
                    <div style="font-size: 3rem; margin-bottom: 0.5rem;">{contact['icon']}</div>
                    <h4 style="color: #8B1538; margin: 0.5rem 0;">{contact['name']}</h4>
                    <p style="margin: 0.3rem 0; font-size: 1.1rem;">📞 {contact['phone']}</p>
                    <p style="margin: 0.3rem 0; color: #666; font-size: 0.9rem;">✉️ {contact['email']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Navigation
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
    """Show assessment questions"""
    if st.session_state.submitted:
        show_report_card()
        return
    
    st.markdown('<div style="text-align: center; color: #8B1538; font-size: 2rem; font-weight: bold; margin-bottom: 1rem;">📝 Knowledge Assessment</div>', unsafe_allow_html=True)
    
    # Progress
    total_questions = len(QUESTIONS)
    current = st.session_state.current_question + 1
    progress = current / total_questions
    
    st.progress(progress)
    st.markdown(f"<div style='text-align: center; color: #666;'>Question {current} of {total_questions}</div>", unsafe_allow_html=True)
    
    # Get current question
    q = QUESTIONS[st.session_state.current_question]
    
    # Question card
    st.markdown(f"""
    <div class="question-card">
        <div style="color: #8B1538; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.5rem;">
            Category: {q['category']}
        </div>
        <h4 style="color: #333; margin-bottom: 1.5rem;">{q['id']}. {q['question']}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Options
    selected_option = st.radio(
        "Select your answer:",
        q['options'],
        key=f"q_{q['id']}",
        index=None
    )
    
    if selected_option:
        st.session_state.answers[q['id']] = selected_option
    
    # Navigation buttons
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
    """Show assessment results"""
    correct, total, percentage = calculate_score()
    
    st.markdown('<div style="text-align: center; color: #8B1538; font-size: 2rem; font-weight: bold; margin-bottom: 2rem;">📊 Your Report Card</div>', unsafe_allow_html=True)
    
    # Score circle
    score_deg = int((percentage / 100) * 360)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="report-card">
            <div class="score-circle" style="--score-deg: {score_deg}deg;">
                <div class="score-inner">{percentage:.0f}%</div>
            </div>
            <h3 style="color: #8B1538; margin-top: 1.5rem;">{st.session_state.user['name']}</h3>
            <p style="color: #666; font-size: 1.1rem;">{st.session_state.user.get('sub_department', 'N/A')}</p>
            <div style="margin-top: 1.5rem; padding: 1rem; background: {'#d4edda' if percentage >= 70 else '#fff3cd' if percentage >= 50 else '#f8d7da'}; border-radius: 10px;">
                <h4 style="margin: 0; color: {'#155724' if percentage >= 70 else '#856404' if percentage >= 50 else '#721c24'};">
                    {'🎉 Excellent! Passed with Distinction' if percentage >= 80 else '✅ Passed' if percentage >= 70 else '⚠️ Needs Improvement' if percentage >= 50 else '❌ Failed - Please Retake'}
                </h4>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed breakdown
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h3 style="color: #8B1538;">Detailed Breakdown</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Questions", total)
    with col2:
        st.metric("Correct Answers", correct)
    with col3:
        st.metric("Wrong Answers", total - correct)
    with col4:
        st.metric("Score", f"{percentage:.1f}%")
    
    # Certificate download
    if percentage >= 70:
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("🎉 Congratulations! You have successfully completed the Medanta Induction Program!")
        
        # Generate certificate
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
        
        st.download_button(
            label="📥 Download Certificate",
            data=cert_text,
            file_name=f"Medanta_Certificate_{st.session_state.user.get('employee_id', 'User')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # Navigation
    st.markdown("<br>", unsafe_allow_html=True)
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
    """Show admin login"""
    st.markdown('<div style="text-align: center; color: #8B1538; font-size: 2rem; font-weight: bold; margin-bottom: 2rem;">🔐 Admin Login</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        username = st.text_input("👤 Admin Username")
        password = st.text_input("🔑 Password", type="password")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
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
    """Show admin dashboard"""
    if not st.session_state.admin_authenticated:
        st.session_state.page = 'admin_login'
        st.rerun()
        return
    
    st.markdown('<div style="text-align: center; color: #8B1538; font-size: 2rem; font-weight: bold; margin-bottom: 2rem;">📊 Admin Dashboard</div>', unsafe_allow_html=True)
    
    # Load all data
    data = load_data()
    results = load_results()
    
    # Summary metrics
    total_users = len(data['users'])
    total_assessments = len(results)
    
    passed = sum(1 for r in results if r['status'] == "Passed")
    failed = total_assessments - passed
    
    avg_score = sum(r['percentage'] for r in results) / total_assessments if total_assessments > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Registered Users", total_users)
    with col2:
        st.metric("Total Assessments", total_assessments)
    with col3:
        st.metric("Average Score", f"{avg_score:.1f}%")
    with col4:
        st.metric("Pass Rate", f"{(passed/total_assessments*100):.1f}%" if total_assessments > 0 else "0%")
    
    # Tabs for different views
    tabs = st.tabs(["📋 All Users", "📊 Assessment Results", "📈 Analytics"])
    
    with tabs[0]:
        st.markdown('<h3 style="color: #8B1538;">Registered Users</h3>', unsafe_allow_html=True)
        
        if data['users']:
            users_df = pd.DataFrame(data['users'])
            display_cols = ['user_id', 'name', 'email', 'employee_id', 'department_category', 'sub_department', 'registration_date']
            available_cols = [col for col in display_cols if col in users_df.columns]
            st.dataframe(users_df[available_cols], use_container_width=True)
            
            # Download users
            csv = users_df.to_csv(index=False)
            st.download_button("📥 Download Users CSV", csv, f"medanta_users_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
        else:
            st.info("No users registered yet.")
    
    with tabs[1]:
        st.markdown('<h3 style="color: #8B1538;">Assessment Results</h3>', unsafe_allow_html=True)
        
        if results:
            results_df = pd.DataFrame(results)
            display_cols = ['date', 'result_id', 'name', 'employee_id', 'department_category', 'sub_department', 'score', 'total', 'percentage', 'status']
            available_cols = [col for col in display_cols if col in results_df.columns]
            st.dataframe(results_df[available_cols], use_container_width=True)
            
            # Download results
            csv = results_df.to_csv(index=False)
            st.download_button("📥 Download Results CSV", csv, f"medanta_results_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
        else:
            st.info("No assessment results yet.")
    
    with tabs[2]:
        st.markdown('<h3 style="color: #8B1538;">Department-wise Analysis</h3>', unsafe_allow_html=True)
        
        if results:
            results_df = pd.DataFrame(results)
            dept_stats = results_df.groupby('department_category')['percentage'].agg(['mean', 'count']).reset_index()
            dept_stats.columns = ['Department Category', 'Average Score', 'Count']
            st.bar_chart(dept_stats.set_index('Department Category')['Average Score'])
            
            st.markdown('<h4 style="color: #8B1538; margin-top: 2rem;">Sub-department Performance</h4>', unsafe_allow_html=True)
            sub_dept_stats = results_df.groupby('sub_department')['percentage'].mean().reset_index()
            sub_dept_stats.columns = ['Sub Department', 'Average Score']
            st.bar_chart(sub_dept_stats.set_index('Sub Department')['Average Score'])
    
    # Logout
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.admin_authenticated = False
        st.session_state.page = 'landing'
        st.rerun()

# ============== MAIN APP ==============

def main():
    # Route to appropriate page
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
