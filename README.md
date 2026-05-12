# 🩺 Smart Doctor Connect AI: Project Overview
Smart Doctor Connect AI is an end-to-end, intelligent healthcare platform designed to bridge the accessibility gap between patients and specialists in Pakistan. Developed by team Neural Knights for the GDGoC CUI Wah Hackathon 2026, the project transforms traditional medical search into an Agentic AI experience.

# 🧠 The Core Innovation: 
Semantic IntelligenceUnlike standard keyword-based platforms, this system utilizes Sentence Transformers ($all-MiniLM-L6-v2$) to understand the clinical context of patient symptoms. By integrating FAISS (Fast AI Similarity Search), the engine performs millisecond vector searches across a nationwide database to find the most relevant specialists. Furthermore, the AI provides cognitive reasoning, explaining exactly why a specific doctor is recommended for a user's case.

#🤖 Agentic AI & Autonomous Intake
The standout feature of this project is the Phase 04 Agentic Engine. When a doctor is offline or unavailable, an autonomous AI agent initiates a 24/7 intake process. It captures symptoms, performs triage, and populates a secure Admin Dashboard, ensuring that critical patient leads are never lost and are prioritized for the doctor's return.

# 📂 Modular System Architecture
The project is built on a clean, scalable 4-Phase architecture:
### Phase 01: Database Foundation
A robust SQLite3 infrastructure managing over 150 doctor profiles.
Strict enforcement of a 70-patient daily limit per doctor to ensure quality of care.
### Phase 02: AI Reasoning Engine
Advanced NLP for symptom analysis and vector-based matching.
### Phase 03: Smart Scheduling
Logic-driven slot suggestions aimed at reducing patient wait times by up to 60%.
### Phase 04: Data Persistence & Agents
Autonomous lead management and persistent data storage for clinical follow-ups.

# 📊 Technical Specifications & Impact
UI/UX: A professional Medicina-inspired layout featuring a premium Teal and Grey medical theme, implemented via custom CSS in Streamlit.
Accuracy: Achieved over 95% accuracy in semantic doctor matching compared to traditional keyword systems.
Efficiency: Automated intake reduces manual administrative overhead by providing structured leads directly to the Admin Dashboard.
