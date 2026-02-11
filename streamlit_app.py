import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Medanta Induction Portal", layout="centered")

# CSS
st.markdown("""
<style>
    .stApp {background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);}
    #MainMenu, footer, header {visibility: hidden;}
    
    .header-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    
    .step-box {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    .contact-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 4px solid #e53e3e;
    }
    
    .contact-box.it {border-left-color: #3182ce;}
    .contact-box.salary {border-left-color: #d69e2e;}
    .contact-box.onboard {border-left-color: #38a169;}
    .contact-box.training {
        border-left-color: #805ad5;
        background: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%);
    }
    
    .number {color: #e53e3e; font-weight: bold; font-size: 1.2em;}
    .number.green {color: #38a169;}
    .number.blue {color: #3182ce;}
</style>
""", unsafe_allow_html=True)

# Session state
if 'step' not in st.session_state:
    st.session_state.step = 'home'  # home, check_id, register, success
if 'existing_user' not in st.session_state:
    st.session_state.existing_user = None

DATA_FILE = "induction_data.json"

# Header
st.markdown("""
<div class="header-box">
    <h1>🏥 Namaste! 🙏</h1>
    <h3>Welcome to Medanta Induction Portal</h3>
</div>
""", unsafe_allow_html=True)

# HOME PAGE - Choose portal
if st.session_state.step == 'home':
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✨ New Joinee", use_container_width=True):
            st.session_state.step = 'check_id'
            st.rerun()
        st.markdown("""
        <div style="background:white; padding:20px; border-radius:15px; text-align:center; margin-top:10px;">
            <h4>Participant Portal</h4>
            <p style="color:#666;">For new employees joining Medanta</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🔐 Returning User", use_container_width=True):
            st.session_state.step = 'returning'
            st.rerun()
        st.markdown("""
        <div style="background:white; padding:20px; border-radius:15px; text-align:center; margin-top:10px;">
            <h4>Administrator Portal</h4>
            <p style="color:#666;">For HR, Trainers & Management</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Contacts
    st.markdown("---")
    st.subheader("📞 Key Contacts")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="contact-box">
            <b>EMR/HIS Query</b><br>Mr. Surjendra<br>
            <span class="number">📱 9883111600</span>
        </div>
        <div class="contact-box salary">
            <b>Salary Related</b><br>HR Department<br>
            <span class="number">📱 9560719167</span>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown("""
        <div class="contact-box it">
            <b>IT Helpdesk</b><br>Internal Extension<br>
            <span class="number blue">☎️ 1010</span>
        </div>
        <div class="contact-box onboard">
            <b>Onboarding Query</b><br>HR Business Partner<br>
            <span style="color:#38a169;font-weight:600;">Contact your HRBP</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="contact-box training">
        <b>Training Related</b> - Dr. Pallavi & Mr. Rohit<br>
        <span class="number green">📞 7860955988</span> &nbsp;&nbsp;
        <span class="number green">📞 7275181822</span>
    </div>
    """, unsafe_allow_html=True)

# STEP 1: CHECK EMPLOYEE ID FIRST
elif st.session_state.step == 'check_id':
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.subheader("📝 Step 1: Verify Employee ID")
    st.info("Please enter your Employee ID to check if you're already registered.")
    
    emp_id = st.text_input("Employee ID *", placeholder="e.g., MED12345")
    
    col_back, col_check = st.columns([1, 2])
    
    with col_back:
        if st.button("← Back to Home"):
            st.session_state.step = 'home'
            st.rerun()
    
    with col_check:
        if st.button("Check ID", type="primary"):
            if not emp_id:
                st.error("Please enter Employee ID!")
            else:
                # Check if already exists
                if os.path.exists(DATA_FILE):
                    with open(DATA_FILE, 'r') as f:
                        data = json.load(f)
                    existing = [u for u in data if u.get('employee_id') == emp_id]
                    
                    if existing:
                        st.session_state.existing_user = existing[-1]
                        st.session_state.step = 'already_registered'
                        st.rerun()
                    else:
                        # New user - save ID and go to registration
                        st.session_state.temp_emp_id = emp_id
                        st.session_state.step = 'register'
                        st.rerun()
                else:
                    # No data file yet - new user
                    st.session_state.temp_emp_id = emp_id
                    st.session_state.step = 'register'
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# STEP 2: REGISTRATION FORM + ASSESSMENT
elif st.session_state.step == 'register':
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.subheader("📝 Step 2: Complete Registration")
    st.info(f"Employee ID: **{st.session_state.temp_emp_id}**")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *")
            dept = st.selectbox("Department *", 
                ["Select", "Nursing", "Medical Services", "Administration", 
                 "HR", "Finance", "Operations", "IT", "Others"])
        
        with col2:
            email = st.text_input("Email *")
            desig = st.selectbox("Designation *",
                ["Select", "Consultant", "Nurse", "Resident", "Intern",
                 "Manager", "Executive", "Technician", "Others"])
        
        phone = st.text_input("Phone Number *", placeholder="+91 XXXXX XXXXX")
        
        st.markdown("---")
        st.subheader("🎯 Assessment")
        st.write("Please answer all questions to complete your registration.")
        
        # Questions
        q1 = st.radio("Q1. What is the primary mission of Medanta?", 
            ["Select an answer", "To provide affordable healthcare", 
             "To deliver world-class healthcare with patient-first approach",
             "To maximize profits", "Research only"], index=0)
        
        q2 = st.radio("Q2. Which is a core value at Medanta?",
            ["Select an answer", "Profit first", "Patient centricity",
             "Cost cutting", "Rapid expansion"], index=0)
        
        q3 = st.radio("Q3. What does 'Samvaad' represent?",
            ["Select an answer", "Medical procedure", "Open communication",
             "Billing system", "Discharge process"], index=0)
        
        col_back, col_submit = st.columns([1, 2])
        
        with col_back:
            if st.form_submit_button("← Back"):
                st.session_state.step = 'check_id'
                st.rerun()
        
        with col_submit:
            submitted = st.form_submit_button("Complete Registration", type="primary")
        
        if submitted:
            # Validation
            errors = []
            if not name: errors.append("Full Name")
            if dept == "Select": errors.append("Department")
            if not email: errors.append("Email")
            if desig == "Select": errors.append("Designation")
            if not phone: errors.append("Phone")
            if q1 == "Select an answer": errors.append("Q1")
            if q2 == "Select an answer": errors.append("Q2")
            if q3 == "Select an answer": errors.append("Q3")
            
            if errors:
                st.error(f"Please complete: {', '.join(errors)}")
            else:
                # Calculate score
                score = 0
                if "world-class" in q1: score += 1
                if "centricity" in q2: score += 1
                if "communication" in q3: score += 1
                
                # Save data
                user_data = {
                    "name": name,
                    "employee_id": st.session_state.temp_emp_id,
                    "department": dept,
                    "email": email,
                    "phone": phone,
                    "designation": desig,
                    "score": score,
                    "timestamp": datetime.now().isoformat()
                }
                
                all_data = []
                if os.path.exists(DATA_FILE):
                    with open(DATA_FILE, 'r') as f:
                        all_data = json.load(f)
                all_data.append(user_data)
                with open(DATA_FILE, 'w') as f:
                    json.dump(all_data, f)
                
                st.session_state.user_name = name
                st.session_state.user_score = score
                st.session_state.step = 'success'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# SUCCESS PAGE
elif st.session_state.step == 'success':
    st.markdown('<div class="step-box" style="text-align:center;">', unsafe_allow_html=True)
    st.balloons()
    st.success("🎉 Registration Successful!")
    st.write(f"### Welcome to Medanta, {st.session_state.user_name}!")
    st.write(f"**Your Score:** {st.session_state.user_score}/3")
    st.info("We wish you a wonderful journey ahead! 🚀")
    
    if st.button("Go to Home", type="primary"):
        st.session_state.step = 'home'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ALREADY REGISTERED PAGE
elif st.session_state.step == 'already_registered':
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.warning("⚠️ Already Registered")
    
    user = st.session_state.existing_user
    st.write(f"**Name:** {user['name']}")
    st.write(f"**Employee ID:** {user['employee_id']}")
    st.write(f"**Department:** {user['department']}")
    st.write(f"**Score:** {user.get('score', 'N/A')}/3")
    st.write(f"**Registered on:** {user['timestamp'][:10]}")
    
    if st.button("Go to Home"):
        st.session_state.step = 'home'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# RETURNING USER (ADMIN)
elif st.session_state.step == 'returning':
    st.markdown('<div class="step-box">', unsafe_allow_html=True)
    st.subheader("🔍 Check Status")
    
    emp_id = st.text_input("Enter Employee ID")
    
    col_back, col_search = st.columns([1, 2])
    
    with col_back:
        if st.button("← Back"):
            st.session_state.step = 'home'
            st.rerun()
    
    with col_search:
        if st.button("Search"):
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                records = [u for u in data if u.get('employee_id') == emp_id]
                
                if records:
                    r = records[-1]
                    st.success(f"Found: {r['name']}")
                    st.write(f"Department: {r['department']}")
                    st.write(f"Score: {r.get('score', 'N/A')}/3")
                else:
                    st.error("Not found.")
            else:
                st.error("No data available.")
    
    st.markdown('</div>', unsafe_allow_html=True)
