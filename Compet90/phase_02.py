import sqlite3
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

def load_data_from_db():
    conn = sqlite3.connect('healthcare.db')
    df = pd.read_sql_query("SELECT * FROM doctors", conn)
    conn.close()
    return df

def build_ai_search(df):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(df['bio'].tolist())
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype('float32'))
    return model, index

def get_llm_reasoning(doctor_name, symptoms):
    # Generative AI Reasoning Simulation
    return f"AI Reasoning: Dr. {doctor_name} specializes in cases like '{symptoms}' based on their clinical history."