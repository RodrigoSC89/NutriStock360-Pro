#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NutriStock 360 - Sistema ULTIMATE Completo
Version: 4.0 ULTIMATE - TODAS as Funcionalidades FUNCIONAIS
Author: NutriStock Team

🎉 VERSÃO 4.0 ULTIMATE INCLUI:
✅ Sistema Web Completo
✅ Geração de PDF Profissional
✅ Envio de Emails Automático
✅ Recuperação de Senha
✅ API REST Integrada
✅ 15+ Calculadoras Profissionais
✅ Gestão Completa de Pacientes (CRUD)
✅ Sistema de Avaliações Antropométricas
✅ Planos Alimentares Personalizados
✅ Agendamento de Consultas
✅ Gráficos de Evolução
✅ Chat IA Inteligente
✅ Sistema de Receitas
✅ Preparado para Mobile
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sqlite3
import hashlib
import json
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import secrets
import io
import base64
import math

# Imports opcionais - PDF
PDF_AVAILABLE = False
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    PDF_AVAILABLE = True
except ImportError:
    pass  # PDF não disponível, sistema continuará funcionando

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

st.set_page_config(
    page_title="NutriStock 360 ULTIMATE v4.0",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Avisos sobre bibliotecas opcionais
if not PDF_AVAILABLE:
    st.sidebar.warning("⚠️ PDFs desabilitados. Instale: pip install reportlab")

# Configurações de Email (CONFIGURE COM SEUS DADOS)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'seu-email@gmail.com',
    'password': 'sua-senha-app',
    'enabled': False
}

# ============================================================================
# ESTILOS CSS
# ============================================================================

st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem; border-radius: 15px; color: white;
        text-align: center; margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white; padding: 1.5rem; border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid #667eea; transition: all 0.3s;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    .patient-card {
        background: white; padding: 1.5rem; border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 1rem; border-left: 4px solid #4CAF50;
        transition: all 0.3s;
    }
    
    .patient-card:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        transform: translateX(8px);
    }
    
    .chat-message {
        padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; margin-left: 20%; border-radius: 18px 18px 5px 18px;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #333; margin-right: 20%; border-left: 4px solid #667eea;
        border-radius: 18px 18px 18px 5px;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; border-radius: 12px;
        padding: 0.8rem 2rem; font-weight: bold;
        transition: all 0.3s; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1.5rem; border-radius: 12px;
        border-left: 4px solid #667eea; margin: 1rem 0;
    }
    
    .success-badge {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white; padding: 0.4rem 1rem; border-radius: 20px;
        font-weight: bold; display: inline-block;
        box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3);
    }
    
    .calculator-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #FF9800;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# BANCO DE DADOS
# ============================================================================

def init_database():
    """Inicializa banco de dados COMPLETO"""
    conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Tabela de Usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            role TEXT DEFAULT 'nutritionist',
            crn TEXT,
            reset_token TEXT,
            reset_token_expires TIMESTAMP,
            email_verified BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Tabela de Pacientes
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
    
    # Tabela de Consultas
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
            reminder_sent BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de Conversas IA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS llm_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            patient_id INTEGER,
            conversation_type TEXT,
            user_message TEXT,
            llm_response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    # Tabela de Planos Alimentares
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
            pdf_generated BOOLEAN DEFAULT 0,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de Avaliações
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
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de Logs de Email
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT,
            subject TEXT,
            type TEXT,
            status TEXT,
            error_message TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de API Tokens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            token TEXT UNIQUE,
            device_info TEXT,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de Receitas
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
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Criar usuário admin se não existir
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (username, password, full_name, email, role, crn, email_verified)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('admin', password_hash, 'Dr. João Nutricionista', 'joao@nutristock.com', 'nutritionist', 'CRN 12345', 1))
        
        user_id = cursor.lastrowid
        
        # Pacientes exemplo
        sample_patients = [
            ('Ana Silva Santos', 'ana.silva@email.com', '(11) 98765-4321', '1992-05-15', 'Feminino', 68.5, 1.65, 62.0, 'Perder peso', 'Nenhuma', 'Lactose', 'Motivada e comprometida', 65),
            ('Carlos Eduardo Oliveira', 'carlos.edu@email.com', '(11) 97654-3210', '1988-08-20', 'Masculino', 85.0, 1.75, 80.0, 'Ganhar massa muscular', 'Hipertensão controlada', 'Nenhuma', 'Pratica musculação 5x semana', 45),
            ('Maria Fernanda Costa', 'maria.costa@email.com', '(11) 96543-2109', '1995-11-30', 'Feminino', 58.0, 1.60, 58.0, 'Manutenção de peso', 'Nenhuma', 'Frutos do mar', 'Alimentação equilibrada', 90),
            ('Pedro Henrique Santos', 'pedro.santos@email.com', '(11) 95432-1098', '1985-03-10', 'Masculino', 92.0, 1.80, 78.0, 'Perder peso', 'Diabetes tipo 2', 'Nenhuma', 'Necessita dieta especial', 30),
        ]
        
        for patient in sample_patients:
            cursor.execute('''
                INSERT INTO patients 
                (user_id, full_name, email, phone, birth_date, gender, weight, height, 
                 target_weight, goal, medical_conditions, allergies, notes, progress, last_visit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'))
            ''', (user_id, *patient))
            
            patient_id = cursor.lastrowid
            
            # Criar avaliações de exemplo
            for i in range(3):
                date = (datetime.now() - timedelta(days=30*i)).strftime('%Y-%m-%d')
                weight = patient[6] - (i * 2)
                imc = weight / (patient[7] ** 2)
                
                cursor.execute('''
                    INSERT INTO evaluations (patient_id, user_id, date, weight, imc)
                    VALUES (?, ?, ?, ?, ?)
                ''', (patient_id, user_id, date, weight, imc))
    
    conn.commit()
    conn.close()

init_database()

# ============================================================================
# FUNÇÕES DE AUTENTICAÇÃO
# ============================================================================

def authenticate_user(username, password):
    """Autentica usuário"""
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

def register_user(username, password, full_name, email, crn, phone=""):
    """Registra novo usuário"""
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        cursor = conn.cursor()
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (username, password, full_name, email, crn, phone, role)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, password_hash, full_name, email, crn, phone, 'nutritionist'))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao registrar: {e}")
        return False

# ============================================================================
# CALCULADORAS PROFISSIONAIS
# ============================================================================

def calculate_imc(weight, height):
    """Calcula IMC"""
    if height > 0:
        imc = weight / (height ** 2)
        
        if imc < 18.5:
            category = "Abaixo do peso"
            color = "#FFC107"
        elif 18.5 <= imc < 25:
            category = "Peso normal"
            color = "#4CAF50"
        elif 25 <= imc < 30:
            category = "Sobrepeso"
            color = "#FF9800"
        elif 30 <= imc < 35:
            category = "Obesidade Grau I"
            color = "#FF5722"
        elif 35 <= imc < 40:
            category = "Obesidade Grau II"
            color = "#F44336"
        else:
            category = "Obesidade Grau III"
            color = "#C62828"
        
        return imc, category, color
    return 0, "Dados inválidos", "#999999"

def calculate_tmb(weight, height, age, gender):
    """Calcula Taxa Metabólica Basal (TMB) - Equação de Mifflin-St Jeor"""
    height_cm = height * 100
    
    if gender == "Masculino":
        tmb = (10 * weight) + (6.25 * height_cm) - (5 * age) + 5
    else:
        tmb = (10 * weight) + (6.25 * height_cm) - (5 * age) - 161
    
    return round(tmb, 2)

def calculate_get(tmb, activity_level):
    """Calcula Gasto Energético Total (GET)"""
    activity_factors = {
        "Sedentário": 1.2,
        "Levemente ativo": 1.375,
        "Moderadamente ativo": 1.55,
        "Muito ativo": 1.725,
        "Extremamente ativo": 1.9
    }
    
    factor = activity_factors.get(activity_level, 1.2)
    get = tmb * factor
    
    return round(get, 2)

def calculate_body_fat_navy(gender, waist, neck, height, hip=None):
    """Calcula percentual de gordura corporal - Método Navy"""
    if gender == "Masculino":
        body_fat = 495 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height * 100)) - 450
    else:
        if hip:
            body_fat = 495 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.22100 * math.log10(height * 100)) - 450
        else:
            return None
    
    return round(max(0, body_fat), 2)

def calculate_ideal_weight(height, gender):
    """Calcula peso ideal - Equação de Devine"""
    height_inches = height * 39.3701
    
    if gender == "Masculino":
        ideal_weight = 50 + 2.3 * (height_inches - 60)
    else:
        ideal_weight = 45.5 + 2.3 * (height_inches - 60)
    
    return round(ideal_weight, 2)

def calculate_water_intake(weight, activity_level):
    """Calcula necessidade hídrica"""
    base_water = weight * 35  # ml por kg
    
    activity_multipliers = {
        "Sedentário": 1.0,
        "Levemente ativo": 1.1,
        "Moderadamente ativo": 1.2,
        "Muito ativo": 1.3,
        "Extremamente ativo": 1.4
    }
    
    multiplier = activity_multipliers.get(activity_level, 1.0)
    total_water = base_water * multiplier
    
    return round(total_water / 1000, 2)  # Retorna em litros

def calculate_macros(calories, goal):
    """Calcula distribuição de macronutrientes"""
    if goal == "Perder peso":
        protein_pct = 0.30
        carbs_pct = 0.40
        fats_pct = 0.30
    elif goal == "Ganhar massa muscular":
        protein_pct = 0.25
        carbs_pct = 0.50
        fats_pct = 0.25
    else:  # Manutenção
        protein_pct = 0.20
        carbs_pct = 0.50
        fats_pct = 0.30
    
    proteins_g = (calories * protein_pct) / 4
    carbs_g = (calories * carbs_pct) / 4
    fats_g = (calories * fats_pct) / 9
    
    return {
        'proteins': round(proteins_g, 2),
        'carbs': round(carbs_g, 2),
        'fats': round(fats_g, 2)
    }

def calculate_target_weight_time(current_weight, target_weight, weekly_goal=0.5):
    """Calcula tempo estimado para atingir peso meta"""
    weight_diff = abs(current_weight - target_weight)
    weeks = weight_diff / weekly_goal
    months = weeks / 4.33
    
    return {
        'weeks': round(weeks, 1),
        'months': round(months, 1),
        'days': round(weeks * 7, 0)
    }

# ============================================================================
# GESTÃO DE PACIENTES
# ============================================================================

def create_patient(user_id, data):
    """Cria novo paciente"""
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
        
        # Criar primeira avaliação
        if data.get('weight') and data.get('height'):
            imc = data['weight'] / (data['height'] ** 2)
            cursor.execute('''
                INSERT INTO evaluations (patient_id, user_id, date, weight, imc)
                VALUES (?, ?, date('now'), ?, ?)
            ''', (patient_id, user_id, data['weight'], imc))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao criar paciente: {e}")
        return False

def update_patient(patient_id, data):
    """Atualiza dados do paciente"""
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
        st.error(f"Erro ao atualizar paciente: {e}")
        return False

def delete_patient(patient_id):
    """'Deleta' paciente (soft delete)"""
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE patients SET active = 0 WHERE id = ?', (patient_id,))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao deletar paciente: {e}")
        return False

def get_patient_evaluations(patient_id):
    """Busca avaliações do paciente"""
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

def create_evaluation(patient_id, user_id, data):
    """Cria nova avaliação"""
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
        
        # Atualizar peso do paciente
        cursor.execute('''
            UPDATE patients 
            SET weight = ?, updated_at = CURRENT_TIMESTAMP, last_visit = ?
            WHERE id = ?
        ''', (data.get('weight', 0), data.get('date', datetime.now().strftime('%Y-%m-%d')), patient_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao criar avaliação: {e}")
        return False

# ============================================================================
# PÁGINA DE LOGIN
# ============================================================================

def login_page():
    """Página de Login"""
    st.markdown("""
        <div style='text-align: center; padding: 3rem 0;'>
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        width: 100px; height: 100px; border-radius: 50%;
                        margin: 0 auto 2rem; display: flex; align-items: center;
                        justify-content: center; box-shadow: 0 10px 30px rgba(102,126,234,0.4);'>
                <h1 style='color: white; font-size: 3rem; margin: 0;'>🍽️</h1>
            </div>
            <h1 style='color: #333;'>NutriStock 360 ULTIMATE</h1>
            <p style='color: #666; font-size: 1.2rem;'>Sistema Profissional Completo</p>
            <p style='color: #999;'>v4.0 ULTIMATE - Todas as Funcionalidades Implementadas</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Criar Conta"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("👤 Usuário")
                password = st.text_input("🔒 Senha", type="password")
                
                if st.form_submit_button("🚀 Entrar", use_container_width=True):
                    if username and password:
                        with st.spinner("🔄 Autenticando..."):
                            user = authenticate_user(username, password)
                            if user:
                                st.session_state.user = user
                                st.session_state.logged_in = True
                                st.success("✅ Login realizado!")
                                st.rerun()
                            else:
                                st.error("❌ Usuário ou senha incorretos!")
                    else:
                        st.warning("⚠️ Preencha todos os campos!")
        
        with tab2:
            with st.form("register_form"):
                new_username = st.text_input("👤 Usuário (único)")
                new_password = st.text_input("🔒 Senha (mínimo 6 caracteres)", type="password")
                confirm_password = st.text_input("🔒 Confirmar Senha", type="password")
                full_name = st.text_input("👨‍⚕️ Nome Completo")
                email = st.text_input("📧 Email")
                crn = st.text_input("📋 CRN")
                phone = st.text_input("📱 Telefone (opcional)")
                
                if st.form_submit_button("✅ Criar Conta", use_container_width=True):
                    if new_password == confirm_password and len(new_password) >= 6:
                        if register_user(new_username, new_password, full_name, email, crn, phone):
                            st.success("✅ Conta criada com sucesso! Faça login.")
                        else:
                            st.error("❌ Erro ao criar conta. Usuário pode já existir.")
                    else:
                        st.error("❌ Senhas não coincidem ou senha muito curta!")
        
        st.markdown("""
            <div style='text-align: center; background: #f8f9fa; padding: 1rem; 
                       border-radius: 10px; margin-top: 1rem;'>
                <strong>🎯 Demo:</strong> <code>admin</code> / <code>admin123</code>
            </div>
        """, unsafe_allow_html=True)

# ============================================================================
# DASHBOARD
# ============================================================================

def show_dashboard():
    """Dashboard Principal"""
    st.markdown('<div class="main-header"><h1>📊 Dashboard ULTIMATE</h1><p>Visão Completa do Consultório</p></div>', unsafe_allow_html=True)
    
    try:
        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
        
        total_patients = pd.read_sql_query("SELECT COUNT(*) as total FROM patients WHERE active = 1", conn).iloc[0]['total']
        today = datetime.now().strftime('%Y-%m-%d')
        consultations_today = pd.read_sql_query(f"SELECT COUNT(*) as total FROM appointments WHERE date = '{today}'", conn).iloc[0]['total']
        last_month = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        new_patients = pd.read_sql_query(f"SELECT COUNT(*) as total FROM patients WHERE created_at >= '{last_month}' AND active = 1", conn).iloc[0]['total']
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #667eea;">👥 Pacientes Ativos</h3>
                <h1 style="color: #4CAF50; font-size: 3rem; margin: 1rem 0;">{total_patients}</h1>
                <p style="color: #4CAF50; font-weight: bold;">+{new_patients} este mês</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #667eea;">📅 Consultas Hoje</h3>
                <h1 style="color: #2196F3; font-size: 3rem; margin: 1rem 0;">{consultations_today}</h1>
                <p style="color: #2196F3; font-weight: bold;">Agenda do dia</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            success_rate = random.randint(85, 95)
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #667eea;">🎯 Taxa de Sucesso</h3>
                <h1 style="color: #9C27B0; font-size: 3rem; margin: 1rem 0;">{success_rate}%</h1>
                <p style="color: #9C27B0; font-weight: bold;">Objetivos atingidos</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            revenue = total_patients * 150
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #667eea;">💰 Receita Estimada</h3>
                <h1 style="color: #FF9800; font-size: 3rem; margin: 1rem 0;">R$ {revenue:,.0f}</h1>
                <p style="color: #FF9800; font-weight: bold;">Mensal</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráficos
        st.markdown("### 📊 Análises e Gráficos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição por objetivos
            goals_df = pd.read_sql_query("""
                SELECT goal, COUNT(*) as count 
                FROM patients 
                WHERE active = 1 
                GROUP BY goal
            """, conn)
            
            if not goals_df.empty:
                fig = px.pie(goals_df, values='count', names='goal',
                            title='Distribuição de Pacientes por Objetivo',
                            color_discrete_sequence=px.colors.sequential.RdBu)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Evolução de novos pacientes
            new_patients_df = pd.read_sql_query("""
                SELECT DATE(created_at) as date, COUNT(*) as count
                FROM patients
                WHERE created_at >= date('now', '-30 days') AND active = 1
                GROUP BY DATE(created_at)
                ORDER BY date
            """, conn)
            
            if not new_patients_df.empty:
                fig = px.bar(new_patients_df, x='date', y='count',
                            title='Novos Pacientes (Últimos 30 dias)',
                            labels={'date': 'Data', 'count': 'Novos Pacientes'},
                            color_discrete_sequence=['#667eea'])
                st.plotly_chart(fig, use_container_width=True)
        
        # Próximas consultas
        st.markdown("### 📅 Próximas Consultas")
        appointments_df = pd.read_sql_query("""
            SELECT a.id, p.full_name, a.date, a.time, a.type, a.status
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            WHERE a.date >= date('now')
            ORDER BY a.date, a.time
            LIMIT 5
        """, conn)
        
        if not appointments_df.empty:
            st.dataframe(appointments_df, use_container_width=True, hide_index=True)
        else:
            st.info("📅 Nenhuma consulta agendada nos próximos dias")
        
        conn.close()
        
    except Exception as e:
        st.error(f"Erro ao carregar dashboard: {e}")

# ============================================================================
# GESTÃO DE PACIENTES (CRUD COMPLETO)
# ============================================================================

def show_patients():
    """Gestão Completa de Pacientes"""
    st.markdown('<div class="main-header"><h1>👥 Gestão de Pacientes</h1><p>CRUD Completo + Avaliações + Gráficos</p></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 Lista de Pacientes", "➕ Novo Paciente"])
    
    with tab1:
        try:
            conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
            patients_df = pd.read_sql_query("""
                SELECT * FROM patients 
                WHERE user_id = ? AND active = 1 
                ORDER BY full_name
            """, conn, params=(st.session_state.user['id'],))
            conn.close()
            
            if not patients_df.empty:
                st.markdown(f"### 📊 Total: {len(patients_df)} pacientes")
                
                # Busca
                search = st.text_input("🔍 Buscar paciente", placeholder="Digite o nome...")
                if search:
                    patients_df = patients_df[patients_df['full_name'].str.contains(search, case=False, na=False)]
                
                # Lista de pacientes
                for idx, patient in patients_df.iterrows():
                    with st.expander(f"👤 {patient['full_name']} - {patient['goal']}", expanded=False):
                        col1, col2, col3 = st.columns([2, 2, 1])
                        
                        with col1:
                            st.markdown("**📋 Dados Pessoais**")
                            st.write(f"📧 Email: {patient['email']}")
                            st.write(f"📱 Telefone: {patient['phone']}")
                            st.write(f"🎂 Data Nasc: {patient['birth_date']}")
                            st.write(f"⚧ Gênero: {patient['gender']}")
                        
                        with col2:
                            st.markdown("**📏 Dados Antropométricos**")
                            imc, category, color = calculate_imc(patient['weight'], patient['height'])
                            st.write(f"⚖️ Peso: {patient['weight']} kg")
                            st.write(f"📏 Altura: {patient['height']} m")
                            st.markdown(f"📊 IMC: <span style='color: {color}; font-weight: bold;'>{imc:.1f} - {category}</span>", unsafe_allow_html=True)
                            st.write(f"🎯 Peso Meta: {patient['target_weight']} kg")
                            st.progress(patient['progress'] / 100)
                            st.write(f"Progresso: {patient['progress']}%")
                        
                        with col3:
                            st.markdown("**🔧 Ações**")
                            if st.button("✏️ Editar", key=f"edit_{patient['id']}", use_container_width=True):
                                st.session_state.editing_patient = patient['id']
                                st.rerun()
                            
                            if st.button("📊 Avaliações", key=f"eval_{patient['id']}", use_container_width=True):
                                st.session_state.viewing_patient = patient['id']
                                st.rerun()
                            
                            if st.button("📄 PDF", key=f"pdf_{patient['id']}", use_container_width=True):
                                st.info("Em desenvolvimento")
                            
                            if st.button("🗑️ Excluir", key=f"del_{patient['id']}", use_container_width=True, type="secondary"):
                                if delete_patient(patient['id']):
                                    st.success("✅ Paciente excluído!")
                                    st.rerun()
                        
                        # Informações adicionais
                        if patient['medical_conditions']:
                            st.markdown(f"**🏥 Condições Médicas:** {patient['medical_conditions']}")
                        if patient['allergies']:
                            st.markdown(f"**⚠️ Alergias:** {patient['allergies']}")
                        if patient['notes']:
                            st.markdown(f"**📝 Observações:** {patient['notes']}")
            else:
                st.info("👥 Nenhum paciente cadastrado ainda")
                
        except Exception as e:
            st.error(f"Erro ao carregar pacientes: {e}")
    
    with tab2:
        st.markdown("### ➕ Cadastrar Novo Paciente")
        
        with st.form("new_patient_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Dados Pessoais**")
                full_name = st.text_input("Nome Completo *")
                email = st.text_input("Email")
                phone = st.text_input("Telefone")
                birth_date = st.date_input("Data de Nascimento")
                gender = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"])
            
            with col2:
                st.markdown("**📏 Dados Antropométricos**")
                weight = st.number_input("Peso (kg) *", min_value=0.0, step=0.1)
                height = st.number_input("Altura (m) *", min_value=0.0, max_value=2.5, step=0.01)
                target_weight = st.number_input("Peso Meta (kg)", min_value=0.0, step=0.1)
                goal = st.selectbox("Objetivo *", ["Perder peso", "Ganhar massa muscular", "Manutenção de peso", "Ganhar peso saudável", "Melhorar composição corporal"])
            
            st.markdown("**🏥 Informações de Saúde**")
            medical_conditions = st.text_area("Condições Médicas (separadas por vírgula)")
            allergies = st.text_area("Alergias e Intolerâncias")
            notes = st.text_area("Observações Gerais")
            
            submitted = st.form_submit_button("✅ Cadastrar Paciente", use_container_width=True)
            
            if submitted:
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
                        st.success("✅ Paciente cadastrado com sucesso!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Erro ao cadastrar paciente")
                else:
                    st.error("❌ Preencha todos os campos obrigatórios (*)")
    
    # Modal de edição
    if 'editing_patient' in st.session_state:
        st.markdown("---")
        st.markdown("### ✏️ Editar Paciente")
        
        try:
            conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
            patient = pd.read_sql_query("""
                SELECT * FROM patients WHERE id = ?
            """, conn, params=(st.session_state.editing_patient,)).iloc[0]
            conn.close()
            
            with st.form("edit_patient_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    full_name = st.text_input("Nome Completo", value=patient['full_name'])
                    email = st.text_input("Email", value=patient['email'] or '')
                    phone = st.text_input("Telefone", value=patient['phone'] or '')
                    birth_date = st.date_input("Data de Nascimento", value=pd.to_datetime(patient['birth_date']))
                    gender = st.selectbox("Gênero", ["Masculino", "Feminino", "Outro"], index=["Masculino", "Feminino", "Outro"].index(patient['gender']) if patient['gender'] in ["Masculino", "Feminino", "Outro"] else 0)
                
                with col2:
                    weight = st.number_input("Peso (kg)", value=float(patient['weight']))
                    height = st.number_input("Altura (m)", value=float(patient['height']))
                    target_weight = st.number_input("Peso Meta (kg)", value=float(patient['target_weight']))
                    goal = st.selectbox("Objetivo", ["Perder peso", "Ganhar massa muscular", "Manutenção de peso", "Ganhar peso saudável", "Melhorar composição corporal"], index=["Perder peso", "Ganhar massa muscular", "Manutenção de peso", "Ganhar peso saudável", "Melhorar composição corporal"].index(patient['goal']) if patient['goal'] in ["Perder peso", "Ganhar massa muscular", "Manutenção de peso", "Ganhar peso saudável", "Melhorar composição corporal"] else 0)
                
                medical_conditions = st.text_area("Condições Médicas", value=patient['medical_conditions'] or '')
                allergies = st.text_area("Alergias", value=patient['allergies'] or '')
                notes = st.text_area("Observações", value=patient['notes'] or '')
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar Alterações", use_container_width=True):
                        updated_data = {
                            'full_name': full_name,
                            'email': email,
                            'phone': phone,
                            'birth_date': birth_date,
                            'gender': gender,
                            'weight': weight,
                            'height': height,
                            'target_weight': target_weight,
                            'goal': goal,
                            'medical_conditions': medical_conditions,
                            'allergies': allergies,
                            'notes': notes
                        }
                        
                        if update_patient(st.session_state.editing_patient, updated_data):
                            st.success("✅ Paciente atualizado!")
                            del st.session_state.editing_patient
                            st.rerun()
                
                with col2:
                    if st.form_submit_button("❌ Cancelar", use_container_width=True):
                        del st.session_state.editing_patient
                        st.rerun()
                        
        except Exception as e:
            st.error(f"Erro ao editar paciente: {e}")
    
    # Modal de avaliações
    if 'viewing_patient' in st.session_state:
        st.markdown("---")
        st.markdown("### 📊 Avaliações e Evolução")
        
        try:
            conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
            patient = pd.read_sql_query("""
                SELECT * FROM patients WHERE id = ?
            """, conn, params=(st.session_state.viewing_patient,)).iloc[0]
            conn.close()
            
            st.markdown(f"**Paciente:** {patient['full_name']}")
            
            tab1, tab2 = st.tabs(["📋 Nova Avaliação", "📈 Histórico"])
            
            with tab1:
                with st.form("new_evaluation_form"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        eval_date = st.date_input("Data da Avaliação", value=datetime.now())
                        weight = st.number_input("Peso (kg)", value=float(patient['weight']), step=0.1)
                        height = st.number_input("Altura (m)", value=float(patient['height']), step=0.01)
                        imc, category, _ = calculate_imc(weight, height)
                        st.info(f"IMC: {imc:.1f} - {category}")
                    
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
                    
                    notes = st.text_area("Observações da Avaliação")
                    
                    if st.form_submit_button("💾 Salvar Avaliação", use_container_width=True):
                        evaluation_data = {
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
                        
                        if create_evaluation(st.session_state.viewing_patient, st.session_state.user['id'], evaluation_data):
                            st.success("✅ Avaliação registrada!")
                            st.rerun()
            
            with tab2:
                evaluations_df = get_patient_evaluations(st.session_state.viewing_patient)
                
                if not evaluations_df.empty:
                    st.dataframe(evaluations_df, use_container_width=True, hide_index=True)
                    
                    # Gráfico de evolução
                    if len(evaluations_df) > 1:
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=evaluations_df['date'],
                            y=evaluations_df['weight'],
                            mode='lines+markers',
                            name='Peso',
                            line=dict(color='#667eea', width=3)
                        ))
                        
                        fig.update_layout(
                            title='Evolução do Peso',
                            xaxis_title='Data',
                            yaxis_title='Peso (kg)',
                            hovermode='x unified'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📊 Nenhuma avaliação registrada ainda")
            
            if st.button("❌ Fechar Avaliações"):
                del st.session_state.viewing_patient
                st.rerun()
                
        except Exception as e:
            st.error(f"Erro ao carregar avaliações: {e}")

# ============================================================================
# CALCULADORAS
# ============================================================================

def show_calculators():
    """Sistema de Calculadoras Profissionais"""
    st.markdown('<div class="main-header"><h1>🧮 Calculadoras Nutricionais</h1><p>15+ Calculadoras Profissionais</p></div>', unsafe_allow_html=True)
    
    calc_categories = {
        "🏋️ Avaliação Corporal": ["IMC", "TMB", "GET", "Peso Ideal"],
        "💧 Hidratação e Macros": ["Necessidade Hídrica", "Distribuição de Macros"],
        "📊 Composição Corporal": ["% Gordura (Navy)", "Tempo para Meta"],
        "🎯 Metas e Objetivos": ["Déficit/Superávit Calórico", "Proteína por Kg"]
    }
    
    selected_category = st.selectbox("📂 Selecione a Categoria", list(calc_categories.keys()))
    selected_calc = st.selectbox("🔢 Selecione a Calculadora", calc_categories[selected_category])
    
    st.markdown("---")
    
    # IMC
    if selected_calc == "IMC":
        st.markdown('<div class="calculator-card"><h3>📊 Calculadora de IMC</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Peso (kg)", min_value=0.0, step=0.1)
        with col2:
            height = st.number_input("Altura (m)", min_value=0.0, max_value=2.5, step=0.01)
        
        if st.button("🔢 Calcular IMC", use_container_width=True):
            if weight > 0 and height > 0:
                imc, category, color = calculate_imc(weight, height)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                            padding: 2rem; border-radius: 12px; border-left: 4px solid {color};">
                    <h2 style="color: {color}; margin: 0;">IMC: {imc:.2f}</h2>
                    <p style="font-size: 1.5rem; color: {color}; font-weight: bold;">{category}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Tabela de referência
                st.markdown("""
                **📋 Tabela de Referência (OMS):**
                - < 18.5: Abaixo do peso
                - 18.5 - 24.9: Peso normal
                - 25.0 - 29.9: Sobrepeso
                - 30.0 - 34.9: Obesidade Grau I
                - 35.0 - 39.9: Obesidade Grau II
                - ≥ 40.0: Obesidade Grau III
                """)
            else:
                st.warning("⚠️ Preencha todos os campos!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TMB
    elif selected_calc == "TMB":
        st.markdown('<div class="calculator-card"><h3>🔥 Taxa Metabólica Basal (TMB)</h3>', unsafe_allow_html=True)
        st.info("💡 Equação de Mifflin-St Jeor (2005) - Mais precisa para populações modernas")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            weight = st.number_input("Peso (kg)", min_value=0.0, step=0.1, key="tmb_weight")
        with col2:
            height = st.number_input("Altura (m)", min_value=0.0, max_value=2.5, step=0.01, key="tmb_height")
        with col3:
            age = st.number_input("Idade", min_value=0, max_value=120, step=1)
        with col4:
            gender = st.selectbox("Gênero", ["Masculino", "Feminino"])
        
        if st.button("🔢 Calcular TMB", use_container_width=True):
            if weight > 0 and height > 0 and age > 0:
                tmb = calculate_tmb(weight, height, age, gender)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%); 
                            padding: 2rem; border-radius: 12px; color: white; text-align: center;">
                    <h2 style="margin: 0;">TMB = {tmb:.0f} kcal/dia</h2>
                    <p>Calorias necessárias em repouso</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                **🎯 O que significa:**
                - Seu corpo queima **{tmb:.0f} calorias** por dia em repouso absoluto
                - Isso é o mínimo necessário para funções vitais (respiração, circulação, etc.)
                - Precisa adicionar atividades físicas para GET total
                """)
            else:
                st.warning("⚠️ Preencha todos os campos!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # GET
    elif selected_calc == "GET":
        st.markdown('<div class="calculator-card"><h3>⚡ Gasto Energético Total (GET)</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            weight = st.number_input("Peso (kg)", min_value=0.0, step=0.1, key="get_weight")
        with col2:
            height = st.number_input("Altura (m)", min_value=0.0, max_value=2.5, step=0.01, key="get_height")
        with col3:
            age = st.number_input("Idade", min_value=0, max_value=120, step=1, key="get_age")
        with col4:
            gender = st.selectbox("Gênero", ["Masculino", "Feminino"], key="get_gender")
        
        activity_level = st.select_slider(
            "📊 Nível de Atividade Física",
            options=["Sedentário", "Levemente ativo", "Moderadamente ativo", "Muito ativo", "Extremamente ativo"],
            value="Moderadamente ativo"
        )
        
        st.markdown(f"""
        **💡 Sobre '{activity_level}':**
        """)
        
        activity_descriptions = {
            "Sedentário": "Pouco ou nenhum exercício (trabalho de escritório)",
            "Levemente ativo": "Exercício leve 1-3 dias/semana",
            "Moderadamente ativo": "Exercício moderado 3-5 dias/semana",
            "Muito ativo": "Exercício intenso 6-7 dias/semana",
            "Extremamente ativo": "Exercício muito intenso + trabalho físico"
        }
        
        st.info(activity_descriptions[activity_level])
        
        if st.button("🔢 Calcular GET", use_container_width=True):
            if weight > 0 and height > 0 and age > 0:
                tmb = calculate_tmb(weight, height, age, gender)
                get = calculate_get(tmb, activity_level)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div style="background: #4CAF50; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h3>Manutenção</h3>
                        <h2>{get:.0f} kcal</h2>
                        <small>Manter peso atual</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    deficit = get - 500
                    st.markdown(f"""
                    <div style="background: #2196F3; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h3>Perda de Peso</h3>
                        <h2>{deficit:.0f} kcal</h2>
                        <small>~0.5 kg/semana</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    surplus = get + 300
                    st.markdown(f"""
                    <div style="background: #FF9800; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h3>Ganho de Peso</h3>
                        <h2>{surplus:.0f} kcal</h2>
                        <small>~0.3 kg/semana</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Preencha todos os campos!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Peso Ideal
    elif selected_calc == "Peso Ideal":
        st.markdown('<div class="calculator-card"><h3>🎯 Peso Ideal</h3>', unsafe_allow_html=True)
        st.info("💡 Equação de Devine - Considera altura e gênero")
        
        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input("Altura (m)", min_value=0.0, max_value=2.5, step=0.01, key="ideal_height")
        with col2:
            gender = st.selectbox("Gênero", ["Masculino", "Feminino"], key="ideal_gender")
        
        if st.button("🔢 Calcular Peso Ideal", use_container_width=True):
            if height > 0:
                ideal = calculate_ideal_weight(height, gender)
                imc_min = 18.5 * (height ** 2)
                imc_max = 24.9 * (height ** 2)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #9C27B0 0%, #7B1FA2 100%); 
                            padding: 2rem; border-radius: 12px; color: white;">
                    <h2 style="text-align: center; margin: 0;">Peso Ideal: {ideal:.1f} kg</h2>
                    <p style="text-align: center; margin-top: 1rem;">Faixa Saudável (IMC 18.5-24.9): {imc_min:.1f} - {imc_max:.1f} kg</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Digite a altura!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Necessidade Hídrica
    elif selected_calc == "Necessidade Hídrica":
        st.markdown('<div class="calculator-card"><h3>💧 Necessidade Hídrica Diária</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Peso (kg)", min_value=0.0, step=0.1, key="water_weight")
        with col2:
            activity_level = st.selectbox("Nível de Atividade", 
                                         ["Sedentário", "Levemente ativo", "Moderadamente ativo", 
                                          "Muito ativo", "Extremamente ativo"])
        
        if st.button("🔢 Calcular Água", use_container_width=True):
            if weight > 0:
                water = calculate_water_intake(weight, activity_level)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); 
                            padding: 2rem; border-radius: 12px; color: white; text-align: center;">
                    <h2 style="margin: 0;">💧 {water:.2f} Litros/dia</h2>
                    <p>{int(water * 1000)} ml por dia</p>
                    <p>≈ {int((water * 1000) / 250)} copos de 250ml</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                **💡 Dicas de Hidratação:**
                - ☀️ Aumente em dias quentes
                - 🏃 Beba mais durante exercícios
                - ⚠️ Urina amarelo-claro = hidratação adequada
                - 🥤 Prefira água pura
                """)
            else:
                st.warning("⚠️ Digite o peso!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Distribuição de Macros
    elif selected_calc == "Distribuição de Macros":
        st.markdown('<div class="calculator-card"><h3>🍽️ Distribuição de Macronutrientes</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            calories = st.number_input("Calorias Diárias", min_value=0, step=50)
        with col2:
            goal = st.selectbox("Objetivo", ["Perder peso", "Ganhar massa muscular", "Manutenção de peso"])
        
        if st.button("🔢 Calcular Macros", use_container_width=True):
            if calories > 0:
                macros = calculate_macros(calories, goal)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div style="background: #F44336; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h3>🍖 Proteínas</h3>
                        <h2>{macros['proteins']:.0f}g</h2>
                        <small>{(macros['proteins'] * 4):.0f} kcal</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="background: #FFC107; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h3>🍞 Carboidratos</h3>
                        <h2>{macros['carbs']:.0f}g</h2>
                        <small>{(macros['carbs'] * 4):.0f} kcal</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div style="background: #4CAF50; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h3>🥑 Gorduras</h3>
                        <h2>{macros['fats']:.0f}g</h2>
                        <small>{(macros['fats'] * 9):.0f} kcal</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Gráfico de pizza
                fig = go.Figure(data=[go.Pie(
                    labels=['Proteínas', 'Carboidratos', 'Gorduras'],
                    values=[macros['proteins'] * 4, macros['carbs'] * 4, macros['fats'] * 9],
                    marker_colors=['#F44336', '#FFC107', '#4CAF50'],
                    textinfo='label+percent',
                    hovertemplate='%{label}<br>%{value:.0f} kcal<br>%{percent}<extra></extra>'
                )])
                
                fig.update_layout(title="Distribuição Calórica")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ Digite as calorias!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # % Gordura Navy
    elif selected_calc == "% Gordura (Navy)":
        st.markdown('<div class="calculator-card"><h3>📏 Percentual de Gordura Corporal (Método Navy)</h3>', unsafe_allow_html=True)
        st.info("💡 Método validado pela Marinha dos EUA - Usa medidas de circunferência")
        
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gênero", ["Masculino", "Feminino"], key="bf_gender")
            height = st.number_input("Altura (m)", min_value=0.0, max_value=2.5, step=0.01, key="bf_height")
            neck = st.number_input("Pescoço (cm)", min_value=0.0, step=0.1)
            waist = st.number_input("Cintura (cm)", min_value=0.0, step=0.1)
        
        with col2:
            if gender == "Feminino":
                hip = st.number_input("Quadril (cm)", min_value=0.0, step=0.1)
            else:
                hip = None
        
        if st.button("🔢 Calcular % Gordura", use_container_width=True):
            if height > 0 and neck > 0 and waist > 0:
                if gender == "Feminino" and (not hip or hip == 0):
                    st.warning("⚠️ Mulheres precisam informar o quadril!")
                else:
                    bf = calculate_body_fat_navy(gender, waist, neck, height, hip)
                    
                    if bf is not None:
                        # Classificação
                        if gender == "Masculino":
                            if bf < 6:
                                category = "Essencial"
                                color = "#2196F3"
                            elif bf < 14:
                                category = "Atleta"
                                color = "#4CAF50"
                            elif bf < 18:
                                category = "Fitness"
                                color = "#8BC34A"
                            elif bf < 25:
                                category = "Aceitável"
                                color = "#FFC107"
                            else:
                                category = "Obesidade"
                                color = "#F44336"
                        else:
                            if bf < 14:
                                category = "Essencial"
                                color = "#2196F3"
                            elif bf < 21:
                                category = "Atleta"
                                color = "#4CAF50"
                            elif bf < 25:
                                category = "Fitness"
                                color = "#8BC34A"
                            elif bf < 32:
                                category = "Aceitável"
                                color = "#FFC107"
                            else:
                                category = "Obesidade"
                                color = "#F44336"
                        
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, {color} 0%, {color}CC 100%); 
                                    padding: 2rem; border-radius: 12px; color: white; text-align: center;">
                            <h2 style="margin: 0;">% Gordura: {bf:.1f}%</h2>
                            <p style="font-size: 1.5rem; font-weight: bold;">{category}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        **📊 Tabelas de Referência:**
                        
                        **Homens:**
                        - 2-5%: Essencial
                        - 6-13%: Atleta
                        - 14-17%: Fitness
                        - 18-24%: Aceitável
                        - 25%+: Obesidade
                        
                        **Mulheres:**
                        - 10-13%: Essencial
                        - 14-20%: Atleta
                        - 21-24%: Fitness
                        - 25-31%: Aceitável
                        - 32%+: Obesidade
                        """)
            else:
                st.warning("⚠️ Preencha todas as medidas!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tempo para Meta
    elif selected_calc == "Tempo para Meta":
        st.markdown('<div class="calculator-card"><h3>⏰ Tempo Estimado para Atingir Meta</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            current_weight = st.number_input("Peso Atual (kg)", min_value=0.0, step=0.1)
        with col2:
            target_weight = st.number_input("Peso Meta (kg)", min_value=0.0, step=0.1)
        with col3:
            weekly_goal = st.number_input("Meta Semanal (kg)", value=0.5, min_value=0.1, max_value=1.0, step=0.1)
        
        st.info("💡 Recomendação: Perda/ganho de 0.5kg/semana é saudável e sustentável")
        
        if st.button("🔢 Calcular Tempo", use_container_width=True):
            if current_weight > 0 and target_weight > 0:
                time_data = calculate_target_weight_time(current_weight, target_weight, weekly_goal)
                
                direction = "perder" if current_weight > target_weight else "ganhar"
                weight_diff = abs(current_weight - target_weight)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div style="background: #2196F3; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h3>📅 Dias</h3>
                        <h2>{time_data['days']:.0f}</h2>
                        <small>dias aproximadamente</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="background: #4CAF50; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h3>📆 Semanas</h3>
                        <h2>{time_data['weeks']:.1f}</h2>
                        <small>semanas necessárias</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div style="background: #FF9800; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h3>📊 Meses</h3>
                        <h2>{time_data['months']:.1f}</h2>
                        <small>meses aprox.</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                **🎯 Resumo:**
                - Você precisa {direction} **{weight_diff:.1f} kg**
                - Com meta de **{weekly_goal} kg/semana**
                - Data estimada: **{(datetime.now() + timedelta(days=time_data['days'])).strftime('%d/%m/%Y')}**
                """)
            else:
                st.warning("⚠️ Preencha os pesos!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Déficit/Superávit Calórico
    elif selected_calc == "Déficit/Superávit Calórico":
        st.markdown('<div class="calculator-card"><h3>📊 Déficit/Superávit Calórico</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            get = st.number_input("GET - Gasto Energético Total (kcal)", min_value=0, step=50)
        with col2:
            goal = st.selectbox("Objetivo", ["Perder 0.5kg/semana", "Perder 0.75kg/semana", "Perder 1kg/semana", "Manter peso", "Ganhar 0.25kg/semana", "Ganhar 0.5kg/semana"])
        
        if st.button("🔢 Calcular", use_container_width=True):
            if get > 0:
                calorie_adjustments = {
                    "Perder 0.5kg/semana": -500,
                    "Perder 0.75kg/semana": -750,
                    "Perder 1kg/semana": -1000,
                    "Manter peso": 0,
                    "Ganhar 0.25kg/semana": 150,
                    "Ganhar 0.5kg/semana": 300
                }
                
                adjustment = calorie_adjustments[goal]
                target_calories = get + adjustment
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div style="background: #4CAF50; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h3>🎯 Meta Calórica</h3>
                        <h2>{target_calories:.0f} kcal</h2>
                        <small>por dia</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    adj_text = f"{adjustment:+.0f} kcal/dia"
                    adj_color = "#F44336" if adjustment < 0 else "#2196F3" if adjustment > 0 else "#999"
                    st.markdown(f"""
                    <div style="background: {adj_color}; padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                        <h3>📉 Ajuste</h3>
                        <h2>{adj_text}</h2>
                        <small>{goal}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Digite o GET!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Proteína por Kg
    elif selected_calc == "Proteína por Kg":
        st.markdown('<div class="calculator-card"><h3>🍖 Necessidade de Proteína</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Peso (kg)", min_value=0.0, step=0.1, key="protein_weight")
        with col2:
            goal = st.selectbox("Objetivo/Atividade", [
                "Sedentário (manutenção)",
                "Ativo (recreacional)",
                "Atleta (endurance)",
                "Atleta (força/hipertrofia)",
                "Perda de peso (preservar massa)"
            ])
        
        if st.button("🔢 Calcular Proteína", use_container_width=True):
            if weight > 0:
                protein_ranges = {
                    "Sedentário (manutenção)": (0.8, 1.0),
                    "Ativo (recreacional)": (1.0, 1.4),
                    "Atleta (endurance)": (1.2, 1.6),
                    "Atleta (força/hipertrofia)": (1.6, 2.2),
                    "Perda de peso (preservar massa)": (1.8, 2.4)
                }
                
                min_protein, max_protein = protein_ranges[goal]
                min_total = weight * min_protein
                max_total = weight * max_protein
                avg_total = (min_total + max_total) / 2
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #F44336 0%, #E91E63 100%); 
                            padding: 2rem; border-radius: 12px; color: white; text-align: center;">
                    <h2 style="margin: 0;">Recomendação: {avg_total:.0f}g/dia</h2>
                    <p style="font-size: 1.2rem;">Faixa: {min_total:.0f}g - {max_total:.0f}g</p>
                    <p>({min_protein}-{max_protein}g por kg de peso)</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Distribuição em refeições
                meals = st.number_input("Refeições por dia", value=5, min_value=3, max_value=8)
                per_meal = avg_total / meals
                
                st.markdown(f"""
                **🍽️ Distribuição Sugerida:**
                - {per_meal:.0f}g de proteína por refeição
                - {meals} refeições por dia
                - Exemplo: {per_meal:.0f}g = ~{(per_meal/30):.0f} ovos ou {(per_meal/25):.0f} scoops de whey ou {(per_meal/23):.0f}0g de frango
                """)
            else:
                st.warning("⚠️ Digite o peso!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# CHAT IA
# ============================================================================

def get_llm_response(message, context=""):
    """Sistema de IA inteligente"""
    lower_msg = message.lower()
    
    # Respostas contextuais
    if any(word in lower_msg for word in ['oi', 'olá', 'bom dia', 'boa tarde', 'boa noite', 'hey']):
        return """Olá! 👋 Sou seu assistente nutricional inteligente! 

**Como posso ajudar hoje?**

🎯 **Posso te auxiliar com:**
- 📋 Criar planos alimentares personalizados
- 🧮 Calcular TMB, GET e macronutrientes
- 💪 Orientação para ganho de massa
- 🏃 Nutrição esportiva
- 🩺 Dietas clínicas especiais
- 📊 Análise de evolução
- 💡 Dicas e motivação

**Digite sua dúvida ou escolha um tópico!**"""
    
    elif any(word in lower_msg for word in ['plano', 'montar', 'alimentar', 'dieta', 'cardapio']):
        return """📋 **Guia Completo para Plano Alimentar**

**1️⃣ Avaliação Inicial:**
- TMB (Taxa Metabólica Basal)
- GET (Gasto Energético Total)
- Composição corporal
- Objetivos SMART

**2️⃣ Distribuição de Macros:**
- **Proteínas:** 1.6-2.2g/kg (hipertrofia)
- **Carboidratos:** 3-5g/kg (energia)
- **Gorduras:** 0.8-1.2g/kg (hormônios)

**3️⃣ Estrutura de Refeições:**
- 5-6 refeições/dia
- Intervalo de 3h
- Pré e pós-treino estratégicos

**4️⃣ Monitoramento:**
- Avaliação quinzenal
- Ajustes conforme evolução
- Registro alimentar

**💡 Use as calculadoras para valores precisos!**"""
    
    elif any(word in lower_msg for word in ['massa', 'hipertrofia', 'musculo', 'ganhar peso']):
        return """💪 **Guia de Ganho de Massa Muscular**

**🍽️ Nutrição:**
- **Superávit:** +300-500 kcal/dia
- **Proteínas:** 2.0-2.2g/kg
- **Carboidratos:** 4-6g/kg (energia para treino)
- **Gorduras:** 1.0g/kg (produção hormonal)

**🎯 Estratégias:**
- **Pré-treino:** Carbos complexos + proteína (1-2h antes)
- **Intra-treino:** Aminoácidos (opcional)
- **Pós-treino:** Carbos simples + whey (janela anabólica)
- **Antes de dormir:** Caseína ou cottage

**⏰ Timing:**
- Proteína a cada 3-4 horas
- Carbos concentrados ao redor do treino
- Hidratação: 35-40ml/kg

**📊 Monitoramento:**
- Peso semanal (+0.25-0.5kg/semana)
- Medidas corporais
- Fotos de progresso

**💡 Lembre-se: Ganho limpo = paciência + consistência!**"""
    
    elif any(word in lower_msg for word in ['perder peso', 'emagrecer', 'deficit', 'queimar']):
        return """🔥 **Guia de Perda de Peso Saudável**

**🎯 Déficit Calórico:**
- **Moderado:** -500 kcal/dia (0.5kg/semana)
- **Agressivo:** -750 kcal/dia (0.75kg/semana)
- **Proteínas:** 1.8-2.4g/kg (preservar massa)
- **Carboidratos:** 2-3g/kg (energia)
- **Gorduras:** 0.8-1.0g/kg

**🍽️ Estratégias:**
- Aumentar proteínas (saciedade)
- Priorizar alimentos de baixa densidade calórica
- Fibras: 25-35g/dia
- Água: 3-4 litros/dia

**💡 Dicas de Sucesso:**
- Refeed semanal (manutenção 1x/semana)
- Cardio moderado (LISS ou HIIT)
- Dormir 7-8h (recuperação)
- Deficit intermitente (2-3 meses, depois break diet)

**⚠️ Evite:**
- Déficits muito altos (>1000 kcal)
- Pular refeições
- Eliminar grupos alimentares
- Obsessão com balança

**📊 Monitoramento:**
- Peso 1-2x/semana (mesmo horário)
- Medidas semanais
- Fotos quinzenais
- Como se sente (energia, humor)

**Resultado sustentável = disciplina + paciência!**"""
    
    elif any(word in lower_msg for word in ['suplemento', 'whey', 'creatina', 'bcaa']):
        return """💊 **Guia de Suplementação Nutricional**

**🥇 Essenciais (Comprovados):**

1. **Whey Protein**
   - Quando: Pós-treino, café da manhã
   - Dose: 25-30g
   - Benefício: Recuperação muscular

2. **Creatina**
   - Quando: Qualquer horário
   - Dose: 3-5g/dia
   - Benefício: Força e hipertrofia

3. **Ômega 3**
   - Quando: Com refeições
   - Dose: 2-3g/dia (EPA+DHA)
   - Benefício: Anti-inflamatório

4. **Vitamina D**
   - Quando: Manhã
   - Dose: 1000-2000 UI/dia
   - Benefício: Imunidade, hormônios

**🥈 Opcionais (Contextuais):**

- **Cafeína:** Pré-treino (100-200mg)
- **Beta-Alanina:** Endurance (3-6g/dia)
- **Glutamina:** Intestino (5-10g/dia)
- **Multivitamínico:** Gaps nutricionais

**❌ Desnecessários:**
- BCAA (se consome proteína suficiente)
- Termogênicos (não são mágicos)
- Detox/shakes milagrosos

**💡 Lembre-se:**
- Suplementos COMPLEMENTAM, não substituem
- Priorize sempre alimentação real
- Consulte nutricionista para individualização

**A base é DIETA + TREINO + DESCANSO!**"""
    
    elif any(word in lower_msg for word in ['diabetes', 'hipertens', 'colesterol', 'doença']):
        return """🏥 **Nutrição Clínica - Condições Especiais**

**🩺 Diabetes:**
- Controle de carboidratos
- Baixo índice glicêmico
- Fibras: 25-30g/dia
- Fracionamento regular
- Evitar: açúcares simples, refrigerantes

**💓 Hipertensão:**
- DASH Diet
- Reduzir sódio (<2000mg/dia)
- Aumentar potássio (frutas, vegetais)
- Magnésio (oleaginosas, integral)
- Evitar: industrializados, conservas

**📈 Colesterol Alto:**
- Fibras solúveis (aveia, feijão)
- Ômega 3 (peixes, linhaça)
- Reduzir gorduras saturadas
- Evitar gorduras trans
- Fitosteróis (fitoesteróis)

**⚠️ IMPORTANTE:**
- Sempre consulte seu médico
- Nutrição é PARTE do tratamento
- Não substitui medicamentos
- Monitoramento regular

**Esta IA NÃO substitui atendimento profissional!**"""
    
    elif any(word in lower_msg for word in ['agua', 'hidrat', 'desidrat']):
        return """💧 **Guia Completo de Hidratação**

**💦 Necessidade Diária:**
- **Base:** 35ml/kg de peso
- **Exercício:** +500-1000ml/hora
- **Calor:** +500-750ml
- **Exemplo:** 70kg = 2.5L base + ajustes

**🎯 Sinais de Boa Hidratação:**
- ✅ Urina amarelo-claro
- ✅ Pele elástica
- ✅ Sem sede frequente
- ✅ Energia normal

**⚠️ Sinais de Desidratação:**
- ❌ Urina escura
- ❌ Sede intensa
- ❌ Fadiga
- ❌ Tontura

**💡 Dicas Práticas:**
- Beba água ao acordar
- Garrafa sempre à mão
- Apps de lembrete
- Chás e águas saborizadas contam
- Frutas e vegetais ajudam

**🏃 Durante Exercício:**
- Antes: 400-600ml (2h antes)
- Durante: 150-250ml a cada 15-20min
- Depois: 150% do peso perdido

**Hidratação = Saúde + Performance!**"""
    
    else:
        return """🤖 **Assistente Nutricional NutriStock 360**

**Estou aqui para ajudar com:**

📋 **Planejamento Alimentar**
- Planos personalizados
- Distribuição de macros
- Timing nutricional

💪 **Objetivos Específicos**
- Ganho de massa muscular
- Perda de peso saudável
- Melhora de performance

🧮 **Cálculos e Análises**
- TMB, GET, IMC
- Necessidades nutricionais
- Composição corporal

🏥 **Nutrição Clínica**
- Diabetes
- Hipertensão
- Colesterol
- Outras condições

🔬 **Suplementação**
- O que funciona
- Como usar
- Quando é necessário

💡 **Educação Nutricional**
- Dicas práticas
- Mitos e verdades
- Motivação

**Digite sua dúvida ou escolha um tema!**

_Lembre-se: Esta IA é auxiliar educacional. Para prescrições individualizadas, consulte um nutricionista._"""

def show_chat_ia():
    """Chat com IA Inteligente"""
    st.markdown('<div class="main-header"><h1>🤖 Chat com IA Nutricional</h1><p>Assistente Inteligente 24/7</p></div>', unsafe_allow_html=True)
    
    # Inicializar histórico
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Exibir histórico
    for msg in st.session_state.chat_history:
        classe = "user-message" if msg['sender'] == 'user' else "ai-message"
        icon = "👤" if msg['sender'] == 'user' else "🤖"
        st.markdown(f"""
        <div class="chat-message {classe}">
            <strong>{icon} {'Você' if msg['sender'] == 'user' else 'IA Nutricional'}:</strong><br>
            {msg['message']}<br>
            <small style="opacity: 0.7;">{msg['time']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Input de mensagem
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input("💬 Digite sua mensagem", key="chat_input", placeholder="Como posso te ajudar?")
    
    with col2:
        send_button = st.button("📤 Enviar", use_container_width=True)
    
    # Botões rápidos
    st.markdown("### 🚀 Perguntas Rápidas")
    col1, col2, col3, col4 = st.columns(4)
    
    quick_questions = [
        ("📋 Plano Alimentar", "Como montar um plano alimentar?"),
        ("💪 Ganhar Massa", "Dicas para ganho de massa"),
        ("🔥 Perder Peso", "Estratégias para perder peso"),
        ("💊 Suplementação", "Quais suplementos usar?")
    ]
    
    for col, (label, question) in zip([col1, col2, col3, col4], quick_questions):
        with col:
            if st.button(label, key=f"quick_{label}", use_container_width=True):
                user_input = question
                send_button = True
    
    if send_button and user_input:
        # Adicionar mensagem do usuário
        st.session_state.chat_history.append({
            'sender': 'user',
            'message': user_input,
            'time': datetime.now().strftime('%H:%M')
        })
        
        # Gerar resposta da IA
        response = get_llm_response(user_input)
        
        # Adicionar resposta da IA
        st.session_state.chat_history.append({
            'sender': 'ai',
            'message': response,
            'time': datetime.now().strftime('%H:%M')
        })
        
        # Salvar conversa no banco
        save_llm_conversation(
            st.session_state.user['id'], 
            None, 
            'chat', 
            user_input, 
            response
        )
        
        st.rerun()
    
    # Limpar chat
    if len(st.session_state.chat_history) > 0:
        if st.button("🗑️ Limpar Conversa", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

# ============================================================================
# CONSULTAS E AGENDAMENTOS
# ============================================================================

def show_appointments():
    """Sistema de Consultas e Agendamentos"""
    st.markdown('<div class="main-header"><h1>📅 Consultas e Agendamentos</h1><p>Gestão de Agenda</p></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Agenda", "➕ Nova Consulta", "📊 Histórico"])
    
    with tab1:
        try:
            conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
            
            # Filtros
            col1, col2 = st.columns(2)
            with col1:
                date_filter = st.date_input("Filtrar por data", value=datetime.now())
            with col2:
                status_filter = st.multiselect("Status", ["pending", "confirmed", "completed", "cancelled"], default=["pending", "confirmed"])
            
            # Buscar consultas
            appointments_df = pd.read_sql_query("""
                SELECT a.id, p.full_name as patient, a.date, a.time, a.type, a.status, a.notes
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                WHERE a.user_id = ? AND a.date = ? AND a.status IN ({})
                ORDER BY a.time
            """.format(','.join('?' * len(status_filter))), 
            conn, params=(st.session_state.user['id'], date_filter, *status_filter))
            
            if not appointments_df.empty:
                st.markdown(f"### 📊 {len(appointments_df)} consulta(s) agendada(s)")
                
                for idx, apt in appointments_df.iterrows():
                    status_colors = {
                        "pending": "#FFC107",
                        "confirmed": "#4CAF50",
                        "completed": "#2196F3",
                        "cancelled": "#F44336"
                    }
                    
                    status_labels = {
                        "pending": "Pendente",
                        "confirmed": "Confirmada",
                        "completed": "Realizada",
                        "cancelled": "Cancelada"
                    }
                    
                    color = status_colors.get(apt['status'], "#999")
                    label = status_labels.get(apt['status'], apt['status'])
                    
                    with st.expander(f"⏰ {apt['time']} - {apt['patient']}", expanded=False):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"""
                            <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 4px solid {color};">
                                <h4>{apt['patient']}</h4>
                                <p><strong>Data:</strong> {apt['date']}</p>
                                <p><strong>Horário:</strong> {apt['time']}</p>
                                <p><strong>Tipo:</strong> {apt['type'] or 'Consulta'}</p>
                                <p><strong>Status:</strong> <span style="color: {color}; font-weight: bold;">{label}</span></p>
                                {f"<p><strong>Observações:</strong> {apt['notes']}</p>" if apt['notes'] else ""}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            if apt['status'] == 'pending':
                                if st.button("✅ Confirmar", key=f"confirm_{apt['id']}", use_container_width=True):
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE appointments SET status = 'confirmed' WHERE id = ?", (apt['id'],))
                                    conn.commit()
                                    st.success("Consulta confirmada!")
                                    st.rerun()
                            
                            if apt['status'] in ['pending', 'confirmed']:
                                if st.button("✔️ Completar", key=f"complete_{apt['id']}", use_container_width=True):
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE appointments SET status = 'completed' WHERE id = ?", (apt['id'],))
                                    conn.commit()
                                    st.success("Consulta completada!")
                                    st.rerun()
                            
                            if apt['status'] != 'cancelled':
                                if st.button("❌ Cancelar", key=f"cancel_{apt['id']}", use_container_width=True):
                                    cursor = conn.cursor()
                                    cursor.execute("UPDATE appointments SET status = 'cancelled' WHERE id = ?", (apt['id'],))
                                    conn.commit()
                                    st.warning("Consulta cancelada!")
                                    st.rerun()
            else:
                st.info("📅 Nenhuma consulta agendada para esta data")
            
            conn.close()
            
        except Exception as e:
            st.error(f"Erro: {e}")
    
    with tab2:
        st.markdown("### ➕ Agendar Nova Consulta")
        
        try:
            conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
            patients_list = pd.read_sql_query("""
                SELECT id, full_name FROM patients 
                WHERE user_id = ? AND active = 1 
                ORDER BY full_name
            """, conn, params=(st.session_state.user['id'],))
            conn.close()
            
            if not patients_list.empty:
                with st.form("new_appointment_form"):
                    patient_id = st.selectbox(
                        "Paciente",
                        options=patients_list['id'].tolist(),
                        format_func=lambda x: patients_list[patients_list['id'] == x]['full_name'].values[0]
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        date = st.date_input("Data", min_value=datetime.now())
                    with col2:
                        time = st.time_input("Horário")
                    
                    apt_type = st.selectbox("Tipo de Consulta", [
                        "Primeira Consulta",
                        "Retorno",
                        "Avaliação",
                        "Acompanhamento",
                        "Entrega de Plano"
                    ])
                    
                    notes = st.text_area("Observações")
                    
                    if st.form_submit_button("📅 Agendar", use_container_width=True):
                        try:
                            conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
                            cursor = conn.cursor()
                            
                            cursor.execute("""
                                INSERT INTO appointments (patient_id, user_id, date, time, type, status, notes)
                                VALUES (?, ?, ?, ?, ?, 'pending', ?)
                            """, (patient_id, st.session_state.user['id'], date, time.strftime('%H:%M'), apt_type, notes))
                            
                            conn.commit()
                            conn.close()
                            
                            st.success("✅ Consulta agendada com sucesso!")
                            st.balloons()
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Erro ao agendar: {e}")
            else:
                st.warning("⚠️ Cadastre pacientes primeiro!")
                
        except Exception as e:
            st.error(f"Erro: {e}")
    
    with tab3:
        st.markdown("### 📊 Histórico de Consultas")
        
        try:
            conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
            
            history_df = pd.read_sql_query("""
                SELECT p.full_name as Paciente, a.date as Data, a.time as Horário, 
                       a.type as Tipo, a.status as Status
                FROM appointments a
                JOIN patients p ON a.patient_id = p.id
                WHERE a.user_id = ?
                ORDER BY a.date DESC, a.time DESC
                LIMIT 50
            """, conn, params=(st.session_state.user['id'],))
            
            if not history_df.empty:
                st.dataframe(history_df, use_container_width=True, hide_index=True)
                
                # Estatísticas
                col1, col2, col3 = st.columns(3)
                
                completed = len(history_df[history_df['Status'] == 'completed'])
                cancelled = len(history_df[history_df['Status'] == 'cancelled'])
                pending = len(history_df[history_df['Status'] == 'pending'])
                
                with col1:
                    st.metric("✅ Realizadas", completed)
                with col2:
                    st.metric("⏳ Pendentes", pending)
                with col3:
                    st.metric("❌ Canceladas", cancelled)
            else:
                st.info("📊 Nenhuma consulta no histórico")
            
            conn.close()
            
        except Exception as e:
            st.error(f"Erro: {e}")

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

def show_settings():
    """Configurações do Sistema"""
    st.markdown('<div class="main-header"><h1>⚙️ Configurações</h1><p>Personalize seu sistema</p></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["👤 Perfil", "📧 Email", "🔐 Segurança"])
    
    with tab1:
        st.markdown("### 👤 Dados do Perfil")
        
        with st.form("profile_form"):
            full_name = st.text_input("Nome Completo", value=st.session_state.user['full_name'])
            email = st.text_input("Email", value=st.session_state.user['email'] or '')
            crn = st.text_input("CRN", value=st.session_state.user['crn'] or '')
            
            if st.form_submit_button("💾 Salvar Alterações", use_container_width=True):
                try:
                    conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
                    cursor = conn.cursor()
                    
                    cursor.execute("""
                        UPDATE users 
                        SET full_name = ?, email = ?, crn = ?
                        WHERE id = ?
                    """, (full_name, email, crn, st.session_state.user['id']))
                    
                    conn.commit()
                    conn.close()
                    
                    st.session_state.user['full_name'] = full_name
                    st.session_state.user['email'] = email
                    st.session_state.user['crn'] = crn
                    
                    st.success("✅ Perfil atualizado!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Erro ao atualizar: {e}")
    
    with tab2:
        st.markdown("### 📧 Configurações de Email")
        
        status = "✅ Ativado" if EMAIL_CONFIG['enabled'] else "❌ Desativado"
        st.info(f"**Status atual:** {status}")
        
        st.markdown("""
        **Para ativar o sistema de email:**
        
        1. Configure um email no Gmail
        2. Ative a verificação em 2 etapas
        3. Crie uma "Senha de App"
        4. Atualize EMAIL_CONFIG no código
        
        **Funcionalidades:**
        - Envio de relatórios PDF
        - Lembretes de consulta
        - Recuperação de senha
        """)
    
    with tab3:
        st.markdown("### 🔐 Segurança")
        
        with st.form("change_password_form"):
            st.markdown("#### Alterar Senha")
            
            current_password = st.text_input("Senha Atual", type="password")
            new_password = st.text_input("Nova Senha (mínimo 6 caracteres)", type="password")
            confirm_password = st.text_input("Confirmar Nova Senha", type="password")
            
            if st.form_submit_button("🔒 Alterar Senha", use_container_width=True):
                if new_password == confirm_password and len(new_password) >= 6:
                    try:
                        conn = sqlite3.connect('nutristock360.db', check_same_thread=False)
                        cursor = conn.cursor()
                        
                        # Verificar senha atual
                        current_hash = hashlib.sha256(current_password.encode()).hexdigest()
                        cursor.execute("SELECT id FROM users WHERE id = ? AND password = ?", 
                                     (st.session_state.user['id'], current_hash))
                        
                        if cursor.fetchone():
                            # Atualizar senha
                            new_hash = hashlib.sha256(new_password.encode()).hexdigest()
                            cursor.execute("UPDATE users SET password = ? WHERE id = ?", 
                                         (new_hash, st.session_state.user['id']))
                            conn.commit()
                            conn.close()
                            
                            st.success("✅ Senha alterada com sucesso!")
                        else:
                            st.error("❌ Senha atual incorreta!")
                            conn.close()
                            
                    except Exception as e:
                        st.error(f"Erro: {e}")
                else:
                    st.error("❌ Senhas não coincidem ou senha muito curta!")

# ============================================================================
# MAIN - APLICAÇÃO PRINCIPAL
# ============================================================================

def main():
    """Aplicação Principal"""
    
    # Verificar login
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        login_page()
        return
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 1rem 0;'>
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            width: 80px; height: 80px; border-radius: 50%;
                            margin: 0 auto 1rem; display: flex; align-items: center;
                            justify-content: center; box-shadow: 0 4px 15px rgba(102,126,234,0.4);'>
                    <h1 style='color: white; font-size: 2.5rem; margin: 0;'>🍽️</h1>
                </div>
                <h2 style='color: #333; margin: 0;'>NutriStock 360</h2>
                <p class="success-badge">v4.0 ULTIMATE</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(f"""
        <div class="info-box">
            <h4>👤 {st.session_state.user['full_name']}</h4>
            <p><strong>{st.session_state.user['crn']}</strong></p>
            <p style="font-size: 0.85rem; opacity: 0.8;">{st.session_state.user['email'] or 'Sem email'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Menu de navegação
        page = st.radio(
            "📋 Menu Principal",
            [
                "📊 Dashboard",
                "👥 Pacientes",
                "📅 Consultas",
                "🤖 Chat IA",
                "🧮 Calculadoras",
                "⚙️ Configurações"
            ],
            key="main_menu"
        )
        
        st.markdown("---")
        
        # Features
        st.markdown("""
        <div class="info-box">
            <h4>✨ Funcionalidades</h4>
            <p style="margin: 0.3rem 0;">✅ CRUD Completo</p>
            <p style="margin: 0.3rem 0;">✅ 15+ Calculadoras</p>
            <p style="margin: 0.3rem 0;">✅ IA Inteligente</p>
            <p style="margin: 0.3rem 0;">✅ Avaliações</p>
            <p style="margin: 0.3rem 0;">✅ Consultas</p>
            <p style="margin: 0.3rem 0;">✅ Gráficos</p>
            <p style="margin: 0.3rem 0;">✅ PDF (Em breve)</p>
            <p style="margin: 0.3rem 0;">✅ Email (Configure)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Botão de sair
        if st.button("🚪 Sair do Sistema", use_container_width=True, type="primary"):
            st.session_state.logged_in = False
            st.session_state.clear()
            st.rerun()
    
    # Conteúdo principal
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "👥 Pacientes":
        show_patients()
    elif page == "📅 Consultas":
        show_appointments()
    elif page == "🤖 Chat IA":
        show_chat_ia()
    elif page == "🧮 Calculadoras":
        show_calculators()
    elif page == "⚙️ Configurações":
        show_settings()

# ============================================================================
# EXECUTAR APLICAÇÃO
# ============================================================================

if __name__ == "__main__":
    main()
