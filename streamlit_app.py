import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import hashlib
import base64

# Page config
st.set_page_config(
    page_title="Medanta Induction Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Medanta Logo Base64 (embedded so it always works)
MEDANTA_LOGO = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTUwIiBoZWlnaHQ9IjE1MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9ImdyYWQiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPjxzdG9wIG9mZnNldD0iMCUiIHN0b3AtY29sb3I9IiNkZTQzNWIiLz48c3RvcCBvZmZzZXQ9IjEwMCUiIHN0b3AtY29sb3I9IiNmNTdhNmMiLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48Y2lyY2xlIGN4PSI3NSIgY3k9Ijc1IiByPSI3MCIgZmlsbD0idXJsKCNncmFkKSIvPjx0ZXh0IHg9Ijc1IiB5PSI4NSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjE4IiBmaWxsPSJ3aGl0ZSIgZm9udC13ZWlnaHQ9ImJvbGQiIHRleHQtYW5jaG9yPSJtaWRkbGUiPk1FREFOVEE8L3RleHQ+PC9zdmc+"

# CSS
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }}
    
    #MainMenu, footer, header {{visibility: hidden;}}
    
    .hero-section {{
        text-align: center;
        padding: 40px 20px;
        color: white;
    }}
    
    .logo-img {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: white;
        padding: 10px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    
    .namaste-text {{
        font-size: 3.5em;
        font-weight: 700;
        margin: 0;
        animation: slideInDown 1s ease-out, float 3s ease-in-out infinite;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
    }}
    
    .welcome-text {{
        font-size: 1.8em;
        font-weight: 300;
        margin: 10px 0 30px 0;
        animation: slideInUp 1s ease-out 0.5s both, glow 2s ease-in-out infinite;
    }}
    
    @keyframes slideInDown {{
        from {{ opacity: 0; transform: translateY(-50px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes slideInUp {{
        from {{ opacity: 0; transform: translateY(50px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    @keyframes glow {{
        0%, 100% {{ text-shadow: 0 0 20px rgba(255,255,255,0.5); }}
        50% {{ text-shadow: 0 0 40px rgba(255,255,255,0.8); }}
    }}
    
    .glass-card {{
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 40px;
        margin: 20px auto;
        max-width: 600px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }}
    
    .portal-btn {{
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border: none;
        padding: 18px;
        border-radius: 12px;
        font-size: 1.2em;
        font-weight: 600;
        width: 100%;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    
    .portal-btn:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }}
    
    .portal-btn.admin {{
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }}
    
    .journey-btn {{
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 20px;
        border-radius: 50px;
        font-size: 1.3em;
        font-weight: 700;
        width: 100%;
        margin-top: 20px;
        cursor: pointer;
        box-shadow: 0 10px 30px rgba(245,87,108,0.4);
    }}
    
    .contact-section {{
        background: rgba(255,255,255,0.1);
        padding: 30px;
        border-radius: 20px;
        margin-top: 30px;
    }}
    
    .contact-card {{
        background: rgba(255,255,255,0.95);
        padding: 15px;
        border-radius: 12px;
        margin: 8px 0;
        border-left: 4px solid #e53e3e;
    }}
    
    .contact-card.it {{border-left-color: #3182ce;}}
    .contact-card.salary {{border-left-color: #d69e2e;}}
    .contact-card.onboard {{border-left-color: #38a169;}}
    .contact-card.training {{border-left-color: #805ad5; background: linear-gradient(135deg, #f0fff4, #e6fffa);}}
    
    @media (max-width: 768px) {{
        .namaste-text {{font-size: 2.5em;}}
        .welcome-text {{font-size: 1.2em;}}
        .logo-img {{width: 100px; height: 100px;}}
    }}
</style>
""", unsafe_allow_html=True)

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'admin' not in st.session_state:
    st.session_state.admin = None

DATA_FILE = "employees.json"

# Admin credentials (hashed)
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

# LANDING PAGE
if st.session_state.page == 'landing':
    # Hero Section with Logo
    st.markdown(f"""
    <div class="hero-section">
        <img src="{MEDANTA_LOGO}" class="logo-img" alt="Medanta Logo">
        <h1 class="namaste-text">Namaste! 🙏</h1>
        <p class="welcome-text">Welcome to Medanta</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Portal Selection
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Choose Your Portal")
    
    if st.button("👤 Employee Portal", use_container_width=True):
        st.session_state.page = 'employee_login'
        st.rerun()
    
    if st.button("🔐 Admin Portal", use_container_width=True):
        st.session_state.page = 'admin_login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Contacts
    st.markdown('<div class="contact-section">', unsafe_allow_html=True)
    st.subheader("📞 Key Contacts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="contact-card">
            <b>EMR/HIS Query</b><br>Mr. Surjendra<br>
            <span style="color:#e53e3e;font-weight:bold;">📱 9883111600</span>
        </div>
        <div class="contact-card salary">
            <b>Salary Related</b><br>HR Department<br>
            <span style="color:#e53e3e;font-weight:bold;">📱 9560719167</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="contact-card it">
            <b>IT Helpdesk</b><br>Internal Extension<br>
            <span style="color:#3182ce;font-weight:bold;">☎️ 1010</span>
        </div>
        <div class="contact-card onboard">
            <b>Onboarding Query</b><br>HR Business Partner<br>
            <span style="color:#38a169;font-weight:bold;">Contact your HRBP</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="contact-card training">
        <b>Training Related</b> - Dr. Pallavi & Mr. Rohit<br>
        <span style="color:#38a169;font-weight:bold;">📞 7860955988 | 7275181822</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# EMPLOYEE LOGIN
elif st.session_state.page == 'employee_login':
    st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 2.5em;">Begin Your Journey</h1>
        <p>Enter your details to get started</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    with st.form("employee_reg"):
        name = st.text_input("Full Name *", placeholder="Enter your full name")
        email = st.text_input("Email Address *", placeholder="your.email@medanta.org")
        department = st.text_input("Department *", placeholder="e.g., Nursing, Cardiology, HR")
        mobile = st.text_input("Mobile Number *", placeholder="+91 XXXXX XXXXX")
        
        col1, col2 = st.columns([1,2])
        
        with col1:
            if st.form_submit_button("← Back"):
                st.session_state.page = 'landing'
                st.rerun()
        
        with col2:
            submitted = st.form_submit_button("🚀 Begin Your Journey")
        
        if submitted:
            if not all([name, email, department, mobile]):
                st.error("Please fill all required fields!")
            else:
                data = load_data()
                existing = [e for e in data if e['email'] == email]
                
                if existing:
                    st.session_state.user = existing[0]
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
    
    # Progress
    progress = 0
    if user.get('handbook_viewed'): progress += 33
    if user.get('assessment_passed'): progress += 33
    if user.get('departmental_induction'): progress += 34
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📊 Your Progress")
    
    st.progress(progress / 100)
    st.write(f"**{progress}% Complete**")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Handbook", "✅" if user.get('handbook_viewed') else "⏳")
    col2.metric("Assessment", "✅" if user.get('assessment_passed') else "⏳")
    col3.metric("Dept Induction", "✅" if user.get('departmental_induction') else "⏳")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Modules
    st.subheader("🎯 Learning Modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📚 Employee Handbook", use_container_width=True):
            # Update handbook viewed
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
            if not user.get('assessment_passed'):
                st.session_state.page = 'assessment'
                st.rerun()
            else:
                st.success("Already passed!")
    
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
    st.info("Score 80% or higher to pass. You can reattempt if needed.")
    
    user = st.session_state.user
    
    with st.form("assessment_form"):
        q1 = st.radio("Q1. Patient safety is everyone's responsibility?", ["True", "False"], index=None)
        q2 = st.radio("Q2. Medanta's core value is?", ["Profit first", "Patient first", "Speed", "Cost"], index=None)
        q3 = st.radio("Q3. HIPAA protects?", ["Patient privacy", "Doctors", "Money", "Buildings"], index=None)
        q4 = st.radio("Q4. In emergency, you should?", ["Panic", "Follow protocol", "Run", "Hide"], index=None)
        q5 = st.radio("Q5. Teamwork is?", ["Optional", "Essential", "Not needed", "Waste"], index=None)
        
        col1, col2 = st.columns([1,2])
        
        with col1:
            if st.form_submit_button("← Back"):
                st.session_state.page = 'employee_dashboard'
                st.rerun()
        
        with col2:
            submitted = st.form_submit_button("Submit")
        
        if submitted:
            if None in [q1, q2, q3, q4, q5]:
                st.error("Answer all questions!")
            else:
                score = 0
                if q1 == "True": score += 20
                if q2 == "Patient first": score += 20
                if q3 == "Patient privacy": score += 20
                if q4 == "Follow protocol": score += 20
                if q5 == "Essential": score += 20
                
                # Update user
                data = load_data()
                for u in data:
                    if u['email'] == user['email']:
                        u['attempts'] = u.get('attempts', 0) + 1
                        u['assessment_score'] = score
                        if score >= 80:
                            u['assessment_passed'] = True
                        st.session_state.user = u
                        break
                save_data(data)
                
                if score >= 80:
                    st.balloons()
                    st.success(f"🎉 Passed! Score: {score}%")
                else:
                    st.error(f"❌ Failed. Score: {score}%. Need 80%. Try again!")
                
                if st.button("Back to Dashboard"):
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
        st.markdown(f"""
        <div style="background:white; padding:20px; border-radius:15px; margin:10px 0; 
                    border-left:5px solid {color}; box-shadow:0 2px 10px rgba(0,0,0,0.1);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span>{icon} <b>{title}</b></span>
                <span style="color:{color}; font-weight:bold;">{status}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("← Back"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# REPORT CARD
elif st.session_state.page == 'report_card':
    st.subheader("📊 Report Card")
    
    user = st.session_state.user
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Score", f"{user.get('assessment_score', 0)}%")
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
Score: {user['assessment_score']}%
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
    st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 2.5em;">Admin Portal</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
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
    
    st.markdown('</div>', unsafe_allow_html=True)

# ADMIN DASHBOARD
elif st.session_state.page == 'admin_dashboard':
    st.subheader(f"🔐 Admin Dashboard - {st.session_state.admin}")
    
    data = load_data()
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", len(data))
    col2.metric("Passed", len([e for e in data if e.get('assessment_passed')]))
    col3.metric("Pending", len([e for e in data if not e.get('assessment_passed')]))
    avg = sum(e.get('assessment_score', 0) for e in data) / len(data) if data else 0
    col4.metric("Avg Score", f"{avg:.1f}%")
    
    # Table
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
