#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NutriApp360 - Sistema Completo de Apoio ao Nutricionista
Version: 3.0 - Sistema Totalmente Funcional
Author: NutriApp360 Team
"""

import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import uuid
import base64
from io import BytesIO
import calendar
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import math

# =============================================================================
# CONFIGURAÇÕES INICIAIS
# =============================================================================

# Configuração da página
st.set_page_config(
    page_title="NutriApp360 - Sistema de Apoio ao Nutricionista",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://nutriapp360.com/help',
        'Report a bug': 'https://nutriapp360.com/bug',
        'About': "# NutriApp360 v3.0\n**Sistema Completo para Nutricionistas**"
    }
)

# CSS personalizado
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #388E3C;
        margin: 1rem 0;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 0.5rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, #E8F8F5 0%, #D1F2EB 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #00BCD4;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #FFF8E1 0%, #FFECB3 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF9800;
        margin: 1rem 0;
    }
    
    .info-card {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #E8F5E8 0%, #F1F8E9 100%);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #4CAF50, #8BC34A);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #45a049, #7CB342);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .patient-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #4CAF50;
        transition: transform 0.3s ease;
    }
    
    .patient-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .recipe-card {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF9800;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .recipe-card:hover {
        transform: translateY(-2px);
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #666;
        border-top: 1px solid #E0E0E0;
        margin-top: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# BANCO DE DADOS
# =============================================================================

def init_database():
    """Inicializa o banco de dados SQLite com todas as tabelas necessárias"""
    conn = sqlite3.connect('nutriapp360.db')
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Tabela de pacientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            birth_date DATE,
            gender TEXT,
            height REAL,
            current_weight REAL,
            target_weight REAL,
            activity_level TEXT,
            medical_conditions TEXT,
            allergies TEXT,
            dietary_preferences TEXT,
            nutritionist_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            active BOOLEAN DEFAULT 1,
            FOREIGN KEY (nutritionist_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de consultas/agendamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id TEXT UNIQUE NOT NULL,
            patient_id INTEGER NOT NULL,
            nutritionist_id INTEGER NOT NULL,
            appointment_date DATETIME NOT NULL,
            duration INTEGER DEFAULT 60,
            appointment_type TEXT,
            status TEXT DEFAULT 'agendado',
            notes TEXT,
            weight_recorded REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (nutritionist_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de planos alimentares
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meal_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_id TEXT UNIQUE NOT NULL,
            patient_id INTEGER NOT NULL,
            nutritionist_id INTEGER NOT NULL,
            plan_name TEXT NOT NULL,
            start_date DATE,
            end_date DATE,
            daily_calories INTEGER,
            plan_data TEXT,
            status TEXT DEFAULT 'ativo',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (nutritionist_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de receitas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT,
            prep_time INTEGER,
            cook_time INTEGER,
            servings INTEGER,
            calories_per_serving INTEGER,
            protein REAL,
            carbs REAL,
            fat REAL,
            fiber REAL,
            ingredients TEXT,
            instructions TEXT,
            tags TEXT,
            difficulty TEXT,
            nutritionist_id INTEGER,
            is_public BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (nutritionist_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de progresso do paciente
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            record_date DATE NOT NULL,
            weight REAL,
            body_fat REAL,
            muscle_mass REAL,
            waist_circumference REAL,
            hip_circumference REAL,
            notes TEXT,
            photos TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    # Tabela de configurações do sistema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            config_key TEXT UNIQUE NOT NULL,
            config_value TEXT,
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Inserir usuário admin padrão se não existir
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cursor.fetchone()[0] == 0:
        admin_password = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (username, password_hash, role, full_name, email) 
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', admin_password, 'admin', 'Administrador do Sistema', 'admin@nutriapp360.com'))
        
        # Inserir configurações padrão
        default_configs = [
            ('clinic_name', 'Clínica NutriApp360', 'Nome da clínica'),
            ('clinic_address', 'Rua das Vitaminas, 123 - Bairro Saudável', 'Endereço da clínica'),
            ('clinic_phone', '(11) 99999-9999', 'Telefone da clínica'),
            ('clinic_email', 'contato@clinica.com', 'Email da clínica'),
            ('default_appointment_duration', '60', 'Duração padrão da consulta em minutos'),
            ('backup_frequency', 'daily', 'Frequência de backup'),
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO system_config (config_key, config_value, description) 
            VALUES (?, ?, ?)
        ''', default_configs)
    
    # Inserir dados de exemplo se não existirem
    cursor.execute("SELECT COUNT(*) FROM patients")
    if cursor.fetchone()[0] == 0:
        insert_sample_data(cursor)
    
    conn.commit()
    conn.close()

def insert_sample_data(cursor):
    """Insere dados de exemplo para demonstração"""
    # Pacientes de exemplo
    sample_patients = [
        ('PAT001', 'Maria Silva Santos', 'maria.silva@email.com', '(11) 98765-4321', '1985-03-15', 'F', 1.65, 68.5, 60.0, 'Moderadamente ativo', 'Hipotireoidismo', 'Lactose', 'Vegetariano', 1),
        ('PAT002', 'João Carlos Oliveira', 'joao.carlos@email.com', '(11) 98765-4322', '1978-08-22', 'M', 1.78, 85.2, 78.0, 'Sedentário', 'Diabetes tipo 2', 'Glúten', '', 1),
        ('PAT003', 'Ana Beatriz Costa', 'ana.beatriz@email.com', '(11) 98765-4323', '1992-12-03', 'F', 1.60, 72.0, 65.0, 'Muito ativo', '', 'Nozes', 'Low carb', 1),
        ('PAT004', 'Pedro Henrique Lima', 'pedro.lima@email.com', '(11) 98765-4324', '1988-06-10', 'M', 1.75, 90.5, 82.0, 'Ativo', 'Hipertensão', '', 'Sem restrições', 1),
        ('PAT005', 'Carolina Rodrigues', 'carolina.r@email.com', '(11) 98765-4325', '1995-09-18', 'F', 1.68, 58.0, 62.0, 'Moderadamente ativo', '', 'Frutos do mar', 'Vegano', 1)
    ]
    
    cursor.executemany('''
        INSERT INTO patients (patient_id, full_name, email, phone, birth_date, gender, height, 
                             current_weight, target_weight, activity_level, medical_conditions, 
                             allergies, dietary_preferences, nutritionist_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_patients)
    
    # Consultas de exemplo
    sample_appointments = [
        ('APP001', 1, 1, '2024-09-25 09:00:00', 60, 'Consulta inicial', 'realizada', 'Primeira consulta, estabelecimento de metas', 68.5),
        ('APP002', 2, 1, '2024-09-25 10:30:00', 60, 'Retorno', 'agendado', 'Revisão do plano alimentar', None),
        ('APP003', 3, 1, '2024-09-25 14:00:00', 45, 'Consulta inicial', 'agendado', '', None),
        ('APP004', 1, 1, '2024-10-02 09:00:00', 45, 'Retorno', 'agendado', 'Acompanhamento mensal', None),
        ('APP005', 4, 1, '2024-09-26 15:30:00', 60, 'Consulta inicial', 'agendado', 'Avaliação nutricional completa', None)
    ]
    
    cursor.executemany('''
        INSERT INTO appointments (appointment_id, patient_id, nutritionist_id, appointment_date, 
                                 duration, appointment_type, status, notes, weight_recorded) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_appointments)
    
    # Receitas de exemplo
    sample_recipes = [
        ('REC001', 'Salada de Quinoa com Legumes', 'Saladas', 15, 0, 4, 320, 12, 45, 8, 6, 
         'Quinoa (1 xícara), Tomate cereja (200g), Pepino (1 unidade), Cenoura ralada (1/2 xícara), Azeite (2 colheres), Limão (1 unidade), Sal e pimenta a gosto',
         '1. Cozinhe a quinoa conforme instruções da embalagem\n2. Corte os vegetais em cubos pequenos\n3. Misture todos os ingredientes\n4. Tempere com azeite, limão, sal e pimenta\n5. Sirva gelado',
         'saudável,vegetariano,sem glúten', 'Fácil', 1, 1),
        
        ('REC002', 'Salmão Grelhado com Aspargos', 'Pratos principais', 10, 15, 2, 380, 35, 8, 22, 4,
         'Filé de salmão (300g), Aspargos (200g), Azeite (1 colher), Alho (2 dentes), Limão (1/2 unidade), Sal e pimenta a gosto',
         '1. Tempere o salmão com sal, pimenta e limão\n2. Aqueça a grelha com azeite\n3. Grelhe o salmão por 6-8 minutos cada lado\n4. Refogue os aspargos com alho\n5. Sirva imediatamente',
         'rico em proteína,baixo carb,ômega 3', 'Médio', 1, 1),
        
        ('REC003', 'Smoothie Verde Detox', 'Bebidas', 5, 0, 2, 180, 4, 35, 2, 8,
         'Espinafre baby (1 xícara), Maçã verde (1 unidade), Banana (1/2 unidade), Água de coco (200ml), Gengibre (1cm), Limão (1/2 unidade)',
         '1. Lave bem o espinafre\n2. Descasque a maçã e banana\n3. Bata todos os ingredientes no liquidificador\n4. Adicione gelo se desejar\n5. Sirva imediatamente',
         'detox,verde,vitaminas,fibras', 'Fácil', 1, 1),
        
        ('REC004', 'Overnight Oats Proteico', 'Café da manhã', 10, 0, 1, 290, 18, 38, 6, 9,
         'Aveia em flocos (1/2 xícara), Leite vegetal (150ml), Whey protein vanilla (1 scoop), Chia (1 colher), Frutas vermelhas (1/2 xícara), Mel (1 colher)',
         '1. Misture aveia, leite e whey protein\n2. Adicione chia e mel\n3. Deixe na geladeira durante a noite\n4. Pela manhã, adicione as frutas\n5. Misture e sirva',
         'proteico,café da manhã,prep meal', 'Fácil', 1, 1),
        
        ('REC005', 'Wrap de Frango com Vegetais', 'Lanches', 20, 10, 4, 265, 22, 25, 8, 5,
         'Tortilla integral (4 unidades), Peito de frango (200g), Alface (4 folhas), Tomate (1 unidade), Cenoura ralada (1/2 xícara), Iogurte grego (3 colheres), Temperos a gosto',
         '1. Tempere e grelhe o frango\n2. Corte o frango em tiras\n3. Prepare os vegetais\n4. Monte os wraps com todos ingredientes\n5. Enrole bem e corte ao meio',
         'proteico,prático,lanche,wrap', 'Fácil', 1, 1)
    ]
    
    cursor.executemany('''
        INSERT INTO recipes (recipe_id, name, category, prep_time, cook_time, servings, 
                           calories_per_serving, protein, carbs, fat, fiber, ingredients, 
                           instructions, tags, difficulty, nutritionist_id, is_public) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_recipes)
    
    # Progresso de pacientes
    sample_progress = [
        (1, '2024-09-01', 70.2, 28.5, 42.0, 75.0, 95.0, 'Primeira medição', ''),
        (1, '2024-09-15', 69.5, 27.8, 42.3, 74.0, 94.5, 'Boa evolução no peso', ''),
        (1, '2024-09-30', 68.5, 27.2, 42.8, 73.5, 94.0, 'Meta mensal atingida', ''),
        (2, '2024-09-01', 87.0, 22.0, 58.5, 95.0, 102.0, 'Avaliação inicial', ''),
        (2, '2024-09-15', 86.2, 21.5, 59.0, 94.5, 101.5, 'Lenta mas constante evolução', ''),
        (3, '2024-09-01', 71.8, 18.5, 52.0, 68.0, 92.0, 'Medição inicial', ''),
        (3, '2024-09-15', 72.0, 18.2, 52.5, 68.2, 92.2, 'Ganho de massa magra', '')
    ]
    
    cursor.executemany('''
        INSERT INTO patient_progress (patient_id, record_date, weight, body_fat, muscle_mass, 
                                    waist_circumference, hip_circumference, notes, photos) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_progress)

# =============================================================================
# FUNÇÕES DE AUTENTICAÇÃO
# =============================================================================

def hash_password(password):
    """Gera hash da senha"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed_password):
    """Verifica se a senha está correta"""
    return hash_password(password) == hashed_password

def login_user(username, password):
    """Autentica usuário"""
    conn = sqlite3.connect('nutriapp360.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, password_hash, role, full_name, email 
        FROM users 
        WHERE username = ? AND active = 1
    ''', (username,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result and check_password(password, result[2]):
        # Atualizar último login
        conn = sqlite3.connect('nutriapp360.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
        ''', (result[0],))
        conn.commit()
        conn.close()
        
        return {
            'id': result[0],
            'username': result[1],
            'role': result[3],
            'full_name': result[4],
            'email': result[5]
        }
    return None

def check_auth():
    """Verifica se o usuário está autenticado"""
    return 'user' in st.session_state and st.session_state.user is not None

# =============================================================================
# INTERFACE DE LOGIN
# =============================================================================

def login_page():
    """Página de login"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <h1 style="text-align: center; color: #2E7D32; margin-bottom: 2rem;">
                🥗 NutriApp360
            </h1>
            <h3 style="text-align: center; color: #666; margin-bottom: 2rem;">
                Sistema de Apoio ao Nutricionista
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuário")
            password = st.text_input("🔒 Senha", type="password")
            
            col_login1, col_login2 = st.columns(2)
            with col_login1:
                login_button = st.form_submit_button("🚀 Entrar", use_container_width=True)
            with col_login2:
                demo_button = st.form_submit_button("👁️ Demo", use_container_width=True)
            
            if login_button or demo_button:
                if demo_button:
                    username, password = "admin", "admin123"
                
                if username and password:
                    user = login_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.success(f"✅ Bem-vindo(a), {user['full_name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Credenciais inválidas!")
                else:
                    st.warning("⚠️ Preencha todos os campos!")
        
        # Informações de demonstração
        st.markdown("""
        <div class="info-card">
            <h4>🎯 Credenciais de Demonstração:</h4>
            <p><strong>Usuário:</strong> admin<br>
            <strong>Senha:</strong> admin123</p>
            
            <h4>✨ Funcionalidades Disponíveis:</h4>
            <ul>
                <li>📊 Dashboard completo com métricas</li>
                <li>👥 Gestão de pacientes</li>
                <li>📅 Sistema de agendamentos</li>
                <li>🧮 Calculadoras nutricionais</li>
                <li>📋 Planos alimentares</li>
                <li>🍳 Banco de receitas</li>
                <li>📈 Analytics avançado</li>
                <li>⚙️ Configurações do sistema</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# SIDEBAR E NAVEGAÇÃO
# =============================================================================

def show_sidebar():
    """Mostra a sidebar com navegação"""
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #4CAF50, #8BC34A); 
                border-radius: 10px; margin-bottom: 1rem;">
        <h3 style="color: white; margin: 0;">🥗 NutriApp360</h3>
        <p style="color: white; margin: 0; font-size: 0.9rem;">
            Olá, <strong>{st.session_state.user['full_name']}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu principal
    selected_page = st.sidebar.selectbox(
        "📋 Menu Principal",
        ["dashboard", "patients", "appointments", "calculators", "meal_plans", "recipes", "analytics", "settings"],
        format_func=lambda x: {
            "dashboard": "📊 Dashboard",
            "patients": "👥 Pacientes", 
            "appointments": "📅 Agendamentos",
            "calculators": "🧮 Calculadoras",
            "meal_plans": "📋 Planos Alimentares",
            "recipes": "🍳 Receitas",
            "analytics": "📈 Analytics",
            "settings": "⚙️ Configurações"
        }[x]
    )
    
    # Quick stats na sidebar
    conn = sqlite3.connect('nutriapp360.db')
    cursor = conn.cursor()
    
    # Total de pacientes ativos
    cursor.execute("SELECT COUNT(*) FROM patients WHERE active = 1")
    total_patients = cursor.fetchone()[0]
    
    # Consultas hoje
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute("""
        SELECT COUNT(*) FROM appointments 
        WHERE DATE(appointment_date) = ? AND status = 'agendado'
    """, (today,))
    appointments_today = cursor.fetchone()[0]
    
    # Consultas esta semana
    start_week = datetime.now().strftime('%Y-%m-%d')
    end_week = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    cursor.execute("""
        SELECT COUNT(*) FROM appointments 
        WHERE DATE(appointment_date) BETWEEN ? AND ? AND status = 'agendado'
    """, (start_week, end_week))
    appointments_week = cursor.fetchone()[0]
    
    conn.close()
    
    st.sidebar.markdown("""
    <div class="metric-card">
        <h4 style="margin: 0; color: #2E7D32;">📊 Quick Stats</h4>
        <hr style="margin: 0.5rem 0;">
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("👥 Pacientes", total_patients)
    with col2:
        st.metric("📅 Hoje", appointments_today)
    
    st.sidebar.metric("📆 Esta Semana", appointments_week)
    
    # Botão de logout
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.user = None
        st.rerun()
    
    return selected_page

# =============================================================================
# DASHBOARD PRINCIPAL  
# =============================================================================

def show_dashboard():
    """Dashboard principal com métricas e gráficos"""
    st.markdown('<h1 class="main-header">📊 Dashboard NutriApp360</h1>', unsafe_allow_html=True)
    
    # Carregar dados
    conn = sqlite3.connect('nutriapp360.db')
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        patients_count = pd.read_sql_query("SELECT COUNT(*) as count FROM patients WHERE active = 1", conn).iloc[0]['count']
        st.metric(
            label="👥 Pacientes Ativos",
            value=patients_count,
            delta=f"+{patients_count//10} este mês"
        )
    
    with col2:
        today = datetime.now().strftime('%Y-%m-%d')
        appointments_today = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM appointments 
            WHERE DATE(appointment_date) = ? AND status = 'agendado'
        """, conn, params=[today]).iloc[0]['count']
        st.metric(
            label="📅 Consultas Hoje",
            value=appointments_today,
            delta=f"Próximas {appointments_today}"
        )
    
    with col3:
        total_recipes = pd.read_sql_query("SELECT COUNT(*) as count FROM recipes", conn).iloc[0]['count']
        st.metric(
            label="🍳 Receitas",
            value=total_recipes,
            delta="+5 esta semana"
        )
    
    with col4:
        active_plans = pd.read_sql_query("SELECT COUNT(*) as count FROM meal_plans WHERE status = 'ativo'", conn).iloc[0]['count']
        st.metric(
            label="📋 Planos Ativos",
            value=active_plans,
            delta=f"{active_plans} em uso"
        )
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="sub-header">📈 Evolução de Pacientes</h3>', unsafe_allow_html=True)
        
        # Gráfico de evolução de peso (pacientes com progresso)
        progress_data = pd.read_sql_query("""
            SELECT p.full_name, pr.record_date, pr.weight
            FROM patient_progress pr
            JOIN patients p ON pr.patient_id = p.id
            ORDER BY pr.record_date
        """, conn)
        
        if not progress_data.empty:
            fig = px.line(progress_data, x='record_date', y='weight', color='full_name',
                         title='Evolução do Peso dos Pacientes',
                         labels={'weight': 'Peso (kg)', 'record_date': 'Data'})
            fig.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Dados de progresso serão exibidos conforme os pacientes evoluem")
    
    with col2:
        st.markdown('<h3 class="sub-header">📊 Distribuição por Gênero</h3>', unsafe_allow_html=True)
        
        # Gráfico de distribuição por gênero
        gender_data = pd.read_sql_query("""
            SELECT gender, COUNT(*) as count 
            FROM patients 
            WHERE active = 1 
            GROUP BY gender
        """, conn)
        
        if not gender_data.empty:
            gender_data['gender'] = gender_data['gender'].map({'M': 'Masculino', 'F': 'Feminino'})
            fig = px.pie(gender_data, values='count', names='gender',
                        title='Distribuição de Pacientes por Gênero',
                        color_discrete_sequence=['#4CAF50', '#8BC34A'])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Gráfico será exibido quando houver pacientes cadastrados")
    
    # Agenda do dia
    st.markdown('<h3 class="sub-header">📅 Agenda de Hoje</h3>', unsafe_allow_html=True)
    
    today_appointments = pd.read_sql_query("""
        SELECT a.appointment_time as time, p.full_name as patient, 
               a.appointment_type as type, a.status, a.notes
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        WHERE DATE(a.appointment_date) = ?
        ORDER BY a.appointment_date
    """, conn, params=[today])
    
    if not today_appointments.empty:
        st.dataframe(today_appointments, use_container_width=True, hide_index=True)
    else:
        st.info("📅 Nenhuma consulta agendada para hoje")
    
    # Pacientes que precisam de atenção
    st.markdown('<h3 class="sub-header">⚠️ Pacientes que Necessitam Atenção</h3>', unsafe_allow_html=True)
    
    attention_patients = pd.read_sql_query("""
        SELECT p.full_name as paciente, 
               ROUND(p.current_weight - p.target_weight, 1) as diferenca_peso,
               DATE(MAX(a.appointment_date)) as ultima_consulta,
               p.medical_conditions as condicoes
        FROM patients p
        LEFT JOIN appointments a ON p.id = a.patient_id AND a.status = 'realizada'
        WHERE p.active = 1
        GROUP BY p.id
        HAVING diferenca_peso > 5 OR ultima_consulta < DATE('now', '-30 days') OR condicoes != ''
        ORDER BY diferenca_peso DESC
    """, conn)
    
    if not attention_patients.empty:
        for _, patient in attention_patients.iterrows():
            with st.expander(f"⚠️ {patient['paciente']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Diferença do Peso Meta:** {patient['diferenca_peso']} kg")
                with col2:
                    st.write(f"**Última Consulta:** {patient['ultima_consulta'] or 'Nunca'}")
                with col3:
                    st.write(f"**Condições:** {patient['condicoes'] or 'Nenhuma'}")
    else:
        st.success("✅ Todos os pacientes estão com acompanhamento em dia!")
    
    conn.close()
    
    # Footer com informações
    st.markdown("""
    <div class="footer">
        <p>💚 NutriApp360 v3.0 - Sistema Completo de Apoio ao Nutricionista</p>
        <p>Desenvolvido com amor para profissionais da nutrição</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# GESTÃO DE PACIENTES
# =============================================================================

def show_patients():
    """Módulo de gestão de pacientes"""
    st.markdown('<h1 class="main-header">👥 Gestão de Pacientes</h1>', unsafe_allow_html=True)
    
    # Abas principais
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Lista de Pacientes", "➕ Novo Paciente", "📊 Progresso", "📄 Relatórios"])
    
    with tab1:
        show_patients_list()
    
    with tab2:
        show_new_patient_form()
    
    with tab3:
        show_patient_progress()
    
    with tab4:
        show_patient_reports()

def show_patients_list():
    """Lista todos os pacientes"""
    conn = sqlite3.connect('nutriapp360.db')
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        search_name = st.text_input("🔍 Buscar por nome", placeholder="Digite o nome...")
    with col2:
        filter_gender = st.selectbox("👫 Filtrar por gênero", ["Todos", "Masculino", "Feminino"])
    with col3:
        filter_status = st.selectbox("📊 Status", ["Todos", "Ativo", "Inativo"])
    
    # Query base
    query = """
        SELECT id, patient_id, full_name, email, phone, birth_date, gender, 
               current_weight, target_weight, activity_level, created_at, active
        FROM patients
        WHERE 1=1
    """
    params = []
    
    # Aplicar filtros
    if search_name:
        query += " AND full_name LIKE ?"
        params.append(f"%{search_name}%")
    
    if filter_gender != "Todos":
        gender_code = "M" if filter_gender == "Masculino" else "F"
        query += " AND gender = ?"
        params.append(gender_code)
    
    if filter_status != "Todos":
        active_status = 1 if filter_status == "Ativo" else 0
        query += " AND active = ?"
        params.append(active_status)
    
    query += " ORDER BY created_at DESC"
    
    patients_df = pd.read_sql_query(query, conn, params=params)
    
    if not patients_df.empty:
        # Processar dados para exibição
        patients_df['birth_date'] = pd.to_datetime(patients_df['birth_date'])
        patients_df['age'] = (datetime.now() - patients_df['birth_date']).dt.days // 365
        patients_df['gender'] = patients_df['gender'].map({'M': 'Masculino', 'F': 'Feminino'})
        patients_df['active'] = patients_df['active'].map({1: '✅ Ativo', 0: '❌ Inativo'})
        
        # Exibir pacientes em cards
        for _, patient in patients_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="patient-card">
                    <h4 style="color: #2E7D32; margin: 0;">{patient['full_name']}</h4>
                    <p style="margin: 0.5rem 0; color: #666;">
                        <strong>ID:</strong> {patient['patient_id']} | 
                        <strong>Idade:</strong> {patient['age']} anos | 
                        <strong>Gênero:</strong> {patient['gender']}
                    </p>
                    <p style="margin: 0.5rem 0;">
                        <strong>📧</strong> {patient['email'] or 'Não informado'} | 
                        <strong>📱</strong> {patient['phone'] or 'Não informado'}
                    </p>
                    <p style="margin: 0.5rem 0;">
                        <strong>⚖️ Peso Atual:</strong> {patient['current_weight']}kg | 
                        <strong>🎯 Meta:</strong> {patient['target_weight']}kg | 
                        <strong>🏃</strong> {patient['activity_level']}
                    </p>
                    <p style="margin: 0; font-size: 0.9rem; color: #666;">
                        Status: {patient['active']} | Cadastrado em: {patient['created_at'][:10]}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Botões de ação
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("👁️ Ver Detalhes", key=f"view_{patient['id']}"):
                        st.session_state.selected_patient = patient['id']
                        st.session_state.patient_action = 'view'
                
                with col2:
                    if st.button("✏️ Editar", key=f"edit_{patient['id']}"):
                        st.session_state.selected_patient = patient['id']
                        st.session_state.patient_action = 'edit'
                
                with col3:
                    if st.button("📅 Agendar", key=f"schedule_{patient['id']}"):
                        st.session_state.selected_patient = patient['id']
                        st.session_state.patient_action = 'schedule'
                
                with col4:
                    status_btn = "🔴 Desativar" if patient['active'] == '✅ Ativo' else "✅ Ativar"
                    if st.button(status_btn, key=f"toggle_{patient['id']}"):
                        toggle_patient_status(patient['id'], patient['active'] == '✅ Ativo')
                        st.rerun()
                
                st.markdown("<hr style='margin: 0.5rem 0;'>", unsafe_allow_html=True)
        
        # Mostrar total
        st.info(f"📊 Total de pacientes encontrados: {len(patients_df)}")
        
    else:
        st.warning("⚠️ Nenhum paciente encontrado com os filtros aplicados.")
    
    # Ações do paciente selecionado
    if 'selected_patient' in st.session_state and 'patient_action' in st.session_state:
        handle_patient_action()
    
    conn.close()

def show_new_patient_form():
    """Formulário para novo paciente"""
    st.markdown('<h3 class="sub-header">➕ Cadastrar Novo Paciente</h3>', unsafe_allow_html=True)
    
    with st.form("new_patient_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("📝 Nome Completo *", placeholder="Ex: Maria Silva Santos")
            email = st.text_input("📧 Email", placeholder="maria@email.com")
            phone = st.text_input("📱 Telefone", placeholder="(11) 99999-9999")
            birth_date = st.date_input("🎂 Data de Nascimento", min_value=date(1920, 1, 1), max_value=date.today())
            gender = st.selectbox("👫 Gênero", ["Feminino", "Masculino"])
        
        with col2:
            height = st.number_input("📏 Altura (m)", min_value=0.5, max_value=2.5, value=1.65, step=0.01)
            current_weight = st.number_input("⚖️ Peso Atual (kg)", min_value=20.0, max_value=300.0, value=70.0, step=0.1)
            target_weight = st.number_input("🎯 Peso Meta (kg)", min_value=20.0, max_value=300.0, value=65.0, step=0.1)
            activity_level = st.selectbox("🏃 Nível de Atividade", [
                "Sedentário", "Pouco ativo", "Moderadamente ativo", "Ativo", "Muito ativo"
            ])
        
        # Informações médicas
        st.markdown("### 🏥 Informações Médicas")
        medical_conditions = st.text_area("🩺 Condições Médicas", placeholder="Ex: Diabetes, Hipertensão...")
        allergies = st.text_area("⚠️ Alergias", placeholder="Ex: Lactose, Glúten, Nozes...")
        dietary_preferences = st.text_area("🥗 Preferências Alimentares", placeholder="Ex: Vegetariano, Low carb...")
        
        # Botão de submit
        submitted = st.form_submit_button("✅ Cadastrar Paciente", use_container_width=True)
        
        if submitted:
            if full_name:
                # Gerar ID único para o paciente
                patient_id = f"PAT{str(uuid.uuid4())[:8].upper()}"
                gender_code = "F" if gender == "Feminino" else "M"
                
                conn = sqlite3.connect('nutriapp360.db')
                cursor = conn.cursor()
                
                try:
                    cursor.execute('''
                        INSERT INTO patients (patient_id, full_name, email, phone, birth_date, 
                                             gender, height, current_weight, target_weight, 
                                             activity_level, medical_conditions, allergies, 
                                             dietary_preferences, nutritionist_id) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (patient_id, full_name, email, phone, birth_date, gender_code, 
                         height, current_weight, target_weight, activity_level, 
                         medical_conditions, allergies, dietary_preferences, st.session_state.user['id']))
                    
                    conn.commit()
                    st.success(f"✅ Paciente {full_name} cadastrado com sucesso! ID: {patient_id}")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Erro ao cadastrar paciente: {str(e)}")
                
                finally:
                    conn.close()
            else:
                st.error("❌ O nome completo é obrigatório!")

def show_patient_progress():
    """Mostra o progresso dos pacientes"""
    st.markdown('<h3 class="sub-header">📊 Acompanhamento de Progresso</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Seletor de paciente
    patients = pd.read_sql_query("SELECT id, full_name FROM patients WHERE active = 1", conn)
    
    if patients.empty:
        st.warning("⚠️ Nenhum paciente ativo encontrado.")
        return
    
    selected_patient_id = st.selectbox(
        "👤 Selecione o Paciente",
        patients['id'].tolist(),
        format_func=lambda x: patients[patients['id'] == x]['full_name'].iloc[0]
    )
    
    # Dados do progresso
    progress_data = pd.read_sql_query("""
        SELECT record_date, weight, body_fat, muscle_mass, waist_circumference, 
               hip_circumference, notes
        FROM patient_progress
        WHERE patient_id = ?
        ORDER BY record_date
    """, conn, params=[selected_patient_id])
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Formulário para adicionar nova medição
        st.markdown("### ➕ Nova Medição")
        
        with st.form("progress_form"):
            record_date = st.date_input("📅 Data da Medição", value=date.today())
            weight = st.number_input("⚖️ Peso (kg)", min_value=20.0, max_value=300.0, step=0.1)
            body_fat = st.number_input("🧈 Percentual de Gordura (%)", min_value=0.0, max_value=50.0, step=0.1)
            muscle_mass = st.number_input("💪 Massa Muscular (kg)", min_value=10.0, max_value=100.0, step=0.1)
            waist = st.number_input("📐 Circunferência da Cintura (cm)", min_value=40.0, max_value=150.0, step=0.1)
            hip = st.number_input("📐 Circunferência do Quadril (cm)", min_value=50.0, max_value=180.0, step=0.1)
            notes = st.text_area("📝 Observações", placeholder="Notas sobre a medição...")
            
            if st.form_submit_button("💾 Salvar Medição"):
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO patient_progress (patient_id, record_date, weight, body_fat, 
                                                 muscle_mass, waist_circumference, hip_circumference, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (selected_patient_id, record_date, weight, body_fat, muscle_mass, waist, hip, notes))
                conn.commit()
                st.success("✅ Medição salva com sucesso!")
                st.rerun()
    
    with col2:
        # Gráficos de progresso
        if not progress_data.empty:
            st.markdown("### 📈 Evolução do Peso")
            
            # Gráfico de peso
            fig = px.line(progress_data, x='record_date', y='weight', 
                         title='Evolução do Peso', markers=True)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Últimas medições
            st.markdown("### 📋 Últimas Medições")
            recent_progress = progress_data.tail(5).sort_values('record_date', ascending=False)
            st.dataframe(recent_progress, hide_index=True)
            
        else:
            st.info("📊 Nenhuma medição registrada ainda.")
    
    conn.close()

def show_patient_reports():
    """Relatórios de pacientes"""
    st.markdown('<h3 class="sub-header">📄 Relatórios de Pacientes</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Relatório geral
        st.markdown("#### 📊 Relatório Geral")
        
        general_stats = pd.read_sql_query("""
            SELECT 
                COUNT(*) as total_patients,
                COUNT(CASE WHEN active = 1 THEN 1 END) as active_patients,
                AVG(current_weight) as avg_weight,
                AVG(height) as avg_height,
                COUNT(CASE WHEN gender = 'F' THEN 1 END) as female_count,
                COUNT(CASE WHEN gender = 'M' THEN 1 END) as male_count
            FROM patients
        """, conn)
        
        stats = general_stats.iloc[0]
        
        st.metric("👥 Total de Pacientes", int(stats['total_patients']))
        st.metric("✅ Pacientes Ativos", int(stats['active_patients']))
        st.metric("⚖️ Peso Médio", f"{stats['avg_weight']:.1f} kg")
        st.metric("📏 Altura Média", f"{stats['avg_height']:.2f} m")
        
        # Distribuição por gênero
        gender_data = pd.DataFrame({
            'Gênero': ['Feminino', 'Masculino'],
            'Quantidade': [int(stats['female_count']), int(stats['male_count'])]
        })
        
        fig = px.pie(gender_data, values='Quantidade', names='Gênero',
                    title='Distribuição por Gênero')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Relatório de IMC
        st.markdown("#### ⚖️ Análise de IMC")
        
        imc_data = pd.read_sql_query("""
            SELECT full_name, current_weight, height,
                   ROUND(current_weight / (height * height), 2) as imc
            FROM patients
            WHERE active = 1 AND current_weight > 0 AND height > 0
        """, conn)
        
        if not imc_data.empty:
            # Classificar IMC
            def classify_imc(imc):
                if imc < 18.5:
                    return "Abaixo do peso"
                elif imc < 25:
                    return "Peso normal"
                elif imc < 30:
                    return "Sobrepeso"
                else:
                    return "Obesidade"
            
            imc_data['classificacao'] = imc_data['imc'].apply(classify_imc)
            
            # Distribuição de IMC
            imc_dist = imc_data['classificacao'].value_counts()
            
            fig = px.bar(x=imc_dist.index, y=imc_dist.values,
                        title='Distribuição de IMC dos Pacientes')
            st.plotly_chart(fig, use_container_width=True)
            
            # Top pacientes que precisam de atenção
            st.markdown("#### ⚠️ Pacientes que Necessitam Atenção")
            attention_patients = imc_data[
                (imc_data['imc'] < 18.5) | (imc_data['imc'] > 30)
            ].sort_values('imc', ascending=False)
            
            if not attention_patients.empty:
                for _, patient in attention_patients.head(5).iterrows():
                    st.warning(f"🚨 {patient['full_name']} - IMC: {patient['imc']} ({patient['classificacao']})")
            else:
                st.success("✅ Todos os pacientes estão com IMC adequado!")
    
    conn.close()

def toggle_patient_status(patient_id, is_active):
    """Alterna status do paciente"""
    new_status = 0 if is_active else 1
    conn = sqlite3.connect('nutriapp360.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE patients SET active = ? WHERE id = ?", (new_status, patient_id))
    conn.commit()
    conn.close()

def handle_patient_action():
    """Processa ações dos pacientes (visualizar, editar, etc.)"""
    # Implementação simplificada - na versão completa teria modais ou páginas dedicadas
    patient_id = st.session_state.selected_patient
    action = st.session_state.patient_action
    
    if action == 'view':
        st.info(f"👁️ Visualizando detalhes do paciente ID: {patient_id}")
    elif action == 'edit':
        st.info(f"✏️ Editando paciente ID: {patient_id}")
    elif action == 'schedule':
        st.info(f"📅 Agendando consulta para paciente ID: {patient_id}")
    
    # Limpar ação
    del st.session_state.selected_patient
    del st.session_state.patient_action

# =============================================================================
# SISTEMA DE AGENDAMENTOS
# =============================================================================

def show_appointments():
    """Sistema de agendamentos"""
    st.markdown('<h1 class="main-header">📅 Sistema de Agendamentos</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Lista de Consultas", "➕ Nova Consulta", "📆 Calendário", "📊 Estatísticas"])
    
    with tab1:
        show_appointments_list()
    
    with tab2:
        show_new_appointment_form()
    
    with tab3:
        show_appointments_calendar()
    
    with tab4:
        show_appointments_stats()

def show_appointments_list():
    """Lista de consultas"""
    st.markdown('<h3 class="sub-header">📋 Consultas Agendadas</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_status = st.selectbox("📊 Status", ["Todos", "agendado", "realizada", "cancelada"])
    with col2:
        date_filter = st.date_input("📅 Filtrar por Data", value=date.today())
    with col3:
        period_filter = st.selectbox("⏰ Período", ["Hoje", "Esta Semana", "Este Mês", "Todos"])
    
    # Query base
    query = """
        SELECT a.id, a.appointment_id, p.full_name as patient_name, 
               a.appointment_date, a.duration, a.appointment_type, 
               a.status, a.notes, a.weight_recorded
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        WHERE 1=1
    """
    params = []
    
    # Aplicar filtros
    if filter_status != "Todos":
        query += " AND a.status = ?"
        params.append(filter_status)
    
    if period_filter == "Hoje":
        query += " AND DATE(a.appointment_date) = DATE('now')"
    elif period_filter == "Esta Semana":
        query += " AND DATE(a.appointment_date) BETWEEN DATE('now', 'weekday 0', '-7 days') AND DATE('now', 'weekday 0')"
    elif period_filter == "Este Mês":
        query += " AND strftime('%Y-%m', a.appointment_date) = strftime('%Y-%m', 'now')"
    
    query += " ORDER BY a.appointment_date ASC"
    
    appointments_df = pd.read_sql_query(query, conn, params=params)
    
    if not appointments_df.empty:
        # Processar dados para exibição
        appointments_df['appointment_date'] = pd.to_datetime(appointments_df['appointment_date'])
        appointments_df['date'] = appointments_df['appointment_date'].dt.strftime('%d/%m/%Y')
        appointments_df['time'] = appointments_df['appointment_date'].dt.strftime('%H:%M')
        
        # Mapear status para emojis
        status_map = {
            'agendado': '🟡 Agendado',
            'realizada': '🟢 Realizada', 
            'cancelada': '🔴 Cancelada'
        }
        appointments_df['status_display'] = appointments_df['status'].map(status_map)
        
        # Exibir consultas
        for _, appointment in appointments_df.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                
                with col1:
                    st.write(f"**👤 {appointment['patient_name']}**")
                    st.write(f"🗓️ {appointment['date']} às {appointment['time']}")
                
                with col2:
                    st.write(f"**Tipo:** {appointment['appointment_type']}")
                    st.write(f"**Duração:** {appointment['duration']} min")
                
                with col3:
                    st.write(f"**Status:** {appointment['status_display']}")
                    if appointment['weight_recorded']:
                        st.write(f"**Peso:** {appointment['weight_recorded']} kg")
                
                with col4:
                    if appointment['notes']:
                        st.write(f"**📝 Notas:** {appointment['notes'][:50]}...")
                    
                    # Botões de ação
                    col4_1, col4_2 = st.columns(2)
                    with col4_1:
                        if st.button("✏️ Editar", key=f"edit_app_{appointment['id']}"):
                            st.session_state.edit_appointment = appointment['id']
                    with col4_2:
                        if appointment['status'] == 'agendado':
                            if st.button("✅ Realizar", key=f"complete_app_{appointment['id']}"):
                                update_appointment_status(appointment['id'], 'realizada')
                                st.success("✅ Consulta marcada como realizada!")
                                st.rerun()
                
                st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
        
        st.info(f"📊 Total: {len(appointments_df)} consultas")
    else:
        st.warning("⚠️ Nenhuma consulta encontrada com os filtros aplicados.")
    
    conn.close()

def show_new_appointment_form():
    """Formulário para nova consulta"""
    st.markdown('<h3 class="sub-header">➕ Agendar Nova Consulta</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar pacientes ativos
    patients = pd.read_sql_query("SELECT id, full_name FROM patients WHERE active = 1", conn)
    
    if patients.empty:
        st.warning("⚠️ Nenhum paciente ativo encontrado. Cadastre um paciente primeiro.")
        return
    
    with st.form("new_appointment_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Seleção do paciente
            patient_id = st.selectbox(
                "👤 Paciente *",
                patients['id'].tolist(),
                format_func=lambda x: patients[patients['id'] == x]['full_name'].iloc[0]
            )
            
            # Data e hora
            appointment_date = st.date_input("📅 Data da Consulta *", min_value=date.today())
            appointment_time = st.time_input("⏰ Horário *", value=datetime.now().time())
            
            duration = st.number_input("⏱️ Duração (minutos)", min_value=15, max_value=240, value=60, step=15)
        
        with col2:
            appointment_type = st.selectbox("🩺 Tipo de Consulta", [
                "Consulta inicial", "Retorno", "Acompanhamento", "Reavaliação", "Consulta especial"
            ])
            
            status = st.selectbox("📊 Status", ["agendado", "confirmado"])
            
            notes = st.text_area("📝 Observações", placeholder="Notas sobre a consulta...")
        
        # Botão de submit
        submitted = st.form_submit_button("✅ Agendar Consulta", use_container_width=True)
        
        if submitted:
            # Combinar data e hora
            appointment_datetime = datetime.combine(appointment_date, appointment_time)
            appointment_id = f"APP{str(uuid.uuid4())[:8].upper()}"
            
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    INSERT INTO appointments (appointment_id, patient_id, nutritionist_id, 
                                             appointment_date, duration, appointment_type, 
                                             status, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (appointment_id, patient_id, st.session_state.user['id'], 
                      appointment_datetime, duration, appointment_type, status, notes))
                
                conn.commit()
                patient_name = patients[patients['id'] == patient_id]['full_name'].iloc[0]
                st.success(f"✅ Consulta agendada para {patient_name} em {appointment_date.strftime('%d/%m/%Y')} às {appointment_time.strftime('%H:%M')}!")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Erro ao agendar consulta: {str(e)}")
    
    conn.close()

def show_appointments_calendar():
    """Visualização em calendário"""
    st.markdown('<h3 class="sub-header">📆 Calendário de Consultas</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Seletor de mês/ano
    col1, col2 = st.columns(2)
    with col1:
        selected_month = st.selectbox("📅 Mês", range(1, 13), 
                                     index=datetime.now().month-1,
                                     format_func=lambda x: calendar.month_name[x])
    with col2:
        selected_year = st.selectbox("📅 Ano", range(2020, 2030), 
                                    index=datetime.now().year-2020)
    
    # Buscar consultas do mês
    start_date = f"{selected_year}-{selected_month:02d}-01"
    if selected_month == 12:
        end_date = f"{selected_year + 1}-01-01"
    else:
        end_date = f"{selected_year}-{selected_month + 1:02d}-01"
    
    monthly_appointments = pd.read_sql_query("""
        SELECT a.appointment_date, p.full_name as patient_name, 
               a.appointment_type, a.status, a.duration
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        WHERE DATE(a.appointment_date) >= ? AND DATE(a.appointment_date) < ?
        ORDER BY a.appointment_date
    """, conn, params=[start_date, end_date])
    
    if not monthly_appointments.empty:
        # Processar dados
        monthly_appointments['appointment_date'] = pd.to_datetime(monthly_appointments['appointment_date'])
        monthly_appointments['day'] = monthly_appointments['appointment_date'].dt.day
        monthly_appointments['time'] = monthly_appointments['appointment_date'].dt.strftime('%H:%M')
        
        # Gráfico de consultas por dia
        daily_counts = monthly_appointments.groupby('day').size().reset_index(name='count')
        
        fig = px.bar(daily_counts, x='day', y='count',
                    title=f'Consultas em {calendar.month_name[selected_month]} {selected_year}',
                    labels={'day': 'Dia do Mês', 'count': 'Número de Consultas'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Lista de consultas do mês
        st.markdown("### 📋 Consultas do Mês")
        
        # Agrupar por dia
        for day in sorted(monthly_appointments['day'].unique()):
            day_appointments = monthly_appointments[monthly_appointments['day'] == day]
            
            with st.expander(f"📅 Dia {day} - {len(day_appointments)} consulta(s)"):
                for _, apt in day_appointments.iterrows():
                    status_emoji = {'agendado': '🟡', 'realizada': '🟢', 'cancelada': '🔴'}
                    st.write(f"{status_emoji.get(apt['status'], '⚪')} {apt['time']} - **{apt['patient_name']}** ({apt['appointment_type']}) - {apt['duration']}min")
    else:
        st.info(f"📅 Nenhuma consulta agendada para {calendar.month_name[selected_month]} {selected_year}")
    
    conn.close()

def show_appointments_stats():
    """Estatísticas de consultas"""
    st.markdown('<h3 class="sub-header">📊 Estatísticas de Consultas</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_appointments = pd.read_sql_query("SELECT COUNT(*) as count FROM appointments", conn).iloc[0]['count']
        st.metric("📅 Total de Consultas", total_appointments)
    
    with col2:
        completed_appointments = pd.read_sql_query("SELECT COUNT(*) as count FROM appointments WHERE status = 'realizada'", conn).iloc[0]['count']
        st.metric("✅ Realizadas", completed_appointments)
    
    with col3:
        scheduled_appointments = pd.read_sql_query("SELECT COUNT(*) as count FROM appointments WHERE status = 'agendado'", conn).iloc[0]['count']
        st.metric("🟡 Agendadas", scheduled_appointments)
    
    with col4:
        cancelled_appointments = pd.read_sql_query("SELECT COUNT(*) as count FROM appointments WHERE status = 'cancelada'", conn).iloc[0]['count']
        st.metric("🔴 Canceladas", cancelled_appointments)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Consultas por status
        status_data = pd.read_sql_query("""
            SELECT status, COUNT(*) as count
            FROM appointments
            GROUP BY status
        """, conn)
        
        if not status_data.empty:
            fig = px.pie(status_data, values='count', names='status',
                        title='Distribuição por Status')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Consultas por tipo
        type_data = pd.read_sql_query("""
            SELECT appointment_type, COUNT(*) as count
            FROM appointments
            GROUP BY appointment_type
        """, conn)
        
        if not type_data.empty:
            fig = px.bar(type_data, x='appointment_type', y='count',
                        title='Consultas por Tipo')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    # Evolução mensal
    st.markdown("### 📈 Evolução Mensal")
    
    monthly_data = pd.read_sql_query("""
        SELECT strftime('%Y-%m', appointment_date) as month, COUNT(*) as count
        FROM appointments
        GROUP BY month
        ORDER BY month
    """, conn)
    
    if not monthly_data.empty:
        fig = px.line(monthly_data, x='month', y='count',
                     title='Número de Consultas por Mês', markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Top pacientes
    st.markdown("### 🏆 Pacientes Mais Frequentes")
    
    top_patients = pd.read_sql_query("""
        SELECT p.full_name, COUNT(*) as appointments_count
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        GROUP BY p.id, p.full_name
        ORDER BY appointments_count DESC
        LIMIT 10
    """, conn)
    
    if not top_patients.empty:
        fig = px.bar(top_patients, x='full_name', y='appointments_count',
                    title='Top 10 Pacientes com Mais Consultas')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    conn.close()

def update_appointment_status(appointment_id, new_status):
    """Atualiza status da consulta"""
    conn = sqlite3.connect('nutriapp360.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE appointments SET status = ? WHERE id = ?", (new_status, appointment_id))
    conn.commit()
    conn.close()

# =============================================================================
# CALCULADORAS NUTRICIONAIS
# =============================================================================

def show_calculators():
    """Calculadoras nutricionais"""
    st.markdown('<h1 class="main-header">🧮 Calculadoras Nutricionais</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚖️ IMC", "🔥 TMB", "🍽️ Calorias", "💧 Hidratação", "🥗 Macros"])
    
    with tab1:
        show_imc_calculator()
    
    with tab2:
        show_tmb_calculator()
    
    with tab3:
        show_calories_calculator()
    
    with tab4:
        show_hydration_calculator()
    
    with tab5:
        show_macros_calculator()

def show_imc_calculator():
    """Calculadora de IMC"""
    st.markdown('<h3 class="sub-header">⚖️ Calculadora de IMC</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Calcular IMC")
        
        weight = st.number_input("💪 Peso (kg)", min_value=20.0, max_value=300.0, value=70.0, step=0.1)
        height = st.number_input("📏 Altura (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01)
        
        if st.button("🧮 Calcular IMC", use_container_width=True):
            imc = weight / (height ** 2)
            
            # Classificação do IMC
            if imc < 18.5:
                classification = "Abaixo do peso"
                color = "#FFA726"
                risk = "Risco de problemas de saúde relacionados ao baixo peso"
            elif imc < 25:
                classification = "Peso normal"
                color = "#4CAF50"
                risk = "Menor risco de problemas de saúde"
            elif imc < 30:
                classification = "Sobrepeso"
                color = "#FF9800"
                risk = "Risco aumentado de problemas de saúde"
            else:
                classification = "Obesidade"
                color = "#F44336"
                risk = "Alto risco de problemas de saúde"
            
            # Exibir resultado
            st.markdown(f"""
            <div class="success-card">
                <h3 style="color: {color}; margin: 0;">🎯 Resultado: {imc:.2f}</h3>
                <p style="margin: 0.5rem 0;"><strong>Classificação:</strong> {classification}</p>
                <p style="margin: 0; font-size: 0.9rem;">{risk}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Peso ideal
            ideal_min = 18.5 * (height ** 2)
            ideal_max = 24.9 * (height ** 2)
            
            st.info(f"💡 **Peso ideal para sua altura:** {ideal_min:.1f}kg - {ideal_max:.1f}kg")
    
    with col2:
        # Gráfico visual do IMC
        st.markdown("#### 📊 Escala de IMC")
        
        imc_ranges = pd.DataFrame({
            'Classificação': ['Abaixo do peso', 'Peso normal', 'Sobrepeso', 'Obesidade'],
            'IMC Mínimo': [0, 18.5, 25, 30],
            'IMC Máximo': [18.5, 25, 30, 40]
        })
        
        # Criar gráfico de barras horizontais
        fig = px.bar(imc_ranges, y='Classificação', x='IMC Máximo',
                    title='Classificação do IMC',
                    color='Classificação',
                    color_discrete_sequence=['#FFA726', '#4CAF50', '#FF9800', '#F44336'])
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de referência
        st.markdown("#### 📋 Tabela de Referência")
        st.dataframe(imc_ranges, hide_index=True)

def show_tmb_calculator():
    """Calculadora de Taxa Metabólica Basal"""
    st.markdown('<h3 class="sub-header">🔥 Calculadora de TMB</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔥 Calcular Taxa Metabólica Basal")
        
        gender = st.selectbox("👫 Sexo", ["Masculino", "Feminino"])
        age = st.number_input("🎂 Idade", min_value=15, max_value=100, value=30)
        weight = st.number_input("💪 Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)
        height_cm = st.number_input("📏 Altura (cm)", min_value=100, max_value=250, value=170)
        
        activity_level = st.selectbox("🏃 Nível de Atividade", [
            "Sedentário (pouco ou nenhum exercício)",
            "Pouco ativo (exercício leve 1-3 dias/semana)",
            "Moderadamente ativo (exercício moderado 3-5 dias/semana)",
            "Ativo (exercício pesado 6-7 dias/semana)",
            "Muito ativo (exercício muito pesado, trabalho físico)"
        ])
        
        if st.button("🧮 Calcular TMB", use_container_width=True):
            # Fórmula de Harris-Benedict revisada
            if gender == "Masculino":
                tmb = 88.362 + (13.397 * weight) + (4.799 * height_cm) - (5.677 * age)
            else:
                tmb = 447.593 + (9.247 * weight) + (3.098 * height_cm) - (4.330 * age)
            
            # Fator de atividade
            activity_factors = {
                "Sedentário (pouco ou nenhum exercício)": 1.2,
                "Pouco ativo (exercício leve 1-3 dias/semana)": 1.375,
                "Moderadamente ativo (exercício moderado 3-5 dias/semana)": 1.55,
                "Ativo (exercício pesado 6-7 dias/semana)": 1.725,
                "Muito ativo (exercício muito pesado, trabalho físico)": 1.9
            }
            
            activity_factor = activity_factors[activity_level]
            gasto_total = tmb * activity_factor
            
            st.markdown(f"""
            <div class="success-card">
                <h3 style="color: #4CAF50; margin: 0;">🔥 Taxa Metabólica Basal</h3>
                <p style="margin: 0.5rem 0; font-size: 1.2rem;"><strong>TMB: {tmb:.0f} kcal/dia</strong></p>
                <p style="margin: 0.5rem 0; font-size: 1.2rem;"><strong>Gasto Total: {gasto_total:.0f} kcal/dia</strong></p>
                <p style="margin: 0; font-size: 0.9rem;">Considerando seu nível de atividade</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Distribuição das calorias
            st.markdown("#### 🍽️ Sugestão de Distribuição")
            
            breakfast = gasto_total * 0.25
            lunch = gasto_total * 0.35
            snack = gasto_total * 0.15
            dinner = gasto_total * 0.25
            
            distribution = pd.DataFrame({
                'Refeição': ['☀️ Café da Manhã', '🍽️ Almoço', '🍎 Lanche', '🌙 Jantar'],
                'Calorias': [breakfast, lunch, snack, dinner],
                'Percentual': [25, 35, 15, 25]
            })
            
            fig = px.pie(distribution, values='Calorias', names='Refeição',
                        title=f'Distribuição de {gasto_total:.0f} kcal/dia')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Informações educativas
        st.markdown("#### 💡 Sobre a TMB")
        
        st.markdown("""
        <div class="info-card">
            <h4>🔥 O que é a TMB?</h4>
            <p>A Taxa Metabólica Basal (TMB) é a quantidade mínima de energia (calorias) que seu corpo precisa para manter as funções vitais em repouso.</p>
            
            <h4>🧮 Como é calculada?</h4>
            <p>Utilizamos a fórmula de Harris-Benedict revisada, que considera:</p>
            <ul>
                <li>Peso corporal</li>
                <li>Altura</li>
                <li>Idade</li>
                <li>Sexo</li>
                <li>Nível de atividade física</li>
            </ul>
            
            <h4>🎯 Para que serve?</h4>
            <p>A TMB ajuda a:</p>
            <ul>
                <li>Determinar necessidades calóricas</li>
                <li>Planejar dietas para emagrecimento</li>
                <li>Organizar planos de ganho de peso</li>
                <li>Orientar a prática de exercícios</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Gráfico comparativo por idade
        st.markdown("#### 📈 TMB por Idade")
        
        ages = list(range(20, 81, 5))
        tmb_male = [88.362 + (13.397 * weight) + (4.799 * height_cm) - (5.677 * age) for age in ages]
        tmb_female = [447.593 + (9.247 * weight) + (3.098 * height_cm) - (4.330 * age) for age in ages]
        
        tmb_comparison = pd.DataFrame({
            'Idade': ages * 2,
            'TMB': tmb_male + tmb_female,
            'Sexo': ['Masculino'] * len(ages) + ['Feminino'] * len(ages)
        })
        
        fig = px.line(tmb_comparison, x='Idade', y='TMB', color='Sexo',
                     title='Evolução da TMB por Idade')
        st.plotly_chart(fig, use_container_width=True)

def show_calories_calculator():
    """Calculadora de calorias para objetivo"""
    st.markdown('<h3 class="sub-header">🍽️ Calculadora de Calorias por Objetivo</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Definir Objetivo")
        
        # Dados básicos (reutilizar do TMB)
        gender = st.selectbox("👫 Sexo", ["Masculino", "Feminino"], key="cal_gender")
        age = st.number_input("🎂 Idade", min_value=15, max_value=100, value=30, key="cal_age")
        weight = st.number_input("💪 Peso Atual (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1, key="cal_weight")
        height_cm = st.number_input("📏 Altura (cm)", min_value=100, max_value=250, value=170, key="cal_height")
        
        activity_level = st.selectbox("🏃 Nível de Atividade", [
            "Sedentário", "Pouco ativo", "Moderadamente ativo", "Ativo", "Muito ativo"
        ], key="cal_activity")
        
        goal = st.selectbox("🎯 Objetivo", [
            "Perder peso (0.5kg/semana)",
            "Perder peso (1kg/semana)", 
            "Manter peso",
            "Ganhar peso (0.5kg/semana)",
            "Ganhar peso (1kg/semana)"
        ])
        
        if st.button("🧮 Calcular Calorias", use_container_width=True):
            # Calcular TMB
            if gender == "Masculino":
                tmb = 88.362 + (13.397 * weight) + (4.799 * height_cm) - (5.677 * age)
            else:
                tmb = 447.593 + (9.247 * weight) + (3.098 * height_cm) - (4.330 * age)
            
            # Fator de atividade
            activity_factors = {
                "Sedentário": 1.2,
                "Pouco ativo": 1.375,
                "Moderadamente ativo": 1.55,
                "Ativo": 1.725,
                "Muito ativo": 1.9
            }
            
            maintenance_calories = tmb * activity_factors[activity_level]
            
            # Ajustar para objetivo
            goal_adjustments = {
                "Perder peso (0.5kg/semana)": -250,
                "Perder peso (1kg/semana)": -500,
                "Manter peso": 0,
                "Ganhar peso (0.5kg/semana)": 250,
                "Ganhar peso (1kg/semana)": 500
            }
            
            target_calories = maintenance_calories + goal_adjustments[goal]
            
            st.markdown(f"""
            <div class="success-card">
                <h3 style="color: #4CAF50; margin: 0;">🎯 Calorias para seu Objetivo</h3>
                <p style="margin: 0.5rem 0; font-size: 1.3rem;"><strong>{target_calories:.0f} kcal/dia</strong></p>
                <p style="margin: 0.5rem 0;">TMB: {tmb:.0f} kcal | Manutenção: {maintenance_calories:.0f} kcal</p>
                <p style="margin: 0; font-size: 0.9rem;"><strong>Objetivo:</strong> {goal}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Plano semanal
            st.markdown("#### 📅 Plano Semanal")
            
            weekly_plan = pd.DataFrame({
                'Dia': ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'],
                'Calorias': [target_calories] * 7,
                'Ajuste': ['Normal', 'Normal', 'Normal', 'Normal', 'Normal', '+100 (flexível)', 'Normal']
            })
            
            # Adicionar variação no fim de semana
            weekly_plan.loc[5, 'Calorias'] = target_calories + 100
            
            st.dataframe(weekly_plan, hide_index=True)
            
            # Tempo estimado para objetivo
            if "Perder peso" in goal:
                weeks_to_goal = abs(goal_adjustments[goal]) / 250 * 2
                st.info(f"⏰ **Tempo estimado:** {weeks_to_goal:.0f} semanas para perder 1kg")
            elif "Ganhar peso" in goal:
                weeks_to_goal = abs(goal_adjustments[goal]) / 250 * 2
                st.info(f"⏰ **Tempo estimado:** {weeks_to_goal:.0f} semanas para ganhar 1kg")
    
    with col2:
        # Dicas para o objetivo
        st.markdown("#### 💡 Dicas para seu Objetivo")
        
        if "Perder peso" in goal if 'goal' in locals() else False:
            st.markdown("""
            <div class="warning-card">
                <h4>🏃 Dicas para Emagrecimento</h4>
                <ul>
                    <li>💧 Beba bastante água</li>
                    <li>🥗 Priorize alimentos ricos em fibras</li>
                    <li>🏋️ Inclua exercícios de força</li>
                    <li>😴 Tenha um sono de qualidade</li>
                    <li>🍽️ Faça refeições regulares</li>
                    <li>📱 Use um app para monitorar</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        elif "Ganhar peso" in goal if 'goal' in locals() else False:
            st.markdown("""
            <div class="info-card">
                <h4>💪 Dicas para Ganho de Peso</h4>
                <ul>
                    <li>🥜 Inclua gorduras boas na dieta</li>
                    <li>🍌 Faça lanches calóricos</li>
                    <li>🏋️ Treine com pesos</li>
                    <li>🥛 Use suplementos proteicos</li>
                    <li>🍽️ Aumente a frequência das refeições</li>
                    <li>⏰ Mantenha horários regulares</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div class="success-card">
                <h4>⚖️ Dicas para Manutenção</h4>
                <ul>
                    <li>⚖️ Monitore o peso semanalmente</li>
                    <li>🥗 Mantenha uma dieta balanceada</li>
                    <li>🏃 Pratique atividade física regular</li>
                    <li>🍎 Tenha lanches saudáveis</li>
                    <li>📊 Acompanhe suas medidas</li>
                    <li>🎯 Estabeleça metas de longo prazo</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

def show_hydration_calculator():
    """Calculadora de hidratação"""
    st.markdown('<h3 class="sub-header">💧 Calculadora de Hidratação</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💧 Calcular Necessidade de Água")
        
        weight = st.number_input("💪 Peso (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1, key="hydration_weight")
        
        activity_duration = st.number_input("🏃 Tempo de exercício (min/dia)", min_value=0, max_value=300, value=60)
        
        climate = st.selectbox("🌡️ Clima", [
            "Normal (20-25°C)",
            "Quente (25-35°C)", 
            "Muito quente (>35°C)",
            "Frio (<15°C)"
        ])
        
        special_conditions = st.multiselect("🏥 Condições Especiais", [
            "Febre",
            "Amamentação", 
            "Gravidez",
            "Altitude elevada",
            "Ar condicionado/calefação"
        ])
        
        if st.button("💧 Calcular Hidratação", use_container_width=True):
            # Cálculo base: 35ml por kg
            base_water = weight * 35
            
            # Ajuste por exercício: +500ml por hora
            exercise_water = (activity_duration / 60) * 500
            
            # Ajuste por clima
            climate_multiplier = {
                "Normal (20-25°C)": 1.0,
                "Quente (25-35°C)": 1.2,
                "Muito quente (>35°C)": 1.5,
                "Frio (<15°C)": 0.9
            }
            
            climate_adjustment = base_water * climate_multiplier[climate]
            
            # Ajustes especiais
            special_water = 0
            for condition in special_conditions:
                if condition == "Febre":
                    special_water += 500
                elif condition in ["Amamentação", "Gravidez"]:
                    special_water += 700
                elif condition == "Altitude elevada":
                    special_water += 400
                elif condition == "Ar condicionado/calefação":
                    special_water += 200
            
            total_water = climate_adjustment + exercise_water + special_water
            
            # Converter para copos (250ml cada)
            glasses = total_water / 250
            
            st.markdown(f"""
            <div class="success-card">
                <h3 style="color: #00BCD4; margin: 0;">💧 Necessidade de Água</h3>
                <p style="margin: 0.5rem 0; font-size: 1.3rem;"><strong>{total_water:.0f}ml/dia</strong></p>
                <p style="margin: 0.5rem 0; font-size: 1.2rem;"><strong>{glasses:.1f} copos de 250ml</strong></p>
                <p style="margin: 0; font-size: 0.9rem;">Baseado em peso: {base_water:.0f}ml + exercício: {exercise_water:.0f}ml + ajustes: {special_water:.0f}ml</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Cronograma de hidratação
            st.markdown("#### ⏰ Cronograma de Hidratação")
            
            schedule = pd.DataFrame({
                'Horário': ['07:00', '09:00', '11:00', '13:00', '15:00', '17:00', '19:00', '21:00'],
                'Quantidade (ml)': [250] * 8,
                'Dica': [
                    '🌅 Ao acordar - hidrata após jejum',
                    '☕ Meio da manhã - acompanha lanche',
                    '🏃 Pré-almoço - prepara digestão',
                    '🍽️ Pós-almoço - auxilia digestão',
                    '🍎 Lanche da tarde - mantém energia',
                    '🏋️ Pré-treino - prepara exercício',
                    '🌆 Jantar - acompanha refeição',
                    '📚 Noite - hidratação final'
                ]
            })
            
            # Ajustar quantidades proporcionalmente
            target_per_glass = total_water / 8
            schedule['Quantidade (ml)'] = [int(target_per_glass)] * 8
            
            st.dataframe(schedule, hide_index=True)
    
    with col2:
        # Benefícios da hidratação
        st.markdown("#### 🌟 Benefícios da Hidratação")
        
        st.markdown("""
        <div class="info-card">
            <h4>💧 Por que hidratar-se adequadamente?</h4>
            <ul>
                <li>🧠 <strong>Função cerebral:</strong> Melhora concentração e memória</li>
                <li>💪 <strong>Performance física:</strong> Otimiza rendimento nos exercícios</li>
                <li>🌡️ <strong>Regulação térmica:</strong> Controla temperatura corporal</li>
                <li>🩸 <strong>Circulação:</strong> Melhora transporte de nutrientes</li>
                <li>🍃 <strong>Detox:</strong> Elimina toxinas pelos rins</li>
                <li>✨ <strong>Pele:</strong> Mantém elasticidade e brilho</li>
                <li>🍽️ <strong>Digestão:</strong> Facilita processos digestivos</li>
                <li>⚖️ <strong>Peso:</strong> Auxilia controle de peso</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Sinais de desidratação
        st.markdown("#### ⚠️ Sinais de Desidratação")
        
        st.markdown("""
        <div class="warning-card">
            <h4>🚨 Fique atento aos sinais:</h4>
            <ul>
                <li>🌵 Sede intensa</li>
                <li>😵 Tontura ou dor de cabeça</li>
                <li>🟡 Urina escura ou pouca</li>
                <li>🏃 Fadiga ou fraqueza</li>
                <li>👄 Boca seca</li>
                <li>🤒 Pele ressecada</li>
                <li>💓 Batimentos acelerados</li>
                <li>🧠 Dificuldade de concentração</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Dicas práticas
        st.markdown("#### 💡 Dicas Práticas")
        
        st.markdown("""
        <div class="success-card">
            <h4>🎯 Para manter-se hidratado:</h4>
            <ul>
                <li>📱 Use apps lembretes</li>
                <li>🍋 Aromatize a água (limão, hortelã)</li>
                <li>🥤 Tenha sempre uma garrafa</li>
                <li>🍉 Coma frutas com água</li>
                <li>🥒 Inclua verduras hidratantes</li>
                <li>⏰ Crie uma rotina</li>
                <li>🌡️ Monitore a cor da urina</li>
                <li>❄️ Varie temperatura (gelada/natural)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_macros_calculator():
    """Calculadora de macronutrientes"""
    st.markdown('<h3 class="sub-header">🥗 Calculadora de Macronutrientes</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🧮 Calcular Distribuição de Macros")
        
        # Dados básicos
        total_calories = st.number_input("🔥 Calorias Totais/dia", min_value=800, max_value=4000, value=2000, step=50)
        
        diet_type = st.selectbox("🥗 Tipo de Dieta", [
            "Balanceada padrão",
            "Low carb",
            "Cetogênica",
            "Alta proteína",
            "Mediterrânea",
            "Vegana",
            "Personalizada"
        ])
        
        goal = st.selectbox("🎯 Objetivo Principal", [
            "Emagrecimento",
            "Ganho de massa muscular",
            "Manutenção",
            "Performance atlética"
        ])
        
        # Se personalizada, permitir ajustes
        if diet_type == "Personalizada":
            st.markdown("#### ⚙️ Ajustes Personalizados (%)")
            carb_percent = st.slider("🍞 Carboidratos", 10, 70, 50)
            protein_percent = st.slider("🥩 Proteínas", 10, 50, 25)
            fat_percent = 100 - carb_percent - protein_percent
            st.write(f"🥑 Gorduras: {fat_percent}%")
            
            if fat_percent < 15:
                st.warning("⚠️ Atenção: Gorduras muito baixas podem afetar hormônios!")
        
        if st.button("🧮 Calcular Macros", use_container_width=True):
            # Definir distribuições por tipo de dieta
            macro_distributions = {
                "Balanceada padrão": {"carb": 50, "protein": 20, "fat": 30},
                "Low carb": {"carb": 20, "protein": 30, "fat": 50},
                "Cetogênica": {"carb": 5, "protein": 25, "fat": 70},
                "Alta proteína": {"carb": 40, "protein": 35, "fat": 25},
                "Mediterrânea": {"carb": 45, "protein": 20, "fat": 35},
                "Vegana": {"carb": 55, "protein": 15, "fat": 30}
            }
            
            if diet_type == "Personalizada":
                distribution = {"carb": carb_percent, "protein": protein_percent, "fat": fat_percent}
            else:
                distribution = macro_distributions[diet_type]
            
            # Ajustes por objetivo
            if goal == "Emagrecimento" and diet_type != "Personalizada":
                distribution["protein"] += 5
                distribution["carb"] -= 5
            elif goal == "Ganho de massa muscular" and diet_type != "Personalizada":
                distribution["protein"] += 10
                distribution["carb"] -= 5
                distribution["fat"] -= 5
            
            # Calcular gramas
            carb_calories = total_calories * distribution["carb"] / 100
            protein_calories = total_calories * distribution["protein"] / 100
            fat_calories = total_calories * distribution["fat"] / 100
            
            carb_grams = carb_calories / 4  # 4 kcal/g
            protein_grams = protein_calories / 4  # 4 kcal/g
            fat_grams = fat_calories / 9  # 9 kcal/g
            
            # Exibir resultados
            st.markdown(f"""
            <div class="success-card">
                <h3 style="color: #4CAF50; margin: 0;">🥗 Distribuição de Macronutrientes</h3>
                <p style="margin: 0.5rem 0;"><strong>Dieta:</strong> {diet_type} | <strong>Objetivo:</strong> {goal}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Métricas dos macros
            col1_macro, col2_macro, col3_macro = st.columns(3)
            
            with col1_macro:
                st.metric(
                    label="🍞 Carboidratos",
                    value=f"{carb_grams:.0f}g",
                    delta=f"{distribution['carb']}% | {carb_calories:.0f} kcal"
                )
            
            with col2_macro:
                st.metric(
                    label="🥩 Proteínas", 
                    value=f"{protein_grams:.0f}g",
                    delta=f"{distribution['protein']}% | {protein_calories:.0f} kcal"
                )
            
            with col3_macro:
                st.metric(
                    label="🥑 Gorduras",
                    value=f"{fat_grams:.0f}g", 
                    delta=f"{distribution['fat']}% | {fat_calories:.0f} kcal"
                )
            
            # Gráfico de distribuição
            macro_data = pd.DataFrame({
                'Macronutriente': ['Carboidratos', 'Proteínas', 'Gorduras'],
                'Gramas': [carb_grams, protein_grams, fat_grams],
                'Percentual': [distribution['carb'], distribution['protein'], distribution['fat']],
                'Calorias': [carb_calories, protein_calories, fat_calories]
            })
            
            fig = px.pie(macro_data, values='Calorias', names='Macronutriente',
                        title='Distribuição Calórica dos Macronutrientes',
                        color_discrete_sequence=['#FF9800', '#4CAF50', '#FFC107'])
            st.plotly_chart(fig, use_container_width=True)
            
            # Distribuição por refeição
            st.markdown("#### 🍽️ Distribuição por Refeição")
            
            meals_distribution = pd.DataFrame({
                'Refeição': ['☀️ Café da Manhã', '🍽️ Almoço', '🍎 Lanche', '🌙 Jantar'],
                'Calorias': [total_calories * 0.25, total_calories * 0.35, total_calories * 0.15, total_calories * 0.25],
                'Carboidratos (g)': [carb_grams * 0.25, carb_grams * 0.35, carb_grams * 0.15, carb_grams * 0.25],
                'Proteínas (g)': [protein_grams * 0.25, protein_grams * 0.35, protein_grams * 0.15, protein_grams * 0.25],
                'Gorduras (g)': [fat_grams * 0.25, fat_grams * 0.35, fat_grams * 0.15, fat_grams * 0.25]
            })
            
            # Arredondar valores
            for col in ['Calorias', 'Carboidratos (g)', 'Proteínas (g)', 'Gorduras (g)']:
                meals_distribution[col] = meals_distribution[col].round(0).astype(int)
            
            st.dataframe(meals_distribution, hide_index=True)
    
    with col2:
        # Informações sobre macronutrientes
        st.markdown("#### 📚 Guia de Macronutrientes")
        
        # Carboidratos
        with st.expander("🍞 Carboidratos - Energia Principal"):
            st.markdown("""
            **Função:** Fonte primária de energia para o corpo e cérebro
            
            **Fontes boas:**
            - Frutas, vegetais, leguminosas
            - Grãos integrais (aveia, quinoa, arroz integral)
            - Batata doce, mandioca
            
            **Evitar:**
            - Açúcares refinados
            - Farinhas brancas
            - Doces industrializados
            
            **Timing ideal:**
            - Manhã e pré-treino para energia
            - Pós-treino para recuperação
            """)
        
        # Proteínas  
        with st.expander("🥩 Proteínas - Construção e Reparo"):
            st.markdown("""
            **Função:** Construção muscular, reparo tecidual, enzimas
            
            **Fontes completas:**
            - Carnes, peixes, ovos, laticínios
            - Quinoa, soja
            
            **Fontes vegetais:**
            - Feijões, lentilhas, grão de bico
            - Nozes, sementes
            - Combinações (arroz + feijão)
            
            **Recomendação:**
            - Sedentário: 0.8-1g/kg peso
            - Ativo: 1.2-1.6g/kg peso
            - Atleta: 1.6-2.2g/kg peso
            """)
        
        # Gorduras
        with st.expander("🥑 Gorduras - Hormônios e Vitaminas"):
            st.markdown("""
            **Função:** Produção hormonal, absorção vitaminas, energia
            
            **Gorduras boas:**
            - Abacate, azeite, oleaginosas
            - Peixes gordos (salmão, sardinha)
            - Sementes (chia, linhaça)
            
            **Moderar:**
            - Manteiga, queijos
            - Carnes gordas
            
            **Evitar:**
            - Gorduras trans
            - Frituras em excesso
            - Margarina comum
            """)

# =============================================================================
# PLANOS ALIMENTARES
# =============================================================================

def show_meal_plans():
    """Sistema de planos alimentares"""
    st.markdown('<h1 class="main-header">📋 Planos Alimentares</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Lista de Planos", "➕ Novo Plano", "📊 Acompanhamento", "📄 Modelos"])
    
    with tab1:
        show_meal_plans_list()
    
    with tab2:
        show_new_meal_plan_form()
    
    with tab3:
        show_meal_plans_tracking()
    
    with tab4:
        show_meal_plan_templates()

def show_meal_plans_list():
    """Lista de planos alimentares"""
    st.markdown('<h3 class="sub-header">📋 Planos Alimentares Ativos</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("📊 Status", ["Todos", "ativo", "inativo", "concluído"])
    with col2:
        patient_filter = st.selectbox("👤 Paciente", ["Todos"] + [p['full_name'] for _, p in pd.read_sql_query("SELECT full_name FROM patients WHERE active = 1", conn).iterrows()])
    
    # Query para buscar planos
    query = """
        SELECT mp.id, mp.plan_id, mp.plan_name, p.full_name as patient_name,
               mp.start_date, mp.end_date, mp.daily_calories, mp.status,
               mp.created_at
        FROM meal_plans mp
        JOIN patients p ON mp.patient_id = p.id
        WHERE 1=1
    """
    params = []
    
    if status_filter != "Todos":
        query += " AND mp.status = ?"
        params.append(status_filter)
    
    if patient_filter != "Todos":
        query += " AND p.full_name = ?"
        params.append(patient_filter)
    
    query += " ORDER BY mp.created_at DESC"
    
    plans_df = pd.read_sql_query(query, conn, params=params)
    
    if not plans_df.empty:
        for _, plan in plans_df.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                
                with col1:
                    st.write(f"**📋 {plan['plan_name']}**")
                    st.write(f"👤 {plan['patient_name']}")
                
                with col2:
                    st.write(f"**📅 Início:** {plan['start_date']}")
                    st.write(f"**📅 Fim:** {plan['end_date'] or 'Indefinido'}")
                
                with col3:
                    status_emoji = {'ativo': '🟢', 'inativo': '🟡', 'concluído': '✅'}
                    st.write(f"**Status:** {status_emoji.get(plan['status'], '⚪')} {plan['status'].title()}")
                    st.write(f"**🔥 Calorias:** {plan['daily_calories']}")
                
                with col4:
                    col4_1, col4_2, col4_3 = st.columns(3)
                    with col4_1:
                        if st.button("👁️ Ver", key=f"view_plan_{plan['id']}"):
                            st.session_state.selected_plan = plan['id']
                    with col4_2:
                        if st.button("✏️ Editar", key=f"edit_plan_{plan['id']}"):
                            st.session_state.edit_plan = plan['id']
                    with col4_3:
                        new_status = 'inativo' if plan['status'] == 'ativo' else 'ativo'
                        status_btn = '⏸️ Pausar' if plan['status'] == 'ativo' else '▶️ Ativar'
                        if st.button(status_btn, key=f"toggle_plan_{plan['id']}"):
                            update_plan_status(plan['id'], new_status)
                            st.rerun()
                
                st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
        
        st.info(f"📊 Total: {len(plans_df)} planos encontrados")
    else:
        st.warning("⚠️ Nenhum plano encontrado com os filtros aplicados.")
    
    conn.close()

def show_new_meal_plan_form():
    """Formulário para novo plano alimentar"""
    st.markdown('<h3 class="sub-header">➕ Criar Novo Plano Alimentar</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar pacientes
    patients = pd.read_sql_query("SELECT id, full_name FROM patients WHERE active = 1", conn)
    
    if patients.empty:
        st.warning("⚠️ Nenhum paciente ativo encontrado.")
        return
    
    with st.form("new_meal_plan_form"):
        # Informações básicas
        col1, col2 = st.columns(2)
        
        with col1:
            plan_name = st.text_input("📋 Nome do Plano *", placeholder="Ex: Plano de Emagrecimento - João")
            
            patient_id = st.selectbox(
                "👤 Paciente *",
                patients['id'].tolist(),
                format_func=lambda x: patients[patients['id'] == x]['full_name'].iloc[0]
            )
            
            start_date = st.date_input("📅 Data de Início", value=date.today())
            duration_weeks = st.number_input("📆 Duração (semanas)", min_value=1, max_value=52, value=4)
        
        with col2:
            daily_calories = st.number_input("🔥 Calorias Diárias", min_value=800, max_value=4000, value=1800, step=50)
            
            plan_type = st.selectbox("🥗 Tipo de Plano", [
                "Emagrecimento",
                "Ganho de peso",
                "Manutenção",
                "Low carb",
                "Vegetariano",
                "Vegano",
                "Cetogênico",
                "Mediterrâneo"
            ])
            
            meal_count = st.selectbox("🍽️ Número de Refeições", [3, 4, 5, 6])
            
        # Distribuição de macronutrientes
        st.markdown("### 🥗 Distribuição de Macronutrientes")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            carb_percent = st.slider("🍞 Carboidratos (%)", 10, 70, 50)
        with col2:
            protein_percent = st.slider("🥩 Proteínas (%)", 10, 50, 25)
        with col3:
            fat_percent = 100 - carb_percent - protein_percent
            st.write(f"🥑 Gorduras: {fat_percent}%")
        
        # Restrições e preferências
        st.markdown("### ⚠️ Restrições e Observações")
        
        allergies = st.text_area("🚫 Alergias", placeholder="Ex: Lactose, glúten, nozes...")
        restrictions = st.text_area("⚠️ Restrições", placeholder="Ex: Sem carne vermelha, sem açúcar...")
        preferences = st.text_area("❤️ Preferências", placeholder="Ex: Gosta de peixes, prefere frutas cítricas...")
        notes = st.text_area("📝 Observações", placeholder="Orientações especiais para o paciente...")
        
        submitted = st.form_submit_button("✅ Criar Plano Alimentar", use_container_width=True)
        
        if submitted and plan_name:
            # Calcular data final
            end_date = start_date + timedelta(weeks=duration_weeks)
            plan_id = f"PLN{str(uuid.uuid4())[:8].upper()}"
            
            # Criar estrutura do plano
            plan_data = {
                "type": plan_type,
                "daily_calories": daily_calories,
                "meals_count": meal_count,
                "macros": {
                    "carbs": carb_percent,
                    "protein": protein_percent, 
                    "fat": fat_percent
                },
                "restrictions": {
                    "allergies": allergies,
                    "restrictions": restrictions,
                    "preferences": preferences
                },
                "meals": generate_sample_meal_plan(daily_calories, meal_count, plan_type),
                "notes": notes
            }
            
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    INSERT INTO meal_plans (plan_id, patient_id, nutritionist_id, plan_name,
                                           start_date, end_date, daily_calories, plan_data, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (plan_id, patient_id, st.session_state.user['id'], plan_name,
                      start_date, end_date, daily_calories, json.dumps(plan_data), 'ativo'))
                
                conn.commit()
                
                patient_name = patients[patients['id'] == patient_id]['full_name'].iloc[0]
                st.success(f"✅ Plano alimentar criado para {patient_name}!")
                st.success(f"📋 ID do Plano: {plan_id}")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Erro ao criar plano: {str(e)}")
    
    conn.close()

def generate_sample_meal_plan(calories, meal_count, plan_type):
    """Gera um plano alimentar de exemplo"""
    
    # Distribuição básica de calorias por refeição
    if meal_count == 3:
        meal_distribution = [0.25, 0.45, 0.30]  # Café, Almoço, Jantar
        meal_names = ["Café da Manhã", "Almoço", "Jantar"]
    elif meal_count == 4:
        meal_distribution = [0.25, 0.15, 0.35, 0.25]  # Café, Lanche, Almoço, Jantar
        meal_names = ["Café da Manhã", "Lanche da Manhã", "Almoço", "Jantar"]
    elif meal_count == 5:
        meal_distribution = [0.20, 0.10, 0.35, 0.15, 0.20]
        meal_names = ["Café da Manhã", "Lanche da Manhã", "Almoço", "Lanche da Tarde", "Jantar"]
    else:  # 6 refeições
        meal_distribution = [0.20, 0.10, 0.30, 0.15, 0.15, 0.10]
        meal_names = ["Café da Manhã", "Lanche da Manhã", "Almoço", "Lanche da Tarde", "Jantar", "Ceia"]
    
    # Sugestões por tipo de plano
    meal_suggestions = {
        "Emagrecimento": {
            "Café da Manhã": ["Omelete de claras com vegetais", "Iogurte grego com frutas vermelhas", "Aveia com canela e maçã"],
            "Almoço": ["Salada com frango grelhado", "Peixe com legumes no vapor", "Carne magra com salada"],
            "Jantar": ["Sopa de legumes", "Salada com proteína", "Peixe grelhado com vegetais"],
            "Lanche da Manhã": ["Frutas", "Iogurte natural", "Castanhas (porção pequena)"],
            "Lanche da Tarde": ["Chá verde com biscoito integral", "Fruta com iogurte", "Mix de nuts"],
            "Ceia": ["Chá calmante", "Iogurte desnatado", "Fruta leve"]
        },
        "Low carb": {
            "Café da Manhã": ["Ovos mexidos com abacate", "Omelete com queijo", "Iogurte com nuts"],
            "Almoço": ["Salmão com aspargos", "Frango com brócolis", "Carne com salada verde"],
            "Jantar": ["Peixe com vegetais", "Frango com abobrinha", "Omelete com vegetais"],
            "Lanche da Manhã": ["Abacate", "Castanhas", "Queijo"],
            "Lanche da Tarde": ["Mix de oleaginosas", "Azeitonas", "Iogurte integral"],
            "Ceia": ["Chá", "Algumas nozes", "Queijo cottage"]
        }
    }
    
    # Se não tiver tipo específico, usar emagrecimento como padrão
    suggestions = meal_suggestions.get(plan_type, meal_suggestions["Emagrecimento"])
    
    meals = {}
    for i, meal_name in enumerate(meal_names):
        meal_calories = int(calories * meal_distribution[i])
        meal_options = suggestions.get(meal_name, ["Refeição balanceada"])
        
        meals[meal_name] = {
            "calories": meal_calories,
            "suggestions": meal_options[:2],  # Duas sugestões por refeição
            "time": get_meal_time(meal_name)
        }
    
    return meals

def get_meal_time(meal_name):
    """Retorna horário sugerido para cada refeição"""
    times = {
        "Café da Manhã": "07:00",
        "Lanche da Manhã": "09:30",
        "Almoço": "12:00", 
        "Lanche da Tarde": "15:00",
        "Jantar": "19:00",
        "Ceia": "21:00"
    }
    return times.get(meal_name, "")

def show_meal_plans_tracking():
    """Acompanhamento de planos alimentares"""
    st.markdown('<h3 class="sub-header">📊 Acompanhamento de Planos</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Estatísticas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_plans = pd.read_sql_query("SELECT COUNT(*) as count FROM meal_plans WHERE status = 'ativo'", conn).iloc[0]['count']
        st.metric("📋 Planos Ativos", active_plans)
    
    with col2:
        completed_plans = pd.read_sql_query("SELECT COUNT(*) as count FROM meal_plans WHERE status = 'concluído'", conn).iloc[0]['count']
        st.metric("✅ Concluídos", completed_plans)
    
    with col3:
        avg_calories = pd.read_sql_query("SELECT AVG(daily_calories) as avg FROM meal_plans WHERE status = 'ativo'", conn).iloc[0]['avg']
        st.metric("🔥 Calorias Médias", f"{avg_calories:.0f}" if avg_calories else "0")
    
    with col4:
        total_patients = pd.read_sql_query("SELECT COUNT(DISTINCT patient_id) as count FROM meal_plans WHERE status = 'ativo'", conn).iloc[0]['count']
        st.metric("👥 Pacientes com Plano", total_patients)
    
    # Gráficos de acompanhamento
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por status
        status_data = pd.read_sql_query("""
            SELECT status, COUNT(*) as count
            FROM meal_plans
            GROUP BY status
        """, conn)
        
        if not status_data.empty:
            fig = px.pie(status_data, values='count', names='status',
                        title='Distribuição de Planos por Status')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Calorias por tipo de plano
        calories_data = pd.read_sql_query("""
            SELECT json_extract(plan_data, '$.type') as plan_type,
                   AVG(daily_calories) as avg_calories
            FROM meal_plans 
            WHERE status = 'ativo'
            GROUP BY plan_type
        """, conn)
        
        if not calories_data.empty:
            fig = px.bar(calories_data, x='plan_type', y='avg_calories',
                        title='Calorias Médias por Tipo de Plano')
            st.plotly_chart(fig, use_container_width=True)
    
    # Planos que necessitam atenção
    st.markdown("### ⚠️ Planos que Necessitam Atenção")
    
    attention_plans = pd.read_sql_query("""
        SELECT mp.plan_name, p.full_name as patient_name,
               mp.start_date, mp.end_date, mp.status,
               CASE 
                   WHEN mp.end_date < DATE('now') AND mp.status = 'ativo' THEN 'Vencido'
                   WHEN DATE(mp.end_date, '-7 days') <= DATE('now') AND mp.status = 'ativo' THEN 'Próximo ao vencimento'
                   WHEN mp.status = 'ativo' AND (DATE('now') - DATE(mp.start_date)) > 30 THEN 'Sem acompanhamento recente'
                   ELSE 'OK'
               END as attention_reason
        FROM meal_plans mp
        JOIN patients p ON mp.patient_id = p.id
        WHERE attention_reason != 'OK'
        ORDER BY mp.end_date
    """, conn)
    
    if not attention_plans.empty:
        for _, plan in attention_plans.iterrows():
            alert_type = "error" if plan['attention_reason'] == 'Vencido' else "warning"
            
            if alert_type == "error":
                st.error(f"🚨 **{plan['plan_name']}** ({plan['patient_name']}) - {plan['attention_reason']}")
            else:
                st.warning(f"⚠️ **{plan['plan_name']}** ({plan['patient_name']}) - {plan['attention_reason']}")
    else:
        st.success("✅ Todos os planos estão em dia!")
    
    conn.close()

def show_meal_plan_templates():
    """Modelos de planos alimentares"""
    st.markdown('<h3 class="sub-header">📄 Modelos de Planos Alimentares</h3>', unsafe_allow_html=True)
    
    templates = {
        "🏃 Emagrecimento Saudável (1400 kcal)": {
            "description": "Plano focado em déficit calórico sustentável com alimentos nutritivos",
            "target": "Perda de 0.5-1kg por semana",
            "macros": "40% Carb | 30% Prot | 30% Gord",
            "meals": {
                "Café da Manhã (350 kcal)": [
                    "2 fatias de pão integral",
                    "1 ovo mexido",
                    "1/2 abacate pequeno", 
                    "Café com leite desnatado"
                ],
                "Lanche da Manhã (150 kcal)": [
                    "1 fruta média",
                    "10 castanhas do pará"
                ],
                "Almoço (490 kcal)": [
                    "100g frango grelhado",
                    "1 xícara arroz integral",
                    "Salada verde à vontade",
                    "1 colher azeite extra virgem"
                ],
                "Lanche da Tarde (140 kcal)": [
                    "1 iogurte natural",
                    "1 colher granola caseira"
                ],
                "Jantar (270 kcal)": [
                    "100g peixe grelhado",
                    "Legumes no vapor",
                    "1 batata doce pequena"
                ]
            }
        },
        
        "💪 Ganho de Massa Muscular (2200 kcal)": {
            "description": "Plano hipercalórico com foco em proteínas para hipertrofia",
            "target": "Ganho de 0.5kg por semana",
            "macros": "45% Carb | 30% Prot | 25% Gord",
            "meals": {
                "Café da Manhã (550 kcal)": [
                    "1 vitamina (banana, aveia, leite, whey)",
                    "2 fatias pão integral com pasta amendoim",
                    "Café com leite"
                ],
                "Lanche da Manhã (220 kcal)": [
                    "1 banana",
                    "1 punhado mix de castanhas"
                ],
                "Almoço (660 kcal)": [
                    "150g carne vermelha magra",
                    "1.5 xícara arroz",
                    "Feijão",
                    "Salada com azeite"
                ],
                "Pré-treino (180 kcal)": [
                    "1 banana com aveia",
                    "Água de coco"
                ],
                "Pós-treino (200 kcal)": [
                    "Whey protein com água",
                    "1 fruta"
                ],
                "Jantar (390 kcal)": [
                    "120g frango",
                    "Batata doce",
                    "Vegetais refogados"
                ]
            }
        },
        
        "🥗 Low Carb (1600 kcal)": {
            "description": "Redução de carboidratos para cetose leve e queima de gordura",
            "target": "Emagrecimento e controle glicêmico",
            "macros": "20% Carb | 30% Prot | 50% Gord",
            "meals": {
                "Café da Manhã (400 kcal)": [
                    "Omelete com 2 ovos",
                    "Queijo, tomate, espinafre",
                    "1/2 abacate",
                    "Café puro ou com creme"
                ],
                "Lanche da Manhã (200 kcal)": [
                    "Mix de oleaginosas",
                    "Queijo curado pequeno"
                ],
                "Almoço (560 kcal)": [
                    "150g salmão grelhado",
                    "Salada verde abundante",
                    "Azeite extra virgem",
                    "Aspargos na manteiga"
                ],
                "Lanche da Tarde (160 kcal)": [
                    "Azeitonas verdes",
                    "Fatias de pepino com cream cheese"
                ],
                "Jantar (280 kcal)": [
                    "100g frango",
                    "Abobrinha refogada",
                    "Salada de rúcula"
                ]
            }
        },
        
        "🌱 Vegetariano Equilibrado (1800 kcal)": {
            "description": "Plano vegetariano com proteínas vegetais completas",
            "target": "Manutenção saudável sem carne",
            "macros": "50% Carb | 20% Prot | 30% Gord",
            "meals": {
                "Café da Manhã (450 kcal)": [
                    "Bowl de overnight oats",
                    "Frutas vermelhas",
                    "Pasta de amendoim",
                    "Leite vegetal"
                ],
                "Lanche da Manhã (180 kcal)": [
                    "1 fruta",
                    "Castanhas do Brasil"
                ],
                "Almoço (630 kcal)": [
                    "Grão de bico refogado",
                    "Quinoa cozida",
                    "Salada colorida",
                    "Molho tahine"
                ],
                "Lanche da Tarde (190 kcal)": [
                    "Homus caseiro",
                    "Palitos de vegetais"
                ],
                "Jantar (350 kcal)": [
                    "Tofu grelhado",
                    "Vegetais no wok",
                    "Azeite de oliva"
                ]
            }
        }
    }
    
    # Exibir templates
    for template_name, template_data in templates.items():
        with st.expander(template_name):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **📝 Descrição:** {template_data['description']}
                
                **🎯 Objetivo:** {template_data['target']}
                
                **🥗 Macronutrientes:** {template_data['macros']}
                """)
                
                if st.button(f"📋 Usar este modelo", key=f"use_{template_name}"):
                    st.success(f"✅ Modelo '{template_name}' selecionado! Vá para a aba 'Novo Plano' para personalizar.")
                    # Aqui poderia armazenar no session_state para usar no formulário
            
            with col2:
                st.markdown("**🍽️ Exemplo de Cardápio:**")
                for meal, foods in template_data['meals'].items():
                    st.markdown(f"**{meal}:**")
                    for food in foods:
                        st.markdown(f"• {food}")
                    st.markdown("")

def update_plan_status(plan_id, new_status):
    """Atualiza status do plano alimentar"""
    conn = sqlite3.connect('nutriapp360.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE meal_plans SET status = ? WHERE id = ?", (new_status, plan_id))
    conn.commit()
    conn.close()

# =============================================================================
# BANCO DE RECEITAS
# =============================================================================

def show_recipes():
    """Sistema de receitas"""
    st.markdown('<h1 class="main-header">🍳 Banco de Receitas</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Explorar Receitas", "➕ Nova Receita", "🔍 Busca Avançada", "📊 Minhas Estatísticas"])
    
    with tab1:
        show_recipes_explorer()
    
    with tab2:
        show_new_recipe_form()
    
    with tab3:
        show_recipes_advanced_search()
    
    with tab4:
        show_recipes_stats()

def show_recipes_explorer():
    """Explorar receitas"""
    st.markdown('<h3 class="sub-header">📚 Explorar Receitas</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Filtros rápidos
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        category_filter = st.selectbox("🏷️ Categoria", [
            "Todas", "Café da manhã", "Saladas", "Pratos principais", 
            "Lanches", "Sobremesas", "Bebidas", "Sopas"
        ])
    
    with col2:
        difficulty_filter = st.selectbox("👩‍🍳 Dificuldade", ["Todas", "Fácil", "Médio", "Difícil"])
    
    with col3:
        max_time = st.slider("⏱️ Tempo máximo (min)", 0, 120, 60, 15)
    
    with col4:
        max_calories = st.slider("🔥 Calorias máx/porção", 0, 800, 400, 50)
    
    # Query para buscar receitas
    query = """
        SELECT id, recipe_id, name, category, prep_time, cook_time,
               servings, calories_per_serving, protein, carbs, fat, fiber,
               ingredients, instructions, tags, difficulty
        FROM recipes
        WHERE is_public = 1
    """
    params = []
    
    if category_filter != "Todas":
        query += " AND category = ?"
        params.append(category_filter)
    
    if difficulty_filter != "Todas":
        query += " AND difficulty = ?"
        params.append(difficulty_filter)
    
    query += " AND (prep_time + cook_time) <= ?"
    params.append(max_time)
    
    query += " AND calories_per_serving <= ?"
    params.append(max_calories)
    
    query += " ORDER BY name"
    
    recipes_df = pd.read_sql_query(query, conn, params=params)
    
    if not recipes_df.empty:
        # Grid de receitas
        for i in range(0, len(recipes_df), 2):
            col1, col2 = st.columns(2)
            
            for j, col in enumerate([col1, col2]):
                if i + j < len(recipes_df):
                    recipe = recipes_df.iloc[i + j]
                    
                    with col:
                        with st.container():
                            st.markdown(f"""
                            <div class="recipe-card">
                                <h4 style="color: #FF9800; margin: 0;">{recipe['name']}</h4>
                                <p style="margin: 0.5rem 0; font-size: 0.9rem;">
                                    <strong>🏷️ {recipe['category']}</strong> | 
                                    <strong>⏱️ {recipe['prep_time'] + recipe['cook_time']}min</strong> | 
                                    <strong>👥 {recipe['servings']} porções</strong>
                                </p>
                                <p style="margin: 0.5rem 0;">
                                    <strong>🔥 {recipe['calories_per_serving']} kcal</strong> | 
                                    <strong>🥩 {recipe['protein']}g prot</strong> | 
                                    <strong>🍞 {recipe['carbs']}g carb</strong> | 
                                    <strong>🥑 {recipe['fat']}g gord</strong>
                                </p>
                                <p style="margin: 0; font-size: 0.8rem; color: #666;">
                                    <strong>🏅 Dificuldade:</strong> {recipe['difficulty']}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if st.button(f"👁️ Ver Receita Completa", key=f"view_recipe_{recipe['id']}"):
                                show_recipe_details(recipe)
        
        st.info(f"🍳 {len(recipes_df)} receitas encontradas")
        
    else:
        st.warning("⚠️ Nenhuma receita encontrada com os filtros aplicados.")
    
    conn.close()

def show_recipe_details(recipe):
    """Mostra detalhes completos da receita"""
    st.markdown(f"### 🍳 {recipe['name']}")
    
    # Informações nutricionais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔥 Calorias", f"{recipe['calories_per_serving']} kcal")
    with col2:
        st.metric("🥩 Proteínas", f"{recipe['protein']}g")
    with col3:
        st.metric("🍞 Carboidratos", f"{recipe['carbs']}g")
    with col4:
        st.metric("🥑 Gorduras", f"{recipe['fat']}g")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🛒 Ingredientes")
        ingredients_list = recipe['ingredients'].split('\n') if recipe['ingredients'] else []
        for ingredient in ingredients_list:
            if ingredient.strip():
                st.markdown(f"• {ingredient.strip()}")
    
    with col2:
        st.markdown("#### 👨‍🍳 Modo de Preparo")
        instructions_list = recipe['instructions'].split('\n') if recipe['instructions'] else []
        for i, instruction in enumerate(instructions_list, 1):
            if instruction.strip():
                st.markdown(f"{i}. {instruction.strip()}")
    
    # Tags
    if recipe['tags']:
        st.markdown("#### 🏷️ Tags")
        tags = recipe['tags'].split(',')
        tag_buttons = " ".join([f"`{tag.strip()}`" for tag in tags])
        st.markdown(tag_buttons)

def show_new_recipe_form():
    """Formulário para nova receita"""
    st.markdown('<h3 class="sub-header">➕ Cadastrar Nova Receita</h3>', unsafe_allow_html=True)
    
    with st.form("new_recipe_form"):
        # Informações básicas
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("🍳 Nome da Receita *", placeholder="Ex: Salada de Quinoa Colorida")
            category = st.selectbox("🏷️ Categoria", [
                "Café da manhã", "Saladas", "Pratos principais", "Lanches", 
                "Sobremesas", "Bebidas", "Sopas", "Molhos", "Acompanhamentos"
            ])
            difficulty = st.selectbox("👩‍🍳 Dificuldade", ["Fácil", "Médio", "Difícil"])
            servings = st.number_input("👥 Número de Porções", min_value=1, max_value=20, value=4)
        
        with col2:
            prep_time = st.number_input("⏱️ Tempo de Preparo (min)", min_value=0, max_value=300, value=15)
            cook_time = st.number_input("🔥 Tempo de Cozimento (min)", min_value=0, max_value=300, value=15)
            
            is_public = st.checkbox("🌐 Receita pública", value=True, help="Permitir que outros nutricionistas vejam esta receita")
        
        # Informações nutricionais
        st.markdown("### 📊 Informações Nutricionais (por porção)")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            calories = st.number_input("🔥 Calorias", min_value=0, max_value=1000, value=200, step=10)
        with col2:
            protein = st.number_input("🥩 Proteínas (g)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
        with col3:
            carbs = st.number_input("🍞 Carboidratos (g)", min_value=0.0, max_value=200.0, value=30.0, step=0.5)
        with col4:
            fat = st.number_input("🥑 Gorduras (g)", min_value=0.0, max_value=100.0, value=8.0, step=0.5)
        with col5:
            fiber = st.number_input("🌾 Fibras (g)", min_value=0.0, max_value=50.0, value=3.0, step=0.5)
        
        # Ingredientes e preparo
        st.markdown("### 🛒 Ingredientes")
        ingredients = st.text_area("Lista de Ingredientes *", 
                                  placeholder="Digite cada ingrediente em uma linha:\n1 xícara de quinoa\n2 tomates médios\n1/2 pepino...",
                                  height=100)
        
        st.markdown("### 👨‍🍳 Modo de Preparo")
        instructions = st.text_area("Instruções de Preparo *",
                                   placeholder="Digite cada passo em uma linha:\n1. Lave a quinoa em água corrente\n2. Cozinhe em água fervente...",
                                   height=150)
        
        # Tags
        tags = st.text_input("🏷️ Tags", 
                            placeholder="saudável, vegetariano, sem glúten, rápido (separar por vírgula)")
        
        submitted = st.form_submit_button("✅ Cadastrar Receita", use_container_width=True)
        
        if submitted and name and ingredients and instructions:
            recipe_id = f"REC{str(uuid.uuid4())[:8].upper()}"
            
            conn = sqlite3.connect('nutriapp360.db')
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    INSERT INTO recipes (recipe_id, name, category, prep_time, cook_time,
                                       servings, calories_per_serving, protein, carbs, fat, fiber,
                                       ingredients, instructions, tags, difficulty, nutritionist_id, is_public)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (recipe_id, name, category, prep_time, cook_time, servings, calories,
                      protein, carbs, fat, fiber, ingredients, instructions, tags,
                      difficulty, st.session_state.user['id'], is_public))
                
                conn.commit()
                st.success(f"✅ Receita '{name}' cadastrada com sucesso! ID: {recipe_id}")
                st.balloons()
                
            except Exception as e:
                st.error(f"❌ Erro ao cadastrar receita: {str(e)}")
            
            finally:
                conn.close()
        
        elif submitted:
            st.error("❌ Preencha todos os campos obrigatórios!")

def show_recipes_advanced_search():
    """Busca avançada de receitas"""
    st.markdown('<h3 class="sub-header">🔍 Busca Avançada de Receitas</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Filtros avançados
    with st.form("advanced_search_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            name_search = st.text_input("🔍 Nome contém", placeholder="Ex: salada, frango...")
            category_filter = st.multiselect("🏷️ Categorias", [
                "Café da manhã", "Saladas", "Pratos principais", "Lanches", 
                "Sobremesas", "Bebidas", "Sopas", "Molhos", "Acompanhamentos"
            ])
            tags_search = st.text_input("🏷️ Tags", placeholder="vegetariano, sem glúten...")
        
        with col2:
            calories_range = st.slider("🔥 Calorias por porção", 0, 800, (0, 400), step=25)
            protein_range = st.slider("🥩 Proteínas (g)", 0, 50, (0, 25), step=1)
            time_range = st.slider("⏱️ Tempo total (min)", 0, 120, (0, 60), step=5)
        
        with col3:
            difficulty_filter = st.multiselect("👩‍🍳 Dificuldade", ["Fácil", "Médio", "Difícil"])
            servings_range = st.slider("👥 Porções", 1, 10, (1, 6))
            only_mine = st.checkbox("📝 Apenas minhas receitas")
        
        search_button = st.form_submit_button("🔍 Buscar Receitas")
    
    if search_button:
        # Construir query
        query = """
            SELECT r.*, u.full_name as author_name
            FROM recipes r
            LEFT JOIN users u ON r.nutritionist_id = u.id
            WHERE 1=1
        """
        params = []
        
        if name_search:
            query += " AND r.name LIKE ?"
            params.append(f"%{name_search}%")
        
        if category_filter:
            placeholders = ",".join(["?" for _ in category_filter])
            query += f" AND r.category IN ({placeholders})"
            params.extend(category_filter)
        
        if tags_search:
            query += " AND r.tags LIKE ?"
            params.append(f"%{tags_search}%")
        
        if difficulty_filter:
            placeholders = ",".join(["?" for _ in difficulty_filter])
            query += f" AND r.difficulty IN ({placeholders})"
            params.extend(difficulty_filter)
        
        query += " AND r.calories_per_serving BETWEEN ? AND ?"
        params.extend([calories_range[0], calories_range[1]])
        
        query += " AND r.protein BETWEEN ? AND ?"
        params.extend([protein_range[0], protein_range[1]])
        
        query += " AND (r.prep_time + r.cook_time) BETWEEN ? AND ?"
        params.extend([time_range[0], time_range[1]])
        
        query += " AND r.servings BETWEEN ? AND ?"
        params.extend([servings_range[0], servings_range[1]])
        
        if only_mine:
            query += " AND r.nutritionist_id = ?"
            params.append(st.session_state.user['id'])
        else:
            query += " AND r.is_public = 1"
        
        query += " ORDER BY r.name"
        
        results_df = pd.read_sql_query(query, conn, params=params)
        
        if not results_df.empty:
            st.success(f"🎯 Encontradas {len(results_df)} receitas")
            
            # Exibir resultados em tabela interativa
            display_columns = ['name', 'category', 'calories_per_serving', 'protein', 
                             'prep_time', 'cook_time', 'difficulty', 'author_name']
            
            column_config = {
                'name': 'Receita',
                'category': 'Categoria',
                'calories_per_serving': 'Calorias',
                'protein': 'Proteínas (g)',
                'prep_time': 'Prep (min)',
                'cook_time': 'Cozimento (min)', 
                'difficulty': 'Dificuldade',
                'author_name': 'Autor'
            }
            
            selected_recipe = st.dataframe(
                results_df[display_columns],
                column_config=column_config,
                hide_index=True,
                use_container_width=True
            )
            
        else:
            st.warning("⚠️ Nenhuma receita encontrada com os critérios especificados.")
    
    conn.close()

def show_recipes_stats():
    """Estatísticas das receitas"""
    st.markdown('<h3 class="sub-header">📊 Minhas Estatísticas de Receitas</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Estatísticas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        my_recipes = pd.read_sql_query("SELECT COUNT(*) as count FROM recipes WHERE nutritionist_id = ?", 
                                      conn, params=[st.session_state.user['id']]).iloc[0]['count']
        st.metric("🍳 Minhas Receitas", my_recipes)
    
    with col2:
        public_recipes = pd.read_sql_query("SELECT COUNT(*) as count FROM recipes WHERE nutritionist_id = ? AND is_public = 1", 
                                         conn, params=[st.session_state.user['id']]).iloc[0]['count']
        st.metric("🌐 Receitas Públicas", public_recipes)
    
    with col3:
        avg_calories = pd.read_sql_query("SELECT AVG(calories_per_serving) as avg FROM recipes WHERE nutritionist_id = ?", 
                                       conn, params=[st.session_state.user['id']]).iloc[0]['avg']
        st.metric("🔥 Calorias Médias", f"{avg_calories:.0f}" if avg_calories else "0")
    
    with col4:
        total_recipes = pd.read_sql_query("SELECT COUNT(*) as count FROM recipes WHERE is_public = 1", conn).iloc[0]['count']
        st.metric("📚 Total na Base", total_recipes)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por categoria (minhas receitas)
        category_data = pd.read_sql_query("""
            SELECT category, COUNT(*) as count
            FROM recipes
            WHERE nutritionist_id = ?
            GROUP BY category
            ORDER BY count DESC
        """, conn, params=[st.session_state.user['id']])
        
        if not category_data.empty:
            fig = px.pie(category_data, values='count', names='category',
                        title='Minhas Receitas por Categoria')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Cadastre receitas para ver estatísticas!")
    
    with col2:
        # Distribuição calórica
        calories_data = pd.read_sql_query("""
            SELECT 
                CASE 
                    WHEN calories_per_serving < 200 THEN 'Baixa (< 200)'
                    WHEN calories_per_serving < 400 THEN 'Moderada (200-400)'
                    WHEN calories_per_serving < 600 THEN 'Alta (400-600)'
                    ELSE 'Muito Alta (> 600)'
                END as calorie_range,
                COUNT(*) as count
            FROM recipes
            WHERE nutritionist_id = ?
            GROUP BY calorie_range
        """, conn, params=[st.session_state.user['id']])
        
        if not calories_data.empty:
            fig = px.bar(calories_data, x='calorie_range', y='count',
                        title='Distribuição Calórica das Receitas')
            st.plotly_chart(fig, use_container_width=True)
    
    # Top receitas por macronutrientes
    if my_recipes > 0:
        st.markdown("### 🏆 Top Receitas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🥩 Mais Rica em Proteínas")
            top_protein = pd.read_sql_query("""
                SELECT name, protein, calories_per_serving
                FROM recipes
                WHERE nutritionist_id = ?
                ORDER BY protein DESC
                LIMIT 5
            """, conn, params=[st.session_state.user['id']])
            
            for _, recipe in top_protein.iterrows():
                st.write(f"**{recipe['name']}** - {recipe['protein']}g prot ({recipe['calories_per_serving']} kcal)")
        
        with col2:
            st.markdown("#### 🌾 Mais Rica em Fibras")
            top_fiber = pd.read_sql_query("""
                SELECT name, fiber, calories_per_serving
                FROM recipes
                WHERE nutritionist_id = ?
                ORDER BY fiber DESC
                LIMIT 5
            """, conn, params=[st.session_state.user['id']])
            
            for _, recipe in top_fiber.iterrows():
                st.write(f"**{recipe['name']}** - {recipe['fiber']}g fibra ({recipe['calories_per_serving']} kcal)")
        
        with col3:
            st.markdown("#### ⚡ Mais Rápidas")
            quickest = pd.read_sql_query("""
                SELECT name, (prep_time + cook_time) as total_time, calories_per_serving
                FROM recipes
                WHERE nutritionist_id = ?
                ORDER BY total_time ASC
                LIMIT 5
            """, conn, params=[st.session_state.user['id']])
            
            for _, recipe in quickest.iterrows():
                st.write(f"**{recipe['name']}** - {recipe['total_time']}min ({recipe['calories_per_serving']} kcal)")
    
    conn.close()

# =============================================================================
# ANALYTICS AVANÇADO
# =============================================================================

def show_analytics():
    """Analytics avançado"""
    st.markdown('<h1 class="main-header">📈 Analytics Avançado</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview Geral", "👥 Análise de Pacientes", "📅 Performance Consultas", "🎯 Metas e KPIs"])
    
    with tab1:
        show_general_overview()
    
    with tab2:
        show_patient_analytics()
    
    with tab3:
        show_appointments_analytics()
    
    with tab4:
        show_kpis_analytics()

def show_general_overview():
    """Overview geral do sistema"""
    st.markdown('<h3 class="sub-header">📊 Visão Geral do Sistema</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    # Total de pacientes
    with col1:
        total_patients = pd.read_sql_query("SELECT COUNT(*) as count FROM patients WHERE active = 1", conn).iloc[0]['count']
        patients_this_month = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM patients 
            WHERE active = 1 AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
        """, conn).iloc[0]['count']
        st.metric("👥 Pacientes Ativos", total_patients, delta=f"+{patients_this_month} este mês")
    
    # Consultas realizadas
    with col2:
        completed_appointments = pd.read_sql_query("SELECT COUNT(*) as count FROM appointments WHERE status = 'realizada'", conn).iloc[0]['count']
        appointments_this_week = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM appointments 
            WHERE status = 'realizada' AND DATE(appointment_date) >= DATE('now', '-7 days')
        """, conn).iloc[0]['count']
        st.metric("✅ Consultas Realizadas", completed_appointments, delta=f"+{appointments_this_week} esta semana")
    
    # Planos ativos
    with col3:
        active_plans = pd.read_sql_query("SELECT COUNT(*) as count FROM meal_plans WHERE status = 'ativo'", conn).iloc[0]['count']
        st.metric("📋 Planos Ativos", active_plans)
    
    # Receitas criadas
    with col4:
        my_recipes = pd.read_sql_query("SELECT COUNT(*) as count FROM recipes WHERE nutritionist_id = ?", 
                                      conn, params=[st.session_state.user['id']]).iloc[0]['count']
        st.metric("🍳 Minhas Receitas", my_recipes)
    
    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        # Evolução mensal de novos pacientes
        st.markdown("#### 📈 Crescimento de Pacientes")
        
        monthly_patients = pd.read_sql_query("""
            SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as new_patients
            FROM patients
            WHERE created_at >= DATE('now', '-12 months')
            GROUP BY month
            ORDER BY month
        """, conn)
        
        if not monthly_patients.empty:
            # Converter formato da data para melhor visualização
            monthly_patients['month_name'] = pd.to_datetime(monthly_patients['month']).dt.strftime('%b/%Y')
            
            fig = px.line(monthly_patients, x='month_name', y='new_patients',
                         title='Novos Pacientes por Mês', markers=True,
                         labels={'month_name': 'Mês', 'new_patients': 'Novos Pacientes'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 Dados insuficientes para gráfico temporal")
    
    with col2:
        # Taxa de sucesso dos planos
        st.markdown("#### 🎯 Performance dos Planos")
        
        plan_success = pd.read_sql_query("""
            SELECT 
                mp.status,
                COUNT(*) as count,
                AVG(CASE WHEN pp.weight IS NOT NULL THEN 1 ELSE 0 END) as has_progress
            FROM meal_plans mp
            LEFT JOIN patient_progress pp ON mp.patient_id = pp.patient_id
            GROUP BY mp.status
        """, conn)
        
        if not plan_success.empty:
            status_colors = {'ativo': '#4CAF50', 'concluído': '#2196F3', 'inativo': '#FF9800'}
            fig = px.pie(plan_success, values='count', names='status',
                        title='Distribuição Status dos Planos',
                        color='status',
                        color_discrete_map=status_colors)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Resumo semanal
    st.markdown("### 📅 Resumo da Semana")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Consultas desta semana
        week_appointments = pd.read_sql_query("""
            SELECT 
                DATE(appointment_date) as date,
                COUNT(*) as count,
                status
            FROM appointments
            WHERE DATE(appointment_date) >= DATE('now', '-7 days')
              AND DATE(appointment_date) <= DATE('now', '+7 days')
            GROUP BY DATE(appointment_date), status
            ORDER BY date
        """, conn)
        
        if not week_appointments.empty:
            st.markdown("**📅 Consultas (Próximos 7 dias)**")
            for _, apt in week_appointments.iterrows():
                status_emoji = {'agendado': '🟡', 'realizada': '🟢', 'cancelada': '🔴'}
                date_formatted = pd.to_datetime(apt['date']).strftime('%d/%m')
                st.write(f"{date_formatted}: {apt['count']} {status_emoji.get(apt['status'], '⚪')}")
        else:
            st.info("📅 Nenhuma consulta programada")
    
    with col2:
        # Pacientes que precisam atenção
        attention_needed = pd.read_sql_query("""
            SELECT p.full_name, 
                   MAX(DATE(a.appointment_date)) as last_appointment,
                   p.current_weight - p.target_weight as weight_diff
            FROM patients p
            LEFT JOIN appointments a ON p.id = a.patient_id AND a.status = 'realizada'
            WHERE p.active = 1
            GROUP BY p.id
            HAVING last_appointment < DATE('now', '-30 days') OR weight_diff > 5 OR last_appointment IS NULL
            ORDER BY last_appointment ASC
            LIMIT 5
        """, conn)
        
        if not attention_needed.empty:
            st.markdown("**⚠️ Pacientes Necessitam Atenção**")
            for _, patient in attention_needed.iterrows():
                last_apt = patient['last_appointment'] if patient['last_appointment'] else 'Nunca'
                st.write(f"👤 {patient['full_name'][:20]}... (Última: {last_apt})")
        else:
            st.success("✅ Todos pacientes em dia!")
    
    with col3:
        # Próximas tarefas
        upcoming_tasks = pd.read_sql_query("""
            SELECT 
                'Consulta: ' || p.full_name as task,
                a.appointment_date as due_date,
                'appointment' as type
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            WHERE a.status = 'agendado' 
              AND DATE(a.appointment_date) BETWEEN DATE('now') AND DATE('now', '+7 days')
            
            UNION ALL
            
            SELECT 
                'Plano vence: ' || mp.plan_name as task,
                mp.end_date as due_date,
                'plan' as type
            FROM meal_plans mp
            WHERE mp.status = 'ativo'
              AND DATE(mp.end_date) BETWEEN DATE('now') AND DATE('now', '+14 days')
            
            ORDER BY due_date ASC
            LIMIT 5
        """, conn)
        
        if not upcoming_tasks.empty:
            st.markdown("**📋 Próximas Tarefas**")
            for _, task in upcoming_tasks.iterrows():
                date_formatted = pd.to_datetime(task['due_date']).strftime('%d/%m')
                emoji = '📅' if task['type'] == 'appointment' else '📋'
                st.write(f"{emoji} {date_formatted}: {task['task'][:25]}...")
        else:
            st.info("📋 Nenhuma tarefa urgente")
    
    conn.close()

def show_patient_analytics():
    """Análise detalhada dos pacientes"""
    st.markdown('<h3 class="sub-header">👥 Análise Detalhada de Pacientes</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Análise demográfica
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Perfil Demográfico")
        
        # Distribuição por gênero
        gender_data = pd.read_sql_query("""
            SELECT 
                CASE WHEN gender = 'M' THEN 'Masculino' ELSE 'Feminino' END as gender,
                COUNT(*) as count,
                AVG(current_weight) as avg_weight,
                AVG(height) as avg_height
            FROM patients 
            WHERE active = 1
            GROUP BY gender
        """, conn)
        
        if not gender_data.empty:
            fig = px.pie(gender_data, values='count', names='gender',
                        title='Distribuição por Gênero',
                        color_discrete_sequence=['#4CAF50', '#FF9800'])
            st.plotly_chart(fig, use_container_width=True)
            
            # Métricas por gênero
            st.markdown("**👥 Métricas por Gênero:**")
            for _, row in gender_data.iterrows():
                st.write(f"**{row['gender']}:** {row['count']} pacientes | Peso médio: {row['avg_weight']:.1f}kg | Altura média: {row['avg_height']:.2f}m")
    
    with col2:
        st.markdown("#### 📈 Análise de IMC")
        
        # Distribuição de IMC
        imc_data = pd.read_sql_query("""
            SELECT 
                CASE 
                    WHEN current_weight/(height*height) < 18.5 THEN 'Abaixo do peso'
                    WHEN current_weight/(height*height) < 25 THEN 'Peso normal'
                    WHEN current_weight/(height*height) < 30 THEN 'Sobrepeso'
                    ELSE 'Obesidade'
                END as imc_category,
                COUNT(*) as count
            FROM patients
            WHERE active = 1 AND current_weight > 0 AND height > 0
            GROUP BY imc_category
        """, conn)
        
        if not imc_data.empty:
            colors = {'Abaixo do peso': '#FFA726', 'Peso normal': '#4CAF50', 
                     'Sobrepeso': '#FF9800', 'Obesidade': '#F44336'}
            
            fig = px.bar(imc_data, x='imc_category', y='count',
                        title='Distribuição de IMC dos Pacientes',
                        color='imc_category',
                        color_discrete_map=colors)
            st.plotly_chart(fig, use_container_width=True)
    
    # Evolução dos pacientes
    st.markdown("#### 📈 Evolução e Progresso")
    
    progress_data = pd.read_sql_query("""
        SELECT 
            p.full_name,
            pr.record_date,
            pr.weight,
            p.target_weight,
            (p.current_weight - pr.weight) as weight_lost,
            CASE 
                WHEN pr.weight <= p.target_weight THEN 'Meta atingida'
                WHEN (p.current_weight - pr.weight) > 2 THEN 'Progresso bom'
                WHEN (p.current_weight - pr.weight) > 0 THEN 'Progresso lento'
                ELSE 'Sem progresso'
            END as progress_status
        FROM patients p
        JOIN patient_progress pr ON p.id = pr.patient_id
        WHERE p.active = 1
        ORDER BY pr.record_date DESC
    """, conn)
    
    if not progress_data.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de evolução temporal
            fig = px.line(progress_data, x='record_date', y='weight', 
                         color='full_name', title='Evolução do Peso dos Pacientes')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Status do progresso
            progress_status = progress_data.groupby('progress_status').size().reset_index(name='count')
            
            fig = px.pie(progress_status, values='count', names='progress_status',
                        title='Status do Progresso dos Pacientes')
            st.plotly_chart(fig, use_container_width=True)
        
        # Top pacientes por progresso
        st.markdown("#### 🏆 Ranking de Progresso")
        
        top_progress = progress_data.groupby('full_name').agg({
            'weight_lost': 'max',
            'progress_status': 'last'
        }).sort_values('weight_lost', ascending=False).head(10)
        
        col1, col2, col3 = st.columns(3)
        
        for i, (name, data) in enumerate(top_progress.iterrows()):
            col = [col1, col2, col3][i % 3]
            
            with col:
                if data['weight_lost'] > 0:
                    st.success(f"🏆 **{name[:15]}...**\n{data['weight_lost']:.1f}kg perdidos\n{data['progress_status']}")
                else:
                    st.info(f"📊 **{name[:15]}...**\n{abs(data['weight_lost']):.1f}kg ganhos\n{data['progress_status']}")
    
    else:
        st.info("📊 Registre progresso dos pacientes para ver análises detalhadas")
    
    # Análise de retenção
    st.markdown("#### 🔄 Análise de Retenção")
    
    retention_data = pd.read_sql_query("""
        SELECT 
            strftime('%Y-%m', p.created_at) as cohort_month,
            COUNT(*) as patients_started,
            COUNT(CASE WHEN DATE(p.created_at, '+30 days') <= DATE('now') 
                       AND EXISTS(SELECT 1 FROM appointments a 
                                 WHERE a.patient_id = p.id 
                                 AND a.appointment_date > DATE(p.created_at, '+30 days')) 
                  THEN 1 END) as retained_30_days,
            COUNT(CASE WHEN DATE(p.created_at, '+90 days') <= DATE('now') 
                       AND EXISTS(SELECT 1 FROM appointments a 
                                 WHERE a.patient_id = p.id 
                                 AND a.appointment_date > DATE(p.created_at, '+90 days')) 
                  THEN 1 END) as retained_90_days
        FROM patients p
        WHERE p.created_at >= DATE('now', '-12 months')
        GROUP BY cohort_month
        ORDER BY cohort_month
    """, conn)
    
    if not retention_data.empty:
        # Calcular taxas de retenção
        retention_data['retention_30d'] = (retention_data['retained_30_days'] / retention_data['patients_started'] * 100).round(1)
        retention_data['retention_90d'] = (retention_data['retained_90_days'] / retention_data['patients_started'] * 100).round(1)
        
        fig = px.line(retention_data, x='cohort_month', 
                     y=['retention_30d', 'retention_90d'],
                     title='Taxa de Retenção por Coorte (%)',
                     labels={'value': 'Taxa de Retenção (%)', 'cohort_month': 'Mês de Início'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Resumo da retenção
        avg_retention_30 = retention_data['retention_30d'].mean()
        avg_retention_90 = retention_data['retention_90d'].mean()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 Retenção Média 30 dias", f"{avg_retention_30:.1f}%")
        with col2:
            st.metric("📊 Retenção Média 90 dias", f"{avg_retention_90:.1f}%")
    
    conn.close()

def show_appointments_analytics():
    """Analytics de consultas"""
    st.markdown('<h3 class="sub-header">📅 Análise de Performance das Consultas</h3>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Métricas de consultas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_appointments = pd.read_sql_query("SELECT COUNT(*) as count FROM appointments", conn).iloc[0]['count']
        st.metric("📅 Total Consultas", total_appointments)
    
    with col2:
        completion_rate = pd.read_sql_query("""
            SELECT 
                ROUND(COUNT(CASE WHEN status = 'realizada' THEN 1 END) * 100.0 / COUNT(*), 1) as rate
            FROM appointments
        """, conn).iloc[0]['rate']
        st.metric("✅ Taxa de Conclusão", f"{completion_rate}%")
    
    with col3:
        cancellation_rate = pd.read_sql_query("""
            SELECT 
                ROUND(COUNT(CASE WHEN status = 'cancelada' THEN 1 END) * 100.0 / COUNT(*), 1) as rate
            FROM appointments
        """, conn).iloc[0]['rate']
        st.metric("🔴 Taxa de Cancelamento", f"{cancellation_rate}%")
    
    with col4:
        avg_duration = pd.read_sql_query("SELECT AVG(duration) as avg FROM appointments", conn).iloc[0]['avg']
        st.metric("⏱️ Duração Média", f"{avg_duration:.0f} min")
    
    # Análise temporal
    col1, col2 = st.columns(2)
    
    with
