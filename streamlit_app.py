import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import base64
from pathlib import Path

# Page config - YOURS
st.set_page_config(
    page_title="Medanta Induction Portal",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Create data folder
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Function to load logo - ADDED
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

# Load questions from EXCEL (your Question_bank.xlsx) - ADDED
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
    except Exception as e:
        st.error(f"Error loading questions: {str(e)}")
        return {}

# Get logo source
logo_src = get_logo_src()

# YOUR CSS - UNCHANGED + small animation additions
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #B8E3FF 0%, #E0F2FE 50%, #DBEAFE 100%);
        min-height: 100vh;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 800px;
    }
    
    .element-container {
        margin-bottom: 0 !important;
    }
    
    .hero-section {
        text-align: center;
        padding: 10px;
    }
    
    .logo-img {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        background: white;
        padding: 8px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        border: 4px solid white;
        object-fit: contain;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .namaste-text {
        font-size: 2.5em;
        font-weight: 700;
        margin: 10px 0;
        color: #1e3a5f;
        animation: slideInDown 1s ease-out;
    }
    
    .welcome-text {
        font-size: 1.3em;
        font-weight: 400;
        margin: 5px 0 15px 0;
        color: #3b5998;
        animation: slideInUp 1s ease-out 0.5s both;
    }
    
    @keyframes slideInDown {
        from { opacity: 0; transform: translateY(-50px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(50px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        border: none;
        padding: 15px;
        border-radius: 12px;
        font-size: 1.1em;
        font-weight: 600;
        width: 100%;
        margin: 8px 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        transition: all 0.3s;
    }
    
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
    }
    
    div[data-testid="stButton"] > button[kind="secondary"] {
        background: linear-gradient(135deg, #0891B2 0%, #0E7490 100%);
    }
    
    .stContainer {
        background: linear-gradient(135deg, #E0F2FE 0%, #BFDBFE 100%);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
        border: 2px solid rgba(255,255,255,0.5);
    }
    
    h1, h2, h3 {color: #1e3a5f !important;}
    
    .row-widget.stHorizontalBlock {
        gap: 0.5rem;
    }
    
    /* Added for questions */
    .question-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

# Session state - YOURS + added current_module_idx
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'admin' not in st.session_state:
    st.session_state.admin = None
if 'assessment_submitted' not in st.session_state:
    st.session_state.assessment_submitted = False
if 'assessment_result' not in st.session_state:
    st.session_state.assessment_result = None
if 'current_module_idx' not in st.session_state:
    st.session_state.current_module_idx = 0

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

# Load questions from EXCEL
questions_data = load_questions()

# LANDING PAGE - YOURS with logo added
if st.session_state.page == 'landing':
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="hero-section">', unsafe_allow_html=True)
        
        # Display logo - ADDED
        if logo_src:
            st.markdown(f'<img src="{logo_src}" class="logo-img" alt="Medanta Logo">', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:60px; text-align:center;">🏥</div>', unsafe_allow_html=True)
        
        st.markdown('<h1 class="namaste-text">Namaste! 🙏</h1>', unsafe_allow_html=True)
        st.markdown('<p class="welcome-text">Welcome to Medanta</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with st.container():
        st.subheader("Choose Your Portal")
        
        if st.button("👤 Employee Portal", use_container_width=True):
            st.session_state.page = 'employee_login'
            st.rerun()
        
        if st.button("🔐 Admin Portal", use_container_width=True):
            st.session_state.page = 'admin_login'
            st.rerun()
    
    with st.container():
        st.markdown("---")
        st.subheader("📞 Key Contacts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("**EMR/HIS** - Mr. Surjendra\n\n📱 9883111600")
            st.info("**Salary** - HR Dept\n\n📱 9560719167")
        
        with col2:
            st.info("**IT Helpdesk**\n\n☎️ 1010")
            st.info("**Onboarding** - HRBP\n\nContact HRBP")
        
        st.success("**Training** - Dr. Pallavi & Mr. Rohit\n\n📞 7860955988 | 7275181822")

# EMPLOYEE LOGIN - YOURS unchanged
elif st.session_state.page == 'employee_login':
    st.markdown('<div class="hero-section"><h1 style="font-size: 2em; color:#1e3a5f;">Employee Portal</h1></div>', unsafe_allow_html=True)
    
    with st.container():
        st.subheader("🆕 New Joinee")
        st.write("First time? Register here:")
        
        with st.form("employee_reg"):
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            email = st.text_input("Email Address *", placeholder="your.email@medanta.org")
            department = st.text_input("Department *", placeholder="e.g., Nursing, Cardiology, HR")
            mobile = st.text_input("Mobile Number *", placeholder="+91 XXXXX XXXXX")
            
            submitted = st.form_submit_button("🚀 Begin Your Journey")
            
            if submitted:
                if not all([name, email, department, mobile]):
                    st.error("Please fill all required fields!")
                else:
                    data = load_data()
                    existing = [e for e in data if e['email'] == email]
                    
                    if existing:
                        st.error("Email already registered! Use 'Returning User' option below.")
                    else:
                        new_user = {
                            "id": len(data) + 1,
                            "name": name,
                            "email": email,
                            "department": department,
                            "mobile": mobile,
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
    
    with st.container():
        st.markdown("---")
        st.subheader("🔙 Returning User")
        st.write("Already registered? Login with your email:")
        
        with st.form("employee_login_form"):
            login_email = st.text_input("Email Address", placeholder="your.email@medanta.org")
            
            col1, col2 = st.columns([1,2])
            
            with col1:
                if st.form_submit_button("← Back to Home"):
                    st.session_state.page = 'landing'
                    st.rerun()
            
            with col2:
                login_submitted = st.form_submit_button("Login")
            
            if login_submitted:
                if not login_email:
                    st.error("Please enter your email!")
                else:
                    data = load_data()
                    user = [e for e in data if e['email'] == login_email]
                    
                    if user:
                        st.session_state.user = user[0]
                        st.success(f"Welcome back, {user[0]['name']}!")
                        st.session_state.page = 'employee_dashboard'
                        st.rerun()
                    else:
                        st.error("Email not found! Please register first.")

# EMPLOYEE DASHBOARD - YOURS with assessment button updated
elif st.session_state.page == 'employee_dashboard':
    user = st.session_state.user
    
    st.markdown(f'<div class="hero-section"><h1 style="font-size: 1.8em; color:#1e3a5f;">Welcome, {user["name"]}!</h1><p style="color:#3b5998;">{user["department"]} Department</p></div>', unsafe_allow_html=True)
    
    progress = 0
    if user.get('handbook_viewed'): progress += 33
    if user.get('assessment_passed'): progress += 33
    if user.get('departmental_induction'): progress += 34
    
    with st.container():
        st.subheader("📊 Your Progress")
        st.progress(progress / 100)
        st.write(f"**{progress}% Complete**")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Handbook", "✅" if user.get('handbook_viewed') else "⏳")
        col2.metric("Assessment", "✅" if user.get('assessment_passed') else "⏳")
        col3.metric("Dept Induction", "✅" if user.get('departmental_induction') else "⏳")
    
    st.subheader("🎯 Learning Modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📚 Employee Handbook", use_container_width=True):
            data = load_data()
            for u in data:
                if u['email'] == user['email']:
                    u['handbook_viewed'] = True
                    st.session_state.user = u
                    break
            save_data(data)
            st.session_state.page = 'handbook'
            st.rerun()
        
        # UPDATED - Multi-module assessment
        if st.button("📝 Assessment", use_container_width=True):
            st.session_state.assessment_submitted = False
            st.session_state.assessment_result = None
            st.session_state.current_module_idx = user.get('current_module', 0)
            st.session_state.page = 'assessment'
            st.rerun()
    
    with col2:
        if st.button("🎯 Learning Journey", use_container_width=True):
            st.session_state.page = 'learning_journey'
            st.rerun()
        
        if st.button("📊 Report Card", use_container_width=True):
            if user.get('assessment_passed'):
                st.session_state.page = 'report_card'
                st.rerun()
            else:
                st.warning("Complete assessment first!")
    
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.user = None
        st.session_state.page = 'landing'
        st.rerun()

# HANDBOOK - YOURS
elif st.session_state.page == 'handbook':
    st.subheader("📚 Employee Handbook")
    
    st.components.v1.iframe(
        src="https://online.flippingbook.com/view/652486186/",
        height=700,
        scrolling=True
    )
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# ASSESSMENT - UPDATED for 172 questions with 80% pass rule
elif st.session_state.page == 'assessment':
    st.subheader("📝 Assessment")
    
    user = st.session_state.user
    
    if not questions_data:
        st.error("⚠️ Could not load questions. Please check Question_bank.xlsx file.")
        if st.button("← Back"):
            st.session_state.page = 'employee_dashboard'
            st.rerun()
        st.stop()
    
    module_ids = list(questions_data.keys())
    current_idx = st.session_state.current_module_idx
    
    # Check if all modules complete
    if current_idx >= len(module_ids):
        st.balloons()
        st.success("🎉 Congratulations! You have completed all assessments!")
        
        # Update user as passed
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
    
    # Show progress
    st.write(f"**Module {current_idx + 1} of {len(module_ids)}: {current_module['name']}**")
    st.progress(current_idx / len(module_ids))
    st.write(f"Questions: {len(questions)} | Need 80% to pass")
    
    if user.get('assessment_score'):
        st.info(f"Previous Score: {user['assessment_score']:.0f}% | Attempts: {user.get('attempts', 0)}")
    
    if not st.session_state.assessment_submitted:
        with st.form("assessment_form"):
            answers = {}
            correct_count = 0
            
            for i, q in enumerate(questions):
                st.markdown(f'<div class="question-box">', unsafe_allow_html=True)
                st.write(f"**Q{i+1}. {q['question']}**")
                
                answer = st.radio(
                    f"Select answer for Q{i+1}:",
                    q['options'],
                    index=None,
                    key=f"q_{current_idx}_{i}",
                    label_visibility="collapsed"
                )
                answers[i] = answer
                
                if answer == q['options'][q['correct']]:
                    correct_count += 1
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Submit Assessment")
            
            if submitted:
                if None in answers.values():
                    st.error("Answer all questions!")
                    st.stop()
                
                score = correct_count
                total = len(questions)
                percentage = (score / total) * 100
                
                st.session_state.assessment_result = {
                    'score': score,
                    'total': total,
                    'percentage': percentage
                }
                st.session_state.assessment_submitted = True
                
                # Save attempt
                data = load_data()
                for u in data:
                    if u['email'] == user['email']:
                        u['attempts'] = u.get('attempts', 0) + 1
                        if percentage >= 80:
                            u['current_module'] = current_idx + 1
                            # Only mark passed if last module
                            if current_idx + 1 >= len(module_ids):
                                u['assessment_passed'] = True
                                u['assessment_score'] = percentage
                        break
                save_data(data)
                
                st.rerun()
    
    else:
        # Show results
        result = st.session_state.assessment_result
        percentage = result['percentage']
        score = result['score']
        total = result['total']
        
        st.markdown("---")
        st.subheader("📊 Result")
        
        if percentage >= 80:
            st.balloons()
            st.success(f"🎉 Congratulations! You passed with {percentage:.0f}%!")
            st.info("Click 'Next Module' to continue.")
            
            if st.button("➡️ Next Module", type="primary"):
                st.session_state.assessment_submitted = False
                st.session_state.assessment_result = None
                st.session_state.current_module_idx += 1
                st.rerun()
        else:
            st.error(f"❌ You scored {percentage:.0f}%. You need 80% to pass.")
            st.info("🔄 Don't worry! Review and try again.")
            
            if st.button("🔄 Reattempt Module"):
                st.session_state.assessment_submitted = False
                st.session_state.assessment_result = None
                st.rerun()
        
        if st.button("← Back to Dashboard"):
            st.session_state.assessment_submitted = False
            st.session_state.assessment_result = None
            st.session_state.page = 'employee_dashboard'
            st.rerun()

# LEARNING JOURNEY - YOURS
elif st.session_state.page == 'learning_journey':
    st.subheader("🎯 Learning Journey")
    
    user = st.session_state.user
    
    items = [
        ("✅", "Welcome", "Completed", "green"),
        ("✅" if user.get('handbook_viewed') else "⏳", "Handbook", 
         "Completed" if user.get('handbook_viewed') else "Pending", 
         "green" if user.get('handbook_viewed') else "orange"),
        ("✅" if user.get('assessment_passed') else "⏳", "Assessment",
         "Passed" if user.get('assessment_passed') else "In Progress",
         "green" if user.get('assessment_passed') else "blue"),
        ("⏳", "Departmental Induction", "Pending", "gray"),
        ("🔒", "Certificate", "Locked", "gray")
    ]
    
    for icon, title, status, color in items:
        if color == "green":
            st.success(f"**{icon} {title}** - {status}")
        elif color == "orange":
            st.warning(f"**{icon} {title}** - {status}")
        elif color == "blue":
            st.info(f"**{icon} {title}** - {status}")
        else:
            st.write(f"**{icon} {title}** - {status}")
    
    if st.button("← Back"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# REPORT CARD - YOURS
elif st.session_state.page == 'report_card':
    st.subheader("📊 Report Card")
    
    user = st.session_state.user
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Score", f"{user.get('assessment_score', 0):.0f}%")
    col2.metric("Attempts", user.get('attempts', 0))
    col3.metric("Status", "PASSED" if user.get('assessment_passed') else "PENDING")
    
    if user.get('assessment_passed'):
        st.success("🎉 Congratulations! You completed the induction!")
        st.balloons()
        
        cert = f"""MEDANTA INDUCTION CERTIFICATE
    
This certifies that
{user['name']}
has successfully completed the Medanta Induction Program.

Department: {user['department']}
Score: {user['assessment_score']:.0f}%
Date: {datetime.now().strftime('%B %d, %Y')}

Authorized by: Dr. Pallavi & Mr. Rohit
"""
        st.download_button("📜 Download Certificate", cert, 
                          f"certificate_{user['name']}.txt", "text/plain")
    
    if st.button("← Back"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# ADMIN LOGIN - YOURS
elif st.session_state.page == 'admin_login':
    st.markdown('<div class="hero-section"><h1 style="font-size: 2em; color:#1e3a5f;">Admin Portal</h1></div>', unsafe_allow_html=True)
    
    with st.container():
        with st.form("admin_login"):
            email = st.text_input("Admin Email")
            password = st.text_input("Password", type="password")
            
            col1, col2 = st.columns([1,2])
            
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

# ADMIN DASHBOARD - YOURS
elif st.session_state.page == 'admin_dashboard':
    st.subheader(f"🔐 Admin Dashboard - {st.session_state.admin}")
    
    data = load_data()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", len(data))
    col2.metric("Passed", len([e for e in data if e.get('assessment_passed')]))
    col3.metric("Pending", len([e for e in data if not e.get('assessment_passed')]))
    avg = sum(e.get('assessment_score', 0) for e in data) / len(data) if data else 0
    col4.metric("Avg Score", f"{avg:.1f}%")
    
    st.markdown("---")
    if data:
        df = pd.DataFrame(data)
        display_df = df[['name', 'email', 'department', 'assessment_score', 'assessment_passed', 'attempts']].copy()
        display_df.columns = ['Name', 'Email', 'Department', 'Score', 'Passed', 'Attempts']
        display_df['Passed'] = display_df['Passed'].map({True: '✅', False: '❌'})
        st.dataframe(display_df, use_container_width=True)
        
        csv = df.to_csv(index=False)
        st.download_button("📥 Download Report", csv, 
                          f"report_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    else:
        st.info("No data yet.")
    
    if st.button("🚪 Logout"):
        st.session_state.admin = None
        st.session_state.page = 'landing'
        st.rerun()
