import requests
import csv
import io
import json
import sqlite3
import time

# Your Google Sheet ID
SHEET_ID = "1CUGrktlzvu_X1xHxzKRSEXmvonclfmR13puKKiGa82I"

def import_all_sheets():
    """Import all sheets from Google Sheets"""
    conn = sqlite3.connect("medanta.db")
    c = conn.cursor()
    
    # Clear existing questions
    c.execute("DELETE FROM questions")
    print("🗑️  Cleared existing questions")
    
    base_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    
    total_imported = 0
    successful_sheets = []
    
    # Try to read sheets 0-20 (covers your 17 topics plus buffer)
    for gid in range(20):
        url = f"{base_url}&gid={gid}"
        
        try:
            print(f"\n📄 Reading Sheet {gid}...")
            response = requests.get(url, timeout=15)
            
            # Check if valid CSV
            if response.status_code != 200:
                print(f"  ⚠️  Sheet not accessible (Status: {response.status_code})")
                continue
            
            content = response.content.decode('utf-8')
            
            # Skip if empty or very small
            if len(content) < 200:
                print(f"  ⚠️  Sheet empty")
                continue
            
            # Parse CSV
            csv_file = io.StringIO(content)
            reader = csv.DictReader(csv_file)
            
            # Get headers to detect format
            headers = reader.fieldnames
            print(f"  📋 Headers found: {headers}")
            
            sheet_count = 0
            topic_name = f"Topic {gid + 1}"  # Default topic name
            
            for row in reader:
                # Skip completely empty rows
                if not any(row.values()):
                    continue
                
                # Try to find question column (variations)
                question = None
                for key in ['Question', 'question', 'Questions', 'QUESTION', 'Que', 'Q']:
                    if key in row and row[key].strip():
                        question = row[key].strip()
                        break
                
                if not question:
                    continue
                
                # Try to find topic/category
                for key in ['Topic', 'topic', 'Category', 'category', 'Subject', 'Module', 'Sheet']:
                    if key in row and row[key].strip():
                        topic_name = row[key].strip()
                        break
                
                # Get options (handle various column names)
                opt_a = row.get('Option A', row.get('option_a', row.get('A', row.get('a', '')))).strip()
                opt_b = row.get('Option B', row.get('option_b', row.get('B', row.get('b', '')))).strip()
                opt_c = row.get('Option C', row.get('option_c', row.get('C', row.get('c', '')))).strip()
                opt_d = row.get('Option D', row.get('option_d', row.get('D', row.get('d', '')))).strip()
                
                # Get answer
                ans = row.get('Answer', row.get('answer', row.get('Correct', row.get('correct', 'A')))).strip().upper()
                
                # Convert to index
                ans_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3, '1': 0, '2': 1, '3': 2, '4': 3}
                correct_idx = ans_map.get(ans, 0)
                
                # Ensure we have 4 options
                options = [opt_a or "Option A", opt_b or "Option B", opt_c or "Option C", opt_d or "Option D"]
                
                # Insert into database
                c.execute("""
                    INSERT INTO questions (question, options, correct_answer, category, marks)
                    VALUES (?, ?, ?, ?, ?)
                """, (question, json.dumps(options), correct_idx, topic_name, 1))
                
                sheet_count += 1
            
            if sheet_count > 0:
                conn.commit()
                print(f"  ✅ SUCCESS: {sheet_count} questions imported")
                total_imported += sheet_count
                successful_sheets.append(f"Sheet {gid}: {sheet_count} questions ({topic_name})")
            else:
                print(f"  ⚠️  No valid questions found")
            
            # Small delay to avoid rate limiting
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:100]}")
            continue
    
    conn.close()
    
    # Summary
    print("\n" + "="*50)
    print("📊 IMPORT SUMMARY")
    print("="*50)
    for sheet_info in successful_sheets:
        print(f"  ✓ {sheet_info}")
    print(f"\n🎉 TOTAL QUESTIONS IMPORTED: {total_imported}")
    print("="*50)

if __name__ == "__main__":
    import_all_sheets()