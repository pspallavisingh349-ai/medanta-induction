from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import json
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import uvicorn

app = FastAPI(title="Medanta Induction API")

# CORS Middleware - CRITICAL for HTML frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path
DB_PATH = "medanta.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Users table - Enhanced
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
    
    # Assessments table - Enhanced
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
    
    # Questions table - Enhanced with category
    c.execute("""CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        options TEXT NOT NULL,
        correct_answer INTEGER NOT NULL,
        category TEXT DEFAULT 'General',
        marks INTEGER DEFAULT 1
    )""")
    
    # Answers table - Track individual answers
    c.execute("""CREATE TABLE IF NOT EXISTS answers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assessment_id INTEGER,
        question_id INTEGER,
        selected_answer INTEGER,
        is_correct BOOLEAN,
        FOREIGN KEY (assessment_id) REFERENCES assessments (id),
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )""")
    
    conn.commit()
    conn.close()
    
    # Add sample questions if none exist
    add_sample_questions()

def add_sample_questions():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM questions")
    if c.fetchone()[0] == 0:
        sample_questions = [
            ("What is Medanta's core value regarding patient care?", 
             json.dumps(["Profit first", "Patient first", "Technology first", "Speed first"]), 
             1, "HR", 1),
            ("What should you do in case of a fire emergency?", 
             json.dumps(["Use elevator", "Run immediately", "Follow evacuation protocol", "Call security only"]), 
             2, "Safety", 1),
            ("Which document is mandatory for all new employees?", 
             json.dumps(["PAN Card", "Aadhar Card", "Both", "None"]), 
             2, "Compliance", 1),
            ("What is the standard hand hygiene protocol?", 
             json.dumps(["Water only", "Soap and water", "Sanitizer only", "Soap and water or sanitizer"]), 
             3, "Clinical", 1),
            ("Who is the founder of Medanta?", 
             json.dumps(["Dr. Naresh Trehan", "Dr. Devi Shetty", "Dr. Prathap Reddy", "Dr. Ashok Seth"]), 
             0, "HR", 1),
        ]
        c.executemany("""INSERT INTO questions (question, options, correct_answer, category, marks) 
                        VALUES (?, ?, ?, ?, ?)""", sample_questions)
        conn.commit()
    conn.close()

@app.on_event("startup")
async def startup():
    init_db()

# ==================== PYDANTIC MODELS ====================

class UserCreate(BaseModel):
    name: str
    email: str
    department: str
    role: str
    employee_id: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str
    role: str
    employee_id: Optional[str]
    status: str
    completion_percentage: float

class AssessmentCreate(BaseModel):
    user_id: int
    title: str = "Induction Assessment"

class AssessmentSubmit(BaseModel):
    user_id: int
    answers: List[int]  # List of selected option indices
    time_taken: int  # in seconds

class QuestionCreate(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    category: str = "General"
    marks: int = 1

class DashboardStats(BaseModel):
    total_participants: int
    completed_assessments: int
    pass_count: int
    fail_count: int
    average_score: float
    department_wise: dict

# ==================== USER APIs ====================

@app.post("/api/register", response_model=dict)
async def register_user(user: UserCreate):
    """Register a new participant"""
    conn = get_db()
    c = conn.cursor()
    
    # Check if email exists
    c.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if c.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    c.execute("""INSERT INTO users (name, email, department, role, employee_id) 
                 VALUES (?, ?, ?, ?, ?)""",
        (user.name, user.email, user.department, user.role, user.employee_id))
    user_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "data": {"id": user_id, "name": user.name, "email": user.email},
        "message": "Registration successful"
    }

@app.get("/api/participants", response_model=dict)
async def get_participants():
    """Get all participants"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY created_at DESC")
    users = []
    for row in c.fetchall():
        users.append({
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "department": row["department"],
            "role": row["role"],
            "employee_id": row["employee_id"],
            "status": row["status"],
            "completion_percentage": row["completion_percentage"],
            "created_at": row["created_at"]
        })
    conn.close()
    return {"success": True, "data": users}

@app.get("/api/participant/{user_id}", response_model=dict)
async def get_participant(user_id: int):
    """Get participant by ID"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    return {
        "success": True,
        "data": {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "department": row["department"],
            "role": row["role"],
            "employee_id": row["employee_id"],
            "status": row["status"],
            "completion_percentage": row["completion_percentage"]
        }
    }

@app.get("/api/participant/email/{email}", response_model=dict)
async def get_participant_by_email(email: str):
    """Get participant by email"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Participant not found")
    
    return {
        "success": True,
        "data": {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "department": row["department"],
            "role": row["role"],
            "status": row["status"],
            "completion_percentage": row["completion_percentage"]
        }
    }

# ==================== ASSESSMENT APIs ====================

@app.get("/api/questions", response_model=dict)
async def get_questions():
    """Get all questions for assessment (without correct answers)"""
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, question, options, category, marks FROM questions")
    questions = []
    for row in c.fetchall():
        questions.append({
            "id": row["id"],
            "question": row["question"],
            "options": json.loads(row["options"]),
            "category": row["category"],
            "marks": row["marks"]
        })
    conn.close()
    return {"success": True, "data": questions}

@app.post("/api/assessments/start", response_model=dict)
async def start_assessment(assessment: AssessmentCreate):
    """Start a new assessment"""
    conn = get_db()
    c = conn.cursor()
    
    # Check if user already has a completed assessment
    c.execute("""SELECT id FROM assessments 
                 WHERE user_id = ? AND status = 'completed'""", (assessment.user_id,))
    if c.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Assessment already completed")
    
    c.execute("""INSERT INTO assessments (user_id, title, status) 
                 VALUES (?, ?, 'in_progress')""",
        (assessment.user_id, assessment.title))
    assessment_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "data": {"id": assessment_id, "status": "in_progress"},
        "message": "Assessment started"
    }

@app.post("/api/assessments/submit", response_model=dict)
async def submit_assessment(submission: AssessmentSubmit):
    """Submit assessment and calculate score"""
    conn = get_db()
    c = conn.cursor()
    
    # Get all questions
    c.execute("SELECT id, correct_answer FROM questions")
    questions = {row["id"]: row["correct_answer"] for row in c.fetchall()}
    
    total_questions = len(questions)
    correct_count = 0
    
    # Check if assessment exists and is in progress
    c.execute("""SELECT id FROM assessments 
                 WHERE user_id = ? AND status = 'in_progress'""", (submission.user_id,))
    assessment_row = c.fetchone()
    
    if assessment_row:
        assessment_id = assessment_row["id"]
    else:
        # Create new assessment record
        c.execute("""INSERT INTO assessments (user_id, title, status) 
                     VALUES (?, ?, 'completed')""",
            (submission.user_id, "Induction Assessment"))
        assessment_id = c.lastrowid
    
    # Calculate score
    question_ids = list(questions.keys())
    for i, answer in enumerate(submission.answers):
        if i < len(question_ids):
            q_id = question_ids[i]
            is_correct = (answer == questions[q_id])
            if is_correct:
                correct_count += 1
            
            # Store answer
            c.execute("""INSERT INTO answers (assessment_id, question_id, selected_answer, is_correct)
                         VALUES (?, ?, ?, ?)""",
                (assessment_id, q_id, answer, is_correct))
    
    score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    
    # Update assessment
    c.execute("""UPDATE assessments 
                 SET score = ?, total_questions = ?, correct_answers = ?, 
                     status = 'completed', time_taken = ?, completed_at = datetime('now')
                 WHERE id = ?""",
        (score_percentage, total_questions, correct_count, submission.time_taken, assessment_id))
    
    # Update user completion percentage
    c.execute("""SELECT AVG(score) FROM assessments 
                 WHERE user_id = ? AND status = 'completed'""", (submission.user_id,))
    avg_score = c.fetchone()[0] or score_percentage
    c.execute("""UPDATE users SET completion_percentage = ?, status = 'completed' 
                 WHERE id = ?""", (avg_score, submission.user_id))
    
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "data": {
            "assessment_id": assessment_id,
            "total_questions": total_questions,
            "correct_answers": correct_count,
            "score_percentage": round(score_percentage, 2),
            "status": "pass" if score_percentage >= 70 else "fail",
            "time_taken": submission.time_taken
        },
        "message": "Assessment submitted successfully"
    }

@app.get("/api/result/{user_id}", response_model=dict)
async def get_result(user_id: int):
    """Get assessment result for a user"""
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT * FROM assessments 
                 WHERE user_id = ? AND status = 'completed' 
                 ORDER BY completed_at DESC LIMIT 1""", (user_id,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="No completed assessment found")
    
    return {
        "success": True,
        "data": {
            "assessment_id": row["id"],
            "score": row["score"],
            "total_questions": row["total_questions"],
            "correct_answers": row["correct_answers"],
            "status": "pass" if row["score"] >= 70 else "fail",
            "time_taken": row["time_taken"],
            "completed_at": row["completed_at"]
        }
    }

# ==================== ADMIN APIs ====================

@app.get("/api/admin/stats", response_model=dict)
async def get_dashboard_stats():
    """Get dashboard statistics"""
    conn = get_db()
    c = conn.cursor()
    
    # Total participants
    c.execute("SELECT COUNT(*) FROM users")
    total_participants = c.fetchone()[0]
    
    # Completed assessments
    c.execute("SELECT COUNT(*) FROM assessments WHERE status = 'completed'")
    completed_assessments = c.fetchone()[0]
    
    # Pass count (score >= 70)
    c.execute("SELECT COUNT(*) FROM assessments WHERE status = 'completed' AND score >= 70")
    pass_count = c.fetchone()[0]
    
    # Fail count
    fail_count = completed_assessments - pass_count
    
    # Average score
    c.execute("SELECT AVG(score) FROM assessments WHERE status = 'completed'")
    avg_score = c.fetchone()[0] or 0
    
    # Department wise stats
    c.execute("""SELECT department, COUNT(*) as count FROM users GROUP BY department""")
    dept_stats = {row["department"]: {"total": row["count"], "completed": 0} for row in c.fetchall()}
    
    c.execute("""SELECT u.department, COUNT(*) as count 
                 FROM assessments a JOIN users u ON a.user_id = u.id 
                 WHERE a.status = 'completed' GROUP BY u.department""")
    for row in c.fetchall():
        if row["department"] in dept_stats:
            dept_stats[row["department"]]["completed"] = row["count"]
    
    conn.close()
    
    return {
        "success": True,
        "data": {
            "total_participants": total_participants,
            "completed_assessments": completed_assessments,
            "pass_count": pass_count,
            "fail_count": fail_count,
            "average_score": round(avg_score, 2),
            "department_wise": dept_stats
        }
    }

@app.get("/api/admin/assessments", response_model=dict)
async def get_all_assessments():
    """Get all assessments with user details"""
    conn = get_db()
    c = conn.cursor()
    c.execute("""SELECT a.*, u.name, u.email, u.department, u.role 
                 FROM assessments a 
                 JOIN users u ON a.user_id = u.id 
                 ORDER BY a.completed_at DESC""")
    assessments = []
    for row in c.fetchall():
        assessments.append({
            "id": row["id"],
            "user_id": row["user_id"],
            "participant_name": row["name"],
            "email": row["email"],
            "department": row["department"],
            "role": row["role"],
            "title": row["title"],
            "score": row["score"],
            "total_questions": row["total_questions"],
            "correct_answers": row["correct_answers"],
            "status": row["status"],
            "time_taken": row["time_taken"],
            "completed_at": row["completed_at"]
        })
    conn.close()
    return {"success": True, "data": assessments}

@app.post("/api/admin/questions", response_model=dict)
async def add_question(question: QuestionCreate):
    """Add new question (Admin only)"""
    conn = get_db()
    c = conn.cursor()
    c.execute("""INSERT INTO questions (question, options, correct_answer, category, marks)
                 VALUES (?, ?, ?, ?, ?)""",
        (question.question, json.dumps(question.options), question.correct_answer, 
         question.category, question.marks))
    question_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "data": {"id": question_id},
        "message": "Question added successfully"
    }

# ==================== HEALTH CHECK ====================

@app.get("/")
async def root():
    return {
        "message": "Medanta Induction API is running",
        "version": "2.0",
        "endpoints": {
            "participant": "/api/register, /api/participants, /api/participant/{id}",
            "assessment": "/api/questions, /api/assessments/start, /api/assessments/submit",
            "admin": "/api/admin/stats, /api/admin/assessments, /api/admin/questions"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)