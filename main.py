#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NutriApp360 PRO - Sistema Completo e Integrado
Version: 15.0 Final - CÓDIGO COMPLETO EM UM SÓ ARQUIVO
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
import re

st.set_page_config(
    page_title="NutriApp360 PRO v15.0",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CSS
# =============================================================================

def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        color: #1B5E20;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9, #A5D6A7);
        padding: 1.5rem;
        border-radius: 20px;
        border: 3px solid #4CAF50;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .ultra-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #1B5E20, #2E7D32, #4CAF50, #66BB6A);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #2E7D32;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        padding: 0.8rem 1.5rem;
        background: linear-gradient(90deg, rgba(76,175,80,0.15), transparent);
        border-left: 5px solid #4CAF50;
        border-radius: 5px;
    }
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(76,175,80,0.2);
        border-color: #4CAF50;
    }
    .metric-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E7D32;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .dashboard-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
        margin-bottom: 1.5rem;
    }
    .dashboard-card-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2E7D32;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E8F5E9;
    }
    .status-badge {
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    .ai-response {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #2196F3;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(33,150,243,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# DADOS
# =============================================================================

ALIMENTOS_TACO = [
    {"nome": "Arroz branco cozido", "grupo": "Cereais", "porcao": 100, "calorias": 128, "carb": 28.1, "prot": 2.5, "lip": 0.2, "fibra": 1.6},
    {"nome": "Arroz integral cozido", "grupo": "Cereais", "porcao": 100, "calorias": 124, "carb": 25.8, "prot": 2.6, "lip": 1.0, "fibra": 2.7},
    {"nome": "Feijão preto cozido", "grupo": "Leguminosas", "porcao": 100, "calorias": 77, "carb": 14.0, "prot": 4.5, "lip": 0.5, "fibra": 8.4},
    {"nome": "Frango grelhado", "grupo": "Carnes", "porcao": 100, "calorias": 165, "carb": 0, "prot": 31.0, "lip": 3.6, "fibra": 0},
    {"nome": "Banana", "grupo": "Frutas", "porcao": 100, "calorias": 98, "carb": 26.0, "prot": 1.3, "lip": 0.1, "fibra": 2.6},
]

CONVERSAO_MEDIDAS = {
    "colher de sopa": {"arroz": 25, "feijao": 20, "aveia": 10},
    "xícara": {"arroz": 160, "feijao": 150},
    "unidade": {"ovo": 50, "banana": 100},
    "copo": 200,
}

# =============================================================================
# IA
# =============================================================================

class AdvancedAIAssistant:
    def __init__(self):
        self.knowledge_base = {
            "diabetes": {"info": "Controle de carboidratos, fibras 25-35g/dia, fracionamento 5-6 refeições"},
            "hipertensao": {"info": "Dieta DASH, reduzir sódio <2300mg/dia, aumentar potássio"},
            "obesidade": {"info": "Déficit 300-500kcal/dia, proteína 1.6-2.2g/kg"},
        }
    
    def get_advice(self, condicao):
        key = condicao.lower().replace(" ", "_")
        if key in self.knowledge_base:
            return f"**ORIENTAÇÕES:** {self.knowledge_base[key]['info']}"
        return "Para orientações específicas, mencione: diabetes, hipertensão ou obesidade"
    
    def gerar_cardapio_ia(self, calorias, objetivo, restricoes, refeicoes=5):
        return f"""
CARDÁPIO PERSONALIZADO - IA
        
Calorias: {calorias} kcal/dia
Objetivo: {objetivo}
Refeições: {refeicoes}x/dia

CAFÉ DA MANHÃ:
- Pão integral (2 fatias)
- Ovo cozido (1 unidade)
- Fruta

LANCHE:
- Iogurte + aveia

ALMOÇO:
- Arroz integral (4 col sopa)
- Feijão (1 concha)
- Frango grelhado (100g)
- Salada

LANCHE TARDE:
- Fruta + oleaginosas

JANTAR:
- Proteína magra
- Vegetais

Hidratação: 2L água/dia
"""

ai_assistant = AdvancedAIAssistant()

# =============================================================================
# CONVERSOR
# =============================================================================

class MeasureConverter:
    def __init__(self):
        self.conversoes = CONVERSAO_MEDIDAS
    
    def converter(self, quantidade, medida, alimento):
        try:
            if medida.lower() in self.conversoes:
                conv = self.conversoes[medida.lower()]
                if isinstance(conv, dict):
                    for key in conv:
                        if key in alimento.lower():
                            return quantidade * conv[key]
                    return quantidade * 20
                return quantidade * conv
            return quantidade
        except:
            return quantidade

converter = MeasureConverter()

# =============================================================================
# DATABASE
# =============================================================================

class DatabaseManager:
    def __init__(self):
        self.db_name = "nutriapp360_pro.db"
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name, check_same_thread=False)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo_usuario TEXT DEFAULT 'nutricionista',
            nivel_acesso TEXT DEFAULT 'completo',
            coren TEXT,
            telefone TEXT,
            clinica TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ultimo_acesso TIMESTAMP,
            ativo INTEGER DEFAULT 1
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            nutricionista_id INTEGER,
            nome TEXT NOT NULL,
            cpf TEXT,
            email TEXT,
            telefone TEXT,
            data_nascimento DATE,
            sexo TEXT,
            profissao TEXT,
            objetivo TEXT,
            restricoes TEXT,
            observacoes TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo INTEGER DEFAULT 1,
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS alimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            grupo TEXT,
            porcao REAL,
            calorias REAL,
            carboidratos REAL,
            proteinas REAL,
            lipidios REAL,
            fibras REAL,
            criado_por INTEGER,
            publico INTEGER DEFAULT 1
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS prontuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            nutricionista_id INTEGER,
            data_atendimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tipo_atendimento TEXT,
            queixa_principal TEXT,
            historia_clinica TEXT,
            diagnostico_nutricional TEXT,
            conduta TEXT,
            observacoes TEXT
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            data_avaliacao DATE NOT NULL,
            peso REAL,
            altura REAL,
            imc REAL,
            gordura_corporal REAL,
            massa_muscular REAL,
            observacoes TEXT
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS prescricoes_suplementos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            paciente_id INTEGER,
            nutricionista_id INTEGER,
            data_prescricao DATE DEFAULT CURRENT_DATE,
            suplementos TEXT,
            orientacoes TEXT,
            validade DATE,
            ativo INTEGER DEFAULT 1
        )''')
        
        # Popular alimentos
        cursor.execute("SELECT COUNT(*) FROM alimentos")
        if cursor.fetchone()[0] == 0:
            for alimento in ALIMENTOS_TACO:
                cursor.execute('''INSERT INTO alimentos (nome, grupo, porcao, calorias, carboidratos, proteinas, lipidios, fibras, publico)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)''',
                (alimento['nome'], alimento['grupo'], alimento['porcao'], alimento['calorias'],
                 alimento['carb'], alimento['prot'], alimento['lip'], alimento['fibra']))
        
        # Criar usuários padrão
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            usuarios = [
                ('Admin', 'admin@nutriapp360.com', 'admin123', 'admin', 'completo', 'ADMIN001'),
                ('Nutricionista', 'nutri@nutriapp360.com', 'nutri123', 'nutricionista', 'completo', 'CRN12345'),
            ]
            for nome, email, senha, tipo, acesso, coren in usuarios:
                senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                cursor.execute('''INSERT INTO usuarios (nome, email, senha, tipo_usuario, nivel_acesso, coren, clinica)
                VALUES (?, ?, ?, ?, ?, ?, ?)''', (nome, email, senha_hash, tipo, acesso, coren, 'NutriApp360'))
        
        conn.commit()
        conn.close()

db_manager = DatabaseManager()

# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def calculate_age(birth_date):
    try:
        if isinstance(birth_date, str):
            birth = datetime.strptime(birth_date, '%Y-%m-%d').date()
        else:
            birth = birth_date
        today = date.today()
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    except:
        return 0

def calculate_imc(peso, altura):
    return peso / (altura ** 2)

def check_permission(user, required_level):
    levels = {'admin': 3, 'completo': 2, 'limitado': 1}
    user_level = levels.get(user.get('nivel_acesso', 'limitado'), 1)
    req_level = levels.get(required_level, 2)
    return user_level >= req_level

# =============================================================================
# LOGIN
# =============================================================================

def authenticate_user(email, password):
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    cursor.execute('''SELECT id, nome, email, tipo_usuario, nivel_acesso, coren, telefone, clinica
    FROM usuarios WHERE email = ? AND senha = ? AND ativo = 1''', (email, password_hash))
    user = cursor.fetchone()
    
    if user:
        cursor.execute('UPDATE usuarios SET ultimo_acesso = CURRENT_TIMESTAMP WHERE id = ?', (user[0],))
        conn.commit()
        return {'id': user[0], 'nome': user[1], 'email': user[2], 'tipo_usuario': user[3],
                'nivel_acesso': user[4], 'coren': user[5], 'telefone': user[6], 'clinica': user[7]}
    
    conn.close()
    return None

def show_login():
    load_css()
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="main-header">🥗 NutriApp360 PRO</h1>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center;">Sistema Completo v15.0</h3>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="seu@email.com")
            senha = st.text_input("Senha", type="password")
            login_btn = st.form_submit_button("Entrar", use_container_width=True)
            
            if login_btn:
                if email and senha:
                    user = authenticate_user(email, senha)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.success(f"Bem-vindo, {user['nome']}!")
                        st.rerun()
                    else:
                        st.error("Email ou senha incorretos!")
                else:
                    st.warning("Preencha todos os campos!")
        
        with st.expander("Credenciais de Demo"):
            st.info("""
            **Admin:** admin@nutriapp360.com / admin123
            **Nutricionista:** nutri@nutriapp360.com / nutri123
            """)

# =============================================================================
# DASHBOARD
# =============================================================================

def show_dashboard(user):
    load_css()
    st.markdown(f'<h1 class="ultra-header">Dashboard - {user["nome"]}</h1>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM pacientes WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    total_pacientes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM prontuarios WHERE nutricionista_id = ?", (user['id'],))
    total_prontuarios = cursor.fetchone()[0]
    
    conn.close()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''<div class="metric-card">
            <div class="metric-icon">👥</div>
            <div class="metric-value">{total_pacientes}</div>
            <div class="metric-label">Pacientes</div>
        </div>''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''<div class="metric-card">
            <div class="metric-icon">📋</div>
            <div class="metric-value">{total_prontuarios}</div>
            <div class="metric-label">Prontuários</div>
        </div>''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''<div class="metric-card">
            <div class="metric-icon">💊</div>
            <div class="metric-value">0</div>
            <div class="metric-label">Prescrições</div>
        </div>''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''<div class="metric-card">
            <div class="metric-icon">🍎</div>
            <div class="metric-value">5</div>
            <div class="metric-label">Alimentos</div>
        </div>''', unsafe_allow_html=True)

# =============================================================================
# ASSISTENTE IA
# =============================================================================

def show_ai_assistant(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Assistente IA</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Consultar IA", "Gerar Cardápio"])
    
    with tab1:
        condicao = st.selectbox("Condição", ["Diabetes", "Hipertensão", "Obesidade"])
        if st.button("Consultar"):
            resposta = ai_assistant.get_advice(condicao)
            st.markdown(f'<div class="ai-response">{resposta}</div>', unsafe_allow_html=True)
    
    with tab2:
        calorias = st.number_input("Calorias", 1200, 5000, 2000, step=100)
        objetivo = st.selectbox("Objetivo", ["Perda Peso", "Ganho Massa", "Saúde"])
        if st.button("Gerar Cardápio"):
            cardapio = ai_assistant.gerar_cardapio_ia(calorias, objetivo, "", 5)
            st.code(cardapio)

# =============================================================================
# PACIENTES
# =============================================================================

def show_pacientes(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Gestão de Pacientes</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Lista", "Novo Paciente"])
    
    with tab1:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""SELECT id, nome, email, telefone, objetivo FROM pacientes
        WHERE nutricionista_id = ? AND ativo = 1 ORDER BY nome""", (user['id'],))
        pacientes = cursor.fetchall()
        conn.close()
        
        if pacientes:
            for pac in pacientes:
                with st.expander(f"{pac[1]} - {pac[4]}", expanded=False):
                    st.markdown(f"**Email:** {pac[2]}\n**Tel:** {pac[3]}")
        else:
            st.info("Nenhum paciente cadastrado")
    
    with tab2:
        with st.form("pac_form"):
            nome = st.text_input("Nome *")
            email = st.text_input("Email")
            telefone = st.text_input("Telefone")
            objetivo = st.selectbox("Objetivo", ["Perda de Peso", "Ganho de Massa", "Saúde"])
            
            if st.form_submit_button("Cadastrar"):
                if nome:
                    try:
                        conn = db_manager.get_connection()
                        cursor = conn.cursor()
                        cursor.execute('''INSERT INTO pacientes (uuid, nutricionista_id, nome, email, telefone, objetivo, sexo)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (str(uuid.uuid4()), user['id'], nome, email, telefone, objetivo, "Não informado"))
                        conn.commit()
                        conn.close()
                        st.success("Paciente cadastrado!")
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

# =============================================================================
# ALIMENTOS
# =============================================================================

def show_alimentos(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Biblioteca de Alimentos</h1>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alimentos WHERE publico = 1")
    alimentos = cursor.fetchall()
    conn.close()
    
    for alim in alimentos:
        with st.expander(f"{alim[1]} - {alim[4]:.0f} kcal", expanded=False):
            st.markdown(f"**Grupo:** {alim[2]}")
            st.markdown(f"**Porção:** {alim[3]:.0f}g")
            st.markdown(f"**Carb:** {alim[5]:.1f}g | **Prot:** {alim[6]:.1f}g | **Lip:** {alim[7]:.1f}g")

# =============================================================================
# PRONTUÁRIO
# =============================================================================

def show_prontuario(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Prontuários</h1>', unsafe_allow_html=True)
    
    if not check_permission(user, 'completo'):
        st.error("Sem permissão")
        return
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM pacientes WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.warning("Cadastre um paciente primeiro")
        return
    
    tab1, tab2 = st.tabs(["Novo", "Histórico"])
    
    with tab1:
        with st.form("pront_form"):
            paciente = st.selectbox("Paciente", options=pacientes, format_func=lambda x: x[1])
            queixa = st.text_area("Queixa *", height=100)
            diagnostico = st.text_area("Diagnóstico *", height=100)
            conduta = st.text_area("Conduta *", height=150)
            
            if st.form_submit_button("Salvar"):
                if queixa and diagnostico:
                    try:
                        conn = db_manager.get_connection()
                        cursor = conn.cursor()
                        cursor.execute('''INSERT INTO prontuarios (paciente_id, nutricionista_id, tipo_atendimento,
                        queixa_principal, diagnostico_nutricional, conduta)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                        (paciente[0], user['id'], "Consulta", queixa, diagnostico, conduta))
                        conn.commit()
                        conn.close()
                        st.success("Prontuário salvo!")
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

# =============================================================================
# AVALIAÇÕES
# =============================================================================

def show_avaliacoes(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Avaliações</h1>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM pacientes WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.warning("Cadastre um paciente primeiro")
        return
    
    with st.form("aval_form"):
        paciente = st.selectbox("Paciente", options=pacientes, format_func=lambda x: x[1])
        
        col1, col2 = st.columns(2)
        with col1:
            peso = st.number_input("Peso (kg)", 30.0, 300.0, 70.0, step=0.1)
            altura = st.number_input("Altura (cm)", 100.0, 250.0, 170.0, step=0.1)
        with col2:
            gordura = st.number_input("% Gordura", 0.0, 60.0, 20.0, step=0.1)
            muscular = st.number_input("% Massa Muscular", 0.0, 100.0, 40.0, step=0.1)
        
        if st.form_submit_button("Salvar"):
            try:
                imc = calculate_imc(peso, altura/100)
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO avaliacoes (paciente_id, data_avaliacao, peso, altura, imc,
                gordura_corporal, massa_muscular) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (paciente[0], date.today(), peso, altura, imc, gordura, muscular))
                conn.commit()
                conn.close()
                st.success(f"Avaliação salva! IMC: {imc:.1f}")
            except Exception as e:
                st.error(f"Erro: {str(e)}")

# =============================================================================
# PRESCRIÇÕES
# =============================================================================

def show_prescricoes(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Prescrições</h1>', unsafe_allow_html=True)
    
    if not check_permission(user, 'completo'):
        st.error("Sem permissão")
        return
    
    st.warning("Prescrição de SUPLEMENTOS NUTRICIONAIS (Lei 8.234/91)")
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM pacientes WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.warning("Cadastre um paciente primeiro")
        return
    
    with st.form("presc_form"):
        paciente = st.selectbox("Paciente", options=pacientes, format_func=lambda x: x[1])
        suplementos = st.text_area("Suplementos e Posologia", height=200,
        placeholder="1. Vitamina D3 - 2000 UI - 1x/dia\n2. Ômega 3 - 1000mg - 2x/dia")
        
        if st.form_submit_button("Gerar Prescrição"):
            if suplementos:
                try:
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    cursor.execute('''INSERT INTO prescricoes_suplementos (uuid, paciente_id, nutricionista_id, suplementos, validade)
                    VALUES (?, ?, ?, ?, ?)''',
                    (str(uuid.uuid4()), paciente[0], user['id'], suplementos, date.today() + timedelta(days=90)))
                    conn.commit()
                    conn.close()
                    st.success("Prescrição gerada!")
                except Exception as e:
                    st.error(f"Erro: {str(e)}")

# =============================================================================
# MENU PRINCIPAL
# =============================================================================

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'page' not in st.session_state:
        st.session_state.page = "Dashboard"
    
    if not st.session_state.logged_in:
        show_login()
        return
    
    user = st.session_state.user
    
    with st.sidebar:
        st.markdown(f'<h2 style="color: #1B5E20;">{user["nome"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #666;">{user["tipo_usuario"].upper()}</p>', unsafe_allow_html=True)
        st.markdown("---")
        
        menu_items = [
            ("Dashboard", "Dashboard"),
            ("Assistente IA", "IA"),
            ("Pacientes", "Pacientes"),
            ("Alimentos", "Alimentos"),
            ("Prontuários", "Prontuario"),
            ("Avaliações", "Avaliacoes"),
            ("Prescrições", "Prescricoes"),
        ]
        
        for label, page in menu_items:
            if st.button(label, use_container_width=True, key=f"menu_{page}",
                        type="primary" if st.session_state.page == page else "secondary"):
                st.session_state.page = page
                st.rerun()
        
        st.markdown("---")
        
        if st.button("Sair", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    # Roteamento
    if st.session_state.page == "Dashboard":
        show_dashboard(user)
    elif st.session_state.page == "IA":
        show_ai_assistant(user)
    elif st.session_state.page == "Pacientes":
        show_pacientes(user)
    elif st.session_state.page == "Alimentos":
        show_alimentos(user)
    elif st.session_state.page == "Prontuario":
        show_prontuario(user)
    elif st.session_state.page == "Avaliacoes":
        show_avaliacoes(user)
    elif st.session_state.page == "Prescricoes":
        show_prescricoes(user)

if __name__ == "__main__":
    main()
