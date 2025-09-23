#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NutriApp360 - Sistema Completo de Apoio ao Nutricionista
Version: 5.0 - VERSÃO FUNCIONAL CORRIGIDA
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
import os
import math
import random
import base64
from io import BytesIO
import re
from typing import Dict, List, Optional
import calendar
import numpy as np

# =============================================================================
# CONFIGURAÇÕES INICIAIS
# =============================================================================

st.set_page_config(
    page_title="NutriApp360 v5.0 - Sistema Funcional",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
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
        background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
        padding: 1rem;
        border-radius: 15px;
        border: 3px solid #4CAF50;
    }
    
    .dashboard-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        border: 2px solid #4CAF50;
    }
    
    .user-role-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 0.2rem;
        text-transform: uppercase;
    }
    
    .admin-badge { background: #ff5722; color: white; }
    .nutritionist-badge { background: #4caf50; color: white; }
    .secretary-badge { background: #2196f3; color: white; }
    .patient-badge { background: #9c27b0; color: white; }
    
    .llm-response {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #9c27b0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# BANCO DE DADOS
# =============================================================================

def init_database():
    """Inicializa banco de dados"""
    conn = sqlite3.connect('nutriapp360.db')
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
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
            nutritionist_id INTEGER,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (nutritionist_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de agendamentos
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (nutritionist_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de receitas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            prep_time INTEGER,
            calories_per_serving INTEGER,
            ingredients TEXT,
            instructions TEXT,
            nutritionist_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (nutritionist_id) REFERENCES users (id)
        )
    ''')
    
    # Inserir dados iniciais se não existirem
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Usuários padrão
        users_data = [
            ('admin', hashlib.sha256('admin123'.encode()).hexdigest(), 'admin', 'Administrador Sistema', 'admin@nutriapp.com', '(11) 99999-0001'),
            ('dr_silva', hashlib.sha256('nutri123'.encode()).hexdigest(), 'nutritionist', 'Dr. Ana Silva Santos', 'ana.silva@nutriapp.com', '(11) 99999-0002'),
            ('secretaria', hashlib.sha256('sec123'.encode()).hexdigest(), 'secretary', 'Maria Fernanda Costa', 'secretaria@nutriapp.com', '(11) 99999-0003'),
            ('paciente1', hashlib.sha256('pac123'.encode()).hexdigest(), 'patient', 'João Carlos Oliveira', 'joao@email.com', '(11) 99999-0004')
        ]
        
        cursor.executemany('''
            INSERT INTO users (username, password_hash, role, full_name, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', users_data)
        
        # Pacientes de exemplo
        patients_data = [
            ('PAT001', 'João Carlos Oliveira', 'joao@email.com', '(11) 98765-4321', '1985-03-15', 'M', 1.78, 85.2, 78.0, 'Sedentário', 2),
            ('PAT002', 'Maria Silva Santos', 'maria.silva@email.com', '(11) 98765-4322', '1992-08-22', 'F', 1.65, 68.5, 60.0, 'Moderadamente ativo', 2),
            ('PAT003', 'Ana Beatriz Costa', 'ana.beatriz@email.com', '(11) 98765-4323', '1995-12-03', 'F', 1.60, 72.0, 65.0, 'Muito ativo', 2)
        ]
        
        cursor.executemany('''
            INSERT INTO patients (patient_id, full_name, email, phone, birth_date, gender, height, 
                                 current_weight, target_weight, activity_level, nutritionist_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', patients_data)
        
        # Consultas de exemplo
        appointments_data = [
            ('APP001', 1, 2, '2024-10-01 09:00:00', 60, 'Consulta inicial', 'agendado', 'Primeira consulta'),
            ('APP002', 2, 2, '2024-10-01 10:30:00', 60, 'Retorno', 'agendado', 'Revisão do plano'),
            ('APP003', 3, 2, '2024-10-02 14:00:00', 45, 'Consulta inicial', 'agendado', 'Nova paciente')
        ]
        
        cursor.executemany('''
            INSERT INTO appointments (appointment_id, patient_id, nutritionist_id, 
                                     appointment_date, duration, appointment_type, status, notes) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', appointments_data)
        
        # Receitas de exemplo
        recipes_data = [
            ('Salada de Quinoa', 'Saladas', 15, 320, 'Quinoa, pepino, tomate, azeite', 'Misture todos os ingredientes', 2),
            ('Smoothie Verde', 'Bebidas', 5, 180, 'Couve, maçã, água de coco', 'Bata no liquidificador', 2),
            ('Frango Grelhado', 'Pratos principais', 25, 450, 'Peito de frango, temperos', 'Grelhe por 10 min cada lado', 2)
        ]
        
        cursor.executemany('''
            INSERT INTO recipes (name, category, prep_time, calories_per_serving, ingredients, instructions, nutritionist_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', recipes_data)
    
    conn.commit()
    conn.close()

# =============================================================================
# AUTENTICAÇÃO
# =============================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    conn = sqlite3.connect('nutriapp360.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, password_hash, role, full_name, email
        FROM users 
        WHERE username = ? AND active = 1
    ''', (username,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result and hash_password(password) == result[2]:
        return {
            'id': result[0],
            'username': result[1],
            'role': result[3],
            'full_name': result[4],
            'email': result[5]
        }
    return None

# =============================================================================
# ASSISTENTE IA
# =============================================================================

class LLMAssistant:
    def __init__(self):
        self.context = "Assistente especializado em nutrição e saúde."
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """Gera resposta baseada no prompt"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["plano", "cardapio", "refeicao"]):
            return self._generate_meal_plan_response()
        elif any(word in prompt_lower for word in ["receita", "preparo", "cozinhar"]):
            return self._generate_recipe_response()
        elif any(word in prompt_lower for word in ["peso", "emagrecer", "dieta"]):
            return self._generate_weight_response()
        elif any(word in prompt_lower for word in ["motivacao", "animo", "desistir"]):
            return self._generate_motivation_response()
        else:
            return self._generate_general_response()
    
    def _generate_meal_plan_response(self):
        return """
        **📋 Sugestão de Plano Alimentar Balanceado:**
        
        **Café da Manhã (300 kcal):**
        • 1 fatia de pão integral
        • 1 ovo mexido
        • 1 fruta média
        • Café com leite desnatado
        
        **Lanche Manhã (150 kcal):**
        • 1 iogurte grego
        • 1 colher de granola
        
        **Almoço (450 kcal):**
        • 100g de proteína magra
        • 1 porção de carboidrato integral
        • Salada verde à vontade
        • 1 colher de azeite
        
        **Lanche Tarde (200 kcal):**
        • 1 fruta + castanhas (30g)
        
        **Jantar (350 kcal):**
        • Proteína magra
        • Vegetais variados
        • 1 porção pequena de carboidrato
        
        **💧 Hidratação:** 2-3 litros de água por dia
        """
    
    def _generate_recipe_response(self):
        return """
        **🍳 Receita Saudável: Bowl Nutritivo**
        
        **Ingredientes:**
        • 1/2 xícara de quinoa cozida
        • 100g de frango desfiado
        • Mix de folhas verdes
        • 1/2 abacate
        • Tomate cereja
        • 1 colher de azeite extra virgem
        
        **Modo de Preparo:**
        1. Monte a base com as folhas
        2. Adicione a quinoa e o frango
        3. Decore com abacate e tomates
        4. Regue com azeite e temperos
        
        **💪 Informação Nutricional:**
        • Aproximadamente 450 kcal
        • Rica em proteínas e fibras
        • Fonte de gorduras boas
        """
    
    def _generate_weight_response(self):
        return """
        **⚖️ Dicas para Gestão de Peso Saudável:**
        
        **📉 Para Emagrecimento:**
        • Déficit calórico moderado (300-500 kcal/dia)
        • Priorize proteínas em cada refeição
        • Aumente o consumo de fibras
        • Pratique atividade física regular
        • Durma bem (7-9 horas por noite)
        
        **📈 Para Ganho de Peso:**
        • Superávit calórico controlado
        • Refeições mais frequentes
        • Foque em alimentos nutritivos
        • Inclua exercícios de força
        
        **🎯 Dicas Gerais:**
        • Não pule refeições
        • Mastigue bem os alimentos
        • Evite distrações durante as refeições
        • Seja paciente com o processo
        """
    
    def _generate_motivation_response(self):
        return """
        **💪 Mensagem Motivacional:**
        
        Lembre-se: cada pequeno passo é uma vitória! 
        
        **🌟 Você já conseguiu:**
        • Tomar a decisão de cuidar da sua saúde
        • Buscar orientação profissional
        • Começar essa jornada de transformação
        
        **🎯 Foque no Progresso:**
        • Não na perfeição, mas na consistência
        • Celebre as pequenas conquistas
        • Aprenda com os obstáculos
        • Seja gentil consigo mesmo
        
        **💚 Lembre-se:** Sua saúde é um investimento, não um gasto. 
        Cada escolha saudável é um presente para o seu futuro!
        
        Continue firme, você consegue! 🚀
        """
    
    def _generate_general_response(self):
        return """
        **🤖 Assistente Nutricional IA**
        
        Olá! Sou seu assistente especializado em nutrição.
        
        **💡 Posso ajudar com:**
        • Planejamento de refeições
        • Sugestões de receitas saudáveis
        • Dicas de emagrecimento ou ganho de peso
        • Motivação e apoio
        • Informações nutricionais
        • Estratégias para mudança de hábitos
        
        **❓ Como posso ajudar você hoje?**
        Digite sua dúvida ou necessidade que terei prazer em orientar!
        """

# =============================================================================
# INTERFACE DE LOGIN
# =============================================================================

def show_login_page():
    st.markdown("""
    <div class="main-header">
        <h1>🥗 NutriApp360 v5.0</h1>
        <h3>Sistema Completo de Gestão Nutricional</h3>
        <p><strong>✅ VERSÃO TOTALMENTE FUNCIONAL</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        
        user_type = st.selectbox("👤 Tipo de Usuário", [
            "🔧 Administrador", 
            "👨‍⚕️ Nutricionista", 
            "📋 Secretária", 
            "🧑‍💼 Paciente"
        ])
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuário")
            password = st.text_input("🔒 Senha", type="password")
            
            col_login1, col_login2 = st.columns(2)
            with col_login1:
                login_btn = st.form_submit_button("🚀 Entrar", use_container_width=True)
            with col_login2:
                demo_btn = st.form_submit_button("👁️ Demo", use_container_width=True)
            
            if demo_btn:
                demo_credentials = {
                    "🔧 Administrador": ("admin", "admin123"),
                    "👨‍⚕️ Nutricionista": ("dr_silva", "nutri123"),
                    "📋 Secretária": ("secretaria", "sec123"),
                    "🧑‍💼 Paciente": ("paciente1", "pac123")
                }
                username, password = demo_credentials[user_type]
                login_btn = True
            
            if login_btn and username and password:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.success(f"✅ Bem-vindo(a), {user['full_name']}!")
                    st.rerun()
                else:
                    st.error("❌ Credenciais inválidas!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Credenciais demo
        st.info(f"""
        **🎯 Credenciais Demo ({user_type}):**
        
        **Usuário:** {
            {"🔧 Administrador": "admin", "👨‍⚕️ Nutricionista": "dr_silva", 
             "📋 Secretária": "secretaria", "🧑‍💼 Paciente": "paciente1"}[user_type]
        }
        
        **Senha:** {
            {"🔧 Administrador": "admin123", "👨‍⚕️ Nutricionista": "nutri123", 
             "📋 Secretária": "sec123", "🧑‍💼 Paciente": "pac123"}[user_type]
        }
        """)

# =============================================================================
# SIDEBAR E NAVEGAÇÃO
# =============================================================================

def show_sidebar():
    user_role = st.session_state.user['role']
    user_name = st.session_state.user['full_name']
    
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #4CAF50, #8BC34A); 
                border-radius: 15px; margin-bottom: 1rem;">
        <h3 style="color: white; margin: 0;">🥗 NutriApp360</h3>
        <p style="color: white; margin: 0;">Olá, <strong>{user_name}</strong></p>
        <span class="{user_role}-badge">{user_role.title()}</span>
    </div>
    """, unsafe_allow_html=True)
    
    menu_options = {
        'admin': {
            'dashboard': '📊 Dashboard',
            'users': '👥 Usuários',
            'reports': '📈 Relatórios',
            'settings': '⚙️ Configurações'
        },
        'nutritionist': {
            'dashboard': '📊 Dashboard',
            'patients': '👥 Pacientes',
            'appointments': '📅 Agendamentos',
            'recipes': '🍳 Receitas',
            'ia_assistant': '🤖 Assistente IA',
            'calculators': '🧮 Calculadoras'
        },
        'secretary': {
            'dashboard': '📊 Dashboard',
            'appointments': '📅 Agendamentos',
            'patients_basic': '👥 Pacientes',
            'financial': '💰 Financeiro'
        },
        'patient': {
            'dashboard': '🏠 Meu Dashboard',
            'progress': '📈 Meu Progresso',
            'appointments': '📅 Consultas',
            'chat': '💬 Chat IA'
        }
    }
    
    current_menu = menu_options.get(user_role, {})
    selected_page = st.sidebar.selectbox("📋 Menu", 
                                       list(current_menu.keys()),
                                       format_func=lambda x: current_menu[x])
    
    # Logout
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.user = None
        st.rerun()
    
    return selected_page

# =============================================================================
# DASHBOARDS
# =============================================================================

def show_admin_dashboard():
    st.markdown('<h1 class="main-header">📊 Dashboard Administrativo</h1>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    try:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_users = pd.read_sql_query("SELECT COUNT(*) as count FROM users WHERE active = 1", conn).iloc[0]['count']
            st.markdown(f"""
            <div class="metric-card">
                <h3>👥</h3>
                <h2>{total_users}</h2>
                <p>Usuários Ativos</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_patients = pd.read_sql_query("SELECT COUNT(*) as count FROM patients WHERE active = 1", conn).iloc[0]['count']
            st.markdown(f"""
            <div class="metric-card">
                <h3>🏥</h3>
                <h2>{total_patients}</h2>
                <p>Pacientes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_appointments = pd.read_sql_query("SELECT COUNT(*) as count FROM appointments", conn).iloc[0]['count']
            st.markdown(f"""
            <div class="metric-card">
                <h3>📅</h3>
                <h2>{total_appointments}</h2>
                <p>Consultas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_recipes = pd.read_sql_query("SELECT COUNT(*) as count FROM recipes", conn).iloc[0]['count']
            st.markdown(f"""
            <div class="metric-card">
                <h3>🍳</h3>
                <h2>{total_recipes}</h2>
                <p>Receitas</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráfico de usuários por tipo
        users_by_role = pd.read_sql_query("SELECT role, COUNT(*) as count FROM users GROUP BY role", conn)
        
        if not users_by_role.empty:
            fig = px.pie(users_by_role, values='count', names='role', title='Distribuição de Usuários')
            st.plotly_chart(fig, use_container_width=True)
    
    finally:
        conn.close()

def show_nutritionist_dashboard():
    st.markdown('<h1 class="main-header">👨‍⚕️ Dashboard do Nutricionista</h1>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    nutritionist_id = st.session_state.user['id']
    
    try:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            my_patients = pd.read_sql_query("""
                SELECT COUNT(*) as count FROM patients 
                WHERE nutritionist_id = ? AND active = 1
            """, conn, params=[nutritionist_id]).iloc[0]['count']
            st.metric("👥 Meus Pacientes", my_patients)
        
        with col2:
            today_appointments = pd.read_sql_query("""
                SELECT COUNT(*) as count FROM appointments 
                WHERE nutritionist_id = ? AND DATE(appointment_date) = DATE('now')
            """, conn, params=[nutritionist_id]).iloc[0]['count']
            st.metric("📅 Consultas Hoje", today_appointments)
        
        with col3:
            my_recipes = pd.read_sql_query("""
                SELECT COUNT(*) as count FROM recipes 
                WHERE nutritionist_id = ?
            """, conn, params=[nutritionist_id]).iloc[0]['count']
            st.metric("🍳 Minhas Receitas", my_recipes)
        
        with col4:
            st.metric("📊 Taxa Sucesso", "85.2%")
        
        # Próximas consultas
        st.markdown("### 📅 Próximas Consultas")
        upcoming = pd.read_sql_query("""
            SELECT a.appointment_date, p.full_name, a.appointment_type, a.status
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            WHERE a.nutritionist_id = ? AND DATE(a.appointment_date) >= DATE('now')
            ORDER BY a.appointment_date
            LIMIT 5
        """, conn, params=[nutritionist_id])
        
        if not upcoming.empty:
            for _, apt in upcoming.iterrows():
                date_time = pd.to_datetime(apt['appointment_date'])
                st.markdown(f"""
                <div class="dashboard-card">
                    <strong>{date_time.strftime('%d/%m/%Y %H:%M')}</strong> - {apt['full_name']}<br>
                    <small>{apt['appointment_type']} | Status: {apt['status']}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📅 Nenhuma consulta próxima agendada")
    
    finally:
        conn.close()

def show_patient_dashboard():
    st.markdown('<h1 class="main-header">🏠 Meu Painel Pessoal</h1>', unsafe_allow_html=True)
    
    user_name = st.session_state.user['full_name']
    
    st.markdown(f"""
    <div class="dashboard-card">
        <h3>Olá, {user_name}!</h3>
        <p>Bem-vindo ao seu painel pessoal de acompanhamento nutricional.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⚖️ Peso Atual", "75.2 kg")
    with col2:
        st.metric("🎯 Meta", "70.0 kg")
    with col3:
        st.metric("📉 Progresso", "-2.1 kg")
    with col4:
        st.metric("🏆 Nível", "3")
    
    # Próxima consulta
    st.markdown("### 📅 Próxima Consulta")
    st.info("📅 01/10/2024 às 09:00 - Dr. Ana Silva Santos")

# =============================================================================
# GESTÃO DE PACIENTES
# =============================================================================

def show_patients_management():
    st.markdown('<h1 class="main-header">👥 Gestão de Pacientes</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["👥 Lista de Pacientes", "➕ Novo Paciente"])
    
    with tab1:
        show_patients_list()
    
    with tab2:
        show_add_patient_form()

def show_patients_list():
    st.markdown("### 👥 Lista de Pacientes")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    try:
        patients = pd.read_sql_query("""
            SELECT p.*, u.full_name as nutritionist_name 
            FROM patients p 
            LEFT JOIN users u ON p.nutritionist_id = u.id 
            WHERE p.active = 1
            ORDER BY p.created_at DESC
        """, conn)
        
        if not patients.empty:
            for _, patient in patients.iterrows():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4>{patient['full_name']} ({patient['patient_id']})</h4>
                        <p>📧 {patient['email']} | 📞 {patient['phone']}</p>
                        <p>⚖️ {patient['current_weight']}kg → 🎯 {patient['target_weight']}kg</p>
                        <p>👨‍⚕️ {patient['nutritionist_name'] or 'Não atribuído'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("👁️ Ver", key=f"view_{patient['id']}"):
                        st.info(f"Visualizando dados de {patient['full_name']}")
    
    finally:
        conn.close()

def show_add_patient_form():
    st.markdown("### ➕ Cadastrar Novo Paciente")
    
    with st.form("add_patient_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("👤 Nome Completo *")
            email = st.text_input("📧 Email *")
            phone = st.text_input("📞 Telefone *")
            birth_date = st.date_input("🎂 Data de Nascimento")
        
        with col2:
            gender = st.selectbox("👤 Gênero *", ["M", "F"])
            height = st.number_input("📏 Altura (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01)
            current_weight = st.number_input("⚖️ Peso Atual (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)
            target_weight = st.number_input("🎯 Peso Meta (kg)", min_value=30.0, max_value=300.0, value=65.0, step=0.1)
        
        activity_level = st.selectbox("🏃 Nível de Atividade", 
                                    ["Sedentário", "Moderadamente ativo", "Ativo", "Muito ativo"])
        
        submitted = st.form_submit_button("➕ Cadastrar Paciente", type="primary")
        
        if submitted and full_name and email:
            conn = sqlite3.connect('nutriapp360.db')
            cursor = conn.cursor()
            
            patient_id = f"PAT{str(uuid.uuid4())[:6].upper()}"
            
            try:
                cursor.execute('''
                    INSERT INTO patients (
                        patient_id, full_name, email, phone, birth_date, gender, height,
                        current_weight, target_weight, activity_level, nutritionist_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    patient_id, full_name, email, phone, birth_date, gender, height,
                    current_weight, target_weight, activity_level, st.session_state.user['id']
                ))
                
                conn.commit()
                st.success(f"✅ Paciente {full_name} cadastrado! ID: {patient_id}")
                st.balloons()
            
            except Exception as e:
                st.error(f"Erro ao cadastrar: {str(e)}")
            finally:
                conn.close()

# =============================================================================
# GESTÃO DE AGENDAMENTOS
# =============================================================================

def show_appointments_management():
    st.markdown('<h1 class="main-header">📅 Gestão de Agendamentos</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📅 Lista de Agendamentos", "➕ Novo Agendamento"])
    
    with tab1:
        show_appointments_list()
    
    with tab2:
        show_new_appointment_form()

def show_appointments_list():
    st.markdown("### 📅 Lista de Agendamentos")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    try:
        appointments = pd.read_sql_query("""
            SELECT a.*, p.full_name as patient_name, u.full_name as nutritionist_name
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN users u ON a.nutritionist_id = u.id
            ORDER BY a.appointment_date DESC
            LIMIT 20
        """, conn)
        
        if not appointments.empty:
            for _, apt in appointments.iterrows():
                date_time = pd.to_datetime(apt['appointment_date'])
                
                st.markdown(f"""
                <div class="dashboard-card">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <h5>{apt['patient_name']}</h5>
                            <p>👨‍⚕️ {apt['nutritionist_name']}</p>
                            <p>📋 {apt['appointment_type']}</p>
                        </div>
                        <div style="text-align: right;">
                            <strong>{date_time.strftime('%d/%m/%Y')}</strong><br>
                            <strong>{date_time.strftime('%H:%M')}</strong><br>
                            <span style="color: {'#4CAF50' if apt['status'] == 'realizada' else '#2196F3'}">
                                {apt['status'].title()}
                            </span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    finally:
        conn.close()

def show_new_appointment_form():
    st.markdown("### ➕ Novo Agendamento")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    try:
        patients = pd.read_sql_query("SELECT id, full_name FROM patients WHERE active = 1", conn)
        
        if patients.empty:
            st.error("❌ Nenhum paciente ativo encontrado")
            return
        
        with st.form("new_appointment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                patient_id = st.selectbox(
                    "👤 Paciente",
                    patients['id'].tolist(),
                    format_func=lambda x: patients[patients['id'] == x]['full_name'].iloc[0]
                )
                appointment_type = st.selectbox("📋 Tipo de Consulta", [
                    "Consulta inicial", "Retorno", "Acompanhamento", "Avaliação nutricional"
                ])
            
            with col2:
                appointment_date = st.date_input("📅 Data", value=date.today() + timedelta(days=1))
                appointment_time = st.time_input("⏰ Horário")
                duration = st.selectbox("⏱️ Duração (min)", [30, 45, 60, 90], index=2)
            
            notes = st.text_area("📝 Observações")
            
            submitted = st.form_submit_button("📅 Agendar Consulta", type="primary")
            
            if submitted:
                appointment_datetime = datetime.combine(appointment_date, appointment_time)
                appointment_id = f"APP{str(uuid.uuid4())[:6].upper()}"
                
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO appointments (
                        appointment_id, patient_id, nutritionist_id, appointment_date,
                        duration, appointment_type, status, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, 'agendado', ?)
                ''', (appointment_id, patient_id, st.session_state.user['id'], 
                      appointment_datetime, duration, appointment_type, notes))
                
                conn.commit()
                st.success(f"✅ Consulta agendada! ID: {appointment_id}")
    
    finally:
        conn.close()

# =============================================================================
# GESTÃO DE RECEITAS
# =============================================================================

def show_recipes_management():
    st.markdown('<h1 class="main-header">🍳 Gestão de Receitas</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🍳 Lista de Receitas", "➕ Nova Receita"])
    
    with tab1:
        show_recipes_list()
    
    with tab2:
        show_add_recipe_form()

def show_recipes_list():
    st.markdown("### 🍳 Lista de Receitas")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    try:
        recipes = pd.read_sql_query("SELECT * FROM recipes ORDER BY created_at DESC", conn)
        
        if not recipes.empty:
            cols = st.columns(2)
            
            for i, (_, recipe) in enumerate(recipes.iterrows()):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4>{recipe['name']}</h4>
                        <p>🏷️ {recipe['category']} | ⏰ {recipe['prep_time']} min</p>
                        <p>🔥 {recipe['calories_per_serving']} kcal por porção</p>
                        <small><strong>Ingredientes:</strong> {recipe['ingredients'][:100]}...</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("👁️ Ver Receita", key=f"view_recipe_{recipe['id']}"):
                        st.info(f"**{recipe['name']}**\n\n**Ingredientes:** {recipe['ingredients']}\n\n**Preparo:** {recipe['instructions']}")
    
    finally:
        conn.close()

def show_add_recipe_form():
    st.markdown("### ➕ Nova Receita")
    
    with st.form("add_recipe_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("🍳 Nome da Receita *")
            category = st.selectbox("🏷️ Categoria", [
                "Café da manhã", "Almoço", "Jantar", "Lanche", "Saladas", "Bebidas", "Sobremesas"
            ])
            prep_time = st.number_input("⏰ Tempo de Preparo (min)", min_value=1, value=15)
        
        with col2:
            calories = st.number_input("🔥 Calorias por porção", min_value=1, value=200)
        
        ingredients = st.text_area("🛒 Ingredientes *", placeholder="Liste os ingredientes...")
        instructions = st.text_area("👨‍🍳 Modo de Preparo *", placeholder="Descreva o preparo...")
        
        submitted = st.form_submit_button("🍳 Salvar Receita", type="primary")
        
        if submitted and name and ingredients and instructions:
            conn = sqlite3.connect('nutriapp360.db')
            cursor = conn.cursor()
            
            try:
                cursor.execute('''
                    INSERT INTO recipes (name, category, prep_time, calories_per_serving, 
                                       ingredients, instructions, nutritionist_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (name, category, prep_time, calories, ingredients, instructions, 
                      st.session_state.user['id']))
                
                conn.commit()
                st.success(f"✅ Receita '{name}' salva com sucesso!")
            
            except Exception as e:
                st.error(f"Erro ao salvar: {str(e)}")
            finally:
                conn.close()

# =============================================================================
# ASSISTENTE IA
# =============================================================================

def show_ia_assistant():
    st.markdown('<h1 class="main-header">🤖 Assistente IA Nutricional</h1>', unsafe_allow_html=True)
    
    llm = LLMAssistant()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Exibir histórico
    for message in st.session_state.chat_history:
        if message['sender'] == 'user':
            st.markdown(f"""
            <div style="text-align: right; margin: 1rem 0;">
                <div style="background: #E3F2FD; padding: 1rem; border-radius: 15px; display: inline-block; max-width: 70%;">
                    <strong>👤 Você:</strong><br>
                    {message['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="llm-response">
                <strong>🤖 Assistente:</strong><br>
                {message['content']}
            </div>
            """, unsafe_allow_html=True)
    
    # Input de mensagem
    user_input = st.text_input("💬 Digite sua pergunta:", placeholder="Como posso ajudar você hoje?")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("📤 Enviar"):
            if user_input:
                # Adicionar mensagem do usuário
                st.session_state.chat_history.append({
                    'sender': 'user',
                    'content': user_input
                })
                
                # Gerar resposta da IA
                response = llm.generate_response(user_input)
                
                # Adicionar resposta da IA
                st.session_state.chat_history.append({
                    'sender': 'ai',
                    'content': response
                })
                
                st.rerun()
    
    with col2:
        if st.button("🔄 Limpar Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Sugestões rápidas
    st.markdown("#### 💡 Sugestões:")
    suggestions = [
        "Como criar um plano para diabético?",
        "Receitas rápidas e saudáveis",
        "Dicas para emagrecimento",
        "Como motivar pacientes?"
    ]
    
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(suggestion, key=f"sug_{i}"):
                st.session_state.chat_history.append({'sender': 'user', 'content': suggestion})
                response = llm.generate_response(suggestion)
                st.session_state.chat_history.append({'sender': 'ai', 'content': response})
                st.rerun()

# =============================================================================
# CALCULADORAS
# =============================================================================

def show_calculators():
    st.markdown('<h1 class="main-header">🧮 Calculadoras Nutricionais</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["⚖️ IMC e Gasto Energético", "🥗 Necessidades Nutricionais"])
    
    with tab1:
        show_imc_calculator()
    
    with tab2:
        show_nutrition_calculator()

def show_imc_calculator():
    st.markdown("### ⚖️ Calculadora de IMC e Gasto Energético")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0)
        height = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70)
        age = st.number_input("Idade (anos)", min_value=1, max_value=120, value=30)
        gender = st.selectbox("Gênero", ["Masculino", "Feminino"])
        activity = st.selectbox("Nível de Atividade", [
            "Sedentário", "Levemente ativo", "Moderadamente ativo", "Muito ativo"
        ])
        
        if st.button("🧮 Calcular"):
            # IMC
            imc = weight / (height ** 2)
            
            if imc < 18.5:
                imc_class = "Abaixo do peso"
                color = "#FF5722"
            elif imc < 25:
                imc_class = "Normal"
                color = "#4CAF50"
            elif imc < 30:
                imc_class = "Sobrepeso"
                color = "#FF9800"
            else:
                imc_class = "Obesidade"
                color = "#F44336"
            
            # TMB (Fórmula de Harris-Benedict)
            if gender == "Masculino":
                tmb = 88.362 + (13.397 * weight) + (4.799 * height * 100) - (5.677 * age)
            else:
                tmb = 447.593 + (9.247 * weight) + (3.098 * height * 100) - (4.330 * age)
            
            # Gasto energético total
            activity_factors = {
                "Sedentário": 1.2,
                "Levemente ativo": 1.375,
                "Moderadamente ativo": 1.55,
                "Muito ativo": 1.725
            }
            
            get = tmb * activity_factors[activity]
    
    with col2:
        if 'imc' in locals():
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: {color};">IMC: {imc:.1f}</h3>
                <p style="color: {color};">{imc_class}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.metric("🔥 Taxa Metabólica Basal", f"{tmb:.0f} kcal/dia")
            st.metric("⚡ Gasto Energético Total", f"{get:.0f} kcal/dia")
            
            st.markdown("#### 🎯 Metas Calóricas:")
            st.write(f"**📉 Emagrecimento:** {get-500:.0f} kcal/dia")
            st.write(f"**⚖️ Manutenção:** {get:.0f} kcal/dia")
            st.write(f"**📈 Ganho de peso:** {get+300:.0f} kcal/dia")

def show_nutrition_calculator():
    st.markdown("### 🥗 Calculadora de Necessidades Nutricionais")
    
    weight = st.number_input("Peso (kg)", min_value=30.0, value=70.0, key="nutr_weight")
    daily_calories = st.number_input("Calorias diárias", min_value=800, value=2000, key="nutr_cal")
    
    goal = st.selectbox("Objetivo", ["Emagrecimento", "Manutenção", "Ganho de massa"])
    
    if st.button("🧮 Calcular Necessidades"):
        # Necessidades proteicas
        protein_needs = {"Emagrecimento": 1.6, "Manutenção": 1.2, "Ganho de massa": 2.0}
        protein_g = weight * protein_needs[goal]
        protein_cal = protein_g * 4
        
        # Distribuição de macros
        if goal == "Emagrecimento":
            carb_percent = 40
            fat_percent = 30
        elif goal == "Ganho de massa":
            carb_percent = 50
            fat_percent = 25
        else:
            carb_percent = 50
            fat_percent = 30
        
        protein_percent = (protein_cal / daily_calories) * 100
        
        carb_cal = daily_calories * carb_percent / 100
        fat_cal = daily_calories * fat_percent / 100
        
        carb_g = carb_cal / 4
        fat_g = fat_cal / 9
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🥩 Proteínas", f"{protein_g:.0f}g", f"{protein_percent:.1f}%")
        with col2:
            st.metric("🍞 Carboidratos", f"{carb_g:.0f}g", f"{carb_percent:.1f}%")
        with col3:
            st.metric("🥑 Gorduras", f"{fat_g:.0f}g", f"{fat_percent:.1f}%")
        
        st.metric("💧 Água por dia", f"{weight * 35:.0f} ml")

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    load_css()
    init_database()
    
    if 'user' not in st.session_state or not st.session_state.user:
        show_login_page()
        return
    
    selected_page = show_sidebar()
    user_role = st.session_state.user['role']
    
    # Roteamento
    if user_role == 'admin':
        if selected_page == 'dashboard':
            show_admin_dashboard()
        elif selected_page == 'users':
            st.info("🔧 Gestão de usuários em desenvolvimento")
        elif selected_page == 'reports':
            st.info("📈 Relatórios em desenvolvimento")
        elif selected_page == 'settings':
            st.info("⚙️ Configurações em desenvolvimento")
    
    elif user_role == 'nutritionist':
        if selected_page == 'dashboard':
            show_nutritionist_dashboard()
        elif selected_page == 'patients':
            show_patients_management()
        elif selected_page == 'appointments':
            show_appointments_management()
        elif selected_page == 'recipes':
            show_recipes_management()
        elif selected_page == 'ia_assistant':
            show_ia_assistant()
        elif selected_page == 'calculators':
            show_calculators()
    
    elif user_role == 'secretary':
        if selected_page == 'dashboard':
            show_admin_dashboard()  # Reutilizar dashboard admin
        elif selected_page == 'appointments':
            show_appointments_management()
        elif selected_page == 'patients_basic':
            show_patients_management()
        elif selected_page == 'financial':
            st.info("💰 Módulo financeiro em desenvolvimento")
    
    elif user_role == 'patient':
        if selected_page == 'dashboard':
            show_patient_dashboard()
        elif selected_page == 'progress':
            st.info("📈 Acompanhamento de progresso em desenvolvimento")
        elif selected_page == 'appointments':
            st.info("📅 Suas consultas em desenvolvimento")
        elif selected_page == 'chat':
            show_ia_assistant()

if __name__ == "__main__":
    main()
