import csv
import json
import sqlite3

def import_questions_from_csv(csv_file):
    conn = sqlite3.connect("medanta.db")
    c = conn.cursor()
    
    # Clear existing questions
    c.execute("DELETE FROM questions")
    print("Cleared existing questions")
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            # Skip empty rows
            if not row.get('Question', '').strip():
                continue
            
            # Get data from columns
            question = row['Question'].strip()
            opt_a = row.get('Option A', '').strip()
            opt_b = row.get('Option B', '').strip()
            opt_c = row.get('Option C', '').strip()
            opt_d = row.get('Option D', '').strip()
            answer_letter = row.get('Answer', 'A').strip().upper()
            
            # Convert letter to index (A=0, B=1, C=2, D=3)
            answer_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            correct_idx = answer_map.get(answer_letter, 0)
            
            # Create options array
            options = [opt_a, opt_b, opt_c, opt_d]
            
            # Default topic since you don't have one
            topic = "HR & Compliance"
            
            # Insert into database
            c.execute("""
                INSERT INTO questions (question, options, correct_answer, category, marks)
                VALUES (?, ?, ?, ?, ?)
            """, (question, json.dumps(options), correct_idx, topic, 1))
            
            count += 1
            print(f"Imported {count}: {question[:50]}...")
    
    conn.commit()
    conn.close()
    print(f"\n✅ SUCCESS! Imported {count} questions total!")

if __name__ == "__main__":
    import_questions_from_csv("questions.csv")