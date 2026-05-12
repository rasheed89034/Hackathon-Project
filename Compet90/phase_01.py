import sqlite3
import random

def init_sqlite_db():
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    
    # Tables creation
    cursor.execute('''CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY, name TEXT, specialization TEXT, location TEXT, 
        consultation_type TEXT, status TEXT, rating REAL, bio TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS patient_leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT, patient_name TEXT, contact TEXT, 
        symptoms TEXT, doctor_id INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, doctor_id INTEGER, patient_name TEXT, 
        symptoms TEXT, appointment_time TEXT, consultation_type TEXT, 
        FOREIGN KEY (doctor_id) REFERENCES doctors (id))''')

    # Data Generation (150 Doctors)
    cursor.execute("SELECT COUNT(*) FROM doctors")
    if cursor.fetchone()[0] < 150:
        cursor.execute("DELETE FROM doctors")
        specs = {
            "Cardiologist": "Expert heart specialist, treats chest pain and heart surgery.",
            "Dermatologist": "Skin care expert, treats acne and laser treatments.",
            "Orthopedic": "Bone and joint specialist, expert in fractures and back pain.",
            "Pediatrician": "Child specialist for checkups and infections.",
            "Neurologist": "Brain and nerve expert, treats migraine and stroke."
        }
        cities = ["Karachi", "Lahore", "Islamabad", "Peshawar", "Quetta"]
        
        batch = []
        for i in range(1, 151):
            s = random.choice(list(specs.keys()))
            batch.append((i, f"Dr. {random.choice(['Ali', 'Sara', 'Usman', 'Zainab'])} {random.choice(['Khan', 'Ahmed', 'Malik'])}", 
                          s, random.choice(cities), random.choice(["Online", "Physical", "Both"]), 
                          random.choice(["Available", "Offline"]), round(random.uniform(4.0, 5.0), 1), specs[s]))
        
        # Test Profile
        batch.append((151, "Dr. Bilal", "Cardiologist", "Wah", "Both", "Available", 5.0, specs["Cardiologist"]))
        
        cursor.executemany("INSERT INTO doctors VALUES (?,?,?,?,?,?,?,?)", batch)
        conn.commit()
    conn.close()