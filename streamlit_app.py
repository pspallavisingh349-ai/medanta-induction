        st.session_state.user = None
        st.session_state.page = 'landing'
        st.rerun()

# HANDBOOK
elif st.session_state.page == 'handbook':
    st.markdown('<h2 style="margin-bottom: 20px; color: #800020;">📚 Employee Handbook</h2>', unsafe_allow_html=True)
    st.components.v1.iframe("https://online.flippingbook.com/view/652486186/  ", height=700)
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# JCI HANDBOOK
elif st.session_state.page == 'jci_handbook':
    st.markdown('<h2 style="margin-bottom: 20px; color: #800020;">🏅 JCI Accreditation Standards</h2>', unsafe_allow_html=True)
    st.components.v1.iframe("https://online.flippingbook.com/view/389334287/  ", height=700)
    if st.button("← Back to Dashboard"):
        st.session_state.page = 'employee_dashboard'
        st.rerun()

# ASSESSMENT - With tabs for each topic
elif st.session_state.page == 'assessment':
    user = st.session_state.user
    
    if not questions_data:
        st.error("⚠️ Could not load questions. Please check Question_bank.xlsx file.")
        if st.button("← Back"):
            st.session_state.page = 'employee_dashboard'
            st.rerun()
        st.stop()
    
    module_ids = list(questions_data.keys())
    current_idx = st.session_state.current_module_idx
    
    if current_idx >= len(module_ids):
        st.balloons()
        st.success("🎉 Congratulations! You have completed all assessments!")
        
        data = load_data()
        for u in data:
            if u['email'] == user.get('email'):
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
    
    # Progress
    st.markdown(f"""
    <div style="margin-bottom: 30px;">
        <h2 style="color: #800020; margin-bottom: 10px;">{current_module['name']}</h2>
        <p style="color: #666666;">Module {current_idx + 1} of {len(module_ids)} • {len(questions)} Questions</p>
        <div class="progress-container" style="margin-top: 15px;">
            <div class="progress-bar" style="width: {(current_idx/len(module_ids))*100}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for each question
    tabs = st.tabs([f"Q{i+1}" for i in range(len(questions))])
    
    answers = {}
    
    for i, (tab, q) in enumerate(zip(tabs, questions)):
        with tab:
            st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
            st.markdown(f'<h3 style="color: #800020; margin-bottom: 20px;">{q["question"]}</h3>', unsafe_allow_html=True)
            
            answer = st.radio(
                "Select your answer:",
                q['options'],
                index=None,
                key=f"q_{current_idx}_{i}"
            )
            answers[i] = answer
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit button
    st.markdown("<hr style='border-color: #D4AF37; margin: 30px 0;'>", unsafe_allow_html=True)
    
    if st.button("Submit Module", type="primary", use_container_width=True):
        if None in answers.values():
            st.error("⚠️ Please answer all questions before submitting!")
            st.stop()
        
        correct_count = 0
        for i, q in enumerate(questions):
            if answers[i] == q['options'][q['correct']]:
                correct_count += 1
        
        percentage = (correct_count / len(questions)) * 100
        
        # Save result
        data = load_data()
        for u in data:
            if u['email'] == user.get('email'):
                u['attempts'] = u.get('attempts', 0) + 1
                if percentage >= 80:
                    u['current_module'] = current_idx + 1
                    if current_idx + 1 >= len(module_ids):
                        u['assessment_passed'] = True
                        u['assessment_score'] = percentage
                break
        save_data(data)
        
        # Show result
        if percentage >= 80:
            st.balloons()
            st.success(f"🎉 Congratulations! You passed with {percentage:.0f}%!")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➡️ Next Module"):
                    st.session_state.current_module_idx += 1
                    st.rerun()
            with col2:
                if st.button("← Back to Dashboard"):
                    st.session_state.page = 'employee_dashboard'
                    st.rerun()
        else:
            st.error(f"❌ You scored {percentage:.0f}%. You need 80% to pass.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Reattempt Module"):
                    st.rerun()
            with col2:
                if st.button("← Back to Dashboard"):
                    st.session_state.page = 'employee_dashboard'
                    st.rerun()

# REPORT CARD
elif st.session_state.page == 'report_card':
    user = st.session_state.user
    data = load_data()
    user_data = next((u for u in data if u['email'] == user.get('email')), None)
    
    st.markdown('<h2 style="margin-bottom: 20px; color: #800020;">📊 Assessment Report Card</h2>', unsafe_allow_html=True)
    
    if not user_data or not user_data.get('assessment_passed'):
        st.warning("⚠️ You haven't completed all assessments yet.")
        if st.button("← Back to Dashboard"):
            st.session_state.page = 'employee_dashboard'
            st.rerun()
    else:
        # Display certificate-style report
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f5f5f5 0%, #ffffff 100%); 
                    border: 3px solid #D4AF37; border-radius: 15px; padding: 40px; 
                    text-align: center; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="color: #800020; font-size: 2.5em; margin-bottom: 10px;">🏆 Certificate of Completion</h1>
            <p style="font-size: 1.2em; color: #666; margin: 20px 0;">This certifies that</p>
            <h2 style="color: #333; font-size: 2em; margin: 20px 0;">{user_data.get('name', 'Employee')}</h2>
            <p style="font-size: 1.2em; color: #666; margin: 20px 0;">has successfully completed all training modules</p>
            <div style="margin: 30px 0;">
                <span style="font-size: 3em; color: #D4AF37;">{'★' * 5}</span>
            </div>
            <p style="font-size: 1.1em; color: #800020; font-weight: bold;">
                Final Score: {user_data.get('assessment_score', 0):.0f}%
            </p>
            <p style="font-size: 0.9em; color: #999; margin-top: 30px;">
                Completed on: {datetime.now().strftime('%B %d, %Y')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Attempts", user_data.get('attempts', 0))
        with col2:
            st.metric("Modules Completed", f"{user_data.get('current_module', 0)}/{len(module_ids)}")
        with col3:
            st.metric("Status", "PASSED" if user_data.get('assessment_passed') else "IN PROGRESS")
        
        # Download certificate button (optional)
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🖨️ Print Certificate"):
                st.info("Use your browser's print function (Ctrl+P) to save as PDF")
        with col2:
            if st.button("← Back to Dashboard"):
                st.session_state.page = 'employee_dashboard'
                st.rerun()
