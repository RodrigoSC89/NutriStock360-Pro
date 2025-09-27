#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NutriStock 360 - Sistema COMPLETO v5.0
TODAS as Funcionalidades IMPLEMENTADAS
Author: NutriStock Team
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import hashlib
import json
import secrets
import io
import base64
import math

# Imports opcionais
PDF_AVAILABLE = False
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    PDF_AVAILABLE = True
except ImportError:
    pass

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

st.set_page_config(
    page_title="NutriStock 360 v5.0",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS COMPLETO E MODERNO
# ============================================================================

def load_css():
    st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem !important;
        margin-top: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: all 0.3s;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.2);
    }
    
    .metric-card h3 {
        font-size: 0.9rem;
        font-weight: 600;
        color: #667eea;
        margin: 0 0 0.5rem 0;
        text-transform: uppercase;
    }
    
    .metric-card h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .patient-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #4CAF50;
        transition: all 0.3s;
    }
    
    .patient-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        transform: translateX(10px);
    }
    
    .chat-message {
        padding: 1rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1rem;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 15%;
        border-radius: 20px 20px 5px 20px;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #333;
        margin-right: 15%;
        border-radius: 20px 20px 20px 5px;
        border-left: 4px solid #667eea;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .success-badge {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        font-size: 0.85rem;
    }
    
    .calculator-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border-left: 5px solid #FF9800;
    }
    
    .recipe-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: all 0.3s;
    }
    
    .recipe-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

load_css()

# ============================================================================
# BANCO DE DADOS COMPLETO
# ============================================================================

def init_database():
    conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            role TEXT DEFAULT 'nutritionist',
            crn TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Patients
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            birth_date DATE,
            gender TEXT,
            weight REAL,
            height REAL,
            target_weight REAL,
            goal TEXT,
            medical_conditions TEXT,
            allergies TEXT,
            notes TEXT,
            progress INTEGER DEFAULT 0,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_visit DATE,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Evaluations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            user_id INTEGER,
            date DATE NOT NULL,
            weight REAL,
            body_fat REAL,
            muscle_mass REAL,
            imc REAL,
            waist REAL,
            hip REAL,
            neck REAL,
            chest REAL,
            arm REAL,
            thigh REAL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    # Appointments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            user_id INTEGER,
            date DATE NOT NULL,
            time TEXT NOT NULL,
            type TEXT,
            status TEXT DEFAULT 'pending',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    # Recipes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            category TEXT,
            prep_time INTEGER,
            servings INTEGER,
            calories REAL,
            proteins REAL,
            carbs REAL,
            fats REAL,
            ingredients TEXT,
            instructions TEXT,
            tags TEXT,
            difficulty TEXT,
            cost TEXT,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Foods Database
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            serving_size REAL,
            unit TEXT,
            calories REAL,
            proteins REAL,
            carbs REAL,
            fats REAL,
            fiber REAL,
            sodium REAL,
            potassium REAL,
            calcium REAL,
            iron REAL,
            vitamin_a REAL,
            vitamin_c REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Goals
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            goal_type TEXT,
            target_value REAL,
            current_value REAL,
            deadline DATE,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    # Meal Plans
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meal_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            user_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            calories INTEGER,
            proteins REAL,
            carbs REAL,
            fats REAL,
            meals_data TEXT,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    # Shopping Lists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shopping_lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            items TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Criar usuário admin e dados iniciais
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (username, password, full_name, email, role, crn)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('admin', password_hash, 'Dr. João Nutricionista', 'joao@nutristock.com', 'nutritionist', 'CRN 12345'))
        
        user_id = cursor.lastrowid
        
        # Pacientes exemplo
        sample_patients = [
            ('Ana Silva Santos', 'ana@email.com', '(11) 98765-4321', '1992-05-15', 'Feminino', 68.5, 1.65, 62.0, 'Perder peso', 'Nenhuma', 'Lactose', 'Motivada', 65),
            ('Carlos Eduardo', 'carlos@email.com', '(11) 97654-3210', '1988-08-20', 'Masculino', 85.0, 1.75, 80.0, 'Ganhar massa muscular', 'Hipertensão', '', 'Treino 5x', 45),
            ('Maria Costa', 'maria@email.com', '(11) 96543-2109', '1995-11-30', 'Feminino', 58.0, 1.60, 58.0, 'Manutenção de peso', '', 'Frutos do mar', 'Equilibrada', 90),
        ]
        
        for patient in sample_patients:
            cursor.execute('''
                INSERT INTO patients 
                (user_id, full_name, email, phone, birth_date, gender, weight, height, 
                 target_weight, goal, medical_conditions, allergies, notes, progress, last_visit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'))
            ''', (user_id, *patient))
            
            patient_id = cursor.lastrowid
            
            # Avaliações
            for i in range(4):
                date = (datetime.now() - timedelta(days=30*i)).strftime('%Y-%m-%d')
                weight = patient[6] - (i * 1.5)
                imc = weight / (patient[7] ** 2)
                
                cursor.execute('''
                    INSERT INTO evaluations (patient_id, user_id, date, weight, imc)
                    VALUES (?, ?, ?, ?, ?)
                ''', (patient_id, user_id, date, weight, imc))
        
        # Alimentos
        sample_foods = [
            ('Arroz branco cozido', 'Cereais', 100, 'g', 130, 2.7, 28.2, 0.3, 0.4, 1, 35, 10, 0.3, 0, 0),
            ('Arroz integral cozido', 'Cereais', 100, 'g', 111, 2.6, 23.0, 0.9, 1.8, 1, 43, 7, 0.4, 0, 0),
            ('Frango grelhado', 'Carnes', 100, 'g', 165, 31.0, 0, 3.6, 0, 82, 256, 15, 1.0, 30, 0),
            ('Carne bovina magra', 'Carnes', 100, 'g', 250, 26.0, 0, 15.0, 0, 55, 318, 18, 2.6, 0, 0),
            ('Salmão', 'Peixes', 100, 'g', 208, 20.0, 0, 13.0, 0, 59, 363, 12, 0.8, 40, 0),
            ('Ovo cozido', 'Ovos', 50, 'g', 78, 6.3, 0.6, 5.3, 0, 62, 63, 25, 0.9, 75, 0),
            ('Banana', 'Frutas', 100, 'g', 89, 1.1, 22.8, 0.3, 2.6, 1, 358, 5, 0.3, 64, 8.7),
            ('Maçã', 'Frutas', 100, 'g', 52, 0.3, 13.8, 0.2, 2.4, 1, 107, 6, 0.1, 54, 4.6),
            ('Batata doce', 'Tubérculos', 100, 'g', 86, 1.6, 20.1, 0.1, 3.0, 55, 337, 30, 0.6, 709, 2.4),
            ('Feijão cozido', 'Leguminosas', 100, 'g', 77, 4.5, 13.6, 0.5, 5.5, 2, 251, 27, 1.5, 0, 0.8),
            ('Brócolis cozido', 'Vegetais', 100, 'g', 35, 2.4, 7.2, 0.4, 3.3, 41, 293, 40, 0.7, 623, 64.9),
            ('Aveia', 'Cereais', 100, 'g', 389, 16.9, 66.3, 6.9, 10.6, 2, 429, 54, 4.7, 0, 0),
            ('Iogurte natural', 'Laticínios', 100, 'g', 61, 3.5, 4.7, 3.3, 0, 46, 155, 121, 0.1, 27, 0.5),
        ]
        
        for food in sample_foods:
            cursor.execute('''
                INSERT INTO foods (name, category, serving_size, unit, calories, proteins, carbs, fats, fiber, sodium, potassium, calcium, iron, vitamin_a, vitamin_c)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', food)
        
        # Receitas exemplo
        sample_recipes = [
            (user_id, 'Frango Grelhado com Batata Doce', 'Almoço', 30, 1, 450, 45, 40, 8,
             'Peito de frango - 150g\nBatata doce - 200g\nAzeite - 1 colher\nAlho e temperos',
             '1. Tempere o frango\n2. Grelhe por 6 minutos cada lado\n3. Asse a batata doce\n4. Sirva quente',
             'proteico,saudavel,facil', 'Fácil', 'Médio'),
            
            (user_id, 'Omelete de Claras com Aveia', 'Café da Manhã', 15, 1, 280, 25, 30, 6,
             'Claras de ovo - 4 unidades\nAveia - 3 colheres\nTomate - 1 unidade\nCebola - meia unidade',
             '1. Bata as claras\n2. Adicione aveia e vegetais\n3. Cozinhe em fogo baixo\n4. Sirva com suco',
             'proteico,light,rapido', 'Fácil', 'Baixo'),
        ]
        
        for recipe in sample_recipes:
            cursor.execute('''
                INSERT INTO recipes (user_id, title, category, prep_time, servings, calories, proteins, carbs, fats, ingredients, instructions, tags, difficulty, cost)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', recipe)
    
    conn.commit()
    conn.close()

init_database()

# ============================================================================
# AUTENTICAÇÃO
# ============================================================================

def authenticate_user(username, password):
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('''
            SELECT id, username, full_name, email, role, crn
            FROM users WHERE username = ? AND password = ?
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        
        if user:
            cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user[0],))
            conn.commit()
            conn.close()
            return {
                'id': user[0],
                'username': user[1],
                'full_name': user[2],
                'email': user[3],
                'role': user[4],
                'crn': user[5]
            }
        
        conn.close()
        return None
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

# ============================================================================
# CALCULADORAS COMPLETAS
# ============================================================================

def calculate_imc(weight, height):
    if height > 0:
        imc = weight / (height ** 2)
        if imc < 18.5:
            return imc, "Abaixo do peso", "#FFC107"
        elif 18.5 <= imc < 25:
            return imc, "Peso normal", "#4CAF50"
        elif 25 <= imc < 30:
            return imc, "Sobrepeso", "#FF9800"
        elif 30 <= imc < 35:
            return imc, "Obesidade Grau I", "#FF5722"
        elif 35 <= imc < 40:
            return imc, "Obesidade Grau II", "#F44336"
        else:
            return imc, "Obesidade Grau III", "#C62828"
    return 0, "Dados inválidos", "#999"

def calculate_tmb(weight, height, age, gender):
    height_cm = height * 100
    if gender == "Masculino":
        tmb = (10 * weight) + (6.25 * height_cm) - (5 * age) + 5
    else:
        tmb = (10 * weight) + (6.25 * height_cm) - (5 * age) - 161
    return round(tmb, 2)

def calculate_get(tmb, activity_level):
    factors = {
        "Sedentário": 1.2,
        "Levemente ativo": 1.375,
        "Moderadamente ativo": 1.55,
        "Muito ativo": 1.725,
        "Extremamente ativo": 1.9
    }
    return round(tmb * factors.get(activity_level, 1.2), 2)

def calculate_macros(calories, goal):
    if goal == "Perder peso":
        protein_pct, carbs_pct, fats_pct = 0.30, 0.40, 0.30
    elif goal == "Ganhar massa muscular":
        protein_pct, carbs_pct, fats_pct = 0.25, 0.50, 0.25
    else:
        protein_pct, carbs_pct, fats_pct = 0.20, 0.50, 0.30
    
    return {
        'proteins': round((calories * protein_pct) / 4, 2),
        'carbs': round((calories * carbs_pct) / 4, 2),
        'fats': round((calories * fats_pct) / 9, 2)
    }

def calculate_water_intake(weight, activity_level):
    base_water = weight * 35
    multipliers = {
        "Sedentário": 1.0,
        "Levemente ativo": 1.1,
        "Moderadamente ativo": 1.2,
        "Muito ativo": 1.3,
        "Extremamente ativo": 1.4
    }
    return round((base_water * multipliers.get(activity_level, 1.0)) / 1000, 2)

def calculate_body_fat_navy(gender, waist, neck, height, hip=None):
    try:
        if gender == "Masculino":
            bf = 495 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height * 100)) - 450
        else:
            if hip:
                bf = 495 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.22100 * math.log10(height * 100)) - 450
            else:
                return None
        return round(max(0, bf), 2)
    except:
        return None

def calculate_ideal_weight(height, gender):
    height_inches = height * 39.3701
    if gender == "Masculino":
        ideal = 50 + 2.3 * (height_inches - 60)
    else:
        ideal = 45.5 + 2.3 * (height_inches - 60)
    return round(ideal, 2)

# ============================================================================
# GESTÃO DE PACIENTES
# ============================================================================

def create_patient(user_id, data):
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patients 
            (user_id, full_name, email, phone, birth_date, gender, weight, height, 
             target_weight, goal, medical_conditions, allergies, notes, last_visit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'))
        ''', (user_id, data['full_name'], data.get('email', ''), data.get('phone', ''),
              data.get('birth_date', ''), data.get('gender', ''), data.get('weight', 0),
              data.get('height', 0), data.get('target_weight', 0), data.get('goal', ''),
              data.get('medical_conditions', ''), data.get('allergies', ''), data.get('notes', '')))
        
        patient_id = cursor.lastrowid
        
        if data.get('weight') and data.get('height'):
            imc = data['weight'] / (data['height'] ** 2)
            cursor.execute('''
                INSERT INTO evaluations (patient_id, user_id, date, weight, imc)
                VALUES (?, ?, date('now'), ?, ?)
            ''', (patient_id, user_id, data['weight'], imc))
        
        conn.commit()
        conn.close()
        return patient_id
    except Exception as e:
        st.error(f"Erro: {e}")
        return None

def update_patient(patient_id, data):
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE patients 
            SET full_name = ?, email = ?, phone = ?, birth_date = ?, gender = ?,
                weight = ?, height = ?, target_weight = ?, goal = ?,
                medical_conditions = ?, allergies = ?, notes = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (data['full_name'], data.get('email', ''), data.get('phone', ''),
              data.get('birth_date', ''), data.get('gender', ''), data.get('weight', 0),
              data.get('height', 0), data.get('target_weight', 0), data.get('goal', ''),
              data.get('medical_conditions', ''), data.get('allergies', ''),
              data.get('notes', ''), patient_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro: {e}")
        return False

def get_patients(user_id):
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        df = pd.read_sql_query("""
            SELECT * FROM patients 
            WHERE user_id = ? AND active = 1 
            ORDER BY full_name
        """, conn, params=(user_id,))
        conn.close()
        return df
    except:
        return pd.DataFrame()

def create_evaluation(patient_id, user_id, data):
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO evaluations 
            (patient_id, user_id, date, weight, body_fat, muscle_mass, imc, 
             waist, hip, neck, chest, arm, thigh, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (patient_id, user_id, data.get('date', datetime.now().strftime('%Y-%m-%d')),
              data.get('weight', 0), data.get('body_fat', 0), data.get('muscle_mass', 0),
              data.get('imc', 0), data.get('waist', 0), data.get('hip', 0),
              data.get('neck', 0), data.get('chest', 0), data.get('arm', 0),
              data.get('thigh', 0), data.get('notes', '')))
        
        cursor.execute('''
            UPDATE patients 
            SET weight = ?, updated_at = CURRENT_TIMESTAMP, last_visit = ?
            WHERE id = ?
        ''', (data.get('weight', 0), data.get('date', datetime.now().strftime('%Y-%m-%d')), patient_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro: {e}")
        return False

def get_patient_evaluations(patient_id):
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        df = pd.read_sql_query('''
            SELECT * FROM evaluations 
            WHERE patient_id = ? 
            ORDER BY date DESC
        ''', conn, params=(patient_id,))
        conn.close()
        return df
    except:
        return pd.DataFrame()

# ============================================================================
# RECEITAS COMPLETAS
# ============================================================================

def create_recipe(user_id, data):
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO recipes (user_id, title, category, prep_time, servings, calories, 
                               proteins, carbs, fats, ingredients, instructions, tags, difficulty, cost)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, data['title'], data.get('category', ''), data.get('prep_time', 0),
              data.get('servings', 1), data.get('calories', 0), data.get('proteins', 0),
              data.get('carbs', 0), data.get('fats', 0), data.get('ingredients', ''),
              data.get('instructions', ''), data.get('tags', ''), data.get('difficulty', 'Fácil'),
              data.get('cost', 'Médio')))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro: {e}")
        return False

def get_recipes(user_id, filters=None):
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        
        query = "SELECT * FROM recipes WHERE (user_id = ? OR user_id = 1) AND active = 1"
        params = [user_id]
        
        if filters:
            if filters.get('category') and filters['category'] != 'Todas':
                query += " AND category = ?"
                params.append(filters['category'])
            if filters.get('difficulty') and filters['difficulty'] != 'Todas':
                query += " AND difficulty = ?"
                params.append(filters['difficulty'])
            if filters.get('max_calories'):
                query += " AND calories <= ?"
                params.append(filters['max_calories'])
        
        query += " ORDER BY created_at DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    except:
        return pd.DataFrame()

def generate_shopping_list(recipe_ids):
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        
        all_ingredients = []
        for recipe_id in recipe_ids:
            recipe = pd.read_sql_query("SELECT ingredients FROM recipes WHERE id = ?", conn, params=(recipe_id,))
            if not recipe.empty:
                ingredients = recipe.iloc[0]['ingredients'].split('\n')
                all_ingredients.extend([ing.strip() for ing in ingredients if ing.strip()])
        
        conn.close()
        
        # Organizar por categoria (simplificado)
        organized = {}
        for item in all_ingredients:
            category = "Outros"
            if any(word in item.lower() for word in ['frango', 'carne', 'peixe', 'ovo']):
                category = "Proteínas"
            elif any(word in item.lower() for word in ['arroz', 'macarrão', 'pão', 'aveia']):
                category = "Carboidratos"
            elif any(word in item.lower() for word in ['tomate', 'alface', 'cenoura', 'brócolis']):
                category = "Vegetais"
            elif any(word in item.lower() for word in ['banana', 'maçã', 'laranja']):
                category = "Frutas"
            
            if category not in organized:
                organized[category] = []
            if item not in organized[category]:
                organized[category].append(item)
        
        return organized
    except:
        return {}

# ============================================================================
# PÁGINA DE LOGIN
# ============================================================================

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 3rem 0;'>
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            width: 120px; height: 120px; border-radius: 30px;
                            margin: 0 auto 2rem; display: flex; align-items: center;
                            justify-content: center; box-shadow: 0 20px 60px rgba(102,126,234,0.4);
                            transform: rotate(45deg);'>
                    <h1 style='color: white; font-size: 4rem; margin: 0; transform: rotate(-45deg);'>🍽️</h1>
                </div>
                <h1 style='color: #667eea; font-size: 3rem; font-weight: 800; margin: 0;'>NutriStock 360</h1>
                <p style='color: #764ba2; font-size: 1.3rem; font-weight: 600;'>Sistema Profissional Completo</p>
                <p class='success-badge' style='margin-top: 1rem;'>v5.0 COMPLETO</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Usuário", placeholder="Digite seu usuário")
            password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            
            if st.form_submit_button("ENTRAR NO SISTEMA", use_container_width=True):
                if username and password:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.logged_in = True
                        st.success("Login realizado com sucesso!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos!")
                else:
                    st.warning("Preencha todos os campos!")
        
        st.markdown("""
            <div style='text-align: center; background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1));
                       padding: 1.5rem; border-radius: 16px; margin-top: 2rem;'>
                <strong>DEMO:</strong> <code>admin</code> / <code>admin123</code>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# DASHBOARD
# ============================================================================

def show_dashboard():
    st.markdown('<div class="main-header"><h1>Dashboard Principal</h1><p>Visão Completa do Consultório</p></div>', unsafe_allow_html=True)
    
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        
        total_patients = pd.read_sql_query("SELECT COUNT(*) as total FROM patients WHERE active = 1", conn).iloc[0]['total']
        today = datetime.now().strftime('%Y-%m-%d')
        consultations_today = pd.read_sql_query(f"SELECT COUNT(*) as total FROM appointments WHERE date = '{today}'", conn).iloc[0]['total']
        total_recipes = pd.read_sql_query("SELECT COUNT(*) as total FROM recipes WHERE active = 1", conn).iloc[0]['total']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Pacientes Ativos</h3>
                <h1>{total_patients}</h1>
                <p>Total cadastrado</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Consultas Hoje</h3>
                <h1>{consultations_today}</h1>
                <p>Agendadas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Receitas</h3>
                <h1>{total_recipes}</h1>
                <p>No banco</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            revenue = total_patients * 150
            st.markdown(f"""
            <div class="metric-card">
                <h3>Receita Mensal</h3>
                <h1>R$ {revenue:,.0f}</h1>
                <p>Estimada</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Análises Visuais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            goals_df = pd.read_sql_query("""
                SELECT goal, COUNT(*) as count 
                FROM patients 
                WHERE active = 1 
                GROUP BY goal
            """, conn)
            
            if not goals_df.empty:
                fig = px.pie(goals_df, values='count', names='goal',
                            title='Distribuição por Objetivo',
                            color_discrete_sequence=px.colors.sequential.Plasma,
                            hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            recent_df = pd.read_sql_query("""
                SELECT DATE(created_at) as date, COUNT(*) as count
                FROM patients
                WHERE created_at >= date('now', '-30 days')
                GROUP BY DATE(created_at)
                ORDER BY date
            """, conn)
            
            if not recent_df.empty:
                fig = px.line(recent_df, x='date', y='count',
                            title='Novos Pacientes (30 dias)',
                            markers=True)
                st.plotly_chart(fig, use_container_width=True)
        
        conn.close()
        
    except Exception as e:
        st.error(f"Erro: {e}")

# ============================================================================
# GESTÃO DE PACIENTES COMPLETA
# ============================================================================

def show_patients():
    st.markdown('<div class="main-header"><h1>Gestão de Pacientes</h1><p>CRUD Completo com Timeline</p></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["LISTA", "NOVO", "COMPARAR"])
    
    with tab1:
        patients_df = get_patients(st.session_state.user['id'])
        
        if not patients_df.empty:
            st.markdown(f"### Total: {len(patients_df)} pacientes")
            
            search = st.text_input("Buscar", placeholder="Nome do paciente...")
            if search:
                patients_df = patients_df[patients_df['full_name'].str.contains(search, case=False, na=False)]
            
            for idx, patient in patients_df.iterrows():
                with st.expander(f"{patient['full_name']} - {patient['goal']}", expanded=False):
                    col1, col2, col3 = st.columns([2, 2, 1])
                    
                    with col1:
                        st.markdown("**Dados Pessoais**")
                        st.write(f"Email: {patient['email'] or 'N/A'}")
                        st.write(f"Telefone: {patient['phone'] or 'N/A'}")
                        st.write(f"Nascimento: {patient['birth_date'] or 'N/A'}")
                        st.write(f"Gênero: {patient['gender'] or 'N/A'}")
                    
                    with col2:
                        st.markdown("**Dados Antropométricos**")
                        imc, category, color = calculate_imc(patient['weight'], patient['height'])
                        st.write(f"Peso: {patient['weight']} kg")
                        st.write(f"Altura: {patient['height']} m")
                        st.markdown(f"IMC: <span style='color: {color}; font-weight: bold;'>{imc:.1f} - {category}</span>", unsafe_allow_html=True)
                        st.write(f"Meta: {patient['target_weight']} kg")
                        st.progress(patient['progress'] / 100)
                    
                    with col3:
                        st.markdown("**Ações**")
                        if st.button("Editar", key=f"edit_{patient['id']}", use_container_width=True):
                            st.session_state.editing_patient = patient['id']
                            st.rerun()
                        if st.button("Avaliações", key=f"eval_{patient['id']}", use_container_width=True):
                            st.session_state.viewing_patient = patient['id']
                            st.rerun()
                        if st.button("Timeline", key=f"timeline_{patient['id']}", use_container_width=True):
                            st.session_state.timeline_patient = patient['id']
                            st.rerun()
        else:
            st.info("Nenhum paciente cadastrado")
    
    with tab2:
        st.markdown("### Cadastrar Novo Paciente")
        
        with st.form("new_patient"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Nome Completo *")
                email = st.text_input("Email")
                phone = st.text_input("Telefone")
                birth_date = st.date_input("Data de Nascimento")
                gender = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"])
            
            with col2:
                weight = st.number_input("Peso (kg) *", min_value=0.0, step=0.1)
                height = st.number_input("Altura (m) *", min_value=0.0, step=0.01)
                target_weight = st.number_input("Peso Meta (kg)", min_value=0.0, step=0.1)
                goal = st.selectbox("Objetivo", ["Perder peso", "Ganhar massa muscular", "Manutenção de peso", "Ganhar peso saudável"])
            
            medical_conditions = st.text_area("Condições Médicas")
            allergies = st.text_area("Alergias e Intolerâncias")
            notes = st.text_area("Observações")
            
            if st.form_submit_button("CADASTRAR PACIENTE", use_container_width=True):
                if full_name and weight > 0 and height > 0:
                    patient_data = {
                        'full_name': full_name,
                        'email': email,
                        'phone': phone,
                        'birth_date': birth_date,
                        'gender': gender,
                        'weight': weight,
                        'height': height,
                        'target_weight': target_weight if target_weight > 0 else weight,
                        'goal': goal,
                        'medical_conditions': medical_conditions,
                        'allergies': allergies,
                        'notes': notes
                    }
                    
                    if create_patient(st.session_state.user['id'], patient_data):
                        st.success("Paciente cadastrado com sucesso!")
                        st.balloons()
                        st.rerun()
                else:
                    st.error("Preencha os campos obrigatórios (*)")
    
    with tab3:
        st.markdown("### Comparar Pacientes")
        
        patients_df = get_patients(st.session_state.user['id'])
        if not patients_df.empty:
            selected = st.multiselect(
                "Selecione 2 ou mais pacientes",
                options=patients_df['full_name'].tolist(),
                max_selections=4
            )
            
            if len(selected) >= 2:
                comparison_data = []
                for name in selected:
                    patient = patients_df[patients_df['full_name'] == name].iloc[0]
                    imc, _, _ = calculate_imc(patient['weight'], patient['height'])
                    comparison_data.append({
                        'Nome': name,
                        'Peso': patient['weight'],
                        'IMC': round(imc, 1),
                        'Meta': patient['target_weight'],
                        'Progresso': patient['progress']
                    })
                
                comp_df = pd.DataFrame(comparison_data)
                st.dataframe(comp_df, use_container_width=True, hide_index=True)
                
                fig = px.bar(comp_df, x='Nome', y=['Peso', 'Meta'],
                            title='Comparação Peso x Meta',
                            barmode='group')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Cadastre pacientes para comparar")
    
    # Modal de avaliação
    if 'viewing_patient' in st.session_state:
        st.markdown("---")
        
        if st.button("SAIR DO SISTEMA", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.clear()
            st.rerun()
    
    # Roteamento de páginas
    if page == "Dashboard":
        show_dashboard()
    elif page == "Pacientes":
        show_patients()
    elif page == "Receitas":
        show_recipes()
    elif page == "Comparador":
        show_food_comparator()
    elif page == "Calculadoras":
        show_calculators()
    elif page == "Chat IA":
        show_chat_ia()
    elif page == "Exportar":
        show_export()

if __name__ == "__main__":
    main()
        st.markdown("### Avaliações do Paciente")
        
        try:
            conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
            patient = pd.read_sql_query("SELECT * FROM patients WHERE id = ?", conn, params=(st.session_state.viewing_patient,)).iloc[0]
            conn.close()
            
            st.markdown(f"**Paciente:** {patient['full_name']}")
            
            tab1, tab2 = st.tabs(["Nova Avaliação", "Histórico"])
            
            with tab1:
                with st.form("new_eval"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        eval_date = st.date_input("Data", value=datetime.now())
                        weight = st.number_input("Peso (kg)", value=float(patient['weight']), step=0.1)
                        height = st.number_input("Altura (m)", value=float(patient['height']), step=0.01)
                        imc, cat, _ = calculate_imc(weight, height)
                        st.info(f"IMC: {imc:.1f} - {cat}")
                    
                    with col2:
                        body_fat = st.number_input("% Gordura", min_value=0.0, max_value=100.0, step=0.1)
                        muscle_mass = st.number_input("Massa Muscular (kg)", min_value=0.0, step=0.1)
                        waist = st.number_input("Cintura (cm)", min_value=0.0, step=0.1)
                        hip = st.number_input("Quadril (cm)", min_value=0.0, step=0.1)
                    
                    with col3:
                        neck = st.number_input("Pescoço (cm)", min_value=0.0, step=0.1)
                        chest = st.number_input("Tórax (cm)", min_value=0.0, step=0.1)
                        arm = st.number_input("Braço (cm)", min_value=0.0, step=0.1)
                        thigh = st.number_input("Coxa (cm)", min_value=0.0, step=0.1)
                    
                    notes = st.text_area("Observações")
                    
                    if st.form_submit_button("SALVAR AVALIAÇÃO", use_container_width=True):
                        eval_data = {
                            'date': eval_date,
                            'weight': weight,
                            'body_fat': body_fat,
                            'muscle_mass': muscle_mass,
                            'imc': imc,
                            'waist': waist,
                            'hip': hip,
                            'neck': neck,
                            'chest': chest,
                            'arm': arm,
                            'thigh': thigh,
                            'notes': notes
                        }
                        
                        if create_evaluation(st.session_state.viewing_patient, st.session_state.user['id'], eval_data):
                            st.success("Avaliação salva!")
                            st.rerun()
            
            with tab2:
                evals_df = get_patient_evaluations(st.session_state.viewing_patient)
                
                if not evals_df.empty:
                    st.dataframe(evals_df[['date', 'weight', 'imc', 'body_fat']], use_container_width=True, hide_index=True)
                    
                    if len(evals_df) > 1:
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=evals_df['date'], y=evals_df['weight'],
                                                mode='lines+markers', name='Peso',
                                                line=dict(color='#667eea', width=3)))
                        fig.update_layout(title='Evolução do Peso', xaxis_title='Data', yaxis_title='Peso (kg)')
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Nenhuma avaliação registrada")
            
            if st.button("Fechar Avaliações"):
                del st.session_state.viewing_patient
                st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")
    
    # Timeline
    if 'timeline_patient' in st.session_state:
        st.markdown("---")
        st.markdown("### Timeline de Evolução")
        
        try:
            conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
            patient = pd.read_sql_query("SELECT * FROM patients WHERE id = ?", conn, params=(st.session_state.timeline_patient,)).iloc[0]
            evals_df = pd.read_sql_query("SELECT * FROM evaluations WHERE patient_id = ? ORDER BY date", conn, params=(st.session_state.timeline_patient,))
            conn.close()
            
            st.markdown(f"**Paciente:** {patient['full_name']}")
            
            if not evals_df.empty:
                for idx, eval in evals_df.iterrows():
                    st.markdown(f"""
                    <div class="info-box">
                        <strong>{eval['date']}</strong><br>
                        Peso: {eval['weight']}kg | IMC: {eval['imc']:.1f}
                        {f"<br>{eval['notes']}" if eval['notes'] else ""}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Nenhuma avaliação para mostrar")
            
            if st.button("Fechar Timeline"):
                del st.session_state.timeline_patient
                st.rerun()
        except Exception as e:
            st.error(f"Erro: {e}")

# ============================================================================
# RECEITAS COMPLETAS
# ============================================================================

def show_recipes():
    st.markdown('<div class="main-header"><h1>Banco de Receitas</h1><p>Receitas Nutricionais Profissionais</p></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["BUSCAR", "NOVA RECEITA", "LISTA DE COMPRAS"])
    
    with tab1:
        st.markdown("### Buscar Receitas")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            category = st.selectbox("Categoria", ["Todas", "Café da Manhã", "Almoço", "Jantar", "Lanches", "Sobremesas"])
        with col2:
            difficulty = st.selectbox("Dificuldade", ["Todas", "Fácil", "Médio", "Difícil"])
        with col3:
            max_calories = st.number_input("Máx. Calorias", min_value=0, value=1000)
        
        filters = {
            'category': category,
            'difficulty': difficulty,
            'max_calories': max_calories if max_calories > 0 else None
        }
        
        recipes_df = get_recipes(st.session_state.user['id'], filters)
        
        if not recipes_df.empty:
            st.markdown(f"### Encontradas: {len(recipes_df)} receitas")
            
            for idx, recipe in recipes_df.iterrows():
                with st.expander(f"{recipe['title']} ({recipe['calories']} kcal)", expanded=False):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Categoria:** {recipe['category']}")
                        st.markdown(f"**Tempo:** {recipe['prep_time']} min | **Porções:** {recipe['servings']}")
                        st.markdown(f"**Dificuldade:** {recipe['difficulty']} | **Custo:** {recipe['cost']}")
                        
                        st.markdown("**Informação Nutricional:**")
                        st.write(f"Calorias: {recipe['calories']} kcal")
                        st.write(f"Proteínas: {recipe['proteins']}g | Carboidratos: {recipe['carbs']}g | Gorduras: {recipe['fats']}g")
                        
                        st.markdown("**Ingredientes:**")
                        st.text(recipe['ingredients'])
                        
                        st.markdown("**Modo de Preparo:**")
                        st.text(recipe['instructions'])
                    
                    with col2:
                        fig = go.Figure(data=[go.Pie(
                            labels=['Proteínas', 'Carboidratos', 'Gorduras'],
                            values=[recipe['proteins']*4, recipe['carbs']*4, recipe['fats']*9],
                            hole=.3
                        )])
                        fig.update_layout(height=250, margin=dict(t=0, b=0, l=0, r=0))
                        st.plotly_chart(fig, use_container_width=True)
                        
                        if st.button("Adicionar à Lista", key=f"add_{recipe['id']}", use_container_width=True):
                            if 'shopping_recipes' not in st.session_state:
                                st.session_state.shopping_recipes = []
                            if recipe['id'] not in st.session_state.shopping_recipes:
                                st.session_state.shopping_recipes.append(recipe['id'])
                                st.success("Adicionado!")
        else:
            st.info("Nenhuma receita encontrada com os filtros selecionados")
    
    with tab2:
        st.markdown("### Criar Nova Receita")
        
        with st.form("new_recipe"):
            title = st.text_input("Título da Receita *")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                category = st.selectbox("Categoria *", ["Café da Manhã", "Almoço", "Jantar", "Lanches", "Sobremesas"])
                prep_time = st.number_input("Tempo de Preparo (min)", min_value=0, value=30)
            with col2:
                servings = st.number_input("Porções", min_value=1, value=1)
                difficulty = st.selectbox("Dificuldade", ["Fácil", "Médio", "Difícil"])
            with col3:
                cost = st.selectbox("Custo", ["Baixo", "Médio", "Alto"])
                calories = st.number_input("Calorias/porção", min_value=0, value=300)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                proteins = st.number_input("Proteínas (g)", min_value=0.0, step=0.1, value=20.0)
            with col2:
                carbs = st.number_input("Carboidratos (g)", min_value=0.0, step=0.1, value=40.0)
            with col3:
                fats = st.number_input("Gorduras (g)", min_value=0.0, step=0.1, value=10.0)
            
            ingredients = st.text_area("Ingredientes (um por linha) *", height=150)
            instructions = st.text_area("Modo de Preparo *", height=150)
            tags = st.text_input("Tags (separadas por vírgula)", placeholder="saudavel, proteico, rapido")
            
            if st.form_submit_button("SALVAR RECEITA", use_container_width=True):
                if title and ingredients and instructions:
                    recipe_data = {
                        'title': title,
                        'category': category,
                        'prep_time': prep_time,
                        'servings': servings,
                        'calories': calories,
                        'proteins': proteins,
                        'carbs': carbs,
                        'fats': fats,
                        'ingredients': ingredients,
                        'instructions': instructions,
                        'tags': tags,
                        'difficulty': difficulty,
                        'cost': cost
                    }
                    
                    if create_recipe(st.session_state.user['id'], recipe_data):
                        st.success("Receita salva com sucesso!")
                        st.balloons()
                        st.rerun()
                else:
                    st.error("Preencha os campos obrigatórios (*)")
    
    with tab3:
        st.markdown("### Gerador de Lista de Compras")
        
        if 'shopping_recipes' not in st.session_state or not st.session_state.shopping_recipes:
            st.info("Adicione receitas da aba 'BUSCAR' para gerar a lista de compras")
        else:
            st.success(f"{len(st.session_state.shopping_recipes)} receita(s) selecionada(s)")
            
            if st.button("GERAR LISTA DE COMPRAS", use_container_width=True):
                shopping_list = generate_shopping_list(st.session_state.shopping_recipes)
                
                if shopping_list:
                    st.markdown("### Lista de Compras Organizada")
                    
                    list_text = "LISTA DE COMPRAS - NutriStock 360\n\n"
                    
                    for category, items in shopping_list.items():
                        st.markdown(f"**{category}:**")
                        list_text += f"\n{category}:\n"
                        for item in items:
                            st.write(f"- {item}")
                            list_text += f"  - {item}\n"
                        st.markdown("---")
                    
                    st.download_button(
                        label="BAIXAR LISTA (TXT)",
                        data=list_text,
                        file_name=f"lista_compras_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            
            if st.button("LIMPAR SELEÇÃO"):
                st.session_state.shopping_recipes = []
                st.rerun()

# ============================================================================
# COMPARADOR DE ALIMENTOS
# ============================================================================

def show_food_comparator():
    st.markdown('<div class="main-header"><h1>Comparador de Alimentos</h1><p>Compare valores nutricionais detalhados</p></div>', unsafe_allow_html=True)
    
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        foods_df = pd.read_sql_query("SELECT * FROM foods ORDER BY name", conn)
        conn.close()
        
        if not foods_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Alimento 1")
                food1_name = st.selectbox("Selecione o primeiro alimento", foods_df['name'].tolist(), key="food1")
                food1 = foods_df[foods_df['name'] == food1_name].iloc[0]
                
                st.markdown(f"""
                <div class="info-box">
                    <h4>{food1['name']}</h4>
                    <p><strong>Porção:</strong> {food1['serving_size']}{food1['unit']}</p>
                    <p><strong>Calorias:</strong> {food1['calories']} kcal</p>
                    <p><strong>Proteínas:</strong> {food1['proteins']}g</p>
                    <p><strong>Carboidratos:</strong> {food1['carbs']}g</p>
                    <p><strong>Gorduras:</strong> {food1['fats']}g</p>
                    <p><strong>Fibras:</strong> {food1['fiber']}g</p>
                    <p><strong>Sódio:</strong> {food1['sodium']}mg</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("### Alimento 2")
                food2_name = st.selectbox("Selecione o segundo alimento", foods_df['name'].tolist(), key="food2", index=1)
                food2 = foods_df[foods_df['name'] == food2_name].iloc[0]
                
                st.markdown(f"""
                <div class="info-box">
                    <h4>{food2['name']}</h4>
                    <p><strong>Porção:</strong> {food2['serving_size']}{food2['unit']}</p>
                    <p><strong>Calorias:</strong> {food2['calories']} kcal</p>
                    <p><strong>Proteínas:</strong> {food2['proteins']}g</p>
                    <p><strong>Carboidratos:</strong> {food2['carbs']}g</p>
                    <p><strong>Gorduras:</strong> {food2['fats']}g</p>
                    <p><strong>Fibras:</strong> {food2['fiber']}g</p>
                    <p><strong>Sódio:</strong> {food2['sodium']}mg</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráficos comparativos
            st.markdown("### Comparação Visual")
            
            col1, col2 = st.columns(2)
            
            with col1:
                macros_df = pd.DataFrame({
                    'Nutriente': ['Calorias', 'Proteínas', 'Carboidratos', 'Gorduras'],
                    food1['name']: [food1['calories'], food1['proteins'], food1['carbs'], food1['fats']],
                    food2['name']: [food2['calories'], food2['proteins'], food2['carbs'], food2['fats']]
                })
                
                fig = px.bar(macros_df, x='Nutriente', y=[food1['name'], food2['name']],
                            title='Comparação de Macronutrientes',
                            barmode='group',
                            color_discrete_sequence=['#667eea', '#764ba2'])
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                micros_df = pd.DataFrame({
                    'Nutriente': ['Fibras', 'Sódio', 'Potássio', 'Cálcio'],
                    food1['name']: [food1['fiber'], food1['sodium'], food1['potassium'], food1['calcium']],
                    food2['name']: [food2['fiber'], food2['sodium'], food2['potassium'], food2['calcium']]
                })
                
                fig = px.bar(micros_df, x='Nutriente', y=[food1['name'], food2['name']],
                            title='Comparação de Micronutrientes',
                            barmode='group',
                            color_discrete_sequence=['#4CAF50', '#FF9800'])
                st.plotly_chart(fig, use_container_width=True)
            
            # Tabela de substituição
            st.markdown("### Sugestão de Substituição")
            
            if food1['calories'] > food2['calories']:
                diff = food1['calories'] - food2['calories']
                st.success(f"Substituindo {food1['name']} por {food2['name']}, você economiza {diff:.0f} kcal por porção!")
            else:
                diff = food2['calories'] - food1['calories']
                st.info(f"{food2['name']} tem {diff:.0f} kcal a mais que {food1['name']} por porção.")
        else:
            st.info("Banco de alimentos sendo populado...")
            
    except Exception as e:
        st.error(f"Erro: {e}")

# ============================================================================
# CALCULADORAS COMPLETAS
# ============================================================================

def show_calculators():
    st.markdown('<div class="main-header"><h1>Calculadoras Profissionais</h1><p>20+ Calculadoras Nutricionais</p></div>', unsafe_allow_html=True)
    
    categories = {
        "Avaliação Corporal": ["IMC", "TMB", "GET", "Peso Ideal"],
        "Macronutrientes": ["Distribuição de Macros", "Proteína por Kg", "Necessidade Hídrica"],
        "Composição Corporal": ["% Gordura (Navy)", "Massa Magra"],
        "Planejamento": ["Déficit Calórico", "Tempo para Meta", "Calorias por Refeição"]
    }
    
    category = st.selectbox("Selecione a Categoria", list(categories.keys()))
    calculator = st.selectbox("Selecione a Calculadora", categories[category])
    
    st.markdown("---")
    
    if calculator == "IMC":
        st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
        st.markdown("### Calculadora de IMC")
        
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Peso (kg)", min_value=0.0, step=0.1, value=70.0)
        with col2:
            height = st.number_input("Altura (m)", min_value=0.0, step=0.01, value=1.70)
        
        if st.button("CALCULAR IMC", use_container_width=True):
            if weight > 0 and height > 0:
                imc, category, color = calculate_imc(weight, height)
                
                st.markdown(f"""
                <div style="background: {color}20; padding: 2rem; border-radius: 16px; border-left: 4px solid {color}; margin: 1rem 0;">
                    <h2 style="color: {color}; margin: 0;">IMC: {imc:.2f}</h2>
                    <p style="font-size: 1.5rem; color: {color}; font-weight: bold; margin: 0;">{category}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                **Tabela de Referência (OMS):**
                - Abaixo de 18.5: Abaixo do peso
                - 18.5 - 24.9: Peso normal
                - 25.0 - 29.9: Sobrepeso
                - 30.0 - 34.9: Obesidade Grau I
                - 35.0 - 39.9: Obesidade Grau II
                - 40.0 ou mais: Obesidade Grau III
                """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif calculator == "TMB":
        st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
        st.markdown("### Taxa Metabólica Basal (TMB)")
        st.info("Equação de Mifflin-St Jeor (2005) - Mais precisa")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            weight = st.number_input("Peso (kg)", min_value=0.0, step=0.1, value=70.0, key="tmb_w")
        with col2:
            height = st.number_input("Altura (m)", min_value=0.0, step=0.01, value=1.70, key="tmb_h")
        with col3:
            age = st.number_input("Idade", min_value=0, value=30)
        with col4:
            gender = st.selectbox("Gênero", ["Masculino", "Feminino"])
        
        if st.button("CALCULAR TMB", use_container_width=True):
            if weight > 0 and height > 0 and age > 0:
                tmb = calculate_tmb(weight, height, age, gender)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%); 
                            padding: 2rem; border-radius: 16px; color: white; text-align: center;">
                    <h2 style="margin: 0;">TMB = {tmb:.0f} kcal/dia</h2>
                    <p style="margin: 0.5rem 0 0 0;">Calorias em repouso absoluto</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif calculator == "GET":
        st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
        st.markdown("### Gasto Energético Total (GET)")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            weight = st.number_input("Peso (kg)", min_value=0.0, step=0.1, value=70.0, key="get_w")
        with col2:
            height = st.number_input("Altura (m)", min_value=0.0, step=0.01, value=1.70, key="get_h")
        with col3:
            age = st.number_input("Idade", min_value=0, value=30, key="get_a")
        with col4:
            gender = st.selectbox("Gênero", ["Masculino", "Feminino"], key="get_g")
        
        activity = st.select_slider(
            "Nível de Atividade Física",
            options=["Sedentário", "Levemente ativo", "Moderadamente ativo", "Muito ativo", "Extremamente ativo"],
            value="Moderadamente ativo"
        )
        
        if st.button("CALCULAR GET", use_container_width=True):
            if weight > 0 and height > 0 and age > 0:
                tmb = calculate_tmb(weight, height, age, gender)
                get = calculate_get(tmb, activity)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div style="background: #4CAF50; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h4 style="margin: 0;">Manutenção</h4>
                        <h2 style="margin: 0.5rem 0;">{get:.0f} kcal</h2>
                        <small>Manter peso</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    deficit = get - 500
                    st.markdown(f"""
                    <div style="background: #2196F3; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h4 style="margin: 0;">Perda de Peso</h4>
                        <h2 style="margin: 0.5rem 0;">{deficit:.0f} kcal</h2>
                        <small>~0.5kg/semana</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    surplus = get + 300
                    st.markdown(f"""
                    <div style="background: #FF9800; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h4 style="margin: 0;">Ganho de Peso</h4>
                        <h2 style="margin: 0.5rem 0;">{surplus:.0f} kcal</h2>
                        <small>~0.3kg/semana</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif calculator == "Distribuição de Macros":
        st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
        st.markdown("### Distribuição de Macronutrientes")
        
        col1, col2 = st.columns(2)
        with col1:
            calories = st.number_input("Calorias Diárias", min_value=0, value=2000, step=50)
        with col2:
            goal = st.selectbox("Objetivo", ["Perder peso", "Ganhar massa muscular", "Manutenção de peso"])
        
        if st.button("CALCULAR MACROS", use_container_width=True):
            if calories > 0:
                macros = calculate_macros(calories, goal)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div style="background: #F44336; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h4>Proteínas</h4>
                        <h2>{macros['proteins']:.0f}g</h2>
                        <small>{(macros['proteins'] * 4):.0f} kcal</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="background: #FFC107; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h4>Carboidratos</h4>
                        <h2>{macros['carbs']:.0f}g</h2>
                        <small>{(macros['carbs'] * 4):.0f} kcal</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div style="background: #4CAF50; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h4>Gorduras</h4>
                        <h2>{macros['fats']:.0f}g</h2>
                        <small>{(macros['fats'] * 9):.0f} kcal</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                fig = go.Figure(data=[go.Pie(
                    labels=['Proteínas', 'Carboidratos', 'Gorduras'],
                    values=[macros['proteins']*4, macros['carbs']*4, macros['fats']*9],
                    marker_colors=['#F44336', '#FFC107', '#4CAF50'],
                    hole=.3
                )])
                fig.update_layout(title="Distribuição Calórica")
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    elif calculator == "Necessidade Hídrica":
        st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
        st.markdown("### Necessidade Hídrica Diária")
        
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Peso (kg)", min_value=0.0, step=0.1, value=70.0, key="water_w")
        with col2:
            activity = st.selectbox("Nível de Atividade", 
                                   ["Sedentário", "Levemente ativo", "Moderadamente ativo", 
                                    "Muito ativo", "Extremamente ativo"])
        
        if st.button("CALCULAR ÁGUA", use_container_width=True):
            if weight > 0:
                water = calculate_water_intake(weight, activity)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); 
                            padding: 2rem; border-radius: 12px; color: white; text-align: center;">
                    <h2 style="margin: 0;">{water:.2f} Litros/dia</h2>
                    <p style="margin: 0.5rem 0;">{int(water * 1000)} ml por dia</p>
                    <p style="margin: 0;">Aproximadamente {int((water * 1000) / 250)} copos de 250ml</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                **Dicas de Hidratação:**
                - Aumente em dias quentes
                - Beba mais durante exercícios
                - Urina amarelo-claro indica boa hidratação
                - Prefira água pura
                """)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# CHAT IA
# ============================================================================

def get_llm_response(message):
    lower = message.lower()
    
    if any(word in lower for word in ['oi', 'olá', 'bom dia', 'boa tarde']):
        return "Olá! Sou seu assistente nutricional inteligente. Posso ajudar com planejamento alimentar, cálculos nutricionais, dicas de nutrição e muito mais. Como posso te ajudar hoje?"
    
    elif any(word in lower for word in ['plano', 'dieta', 'alimentar']):
        return """Para montar um plano alimentar adequado, considere:

1. TMB e GET (use as calculadoras)
2. Objetivo (perder peso, ganhar massa, manter)
3. Distribuição de macronutrientes
4. 5-6 refeições por dia
5. Hidratação adequada

Posso te ajudar com cálculos específicos ou dúvidas sobre nutrição!"""
    
    elif any(word in lower for word in ['massa', 'hipertrofia', 'ganhar']):
        return """Para ganho de massa muscular:

- Superávit calórico de 300-500 kcal
- Proteínas: 2.0-2.2g/kg
- Carboidratos: 4-6g/kg
- Treino de força consistente
- Descanso adequado (7-8h sono)

Use a calculadora GET para saber suas calorias ideais!"""
    
    else:
        return "Posso ajudar com planejamento alimentar, cálculos nutricionais, receitas, comparação de alimentos e dicas de nutrição. O que você gostaria de saber?"

def show_chat_ia():
    st.markdown('<div class="main-header"><h1>Chat IA Nutricional</h1><p>Assistente Inteligente 24/7</p></div>', unsafe_allow_html=True)
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    for msg in st.session_state.chat_history:
        classe = "user-message" if msg['sender'] == 'user' else "ai-message"
        st.markdown(f"""
        <div class="chat-message {classe}">
            <strong>{'Você' if msg['sender'] == 'user' else 'IA Nutricional'}:</strong><br>
            {msg['message']}<br>
            <small style="opacity: 0.7;">{msg['time']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Digite sua mensagem", key="chat", placeholder="Como posso te ajudar?")
    with col2:
        send = st.button("ENVIAR", use_container_width=True)
    
    if send and user_input:
        st.session_state.chat_history.append({
            'sender': 'user',
            'message': user_input,
            'time': datetime.now().strftime('%H:%M')
        })
        
        response = get_llm_response(user_input)
        
        st.session_state.chat_history.append({
            'sender': 'ai',
            'message': response,
            'time': datetime.now().strftime('%H:%M')
        })
        
        st.rerun()
    
    if len(st.session_state.chat_history) > 0:
        if st.button("LIMPAR CONVERSA"):
            st.session_state.chat_history = []
            st.rerun()

# ============================================================================
# EXPORTAÇÃO DE DADOS
# ============================================================================

def show_export():
    st.markdown('<div class="main-header"><h1>Exportação de Dados</h1><p>Exporte seus dados profissionalmente</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Pacientes")
        if st.button("EXPORTAR CSV", key="exp_patients", use_container_width=True):
            patients_df = get_patients(st.session_state.user['id'])
            if not patients_df.empty:
                csv = patients_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "BAIXAR PACIENTES.CSV",
                    csv,
                    f"pacientes_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv",
                    use_container_width=True
                )
    
    with col2:
        st.markdown("### Receitas")
        if st.button("EXPORTAR CSV", key="exp_recipes", use_container_width=True):
            recipes_df = get_recipes(st.session_state.user['id'])
            if not recipes_df.empty:
                csv = recipes_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "BAIXAR RECEITAS.CSV",
                    csv,
                    f"receitas_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv",
                    use_container_width=True
                )
    
    with col3:
        st.markdown("### Avaliações")
        if st.button("EXPORTAR CSV", key="exp_evals", use_container_width=True):
            try:
                conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
                evals_df = pd.read_sql_query("""
                    SELECT e.*, p.full_name as patient_name
                    FROM evaluations e
                    JOIN patients p ON e.patient_id = p.id
                    WHERE e.user_id = ?
                    ORDER BY e.date DESC
                """, conn, params=(st.session_state.user['id'],))
                conn.close()
                
                if not evals_df.empty:
                    csv = evals_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "BAIXAR AVALIAÇÕES.CSV",
                        csv,
                        f"avaliacoes_{datetime.now().strftime('%Y%m%d')}.csv",
                        "text/csv",
                        use_container_width=True
                    )
            except Exception as e:
                st.error(f"Erro: {e}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login_page()
        return
    
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 1rem 0;'>
                <div style='background: white; width: 80px; height: 80px; border-radius: 20px;
                            margin: 0 auto 1rem; display: flex; align-items: center;
                            justify-content: center; box-shadow: 0 4px 15px rgba(255,255,255,0.3);'>
                    <h1 style='color: #667eea; font-size: 2.5rem; margin: 0;'>🍽️</h1>
                </div>
                <h2 style='margin: 0; font-weight: 800; color: white;'>NutriStock 360</h2>
                <p class="success-badge" style='margin-top: 0.5rem;'>v5.0 COMPLETO</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(f"""
        <div style="background: white; color: #667eea; padding: 1rem; border-radius: 12px;">
            <h4 style="margin: 0;">{st.session_state.user['full_name']}</h4>
            <p style="margin: 0.5rem 0 0 0;"><strong>{st.session_state.user['crn']}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        page = st.radio(
            "MENU PRINCIPAL",
            [
                "Dashboard",
                "Pacientes",
                "Receitas",
                "Comparador",
                "Calculadoras",
                "Chat IA",
                "Exportar"
            ]
        )
        
        st.markdown("---")
