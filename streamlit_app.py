import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import base64

# Page config
st.set_page_config(
    page_title="Medanta Induction Portal",
    page_icon="🏥",
    layout="centered",  # Changed to centered for better layout
    initial_sidebar_state="collapsed"
)

# Function to load logo
def get_logo_src():
    try:
        with open("Medanta Lucknow Logo.jpg", "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    except:
        return "https://www.medanta.org/images/medanta-logo.png"

# Load questions from CSV
def load_questions():
    try:
        df = pd.read_csv("questions.csv")
        df = df.dropna(subset=['Question'])
        
        questions = []
        for idx, row in df.iterrows():
            q_id = int(row['Q No'])
            question_text = str(row['Question'])
            
            options = [
                str(row['Option A']),
                str(row['Option B']),
                str(row['Option C']),
                str(row['Option D'])
            ]
            
            answer_letter = str(row['Answer']).strip().upper()
            correct_index = ord(answer_letter) - ord('A')
            
            questions.append({
                "id": q_id,
                "question": question_text,
                "options": options,
                "correct": correct_index
            })
        
        return questions
        
    except Exception as e:
        st.error(f"Error loading questions: {str(e)}")
        return []

# Get logo source
logo_src = get_logo_src()

# CSS - Fixed to remove empty patches
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #B8E3FF 0%, #E0F2FE 50%, #DBEAFE 100%);
        min-height: 100vh;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Remove ALL extra padding */
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 800px;
    }
    
    /* Remove gap between elements */
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
    
    .namaste-text {
        font-size: 2.5em;
        font-weight: 700;
        margin: 10px 0;
        color: #1e3a5f;
        animation: slideInDown 1s ease-out, float 3s ease-in-out infinite;
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
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    
    /* Style for buttons - NO HTML WRAPPERS */
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
    
    /* Cards using Streamlit native components */
    .stContainer {
        background: linear-gradient(135deg, #E0F2FE 0%, #BFDBFE 100%);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
        border: 2px solid rgba(255,255,255,0.5);
    }
    
    h1, h2, h3 {color: #1e3a5f !important;}
    
    /* Remove empty space from columns */
    .row-widget.stHorizontalBlock {
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Session state
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

DATA_FILE = "employees.json"

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

# LANDING PAGE - NO HTML WRAPPERS THAT CAUSE PATCHES
if st.session_state.page == 'landing':
    # Hero with Logo
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="hero-section">', unsafe_allow_html=True)
        
        # Display logo
        try:
            if logo_src.startswith("data:"):
                st.markdown(f'<img src="{logo_src}" class="logo-img" alt="Medanta Logo">', unsafe_allow_html=True)
            else:
                st.image(logo_src, width=100, use_column_width=False)
        except:
            st.markdown('<div style="font-size:60px; text-align:center;">🏥</div>', unsafe_allow_html=True)
        
        st.markdown('<h1 class="namaste-text">Namaste! 🙏</h1>', unsafe_allow_html=True)
        st.markdown('<p class="welcome-text">Welcome to Medanta</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Portal Selection - USING ST.CONTAINER INSTEAD OF HTML DIVS
    with st.container():
        st.subheader("Choose Your Portal")
        
        if st.button("👤 Employee Portal", use_container_width=True):
            st.session_state.page = 'employee_login'
            st.rerun()
        
        if st.button("🔐 Admin Portal", use_container_width=True):
            st.session_state.page = 'admin_login'
            st.rerun()
    
    # Contacts - COMPACT
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

# EMPLOYEE LOGIN
elif st.session_state.page == 'employee_login':
    st.markdown('<div class="hero-section"><h1 style="font-size: 2em; color:#1e3a5f;">Employee Portal</h1></div>', unsafe_allow_html=True)
    
    # New Joinee
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
                            "handbook_viewed": False
                        }
                        data.append(new_user)
                        save_data(data)
                        st.session_state.user = new_user
                        st.session_state.page = 'employee_dashboard'
                        st.rerun()
    
    # Returning User
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

# EMPLOYEE DASHBOARD
elif st.session_state.page == 'employee_dashboard':
    user = st.session_state.user
    
    st.markdown(f'<div class="hero-section"><h1 style="font-size: 1.8em; color:#1e3a5f;">Welcome, {user["name"]}!</h1><p style="color:#3b5998;">{user["department"]} Department</p></div>', unsafe_allow_html=True)
    
    # Progress
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
    
    # Modules
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
        
        if st.button("📝 Assessment", use_container_width=True):
            st.session_state.assessment_submitted = False
            st.session_state.assessment_result = None
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

# HANDBOOK
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

# ASSESSMENT
elif st.session_state.page == 'assessment':
    st.subheader("📝 Assessment")
    
    user = st.session_state.user
    questions = load_questions()
    
    if user.get('assessment_score') is not None:
        st.info(f"Previous Score: {user['assessment_score']:.0f}% | Attempts: {user.get('attempts', 0)}")
        if user.get('assessment_passed'):
            st.success("✅ You have already passed! You can reattempt for practice.")
        else:
            st.warning("❌ You need 80% to pass. Try again!")
    
    st.write("Answer all questions. You need 80% to pass.")
    st.caption(f"Total Questions: {len(questions)}")
    
    if not st.session_state.assessment_submitted:
        with st.form("assessment_form"):
            answers = {}
            
            for q in questions:
                st.write(f"**Q{q['id']}. {q['question']}**")
                answers[q['id']] = st.radio(
                    f"q_{q['id']}",
                    q['options'],
                    index=None,
                    key=f"question_{q['id']}",
                    label_visibility="collapsed"
                )
                st.write("")
            
            submitted = st.form_submit_button("Submit Assessment")
            
            if submitted:
                if None in answers.values():
                    st.error("Answer all questions!")
                    st.stop()
                else:
                    score = 0
                    total = len(questions)
                    for q in questions:
                        if answers[q['id']] == q['options'][q['correct']]:
                            score += 1
                    
                    percentage = (score / total) * 100
                    
                    st.session_state.assessment_result = {
                        'score': score,
                        'total': total,
                        'percentage': percentage
                    }
                    st.session_state.assessment_submitted = True
                    
                    data = load_data()
                    for u in data:
                        if u['email'] == user['email']:
                            u['attempts'] = u.get('attempts', 0) + 1
                            u['assessment_score'] = percentage
                            if percentage >= 80:
                                u['assessment_passed'] = True
                            st.session_state.user = u
                            break
                    save_data(data)
                    
                    st.rerun()
    
    else:
        result = st.session_state.assessment_result
        percentage = result['percentage']
        score = result['score']
        total = result['total']
        
        st.markdown("---")
        st.subheader("📊 Result")
        
        if percentage >= 80:
            st.balloons()
            st.success(f"🎉 Congratulations! You Passed!")
        else:
            st.error(f"❌ You did not pass.")
        
        st.write(f"**Score: {percentage:.0f}% ({score}/{total})**")
        st.info("You need 80% to pass.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Reattempt Assessment"):
                st.session_state.assessment_submitted = False
                st.session_state.assessment_result = None
                st.rerun()
        
        with col2:
            if st.button("← Back to Dashboard"):
                st.session_state.assessment_submitted = False
                st.session_state.assessment_result = None
                st.session_state.page = 'employee_dashboard'
                st.rerun()

# LEARNING JOURNEY
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

# REPORT CARD
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

# ADMIN LOGIN
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

# ADMIN DASHBOARD
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
