import streamlit as st
import pandas as pd
import json
import base64
from datetime import datetime
from PIL import Image
import io

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
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(139, 21, 56, 0.3);
    }
    
    /* Input Styling */
    .stTextInput>div>div>input, .stSelectbox>div>div>select {
        border-radius: 10px;
        border: 2px solid #D4AF37;
        background: white;
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
    .contact-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
    }
    
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
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .welcome-text { font-size: 2rem; }
        .namaste-text { font-size: 2.5rem; }
        .info-card { padding: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# ============== SESSION STATE INITIALIZATION ==============
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# ============== MEDANTA LOGO (BASE64) ==============
# Replace this with your actual base64 encoded logo
MEDANTA_LOGO = """data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjgwIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjx0ZXh0IHg9IjEwIiB5PSI1MCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjI0IiBmaWxsPSIjOEIxNTM4IiBmb250LXdlaWdodD0iYm9sZCI+TUVEQU5UQTwvdGV4dD48L3N2Zz4="""

# ============== QUESTIONS DATA ==============
# All 175 questions organized by category
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
    # ... (Adding sample questions - you'll need to add all 175)
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
    
    # Clinical Excellence (Questions 26-50)
    {"id": 26, "category": "Clinical Excellence", "question": "What is the standard temperature for medication refrigerator?",
     "options": ["2-8°C", "0-5°C", "10-15°C", "Room temperature"]},
    {"id": 27, "category": "Clinical Excellence", "question": "What does NABH stand for?",
     "options": ["National Accreditation Board for Hospitals", "National Association of Better Healthcare", "National Accreditation for Better Hospitals", "National Advisory Board for Health"]},
    {"id": 28, "category": "Clinical Excellence", "question": "What is the correct technique for aseptic dressing change?",
     "options": ["Sterile to sterile, clean to clean", "Clean to sterile", "Sterile to clean", "No specific technique"]},
    {"id": 29, "category": "Clinical Excellence", "question": "What is the normal range for adult blood pressure?",
     "options": ["90/60 to 120/80 mmHg", "80/50 to 100/60 mmHg", "100/70 to 140/90 mmHg", "120/80 to 160/100 mmHg"]},
    {"id": 30, "category": "Clinical Excellence", "question": "What is the proper disposal method for sharps?",
     "options": ["Puncture-resistant yellow container", "Regular trash bin", "Recycling bin", "Biohazard bag"]},
    
    # Emergency Protocols (Questions 51-75)
    {"id": 51, "category": "Emergency Protocols", "question": "What is the first step in Basic Life Support (BLS)?",
     "options": ["Check scene safety", "Start chest compressions", "Call for help", "Check pulse"]},
    {"id": 52, "category": "Emergency Protocols", "question": "What is the compression-to-ventilation ratio for adult CPR?",
     "options": ["30:2", "15:2", "20:2", "40:2"]},
    {"id": 53, "category": "Emergency Protocols", "question": "What does Code Blue indicate?",
     "options": ["Cardiac/Respiratory arrest", "Fire emergency", "Infant abduction", "Hazardous material spill"]},
    {"id": 54, "category": "Emergency Protocols", "question": "What is the proper angle for head tilt in airway opening?",
     "options": ["Past neutral position", "Neutral position", "Flexed position", "Extended position"]},
    {"id": 55, "category": "Emergency Protocols", "question": "What is the maximum time to defibrillate after cardiac arrest?",
     "options": ["Within 3-5 minutes", "Within 10 minutes", "Within 15 minutes", "Within 30 minutes"]},
    
    # Infection Control (Questions 76-100)
    {"id": 76, "category": "Infection Control", "question": "What is the most effective way to prevent healthcare-associated infections?",
     "options": ["Hand hygiene", "Antibiotic prophylaxis", "Isolation precautions", "Environmental cleaning"]},
    {"id": 77, "category": "Infection Control", "question": "What PPE is required for contact precautions?",
     "options": ["Gown and gloves", "Mask only", "Eye protection only", "N95 respirator"]},
    {"id": 78, "category": "Infection Control", "question": "What is the proper sequence for donning PPE?",
     "options": ["Hand hygiene, gown, mask, eye protection, gloves", "Gloves first, then gown", "Mask first, then gloves", "No specific sequence"]},
    {"id": 79, "category": "Infection Control", "question": "How long should hands be rubbed with alcohol-based sanitizer?",
     "options": ["20-30 seconds", "5-10 seconds", "10-15 seconds", "Until dry"]},
    {"id": 80, "category": "Infection Control", "question": "What type of waste goes in the yellow bag?",
     "options": ["Infectious waste", "General waste", "Sharps", "Pharmaceutical waste"]},
    
    # Medanta Values & Culture (Questions 101-125)
    {"id": 101, "category": "Medanta Values", "question": "What is Medanta's core mission?",
     "options": ["Deliver international standard healthcare", "Maximize profits", "Expand globally", "Reduce costs"]},
    {"id": 102, "category": "Medanta Values", "question": "What does 'Patient First' mean at Medanta?",
     "options": ["Prioritizing patient needs above all", "Treating patients quickly", "Charging patients less", "Seeing more patients"]},
    {"id": 103, "category": "Medanta Values", "question": "What is the expected response time to patient calls?",
     "options": ["Within 2 minutes", "Within 5 minutes", "Within 10 minutes", "Within 15 minutes"]},
    {"id": 104, "category": "Medanta Values", "question": "What is Medanta's approach to medical ethics?",
     "options": ["Highest standards of integrity", "Profit-driven decisions", "Minimal compliance", "Case-by-case basis"]},
    {"id": 105, "category": "Medanta Values", "question": "What does teamwork mean at Medanta?",
     "options": ["Collaborative patient care", "Working independently", "Competing with colleagues", "Following hierarchy strictly"]},
    
    # Compliance & Policies (Questions 126-150)
    {"id": 126, "category": "Compliance", "question": "What is the policy on patient confidentiality?",
     "options": ["Strict HIPAA compliance", "Share with family freely", "Discuss in public areas", "Post on social media"]},
    {"id": 127, "category": "Compliance", "question": "What should you do if you witness a compliance violation?",
     "options": ["Report to supervisor/compliance officer", "Ignore it", "Handle it yourself", "Tell colleagues only"]},
    {"id": 128, "category": "Compliance", "question": "What is the proper documentation standard?",
     "options": ["Accurate, timely, complete", "Brief notes only", "End of shift summary", "Verbal handoffs only"]},
    {"id": 129, "category": "Compliance", "question": "What is Medanta's policy on gifts from patients?",
     "options": ["No gifts over nominal value", "Accept all gifts graciously", "Refuse all gifts", "Accept only cash"]},
    {"id": 130, "category": "Compliance", "question": "What is required for informed consent?",
     "options": ["Patient understanding of risks, benefits, alternatives", "Doctor's recommendation only", "Family approval", "Written form only"]},
    
    # Department Specific (Questions 151-175)
    {"id": 151, "category": "Department Specific", "question": "What is the nurse-to-patient ratio in ICU?",
     "options": ["1:1 or 1:2 depending on acuity", "1:5", "1:10", "1:20"]},
    {"id": 152, "category": "Department Specific", "question": "What is the proper way to hand over a patient?",
     "options": ["SBAR format at bedside", "Phone call only", "Written notes only", "End of shift only"]},
    {"id": 153, "category": "Department Specific", "question": "What is the policy on medication administration checks?",
     "options": ["Five rights: right patient, drug, dose, route, time", "Three checks only", "Visual verification only", "Patient confirmation only"]},
    {"id": 154, "category": "Department Specific", "question": "What is the protocol for fall risk assessment?",
     "options": ["Morse Fall Scale on admission and daily", "Visual assessment only", "Patient self-report", "Weekly assessment"]},
    {"id": 155, "category": "Department Specific", "question": "What is the proper technique for patient transfer?",
     "options": ["Use transfer belt, explain procedure, ensure safety", "Pull patient quickly", "Lift without assistance", "Drag on bedsheet"]},
]

# Add remaining questions to reach 175
for i in range(156, 176):
    QUESTIONS.append({
        "id": i,
        "category": "Department Specific",
        "question": f"Sample Question {i}: What is the standard protocol for departmental procedure {i}?",
        "options": ["Correct Answer", "Wrong Answer A", "Wrong Answer B", "Wrong Answer C"]
    })

# Fill in gaps to ensure we have exactly 175 questions
while len(QUESTIONS) < 175:
    idx = len(QUESTIONS) + 1
    QUESTIONS.append({
        "id": idx,
        "category": "General",
        "question": f"Question {idx}: Please refer to Medanta policies for complete information.",
        "options": ["Option A", "Option B", "Option C", "Option D"]
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
    26: "2-8°C",
    27: "National Accreditation Board for Hospitals",
    28: "Sterile to sterile, clean to clean",
    29: "90/60 to 120/80 mmHg",
    30: "Puncture-resistant yellow container",
    51: "Check scene safety",
    52: "30:2",
    53: "Cardiac/Respiratory arrest",
    54: "Past neutral position",
    55: "Within 3-5 minutes",
    76: "Hand hygiene",
    77: "Gown and gloves",
    78: "Hand hygiene, gown, mask, eye protection, gloves",
    79: "20-30 seconds",
    80: "Infectious waste",
    101: "Deliver international standard healthcare",
    102: "Prioritizing patient needs above all",
    103: "Within 2 minutes",
    104: "Highest standards of integrity",
    105: "Collaborative patient care",
    126: "Strict HIPAA compliance",
    127: "Report to supervisor/compliance officer",
    128: "Accurate, timely, complete",
    129: "No gifts over nominal value",
    130: "Patient understanding of risks, benefits, alternatives",
    151: "1:1 or 1:2 depending on acuity",
    152: "SBAR format at bedside",
    153: "Five rights: right patient, drug, dose, route, time",
    154: "Morse Fall Scale on admission and daily",
    155: "Use transfer belt, explain procedure, ensure safety",
}

# Default correct answer for remaining questions
for i in range(11, 176):
    if i not in CORRECT_ANSWERS:
        CORRECT_ANSWERS[i] = "Correct Answer" if i >= 156 else QUESTIONS[i-1]["options"][0]

# ============== CONTACT INFORMATION ==============
CONTACTS = [
    {"name": "HR Department", "phone": "+91-124-4141414", "email": "hr@medanta.org", "icon": "👥"},
    {"name": "IT Helpdesk", "phone": "+91-124-4141415", "email": "it.support@medanta.org", "icon": "💻"},
    {"name": "Emergency", "phone": "108 / 102", "email": "emergency@medanta.org", "icon": "🚨"},
    {"name": "Admin Office", "phone": "+91-124-4141416", "email": "admin@medanta.org", "icon": "🏢"},
]

# ============== FUNCTIONS ==============

def get_base64_of_bin_file(bin_file):
    """Convert binary file to base64 string"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def check_logo_exists():
    """Check if logo file exists and return path"""
    logo_paths = ['medanta_logo.png', 'medanta_logo.jpg', 'logo.png', 'assets/logo.png']
    for path in logo_paths:
        try:
            return path
        except:
            continue
    return None

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

def save_results():
    """Save assessment results"""
    correct, total, percentage = calculate_score()
    result_data = {
        "employee_id": st.session_state.user['employee_id'],
        "name": st.session_state.user['name'],
        "department": st.session_state.user['department'],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": correct,
        "total": total,
        "percentage": round(percentage, 2),
        "answers": st.session_state.answers
    }
    
    # Save to JSON file (in production, use database)
    try:
        with open('assessment_results.json', 'r') as f:
            all_results = json.load(f)
    except:
        all_results = []
    
    all_results.append(result_data)
    
    with open('assessment_results.json', 'w') as f:
        json.dump(all_results, f, indent=4)
    
    return result_data

def get_all_results():
    """Get all assessment results"""
    try:
        with open('assessment_results.json', 'r') as f:
            return json.load(f)
    except:
        return []

# ============== PAGE FUNCTIONS ==============

def show_welcome():
    """Show welcome page with animation"""
    # Logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("medanta_logo.png", width=300)
        except:
            st.markdown(f'<div style="text-align: center; color: #8B1538; font-size: 2rem; font-weight: bold;">🏥 MEDANTA</div>', unsafe_allow_html=True)
    
    # Animated Namaste
    st.markdown('<div class="namaste-text">🙏 Namaste</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-text">Welcome to Medanta</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #666; font-size: 1.2rem; margin-top: 1rem;">The Medicity - Where Healing Meets Innovation</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Welcome message
    st.markdown("""
    <div class="info-card" style="text-align: center;">
        <h3 style="color: #8B1538;">Your Journey Begins Here</h3>
        <p style="font-size: 1.1rem; color: #444;">
            Welcome to the Medanta family! This induction portal will guide you through everything you need to know 
            about our world-class healthcare institution, our values, protocols, and your role in delivering 
            exceptional patient care.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Start button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Begin Your Journey", key="start_btn", use_container_width=True):
            st.session_state.page = 'registration'
            st.rerun()

def show_registration():
    """Show registration form"""
    st.markdown('<div style="text-align: center; color: #8B1538; font-size: 2rem; font-weight: bold; margin-bottom: 2rem;">📝 New Hire Registration</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Full Name *", placeholder="Enter your full name")
            employee_id = st.text_input("🆔 Employee ID *", placeholder="e.g., MED2024001")
            email = st.text_input("📧 Email Address *", placeholder="your.name@medanta.org")
        
        with col2:
            department = st.selectbox("🏥 Department *", [
                "Select Department",
                "Nursing",
                "Medical Services",
                "Emergency Medicine",
                "ICU",
                "OT/CSSD",
                "Pharmacy",
                "Laboratory",
                "Radiology",
                "Administration",
                "HR",
                "Finance",
                "IT",
                "Housekeeping",
                "F&B Services",
                "Security",
                "Other"
            ])
            
            designation = st.selectbox("💼 Designation *", [
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
            
            joining_date = st.date_input("📅 Joining Date")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.page = 'welcome'
                st.rerun()
        
        with col3:
            if st.button("Continue →", use_container_width=True):
                if name and employee_id and email and department != "Select Department" and designation != "Select Designation":
                    st.session_state.user = {
                        'name': name,
                        'employee_id': employee_id,
                        'email': email,
                        'department': department,
                        'designation': designation,
                        'joining_date': str(joining_date)
                    }
                    st.session_state.page = 'handbook'
                    st.rerun()
                else:
                    st.error("⚠️ Please fill all required fields!")

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
            <p><strong>Key Facilities:</strong></p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 10px; border: 2px solid #D4AF37;">🏥 Main Hospital Block</div>
                <div style="background: white; padding: 1rem; border-radius: 10px; border: 2px solid #D4AF37;">🫀 Heart Institute</div>
                <div style="background: white; padding: 1rem; border-radius: 10px; border: 2px solid #D4AF37;">🧠 Neurosciences</div>
                <div style="background: white; padding: 1rem; border-radius: 10px; border: 2px solid #D4AF37;">🦴 Orthopedics</div>
                <div style="background: white; padding: 1rem; border-radius: 10px; border: 2px solid #D4AF37;">🧪 Advanced Labs</div>
                <div style="background: white; padding: 1rem; border-radius: 10px; border: 2px solid #D4AF37;">🍽️ Staff Cafeteria</div>
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
        if st.button("← Back to Registration", use_container_width=True):
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
                    save_results()
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
            <p style="color: #666; font-size: 1.1rem;">{st.session_state.user['department']}</p>
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
    
    # Category-wise performance
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h4 style="color: #8B1538;">Category-wise Performance</h4>', unsafe_allow_html=True)
    
    categories = {}
    for q in QUESTIONS:
        cat = q['category']
        if cat not in categories:
            categories[cat] = {'total': 0, 'correct': 0}
        categories[cat]['total'] += 1
        if st.session_state.answers.get(q['id']) == CORRECT_ANSWERS.get(q['id']):
            categories[cat]['correct'] += 1
    
    for cat, data in categories.items():
        cat_percentage = (data['correct'] / data['total']) * 100 if data['total'] > 0 else 0
        st.markdown(f"""
        <div style="margin: 0.5rem 0; padding: 1rem; background: white; border-radius: 10px; border-left: 5px solid {'#28a745' if cat_percentage >= 70 else '#ffc107' if cat_percentage >= 50 else '#dc3545'};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600; color: #333;">{cat}</span>
                <span style="font-weight: bold; color: {'#28a745' if cat_percentage >= 70 else '#ffc107' if cat_percentage >= 50 else '#dc3545'};">{data['correct']}/{data['total']} ({cat_percentage:.0f}%)</span>
            </div>
            <div style="margin-top: 0.5rem; background: #f0f0f0; height: 8px; border-radius: 4px;">
                <div style="width: {cat_percentage}%; height: 100%; background: {'#28a745' if cat_percentage >= 70 else '#ffc107' if cat_percentage >= 50 else '#dc3545'}; border-radius: 4px; transition: width 1s;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Certificate download
    if percentage >= 70:
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("🎉 Congratulations! You have successfully completed the Medanta Induction Program!")
        
        # Generate certificate data
        cert_data = f"""
        CERTIFICATE OF COMPLETION
        ----------------------------
        This certifies that
        
        {st.session_state.user['name']}
        
        has successfully completed the
        Medanta New Hire Induction Program
        
        Department: {st.session_state.user['department']}
        Score: {percentage:.1f}%
        Date: {datetime.now().strftime("%B %d, %Y")}
        """
        
        st.download_button(
            label="📥 Download Certificate",
            data=cert_data,
            file_name=f"Medanta_Certificate_{st.session_state.user['employee_id']}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    # Navigation
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🏠 Return to Home", use_container_width=True):
            st.session_state.page = 'welcome'
            st.session_state.user = None
            st.session_state.answers = {}
            st.session_state.current_question = 0
            st.session_state.submitted = False
            st.rerun()

def show_admin():
    """Show admin dashboard"""
    st.markdown('<div style="text-align: center; color: #8B1538; font-size: 2rem; font-weight: bold; margin-bottom: 2rem;">🔐 Admin Dashboard</div>', unsafe_allow_html=True)
    
    # Simple password protection (in production, use proper authentication)
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        password = st.text_input("Enter Admin Password", type="password")
        if st.button("Login"):
            if password == "medanta2024":  # Change this in production
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Invalid password!")
        return
    
    # Admin content
    results = get_all_results()
    
    if not results:
        st.info("No assessment results found yet.")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Assessments", len(results))
    with col2:
        avg_score = sum(r['percentage'] for r in results) / len(results)
        st.metric("Average Score", f"{avg_score:.1f}%")
    with col3:
        passed = sum(1 for r in results if r['percentage'] >= 70)
        st.metric("Passed", passed)
    with col4:
        failed = len(results) - passed
        st.metric("Needs Improvement", failed)
    
    # Results table
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h3 style="color: #8B1538;">Assessment Results</h3>', unsafe_allow_html=True)
    
    df = pd.DataFrame(results)
    if not df.empty:
        df = df[['date', 'employee_id', 'name', 'department', 'score', 'total', 'percentage']]
        df.columns = ['Date', 'Employee ID', 'Name', 'Department', 'Score', 'Total', 'Percentage']
        st.dataframe(df, use_container_width=True)
        
        # Download option
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV Report",
            data=csv,
            file_name=f"medanta_assessment_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # Department-wise analysis
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h3 style="color: #8B1538;">Department-wise Analysis</h3>', unsafe_allow_html=True)
    
    dept_stats = df.groupby('Department')['Percentage'].agg(['mean', 'count']).reset_index()
    dept_stats.columns = ['Department', 'Average Score', 'Count']
    st.bar_chart(dept_stats.set_index('Department')['Average Score'])
    
    if st.button("Logout", key="admin_logout"):
        st.session_state.admin_authenticated = False
        st.rerun()

# ============== MAIN APP ==============

def main():
    # Sidebar for navigation (hidden by default, shown only for admin)
    with st.sidebar:
        if st.session_state.page != 'welcome':
            st.markdown("### Navigation")
            if st.button("🏠 Home"):
                st.session_state.page = 'welcome'
                st.rerun()
            if st.button("🔐 Admin Portal"):
                st.session_state.page = 'admin'
                st.rerun()
    
    # Route to appropriate page
    if st.session_state.page == 'welcome':
        show_welcome()
    elif st.session_state.page == 'registration':
        show_registration()
    elif st.session_state.page == 'handbook':
        show_handbook()
    elif st.session_state.page == 'assessment':
        show_assessment()
    elif st.session_state.page == 'admin':
        show_admin()
    else:
        show_welcome()

if __name__ == "__main__":
    main()
