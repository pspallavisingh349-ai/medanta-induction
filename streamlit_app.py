import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import hashlib

# Page config
st.set_page_config(
    page_title="Medanta Induction Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS with animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {font-family: 'Poppins', sans-serif;}
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Animated Header */
    .hero-section {
        text-align: center;
        padding: 60px 20px;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .logo-container {
        width: 150px;
        height: 150px;
        margin: 0 auto 30px auto;
        background: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
        50% { transform: scale(1.05); box-shadow: 0 30px 80px rgba(0,0,0,0.4); }
    }
    
    .namaste-text {
        font-size: 4em;
        font-weight: 700;
        margin: 0;
        animation: slideInDown 1s ease-out, float 3s ease-in-out infinite;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
    }
    
    .welcome-text {
        font-size: 2em;
        font-weight: 300;
        margin: 10px 0;
        animation: slideInUp 1s ease-out 0.5s both, glow 2s ease-in-out infinite;
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
        50% { transform: translateY(-10px); }
    }
    
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 20px rgba(255,255,255,0.5); }
        50% { text-shadow: 0 0 40px rgba(255,255,255,0.8), 0 0 60px rgba(255,255,255,0.6); }
    }
    
    /* Glass Cards */
    .glass-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 40px;
        margin: 20px 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    }
    
    /* Portal Buttons */
    .portal-btn {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 20px 40px;
        border-radius: 50px;
        font-size: 1.2em;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(245,87,108,0.4);
        width: 100%;
    }
    
    .portal-btn:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 15px 40px rgba(245,87,108,0.6);
    }
    
    .portal-btn.admin {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        box-shadow: 0 10px 30px rgba(79,172,254,0.4);
    }
    
    .portal-btn.admin:hover {
        box-shadow: 0 15px 40px rgba(79,172,254,0.6);
    }
    
    /* Form Styling */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #e0e0e0;
        padding: 15px;
        font-size: 16px;
        transition: all 0.3s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102,126,234,0.1);
    }
    
    /* Begin Journey Button */
    .journey-btn {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border: none;
        padding: 20px 60px;
        border-radius: 50px;
        font-size: 1.3em;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(17,153,142,0.4);
        width: 100%;
        margin-top: 20px;
    }
    
    .journey-btn:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 20px 50px rgba(17,153,142,0.6);
    }
    
    /* Dashboard Cards */
    .dash-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .dash-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    }
    
    .dash-icon {
        font-size: 3em;
        margin-bottom: 15px;
    }
    
    .dash-title {
        font-size: 1.3em;
        font-weight: 600;
        color: #2d3748;
    }
    
    /* Progress Bar */
    .progress-container {
        background: #e0e0e0;
        border-radius: 20px;
        height: 30px;
        overflow: hidden;
        margin: 20px 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #11998e, #38ef7d);
        border-radius: 20px;
        transition: width 0.5s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    
    /* Contact Cards */
    .contact-card {
        background: rgba(255,255,255,0.95);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #e53e3e;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .contact-card.it {border-left-color: #3182ce;}
    .contact-card.salary {border-left-color: #d69e2e;}
    .contact-card.onboard {border-left-color: #38a169;}
    .contact-card.training {border-left-color: #805ad5; background: linear-gradient(135deg, #f0fff4, #e6fffa);}
    
    .contact-number {color: #e53e3e; font-weight: bold; font-size: 1.2em;}
    .contact-number.green {color: #38a169;}
    .contact-number.blue {color: #3182ce;}
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .namaste-text {font-size: 2.5em;}
        .welcome-text {font-size: 1.2em;}
        .logo-container {width: 100px; height: 100px;}
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'admin' not in st.session_state:
    st.session_state.admin = None
if 'assessment_attempts' not in st.session_state:
    st.session_state.assessment_attempts = 0
if 'assessment_passed' not in st.session_state:
    st.session_state.assessment_passed = False

DATA_FILE = "employees.json"
ASSESSMENT_LINKS = {
    "nursing": "https://github.com/your-repo/nursing-assessment",
    "hr": "https://github.com/your-repo/hr-assessment",
    "default": "https://github.com/your-repo/general-assessment"
}

# Hash passwords (in production, use proper auth)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Admin credentials (hashed)
ADMIN_CREDENTIALS = {
    "pallavi.singh@medanta.org": hash_password("Pallavi@2024"),
    "rohit.singh@medanta.org": hash_password("Rohit@2024")
}

# Load/save data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# LANDING PAGE
if st.session_state.page == 'landing':
    st.markdown("""
    <div class="hero-section">
        <div class="logo-container">
            <img src="Medanta Lucknow Logo.jpg" width="130" height="130" 
                 onerror="this.src='https://www.medanta.org/images/medanta-logo.png'; this.onerror=function(){this.parentElement.innerHTML='🏥';}" 
                 style="border-radius:50%;">
        </div>
        <h1 class="namaste-text">Namaste! 🙏</h1>
        <p class="welcome-text">Welcome to Medanta</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Choose Your Portal")
        
        if st.button("👤 Employee Portal", use_container_width=True):
            st.session_state.page = 'employee_login'
            st.rerun()
        
        st.write("")
        
        if st.button("🔐 Admin Portal", use_container_width=True):
            st.session_state.page = 'admin_login'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Contacts
        st.markdown("---")
        st.subheader("📞 Key Contacts")
        
        contacts = [
            ("EMR/HIS Query", "Mr. Surjendra", "9883111600", "🔴"),
            ("IT Helpdesk", "Internal Extension", "1010", "🔵"),
            ("Salary Related", "HR Department", "9560719167", "🟡"),
            ("Onboarding", "HR Business Partner", "Contact HRBP", "🟢"),
            ("Training", "Dr. Pallavi & Mr. Rohit", "7860955988 / 7275181822", "🟣")
        ]
        
        for title, person, contact, color in contacts:
            st.markdown(f"""
            <div class="contact-card {'training' if 'Training' in title else ''}">
                <b>{title}</b><br>
                {person}<br>
                <span class="contact-number {'green' if 'Training' in title else 'blue' if 'IT' in title else ''}">{contact}</span>
            </div>
            """, unsafe_allow_html=True)

# EMPLOYEE LOGIN/REGISTRATION
elif st.session_state.page == 'employee_login':
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h1 style="font-size: 2.5em; margin: 0;">Begin Your Journey</h1>
        <p style="font-size: 1.2em; opacity: 0.9;">Enter your details to start</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        with st.form("employee_registration"):
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            email = st.text_input("Email Address *", placeholder="your.email@medanta.org")
            department = st.text_input("Department *", placeholder="e.g., Nursing, Cardiology, HR")
            mobile = st.text_input("Mobile Number *", placeholder="+91 XXXXX XXXXX")
            
            col_back, col_submit = st.columns([1,2])
            
            with col_back:
                if st.form_submit_button("← Back"):
                    st.session_state.page = 'landing'
                    st.rerun()
            
            with col_submit:
                submitted = st.form_submit_button("🚀 Begin Your Journey")
            
            if submitted:
                if not all([name, email, department, mobile]):
                    st.error("Please fill all required fields!")
                else:
                    # Check if already exists
                    data = load_data()
                    existing = [e for e in data if e['email'] == email]
                    
                    if existing:
                        st.session_state.user = existing[0]
                    else:
                        # Create new user
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
                            "learning_journey": []
                        }
                        data.append(new_user)
                        save_data(data)
                        st.session_state.user = new_user
                    
                    st.session_state.page = 'employee_dashboard'
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# EMPLOYEE DASHBOARD
elif st.session_state.page == 'employee_dashboard':
    user = st.session_state.user
    
    st.markdown(f"""
    <div class="hero-section" style="padding: 20px;">
        <h1 style="font-size: 2em;">Welcome, {user['name']}!</h1>
        <p>{user['department']} Department</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress Overview
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📊 Your Learning Progress")
    
    progress = 0
    if user.get('handbook_viewed'):
        progress += 33
    if user.get('assessment_passed'):
        progress += 33
    if user.get('departmental_induction'):
        progress += 34
    
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress}%;">{progress}% Complete</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Handbook", "✅" if user.get('handbook_viewed') else "⏳")
    with col2:
        st.metric("Assessment", "✅" if user.get('assessment_passed') else "⏳")
    with col3:
        st.metric("Dept Induction", "✅" if user.get('departmental_induction') else "⏳")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Dashboard Modules
    st.subheader("🎯 Learning Modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Handbook
        st.markdown('<div class="dash-card" onclick="window.location.href=\'#handbook\'">', unsafe_allow_html=True)
        st.markdown('<div class="dash-icon">📚</div>', unsafe_allow_html=True)
        st.markdown('<div class="dash-title">Employee Handbook</div>', unsafe_allow_html=True)
        if st.button("Access Handbook", key="handbook_btn"):
            st.session_state.page = 'handbook'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Assessment
        st.markdown('<div class="dash-card" style="margin-top: 20px;">', unsafe_allow_html=True)
        st.markdown('<div class="dash-icon">📝</div>', unsafe_allow_html=True)
        st.markdown('<div class="dash-title">Assessment</div>', unsafe_allow_html=True)
        status = "✅ Passed" if user.get('assessment_passed') else f"Attempt {user.get('attempts', 0) + 1}"
        st.caption(f"Status: {status}")
        if not user.get('assessment_passed') and st.button("Start Assessment", key="assessment_btn"):
            st.session_state.page = 'assessment'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Learning Journey
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="dash-icon">🎯</div>', unsafe_allow_html=True)
        st.markdown('<div class="dash-title">Learning Journey</div>', unsafe_allow_html=True)
        if st.button("View Journey", key="journey_btn"):
            st.session_state.page = 'learning_journey'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Report Card
        st.markdown('<div class="dash-card" style="margin-top: 20px;">', unsafe_allow_html=True)
        st.markdown('<div class="dash-icon">📊</div>', unsafe_allow_html=True)
        st.markdown('<div class="dash-title">Report Card</div>', unsafe_allow_html=True)
        if user.get('assessment_passed'):
            if st.button("View Report", key="report_btn"):
                st.session_state.page = 'report_card'
                st.rerun()
        else:
            st.caption("Complete assessment first")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Logout
    if st.button("🚪 Logout", type="secondary"):
        st.session_state.user = None
        st.session_state.page = 'landing'
        st.rerun()

# HANDBOOK PAGE
elif st.session_state.page == 'handbook':
    st.subheader("📚 Employee Handbook")
    
    # Update user
    if st.session_state.user:
        data = load_data()
        for u in data:
            if u['email'] == st.session_state.user['email']:
                u['handbook_viewed'] = True
                st.session_state.user = u
                break
        save_data(data)
    
    # Embed FlippingBook
    st.components.v1.iframe(
        src="https://online.flippingbook.com/view/652486186/",
        height=700,
        scrolling=True
    )
    
    col1, col2 = st.columns([1,4])
    with col1:
        if st.button("← Back to Dashboard"):
            st.session_state.page = 'employee_dashboard'
            st.rerun()

# ASSESSMENT PAGE
elif st.session_state.page == 'assessment':
    st.subheader("📝 Department Assessment")
    
    dept = st.session_state.user.get('department', '').lower()
    assessment_link = ASSESSMENT_LINKS.get(dept, ASSESSMENT_LINKS['default'])
    
    st.info(f"Department: {st.session_state.user['department']}")
    st.write("Complete the assessment to proceed. You need 80% to pass.")
    
    # Mock assessment (replace with actual GitHub links)
    with st.form("assessment"):
        st.write("**Sample Questions:**")
        
        q1 = st.radio("Q1. Patient safety is:", 
            ["Optional", "Everyone's responsibility", "Only doctor's job", "Nursing duty only"],
            index=None)
        
        q2 = st.radio("Q2. In case of emergency:", 
            ["Panic", "Follow protocol", "Ignore", "Leave"],
            index=None)
        
        q3 = st.radio("Q3. Medanta's core value:", 
            ["Profit", "Patient First", "Speed", "Cost"],
            index=None)
        
        q4 = st.radio("Q4. HIPAA compliance means:", 
            ["Share data freely", "Protect patient privacy", "Ignore rules", "Sell data"],
            index=None)
        
        q5 = st.radio("Q5. Teamwork is:", 
            ["Not important", "Essential", "Optional", "Waste of time"],
            index=None)
        
        submitted = st.form_submit_button("Submit Assessment")
        
        if submitted:
            if None in [q1, q2, q3, q4, q5]:
                st.error("Answer all questions!")
            else:
                # Calculate score
                score = 0
                correct = ["Everyone's responsibility", "Follow protocol", "Patient First", 
                          "Protect patient privacy", "Essential"]
                answers = [q1, q2, q3, q4, q5]
                
                for i, ans in enumerate(answers):
                    if ans == correct[i]:
                        score += 20
                
                # Update user
                data = load_data()
                for u in data:
                    if u['email'] == st.session_state.user['email']:
                        u['attempts'] = u.get('attempts', 0) + 1
                        u['assessment_score'] = score
                        if score >= 80:
                            u['assessment_passed'] = True
                            st.session_state.assessment_passed = True
                        st.session_state.user = u
                        break
                save_data(data)
                
                if score >= 80:
                    st.balloons()
                    st.success(f"🎉 Congratulations! You scored {score}%. You passed!")
                    st.session_state.assessment_passed = True
                else:
                    st.error(f"❌ You scored {score}%. You need 80% to pass. Please reattempt.")
                
                if st.button("Back to Dashboard"):
                    st.session_state.page = 'employee_dashboard'
                    st.rerun()

# LEARNING JOURNEY
elif st.session_state.page == 'learning_journey':
    st.subheader("🎯 Your Learning Journey")
    
    journey_items = [
        ("✅", "Welcome to Medanta", "Completed", "green"),
        ("✅", "Employee Handbook", "Viewed" if st.session_state.user.get('handbook_viewed') else "Pending", 
         "green" if st.session_state.user.get('handbook_viewed') else "orange"),
        ("⏳", "Department Assessment", "Passed" if st.session_state.user.get('assessment_passed') else "In Progress",
         "green" if st.session_state.user.get('assessment_passed') else "blue"),
        ("📋", "Departmental Induction", "Pending", "gray"),
        ("🎓", "Certificate of Completion", "Locked", "gray")
    ]
    
    for icon, title, status, color in journey_items:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 15px; margin: 10px 0; 
                    border-left: 5px solid {color}; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 1.5em;">{icon}</span>
                    <b style="margin-left: 10px;">{title}</b>
                </div>
                <span style="color: {color}; font-weight: bold;">{status}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# REPORT CARD
elif st.session_state.page == 'report_card':
    st.subheader("📊 Your Report Card")
    
    user = st.session_state.user
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Assessment Score", f"{user.get('assessment_score', 0)}%")
    with col2:
        st.metric("Attempts", user.get('attempts', 0))
    with col3:
        st.metric("Status", "PASSED" if user.get('assessment_passed') else "PENDING")
    
    st.markdown("---")
    
    if user.get('assessment_passed'):
        st.success("🎉 You have successfully completed the induction program!")
        st.balloons()
        
        # Generate certificate button
        st.download_button(
            label="📜 Download Certificate",
            data=f"CERTIFICATE OF COMPLETION\n\nThis certifies that\n{user['name']}\nhas successfully completed the Medanta Induction Program.\n\nDate: {datetime.now().strftime('%B %d, %Y')}",
            file_name=f"certificate_{user['name'].replace(' ', '_')}.txt",
            mime="text/plain"
        )
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# ADMIN LOGIN
elif st.session_state.page == 'admin_login':
    st.markdown("""
    <div class="hero-section" style="padding: 30px;">
        <h1 style="font-size: 2.5em;">Admin Portal</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        with st.form("admin_login"):
            email = st.text_input("Admin Email", placeholder="pallavi.singh@medanta.org")
            password = st.text_input("Password", type="password")
            
            col_back, col_submit = st.columns([1,2])
            
            with col_back:
                if st.form_submit_button("← Back"):
                    st.session_state.page = 'landing'
                    st.rerun()
            
            with col_submit:
                submitted = st.form_submit_button("Login", type="primary")
            
            if submitted:
                if email in ADMIN_CREDENTIALS:
                    if hash_password(password) == ADMIN_CREDENTIALS[email]:
                        st.session_state.admin = email
                        st.session_state.page = 'admin_dashboard'
                        st.rerun()
                    else:
                        st.error("Invalid password!")
                else:
                    st.error("Unauthorized email!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ADMIN DASHBOARD
elif st.session_state.page == 'admin_dashboard':
    st.subheader(f"🔐 Admin Dashboard - {st.session_state.admin}")
    
    data = load_data()
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Employees", len(data))
    with col2:
        passed = len([e for e in data if e.get('assessment_passed')])
        st.metric("Passed Assessment", passed)
    with col3:
        pending = len([e for e in data if not e.get('assessment_passed')])
        st.metric("Pending", pending)
    with col4:
        avg_score = sum(e.get('assessment_score', 0) for e in data) / len(data) if data else 0
        st.metric("Avg Score", f"{avg_score:.1f}%")
    
    # Employee table
    st.markdown("---")
    st.subheader("Employee Records")
    
    if data:
        df = pd.DataFrame(data)
        df_display = df[['name', 'email', 'department', 'assessment_score', 'assessment_passed', 'attempts']].copy()
        df_display.columns = ['Name', 'Email', 'Department', 'Score', 'Passed', 'Attempts']
        df_display['Passed'] = df_display['Passed'].map({True: '✅', False: '❌'})
        
        st.dataframe(df_display, use_container_width=True)
        
        # Download
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download Report",
            csv,
            f"medanta_report_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    else:
        st.info("No employees registered yet.")
    
    if st.button("🚪 Logout"):
        st.session_state.admin = None
        st.session_state.page = 'landing'
        st.rerun()
