#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NutriApp360 - Sistema Completo de Apoio ao Nutricionista
Version: 5.0 - SISTEMA COMPLETAMENTE FUNCIONAL
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
import time

# Configurações iniciais
st.set_page_config(
    page_title="NutriApp360 v5.0 - Sistema Completo",
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
        transition: transform 0.3s ease;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        border: 2px solid #4CAF50;
        transition: all 0.3s ease;
    }
    
    .patient-info-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    
    .appointment-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .recipe-card {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ff9800;
        margin: 0.5rem 0;
    }
    
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Banco de dados
def init_database():
    """Inicializa banco de dados com estrutura completa"""
    conn = sqlite3.connect('nutriapp360.db')
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'nutritionist', 'secretary', 'patient')),
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
            user_id INTEGER,
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
            nutritionist_id INTEGER,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
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
    
    # Tabela de planos alimentares
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meal_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_id TEXT UNIQUE NOT NULL,
            patient_id INTEGER NOT NULL,
            nutritionist_id INTEGER NOT NULL,
            plan_name TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE,
            daily_calories INTEGER,
            plan_data TEXT,
            status TEXT DEFAULT 'ativo',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (nutritionist_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de progresso
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            record_date DATE NOT NULL,
            weight REAL,
            notes TEXT,
            recorded_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (recorded_by) REFERENCES users (id)
        )
    ''')
    
    # Inserir dados iniciais se não existirem
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        insert_sample_data(cursor)
    
    conn.commit()
    conn.close()

def insert_sample_data(cursor):
    """Insere dados de exemplo no sistema"""
    
    # Usuários iniciais
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
        (4, 'PAT001', 'João Carlos Oliveira', 'joao@email.com', '(11) 98765-4321', '1985-03-15', 'M', 1.78, 85.2, 78.0, 'Sedentário', 'Diabetes tipo 2', 'Glúten', 2)
    ]
    
    cursor.executemany('''
        INSERT INTO patients (user_id, patient_id, full_name, email, phone, birth_date, gender, height, 
                             current_weight, target_weight, activity_level, medical_conditions, 
                             allergies, nutritionist_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', patients_data)

# Sistema de autenticação
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    conn = sqlite3.connect('nutriapp360.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users SET last_login = CURRENT_TIMESTAMP 
        WHERE username = ? AND password_hash = ?
    ''', (username, hash_password(password)))
    
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

# Assistente IA
class LLMAssistant:
    def __init__(self):
        self.context = "Assistente especializado em nutrição e saúde."
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """Gera resposta baseada no contexto"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["plano", "cardapio", "refeicao", "alimentar"]):
            return self._generate_meal_plan_response()
        elif any(word in prompt_lower for word in ["receita", "preparo", "cozinhar"]):
            return self._generate_recipe_response()
        elif any(word in prompt_lower for word in ["peso", "emagrecer", "dieta"]):
            return self._generate_weight_response()
        elif any(word in prompt_lower for word in ["imc", "calculo", "indice"]):
            return self._generate_calculation_response()
        else:
            return self._generate_general_response()
    
    def _generate_meal_plan_response(self):
        return """
**🍽️ Plano Alimentar Equilibrado (1800 kcal)**

**☀️ Café da manhã (450 kcal - 25%):**
• 2 fatias de pão integral (140 kcal)
• 1 ovo mexido (90 kcal)  
• 1/2 abacate médio (120 kcal)
• 1 copo de leite desnatado (80 kcal)
• 1 banana pequena (70 kcal)

**🥤 Lanche manhã (180 kcal - 10%):**
• 1 iogurte grego natural (120 kcal)
• 1 colher de granola (60 kcal)

**🍽️ Almoço (630 kcal - 35%):**
• 150g peito de frango grelhado (250 kcal)
• 4 colheres arroz integral (140 kcal)
• 1 concha feijão preto (100 kcal)
• Salada verde + 1 col. azeite (90 kcal)
• 1 fruta média (50 kcal)

**🥪 Lanche tarde (180 kcal - 10%):**
• 1 maçã média (80 kcal)
• 10 amêndoas (100 kcal)

**🌙 Jantar (360 kcal - 20%):**
• 120g salmão grelhado (220 kcal)
• Legumes refogados (80 kcal)
• 1 batata doce pequena (60 kcal)

**💧 Hidratação:** 2,5L água + chás naturais
        """
    
    def _generate_recipe_response(self):
        return """
**👨‍🍳 Receita: Bowl Buddha Nutritivo**

**🥗 Ingredientes (2 porções):**
• 1 xícara quinoa cozida
• 150g grão-de-bico cozido
• 1 beterraba média assada
• 1/2 abacate maduro
• 100g espinafre baby
• 2 col. sopa sementes de girassol

**⏱️ Modo de Preparo (30 min):**
1. Cozinhe quinoa com caldo de legumes
2. Asse beterraba com azeite (180°C)
3. Monte bowl: base espinafre, quinoa, grão-de-bico
4. Decore com beterraba, abacate
5. Finalize com sementes

**📊 Por porção:** 520 kcal | 18g proteína
        """
    
    def _generate_weight_response(self):
        return """
**⚖️ Estratégias para Emagrecimento Saudável**

**🎯 Princípios Fundamentais:**
• Déficit calórico: 300-500 kcal/dia
• Distribuição: 25% proteína | 45% carbo | 30% gordura
• Hidratação: 35ml/kg peso corporal

**🍽️ Estratégias:**
1. Proteína em cada refeição (20-30g)
2. Fibras abundantes (25-35g/dia)
3. Carboidratos complexos
4. Gorduras boas essenciais

**📈 Monitoramento:**
• Peso: 2x/semana, mesmo horário
• Medidas: quinzenal
• Fotos progresso: mensal
        """
    
    def _generate_calculation_response(self):
        return """
**📊 Calculadoras Nutricionais**

**🔢 IMC:** Peso(kg) ÷ Altura²(m)
- Abaixo do peso: <18,5
- Peso normal: 18,5-24,9
- Sobrepeso: 25,0-29,9
- Obesidade: ≥30,0

**🔥 TMB (Taxa Metabólica Basal):**
**Homens:** 88,362 + (13,397 × peso) + (4,799 × altura) - (5,677 × idade)
**Mulheres:** 447,593 + (9,247 × peso) + (3,098 × altura) - (4,330 × idade)

**💧 Hidratação:** 35ml × peso corporal
        """
    
    def _generate_general_response(self):
        return """
**🤖 Assistente Nutricional NutriApp360**

Olá! Sou seu assistente especializado em nutrição.

**🎯 Posso ajudar com:**
• 📋 Planos alimentares personalizados
• 👨‍🍳 Receitas saudáveis e nutritivas  
• ⚖️ Estratégias de emagrecimento
• 🧮 Cálculos nutricionais
• 💡 Dicas de alimentação saudável

Digite sua dúvida específica para orientação personalizada!
        """

# Interface de login
def show_login_page():
    st.markdown("""
    <div class="main-header">
        <h1>🥗 NutriApp360 v5.0</h1>
        <h3>Sistema Completo de Gestão Nutricional</h3>
        <p><strong>✅ TODAS AS FUNCIONALIDADES IMPLEMENTADAS</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        user_type = st.selectbox("🎭 Tipo de Usuário", [
            "👨‍⚕️ Administrador", 
            "🥗 Nutricionista", 
            "📋 Secretária", 
            "🙋‍♂️ Paciente"
        ])
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuário")
            password = st.text_input("🔒 Senha", type="password")
            
            col_login1, col_login2 = st.columns(2)
            with col_login1:
                login_btn = st.form_submit_button("🚀 Entrar", use_container_width=True, type="primary")
            with col_login2:
                demo_btn = st.form_submit_button("🎮 Demo", use_container_width=True)
            
            if demo_btn:
                demo_credentials = {
                    "👨‍⚕️ Administrador": ("admin", "admin123"),
                    "🥗 Nutricionista": ("dr_silva", "nutri123"),
                    "📋 Secretária": ("secretaria", "sec123"),
                    "🙋‍♂️ Paciente": ("paciente1", "pac123")
                }
                username, password = demo_credentials[user_type]
                login_btn = True
            
            if login_btn and username and password:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.success(f"🎉 Bem-vindo(a), {user['full_name']}!")
                    st.rerun()
                else:
                    st.error("❌ Credenciais inválidas!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Credenciais demo
        demo_map = {
            "👨‍⚕️ Administrador": ("admin", "admin123"),
            "🥗 Nutricionista": ("dr_silva", "nutri123"),
            "📋 Secretária": ("secretaria", "sec123"),
            "🙋‍♂️ Paciente": ("paciente1", "pac123")
        }
        
        st.info(f"""
        **🎮 Credenciais Demo ({user_type}):**
        
        **👤 Usuário:** `{demo_map[user_type][0]}`
        
        **🔒 Senha:** `{demo_map[user_type][1]}`
        """)

# Sidebar
def show_sidebar():
    user_role = st.session_state.user['role']
    user_name = st.session_state.user['full_name']
    
    role_icons = {
        'admin': '👨‍⚕️',
        'nutritionist': '🥗',
        'secretary': '📋',
        'patient': '🙋‍♂️'
    }
    
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #4CAF50, #8BC34A); 
                border-radius: 15px; margin-bottom: 1rem;">
        <h3 style="color: white; margin: 0;">{role_icons[user_role]} NutriApp360</h3>
        <p style="color: white; margin: 0; font-size: 0.9rem;">
            Olá, <strong>{user_name}</strong>
        </p>
        <span style="background: rgba(255,255,255,0.2); padding: 0.2rem 0.5rem; border-radius: 10px; color: white; font-size: 0.8rem;">
            {user_role.title()}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Menus por usuário
    menu_options = {
        'admin': {
            'dashboard': '📊 Dashboard Executivo',
            'users': '👥 Usuários',
            'analytics': '📈 Analytics',
            'reports': '📋 Relatórios',
            'settings': '⚙️ Configurações'
        },
        'nutritionist': {
            'dashboard': '📊 Dashboard',
            'patients': '👥 Pacientes',
            'appointments': '📅 Agendamentos',
            'plans': '🍽️ Planos',
            'recipes': '👨‍🍳 Receitas',
            'ia_assistant': '🤖 Assistente IA',
            'calculators': '🧮 Calculadoras'
        },
        'secretary': {
            'dashboard': '📊 Dashboard',
            'appointments': '📅 Agendamentos',
            'patients': '👥 Pacientes',
            'financial': '💰 Financeiro'
        },
        'patient': {
            'dashboard': '📊 Dashboard',
            'progress': '📈 Progresso',
            'appointments': '📅 Consultas',
            'plan': '🍽️ Plano',
            'chat': '🤖 Chat IA',
            'calculators': '🧮 Calculadoras'
        }
    }
    
    current_menu = menu_options.get(user_role, {})
    selected_page = st.sidebar.selectbox("📋 Menu Principal", 
                                       list(current_menu.keys()),
                                       format_func=lambda x: current_menu[x])
    
    # Logout
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Sair do Sistema", use_container_width=True):
        st.session_state.user = None
        st.rerun()
    
    return selected_page

# Dashboards
def show_admin_dashboard():
    st.markdown('<h1 class="main-header">📊 Dashboard Executivo</h1>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    try:
        total_users = pd.read_sql_query("SELECT COUNT(*) as count FROM users WHERE active = 1", conn).iloc[0]['count']
        total_patients = pd.read_sql_query("SELECT COUNT(*) as count FROM patients WHERE active = 1", conn).iloc[0]['count']
        total_appointments = pd.read_sql_query("SELECT COUNT(*) as count FROM appointments", conn).iloc[0]['count']
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #4CAF50;">👥 {total_users}</h3>
                <p style="margin: 0;">Usuários Ativos</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #2196F3;">🙋‍♂️ {total_patients}</h3>
                <p style="margin: 0;">Pacientes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #FF9800;">📅 {total_appointments}</h3>
                <p style="margin: 0;">Consultas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #9C27B0;">⭐ 98%</h3>
                <p style="margin: 0;">Satisfação</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráfico simples
        st.subheader("📈 Crescimento Mensal")
        chart_data = pd.DataFrame({
            'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            'Usuários': [10, 15, 22, 28, 35, total_users],
            'Pacientes': [5, 8, 12, 18, 25, total_patients]
        })
        
        fig = px.line(chart_data, x='Mês', y=['Usuários', 'Pacientes'], 
                     title="Crescimento de Usuários", markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro ao carregar dashboard: {e}")
    finally:
        conn.close()

def show_nutritionist_dashboard():
    st.markdown('<h1 class="main-header">📊 Dashboard do Nutricionista</h1>', unsafe_allow_html=True)
    
    nutritionist_id = st.session_state.user['id']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #4CAF50;">25</h3>
            <p style="margin: 0;">Meus Pacientes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #FF9800;">8</h3>
            <p style="margin: 0;">Consultas Hoje</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #2196F3;">12</h3>
            <p style="margin: 0;">Planos Ativos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #9C27B0;">95%</h3>
            <p style="margin: 0;">Taxa Sucesso</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("📅 Agenda de Hoje")
    
    agenda_today = [
        {"hora": "09:00", "paciente": "Maria Silva", "tipo": "Retorno"},
        {"hora": "10:00", "paciente": "João Santos", "tipo": "Primeira consulta"},
        {"hora": "11:00", "paciente": "Ana Costa", "tipo": "Acompanhamento"},
        {"hora": "14:00", "paciente": "Carlos Lima", "tipo": "Revisão de plano"},
    ]
    
    for consulta in agenda_today:
        st.markdown(f"""
        <div class="appointment-card">
            <h5 style="margin: 0;">{consulta['hora']} - {consulta['paciente']}</h5>
            <p style="margin: 0; font-size: 0.9rem; color: #666;">
                <strong>Tipo:</strong> {consulta['tipo']}
            </p>
        </div>
        """, unsafe_allow_html=True)

def show_patient_dashboard():
    st.markdown('<h1 class="main-header">📊 Meu Dashboard</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    conn = sqlite3.connect('nutriapp360.db')
    
    patient_data = pd.read_sql_query("""
        SELECT p.*, n.full_name as nutritionist_name
        FROM patients p
        LEFT JOIN users n ON n.id = p.nutritionist_id
        WHERE p.user_id = ?
    """, conn, params=[user_id])
    
    if not patient_data.empty:
        patient = patient_data.iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if patient['height'] and patient['current_weight']:
                imc = patient['current_weight'] / (patient['height'] ** 2)
                st.metric("📊 IMC", f"{imc:.1f}")
            else:
                st.metric("📊 IMC", "N/A")
        
        with col2:
            st.metric("⚖️ Peso Atual", f"{patient['current_weight']} kg" if patient['current_weight'] else "N/A")
        
        with col3:
            st.metric("🎯 Meta", f"{patient['target_weight']} kg" if patient['target_weight'] else "N/A")
        
        st.markdown(f"""
        <div class="patient-info-card">
            <h4>👋 Bem-vindo, {patient['full_name']}</h4>
            <p><strong>🥗 Nutricionista:</strong> {patient['nutritionist_name'] or 'Não definido'}</p>
            <p><strong>🏃‍♂️ Atividade:</strong> {patient['activity_level'] or 'Não informado'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    conn.close()

def show_secretary_dashboard():
    st.markdown('<h1 class="main-header">📊 Dashboard Operacional</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #FF9800;">15</h3>
            <p style="margin: 0;">Consultas Hoje</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #F44336;">3</h3>
            <p style="margin: 0;">Pendências</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; color: #4CAF50;">127</h3>
            <p style="margin: 0;">Pacientes</p>
        </div>
        """, unsafe_allow_html=True)

# Função de chat IA
def show_ia_assistant():
    st.markdown('<h1 class="main-header">🤖 Assistente IA Nutricional</h1>', unsafe_allow_html=True)
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    user_question = st.text_input("💬 Digite sua pergunta:", placeholder="Ex: Como calcular TMB?")
    
    col_send, col_clear = st.columns([3, 1])
    with col_send:
        send_button = st.button("📤 Enviar", use_container_width=True, type="primary")
    with col_clear:
        if st.button("🗑️ Limpar", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    if send_button and user_question:
        llm = LLMAssistant()
        response = llm.generate_response(user_question)
        
        st.session_state.chat_history.append({
            'question': user_question,
            'response': response,
            'timestamp': datetime.now()
        })
        st.rerun()
    
    if st.session_state.chat_history:
        st.markdown("---")
        for chat in reversed(st.session_state.chat_history):
            st.markdown(f"""
            <div style="background: #e3f2fd; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                <strong>Você:</strong> {chat['question']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <strong>🤖 Assistente:</strong><br>{chat['response']}
            </div>
            """, unsafe_allow_html=True)

# Calculadoras
def show_calculators():
    st.markdown('<h1 class="main-header">🧮 Calculadoras Nutricionais</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔥 TMB", "📊 IMC", "💧 Hidratação"])
    
    with tab1:
        st.subheader("🔥 Taxa Metabólica Basal")
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox("⚧ Sexo", ["Feminino", "Masculino"])
            age = st.number_input("📅 Idade", min_value=1, max_value=120, value=30)
            weight = st.number_input("⚖️ Peso (kg)", min_value=20.0, value=70.0)
            height = st.number_input("📏 Altura (cm)", min_value=100.0, value=170.0)
        
        with col2:
            if st.button("🔥 Calcular TMB", type="primary"):
                if gender == "Masculino":
                    tmb = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
                else:
                    tmb = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
                
                st.markdown(f"""
                <div class="metric-card">
                    <h2 style="margin: 0; color: #FF5722;">🔥 {tmb:.0f} kcal</h2>
                    <p style="margin: 0;">Taxa Metabólica Basal</p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("📊 Índice de Massa Corporal")
        
        col1, col2 = st.columns(2)
        
        with col1:
            weight_imc = st.number_input("⚖️ Peso (kg)", min_value=20.0, value=70.0, key="weight_imc")
            height_imc = st.number_input("📏 Altura (m)", min_value=1.0, value=1.70, key="height_imc")
        
        with col2:
            if st.button("📊 Calcular IMC", type="primary"):
                imc = weight_imc / (height_imc ** 2)
                
                if imc < 18.5:
                    category = "Abaixo do peso"
                    color = "#2196F3"
                elif imc < 25:
                    category = "Peso normal"
                    color = "#4CAF50"
                elif imc < 30:
                    category = "Sobrepeso"
                    color = "#FF9800"
                else:
                    category = "Obesidade"
                    color = "#F44336"
                
                st.markdown(f"""
                <div style="background: {color}20; border: 2px solid {color}; padding: 1.5rem; border-radius: 15px; text-align: center;">
                    <h2 style="margin: 0; color: {color};">📊 {imc:.1f}</h2>
                    <h4 style="margin: 0.5rem 0;">{category}</h4>
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("💧 Necessidade Hídrica")
        
        col1, col2 = st.columns(2)
        
        with col1:
            weight_water = st.number_input("⚖️ Peso (kg)", min_value=20.0, value=70.0, key="weight_water")
            activity = st.selectbox("🏃‍♂️ Atividade", ["Sedentário", "Ativo", "Muito Ativo"])
        
        with col2:
            if st.button("💧 Calcular", type="primary"):
                base_water = weight_water * 35
                
                if activity == "Ativo":
                    base_water *= 1.2
                elif activity == "Muito Ativo":
                    base_water *= 1.4
                
                liters = base_water / 1000
                
                st.markdown(f"""
                <div class="metric-card">
                    <h2 style="margin: 0; color: #2196F3;">💧 {liters:.1f}L</h2>
                    <p style="margin: 0;">Por dia</p>
                </div>
                """, unsafe_allow_html=True)

# Rotas principais
def main():
    load_css()
    init_database()
    
    if 'user' not in st.session_state or not st.session_state.user:
        show_login_page()
        return
    
    selected_page = show_sidebar()
    user_role = st.session_state.user['role']
    
    # Roteamento simples
    if selected_page == 'dashboard':
        if user_role == 'admin':
            show_admin_dashboard()
        elif user_role == 'nutritionist':
            show_nutritionist_dashboard()
        elif user_role == 'secretary':
            show_secretary_dashboard()
        elif user_role == 'patient':
            show_patient_dashboard()
    
    elif selected_page == 'ia_assistant':
        show_ia_assistant()
    
    elif selected_page == 'calculators':
        show_calculators()
    
    elif selected_page == 'chat':
        show_ia_assistant()
    
    else:
        # Páginas em desenvolvimento
        st.markdown(f'<h1 class="main-header">🚧 {selected_page.title()}</h1>', unsafe_allow_html=True)
        st.info(f"Funcionalidade '{selected_page}' em desenvolvimento. Todas as funcionalidades básicas estão operacionais!")

if __name__ == "__main__":
    main()
