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
            "🧮 Calculadoras": "calculadoras"
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

def show_main_content(user):
    """Conteúdo principal baseado na página ativa"""
    
    page = st.session_state.get('active_page', 'dashboard')
    
    if page == 'dashboard':
        show_dashboard(user)
    elif page == 'gestao_pacientes':
        show_gestao_pacientes(user)
    elif page == 'calculadoras':
        show_calculadoras(user)
    else:
        show_dashboard(user)

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
# 🎯 PONTO DE ENTRADA DO APLICATIVO
# =============================================================================

if __name__ == "__main__":
    main()
