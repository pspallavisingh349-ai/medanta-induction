import streamlit as st
import pandas as pd
import sqlite3
import json
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Medanta Induction Portal",
    page_icon="🏥",
    layout="wide"
)

# Database path
DB_PATH = "medanta.db"

def init_db():
    """Initialize database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        department TEXT NOT NULL,
        role TEXT NOT NULL,
        employee_id TEXT,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completion_percentage REAL DEFAULT 0
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        options TEXT NOT NULL,
        correct_answer INTEGER NOT NULL,
        category TEXT DEFAULT 'General',
        marks INTEGER DEFAULT 1
    )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        score INTEGER,
        total_questions INTEGER DEFAULT 0,
        correct_answers INTEGER DEFAULT 0,
        status TEXT DEFAULT 'pending',
        time_taken INTEGER DEFAULT 0,
        completed_at TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )""")
    
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize
init_db()

# Sidebar navigation
st.sidebar.image("frontend/Medanta Lucknow Logo.jpg", width=200)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "📊 Dashboard",
    "📁 Import Questions", 
    "👥 Participants",
    "📝 Assessment Results",
    "❓ View Questions"
])

# ==================== DASHBOARD ====================
if page == "📊 Dashboard":
    st.title("🏥 Medanta Induction Dashboard")
    
    conn = get_db()
    c = conn.cursor()
    
    # Stats
    c.execute("SELECT COUNT(*) FROM users")
    total_participants = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM assessments WHERE status = 'completed'")
    completed = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM questions")
    total_questions = c.fetchone()[0]
    
    c.execute("SELECT AVG(score) FROM assessments WHERE status = 'completed'")
    avg_score = c.fetchone()[0] or 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Participants", total_participants)
    col2.metric("Completed Assessments", completed)
    col3.metric("Total Questions", total_questions)
    col4.metric("Average Score", f"{avg_score:.1f}%")
    
    # Recent participants
    st.subheader("Recent Registrations")
    c.execute("SELECT * FROM users ORDER BY created_at DESC LIMIT 10")
    users = c.fetchall()
    
    if users:
        df = pd.DataFrame([dict(row) for row in users])
        st.dataframe(df[['id', 'name', 'email', 'department', 'status', 'created_at']])
    else:
        st.info("No participants yet")
    
    conn.close()

# ==================== IMPORT QUESTIONS ====================
elif page == "📁 Import Questions":
    st.title("📁 Import Questions from Excel/CSV")
    
    st.markdown("""
    ### Instructions:
    1. Export each sheet from Google Sheets as CSV or Excel
    2. Upload files here (one or multiple)
    3. The system will automatically detect columns
    
    **Required columns:** Question, Option A, Option B, Option C, Option D, Answer
    **Optional:** Topic/Category
    """)
    
    uploaded_files = st.file_uploader(
        "Upload CSV or Excel files", 
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        total_imported = 0
        
        for uploaded_file in uploaded_files:
            st.subheader(f"Processing: {uploaded_file.name}")
            
            try:
                # Read file
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.write(f"Found {len(df)} rows")
                st.write("Preview:", df.head())
                
                # Detect columns
                cols = df.columns.tolist()
                st.write("Columns detected:", cols)
                
                # Standardize column names
                col_mapping = {}
                for col in cols:
                    col_lower = col.lower().strip()
                    if 'question' in col_lower:
                        col_mapping['question'] = col
                    elif col in ['Option A', 'A', 'option_a', 'option a']:
                        col_mapping['opt_a'] = col
                    elif col in ['Option B', 'B', 'option_b', 'option b']:
                        col_mapping['opt_b'] = col
                    elif col in ['Option C', 'C', 'option_c', 'option c']:
                        col_mapping['opt_c'] = col
                    elif col in ['Option D', 'D', 'option_d', 'option d']:
                        col_mapping['opt_d'] = col
                    elif col in ['Answer', 'answer', 'Correct', 'correct']:
                        col_mapping['answer'] = col
                    elif col in ['Topic', 'topic', 'Category', 'category']:
                        col_mapping['topic'] = col
                
                # Get topic from filename if not in columns
                default_topic = uploaded_file.name.replace('.csv', '').replace('.xlsx', '')
                
                # Import to database
                conn = get_db()
                c = conn.cursor()
                
                imported = 0
                for _, row in df.iterrows():
                    try:
                        question = str(row[col_mapping.get('question', 'Question')]).strip()
                        if not question or question == 'nan':
                            continue
                        
                        opt_a = str(row.get(col_mapping.get('opt_a', 'Option A'), '')).strip()
                        opt_b = str(row.get(col_mapping.get('opt_b', 'Option B'), '')).strip()
                        opt_c = str(row.get(col_mapping.get('opt_c', 'Option C'), '')).strip()
                        opt_d = str(row.get(col_mapping.get('opt_d', 'Option D'), '')).strip()
                        answer = str(row.get(col_mapping.get('answer', 'Answer'), 'A')).strip().upper()
                        
                        topic = str(row.get(col_mapping.get('topic', ''), default_topic)).strip()
                        if not topic:
                            topic = default_topic
                        
                        # Convert answer
                        ans_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, '1': 0, '2': 1, '3': 2, '4': 3}
                        correct_idx = ans_map.get(answer, 0)
                        
                        options = [opt_a, opt_b, opt_c, opt_d]
                        
                        c.execute("""
                            INSERT INTO questions (question, options, correct_answer, category, marks)
                            VALUES (?, ?, ?, ?, ?)
                        """, (question, json.dumps(options), correct_idx, topic, 1))
                        
                        imported += 1
                    except Exception as e:
                        st.error(f"Error on row: {e}")
                        continue
                
                conn.commit()
                conn.close()
                
                total_imported += imported
                st.success(f"✅ Imported {imported} questions from {uploaded_file.name}")
                
            except Exception as e:
                st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
        
        st.balloons()
        st.success(f"🎉 TOTAL: {total_imported} questions imported!")

# ==================== PARTICIPANTS ====================
elif page == "👥 Participants":
    st.title("👥 Registered Participants")
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = c.fetchall()
    
    if users:
        df = pd.DataFrame([dict(row) for row in users])
        st.dataframe(df)
        
        # Export option
        csv = df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            csv,
            "participants.csv",
            "text/csv"
        )
    else:
        st.info("No participants registered yet")
    
    conn.close()

# ==================== ASSESSMENT RESULTS ====================
elif page == "📝 Assessment Results":
    st.title("📝 Assessment Results")
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute("""SELECT a.*, u.name, u.email, u.department 
                 FROM assessments a 
                 JOIN users u ON a.user_id = u.id 
                 WHERE a.status = 'completed'
                 ORDER BY a.completed_at DESC""")
    results = c.fetchall()
    
    if results:
        df = pd.DataFrame([dict(row) for row in results])
        st.dataframe(df)
        
        # Statistics
        st.subheader("Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Completed", len(df))
        col2.metric("Average Score", f"{df['score'].mean():.1f}%")
        col3.metric("Pass Rate", f"{(df['score'] >= 70).mean() * 100:.1f}%")
        
        # Export
        csv = df.to_csv(index=False)
        st.download_button("Download Results", csv, "assessment_results.csv", "text/csv")
    else:
        st.info("No completed assessments yet")
    
    conn.close()

# ==================== VIEW QUESTIONS ====================
elif page == "❓ View Questions":
    st.title("❓ All Questions")
    
    conn = get_db()
    c = conn.cursor()
    
    c.execute("SELECT * FROM questions ORDER BY category, id")
    questions = c.fetchall()
    
    if questions:
        # Filter by category
        categories = list(set([q['category'] for q in questions]))
        selected_cat = st.selectbox("Filter by Category", ["All"] + categories)
        
        for q in questions:
            if selected_cat != "All" and q['category'] != selected_cat:
                continue
            
            with st.expander(f"{q['category']}: {q['question'][:80]}..."):
                st.write(f"**Question:** {q['question']}")
                opts = json.loads(q['options'])
                for i, opt in enumerate(['A', 'B', 'C', 'D']):
                    if i == q['correct_answer']:
                        st.success(f"**{opt}. {opts[i]}** ✓ (Correct)")
                    else:
                        st.write(f"{opt}. {opts[i]}")
    else:
        st.info("No questions imported yet. Go to 'Import Questions' to add them.")
    
    conn.close()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Medanta Induction Portal v2.0")