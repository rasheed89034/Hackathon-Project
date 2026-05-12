import streamlit as st
import sqlite3
import pandas as pd
from phase_01 import init_sqlite_db
from phase_02 import load_data_from_db, build_ai_search, get_llm_reasoning
from phase_03 import suggest_optimal_slot
from phase_04 import save_patient_lead, generate_ai_intake_question

# --- 🛠️ STYLING & THEME ---
st.set_page_config(page_title="Smart Doctor Connect AI", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stSidebar { background-color: #455a64 !important; color: white; }
    .stButton>button { background-color: #4db6ac; color: white; border-radius: 5px; width: 100%; }
    .stExpander { background-color: white; border-radius: 10px; border: 1px solid #e0e0e0; }
    h1 { color: #00796b; font-family: 'Helvetica Neue', sans-serif; }
    .group-box { padding: 20px; background-color: #37474f; border-radius: 10px; border-left: 5px solid #4db6ac; }
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 INITIALIZATION ---
init_sqlite_db()
df, model, index = load_data_from_db(), *build_ai_search(load_data_from_db())

# --- 🛡️ SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/387/387561.png", width=100) 
    st.title("Neural Knights")
    with st.container():
        st.markdown(f"""
        <div class="group-box">
            <h4 style='color: #4db6ac; margin-top:0;'>🛡️ Group Details</h4>
            <p style='font-size: 0.9em;'><b>Project:</b> Smart Doctor Connect AI</p>
            <p style='font-size: 0.9em;'><b>Lead:</b> Rasheed Ahmad</p>
            <p style='font-size: 0.9em;'><b>Goal:</b> Healthcare Accessibility via Agentic AI</p>
        </div>
        """, unsafe_allow_html=True)
    st.divider()
    page = st.radio("Navigation Menu", ["🏠 Home / Search", "👨‍⚕️ Doctor Availability", "📊 Admin Dashboard"])
    st.info("Built for GDGoC CUI Wah Hackathon 2026")

# --- 🏥 MAIN CONTENT ---
if page == "🏠 Home / Search":
    st.title("We have more +150 doctors to take care of you")
    query = st.text_input("🔍 Describe symptoms in detail...", placeholder="e.g. Severe chest pain")
    
    if query:
        q_vec = model.encode([query]).astype('float32')
        D, I = index.search(q_vec, k=3)
        results = df.iloc[I[0]]
        
        for _, doc in results.iterrows():
            with st.expander(f"{doc['name']} - {doc['specialization']}"):
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.write(f"**Bio:** {doc['bio']}")
                    st.info(get_llm_reasoning(doc['name'], query))
                with col_b:
                    st.write(f"⭐ **Rating:** {doc['rating']}")
                    
                   
                    if doc['status'] == "Available":
                        slot = suggest_optimal_slot(doc['id'])
                        st.success(f"AI Suggests: {slot}")
                        
                       
                        with st.form(key=f"book_home_{doc['id']}"):
                            st.markdown("### 📅 Booking Details")
                            p_name = st.text_input("Your Full Name")
                            p_contact = st.text_input("Contact (WhatsApp/Email)")
                            
                            if st.form_submit_button("Confirm Booking"):
                                if p_name and p_contact:
                                    # Save data to patient_leads table
                                    save_patient_lead(p_name, p_contact, query, doc['id']) 
                                    st.balloons()
                                    st.success(f"Appointment confirmed for {slot}!")
                                    st.rerun()
                                else:
                                    st.warning("Please enter your name and contact info.")
                    else:
                        st.warning("Currently Offline")

elif page == "👨‍⚕️ Doctor Availability":
    st.header("👨‍⚕️ Specific Doctor Search & Slots")
    search_name = st.text_input("Search Doctor by Name", placeholder="Enter name...")
    
    if search_name:
        conn = sqlite3.connect('healthcare.db')
        doc_res = pd.read_sql_query(f"SELECT * FROM doctors WHERE name LIKE '%{search_name}%'", conn)
        
        if not doc_res.empty:
            for _, row in doc_res.iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.subheader(row['name'])
                        st.markdown(f"💼 **{row['specialization']}** | 📍 **{row['location']}**")
                    with c2:
                        st.write(f"⭐ **Rating: {row['rating']}**")
                    
                    st.divider()
                    count_query = f"SELECT COUNT(*) as total FROM appointments WHERE doctor_id = {row['id']}"
                    booked_today = pd.read_sql_query(count_query, conn)['total'][0]
                    
                    if booked_today < 70:
                        slot = suggest_optimal_slot(row['id'])
                        st.success(f"✅ AI suggests: **{slot}**")
                        with st.form(key=f"spec_form_{row['id']}"):
                            p_n = st.text_input("Patient Full Name")
                            p_c = st.text_input("Contact Details")
                            if st.form_submit_button("Confirm Booking"):
                                save_patient_lead(p_n, p_c, "Checkup", row['id'])
                                cursor = conn.cursor()
                                cursor.execute("INSERT INTO appointments (doctor_id, patient_name, symptoms, appointment_time, consultation_type) VALUES (?,?,?,?,?)", 
                                               (row['id'], p_n, "Routine Checkup", slot, row['consultation_type']))
                                conn.commit()
                                st.balloons()
                                st.rerun()
        conn.close()

elif page == "📊 Admin Dashboard":
    st.header("AI Agent Leads & Intake Records")
    conn = sqlite3.connect('healthcare.db')
    st.dataframe(pd.read_sql_query("SELECT * FROM patient_leads ORDER BY timestamp DESC", conn), use_container_width=True)
    conn.close()
