import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(page_title="Medanta Induction Portal", layout="wide", initial_sidebar_state="collapsed")

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
    
    .logo-container {
        background: white;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        margin: 0 auto 20px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .portal-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 10px 0;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .portal-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .contact-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 4px solid #e53e3e;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
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
    
    .form-box {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stat-number {
        font-size: 2.5em;
        font-weight: bold;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

DATA_FILE = "induction_data.json"

# Header
st.markdown("""
<div class="header-box">
    <div class="logo-container">
        <img src="https://www.medanta.org/images/medanta-logo.png" width="80" height="80" 
             onerror="this.style.display='none'; this.parentElement.innerHTML='<span style=font-size:40px;>🏥</span>';" 
             style="border-radius:50%;">
    </div>
    <h1>Namaste! 🙏</h1>
    <h3>Welcome to Medanta Induction Portal</h3>
</div>
""", unsafe_allow_html=True)

# HOME PAGE
if st.session_state.page == 'home':
    # Portal Selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✨ New Joinee", use_container_width=True):
            st.session_state.page = 'register'
            st.rerun()
        st.markdown("""
        <div class="portal-card">
            <h4>Participant Portal</h4>
            <p style="color:#666;">For new employees</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("📚 Handbook", use_container_width=True):
            st.session_state.page = 'handbook'
            st.rerun()
        st.markdown("""
        <div class="portal-card">
            <h4>Employee Handbook</h4>
            <p style="color:#666;">Digital handbook & resources</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🔐 Admin", use_container_width=True):
            st.session_state.page = 'admin'
            st.rerun()
        st.markdown("""
        <div class="portal-card">
            <h4>Administrator Portal</h4>
            <p style="color:#666;">For HR & Management</p>
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

# REGISTRATION PAGE
elif st.session_state.page == 'register':
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.subheader("📝 New Joinee Registration")
    
    with st.form("reg_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *")
            emp_id = st.text_input("Employee ID (if assigned)")
            department = st.text_input("Department *", placeholder="e.g., Nursing, HR, Finance")
        
        with col2:
            email = st.text_input("Email *")
            phone = st.text_input("Phone *")
            designation = st.text_input("Designation *", placeholder="e.g., Consultant, Nurse")
        
        col_back, col_submit = st.columns([1, 2])
        
        with col_back:
            if st.form_submit_button("← Back"):
                st.session_state.page = 'home'
                st.rerun()
        
        with col_submit:
            submitted = st.form_submit_button("Register & Continue", type="primary")
        
        if submitted:
            if not all([name, department, email, phone, designation]):
                st.error("Please fill all required fields!")
            else:
                # Save to session and go to assessment
                st.session_state.reg_data = {
                    "name": name,
                    "employee_id": emp_id if emp_id else "PENDING",
                    "department": department,
                    "email": email,
                    "phone": phone,
                    "designation": designation,
                    "timestamp": datetime.now().isoformat()
                }
                st.session_state.page = 'assessment'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ASSESSMENT PAGE (Separate from registration)
elif st.session_state.page == 'assessment':
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.subheader("🎯 Induction Assessment")
    st.info(f"Welcome {st.session_state.reg_data['name']}! Complete this assessment to finish your registration.")
    
    with st.form("assessment_form"):
        q1 = st.radio("Q1. What is the primary mission of Medanta?", 
            ["To provide affordable healthcare", 
             "To deliver world-class healthcare with patient-first approach",
             "To maximize profits", "Research only"], index=None)
        
        q2 = st.radio("Q2. Which is a core value at Medanta?",
            ["Profit first", "Patient centricity",
             "Cost cutting", "Rapid expansion"], index=None)
        
        q3 = st.radio("Q3. What does 'Samvaad' represent?",
            ["Medical procedure", "Open communication",
             "Billing system", "Discharge process"], index=None)
        
        col_back, col_submit = st.columns([1, 2])
        
        with col_back:
            if st.form_submit_button("← Back"):
                st.session_state.page = 'register'
                st.rerun()
        
        with col_submit:
            submitted = st.form_submit_button("Submit Assessment", type="primary")
        
        if submitted:
            if None in [q1, q2, q3]:
                st.error("Please answer all questions!")
            else:
                # Calculate score
                score = 0
                if "world-class" in q1: score += 1
                if "centricity" in q2: score += 1
                if "communication" in q3: score += 1
                
                # Save complete data
                final_data = st.session_state.reg_data
                final_data['score'] = score
                final_data['answers'] = {'q1': q1, 'q2': q2, 'q3': q3}
                
                all_data = []
                if os.path.exists(DATA_FILE):
                    with open(DATA_FILE, 'r') as f:
                        all_data = json.load(f)
                all_data.append(final_data)
                with open(DATA_FILE, 'w') as f:
                    json.dump(all_data, f)
                
                st.session_state.user_score = score
                st.session_state.page = 'success'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# SUCCESS PAGE
elif st.session_state.page == 'success':
    st.markdown('<div class="form-box" style="text-align:center;">', unsafe_allow_html=True)
    st.balloons()
    st.success("🎉 Registration Complete!")
    st.write(f"### Welcome to Medanta!")
    st.write(f"**Your Score:** {st.session_state.user_score}/3")
    st.info("You can now access the Employee Handbook from the home page.")
    
    if st.button("Go to Home", type="primary"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# HANDBOOK PAGE (FlippingBook)
elif st.session_state.page == 'handbook':
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.subheader("📚 Employee Handbook")
    st.info("Access the digital employee handbook below.")
    
    # Embed FlippingBook
    st.components.v1.iframe(
        src="https://online.flippingbook.com/view/652486186/",
        height=600,
        scrolling=True
    )
    
    st.markdown("---")
    st.write("Or open in new tab:")
    st.link_button("Open Handbook", "https://online.flippingbook.com/view/652486186/")
    
    if st.button("← Back to Home"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ADMIN DASHBOARD
elif st.session_state.page == 'admin':
    st.markdown('<div class="form-box">', unsafe_allow_html=True)
    st.subheader("🔐 Administrator Dashboard")
    
    # Password protection
    pwd = st.text_input("Enter Admin Password", type="password")
    
    if pwd == "medanta2024":
        st.success("Access Granted!")
        
        # Load data
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            
            # Stats
            st.markdown("---")
            st.subheader("📊 Statistics")
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{len(data)}</div>
                    <div>Total Registrations</div>
                </div>
                """, unsafe_allow_html=True)
            
            with c2:
                avg_score = sum(d.get('score', 0) for d in data) / len(data) if data else 0
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{avg_score:.1f}</div>
                    <div>Average Score</div>
                </div>
                """, unsafe_allow_html=True)
            
            with c3:
                departments = len(set(d.get('department', '') for d in data))
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{departments}</div>
                    <div>Departments</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Data table
            st.markdown("---")
            st.subheader("📋 Recent Registrations")
            
            df = pd.DataFrame(data)
            if not df.empty:
                df_display = df[['name', 'employee_id', 'department', 'designation', 'score', 'timestamp']].tail(10)
                df_display.columns = ['Name', 'Employee ID', 'Department', 'Designation', 'Score', 'Date']
                st.dataframe(df_display, use_container_width=True)
                
                # Download button
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Full Report (CSV)",
                    data=csv,
                    file_name=f"medanta_induction_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No data available yet.")
    
    elif pwd:
        st.error("Invalid password!")
    
    if st.button("← Back to Home"):
        st.session_state.page = 'home'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
