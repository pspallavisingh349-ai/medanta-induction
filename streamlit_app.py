import streamlit as st
import pandas as pd
import sqlite3
import json
import time
import os
import base64
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO

# Page config
st.set_page_config(
    page_title="Medanta Induction",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS with animations restored
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
        -webkit-tap-highlight-color: transparent;
    }
    
    /* Remove default spacing */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
        max-width: 600px !important;
    }
    
    #MainMenu, footer, header, .stDeployButton {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #00695c 0%, #004d40 50%, #00352c 100%);
        margin-top: 0 !important;
        min-height: 100vh;
    }
    
    /* Floating particles background */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
    }
    
    .particle {
        position: absolute;
        width: 10px;
        height: 10px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        animation: float-particle 15s infinite;
    }
    
    @keyframes float-particle {
        0%, 100% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
    }
    
    /* Glass card */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 30px 20px;
        margin: 10px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    /* Animated Logo with pulse */
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
        position: relative;
    }
    
    .logo-ring {
        width: 120px;
        height: 120px;
        margin: 0 auto;
        background: linear-gradient(135deg, #00897b 0%, #00695c 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        box-shadow: 0 20px 40px rgba(0,137,123,0.4);
        animation: pulse-ring 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
    }
    
    @keyframes pulse-ring {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0,137,123,0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 20px rgba(0,137,123,0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0,137,123,0); }
    }
    
    .logo-icon {
        font-size: 60px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
        animation: heartbeat 1.5s ease-in-out infinite;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        14% { transform: scale(1.1); }
        28% { transform: scale(1); }
        42% { transform: scale(1.1); }
        70% { transform: scale(1); }
    }
    
    /* ANIMATED TEXT - Gradient flowing */
    .animated-title {
        text-align: center;
        margin-bottom: 10px;
    }
    
    .namaste-text {
        font-size: 3em;
        font-weight: 700;
        background: linear-gradient(90deg, #ffffff, #80cbc4, #ffffff, #80cbc4);
        background-size: 300% 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-flow 3s ease infinite;
        display: inline-block;
        text-shadow: 0 0 30px rgba(255,255,255,0.3);
    }
    
    @keyframes gradient-flow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .welcome-text {
        font-size: 1.8em;
        font-weight: 300;
        color: #ffffff;
        text-align: center;
        margin-bottom: 10px;
        animation: slide-up 1s ease-out;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    @keyframes slide-up {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .tagline {
        text-align: center;
        color: rgba(255,255,255,0.8);
        font-size: 1em;
        margin-bottom: 30px;
        line-height: 1.6;
        animation: fade-in 1.5s ease-out;
    }
    
    @keyframes fade-in {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Shimmer effect on card */
    .glass-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
        pointer-events: none;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* Form labels */
    .form-label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 0.85em;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background: rgba(255,255,255,0.95) !important;
        border-radius: 12px !important;
        border: 2px solid transparent !important;
        padding: 14px !important;
        font-size: 16px !important;
        transition: all 0.3s !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #00897b !important;
        box-shadow: 0 0 0 4px rgba(0,137,123,0.2) !important;
    }
    
    /* Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #00897b 0%, #00695c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 16px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        box-shadow: 0 10px 30px rgba(0,137,123,0.3) !important;
        transition: all 0.3s !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 40px rgba(0,137,123,0.4) !important;
    }
    
    .stButton > button[kind="secondary"] {
        background: rgba(255,255,255,0.15) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.4) !important;
        border-radius: 25px !important;
        padding: 14px 24px !important;
        font-weight: 600 !important;
    }
    
    /* Floating shapes */
    .shape {
        position: absolute;
        opacity: 0.1;
        animation: float-shape 20s infinite;
    }
    
    @keyframes float-shape {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(30px, -30px) rotate(120deg); }
        66% { transform: translate(-20px, 20px) rotate(240deg); }
    }
</style>

<!-- Floating particles -->
<div class="particles">
    <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
    <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
    <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
    <div class="particle" style="left: 40%; animation-delay: 6s;"></div>
    <div class="particle" style="left: 50%; animation-delay: 8s;"></div>
    <div class="particle" style="left: 60%; animation-delay: 10s;"></div>
    <div class="particle" style="left: 70%; animation-delay: 12s;"></div>
    <div class="particle" style="left: 80%; animation-delay: 14s;"></div>
    <div class="particle" style="left: 90%; animation-delay: 16s;"></div>
</div>
""", unsafe_allow_html=True)

# Database setup
DB_PATH = "medanta.db"

def init_db():
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
        answers TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )""")
    
    conn.commit()
    conn.close()

def import_questions_from_csv():
    csv_path = "questions.csv"
    if not os.path.exists(csv_path):
        return False
    
    try:
        df = pd.read_csv(csv_path)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM questions")
        
        for _, row in df.iterrows():
            question = str(row.get('Question', '')).strip()
            if not question or pd.isna(question):
                continue
            
            opt_a = str(row.get('Option A', '')).strip()
            opt_b = str(row.get('Option B', '')).strip()
            opt_c = str(row.get('Option C', '')).strip()
            opt_d = str(row.get('Option D', '')).strip()
            answer = str(row.get('Answer', 'A')).strip().upper()
            
            ans_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            correct_idx = ans_map.get(answer, 0)
            
            options = json.dumps([opt_a, opt_b, opt_c, opt_d])
            topic = str(row.get('Topic', row.get('Category', 'General'))).strip()
            if not topic or topic == 'nan':
                topic = 'General'
            
            c.execute("""
                INSERT INTO questions (question, options, correct_answer, category, marks)
                VALUES (?, ?, ?, ?, ?)
            """, (question, options, correct_idx, topic, 1))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        st.error(f"Import error: {e}")
        return False

def add_sample_questions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM questions")
    count = c.fetchone()[0]
    
    if count == 0:
        sample_questions = [
            ("What is Medanta's core value regarding patient care?", 
             json.dumps(["Profit first", "Patient first", "
