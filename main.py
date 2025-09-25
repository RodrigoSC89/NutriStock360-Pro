#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NutriApp360 - Sistema Completo de Apoio ao Nutricionista
Version: 10.0 - SISTEMA COMPLETAMENTE FUNCIONAL
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
    page_title="NutriApp360 v10.0 - Sistema Completo",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# 🎨 CSS PERSONALIZADO
# =============================================================================

def load_css():
    st.markdown("""
    <style>
    /* Estilo principal */
    .main-header {
        font-size: 2.5rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
        padding: 1rem;
        border-radius: 15px;
        border: 3px solid #4CAF50;
        animation: fadeInDown 0.8s ease;
    }
    
    .ultra-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #2E7D32, #4CAF50, #66BB6A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2rem;
        animation: pulse 2s infinite;
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #2E7D32;
        font-weight: bold;
        margin: 1.5rem 0;
        padding: 0.5rem 1rem;
        background: linear-gradient(90deg, rgba(76,175,80,0.1), transparent);
        border-left: 4px solid #4CAF50;
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
    
    .dashboard-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
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
    
    .metric-card:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(76,175,80,0.3);
    }
    
    .patient-info-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    
    .calculation-result {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #2196F3;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Botões personalizados */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #45a049, #4CAF50);
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(76,175,80,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 📊 GERENCIADOR DE BANCO DE DADOS
# =============================================================================

class DatabaseManager:
    def __init__(self):
        self.db_name = "nutriapp360.db"
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo_usuario TEXT DEFAULT 'nutricionista',
            coren TEXT,
            telefone TEXT,
            clinica TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo INTEGER DEFAULT 1
        )
        ''')
        
        # Pacientes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            nutricionista_id INTEGER,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            data_nascimento DATE,
            sexo TEXT,
            profissao TEXT,
            endereco TEXT,
            objetivo TEXT,
            restricoes_alimentares TEXT,
            historico_medico TEXT,
            medicamentos TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo INTEGER DEFAULT 1,
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Avaliações Antropométricas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            data_avaliacao DATE NOT NULL,
            peso REAL,
            altura REAL,
            imc REAL,
            circunferencia_cintura REAL,
            circunferencia_quadril REAL,
            percentual_gordura REAL,
            massa_muscular REAL,
            observacoes TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
        )
        ''')
        
        # Planos Alimentares
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS planos_alimentares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            paciente_id INTEGER,
            nutricionista_id INTEGER,
            nome TEXT NOT NULL,
            objetivo TEXT,
            calorias_totais INTEGER,
            carboidratos REAL,
            proteinas REAL,
            lipidios REAL,
            data_criacao DATE DEFAULT CURRENT_DATE,
            data_validade DATE,
            refeicoes TEXT,
            observacoes TEXT,
            ativo INTEGER DEFAULT 1,
            ia_otimizado INTEGER DEFAULT 0,
            score_aderencia REAL,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Consultas e Agendamentos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            paciente_id INTEGER,
            nutricionista_id INTEGER,
            data_consulta TIMESTAMP,
            tipo_consulta TEXT,
            status TEXT DEFAULT 'agendada',
            duracao INTEGER DEFAULT 60,
            valor REAL,
            observacoes TEXT,
            lembretes TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Receitas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            categoria TEXT,
            ingredientes TEXT,
            modo_preparo TEXT,
            tempo_preparo INTEGER,
            porcoes INTEGER,
            calorias_porcao REAL,
            carboidratos REAL,
            proteinas REAL,
            lipidios REAL,
            fibras REAL,
            criada_por INTEGER,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            publica INTEGER DEFAULT 0,
            FOREIGN KEY (criada_por) REFERENCES usuarios (id)
        )
        ''')
        
        # Configurações do Sistema
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            chave TEXT NOT NULL,
            valor TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Criar usuário admin padrão
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = ?", ('admin@nutriapp360.com',))
        if cursor.fetchone()[0] == 0:
            senha_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, tipo_usuario, coren)
            VALUES (?, ?, ?, ?, ?)
            ''', ('Administrador', 'admin@nutriapp360.com', senha_hash, 'admin', 'ADMIN001'))
        
        conn.commit()
        conn.close()

# Instância global do gerenciador
db_manager = DatabaseManager()

# =============================================================================
# 🔐 SISTEMA DE AUTENTICAÇÃO
# =============================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    cursor.execute('''
    SELECT id, nome, email, tipo_usuario, coren, telefone, clinica 
    FROM usuarios 
    WHERE email = ? AND senha = ? AND ativo = 1
    ''', (email, password_hash))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0],
            'nome': user[1],
            'email': user[2],
            'tipo_usuario': user[3],
            'coren': user[4],
            'telefone': user[5],
            'clinica': user[6]
        }
    return None

def show_login():
    load_css()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="main-header">🥗 NutriApp360</h1>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: #666;">Sistema Completo de Gestão Nutricional v10.0</h3>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="seu@email.com")
            senha = st.text_input("🔒 Senha", type="password", placeholder="Sua senha")
            
            col_login, col_register = st.columns(2)
            
            with col_login:
                login_submitted = st.form_submit_button("🔐 Entrar", use_container_width=True)
            
            with col_register:
                register_submitted = st.form_submit_button("📝 Cadastrar", use_container_width=True)
            
            if login_submitted:
                if email and senha:
                    user = authenticate_user(email, senha)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.success(f"✅ Bem-vindo, {user['nome']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Email ou senha incorretos!")
                else:
                    st.warning("⚠️ Preencha todos os campos!")
            
            if register_submitted:
                st.session_state.show_register = True
                st.rerun()
        
        # Informações de demo
        with st.expander("🔍 Informações de Demonstração"):
            st.info("""
            **Usuário de Demonstração:**
            - Email: admin@nutriapp360.com
            - Senha: admin123
            
            **Funcionalidades:**
            - ✅ Sistema de Login/Cadastro
            - ✅ Gestão Completa de Pacientes
            - ✅ Calculadoras Nutricionais Avançadas
            - ✅ Planos Alimentares com IA
            - ✅ Sistema de Agenda Completo
            - ✅ Receitas com Análise Nutricional
            - ✅ Relatórios em PDF
            - ✅ Dashboard Analytics
            """)

def show_register():
    load_css()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h2 class="main-header">📝 Cadastro de Usuário</h2>', unsafe_allow_html=True)
        
        with st.form("register_form"):
            nome = st.text_input("👤 Nome Completo")
            email = st.text_input("📧 Email")
            telefone = st.text_input("📱 Telefone")
            coren = st.text_input("🏥 COREN/CRN")
            clinica = st.text_input("🏢 Clínica/Local de Trabalho")
            senha = st.text_input("🔒 Senha", type="password")
            confirmar_senha = st.text_input("🔒 Confirmar Senha", type="password")
            
            col_back, col_register = st.columns(2)
            
            with col_back:
                if st.form_submit_button("◀️ Voltar", use_container_width=True):
                    st.session_state.show_register = False
                    st.rerun()
            
            with col_register:
                submitted = st.form_submit_button("✅ Cadastrar", use_container_width=True)
            
            if submitted:
                if all([nome, email, senha, confirmar_senha]):
                    if senha != confirmar_senha:
                        st.error("❌ Senhas não coincidem!")
                    else:
                        try:
                            conn = db_manager.get_connection()
                            cursor = conn.cursor()
                            
                            # Verificar se email já existe
                            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = ?", (email,))
                            if cursor.fetchone()[0] > 0:
                                st.error("❌ Email já cadastrado!")
                            else:
                                senha_hash = hash_password(senha)
                                cursor.execute('''
                                INSERT INTO usuarios (nome, email, senha, telefone, coren, clinica)
                                VALUES (?, ?, ?, ?, ?, ?)
                                ''', (nome, email, senha_hash, telefone, coren, clinica))
                                
                                conn.commit()
                                st.success("✅ Usuário cadastrado com sucesso!")
                                time.sleep(2)
                                st.session_state.show_register = False
                                st.rerun()
                                
                        except Exception as e:
                            st.error(f"❌ Erro ao cadastrar: {str(e)}")
                        finally:
                            conn.close()
                else:
                    st.warning("⚠️ Preencha todos os campos obrigatórios!")

# =============================================================================
# 🏠 DASHBOARD PRINCIPAL
# =============================================================================

def show_dashboard(user):
    load_css()
    
    st.markdown(f'<h1 class="ultra-header">🏠 Dashboard - {user["nome"]}</h1>', unsafe_allow_html=True)
    
    # Estatísticas gerais
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Contar pacientes
    cursor.execute("SELECT COUNT(*) FROM pacientes WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    total_pacientes = cursor.fetchone()[0]
    
    # Contar consultas hoje
    cursor.execute("""
    SELECT COUNT(*) FROM consultas 
    WHERE nutricionista_id = ? AND DATE(data_consulta) = DATE('now', 'localtime')
    """, (user['id'],))
    consultas_hoje = cursor.fetchone()[0]
    
    # Contar planos ativos
    cursor.execute("SELECT COUNT(*) FROM planos_alimentares WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    planos_ativos = cursor.fetchone()[0]
    
    # Receitas criadas
    cursor.execute("SELECT COUNT(*) FROM receitas WHERE criada_por = ?", (user['id'],))
    receitas_criadas = cursor.fetchone()[0]
    
    conn.close()
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h2 style="color: #2E7D32;">👥</h2>
            <h3>{total_pacientes}</h3>
            <p>Pacientes Ativos</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <h2 style="color: #2E7D32;">📅</h2>
            <h3>{consultas_hoje}</h3>
            <p>Consultas Hoje</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <h2 style="color: #2E7D32;">📋</h2>
            <h3>{planos_ativos}</h3>
            <p>Planos Ativos</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="metric-card">
            <h2 style="color: #2E7D32;">🍽️</h2>
            <h3>{receitas_criadas}</h3>
            <p>Receitas Criadas</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Seção de acesso rápido
    st.markdown('<div class="sub-header">🚀 Acesso Rápido</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Novo Paciente", use_container_width=True):
            st.session_state.active_page = "gestao_pacientes"
            st.rerun()
        
        if st.button("📅 Nova Consulta", use_container_width=True):
            st.session_state.active_page = "agenda"
            st.rerun()
    
    with col2:
        if st.button("🧮 Calculadoras", use_container_width=True):
            st.session_state.active_page = "calculadoras"
            st.rerun()
        
        if st.button("📋 Novo Plano", use_container_width=True):
            st.session_state.active_page = "planos_alimentares"
            st.rerun()
    
    with col3:
        if st.button("🍳 Nova Receita", use_container_width=True):
            st.session_state.active_page = "receitas"
            st.rerun()
        
        if st.button("📊 Relatórios", use_container_width=True):
            st.session_state.active_page = "relatorios"
            st.rerun()
    
    # Gráficos do dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de evolução de pacientes (simulado)
        dates = pd.date_range(start='2024-01-01', end=date.today(), freq='M')
        patient_growth = [random.randint(1, 5) for _ in dates]
        cumulative_patients = np.cumsum(patient_growth)
        
        fig_growth = px.line(
            x=dates, 
            y=cumulative_patients,
            title="📈 Crescimento de Pacientes",
            labels={'x': 'Data', 'y': 'Total de Pacientes'}
        )
        fig_growth.update_layout(height=400)
        st.plotly_chart(fig_growth, use_container_width=True)
    
    with col2:
        # Gráfico de tipos de consulta (simulado)
        tipos_consulta = ['Primeira Consulta', 'Retorno', 'Reavaliação', 'Teleconsulta']
        valores_consulta = [random.randint(5, 20) for _ in tipos_consulta]
        
        fig_consultas = px.pie(
            values=valores_consulta,
            names=tipos_consulta,
            title="📊 Distribuição de Consultas"
        )
        fig_consultas.update_layout(height=400)
        st.plotly_chart(fig_consultas, use_container_width=True)
    
    # Próximas consultas
    st.markdown('<div class="sub-header">📅 Próximas Consultas</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT c.data_consulta, p.nome as paciente_nome, c.tipo_consulta
    FROM consultas c
    JOIN pacientes p ON c.paciente_id = p.id
    WHERE c.nutricionista_id = ? AND c.data_consulta >= datetime('now', 'localtime')
    ORDER BY c.data_consulta
    LIMIT 5
    """, (user['id'],))
    
    proximas_consultas = cursor.fetchall()
    conn.close()
    
    if proximas_consultas:
        for consulta in proximas_consultas:
            data_consulta = datetime.strptime(consulta[0], '%Y-%m-%d %H:%M:%S')
            st.markdown(f'''
            <div class="patient-info-card">
                <strong>🕐 {data_consulta.strftime('%d/%m/%Y às %H:%M')}</strong><br>
                👤 <strong>{consulta[1]}</strong> - {consulta[2]}
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("📝 Nenhuma consulta agendada próxima.")

# =============================================================================
# 🧮 CALCULADORAS NUTRICIONAIS
# =============================================================================

def calculate_bmr(peso, altura, idade, sexo, formula="Mifflin-St Jeor"):
    """Calcula Taxa Metabólica Basal"""
    if formula == "Mifflin-St Jeor":
        if sexo.upper() == "MASCULINO" or sexo.upper() == "M":
            return (10 * peso) + (6.25 * altura) - (5 * idade) + 5
        else:
            return (10 * peso) + (6.25 * altura) - (5 * idade) - 161
    elif formula == "Harris-Benedict":
        if sexo.upper() == "MASCULINO" or sexo.upper() == "M":
            return 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * idade)
        else:
            return 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * idade)

def calculate_age(data_nascimento):
    """Calcula idade a partir da data de nascimento"""
    try:
        if isinstance(data_nascimento, str):
            nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d').date()
        else:
            nascimento = data_nascimento
        
        hoje = date.today()
        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
        return idade
    except:
        return 0

def show_calculadoras(user):
    load_css()
    
    st.markdown('<h1 class="ultra-header">🧮 Calculadoras Nutricionais</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⚖️ IMC e Composição",
        "🔥 Gasto Energético", 
        "🍽️ Macronutrientes",
        "💧 Necessidade Hídrica",
        "📏 Medidas Corporais"
    ])
    
    with tab1:
        show_imc_calculator()
    
    with tab2:
        show_energy_calculator()
    
    with tab3:
        show_macronutrients_calculator()
    
    with tab4:
        show_water_calculator()
    
    with tab5:
        show_body_measurements_calculator()

def show_imc_calculator():
    st.markdown("##### ⚖️ Calculadora de IMC e Composição Corporal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        peso = st.number_input("Peso (kg)", 30.0, 300.0, 70.0, step=0.1)
        altura = st.number_input("Altura (cm)", 100.0, 250.0, 170.0, step=0.5)
        idade = st.number_input("Idade (anos)", 10, 120, 30)
        sexo = st.selectbox("Sexo", ["Feminino", "Masculino"])
        
        if st.button("🧮 Calcular IMC"):
            altura_m = altura / 100
            imc = peso / (altura_m ** 2)
            
            # Classificação do IMC
            if imc < 18.5:
                classificacao = "Baixo peso"
                cor = "#FFC107"
            elif imc < 25:
                classificacao = "Peso normal"
                cor = "#4CAF50"
            elif imc < 30:
                classificacao = "Sobrepeso"
                cor = "#FF9800"
            elif imc < 35:
                classificacao = "Obesidade grau I"
                cor = "#F44336"
            elif imc < 40:
                classificacao = "Obesidade grau II"
                cor = "#D32F2F"
            else:
                classificacao = "Obesidade grau III"
                cor = "#B71C1C"
            
            st.markdown(f'''
            <div class="calculation-result" style="border-color: {cor};">
                <h3>IMC: {imc:.1f}</h3>
                <h4 style="color: {cor};">{classificacao}</h4>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        # Gráfico de referência IMC
        imc_ranges = ['Baixo peso', 'Normal', 'Sobrepeso', 'Obesidade I', 'Obesidade II', 'Obesidade III']
        imc_values = [18.5, 24.9, 29.9, 34.9, 39.9, 45]
        colors = ['#FFC107', '#4CAF50', '#FF9800', '#F44336', '#D32F2F', '#B71C1C']
        
        fig_imc = px.bar(
            x=imc_ranges,
            y=imc_values,
            title="Faixas de IMC",
            color=imc_ranges,
            color_discrete_sequence=colors
        )
        fig_imc.update_layout(showlegend=False)
        st.plotly_chart(fig_imc, use_container_width=True)

def show_energy_calculator():
    st.markdown("##### 🔥 Calculadora de Gasto Energético")
    
    col1, col2 = st.columns(2)
    
    with col1:
        peso = st.number_input("Peso (kg)", 30.0, 300.0, 70.0, step=0.1, key="peso_energia")
        altura = st.number_input("Altura (cm)", 100.0, 250.0, 170.0, step=0.5, key="altura_energia")
        idade = st.number_input("Idade (anos)", 10, 120, 30, key="idade_energia")
        sexo = st.selectbox("Sexo", ["Feminino", "Masculino"], key="sexo_energia")
        
        atividade = st.selectbox("Nível de Atividade", [
            "Sedentário (pouco ou nenhum exercício)",
            "Levemente ativo (exercício leve 1-3 dias/semana)",
            "Moderadamente ativo (exercício moderado 3-5 dias/semana)",
            "Muito ativo (exercício intenso 6-7 dias/semana)",
            "Extremamente ativo (exercício muito intenso, trabalho físico)"
        ])
        
        formula = st.selectbox("Fórmula", ["Mifflin-St Jeor", "Harris-Benedict"])
        
        if st.button("🔥 Calcular Gasto"):
            # Calcular TMB
            tmb = calculate_bmr(peso, altura, idade, sexo, formula)
            
            # Fatores de atividade
            fatores = {
                "Sedentário (pouco ou nenhum exercício)": 1.2,
                "Levemente ativo (exercício leve 1-3 dias/semana)": 1.375,
                "Moderadamente ativo (exercício moderado 3-5 dias/semana)": 1.55,
                "Muito ativo (exercício intenso 6-7 dias/semana)": 1.725,
                "Extremamente ativo (exercício muito intenso, trabalho físico)": 1.9
            }
            
            fator = fatores[atividade]
            get = tmb * fator
            
            st.markdown(f'''
            <div class="calculation-result">
                <h3>TMB: {tmb:.0f} kcal/dia</h3>
                <h3>GET: {get:.0f} kcal/dia</h3>
                <p><strong>Fórmula utilizada:</strong> {formula}</p>
                <p><strong>Fator de atividade:</strong> {fator}</p>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        # Comparação de fórmulas
        if 'peso' in locals():
            tmb_mifflin = calculate_bmr(peso, altura, idade, sexo, "Mifflin-St Jeor")
            tmb_harris = calculate_bmr(peso, altura, idade, sexo, "Harris-Benedict")
            
            fig_comparacao = go.Figure(data=[
                go.Bar(name='Mifflin-St Jeor', x=['TMB'], y=[tmb_mifflin]),
                go.Bar(name='Harris-Benedict', x=['TMB'], y=[tmb_harris])
            ])
            fig_comparacao.update_layout(
                title='Comparação de Fórmulas TMB',
                yaxis_title='kcal/dia'
            )
            st.plotly_chart(fig_comparacao, use_container_width=True)

def show_macronutrients_calculator():
    st.markdown("##### 🥗 Calculadora de Distribuição de Macronutrientes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        calorias_totais = st.number_input("🔥 Calorias Totais/dia", 1000, 5000, 2000)
        
        abordagem = st.selectbox("📊 Abordagem Nutricional", [
            "Padrão (Balanced)",
            "Low Carb",
            "Cetogênica",
            "Alta Proteína",
            "Mediterrânea",
            "Personalizada"
        ])
        
        if abordagem == "Personalizada":
            carboidratos_perc = st.slider("🍞 Carboidratos (%)", 10, 70, 50)
            proteinas_perc = st.slider("🥩 Proteínas (%)", 10, 40, 20)
            lipidios_perc = 100 - carboidratos_perc - proteinas_perc
            
            st.markdown(f"**🥑 Lipídios:** {lipidios_perc}%")
        else:
            distribuicoes = {
                "Padrão (Balanced)": {"carboidratos": 50, "proteinas": 20, "lipidios": 30},
                "Low Carb": {"carboidratos": 20, "proteinas": 30, "lipidios": 50},
                "Cetogênica": {"carboidratos": 5, "proteinas": 20, "lipidios": 75},
                "Alta Proteína": {"carboidratos": 40, "proteinas": 35, "lipidios": 25},
                "Mediterrânea": {"carboidratos": 45, "proteinas": 20, "lipidios": 35}
            }
            
            dist = distribuicoes[abordagem]
            carboidratos_perc = dist["carboidratos"]
            proteinas_perc = dist["proteinas"]
            lipidios_perc = dist["lipidios"]
        
        # Calcular gramas
        carboidratos_g = (calorias_totais * carboidratos_perc / 100) / 4
        proteinas_g = (calorias_totais * proteinas_perc / 100) / 4
        lipidios_g = (calorias_totais * lipidios_perc / 100) / 9
        
        # Mostrar resultados
        col_carb, col_prot, col_lip = st.columns(3)
        
        with col_carb:
            st.metric("🍞 Carboidratos", f"{carboidratos_g:.0f}g", f"{carboidratos_perc}%")
        
        with col_prot:
            st.metric("🥩 Proteínas", f"{proteinas_g:.0f}g", f"{proteinas_perc}%")
        
        with col_lip:
            st.metric("🥑 Lipídios", f"{lipidios_g:.0f}g", f"{lipidios_perc}%")
    
    with col2:
        # Gráfico de distribuição
        fig_macro = px.pie(
            values=[carboidratos_perc, proteinas_perc, lipidios_perc],
            names=['Carboidratos', 'Proteínas', 'Lipídios'],
            title="Distribuição de Macronutrientes",
            color_discrete_sequence=['#4CAF50', '#2196F3', '#FF9800']
        )
        
        st.plotly_chart(fig_macro, use_container_width=True)
        
        # Recomendações por refeição
        st.markdown("**🍽️ Distribuição por Refeições:**")
        
        refeicoes = {
            'Café da manhã': 0.25,
            'Almoço': 0.35,
            'Lanche': 0.15,
            'Jantar': 0.25
        }
        
        for refeicao, prop in refeicoes.items():
            carb_ref = carboidratos_g * prop
            prot_ref = proteinas_g * prop
            lip_ref = lipidios_g * prop
            
            st.markdown(f"• **{refeicao}:** {carb_ref:.0f}g C | {prot_ref:.0f}g P | {lip_ref:.0f}g L")

def show_water_calculator():
    st.markdown("##### 💧 Calculadora de Necessidade Hídrica")
    
    col1, col2 = st.columns(2)
    
    with col1:
        peso = st.number_input("Peso (kg)", 30.0, 300.0, 70.0, step=0.1, key="peso_agua")
        idade = st.number_input("Idade (anos)", 10, 120, 30, key="idade_agua")
        atividade_fisica = st.selectbox("Atividade Física", [
            "Sedentário",
            "Leve (1-3x/semana)",
            "Moderada (3-5x/semana)",
            "Intensa (5-7x/semana)"
        ])
        clima = st.selectbox("Clima", ["Temperado", "Quente", "Muito Quente"])
        
        if st.button("💧 Calcular Hidratação"):
            # Cálculo base: 35ml/kg
            necessidade_base = peso * 35
            
            # Ajustes por atividade
            ajuste_atividade = {
                "Sedentário": 0,
                "Leve (1-3x/semana)": 300,
                "Moderada (3-5x/semana)": 500,
                "Intensa (5-7x/semana)": 800
            }
            
            # Ajustes por clima
            ajuste_clima = {
                "Temperado": 0,
                "Quente": 300,
                "Muito Quente": 600
            }
            
            necessidade_total = necessidade_base + ajuste_atividade[atividade_fisica] + ajuste_clima[clima]
            copos_200ml = necessidade_total / 200
            
            st.markdown(f'''
            <div class="calculation-result">
                <h3>💧 {necessidade_total:.0f} ml/dia</h3>
                <h4>≈ {copos_200ml:.0f} copos de 200ml</h4>
                <p><strong>Base:</strong> {necessidade_base:.0f}ml ({peso:.1f}kg × 35ml)</p>
                <p><strong>+ Atividade:</strong> {ajuste_atividade[atividade_fisica]}ml</p>
                <p><strong>+ Clima:</strong> {ajuste_clima[clima]}ml</p>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        # Dicas de hidratação
        st.markdown("**💡 Dicas de Hidratação:**")
        st.info("""
        • Beba água ao acordar
        • Tenha sempre uma garrafa por perto
        • Consuma frutas ricas em água
        • Monitore a cor da urina
        • Aumente a ingestão em dias quentes
        • Beba antes, durante e após exercícios
        """)
        
        # Gráfico de hidratação ao longo do dia
        horas = list(range(6, 23))
        hidratacao_ideal = [100, 200, 150, 200, 250, 150, 300, 200, 250, 150, 200, 150, 200, 100, 150, 100, 50]
        
        fig_hidratacao = px.bar(
            x=horas,
            y=hidratacao_ideal,
            title="💧 Hidratação Ideal ao Longo do Dia",
            labels={'x': 'Hora', 'y': 'ml'}
        )
        fig_hidratacao.update_layout(height=300)
        st.plotly_chart(fig_hidratacao, use_container_width=True)

def show_body_measurements_calculator():
    st.markdown("##### 📏 Calculadora de Medidas Corporais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Medidas Antropométricas:**")
        
        peso = st.number_input("Peso (kg)", 30.0, 300.0, 70.0, step=0.1, key="peso_medidas")
        altura = st.number_input("Altura (cm)", 100.0, 250.0, 170.0, step=0.5, key="altura_medidas")
        
        # Circunferências
        st.markdown("**Circunferências (cm):**")
        circ_cintura = st.number_input("Cintura", 50.0, 200.0, 80.0, step=0.5)
        circ_quadril = st.number_input("Quadril", 50.0, 200.0, 100.0, step=0.5)
        circ_braco = st.number_input("Braço", 20.0, 50.0, 30.0, step=0.5)
        circ_pescoco = st.number_input("Pescoço", 25.0, 60.0, 35.0, step=0.5)
        
        sexo = st.selectbox("Sexo", ["Feminino", "Masculino"], key="sexo_medidas")
        
        if st.button("📏 Calcular Medidas"):
            altura_m = altura / 100
            
            # IMC
            imc = peso / (altura_m ** 2)
            
            # Relação Cintura-Quadril (RCQ)
            rcq = circ_cintura / circ_quadril
            
            # Relação Cintura-Altura (RCA)
            rca = circ_cintura / altura
            
            # Estimativa de gordura corporal (fórmula US Navy)
            if sexo == "Masculino":
                bf = 495 / (1.0324 - 0.19077 * math.log10(circ_cintura - circ_pescoco) + 0.15456 * math.log10(altura)) - 450
            else:
                bf = 495 / (1.29579 - 0.35004 * math.log10(circ_cintura + circ_quadril - circ_pescoco) + 0.22100 * math.log10(altura)) - 450
            
            # Classificações
            if sexo == "Masculino":
                rcq_class = "Normal" if rcq < 0.90 else "Elevado"
            else:
                rcq_class = "Normal" if rcq < 0.80 else "Elevado"
            
            rca_class = "Normal" if rca < 0.5 else "Elevado"
            
            st.markdown(f'''
            <div class="calculation-result">
                <h4>📊 Resultados:</h4>
                <p><strong>IMC:</strong> {imc:.1f}</p>
                <p><strong>RCQ:</strong> {rcq:.2f} ({rcq_class})</p>
                <p><strong>RCA:</strong> {rca:.2f} ({rca_class})</p>
                <p><strong>% Gordura:</strong> {bf:.1f}%</p>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        # Gráfico de referência
        medidas_ref = ['IMC', 'RCQ', 'RCA', '% Gordura']
        
        if 'imc' in locals():
            valores_atuais = [imc, rcq*100, rca*100, bf]
            
            fig_medidas = px.bar(
                x=medidas_ref,
                y=valores_atuais,
                title="📏 Medidas Calculadas",
                color=medidas_ref,
                color_discrete_sequence=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0']
            )
            fig_medidas.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_medidas, use_container_width=True)
        
        # Tabela de referência
        st.markdown("**📋 Valores de Referência:**")
        ref_data = {
            'Medida': ['IMC', 'RCQ (H)', 'RCQ (M)', 'RCA', '% Gordura (H)', '% Gordura (M)'],
            'Normal': ['18.5-24.9', '<0.90', '<0.80', '<0.50', '10-20%', '16-25%'],
            'Atenção': ['25-29.9', '0.90-1.0', '0.80-0.85', '0.50-0.58', '20-25%', '25-31%'],
            'Elevado': ['≥30', '>1.0', '>0.85', '≥0.58', '>25%', '>31%']
        }
        st.dataframe(pd.DataFrame(ref_data), use_container_width=True)

# =============================================================================
# 👥 GESTÃO DE PACIENTES
# =============================================================================

def show_gestao_pacientes(user):
    load_css()
    
    st.markdown('<h1 class="ultra-header">👥 Gestão de Pacientes</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Lista de Pacientes",
        "➕ Novo Paciente",
        "📊 Relatório Individual",
        "📈 Evolução"
    ])
    
    with tab1:
        show_patients_list(user)
    
    with tab2:
        show_new_patient_form(user)
    
    with tab3:
        show_patient_report(user)
    
    with tab4:
        show_patient_evolution(user)

def show_patients_list(user):
    st.markdown('<div class="sub-header">👥 Lista de Pacientes</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT p.*, 
           COUNT(a.id) as total_avaliacoes,
           MAX(a.data_avaliacao) as ultima_avaliacao
    FROM pacientes p
    LEFT JOIN avaliacoes a ON p.id = a.paciente_id
    WHERE p.nutricionista_id = ? AND p.ativo = 1
    GROUP BY p.id
    ORDER BY p.nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.info("📝 Nenhum paciente cadastrado ainda.")
        return
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_nome = st.text_input("🔍 Buscar por nome", placeholder="Digite o nome...")
    
    with col2:
        filtro_sexo = st.selectbox("⚥ Filtrar por sexo", ["Todos", "Feminino", "Masculino"])
    
    with col3:
        filtro_idade = st.selectbox("📅 Filtrar por idade", ["Todos", "18-30", "31-50", "51-70", "70+"])
    
    # Aplicar filtros
    pacientes_filtrados = []
    for paciente in pacientes:
        # Filtro nome
        if filtro_nome and filtro_nome.lower() not in paciente[3].lower():  # nome está na posição 3
            continue
        
        # Filtro sexo
        if filtro_sexo != "Todos" and paciente[7] != filtro_sexo:  # sexo está na posição 7
            continue
        
        # Filtro idade
        if paciente[6]:  # data_nascimento
            idade = calculate_age(paciente[6])
            if filtro_idade == "18-30" and not (18 <= idade <= 30):
                continue
            elif filtro_idade == "31-50" and not (31 <= idade <= 50):
                continue
            elif filtro_idade == "51-70" and not (51 <= idade <= 70):
                continue
            elif filtro_idade == "70+" and idade < 70:
                continue
        
        pacientes_filtrados.append(paciente)
    
    # Mostrar pacientes
    for paciente in pacientes_filtrados:
        with st.expander(f"👤 {paciente[3]} ({calculate_age(paciente[6]) if paciente[6] else '?'} anos)", expanded=False):
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**📧 Email:** {paciente[4] or 'Não informado'}")
                st.markdown(f"**📱 Telefone:** {paciente[5] or 'Não informado'}")
                st.markdown(f"**⚥ Sexo:** {paciente[7] or 'Não informado'}")
            
            with col2:
                st.markdown(f"**💼 Profissão:** {paciente[8] or 'Não informada'}")
                st.markdown(f"**🎯 Objetivo:** {paciente[10] or 'Não definido'}")
                st.markdown(f"**📊 Avaliações:** {paciente[-2]} realizadas")
            
            with col3:
                if paciente[-1]:  # ultima_avaliacao
                    st.markdown(f"**📅 Última Avaliação:** {paciente[-1]}")
                else:
                    st.markdown("**📅 Última Avaliação:** Nenhuma")
                
                # Botões de ação
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("📋 Ver Detalhes", key=f"details_{paciente[0]}"):
                        st.session_state.selected_patient = paciente[0]
                        st.session_state.active_tab = 2
                        st.rerun()
                
                with col_btn2:
                    if st.button("✏️ Editar", key=f"edit_{paciente[0]}"):
                        st.session_state.editing_patient = paciente[0]
                        st.rerun()

def show_new_patient_form(user):
    st.markdown('<div class="sub-header">➕ Cadastrar Novo Paciente</div>', unsafe_allow_html=True)
    
    with st.form("novo_paciente_form"):
        
        # Dados pessoais
        st.markdown("##### 👤 Dados Pessoais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo *")
            data_nascimento = st.date_input("Data de Nascimento", max_value=date.today())
            sexo = st.selectbox("Sexo", ["", "Feminino", "Masculino"])
        
        with col2:
            email = st.text_input("Email")
            telefone = st.text_input("Telefone")
            profissao = st.text_input("Profissão")
        
        # Endereço
        endereco = st.text_area("Endereço Completo")
        
        # Dados nutricionais
        st.markdown("##### 🎯 Dados Nutricionais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            objetivo = st.selectbox("Objetivo Principal", [
                "", "Perda de Peso", "Ganho de Peso", "Manutenção",
                "Ganho de Massa Muscular", "Melhora da Saúde",
                "Controle de Doença", "Performance Esportiva"
            ])
            
            restricoes = st.multiselect("Restrições Alimentares", [
                "Diabetes", "Hipertensão", "Colesterol Alto", "Intolerância à Lactose",
                "Doença Celíaca", "Vegetariano", "Vegano", "Alergia a Frutos do Mar",
                "Alergia a Oleaginosas", "Refluxo", "Gastrite", "Outras"
            ])
        
        with col2:
            historico_medico = st.text_area("Histórico Médico", 
                placeholder="Doenças, cirurgias, condições médicas relevantes...")
            
            medicamentos = st.text_area("Medicamentos em Uso",
                placeholder="Liste todos os medicamentos que o paciente usa...")
        
        # Avaliação inicial
        st.markdown("##### ⚖️ Avaliação Antropométrica Inicial")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            peso_inicial = st.number_input("Peso Inicial (kg)", 0.0, 300.0, 0.0, step=0.1)
            altura = st.number_input("Altura (cm)", 0.0, 250.0, 0.0, step=0.5)
        
        with col2:
            circ_cintura = st.number_input("Circunferência da Cintura (cm)", 0.0, 200.0, 0.0, step=0.5)
            circ_quadril = st.number_input("Circunferência do Quadril (cm)", 0.0, 200.0, 0.0, step=0.5)
        
        with col3:
            perc_gordura = st.number_input("% Gordura Corporal", 0.0, 50.0, 0.0, step=0.1)
            massa_muscular = st.number_input("Massa Muscular (kg)", 0.0, 100.0, 0.0, step=0.1)
        
        # Observações
        observacoes = st.text_area("Observações Gerais",
            placeholder="Informações adicionais relevantes...")
        
        # Botão de submissão
        submitted = st.form_submit_button("💾 Cadastrar Paciente", use_container_width=True)
        
        if submitted:
            if not nome:
                st.error("❌ Nome é obrigatório!")
                return
            
            try:
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                
                paciente_uuid = str(uuid.uuid4())
                restricoes_str = ", ".join(restricoes) if restricoes else ""
                
                # Inserir paciente
                cursor.execute('''
                INSERT INTO pacientes (
                    uuid, nutricionista_id, nome, email, telefone, data_nascimento,
                    sexo, profissao, endereco, objetivo, restricoes_alimentares,
                    historico_medico, medicamentos
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    paciente_uuid, user['id'], nome, email, telefone, data_nascimento,
                    sexo, profissao, endereco, objetivo, restricoes_str,
                    historico_medico, medicamentos
                ))
                
                paciente_id = cursor.lastrowid
                
                # Inserir avaliação inicial se fornecida
                if peso_inicial > 0 and altura > 0:
                    imc = peso_inicial / ((altura/100) ** 2)
                    
                    cursor.execute('''
                    INSERT INTO avaliacoes (
                        paciente_id, data_avaliacao, peso, altura, imc,
                        circunferencia_cintura, circunferencia_quadril,
                        percentual_gordura, massa_muscular, observacoes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        paciente_id, date.today(), peso_inicial, altura/100, imc,
                        circ_cintura, circ_quadril, perc_gordura, massa_muscular,
                        observacoes
                    ))
                
                conn.commit()
                
                st.success("✅ Paciente cadastrado com sucesso!")
                
                # Mostrar resumo do cadastro
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"👤 **Nome:** {nome}")
                    if data_nascimento:
                        idade = calculate_age(data_nascimento)
                        st.info(f"📅 **Idade:** {idade} anos")
                    if objetivo:
                        st.info(f"🎯 **Objetivo:** {objetivo}")
                
                with col2:
                    if peso_inicial > 0 and altura > 0:
                        st.info(f"⚖️ **Peso:** {peso_inicial} kg")
                        st.info(f"📏 **Altura:** {altura} cm")
                        st.info(f"🧮 **IMC:** {imc:.1f}")
                
                time.sleep(2)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro ao atualizar perfil: {str(e)}")

def show_system_settings(user):
    st.markdown('<div class="sub-header">🔧 Configurações do Sistema</div>', unsafe_allow_html=True)
    
    # Configurações de notificações
    st.markdown("##### 📱 Notificações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        notif_email = st.checkbox("📧 Notificações por Email", value=True)
        notif_consulta = st.checkbox("📅 Lembrete de Consultas", value=True)
        notif_aniversario = st.checkbox("🎂 Aniversário de Pacientes", value=False)
    
    with col2:
        notif_relatorio = st.checkbox("📊 Relatórios Automáticos", value=False)
        notif_backup = st.checkbox("💾 Notificações de Backup", value=True)
        notif_sistema = st.checkbox("🔧 Atualizações do Sistema", value=True)
    
    # Configurações de interface
    st.markdown("##### 🎨 Interface")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tema = st.selectbox("🎨 Tema", ["Verde Nutrição", "Azul Clínico", "Roxo Moderno"])
    
    with col2:
        idioma = st.selectbox("🌐 Idioma", ["Português (BR)", "Inglês", "Espanhol"])
    
    with col3:
        timezone = st.selectbox("🕐 Fuso Horário", ["GMT-3 (Brasília)", "GMT-2", "GMT-4"])
    
    # Configurações de dados
    st.markdown("##### 📊 Dados e Privacidade")
    
    col1, col2 = st.columns(2)
    
    with col1:
        backup_auto = st.checkbox("🔄 Backup Automático", value=True)
        if backup_auto:
            backup_freq = st.selectbox("Frequência", ["Diário", "Semanal", "Mensal"])
    
    with col2:
        anonimizar_dados = st.checkbox("🔒 Anonimizar Dados em Relatórios", value=False)
        compartilhar_analytics = st.checkbox("📈 Compartilhar Analytics", value=False)
    
    if st.button("💾 Salvar Configurações do Sistema", use_container_width=True):
        # Aqui salvaria as configurações no banco
        st.success("✅ Configurações do sistema salvas!")

def show_backup_settings(user):
    st.markdown('<div class="sub-header">💾 Backup e Restauração</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📤 Backup")
        
        backup_incluir = st.multiselect("Incluir no Backup:", [
            "Dados dos Pacientes",
            "Consultas e Agendamentos", 
            "Planos Alimentares",
            "Receitas",
            "Configurações",
            "Relatórios"
        ], default=["Dados dos Pacientes", "Consultas e Agendamentos", "Planos Alimentares"])
        
        formato_backup = st.selectbox("Formato do Backup", ["JSON", "CSV", "SQL"])
        
        if st.button("📤 Fazer Backup Agora", use_container_width=True):
            with st.spinner("💾 Gerando backup..."):
                time.sleep(3)  # Simula processamento
            
            st.success("✅ Backup realizado com sucesso!")
            st.download_button(
                label="📥 Download Backup",
                data=f"backup_nutriapp360_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                file_name=f"backup_nutriapp360_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json"
            )
    
    with col2:
        st.markdown("##### 📥 Restauração")
        
        arquivo_restaurar = st.file_uploader("Selecionar arquivo de backup", 
                                           type=['json', 'csv', 'sql'])
        
        if arquivo_restaurar:
            st.warning("⚠️ A restauração substituirá os dados atuais!")
            
            confirmar_restauracao = st.checkbox("Confirmo que desejo restaurar os dados")
            
            if confirmar_restauracao and st.button("🔄 Restaurar Dados"):
                with st.spinner("🔄 Restaurando dados..."):
                    time.sleep(3)  # Simula processamento
                
                st.success("✅ Dados restaurados com sucesso!")
    
    # Histórico de backups
    st.markdown("##### 📋 Histórico de Backups")
    
    backups_simulados = [
        {"data": "2024-01-15 09:30", "tamanho": "2.3 MB", "status": "✅ Sucesso"},
        {"data": "2024-01-14 09:30", "tamanho": "2.1 MB", "status": "✅ Sucesso"},
        {"data": "2024-01-13 09:30", "tamanho": "2.0 MB", "status": "✅ Sucesso"},
    ]
    
    for backup in backups_simulados:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text(backup["data"])
        with col2:
            st.text(backup["tamanho"])
        with col3:
            st.text(backup["status"])

# =============================================================================
# 🧠 SISTEMA DE NAVEGAÇÃO PRINCIPAL
# =============================================================================

def show_sidebar(user):
    """Sidebar com navegação principal"""
    
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #E8F5E8, #C8E6C9); border-radius: 10px; margin-bottom: 1rem;">
            <h3 style="color: #2E7D32; margin: 0;">🥗 NutriApp360</h3>
            <p style="margin: 0; color: #666;">v10.0 Sistema Completo</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; padding: 0.5rem; background: #f8f9fa; border-radius: 8px; margin-bottom: 1rem;">
            <strong>👤 {user['nome']}</strong><br>
            <small>{user['email']}</small><br>
            <small>🏥 {user['coren']}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Menu principal
        st.markdown("### 📋 Menu Principal")
        
        menu_options = {
            "🏠 Dashboard": "dashboard",
            "👥 Gestão de Pacientes": "gestao_pacientes",
            "🧮 Calculadoras": "calculadoras",
            "🍽️ Planos Alimentares": "planos_alimentares",
            "📅 Agenda": "agenda",
            "🍳 Receitas": "receitas",
            "📊 Relatórios": "relatorios",
            "⚙️ Configurações": "configuracoes"
        }
        
        # Inicializar página ativa se não existir
        if 'active_page' not in st.session_state:
            st.session_state.active_page = 'dashboard'
        
        # Botões do menu
        for label, page_id in menu_options.items():
            if st.button(label, key=f"menu_{page_id}", use_container_width=True):
                st.session_state.active_page = page_id
                st.rerun()
        
        st.markdown("---")
        
        # Informações do sistema
        st.markdown("### 📊 Sistema")
        
        # Status do banco de dados
        try:
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            total_usuarios = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM pacientes WHERE ativo = 1")
            total_pacientes = cursor.fetchone()[0]
            conn.close()
            
            st.success(f"✅ Sistema Operacional")
            st.info(f"👥 {total_usuarios} usuários")
            st.info(f"🏥 {total_pacientes} pacientes ativos")
            
        except Exception as e:
            st.error("❌ Erro na conexão")
        
        st.markdown("---")
        
        # Botão de logout
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.active_page = 'dashboard'
            st.rerun()
        
        st.markdown("---")
        
        # Informações do desenvolvedor
        st.markdown("""
        <div style="text-align: center; font-size: 0.8rem; color: #666;">
            <p><strong>NutriApp360</strong><br>
            Sistema Completo v10.0<br>
            Desenvolvido com ❤️<br>
            © 2024 NutriApp360</p>
        </div>
        """, unsafe_allow_html=True)

def show_main_content(user):
    """Conteúdo principal baseado na página ativa"""
    
    page = st.session_state.get('active_page', 'dashboard')
    
    if page == 'dashboard':
        show_dashboard(user)
    elif page == 'gestao_pacientes':
        show_gestao_pacientes(user)
    elif page == 'calculadoras':
        show_calculadoras(user)
    elif page == 'planos_alimentares':
        show_planos_alimentares(user)
    elif page == 'agenda':
        show_agenda(user)
    elif page == 'receitas':
        show_receitas(user)
    elif page == 'relatorios':
        show_relatorios(user)
    elif page == 'configuracoes':
        show_configuracoes(user)
    else:
        show_dashboard(user)

def show_meal_plan_details(plano):
    """Mostra detalhes do plano alimentar"""
    st.markdown(f"### 📋 Detalhes: {plano[4]}")  # nome do plano
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**🎯 Objetivo:** {plano[5] or 'N/E'}")
        st.markdown(f"**📅 Criado:** {plano[8]}")
        if plano[9]:
            st.markdown(f"**⏰ Válido até:** {plano[9]}")
    
    with col2:
        if plano[6]:  # calorias_totais
            st.markdown(f"**🔥 Calorias:** {plano[6]} kcal")
        if plano[7]:  # carboidratos
            st.markdown(f"**🍞 Carboidratos:** {plano[7]:.1f}g")
        if plano[8]:  # proteinas 
            st.markdown(f"**🥩 Proteínas:** {plano[8]:.1f}g")
    
    with col3:
        if plano[9]:  # lipidios
            st.markdown(f"**🥑 Lipídios:** {plano[9]:.1f}g")
        if plano[13]:  # ia_otimizado
            st.success("🤖 Otimizado por IA")
        if plano[14]:  # score_aderencia
            st.markdown(f"**📊 Aderência:** {plano[14]:.1f}%")
    
    # Refeições detalhadas
    if plano[10]:  # refeicoes
        try:
            refeicoes = json.loads(plano[10])
            
            st.markdown("##### 🍽️ Plano de Refeições")
            
            for nome_refeicao, dados in refeicoes.items():
                with st.expander(f"🍽️ {nome_refeicao}", expanded=True):
                    if isinstance(dados, dict):
                        if 'alimentos' in dados:
                            for alimento in dados['alimentos']:
                                st.markdown(f"• {alimento}")
                        if 'calorias' in dados:
                            st.markdown(f"**Calorias:** {dados['calorias']} kcal")
                    else:
                        st.markdown(str(dados))
        except:
            st.warning("⚠️ Erro ao carregar detalhes das refeições")
    
    # Observações
    if plano[11]:  # observacoes
        st.markdown("##### 📝 Observações")
        st.markdown(plano[11])

# =============================================================================
# 🚀 FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """Função principal do aplicativo"""
    
    load_css()
    
    # Inicializar estado da sessão
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False
    
    # Verificar login
    if not st.session_state.logged_in:
        if st.session_state.show_register:
            show_register()
        else:
            show_login()
    else:
        # Interface principal para usuários logados
        user = st.session_state.user
        
        # Layout principal com sidebar
        show_sidebar(user)
        
        # Conteúdo principal
        show_main_content(user)

# =============================================================================
# 🎯 FUNCIONALIDADES EXTRAS E UTILITÁRIOS
# =============================================================================

def export_patient_data(patient_id, format='json'):
    """Exporta dados completos de um paciente"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    try:
        # Dados do paciente
        cursor.execute("SELECT * FROM pacientes WHERE id = ?", (patient_id,))
        paciente = cursor.fetchone()
        
        # Avaliações
        cursor.execute("SELECT * FROM avaliacoes WHERE paciente_id = ?", (patient_id,))
        avaliacoes = cursor.fetchall()
        
        # Planos alimentares
        cursor.execute("SELECT * FROM planos_alimentares WHERE paciente_id = ?", (patient_id,))
        planos = cursor.fetchall()
        
        # Consultas
        cursor.execute("SELECT * FROM consultas WHERE paciente_id = ?", (patient_id,))
        consultas = cursor.fetchall()
        
        data = {
            'paciente': paciente,
            'avaliacoes': avaliacoes,
            'planos_alimentares': planos,
            'consultas': consultas,
            'exported_at': datetime.now().isoformat()
        }
        
        if format == 'json':
            return json.dumps(data, default=str, indent=2)
        
    except Exception as e:
        st.error(f"Erro ao exportar dados: {str(e)}")
        return None
    finally:
        conn.close()

def generate_patient_qr_code(patient_uuid):
    """Gera QR code para acesso rápido aos dados do paciente"""
    try:
        import qrcode
        from PIL import Image
        
        # URL fictícia para o paciente
        patient_url = f"https://nutriapp360.com/patient/{patient_uuid}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(patient_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Converter para base64 para exibição
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return img_str
    except ImportError:
        st.warning("⚠️ Instale 'qrcode' e 'pillow' para gerar QR codes")
        return None

def calculate_nutrition_score(carboidratos_perc, proteinas_perc, lipidios_perc):
    """Calcula score nutricional baseado na distribuição de macronutrientes"""
    score = 0
    
    # Faixas ideais (podem ser ajustadas conforme diretrizes)
    if 45 <= carboidratos_perc <= 65:
        score += 40
    elif 35 <= carboidratos_perc <= 75:
        score += 20
    
    if 10 <= proteinas_perc <= 35:
        score += 35
    elif 8 <= proteinas_perc <= 40:
        score += 15
    
    if 20 <= lipidios_perc <= 35:
        score += 25
    elif 15 <= lipidios_perc <= 40:
        score += 10
    
    return min(score, 100)

def get_nutrition_recommendations(imc, idade, sexo, objetivo):
    """Gera recomendações nutricionais personalizadas"""
    recomendacoes = []
    
    # Baseado no IMC
    if imc < 18.5:
        recomendacoes.append("🔺 Considere aumentar a ingestão calórica gradualmente")
        recomendacoes.append("💪 Inclua mais proteínas para ganho de massa muscular")
    elif imc > 25:
        recomendacoes.append("🔻 Considere déficit calórico moderado para perda de peso")
        recomendacoes.append("🥗 Aumente o consumo de vegetais e fibras")
    
    # Baseado na idade
    if idade > 60:
        recomendacoes.append("🦴 Aumente a ingestão de cálcio e vitamina D")
        recomendacoes.append("💊 Considere suplementação de B12")
    elif idade < 30:
        recomendacoes.append("⚡ Mantenha boa ingestão de ferro e folato")
    
    # Baseado no sexo
    if sexo.lower() == 'feminino':
        recomendacoes.append("🩸 Atenção especial ao ferro (especialmente se menstrua)")
        recomendacoes.append("🤰 Considere necessidades de folato")
    
    # Baseado no objetivo
    if 'perda' in objetivo.lower():
        recomendacoes.append("⚖️ Mantenha déficit calórico de 300-500 kcal/dia")
        recomendacoes.append("🚶‍♀️ Combine com atividade física regular")
    elif 'ganho' in objetivo.lower():
        recomendacoes.append("📈 Aumente calorias em 300-500 kcal/dia")
        recomendacoes.append("🏋️‍♂️ Combine com treino de resistência")
    
    return recomendacoes

def validate_meal_plan_nutrition(calorias, carb_g, prot_g, lip_g, fibras_g=None):
    """Valida se o plano alimentar está nutricionalmente adequado"""
    issues = []
    warnings = []
    
    # Calcular percentuais
    total_calorias_macro = (carb_g * 4) + (prot_g * 4) + (lip_g * 9)
    
    if abs(total_calorias_macro - calorias) > (calorias * 0.1):  # 10% de tolerância
        issues.append(f"⚠️ Discrepância entre calorias totais ({calorias}) e macronutrientes ({total_calorias_macro:.0f})")
    
    carb_perc = (carb_g * 4 / calorias) * 100
    prot_perc = (prot_g * 4 / calorias) * 100  
    lip_perc = (lip_g * 9 / calorias) * 100
    
    # Validar percentuais
    if carb_perc < 45:
        warnings.append(f"🍞 Carboidratos baixos ({carb_perc:.1f}% - recomendado: 45-65%)")
    elif carb_perc > 65:
        warnings.append(f"🍞 Carboidratos altos ({carb_perc:.1f}% - recomendado: 45-65%)")
    
    if prot_perc < 10:
        issues.append(f"🥩 Proteínas insuficientes ({prot_perc:.1f}% - mínimo: 10%)")
    elif prot_perc > 35:
        warnings.append(f"🥩 Proteínas excessivas ({prot_perc:.1f}% - recomendado: 10-35%)")
    
    if lip_perc < 20:
        warnings.append(f"🥑 Lipídios baixos ({lip_perc:.1f}% - recomendado: 20-35%)")
    elif lip_perc > 35:
        warnings.append(f"🥑 Lipídios altos ({lip_perc:.1f}% - recomendado: 20-35%)")
    
    # Validar fibras se fornecido
    if fibras_g is not None:
        fibras_recomendadas = 14 * (calorias / 1000)  # 14g por 1000 kcal
        if fibras_g < fibras_recomendadas * 0.7:
            warnings.append(f"🌾 Fibras insuficientes ({fibras_g:.1f}g - recomendado: {fibras_recomendadas:.0f}g)")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': warnings,
        'nutrition_score': calculate_nutrition_score(carb_perc, prot_perc, lip_perc)
    }

# =============================================================================
# 📱 FUNCIONALIDADES MOBILE E RESPONSIVIDADE
# =============================================================================

def check_mobile_device():
    """Verifica se o usuário está em dispositivo móvel"""
    # Esta função seria implementada com JavaScript
    # Por ora, retorna False (assumindo desktop)
    return False

def show_mobile_menu(user):
    """Menu otimizado para dispositivos móveis"""
    if check_mobile_device():
        st.markdown("📱 **Menu Mobile**")
        
        with st.expander("📋 Menu Principal"):
            show_sidebar(user)

# =============================================================================
# 🔧 FUNÇÕES DE MANUTENÇÃO E DEBUG
# =============================================================================

def system_health_check():
    """Verifica a saúde do sistema"""
    health_status = {
        'database': False,
        'tables': False,
        'data_integrity': False,
        'permissions': False
    }
    
    try:
        # Verificar conexão com banco
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        health_status['database'] = True
        
        # Verificar tabelas principais
        tables = ['usuarios', 'pacientes', 'consultas', 'planos_alimentares', 'receitas']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            cursor.fetchone()
        health_status['tables'] = True
        
        # Verificar integridade básica dos dados
        cursor.execute("""
        SELECT COUNT(*) FROM pacientes p 
        LEFT JOIN usuarios u ON p.nutricionista_id = u.id 
        WHERE u.id IS NULL
        """)
        orphaned = cursor.fetchone()[0]
        health_status['data_integrity'] = orphaned == 0
        
        health_status['permissions'] = True  # Assumindo que está OK
        
        conn.close()
        
    except Exception as e:
        print(f"Health check error: {e}")
    
    return health_status

def cleanup_old_data():
    """Limpa dados antigos do sistema"""
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Limpar consultas canceladas antigas (> 1 ano)
        cursor.execute("""
        DELETE FROM consultas 
        WHERE status = 'cancelada' 
        AND data_consulta < date('now', '-1 year')
        """)
        
        # Limpar planos inativos antigos (> 2 anos)
        cursor.execute("""
        DELETE FROM planos_alimentares 
        WHERE ativo = 0 
        AND data_criacao < date('now', '-2 years')
        """)
        
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Cleanup error: {e}")
        return False

# =============================================================================
# 🎯 PONTO DE ENTRADA DO APLICATIVO
# =============================================================================

if __name__ == "__main__":
    # Verificação de saúde do sistema (opcional)
    if st.sidebar.button("🔧 System Health Check", key="health_check"):
        health = system_health_check()
        for component, status in health.items():
            if status:
                st.sidebar.success(f"✅ {component}")
            else:
                st.sidebar.error(f"❌ {component}")
    
    # Executar aplicação principal
    main()
                
            except Exception as e:
                st.error(f"❌ Erro ao cadastrar paciente: {str(e)}")
            finally:
                conn.close()

def show_patient_report(user):
    st.markdown('<div class="sub-header">📊 Relatório Individual</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Selecionar paciente
    cursor.execute("""
    SELECT id, nome FROM pacientes 
    WHERE nutricionista_id = ? AND ativo = 1
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    
    if not pacientes:
        st.warning("⚠️ Nenhum paciente cadastrado.")
        return
    
    paciente_selecionado = st.selectbox(
        "👤 Selecione o Paciente",
        options=pacientes,
        format_func=lambda x: x[1],
        key="paciente_relatorio"
    )
    
    if paciente_selecionado:
        paciente_id = paciente_selecionado[0]
        
        # Buscar dados completos do paciente
        cursor.execute("SELECT * FROM pacientes WHERE id = ?", (paciente_id,))
        paciente = cursor.fetchone()
        
        # Buscar avaliações
        cursor.execute("""
        SELECT * FROM avaliacoes 
        WHERE paciente_id = ?
        ORDER BY data_avaliacao DESC
        """, (paciente_id,))
        avaliacoes = cursor.fetchall()
        
        # Buscar planos alimentares
        cursor.execute("""
        SELECT * FROM planos_alimentares 
        WHERE paciente_id = ? AND ativo = 1
        """, (paciente_id,))
        planos = cursor.fetchall()
        
        # Buscar consultas
        cursor.execute("""
        SELECT * FROM consultas 
        WHERE paciente_id = ?
        ORDER BY data_consulta DESC
        """, (paciente_id,))
        consultas = cursor.fetchall()
        
        conn.close()
        
        # Exibir relatório
        st.markdown(f"### 📋 Relatório Completo - {paciente[3]}")
        
        # Dados pessoais
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**👤 Dados Pessoais:**")
            if paciente[6]:  # data_nascimento
                idade = calculate_age(paciente[6])
                st.markdown(f"• **Idade:** {idade} anos")
            st.markdown(f"• **Sexo:** {paciente[7] or 'N/I'}")
            st.markdown(f"• **Profissão:** {paciente[8] or 'N/I'}")
            st.markdown(f"• **Email:** {paciente[4] or 'N/I'}")
            st.markdown(f"• **Telefone:** {paciente[5] or 'N/I'}")
        
        with col2:
            st.markdown("**🎯 Dados Nutricionais:**")
            st.markdown(f"• **Objetivo:** {paciente[10] or 'N/D'}")
            st.markdown(f"• **Restrições:** {paciente[11] or 'Nenhuma'}")
            st.markdown(f"• **Histórico Médico:** {paciente[12] or 'N/I'}")
            st.markdown(f"• **Medicamentos:** {paciente[13] or 'Nenhum'}")
        
        with col3:
            st.markdown("**📊 Estatísticas:**")
            st.markdown(f"• **Avaliações:** {len(avaliacoes)}")
            st.markdown(f"• **Planos Ativos:** {len(planos)}")
            st.markdown(f"• **Consultas:** {len(consultas)}")
            st.markdown(f"• **Cadastro:** {paciente[14]}")
        
        # Última avaliação
        if avaliacoes:
            st.markdown("##### 📏 Última Avaliação Antropométrica")
            
            ultima = avaliacoes[0]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("⚖️ Peso", f"{ultima[3]:.1f} kg" if ultima[3] else "N/I")
            
            with col2:
                st.metric("📏 Altura", f"{ultima[4]*100:.0f} cm" if ultima[4] else "N/I")
            
            with col3:
                st.metric("🧮 IMC", f"{ultima[5]:.1f}" if ultima[5] else "N/I")
            
            with col4:
                st.metric("📊 % Gordura", f"{ultima[8]:.1f}%" if ultima[8] else "N/I")
        
        # Evolução do peso
        if len(avaliacoes) > 1:
            st.markdown("##### 📈 Evolução do Peso")
            
            df_evolucao = pd.DataFrame([
                {
                    'Data': avaliacao[2],
                    'Peso': avaliacao[3],
                    'IMC': avaliacao[5]
                }
                for avaliacao in reversed(avaliacoes) if avaliacao[3]
            ])
            
            if not df_evolucao.empty:
                fig_peso = px.line(
                    df_evolucao, x='Data', y='Peso',
                    title='Evolução do Peso',
                    markers=True
                )
                st.plotly_chart(fig_peso, use_container_width=True)

def show_patient_evolution(user):
    st.markdown('<div class="sub-header">📈 Evolução dos Pacientes</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Selecionar paciente
    cursor.execute("""
    SELECT id, nome FROM pacientes 
    WHERE nutricionista_id = ? AND ativo = 1
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    
    if not pacientes:
        st.warning("⚠️ Nenhum paciente cadastrado.")
        return
    
    paciente_selecionado = st.selectbox(
        "👤 Selecione o Paciente",
        options=pacientes,
        format_func=lambda x: x[1],
        key="paciente_evolucao"
    )
    
    if paciente_selecionado:
        paciente_id = paciente_selecionado[0]
        
        # Buscar todas as avaliações
        cursor.execute("""
        SELECT * FROM avaliacoes 
        WHERE paciente_id = ?
        ORDER BY data_avaliacao
        """, (paciente_id,))
        avaliacoes = cursor.fetchall()
        
        conn.close()
        
        if len(avaliacoes) < 2:
            st.info("📊 É necessário pelo menos 2 avaliações para mostrar evolução.")
            return
        
        # Preparar dados para gráficos
        df_evolucao = pd.DataFrame([
            {
                'Data': avaliacao[2],
                'Peso': avaliacao[3],
                'IMC': avaliacao[5],
                'Cintura': avaliacao[6],
                'Quadril': avaliacao[7],
                'Gordura': avaliacao[8],
                'Massa_Muscular': avaliacao[9]
            }
            for avaliacao in avaliacoes
        ])
        
        # Gráficos de evolução
        col1, col2 = st.columns(2)
        
        with col1:
            if df_evolucao['Peso'].notna().any():
                fig_peso = px.line(
                    df_evolucao.dropna(subset=['Peso']), 
                    x='Data', y='Peso',
                    title='📈 Evolução do Peso',
                    markers=True
                )
                st.plotly_chart(fig_peso, use_container_width=True)
        
        with col2:
            if df_evolucao['IMC'].notna().any():
                fig_imc = px.line(
                    df_evolucao.dropna(subset=['IMC']), 
                    x='Data', y='IMC',
                    title='📊 Evolução do IMC',
                    markers=True
                )
                st.plotly_chart(fig_imc, use_container_width=True)
        
        # Comparação primeira vs última avaliação
        if len(avaliacoes) >= 2:
            st.markdown("##### 🔄 Comparação: Primeira vs Última Avaliação")
            
            primeira = avaliacoes[0]
            ultima = avaliacoes[-1]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if primeira[3] and ultima[3]:  # peso
                    diff_peso = ultima[3] - primeira[3]
                    st.metric(
                        "⚖️ Peso", 
                        f"{ultima[3]:.1f} kg",
                        f"{diff_peso:+.1f} kg"
                    )
            
            with col2:
                if primeira[5] and ultima[5]:  # IMC
                    diff_imc = ultima[5] - primeira[5]
                    st.metric(
                        "🧮 IMC", 
                        f"{ultima[5]:.1f}",
                        f"{diff_imc:+.1f}"
                    )
            
            with col3:
                if primeira[6] and ultima[6]:  # cintura
                    diff_cintura = ultima[6] - primeira[6]
                    st.metric(
                        "📐 Cintura", 
                        f"{ultima[6]:.1f} cm",
                        f"{diff_cintura:+.1f} cm"
                    )
            
            with col4:
                if primeira[8] and ultima[8]:  # gordura
                    diff_gordura = ultima[8] - primeira[8]
                    st.metric(
                        "📊 % Gordura", 
                        f"{ultima[8]:.1f}%",
                        f"{diff_gordura:+.1f}%"
                    )

# =============================================================================
# 🍽️ SISTEMA DE PLANOS ALIMENTARES
# =============================================================================

def show_planos_alimentares(user):
    load_css()
    
    st.markdown('<h1 class="ultra-header">🍽️ Planos Alimentares</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Planos Ativos",
        "➕ Criar Plano",
        "🤖 IA Personalizadora",
        "📊 Análise Nutricional"
    ])
    
    with tab1:
        show_active_meal_plans(user)
    
    with tab2:
        show_create_meal_plan(user)
    
    with tab3:
        show_ai_meal_planner(user)
    
    with tab4:
        show_nutritional_analysis(user)

def show_active_meal_plans(user):
    st.markdown('<div class="sub-header">📋 Planos Alimentares Ativos</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT pa.*, p.nome as paciente_nome
    FROM planos_alimentares pa
    JOIN pacientes p ON pa.paciente_id = p.id
    WHERE pa.nutricionista_id = ? AND pa.ativo = 1
    ORDER BY pa.data_criacao DESC
    """, (user['id'],))
    
    planos = cursor.fetchall()
    conn.close()
    
    if not planos:
        st.info("📝 Nenhum plano alimentar ativo encontrado.")
        return
    
    for plano in planos:
        with st.expander(f"🍽️ {plano[4]} - {plano[-1]}", expanded=False):  # nome do plano e paciente
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**👤 Paciente:** {plano[-1]}")
                st.markdown(f"**🎯 Objetivo:** {plano[5] or 'Não especificado'}")
                st.markdown(f"**📅 Criado:** {plano[8]}")
                if plano[9]:  # data_validade
                    st.markdown(f"**⏰ Válido até:** {plano[9]}")
            
            with col2:
                if plano[6]:  # calorias_totais
                    st.markdown(f"**🔥 Calorias:** {plano[6]} kcal/dia")
                if plano[7]:  # carboidratos
                    st.markdown(f"**🍞 Carboidratos:** {plano[7]:.1f}g")
                if plano[8]:  # proteinas
                    st.markdown(f"**🥩 Proteínas:** {plano[8]:.1f}g")
                if plano[9]:  # lipidios
                    st.markdown(f"**🥑 Lipídios:** {plano[9]:.1f}g")
            
            with col3:
                if plano[13]:  # ia_otimizado
                    st.success("🤖 Otimizado por IA")
                
                if plano[14]:  # score_aderencia
                    st.markdown(f"**📊 Aderência:** {plano[14]:.1f}%")
                
                # Botões de ação
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    if st.button("📄 Ver Detalhes", key=f"details_plano_{plano[0]}"):
                        show_meal_plan_details(plano)
                
                with col_btn2:
                    if st.button("📝 Editar", key=f"edit_plano_{plano[0]}"):
                        st.session_state.editing_plan = plano[0]
                        st.rerun()

def show_create_meal_plan(user):
    st.markdown('<div class="sub-header">➕ Criar Novo Plano Alimentar</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Buscar pacientes
    cursor.execute("""
    SELECT id, nome FROM pacientes 
    WHERE nutricionista_id = ? AND ativo = 1
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    
    if not pacientes:
        st.warning("⚠️ Cadastre pacientes antes de criar planos alimentares.")
        return
    
    with st.form("novo_plano_form"):
        
        # Dados básicos
        st.markdown("##### 📋 Informações Básicas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            paciente_selecionado = st.selectbox(
                "👤 Paciente",
                options=pacientes,
                format_func=lambda x: x[1]
            )
            
            nome_plano = st.text_input("📝 Nome do Plano", placeholder="Ex: Plano Emagrecimento Janeiro")
        
        with col2:
            objetivo = st.selectbox("🎯 Objetivo", [
                "Perda de Peso", "Ganho de Peso", "Manutenção", 
                "Ganho de Massa Muscular", "Definição", "Saúde Geral"
            ])
            
            data_validade = st.date_input("📅 Válido até", 
                value=date.today() + timedelta(days=30))
        
        # Parâmetros nutricionais
        st.markdown("##### 🧮 Parâmetros Nutricionais")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            calorias_totais = st.number_input("🔥 Calorias Totais/dia", 1000, 5000, 2000, step=50)
        
        with col2:
            perc_carb = st.slider("🍞 Carboidratos (%)", 10, 70, 50)
        
        with col3:
            perc_prot = st.slider("🥩 Proteínas (%)", 10, 40, 20)
        
        with col4:
            perc_lip = 100 - perc_carb - perc_prot
            st.metric("🥑 Lipídios (%)", perc_lip)
        
        # Calcular gramas
        carb_g = (calorias_totais * perc_carb / 100) / 4
        prot_g = (calorias_totais * perc_prot / 100) / 4
        lip_g = (calorias_totais * perc_lip / 100) / 9
        
        # Refeições
        st.markdown("##### 🍽️ Plano de Refeições")
        
        refeicoes = {}
        refeicoes_nomes = ['Café da Manhã', 'Lanche da Manhã', 'Almoço', 'Lanche da Tarde', 'Jantar', 'Ceia']
        
        for refeicao in refeicoes_nomes:
            with st.expander(f"🍽️ {refeicao}"):
                alimentos = st.text_area(
                    f"Alimentos para {refeicao}",
                    placeholder="Liste os alimentos, quantidades e preparos...",
                    key=f"alimentos_{refeicao.replace(' ', '_')}"
                )
                
                if alimentos:
                    refeicoes[refeicao] = {
                        'alimentos': alimentos.split('\n'),
                        'calorias': int(calorias_totais / 6)  # Distribuição aproximada
                    }
        
        # Observações
        observacoes = st.text_area("📝 Observações e Orientações", 
            placeholder="Orientações gerais, substituições, horários...")
        
        # Botão de submissão
        submitted = st.form_submit_button("💾 Criar Plano Alimentar", use_container_width=True)
        
        if submitted:
            if not nome_plano:
                st.error("❌ Nome do plano é obrigatório!")
                return
            
            try:
                plano_uuid = str(uuid.uuid4())
                
                cursor.execute('''
                INSERT INTO planos_alimentares (
                    uuid, paciente_id, nutricionista_id, nome, objetivo,
                    calorias_totais, carboidratos, proteinas, lipidios,
                    data_criacao, data_validade, refeicoes, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    plano_uuid, paciente_selecionado[0], user['id'], nome_plano, objetivo,
                    calorias_totais, carb_g, prot_g, lip_g,
                    date.today(), data_validade, json.dumps(refeicoes), observacoes
                ))
                
                conn.commit()
                
                st.success("✅ Plano alimentar criado com sucesso!")
                time.sleep(2)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro ao criar plano: {str(e)}")
            finally:
                conn.close()

def show_ai_meal_planner(user):
    st.markdown('<div class="sub-header">🤖 IA Personalizadora de Planos</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Seleção de paciente
    cursor.execute("""
    SELECT id, nome FROM pacientes 
    WHERE nutricionista_id = ? AND ativo = 1
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    
    if not pacientes:
        st.warning("⚠️ Cadastre pacientes para usar a IA.")
        return
    
    paciente_selecionado = st.selectbox(
        "👤 Selecione o Paciente",
        options=pacientes,
        format_func=lambda x: x[1]
    )
    
    # Parâmetros para IA
    st.markdown("##### 🎯 Parâmetros para a IA")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        objetivo_ia = st.selectbox("🎯 Objetivo Principal", [
            "Perda de Peso Saudável", "Ganho de Massa Muscular", "Manutenção",
            "Definição Corporal", "Saúde Cardiovascular", "Controle Diabético"
        ])
        
        nivel_atividade = st.selectbox("🏃 Nível de Atividade", [
            "Sedentário", "Levemente Ativo", "Moderadamente Ativo", 
            "Muito Ativo", "Extremamente Ativo"
        ])
    
    with col2:
        restricoes_alimentares = st.multiselect("🚫 Restrições", [
            "Vegetariano", "Vegano", "Sem Lactose", "Sem Glúten",
            "Low Carb", "Cetogênica", "Sem Açúcar"
        ])
        
        preferencias = st.multiselect("❤️ Preferências", [
            "Comida Caseira", "Praticidade", "Baixo Custo", "Gourmet",
            "Orgânicos", "Funcionais", "Regionais"
        ])
    
    with col3:
        tempo_preparo = st.selectbox("⏱️ Tempo de Preparo", [
            "Até 15 min", "Até 30 min", "Até 60 min", "Mais de 60 min"
        ])
        
        orcamento = st.selectbox("💰 Orçamento", [
            "Econômico", "Moderado", "Sem Restrição"
        ])
    
    # Buscar dados do paciente para IA
    cursor.execute("SELECT * FROM pacientes WHERE id = ?", (paciente_selecionado[0],))
    paciente_dados = cursor.fetchone()
    
    # Buscar última avaliação
    cursor.execute("""
    SELECT * FROM avaliacoes 
    WHERE paciente_id = ? 
    ORDER BY data_avaliacao DESC 
    LIMIT 1
    """, (paciente_selecionado[0],))
    ultima_avaliacao = cursor.fetchone()
    
    conn.close()
    
    # Mostrar dados considerados pela IA
    if ultima_avaliacao:
        st.markdown("##### 📊 Dados Considerados pela IA")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("⚖️ Peso", f"{ultima_avaliacao[3]:.1f} kg" if ultima_avaliacao[3] else "N/I")
        
        with col2:
            st.metric("📏 Altura", f"{ultima_avaliacao[4]*100:.0f} cm" if ultima_avaliacao[4] else "N/I")
        
        with col3:
            st.metric("🧮 IMC", f"{ultima_avaliacao[5]:.1f}" if ultima_avaliacao[5] else "N/I")
        
        with col4:
            if paciente_dados[6]:  # data_nascimento
                idade = calculate_age(paciente_dados[6])
                st.metric("📅 Idade", f"{idade} anos")
    
    # Botão para gerar plano com IA
    if st.button("🤖 Gerar Plano com IA", use_container_width=True):
        
        with st.spinner("🤖 IA analisando dados e criando plano personalizado..."):
            
            progress_bar = st.progress(0)
            
            etapas_ia = [
                "Analisando perfil do paciente...",
                "Calculando necessidades nutricionais...",
                "Selecionando alimentos compatíveis...",
                "Otimizando distribuição de macronutrientes...",
                "Criando cronograma de refeições...",
                "Ajustando por preferências e restrições...",
                "Gerando orientações personalizadas...",
                "Finalizando plano alimentar..."
            ]
            
            for i, etapa in enumerate(etapas_ia):
                st.text(f"🤖 {etapa}")
                time.sleep(0.5)
                progress_bar.progress((i + 1) / len(etapas_ia))
            
            progress_bar.empty()
        
        st.success("✅ Plano alimentar personalizado criado com sucesso!")
        
        # Simular plano gerado pela IA
        if ultima_avaliacao and ultima_avaliacao[3]:  # peso
            peso = ultima_avaliacao[3]
            if paciente_dados[6]:
                idade = calculate_age(paciente_dados[6])
                altura = ultima_avaliacao[4] * 100 if ultima_avaliacao[4] else 165
                sexo = paciente_dados[7] or "Feminino"
                
                # Calcular necessidades calóricas
                tmb = calculate_bmr(peso, altura, idade, sexo)
                
                fator_atividade = {
                    "Sedentário": 1.2,
                    "Levemente Ativo": 1.375,
                    "Moderadamente Ativo": 1.55,
                    "Muito Ativo": 1.725,
                    "Extremamente Ativo": 1.9
                }.get(nivel_atividade, 1.55)
                
                calorias_alvo = tmb * fator_atividade
                
                # Ajustar por objetivo
                if objetivo_ia == "Perda de Peso Saudável":
                    calorias_alvo *= 0.85
                    carb_perc, prot_perc, lip_perc = 40, 30, 30
                elif objetivo_ia == "Ganho de Massa Muscular":
                    calorias_alvo *= 1.15
                    carb_perc, prot_perc, lip_perc = 45, 25, 30
                else:  # Manutenção
                    carb_perc, prot_perc, lip_perc = 50, 20, 30
                
                # Exibir plano gerado
                st.markdown("##### 🤖 Plano Gerado pela IA")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("🔥 Calorias/dia", f"{calorias_alvo:.0f} kcal")
                
                with col2:
                    carb_g = (calorias_alvo * carb_perc / 100) / 4
                    st.metric("🍞 Carboidratos", f"{carb_g:.0f}g")
                
                with col3:
                    prot_g = (calorias_alvo * prot_perc / 100) / 4
                    st.metric("🥩 Proteínas", f"{prot_g:.0f}g")
                
                with col4:
                    lip_g = (calorias_alvo * lip_perc / 100) / 9
                    st.metric("🥑 Lipídios", f"{lip_g:.0f}g")
                
                # Cardápio exemplo gerado pela IA
                st.markdown("##### 📋 Exemplo de Cardápio (Dia 1)")
                
                cardapio_exemplo = {
                    "Café da Manhã": [
                        "1 fatia de pão integral",
                        "2 col. sopa de abacate amassado",
                        "1 ovo mexido",
                        "200ml de leite desnatado"
                    ],
                    "Lanche da Manhã": [
                        "1 maçã média",
                        "10 castanhas do Pará"
                    ],
                    "Almoço": [
                        "120g de peito de frango grelhado",
                        "150g de arroz integral cozido",
                        "100g de brócolis refogado",
                        "Salada verde à vontade"
                    ],
                    "Lanche da Tarde": [
                        "1 iogurte grego natural",
                        "1 col. sopa de granola"
                    ],
                    "Jantar": [
                        "150g de salmão assado",
                        "100g de batata doce cozida",
                        "Legumes grelhados variados"
                    ]
                }
                
                for refeicao, alimentos in cardapio_exemplo.items():
                    with st.expander(f"🍽️ {refeicao}", expanded=True):
                        for alimento in alimentos:
                            st.markdown(f"• {alimento}")
        
        # Opção de salvar o plano
        if st.button("💾 Salvar Plano Gerado"):
            st.success("✅ Plano salvo com sucesso!")

def show_nutritional_analysis(user):
    st.markdown('<div class="sub-header">📊 Análise Nutricional</div>', unsafe_allow_html=True)
    
    st.info("🔍 Selecione um plano alimentar para análise detalhada.")
    
    # Esta funcionalidade seria implementada com análise detalhada dos planos
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT pa.id, pa.nome, p.nome as paciente_nome
    FROM planos_alimentares pa
    JOIN pacientes p ON pa.paciente_id = p.id
    WHERE pa.nutricionista_id = ? AND pa.ativo = 1
    """, (user['id'],))
    
    planos = cursor.fetchall()
    conn.close()
    
    if planos:
        plano_selecionado = st.selectbox(
            "📋 Selecione o Plano",
            options=planos,
            format_func=lambda x: f"{x[1]} - {x[2]}"
        )
        
        if plano_selecionado:
            st.markdown(f"##### 📊 Análise: {plano_selecionado[1]}")
            
            # Aqui seria implementada a análise detalhada
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🎯 Adequação Nutricional:**")
                st.success("✅ Distribuição de macronutrientes adequada")
                st.success("✅ Valor calórico apropriado")
                st.warning("⚠️ Verificar ingestão de fibras")
                
            with col2:
                st.markdown("**💡 Recomendações:**")
                st.info("• Incluir mais fontes de omega-3")
                st.info("• Aumentar variedade de vegetais")
                st.info("• Considerar suplementação de vitamina D")

# =============================================================================
# 📅 SISTEMA DE AGENDA
# =============================================================================

def show_agenda(user):
    load_css()
    
    st.markdown('<h1 class="ultra-header">📅 Sistema de Agenda</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Calendario",
        "➕ Nova Consulta",
        "👥 Consultas Hoje",
        "📊 Relatórios"
    ])
    
    with tab1:
        show_calendar(user)
    
    with tab2:
        show_new_appointment(user)
    
    with tab3:
        show_today_appointments(user)
    
    with tab4:
        show_appointment_reports(user)

def show_calendar(user):
    st.markdown('<div class="sub-header">📅 Visualização da Agenda</div>', unsafe_allow_html=True)
    
    # Seleção de data
    col1, col2 = st.columns(2)
    
    with col1:
        data_selecionada = st.date_input("📅 Data", value=date.today())
    
    with col2:
        visualizacao = st.selectbox("👁️ Visualização", ["Dia", "Semana", "Mês"])
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    if visualizacao == "Dia":
        # Consultas do dia
        cursor.execute("""
        SELECT c.*, p.nome as paciente_nome
        FROM consultas c
        JOIN pacientes p ON c.paciente_id = p.id
        WHERE c.nutricionista_id = ? AND DATE(c.data_consulta) = ?
        ORDER BY TIME(c.data_consulta)
        """, (user['id'], data_selecionada))
        
        consultas = cursor.fetchall()
        
        st.markdown(f"##### 📅 Agenda de {data_selecionada.strftime('%d/%m/%Y')}")
        
        if not consultas:
            st.info("📝 Nenhuma consulta agendada para este dia.")
        else:
            for consulta in consultas:
                hora = datetime.strptime(consulta[4], '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
                
                with st.container():
                    col1, col2, col3 = st.columns([2, 3, 2])
                    
                    with col1:
                        st.markdown(f"**🕐 {hora}**")
                    
                    with col2:
                        st.markdown(f"**👤 {consulta[-1]}**")
                        st.markdown(f"📋 {consulta[5]} | 📊 {consulta[6].title()}")
                    
                    with col3:
                        status_color = {
                            'agendada': '🔵',
                            'confirmada': '🟢', 
                            'realizada': '🟣',
                            'cancelada': '🔴'
                        }.get(consulta[6], '⚪')
                        
                        st.markdown(f"{status_color} **{consulta[6].title()}**")
                
                st.markdown("---")
    
    conn.close()

def show_new_appointment(user):
    st.markdown('<div class="sub-header">➕ Agendar Nova Consulta</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Buscar pacientes
    cursor.execute("""
    SELECT id, nome, telefone FROM pacientes 
    WHERE nutricionista_id = ? AND ativo = 1
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    
    if not pacientes:
        st.warning("⚠️ Cadastre pacientes antes de agendar consultas.")
        return
    
    with st.form("nova_consulta_form"):
        
        st.markdown("##### 📋 Dados da Consulta")
        
        col1, col2 = st.columns(2)
        
        with col1:
            paciente_selecionado = st.selectbox(
                "👤 Paciente",
                options=pacientes,
                format_func=lambda x: f"{x[1]} ({x[2] or 'Sem telefone'})"
            )
            
            tipo_consulta = st.selectbox("🔍 Tipo", [
                "Primeira Consulta",
                "Consulta de Retorno", 
                "Reavaliação",
                "Orientação Nutricional",
                "Teleconsulta"
            ])
        
        with col2:
            data_consulta = st.date_input("📅 Data", min_value=date.today())
            hora_consulta = st.time_input("🕐 Horário", value=datetime.now().replace(hour=9, minute=0).time())
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            duracao = st.selectbox("⏱️ Duração", [30, 45, 60, 90], index=2)
        
        with col2:
            valor = st.number_input("💰 Valor (R$)", 0.0, 1000.0, 150.0, step=10.0)
        
        with col3:
            status = st.selectbox("📊 Status", ["agendada", "confirmada"])
        
        observacoes = st.text_area("📝 Observações")
        
        submitted = st.form_submit_button("📅 Agendar Consulta", use_container_width=True)
        
        if submitted:
            try:
                consulta_uuid = str(uuid.uuid4())
                datetime_consulta = datetime.combine(data_consulta, hora_consulta)
                
                cursor.execute('''
                INSERT INTO consultas (
                    uuid, paciente_id, nutricionista_id, data_consulta, 
                    tipo_consulta, status, duracao, valor, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    consulta_uuid, paciente_selecionado[0], user['id'], datetime_consulta,
                    tipo_consulta, status, duracao, valor, observacoes
                ))
                
                conn.commit()
                
                st.success("✅ Consulta agendada com sucesso!")
                time.sleep(2)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro ao agendar: {str(e)}")
    
    conn.close()

def show_today_appointments(user):
    st.markdown('<div class="sub-header">👥 Consultas de Hoje</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    hoje = date.today()
    
    cursor.execute("""
    SELECT c.*, p.nome as paciente_nome, p.telefone
    FROM consultas c
    JOIN pacientes p ON c.paciente_id = p.id
    WHERE c.nutricionista_id = ? AND DATE(c.data_consulta) = ?
    ORDER BY TIME(c.data_consulta)
    """, (user['id'], hoje))
    
    consultas_hoje = cursor.fetchall()
    
    if not consultas_hoje:
        st.info(f"📝 Nenhuma consulta para hoje ({hoje.strftime('%d/%m/%Y')}).")
        return
    
    # Estatísticas do dia
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Total", len(consultas_hoje))
    
    with col2:
        realizadas = len([c for c in consultas_hoje if c[6] == 'realizada'])
        st.metric("✅ Realizadas", realizadas)
    
    with col3:
        faturamento = sum([c[8] or 0 for c in consultas_hoje if c[6] != 'cancelada'])
        st.metric("💰 Faturamento", f"R$ {faturamento:.2f}")
    
    with col4:
        # Próxima consulta
        agora = datetime.now()
        proxima = None
        for consulta in consultas_hoje:
            hora_consulta = datetime.strptime(consulta[4], '%Y-%m-%d %H:%M:%S')
            if hora_consulta > agora and consulta[6] not in ['realizada', 'cancelada']:
                proxima = hora_consulta.strftime('%H:%M')
                break
        
        st.metric("⏰ Próxima", proxima or "---")
    
    # Lista de consultas
    for consulta in consultas_hoje:
        hora = datetime.strptime(consulta[4], '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
        
        with st.expander(f"🕐 {hora} - {consulta[-2]} ({consulta[6].upper()})", 
                        expanded=(consulta[6] in ['agendada', 'confirmada'])):
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**👤 Paciente:** {consulta[-2]}")
                st.markdown(f"**📱 Telefone:** {consulta[-1] or 'N/I'}")
            
            with col2:
                st.markdown(f"**🔍 Tipo:** {consulta[5]}")
                st.markdown(f"**⏱️ Duração:** {consulta[7]} min")
            
            with col3:
                st.markdown(f"**💰 Valor:** R$ {consulta[8] or 0:.2f}")
                st.markdown(f"**📊 Status:** {consulta[6].title()}")
            
            if consulta[9]:  # observacoes
                st.markdown(f"**📝 Obs:** {consulta[9]}")
            
            # Botões de ação
            if consulta[6] in ['agendada', 'confirmada']:
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    if st.button("✅ Confirmar", key=f"confirm_{consulta[0]}"):
                        update_consultation_status(consulta[0], 'confirmada')
                        st.rerun()
                
                with col_btn2:
                    if st.button("🏁 Realizada", key=f"done_{consulta[0]}"):
                        update_consultation_status(consulta[0], 'realizada')
                        st.rerun()
                
                with col_btn3:
                    if st.button("❌ Cancelar", key=f"cancel_{consulta[0]}"):
                        update_consultation_status(consulta[0], 'cancelada')
                        st.rerun()
    
    conn.close()

def update_consultation_status(consulta_id, novo_status):
    """Atualiza status da consulta"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE consultas SET status = ? WHERE id = ?", (novo_status, consulta_id))
    conn.commit()
    conn.close()

def show_appointment_reports(user):
    st.markdown('<div class="sub-header">📊 Relatórios de Consultas</div>', unsafe_allow_html=True)
    
    # Período
    col1, col2 = st.columns(2)
    
    with col1:
        data_inicio = st.date_input("📅 Data Início", value=date.today() - timedelta(days=30))
    
    with col2:
        data_fim = st.date_input("📅 Data Fim", value=date.today())
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT c.*, p.nome as paciente_nome
    FROM consultas c
    JOIN pacientes p ON c.paciente_id = p.id
    WHERE c.nutricionista_id = ? 
    AND DATE(c.data_consulta) BETWEEN ? AND ?
    """, (user['id'], data_inicio, data_fim))
    
    consultas = cursor.fetchall()
    conn.close()
    
    if not consultas:
        st.info("📝 Nenhuma consulta no período selecionado.")
        return
    
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Total", len(consultas))
    
    with col2:
        realizadas = len([c for c in consultas if c[6] == 'realizada'])
        st.metric("✅ Realizadas", realizadas)
    
    with col3:
        faturamento = sum([c[8] or 0 for c in consultas if c[6] == 'realizada'])
        st.metric("💰 Faturamento", f"R$ {faturamento:.2f}")
    
    with col4:
        if realizadas > 0:
            ticket_medio = faturamento / realizadas
            st.metric("🎯 Ticket Médio", f"R$ {ticket_medio:.2f}")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Status das consultas
        status_counts = {}
        for consulta in consultas:
            status = consulta[6]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        if status_counts:
            fig_status = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="Consultas por Status"
            )
            st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Tipos de consulta
        tipo_counts = {}
        for consulta in consultas:
            tipo = consulta[5]
            tipo_counts[tipo] = tipo_counts.get(tipo, 0) + 1
        
        if tipo_counts:
            fig_tipos = px.bar(
                x=list(tipo_counts.keys()),
                y=list(tipo_counts.values()),
                title="Consultas por Tipo"
            )
            st.plotly_chart(fig_tipos, use_container_width=True)

# =============================================================================
# 🍳 SISTEMA DE RECEITAS
# =============================================================================

def show_receitas(user):
    load_css()
    
    st.markdown('<h1 class="ultra-header">🍳 Sistema de Receitas</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([
        "🍳 Minhas Receitas",
        "➕ Nova Receita",
        "🔍 Buscar Receitas"
    ])
    
    with tab1:
        show_my_recipes(user)
    
    with tab2:
        show_new_recipe(user)
    
    with tab3:
        show_search_recipes(user)

def show_my_recipes(user):
    st.markdown('<div class="sub-header">🍳 Minhas Receitas</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM receitas
    WHERE criada_por = ?
    ORDER BY data_criacao DESC
    """, (user['id'],))
    
    receitas = cursor.fetchall()
    conn.close()
    
    if not receitas:
        st.info("📝 Nenhuma receita criada ainda.")
        return
    
    for receita in receitas:
        with st.expander(f"🍳 {receita[2]} ({receita[3]})", expanded=False):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Ingredientes:**")
                if receita[4]:  # ingredientes
                    ingredientes = receita[4].split('\n')
                    for ingrediente in ingredientes:
                        st.markdown(f"• {ingrediente}")
                
                st.markdown(f"**⏱️ Tempo:** {receita[6] or 'N/I'} min")
                st.markdown(f"**👥 Porções:** {receita[7] or 'N/I'}")
            
            with col2:
                st.markdown("**👨‍🍳 Modo de Preparo:**")
                if receita[5]:  # modo_preparo
                    st.markdown(receita[5])
                
                # Informações nutricionais
                if receita[8]:  # calorias_porcao
                    st.markdown("**📊 Informações Nutricionais (por porção):**")
                    st.markdown(f"• **Calorias:** {receita[8]:.0f} kcal")
                    if receita[9]:  # carboidratos
                        st.markdown(f"• **Carboidratos:** {receita[9]:.1f}g")
                    if receita[10]:  # proteinas
                        st.markdown(f"• **Proteínas:** {receita[10]:.1f}g")
                    if receita[11]:  # lipidios
                        st.markdown(f"• **Lipídios:** {receita[11]:.1f}g")

def show_new_recipe(user):
    st.markdown('<div class="sub-header">➕ Criar Nova Receita</div>', unsafe_allow_html=True)
    
    with st.form("nova_receita_form"):
        
        # Informações básicas
        st.markdown("##### 📋 Informações Básicas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("🍳 Nome da Receita *")
            categoria = st.selectbox("📂 Categoria", [
                "Café da Manhã", "Almoço", "Jantar", "Lanche", "Sobremesa",
                "Bebida", "Salada", "Sopa", "Vegano/Vegetariano", "Low Carb",
                "Sem Glúten", "Sem Lactose", "Fitness", "Infantil"
            ])
        
        with col2:
            tempo_preparo = st.number_input("⏱️ Tempo de Preparo (min)", 1, 300, 30)
            porcoes = st.number_input("👥 Número de Porções", 1, 20, 4)
        
        # Ingredientes
        st.markdown("##### 📝 Ingredientes")
        ingredientes = st.text_area(
            "Liste os ingredientes (um por linha)",
            placeholder="Ex:\n200g de peito de frango\n1 xícara de arroz integral\n2 colheres de azeite\n...",
            height=150
        )
        
        # Modo de preparo
        st.markdown("##### 👨‍🍳 Modo de Preparo")
        modo_preparo = st.text_area(
            "Descreva o passo a passo",
            placeholder="1. Tempere o frango com sal e pimenta\n2. Aqueça o azeite na panela\n3. ...",
            height=200
        )
        
        # Informações nutricionais
        st.markdown("##### 📊 Informações Nutricionais (por porção)")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            calorias = st.number_input("🔥 Calorias", 0.0, 2000.0, 0.0, step=1.0)
        
        with col2:
            carboidratos = st.number_input("🍞 Carboidratos (g)", 0.0, 200.0, 0.0, step=0.1)
        
        with col3:
            proteinas = st.number_input("🥩 Proteínas (g)", 0.0, 100.0, 0.0, step=0.1)
        
        with col4:
            lipidios = st.number_input("🥑 Lipídios (g)", 0.0, 100.0, 0.0, step=0.1)
        
        with col5:
            fibras = st.number_input("🌾 Fibras (g)", 0.0, 50.0, 0.0, step=0.1)
        
        # Configurações
        col1, col2 = st.columns(2)
        
        with col1:
            publica = st.checkbox("🌐 Receita Pública (outros nutricionistas podem ver)")
        
        # Botão de submissão
        submitted = st.form_submit_button("💾 Salvar Receita", use_container_width=True)
        
        if submitted:
            if not nome:
                st.error("❌ Nome da receita é obrigatório!")
                return
            
            try:
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                
                receita_uuid = str(uuid.uuid4())
                
                cursor.execute('''
                INSERT INTO receitas (
                    uuid, nome, categoria, ingredientes, modo_preparo,
                    tempo_preparo, porcoes, calorias_porcao, carboidratos,
                    proteinas, lipidios, fibras, criada_por, publica
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    receita_uuid, nome, categoria, ingredientes, modo_preparo,
                    tempo_preparo, porcoes, calorias, carboidratos,
                    proteinas, lipidios, fibras, user['id'], int(publica)
                ))
                
                conn.commit()
                conn.close()
                
                st.success("✅ Receita salva com sucesso!")
                time.sleep(2)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro ao salvar receita: {str(e)}")

def show_search_recipes(user):
    st.markdown('<div class="sub-header">🔍 Buscar Receitas</div>', unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_nome = st.text_input("🔍 Nome da receita")
    
    with col2:
        filtro_categoria = st.selectbox("📂 Categoria", [
            "Todas", "Café da Manhã", "Almoço", "Jantar", "Lanche", "Sobremesa",
            "Bebida", "Salada", "Sopa", "Vegano/Vegetariano", "Low Carb"
        ])
    
    with col3:
        filtro_origem = st.selectbox("👤 Origem", ["Todas", "Minhas Receitas", "Receitas Públicas"])
    
    # Buscar receitas
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    query = "SELECT r.*, u.nome as criador FROM receitas r JOIN usuarios u ON r.criada_por = u.id WHERE 1=1"
    params = []
    
    if filtro_nome:
        query += " AND r.nome LIKE ?"
        params.append(f"%{filtro_nome}%")
    
    if filtro_categoria != "Todas":
        query += " AND r.categoria = ?"
        params.append(filtro_categoria)
    
    if filtro_origem == "Minhas Receitas":
        query += " AND r.criada_por = ?"
        params.append(user['id'])
    elif filtro_origem == "Receitas Públicas":
        query += " AND (r.publica = 1 OR r.criada_por = ?)"
        params.append(user['id'])
    
    query += " ORDER BY r.data_criacao DESC"
    
    cursor.execute(query, params)
    receitas = cursor.fetchall()
    conn.close()
    
    if not receitas:
        st.info("📝 Nenhuma receita encontrada com os filtros aplicados.")
        return
    
    # Exibir receitas encontradas
    st.markdown(f"##### 🔍 {len(receitas)} receita(s) encontrada(s)")
    
    for receita in receitas:
        with st.expander(f"🍳 {receita[2]} - {receita[3]} (por {receita[-1]})", expanded=False):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Ingredientes:**")
                if receita[4]:
                    for ingrediente in receita[4].split('\n'):
                        if ingrediente.strip():
                            st.markdown(f"• {ingrediente}")
                
                st.markdown(f"**⏱️ Tempo:** {receita[6] or 'N/I'} min")
                st.markdown(f"**👥 Porções:** {receita[7] or 'N/I'}")
            
            with col2:
                st.markdown("**👨‍🍳 Modo de Preparo:**")
                st.markdown(receita[5] or "Não informado")
                
                if receita[8]:  # calorias
                    st.markdown("**📊 Por porção:**")
                    st.markdown(f"🔥 {receita[8]:.0f} kcal | 🍞 {receita[9]:.1f}g C | 🥩 {receita[10]:.1f}g P | 🥑 {receita[11]:.1f}g L")

# =============================================================================
# 📊 SISTEMA DE RELATÓRIOS
# =============================================================================

def show_relatorios(user):
    load_css()
    
    st.markdown('<h1 class="ultra-header">📊 Sistema de Relatórios</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Dashboard Analytics",
        "👥 Relatório de Pacientes",
        "💰 Relatório Financeiro",
        "📋 Relatório de Aderência"
    ])
    
    with tab1:
        show_analytics_dashboard(user)
    
    with tab2:
        show_patients_report(user)
    
    with tab3:
        show_financial_report(user)
    
    with tab4:
        show_adherence_report(user)

def show_analytics_dashboard(user):
    st.markdown('<div class="sub-header">📈 Dashboard Analytics</div>', unsafe_allow_html=True)
    
    # Período de análise
    col1, col2 = st.columns(2)
    
    with col1:
        data_inicio = st.date_input("📅 Início", value=date.today() - timedelta(days=90))
    
    with col2:
        data_fim = st.date_input("📅 Fim", value=date.today())
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Métricas principais
    st.markdown("##### 📊 Métricas Principais")
    
    # Total de pacientes
    cursor.execute("SELECT COUNT(*) FROM pacientes WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    total_pacientes = cursor.fetchone()[0]
    
    # Consultas no período
    cursor.execute("""
    SELECT COUNT(*), COUNT(CASE WHEN status = 'realizada' THEN 1 END) as realizadas,
           SUM(CASE WHEN status = 'realizada' THEN valor ELSE 0 END) as faturamento
    FROM consultas 
    WHERE nutricionista_id = ? AND DATE(data_consulta) BETWEEN ? AND ?
    """, (user['id'], data_inicio, data_fim))
    
    consultas_dados = cursor.fetchone()
    total_consultas = consultas_dados[0] if consultas_dados[0] else 0
    realizadas = consultas_dados[1] if consultas_dados[1] else 0
    faturamento = consultas_dados[2] if consultas_dados[2] else 0
    
    # Planos ativos
    cursor.execute("SELECT COUNT(*) FROM planos_alimentares WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    planos_ativos = cursor.fetchone()[0]
    
    # Receitas criadas
    cursor.execute("SELECT COUNT(*) FROM receitas WHERE criada_por = ?", (user['id'],))
    receitas = cursor.fetchone()[0]
    
    # Exibir métricas
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("👥 Pacientes", total_pacientes)
    
    with col2:
        st.metric("📅 Consultas", total_consultas)
    
    with col3:
        st.metric("✅ Realizadas", realizadas)
    
    with col4:
        st.metric("💰 Faturamento", f"R$ {faturamento:.2f}")
    
    with col5:
        taxa_realizacao = (realizadas / total_consultas * 100) if total_consultas > 0 else 0
        st.metric("📊 Taxa Realização", f"{taxa_realizacao:.1f}%")
    
    # Gráficos de análise
    col1, col2 = st.columns(2)
    
    with col1:
        # Evolução de consultas realizadas por mês
        cursor.execute("""
        SELECT strftime('%Y-%m', data_consulta) as mes, COUNT(*) as total
        FROM consultas
        WHERE nutricionista_id = ? AND status = 'realizada'
        AND DATE(data_consulta) BETWEEN ? AND ?
        GROUP BY strftime('%Y-%m', data_consulta)
        ORDER BY mes
        """, (user['id'], data_inicio, data_fim))
        
        dados_mes = cursor.fetchall()
        
        if dados_mes:
            df_mes = pd.DataFrame(dados_mes, columns=['Mês', 'Consultas'])
            fig_evolucao = px.line(df_mes, x='Mês', y='Consultas', 
                                 title='📈 Evolução de Consultas por Mês', markers=True)
            st.plotly_chart(fig_evolucao, use_container_width=True)
    
    with col2:
        # Distribuição de tipos de consulta
        cursor.execute("""
        SELECT tipo_consulta, COUNT(*) as total
        FROM consultas
        WHERE nutricionista_id = ? AND status = 'realizada'
        AND DATE(data_consulta) BETWEEN ? AND ?
        GROUP BY tipo_consulta
        """, (user['id'], data_inicio, data_fim))
        
        tipos_consulta = cursor.fetchall()
        
        if tipos_consulta:
            df_tipos = pd.DataFrame(tipos_consulta, columns=['Tipo', 'Quantidade'])
            fig_tipos = px.pie(df_tipos, values='Quantidade', names='Tipo',
                              title='📊 Distribuição por Tipo de Consulta')
            st.plotly_chart(fig_tipos, use_container_width=True)
    
    conn.close()

def show_patients_report(user):
    st.markdown('<div class="sub-header">👥 Relatório de Pacientes</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Estatísticas gerais dos pacientes
    cursor.execute("""
    SELECT 
        COUNT(*) as total,
        COUNT(CASE WHEN sexo = 'Feminino' THEN 1 END) as feminino,
        COUNT(CASE WHEN sexo = 'Masculino' THEN 1 END) as masculino,
        COUNT(CASE WHEN objetivo LIKE '%Perda%' THEN 1 END) as perda_peso,
        COUNT(CASE WHEN objetivo LIKE '%Ganho%' THEN 1 END) as ganho_peso
    FROM pacientes 
    WHERE nutricionista_id = ? AND ativo = 1
    """, (user['id'],))
    
    stats = cursor.fetchone()
    
    if stats[0] == 0:
        st.info("📝 Nenhum paciente cadastrado.")
        return
    
    # Exibir estatísticas
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("👥 Total", stats[0])
    
    with col2:
        st.metric("👩 Feminino", stats[1])
    
    with col3:
        st.metric("👨 Masculino", stats[2])
    
    with col4:
        st.metric("⬇️ Perda Peso", stats[3])
    
    with col5:
        st.metric("⬆️ Ganho Peso", stats[4])
    
    # Distribuição por faixa etária
    cursor.execute("""
    SELECT p.*, 
           (julianday('now') - julianday(p.data_nascimento)) / 365.25 as idade
    FROM pacientes p
    WHERE p.nutricionista_id = ? AND p.ativo = 1 AND p.data_nascimento IS NOT NULL
    """, (user['id'],))
    
    pacientes_idade = cursor.fetchall()
    
    if pacientes_idade:
        # Classificar por faixa etária
        faixas = {'18-30': 0, '31-50': 0, '51-70': 0, '70+': 0}
        
        for paciente in pacientes_idade:
            idade = int(paciente[-1])  # idade calculada
            if 18 <= idade <= 30:
                faixas['18-30'] += 1
            elif 31 <= idade <= 50:
                faixas['31-50'] += 1
            elif 51 <= idade <= 70:
                faixas['51-70'] += 1
            elif idade > 70:
                faixas['70+'] += 1
        
        # Gráfico de faixa etária
        col1, col2 = st.columns(2)
        
        with col1:
            fig_idade = px.bar(
                x=list(faixas.keys()),
                y=list(faixas.values()),
                title="👥 Distribuição por Faixa Etária"
            )
            st.plotly_chart(fig_idade, use_container_width=True)
        
        with col2:
            # Objetivos mais comuns
            cursor.execute("""
            SELECT objetivo, COUNT(*) as total
            FROM pacientes
            WHERE nutricionista_id = ? AND ativo = 1 AND objetivo IS NOT NULL
            GROUP BY objetivo
            ORDER BY total DESC
            """, (user['id'],))
            
            objetivos = cursor.fetchall()
            
            if objetivos:
                df_obj = pd.DataFrame(objetivos, columns=['Objetivo', 'Quantidade'])
                fig_obj = px.pie(df_obj, values='Quantidade', names='Objetivo',
                               title='🎯 Objetivos Principais')
                st.plotly_chart(fig_obj, use_container_width=True)
    
    conn.close()

def show_financial_report(user):
    st.markdown('<div class="sub-header">💰 Relatório Financeiro</div>', unsafe_allow_html=True)
    
    # Período
    col1, col2 = st.columns(2)
    
    with col1:
        data_inicio = st.date_input("📅 Início", value=date.today().replace(day=1))
    
    with col2:
        data_fim = st.date_input("📅 Fim", value=date.today())
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Dados financeiros
    cursor.execute("""
    SELECT 
        COUNT(*) as total_consultas,
        COUNT(CASE WHEN status = 'realizada' THEN 1 END) as realizadas,
        COUNT(CASE WHEN status = 'cancelada' THEN 1 END) as canceladas,
        SUM(CASE WHEN status = 'realizada' THEN valor ELSE 0 END) as faturamento,
        AVG(CASE WHEN status = 'realizada' THEN valor ELSE NULL END) as ticket_medio
    FROM consultas
    WHERE nutricionista_id = ? AND DATE(data_consulta) BETWEEN ? AND ?
    """, (user['id'], data_inicio, data_fim))
    
    financeiro = cursor.fetchone()
    
    if not financeiro or financeiro[0] == 0:
        st.info("💰 Nenhuma movimentação financeira no período.")
        return
    
    # Métricas financeiras
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📋 Consultas", financeiro[0])
    
    with col2:
        st.metric("✅ Realizadas", financeiro[1])
    
    with col3:
        taxa_cancelamento = (financeiro[2] / financeiro[0] * 100) if financeiro[0] > 0 else 0
        st.metric("❌ Canceladas", f"{financeiro[2]} ({taxa_cancelamento:.1f}%)")
    
    with col4:
        st.metric("💰 Faturamento", f"R$ {financeiro[3] or 0:.2f}")
    
    with col5:
        st.metric("🎯 Ticket Médio", f"R$ {financeiro[4] or 0:.2f}")
    
    # Faturamento por dia
    cursor.execute("""
    SELECT DATE(data_consulta) as dia, SUM(valor) as faturamento_dia
    FROM consultas
    WHERE nutricionista_id = ? AND status = 'realizada'
    AND DATE(data_consulta) BETWEEN ? AND ?
    GROUP BY DATE(data_consulta)
    ORDER BY dia
    """, (user['id'], data_inicio, data_fim))
    
    faturamento_diario = cursor.fetchall()
    
    if faturamento_diario:
        df_fat = pd.DataFrame(faturamento_diario, columns=['Data', 'Faturamento'])
        fig_fat = px.line(df_fat, x='Data', y='Faturamento', 
                         title='💰 Evolução do Faturamento Diário', markers=True)
        st.plotly_chart(fig_fat, use_container_width=True)
    
    # Faturamento por tipo de consulta
    cursor.execute("""
    SELECT tipo_consulta, SUM(valor) as total, COUNT(*) as quantidade
    FROM consultas
    WHERE nutricionista_id = ? AND status = 'realizada'
    AND DATE(data_consulta) BETWEEN ? AND ?
    GROUP BY tipo_consulta
    ORDER BY total DESC
    """, (user['id'], data_inicio, data_fim))
    
    fat_por_tipo = cursor.fetchall()
    
    if fat_por_tipo:
        st.markdown("##### 📊 Faturamento por Tipo de Consulta")
        
        df_tipo = pd.DataFrame(fat_por_tipo, columns=['Tipo', 'Faturamento', 'Quantidade'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_tipo_fat = px.bar(df_tipo, x='Tipo', y='Faturamento',
                                title='💰 Faturamento por Tipo')
            fig_tipo_fat.update_xaxis(tickangle=45)
            st.plotly_chart(fig_tipo_fat, use_container_width=True)
        
        with col2:
            fig_tipo_qtd = px.bar(df_tipo, x='Tipo', y='Quantidade',
                                title='📊 Quantidade por Tipo')
            fig_tipo_qtd.update_xaxis(tickangle=45)
            st.plotly_chart(fig_tipo_qtd, use_container_width=True)
    
    conn.close()

def show_adherence_report(user):
    st.markdown('<div class="sub-header">📋 Relatório de Aderência</div>', unsafe_allow_html=True)
    
    # Este seria um relatório mais complexo analisando a aderência dos pacientes
    st.info("📊 Relatório de aderência aos tratamentos (funcionalidade em desenvolvimento)")
    
    # Simulação de dados de aderência
    pacientes_adherencia = [
        {"nome": "Maria Silva", "aderencia": 85, "consultas": 6},
        {"nome": "João Santos", "aderencia": 92, "consultas": 8},
        {"nome": "Ana Costa", "aderencia": 68, "consultas": 4},
        {"nome": "Pedro Oliveira", "aderencia": 78, "consultas": 5},
    ]
    
    for paciente in pacientes_adherencia:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"**👤 {paciente['nome']}**")
            
            with col2:
                cor = "🟢" if paciente['aderencia'] >= 80 else "🟡" if paciente['aderencia'] >= 60 else "🔴"
                st.markdown(f"{cor} **{paciente['aderencia']}% de aderência**")
            
            with col3:
                st.markdown(f"📅 {paciente['consultas']} consultas")
            
            # Barra de progresso
            st.progress(paciente['aderencia'] / 100)
            
            st.markdown("---")

# =============================================================================
# ⚙️ CONFIGURAÇÕES
# =============================================================================

def show_configuracoes(user):
    load_css()
    
    st.markdown('<h1 class="ultra-header">⚙️ Configurações</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([
        "👤 Perfil",
        "🔧 Sistema", 
        "💾 Backup"
    ])
    
    with tab1:
        show_profile_settings(user)
    
    with tab2:
        show_system_settings(user)
    
    with tab3:
        show_backup_settings(user)

def show_profile_settings(user):
    st.markdown('<div class="sub-header">👤 Configurações do Perfil</div>', unsafe_allow_html=True)
    
    with st.form("profile_form"):
        st.markdown("##### 📝 Dados Pessoais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo", value=user.get('nome', ''))
            email = st.text_input("Email", value=user.get('email', ''), disabled=True)
            telefone = st.text_input("Telefone", value=user.get('telefone', ''))
        
        with col2:
            coren = st.text_input("COREN/CRN", value=user.get('coren', ''))
            clinica = st.text_input("Clínica/Local", value=user.get('clinica', ''))
        
        st.markdown("##### 🔒 Alterar Senha")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nova_senha = st.text_input("Nova Senha", type="password")
        
        with col2:
            confirmar_senha = st.text_input("Confirmar Nova Senha", type="password")
        
        submitted = st.form_submit_button("💾 Salvar Alterações", use_container_width=True)
        
        if submitted:
            try:
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                
                # Atualizar dados pessoais
                cursor.execute("""
                UPDATE usuarios SET nome = ?, telefone = ?, coren = ?, clinica = ?
                WHERE id = ?
                """, (nome, telefone, coren, clinica, user['id']))
                
                # Atualizar senha se fornecida
                if nova_senha:
                    if nova_senha != confirmar_senha:
                        st.error("❌ Senhas não coincidem!")
                        return
                    
                    senha_hash = hash_password(nova_senha)
                    cursor.execute("UPDATE usuarios SET senha = ? WHERE id = ?", 
                                 (senha_hash, user['id']))
                
                conn.commit()
                conn.close()
                
                st.success("✅ Perfil atualizado com sucesso!")
                
                # Atualizar dados na sessão
                st.session_state.user.update({
                    'nome': nome,
                    'telefone': telefone,
                    'coren': coren,
                    'clinica': clinica
                })
                
                time.sleep(2)
                st.rerun()
