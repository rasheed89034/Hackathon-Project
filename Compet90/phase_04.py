import sqlite3

def save_patient_lead(name, contact, symptoms, doctor_id):
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patient_leads (patient_name, contact, symptoms, doctor_id) VALUES (?,?,?,?)", 
                   (name, contact, symptoms, doctor_id))
    conn.commit()
    conn.close()

def generate_ai_intake_question(symptoms):
    # LLM-based autonomous intake
    return f"AI Agent: I see you mentioned '{symptoms}'. Can you tell me if this is a chronic or acute issue?"