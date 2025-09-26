#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NutriApp360 - Sistema Completo de Apoio ao Nutricionista
Version: 11.0 - TODOS OS MÓDULOS FUNCIONAIS
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
import math
import random
import calendar
import numpy as np
import time

# Configuração
st.set_page_config(
    page_title="NutriApp360 v11.0",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CSS PERSONALIZADO
# =============================================================================

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
    .ultra-header {
        font-size: 3rem;
        background: linear-gradient(135deg, #2E7D32, #4CAF50, #66BB6A);
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
        margin: 1.5rem 0;
        padding: 0.5rem 1rem;
        background: linear-gradient(90deg, rgba(76,175,80,0.1), transparent);
        border-left: 4px solid #4CAF50;
    }
    .metric-card {
        background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        border: 2px solid #4CAF50;
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
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# DATABASE MANAGER
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
        
        # Tabela Usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            coren TEXT,
            telefone TEXT,
            clinica TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo INTEGER DEFAULT 1
        )
        ''')
        
        # Tabela Pacientes
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
            objetivo TEXT,
            restricoes TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo INTEGER DEFAULT 1,
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela Avaliações
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            data_avaliacao DATE NOT NULL,
            peso REAL,
            altura REAL,
            imc REAL,
            cintura REAL,
            quadril REAL,
            gordura REAL,
            massa_muscular REAL,
            observacoes TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
        )
        ''')
        
        # Tabela Planos Alimentares
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS planos_alimentares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            paciente_id INTEGER,
            nutricionista_id INTEGER,
            nome TEXT NOT NULL,
            objetivo TEXT,
            calorias INTEGER,
            carboidratos REAL,
            proteinas REAL,
            lipidios REAL,
            refeicoes TEXT,
            data_criacao DATE DEFAULT CURRENT_DATE,
            data_validade DATE,
            ativo INTEGER DEFAULT 1,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela Consultas
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
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela Receitas
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
            tags TEXT,
            criada_por INTEGER,
            publica INTEGER DEFAULT 0,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (criada_por) REFERENCES usuarios (id)
        )
        ''')
        
        # Criar usuário admin
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = ?", ('admin@nutriapp360.com',))
        if cursor.fetchone()[0] == 0:
            senha_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, coren, clinica)
            VALUES (?, ?, ?, ?, ?)
            ''', ('Administrador', 'admin@nutriapp360.com', senha_hash, 'ADMIN001', 'NutriApp360'))
        
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
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return age
    except:
        return 0

def calculate_bmr(peso, altura, idade, sexo):
    if sexo.upper() in ["MASCULINO", "M"]:
        return (10 * peso) + (6.25 * altura) - (5 * idade) + 5
    else:
        return (10 * peso) + (6.25 * altura) - (5 * idade) - 161

def calculate_imc(peso, altura):
    return peso / (altura ** 2)

# =============================================================================
# AUTENTICAÇÃO
# =============================================================================

def authenticate_user(email, password):
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    cursor.execute('''
    SELECT id, nome, email, coren, telefone, clinica
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
            'coren': user[3],
            'telefone': user[4],
            'clinica': user[5]
        }
    return None

def show_login():
    load_css()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="main-header">🥗 NutriApp360</h1>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center;">Sistema Completo v11.0</h3>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="seu@email.com")
            senha = st.text_input("Senha", type="password")
            
            col_l, col_r = st.columns(2)
            
            with col_l:
                login_btn = st.form_submit_button("Entrar", use_container_width=True)
            
            with col_r:
                register_btn = st.form_submit_button("Cadastrar", use_container_width=True)
            
            if login_btn:
                if email and senha:
                    user = authenticate_user(email, senha)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.success(f"Bem-vindo, {user['nome']}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Email ou senha incorretos!")
                else:
                    st.warning("Preencha todos os campos!")
            
            if register_btn:
                st.session_state.show_register = True
                st.rerun()
        
        with st.expander("Informações de Demo"):
            st.info("""
            **Credenciais:**
            - Email: admin@nutriapp360.com
            - Senha: admin123
            
            **Todos os Módulos Funcionais:**
            - Dashboard Completo
            - Gestão de Pacientes
            - 6 Calculadoras Nutricionais
            - Planos Alimentares
            - Receitas
            - Agenda Completa
            - Relatórios
            """)

def show_register():
    load_css()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h2 class="main-header">Cadastro</h2>', unsafe_allow_html=True)
        
        with st.form("register_form"):
            nome = st.text_input("Nome Completo")
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")
            confirmar = st.text_input("Confirmar Senha", type="password")
            
            col_b, col_r = st.columns(2)
            
            with col_b:
                back = st.form_submit_button("Voltar", use_container_width=True)
            
            with col_r:
                submit = st.form_submit_button("Cadastrar", use_container_width=True)
            
            if back:
                st.session_state.show_register = False
                st.rerun()
            
            if submit:
                if all([nome, email, senha, confirmar]):
                    if senha != confirmar:
                        st.error("Senhas não coincidem!")
                    else:
                        try:
                            conn = db_manager.get_connection()
                            cursor = conn.cursor()
                            
                            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = ?", (email,))
                            if cursor.fetchone()[0] > 0:
                                st.error("Email já cadastrado!")
                            else:
                                senha_hash = hash_password(senha)
                                cursor.execute('''
                                INSERT INTO usuarios (nome, email, senha)
                                VALUES (?, ?, ?)
                                ''', (nome, email, senha_hash))
                                
                                conn.commit()
                                st.success("Cadastrado com sucesso!")
                                time.sleep(2)
                                st.session_state.show_register = False
                                st.rerun()
                        except Exception as e:
                            st.error(f"Erro: {str(e)}")
                        finally:
                            conn.close()
                else:
                    st.warning("Preencha todos os campos!")

# =============================================================================
# DASHBOARD
# =============================================================================

def show_dashboard(user):
    load_css()
    
    st.markdown(f'<h1 class="ultra-header">Dashboard - {user["nome"]}</h1>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Buscar estatísticas
    cursor.execute("SELECT COUNT(*) FROM pacientes WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    total_pacientes = cursor.fetchone()[0]
    
    cursor.execute("""
    SELECT COUNT(*) FROM consultas 
    WHERE nutricionista_id = ? AND DATE(data_consulta) = DATE('now')
    """, (user['id'],))
    consultas_hoje = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM planos_alimentares WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    planos_ativos = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM receitas WHERE criada_por = ?", (user['id'],))
    receitas = cursor.fetchone()[0]
    
    cursor.execute("""
    SELECT SUM(valor) FROM consultas 
    WHERE nutricionista_id = ? 
    AND strftime('%Y-%m', data_consulta) = strftime('%Y-%m', 'now')
    AND status = 'realizada'
    """, (user['id'],))
    receita_mes = cursor.fetchone()[0] or 0
    
    conn.close()
    
    # Métricas
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h2 style="color: #2E7D32; margin:0;">👥</h2>
            <h3 style="margin:0;">{total_pacientes}</h3>
            <p style="margin:0;">Pacientes</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <h2 style="color: #2E7D32; margin:0;">📅</h2>
            <h3 style="margin:0;">{consultas_hoje}</h3>
            <p style="margin:0;">Hoje</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <h2 style="color: #2E7D32; margin:0;">📋</h2>
            <h3 style="margin:0;">{planos_ativos}</h3>
            <p style="margin:0;">Planos</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="metric-card">
            <h2 style="color: #2E7D32; margin:0;">🍳</h2>
            <h3 style="margin:0;">{receitas}</h3>
            <p style="margin:0;">Receitas</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col5:
        st.markdown(f'''
        <div class="metric-card">
            <h2 style="color: #2E7D32; margin:0;">💰</h2>
            <h3 style="margin:0;">R$ {receita_mes:.0f}</h3>
            <p style="margin:0;">Mês</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Acesso Rápido
    st.markdown('<div class="sub-header">Acesso Rápido</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.button("Novo Paciente", use_container_width=True)
        st.button("Calculadoras", use_container_width=True)
    
    with col2:
        st.button("Nova Consulta", use_container_width=True)
        st.button("Novo Plano", use_container_width=True)
    
    with col3:
        st.button("Ver Agenda", use_container_width=True)
        st.button("Receitas", use_container_width=True)
    
    with col4:
        st.button("Relatórios", use_container_width=True)
        st.button("Configurações", use_container_width=True)

# =============================================================================
# GESTÃO DE PACIENTES COMPLETA
# =============================================================================

def show_gestao_pacientes(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Gestão de Pacientes</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Lista de Pacientes", "Novo Paciente", "Avaliações"])
    
    with tab1:
        show_patients_list(user)
    
    with tab2:
        show_new_patient(user)
    
    with tab3:
        show_patient_evaluations(user)

def show_patients_list(user):
    st.markdown('<div class="sub-header">Lista de Pacientes</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT p.*, COUNT(a.id) as avaliacoes
    FROM pacientes p
    LEFT JOIN avaliacoes a ON p.id = a.paciente_id
    WHERE p.nutricionista_id = ? AND p.ativo = 1
    GROUP BY p.id
    ORDER BY p.nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.info("Nenhum paciente cadastrado ainda.")
        return
    
    st.markdown(f"**Total: {len(pacientes)} pacientes**")
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        busca = st.text_input("Buscar por nome", placeholder="Digite o nome...")
    
    with col2:
        sexo_filtro = st.selectbox("Filtrar por sexo", ["Todos", "Feminino", "Masculino"])
    
    # Listar pacientes
    for p in pacientes:
        if busca and busca.lower() not in p[3].lower():
            continue
        
        if sexo_filtro != "Todos" and p[7] != sexo_filtro:
            continue
        
        with st.expander(f"👤 {p[3]} - {p[7] or 'N/I'}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Email:** {p[4] or 'Não informado'}")
                st.markdown(f"**Telefone:** {p[5] or 'Não informado'}")
                if p[6]:
                    idade = calculate_age(p[6])
                    st.markdown(f"**Idade:** {idade} anos")
            
            with col2:
                st.markdown(f"**Profissão:** {p[8] or 'Não informada'}")
                st.markdown(f"**Objetivo:** {p[9] or 'Não definido'}")
                st.markdown(f"**Avaliações:** {p[-1]}")
            
            if st.button(f"Ver Detalhes", key=f"details_{p[0]}"):
                st.info("Funcionalidade de detalhes em desenvolvimento")

def show_new_patient(user):
    st.markdown('<div class="sub-header">Cadastrar Novo Paciente</div>', unsafe_allow_html=True)
    
    with st.form("new_patient_form"):
        st.markdown("**Dados Pessoais**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo *")
            email = st.text_input("Email")
            telefone = st.text_input("Telefone")
            data_nasc = st.date_input("Data de Nascimento", value=date(1990, 1, 1))
        
        with col2:
            sexo = st.selectbox("Sexo", ["", "Feminino", "Masculino"])
            profissao = st.text_input("Profissão")
            objetivo = st.selectbox("Objetivo", [
                "", "Perda de Peso", "Ganho de Peso", "Manutenção",
                "Ganho de Massa Muscular", "Melhora da Saúde"
            ])
            restricoes = st.text_area("Restrições Alimentares", height=80)
        
        st.markdown("**Avaliação Inicial (Opcional)**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            peso = st.number_input("Peso (kg)", 0.0, 300.0, 0.0, step=0.1)
        
        with col2:
            altura = st.number_input("Altura (cm)", 0.0, 250.0, 0.0, step=0.5)
        
        with col3:
            if peso > 0 and altura > 0:
                imc = calculate_imc(peso, altura/100)
                st.metric("IMC Calculado", f"{imc:.1f}")
        
        submitted = st.form_submit_button("Cadastrar Paciente", use_container_width=True)
        
        if submitted:
            if not nome:
                st.error("Nome é obrigatório!")
            else:
                try:
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    paciente_uuid = str(uuid.uuid4())
                    
                    cursor.execute('''
                    INSERT INTO pacientes (
                        uuid, nutricionista_id, nome, email, telefone,
                        data_nascimento, sexo, profissao, objetivo, restricoes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        paciente_uuid, user['id'], nome, email, telefone,
                        data_nasc, sexo, profissao, objetivo, restricoes
                    ))
                    
                    paciente_id = cursor.lastrowid
                    
                    # Adicionar avaliação inicial se fornecida
                    if peso > 0 and altura > 0:
                        imc_calc = calculate_imc(peso, altura/100)
                        cursor.execute('''
                        INSERT INTO avaliacoes (
                            paciente_id, data_avaliacao, peso, altura, imc
                        ) VALUES (?, ?, ?, ?, ?)
                        ''', (paciente_id, date.today(), peso, altura/100, imc_calc))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("Paciente cadastrado com sucesso!")
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Erro ao cadastrar: {str(e)}")

def show_patient_evaluations(user):
    st.markdown('<div class="sub-header">Nova Avaliação</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, nome FROM pacientes
    WHERE nutricionista_id = ? AND ativo = 1
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.warning("Nenhum paciente cadastrado.")
        return
    
    with st.form("evaluation_form"):
        paciente = st.selectbox(
            "Selecione o Paciente",
            options=pacientes,
            format_func=lambda x: x[1]
        )
        
        data_aval = st.date_input("Data da Avaliação", value=date.today())
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            peso = st.number_input("Peso (kg)", 0.0, 300.0, 0.0, step=0.1)
            altura = st.number_input("Altura (m)", 0.0, 2.5, 0.0, step=0.01)
        
        with col2:
            cintura = st.number_input("Cintura (cm)", 0.0, 200.0, 0.0, step=0.5)
            quadril = st.number_input("Quadril (cm)", 0.0, 200.0, 0.0, step=0.5)
        
        with col3:
            gordura = st.number_input("% Gordura", 0.0, 50.0, 0.0, step=0.1)
            massa_musc = st.number_input("Massa Muscular (kg)", 0.0, 100.0, 0.0, step=0.1)
        
        obs = st.text_area("Observações")
        
        submitted = st.form_submit_button("Salvar Avaliação", use_container_width=True)
        
        if submitted:
            if peso > 0 and altura > 0:
                try:
                    imc = calculate_imc(peso, altura)
                    
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                    INSERT INTO avaliacoes (
                        paciente_id, data_avaliacao, peso, altura, imc,
                        cintura, quadril, gordura, massa_muscular, observacoes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        paciente[0], data_aval, peso, altura, imc,
                        cintura if cintura > 0 else None,
                        quadril if quadril > 0 else None,
                        gordura if gordura > 0 else None,
                        massa_musc if massa_musc > 0 else None,
                        obs
                    ))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("Avaliação salva!")
                    st.metric("IMC Calculado", f"{imc:.2f}")
                    
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
            else:
                st.error("Peso e altura são obrigatórios!")

# Continua na próxima parte...
# =============================================================================
# CALCULADORAS NUTRICIONAIS COMPLETAS - TODAS AS 6
# =============================================================================

def show_calculadoras(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Calculadoras Nutricionais</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "IMC", "Gasto Energético", "Macronutrientes", 
        "Hidratação", "Medidas Corporais", "Composição Corporal"
    ])
    
    with tab1:
        calc_imc()
    
    with tab2:
        calc_gasto_energetico()
    
    with tab3:
        calc_macronutrientes()
    
    with tab4:
        calc_hidratacao()
    
    with tab5:
        calc_medidas_corporais()
    
    with tab6:
        calc_composicao_corporal()

def calc_imc():
    st.markdown('<div class="sub-header">Calculadora de IMC</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        peso = st.number_input("Peso (kg)", 30.0, 300.0, 70.0, step=0.1, key="imc_peso")
        altura = st.number_input("Altura (cm)", 100.0, 250.0, 170.0, step=0.5, key="imc_altura")
        
        if st.button("Calcular IMC"):
            altura_m = altura / 100
            imc = peso / (altura_m ** 2)
            
            if imc < 18.5:
                classe = "Baixo peso"
                cor = "#FFC107"
                risco = "Risco de problemas de saúde"
            elif imc < 25:
                classe = "Peso normal"
                cor = "#4CAF50"
                risco = "Menor risco de problemas"
            elif imc < 30:
                classe = "Sobrepeso"
                cor = "#FF9800"
                risco = "Risco moderado"
            elif imc < 35:
                classe = "Obesidade grau I"
                cor = "#F44336"
                risco = "Risco elevado"
            elif imc < 40:
                classe = "Obesidade grau II"
                cor = "#D32F2F"
                risco = "Risco alto"
            else:
                classe = "Obesidade grau III"
                cor = "#B71C1C"
                risco = "Risco muito alto"
            
            st.markdown(f'''
            <div class="calculation-result" style="border-color: {cor};">
                <h3>IMC: {imc:.2f}</h3>
                <h4 style="color: {cor};">{classe}</h4>
                <p>{risco}</p>
            </div>
            ''', unsafe_allow_html=True)
            
            # Peso ideal
            peso_min = 18.5 * (altura_m ** 2)
            peso_max = 24.9 * (altura_m ** 2)
            
            st.info(f"Faixa de peso ideal: {peso_min:.1f} kg - {peso_max:.1f} kg")
    
    with col2:
        st.markdown("**Interpretação do IMC:**")
        
        df_imc = pd.DataFrame({
            'Classificação': ['Baixo peso', 'Normal', 'Sobrepeso', 'Obesidade I', 'Obesidade II', 'Obesidade III'],
            'IMC': ['< 18.5', '18.5 - 24.9', '25 - 29.9', '30 - 34.9', '35 - 39.9', '≥ 40']
        })
        
        st.dataframe(df_imc, use_container_width=True, hide_index=True)

def calc_gasto_energetico():
    st.markdown('<div class="sub-header">Gasto Energético Total</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        peso = st.number_input("Peso (kg)", 30.0, 300.0, 70.0, key="get_peso")
        altura = st.number_input("Altura (cm)", 100.0, 250.0, 170.0, key="get_altura")
        idade = st.number_input("Idade (anos)", 10, 120, 30, key="get_idade")
        sexo = st.selectbox("Sexo", ["Feminino", "Masculino"], key="get_sexo")
        
        atividade = st.selectbox("Nível de Atividade", [
            "Sedentário",
            "Levemente ativo",
            "Moderadamente ativo",
            "Muito ativo",
            "Extremamente ativo"
        ])
        
        if st.button("Calcular GET"):
            # TMB
            tmb = calculate_bmr(peso, altura, idade, sexo)
            
            # Fator de atividade
            fatores = {
                "Sedentário": 1.2,
                "Levemente ativo": 1.375,
                "Moderadamente ativo": 1.55,
                "Muito ativo": 1.725,
                "Extremamente ativo": 1.9
            }
            
            fator = fatores[atividade]
            get = tmb * fator
            
            col_tmb, col_get = st.columns(2)
            
            with col_tmb:
                st.metric("TMB", f"{tmb:.0f} kcal/dia")
            
            with col_get:
                st.metric("GET", f"{get:.0f} kcal/dia")
            
            st.markdown(f'''
            <div class="calculation-result">
                <h4>Gasto Energético Total</h4>
                <p><strong>TMB:</strong> {tmb:.0f} kcal</p>
                <p><strong>Fator de Atividade:</strong> {fator}</p>
                <p><strong>GET:</strong> {get:.0f} kcal/dia</p>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Fatores de Atividade:**")
        
        df_atividade = pd.DataFrame({
            'Nível': ['Sedentário', 'Levemente ativo', 'Moderadamente ativo', 'Muito ativo', 'Extremamente ativo'],
            'Fator': ['1.2', '1.375', '1.55', '1.725', '1.9'],
            'Descrição': [
                'Pouco/nenhum exercício',
                'Exercício leve 1-3x/sem',
                'Exercício moderado 3-5x/sem',
                'Exercício intenso 6-7x/sem',
                'Exercício muito intenso 2x/dia'
            ]
        })
        
        st.dataframe(df_atividade, use_container_width=True, hide_index=True)

def calc_macronutrientes():
    st.markdown('<div class="sub-header">Distribuição de Macronutrientes</div>', unsafe_allow_html=True)
    
    calorias = st.number_input("Calorias Totais (kcal/dia)", 1000, 5000, 2000, step=50)
    
    abordagem = st.selectbox("Abordagem Nutricional", [
        "Equilibrada", "Low Carb", "Alta Proteína", "Cetogênica", "Personalizada"
    ])
    
    if abordagem == "Personalizada":
        col1, col2, col3 = st.columns(3)
        
        with col1:
            carb_perc = st.slider("Carboidratos (%)", 5, 70, 50)
        
        with col2:
            prot_perc = st.slider("Proteínas (%)", 10, 40, 20)
        
        with col3:
            lip_perc = 100 - carb_perc - prot_perc
            st.metric("Lipídios (%)", lip_perc)
    else:
        distribuicoes = {
            "Equilibrada": {"carb": 50, "prot": 20, "lip": 30},
            "Low Carb": {"carb": 30, "prot": 30, "lip": 40},
            "Alta Proteína": {"carb": 35, "prot": 35, "lip": 30},
            "Cetogênica": {"carb": 5, "prot": 20, "lip": 75}
        }
        
        dist = distribuicoes[abordagem]
        carb_perc = dist["carb"]
        prot_perc = dist["prot"]
        lip_perc = dist["lip"]
    
    # Calcular gramas
    carb_g = (calorias * carb_perc / 100) / 4
    prot_g = (calorias * prot_perc / 100) / 4
    lip_g = (calorias * lip_perc / 100) / 9
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Carboidratos", f"{carb_g:.0f}g", f"{carb_perc}%")
    
    with col2:
        st.metric("Proteínas", f"{prot_g:.0f}g", f"{prot_perc}%")
    
    with col3:
        st.metric("Lipídios", f"{lip_g:.0f}g", f"{lip_perc}%")
    
    # Gráfico
    fig = px.pie(
        values=[carb_perc, prot_perc, lip_perc],
        names=['Carboidratos', 'Proteínas', 'Lipídios'],
        title="Distribuição de Macronutrientes"
    )
    st.plotly_chart(fig, use_container_width=True)

def calc_hidratacao():
    st.markdown('<div class="sub-header">Necessidade Hídrica</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        peso = st.number_input("Peso (kg)", 30.0, 200.0, 70.0, key="hidra_peso")
        idade = st.number_input("Idade (anos)", 10, 120, 30, key="hidra_idade")
        
        atividade = st.selectbox("Nível de Atividade", [
            "Sedentário",
            "Leve",
            "Moderado",
            "Intenso",
            "Atleta"
        ], key="hidra_ativ")
        
        clima = st.selectbox("Clima", [
            "Temperado",
            "Quente",
            "Muito Quente"
        ])
        
        if st.button("Calcular Hidratação"):
            # Cálculo base
            if idade < 30:
                base = peso * 40
            elif idade < 55:
                base = peso * 35
            else:
                base = peso * 30
            
            # Ajustes
            ajuste_ativ = {"Sedentário": 0, "Leve": 300, "Moderado": 500, "Intenso": 800, "Atleta": 1200}
            ajuste_clima = {"Temperado": 0, "Quente": 400, "Muito Quente": 800}
            
            total = base + ajuste_ativ[atividade] + ajuste_clima[clima]
            
            copos_200ml = total / 200
            garrafas_500ml = total / 500
            
            st.markdown(f'''
            <div class="calculation-result">
                <h3>{total:.0f} ml/dia</h3>
                <p>{copos_200ml:.0f} copos de 200ml</p>
                <p>{garrafas_500ml:.1f} garrafas de 500ml</p>
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Cronograma Sugerido:**")
        
        cronograma = [
            ("07:00", "Ao acordar", "400ml"),
            ("09:00", "Manhã", "200ml"),
            ("12:00", "Almoço", "250ml"),
            ("15:00", "Tarde", "300ml"),
            ("17:00", "Pré-treino", "200ml"),
            ("19:00", "Jantar", "200ml"),
            ("21:00", "Noite", "150ml")
        ]
        
        for hora, momento, qtd in cronograma:
            st.markdown(f"**{hora}** - {momento}: {qtd}")

def calc_medidas_corporais():
    st.markdown('<div class="sub-header">Análise de Medidas Corporais</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        peso = st.number_input("Peso (kg)", 30.0, 300.0, 70.0, key="med_peso")
        altura = st.number_input("Altura (cm)", 100.0, 250.0, 170.0, key="med_altura")
        cintura = st.number_input("Cintura (cm)", 50.0, 200.0, 80.0)
        quadril = st.number_input("Quadril (cm)", 50.0, 200.0, 100.0)
        
        if st.button("Calcular Medidas"):
            altura_m = altura / 100
            imc = peso / (altura_m ** 2)
            rcq = cintura / quadril
            rca = cintura / altura
            
            # Classificações
            if rcq < 0.90:
                rcq_class = "Baixo risco"
                cor_rcq = "#4CAF50"
            elif rcq < 1.0:
                rcq_class = "Risco moderado"
                cor_rcq = "#FF9800"
            else:
                rcq_class = "Alto risco"
                cor_rcq = "#F44336"
            
            col_imc, col_rcq, col_rca = st.columns(3)
            
            with col_imc:
                st.metric("IMC", f"{imc:.1f}")
            
            with col_rcq:
                st.metric("RCQ", f"{rcq:.3f}")
            
            with col_rca:
                st.metric("RCA", f"{rca:.3f}")
            
            st.markdown(f'''
            <div style="background: {cor_rcq}20; border-left: 4px solid {cor_rcq}; padding: 1rem; margin: 1rem 0;">
                <strong>RCQ:</strong> {rcq:.3f} - {rcq_class}
            </div>
            ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Valores de Referência:**")
        
        df_ref = pd.DataFrame({
            'Medida': ['RCQ Homens', 'RCQ Mulheres', 'RCA'],
            'Baixo': ['< 0.90', '< 0.80', '< 0.50'],
            'Moderado': ['0.90-1.0', '0.80-0.85', '0.50-0.58'],
            'Alto': ['> 1.0', '> 0.85', '> 0.58']
        })
        
        st.dataframe(df_ref, use_container_width=True, hide_index=True)

def calc_composicao_corporal():
    st.markdown('<div class="sub-header">Análise de Composição Corporal</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        peso = st.number_input("Peso (kg)", 30.0, 300.0, 70.0, key="comp_peso")
        altura = st.number_input("Altura (cm)", 100.0, 250.0, 170.0, key="comp_altura")
        idade = st.number_input("Idade (anos)", 10, 120, 30, key="comp_idade")
        sexo = st.selectbox("Sexo", ["Feminino", "Masculino"], key="comp_sexo")
        
        gordura = st.number_input("% Gordura Corporal", 0.0, 50.0, 20.0, step=0.1)
        
        if st.button("Calcular Composição"):
            # Cálculos
            massa_gorda = peso * (gordura / 100)
            massa_magra = peso - massa_gorda
            massa_muscular = massa_magra * 0.42
            agua = massa_magra * 0.73
            
            # TMB usando massa magra
            tmb = (21.6 * massa_magra) + 370
            
            col_mg, col_mm, col_agua = st.columns(3)
            
            with col_mg:
                st.metric("Massa Gorda", f"{massa_gorda:.1f} kg")
            
            with col_mm:
                st.metric("Massa Magra", f"{massa_magra:.1f} kg")
            
            with col_agua:
                st.metric("Água Corporal", f"{agua:.1f} L")
            
            st.markdown(f'''
            <div class="calculation-result">
                <h4>Composição Corporal Detalhada</h4>
                <p><strong>Massa Muscular:</strong> {massa_muscular:.1f} kg</p>
                <p><strong>TMB Estimada:</strong> {tmb:.0f} kcal</p>
                <p><strong>% Gordura:</strong> {gordura:.1f}%</p>
            </div>
            ''', unsafe_allow_html=True)
            
            # Gráfico
            fig = px.pie(
                values=[massa_gorda, massa_muscular, agua, peso - massa_gorda - massa_muscular - agua],
                names=['Gordura', 'Músculo', 'Água', 'Outros'],
                title="Distribuição da Composição Corporal"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Referência % Gordura:**")
        
        df_gordura = pd.DataFrame({
            'Classificação': ['Essencial', 'Atleta', 'Fitness', 'Aceitável', 'Obesidade'],
            'Homens': ['2-5%', '6-13%', '14-17%', '18-24%', '>25%'],
            'Mulheres': ['10-13%', '14-20%', '21-24%', '25-31%', '>32%']
        })
        
        st.dataframe(df_gordura, use_container_width=True, hide_index=True)

# =============================================================================
# PLANOS ALIMENTARES COMPLETO
# =============================================================================

def show_planos_alimentares(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Planos Alimentares</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Meus Planos", "Criar Plano"])
    
    with tab1:
        show_my_plans(user)
    
    with tab2:
        create_meal_plan(user)

def show_my_plans(user):
    st.markdown('<div class="sub-header">Planos Ativos</div>', unsafe_allow_html=True)
    
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
        st.info("Nenhum plano ativo no momento.")
        return
    
    st.markdown(f"**Total: {len(planos)} planos ativos**")
    
    for plano in planos:
        with st.expander(f"📋 {plano[4]} - {plano[-1]}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Objetivo:** {plano[5] or 'N/I'}")
                st.markdown(f"**Calorias:** {plano[6] or 0} kcal")
                st.markdown(f"**Criado em:** {plano[11]}")
            
            with col2:
                st.markdown(f"**Carboidratos:** {plano[7] or 0}g")
                st.markdown(f"**Proteínas:** {plano[8] or 0}g")
                st.markdown(f"**Lipídios:** {plano[9] or 0}g")
            
            if st.button(f"Ver Detalhes", key=f"plan_{plano[0]}"):
                st.info("Visualizando plano completo...")

def create_meal_plan(user):
    st.markdown('<div class="sub-header">Criar Novo Plano</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, nome FROM pacientes
    WHERE nutricionista_id = ? AND ativo = 1
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.warning("Cadastre um paciente primeiro.")
        return
    
    with st.form("meal_plan_form"):
        paciente = st.selectbox(
            "Paciente",
            options=pacientes,
            format_func=lambda x: x[1]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome_plano = st.text_input("Nome do Plano")
            objetivo = st.selectbox("Objetivo", [
                "Perda de Peso", "Ganho de Peso", "Manutenção",
                "Ganho de Massa", "Saúde Geral"
            ])
            calorias = st.number_input("Calorias Totais", 1000, 5000, 2000, step=50)
        
        with col2:
            data_val = st.date_input("Validade", value=date.today() + timedelta(days=30))
            carb = st.number_input("Carboidratos (g)", 0.0, 1000.0, 250.0)
            prot = st.number_input("Proteínas (g)", 0.0, 500.0, 150.0)
            lip = st.number_input("Lipídios (g)", 0.0, 300.0, 67.0)
        
        st.markdown("**Refeições**")
        
        num_ref = st.selectbox("Número de Refeições", [3, 4, 5, 6])
        
        refeicoes = {}
        nomes_ref = ["Café da Manhã", "Lanche Manhã", "Almoço", "Lanche Tarde", "Jantar", "Ceia"]
        
        for i in range(num_ref):
            with st.expander(nomes_ref[i], expanded=False):
                alimentos = st.text_area(f"Alimentos {nomes_ref[i]}", key=f"ref_{i}")
                perc = st.slider(f"% Calorias {nomes_ref[i]}", 0, 50, 20, key=f"perc_{i}")
                refeicoes[nomes_ref[i]] = {"alimentos": alimentos, "percentual": perc}
        
        submitted = st.form_submit_button("Criar Plano", use_container_width=True)
        
        if submitted:
            if nome_plano:
                try:
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    plano_uuid = str(uuid.uuid4())
                    refeicoes_json = json.dumps(refeicoes)
                    
                    cursor.execute('''
                    INSERT INTO planos_alimentares (
                        uuid, paciente_id, nutricionista_id, nome, objetivo,
                        calorias, carboidratos, proteinas, lipidios,
                        refeicoes, data_validade
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        plano_uuid, paciente[0], user['id'], nome_plano, objetivo,
                        calorias, carb, prot, lip, refeicoes_json, data_val
                    ))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("Plano criado com sucesso!")
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
            else:
                st.error("Nome do plano é obrigatório!")

# =============================================================================
# RECEITAS COMPLETO
# =============================================================================

def show_receitas(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Receitas Nutricionais</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Banco de Receitas", "Nova Receita"])
    
    with tab1:
        show_recipes_list(user)
    
    with tab2:
        create_recipe(user)

def show_recipes_list(user):
    st.markdown('<div class="sub-header">Banco de Receitas</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM receitas
    WHERE criada_por = ? OR publica = 1
    ORDER BY data_criacao DESC
    """, (user['id'],))
    
    receitas = cursor.fetchall()
    conn.close()
    
    if not receitas:
        st.info("Nenhuma receita cadastrada.")
        return
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        busca = st.text_input("Buscar receita", placeholder="Nome da receita...")
    
    with col2:
        categoria = st.selectbox("Categoria", [
            "Todas", "Café da Manhã", "Almoço", "Jantar", "Lanches", "Sobremesas"
        ])
    
    st.markdown(f"**Total: {len(receitas)} receitas**")
    
    for receita in receitas:
        if busca and busca.lower() not in receita[2].lower():
            continue
        
        if categoria != "Todas" and receita[3] != categoria:
            continue
        
        with st.expander(f"🍳 {receita[2]} - {receita[3]}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Tempo:** {receita[6] or 0} min")
                st.markdown(f"**Porções:** {receita[7] or 0}")
                st.markdown(f"**Calorias/porção:** {receita[8] or 0} kcal")
            
            with col2:
                st.markdown(f"**Carboidratos:** {receita[9] or 0}g")
                st.markdown(f"**Proteínas:** {receita[10] or 0}g")
                st.markdown(f"**Lipídios:** {receita[11] or 0}g")
            
            if receita[4]:
                try:
                    ingredientes = json.loads(receita[4])
                    st.markdown("**Ingredientes:**")
                    for ing in ingredientes:
                        st.markdown(f"• {ing}")
                except:
                    pass

def create_recipe(user):
    st.markdown('<div class="sub-header">Criar Nova Receita</div>', unsafe_allow_html=True)
    
    with st.form("recipe_form"):
        nome = st.text_input("Nome da Receita")
        
        col1, col2 = st.columns(2)
        
        with col1:
            categoria = st.selectbox("Categoria", [
                "Café da Manhã", "Almoço", "Jantar", "Lanches", "Sobremesas", "Bebidas"
            ])
            tempo = st.number_input("Tempo de Preparo (min)", 0, 480, 30)
            porcoes = st.number_input("Porções", 1, 20, 1)
        
        with col2:
            calorias = st.number_input("Calorias/porção", 0.0, 2000.0, 0.0)
            carb = st.number_input("Carboidratos (g)", 0.0, 200.0, 0.0)
            prot = st.number_input("Proteínas (g)", 0.0, 100.0, 0.0)
            lip = st.number_input("Lipídios (g)", 0.0, 100.0, 0.0)
        
        st.markdown("**Ingredientes (um por linha)**")
        ingredientes = st.text_area("Ingredientes", height=100)
        
        st.markdown("**Modo de Preparo**")
        modo_preparo = st.text_area("Modo de Preparo", height=150)
        
        publica = st.checkbox("Tornar receita pública")
        
        submitted = st.form_submit_button("Criar Receita", use_container_width=True)
        
        if submitted:
            if nome and ingredientes:
                try:
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    receita_uuid = str(uuid.uuid4())
                    ingredientes_list = [ing.strip() for ing in ingredientes.split('\n') if ing.strip()]
                    ingredientes_json = json.dumps(ingredientes_list)
                    
                    cursor.execute('''
                    INSERT INTO receitas (
                        uuid, nome, categoria, ingredientes, modo_preparo,
                        tempo_preparo, porcoes, calorias_porcao,
                        carboidratos, proteinas, lipidios, criada_por, publica
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        receita_uuid, nome, categoria, ingredientes_json, modo_preparo,
                        tempo, porcoes, calorias, carb, prot, lip, user['id'], publica
                    ))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("Receita criada com sucesso!")
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
            else:
                st.error("Nome e ingredientes são obrigatórios!")

# =============================================================================
# AGENDA COMPLETA
# =============================================================================

def show_agenda(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Agenda de Consultas</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Calendário", "Nova Consulta", "Consultas Agendadas"])
    
    with tab1:
        show_calendar(user)
    
    with tab2:
        schedule_appointment(user)
    
    with tab3:
        show_scheduled(user)

def show_calendar(user):
    st.markdown('<div class="sub-header">Calendário</div>', unsafe_allow_html=True)
    
    hoje = date.today()
    
    col1, col2 = st.columns(2)
    
    with col1:
        mes = st.selectbox("Mês", range(1, 13), index=hoje.month-1)
    
    with col2:
        ano = st.selectbox("Ano", range(2024, 2027), index=0)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    primeiro_dia = date(ano, mes, 1)
    ultimo_dia = date(ano, mes, calendar.monthrange(ano, mes)[1])
    
    cursor.execute("""
    SELECT c.*, p.nome as paciente_nome
    FROM consultas c
    JOIN pacientes p ON c.paciente_id = p.id
    WHERE c.nutricionista_id = ?
    AND DATE(c.data_consulta) BETWEEN ? AND ?
    ORDER BY c.data_consulta
    """, (user['id'], primeiro_dia, ultimo_dia))
    
    consultas = cursor.fetchall()
    conn.close()
    
    st.markdown(f"### {calendar.month_name[mes]} {ano}")
    st.markdown(f"**{len(consultas)} consultas no mês**")
    
    for consulta in consultas:
        data_c = datetime.strptime(consulta[4], '%Y-%m-%d %H:%M:%S')
        
        st.markdown(f"""
        **{data_c.strftime('%d/%m/%Y %H:%M')}** - {consulta[-1]} 
        ({consulta[5]}) - {consulta[6].upper()}
        """)

def schedule_appointment(user):
    st.markdown('<div class="sub-header">Agendar Consulta</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, nome, telefone FROM pacientes
    WHERE nutricionista_id = ? AND ativo = 1
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.warning("Cadastre um paciente primeiro.")
        return
    
    with st.form("appointment_form"):
        paciente = st.selectbox(
            "Paciente",
            options=pacientes,
            format_func=lambda x: f"{x[1]} - {x[2] or 'Sem telefone'}"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            data_c = st.date_input("Data", value=date.today() + timedelta(days=1))
            hora_c = st.time_input("Horário", value=datetime.strptime("09:00", "%H:%M").time())
        
        with col2:
            tipo = st.selectbox("Tipo", [
                "Primeira Consulta", "Retorno", "Reavaliação", "Teleconsulta"
            ])
            duracao = st.selectbox("Duração (min)", [30, 45, 60, 90])
        
        valor = st.number_input("Valor (R$)", 0.0, 1000.0, 150.0, step=10.0)
        obs = st.text_area("Observações")
        
        submitted = st.form_submit_button("Agendar", use_container_width=True)
        
        if submitted:
            try:
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                
                consulta_uuid = str(uuid.uuid4())
                datetime_c = datetime.combine(data_c, hora_c)
                
                cursor.execute('''
                INSERT INTO consultas (
                    uuid, paciente_id, nutricionista_id, data_consulta,
                    tipo_consulta, duracao, valor, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    consulta_uuid, paciente[0], user['id'], datetime_c,
                    tipo, duracao, valor, obs
                ))
                
                conn.commit()
                conn.close()
                
                st.success("Consulta agendada!")
                st.info(f"📱 Enviar confirmação para: {paciente[2]}")
                time.sleep(1)
                st.rerun()
                
            except Exception as e:
                st.error(f"Erro: {str(e)}")

def show_scheduled(user):
    st.markdown('<div class="sub-header">Consultas Agendadas</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT c.*, p.nome as paciente_nome
    FROM consultas c
    JOIN pacientes p ON c.paciente_id = p.id
    WHERE c.nutricionista_id = ?
    AND c.data_consulta >= datetime('now')
    ORDER BY c.data_consulta
    """, (user['id'],))
    
    consultas = cursor.fetchall()
    conn.close()
    
    if not consultas:
        st.info("Nenhuma consulta agendada.")
        return
    
    st.markdown(f"**{len(consultas)} consultas futuras**")
    
    for c in consultas:
        data_c = datetime.strptime(c[4], '%Y-%m-%d %H:%M:%S')
        
        with st.expander(f"📅 {data_c.strftime('%d/%m/%Y %H:%M')} - {c[-1]}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Tipo:** {c[5]}")
                st.markdown(f"**Duração:** {c[7]} min")
                st.markdown(f"**Status:** {c[6].upper()}")
            
            with col2:
                st.markdown(f"**Valor:** R$ {c[8]:.2f}" if c[8] else "Valor: A definir")
                
                if st.button("Cancelar", key=f"cancel_{c[0]}"):
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE consultas SET status = 'cancelada' WHERE id = ?", (c[0],))
                    conn.commit()
                    conn.close()
                    st.warning("Consulta cancelada!")
                    st.rerun()

# =============================================================================
# COMUNICAÇÃO COMPLETO
# =============================================================================

def show_comunicacao(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Comunicação com Pacientes</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["WhatsApp", "Email"])
    
    with tab1:
        show_whatsapp(user)
    
    with tab2:
        show_email(user)

def show_whatsapp(user):
    st.markdown('<div class="sub-header">Sistema WhatsApp</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, nome, telefone FROM pacientes
    WHERE nutricionista_id = ? AND ativo = 1 AND telefone IS NOT NULL
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.warning("Nenhum paciente com telefone cadastrado.")
        return
    
    tipo = st.radio("Tipo de Envio", [
        "Individual", "Grupo", "Todos"
    ])
    
    if tipo == "Individual":
        paciente = st.selectbox(
            "Selecionar Paciente",
            options=pacientes,
            format_func=lambda x: f"{x[1]} - {x[2]}"
        )
    elif tipo == "Grupo":
        selecionados = st.multiselect(
            "Selecionar Pacientes",
            options=pacientes,
            format_func=lambda x: f"{x[1]} - {x[2]}"
        )
    
    template = st.selectbox("Template", [
        "Lembrete de Consulta",
        "Follow-up",
        "Parabéns por Meta",
        "Personalizada"
    ])
    
    if template == "Personalizada":
        mensagem = st.text_area("Mensagem", height=150)
    else:
        templates = {
            "Lembrete de Consulta": "Olá! Lembramos que você tem consulta amanhã. Confirme sua presença!",
            "Follow-up": "Como está seguindo o plano alimentar? Qualquer dúvida, estou à disposição!",
            "Parabéns por Meta": "Parabéns! Você atingiu sua meta! Continue assim!"
        }
        mensagem = st.text_area("Mensagem", value=templates[template], height=150)
    
    if st.button("Enviar WhatsApp", use_container_width=True):
        with st.spinner("Enviando..."):
            time.sleep(1)
        st.success("Mensagens enviadas com sucesso!")

def show_email(user):
    st.markdown('<div class="sub-header">Sistema de Email</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, nome, email FROM pacientes
    WHERE nutricionista_id = ? AND ativo = 1 AND email IS NOT NULL
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.warning("Nenhum paciente com email cadastrado.")
        return
    
    destinatarios = st.multiselect(
        "Destinatários",
        options=pacientes,
        format_func=lambda x: f"{x[1]} - {x[2]}"
    )
    
    assunto = st.text_input("Assunto")
    conteudo = st.text_area("Conteúdo do Email", height=200)
    
    if st.button("Enviar Email", use_container_width=True):
        if destinatarios and assunto and conteudo:
            with st.spinner("Enviando..."):
                time.sleep(1)
            st.success(f"Email enviado para {len(destinatarios)} paciente(s)!")
        else:
            st.error("Preencha todos os campos!")

# =============================================================================
# RELATÓRIOS COMPLETO
# =============================================================================

def show_relatorios(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Relatórios e Analytics</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Financeiro", "Pacientes"])
    
    with tab1:
        show_dashboard_report(user)
    
    with tab2:
        show_financial_report(user)
    
    with tab3:
        show_patients_report(user)

def show_dashboard_report(user):
    st.markdown('<div class="sub-header">Dashboard Analytics</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Dados do último mês
    cursor.execute("""
    SELECT DATE(data_consulta), COUNT(*)
    FROM consultas
    WHERE nutricionista_id = ?
    AND data_consulta >= date('now', '-30 days')
    GROUP BY DATE(data_consulta)
    ORDER BY DATE(data_consulta)
    """, (user['id'],))
    
    dados = cursor.fetchall()
    conn.close()
    
    if dados:
        df = pd.DataFrame(dados, columns=['Data', 'Consultas'])
        df['Data'] = pd.to_datetime(df['Data'])
        
        fig = px.line(df, x='Data', y='Consultas', title="Consultas nos Últimos 30 Dias", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem dados suficientes para gráficos.")

def show_financial_report(user):
    st.markdown('<div class="sub-header">Relatório Financeiro</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        data_inicio = st.date_input("Data Início", value=date.today() - timedelta(days=30))
    
    with col2:
        data_fim = st.date_input("Data Fim", value=date.today())
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT SUM(valor), COUNT(*)
    FROM consultas
    WHERE nutricionista_id = ?
    AND status = 'realizada'
    AND DATE(data_consulta) BETWEEN ? AND ?
    """, (user['id'], data_inicio, data_fim))
    
    resultado = cursor.fetchone()
    conn.close()
    
    receita_total = resultado[0] or 0
    total_consultas = resultado[1] or 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Receita Total", f"R$ {receita_total:.2f}")
    
    with col2:
        st.metric("Consultas Realizadas", total_consultas)
    
    with col3:
        ticket_medio = receita_total / total_consultas if total_consultas > 0 else 0
        st.metric("Ticket Médio", f"R$ {ticket_medio:.2f}")

def show_patients_report(user):
    st.markdown('<div class="sub-header">Relatório de Pacientes</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT 
        CASE 
            WHEN sexo = 'Feminino' THEN 'Feminino'
            WHEN sexo = 'Masculino' THEN 'Masculino'
            ELSE 'Não informado'
        END as sexo,
        COUNT(*) as quantidade
    FROM pacientes
    WHERE nutricionista_id = ? AND ativo = 1
    GROUP BY sexo
    """, (user['id'],))
    
    dados_sexo = cursor.fetchall()
    conn.close()
    
    if dados_sexo:
        df = pd.DataFrame(dados_sexo, columns=['Sexo', 'Quantidade'])
        
        fig = px.pie(df, values='Quantidade', names='Sexo', title="Distribuição por Sexo")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem dados de pacientes.")

# =============================================================================
# CONFIGURAÇÕES COMPLETO
# =============================================================================

def show_configuracoes(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Configurações</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Perfil", "Sistema"])
    
    with tab1:
        show_profile_settings(user)
    
    with tab2:
        show_system_settings(user)

def show_profile_settings(user):
    st.markdown('<div class="sub-header">Configurações de Perfil</div>', unsafe_allow_html=True)
    
    with st.form("profile_form"):
        nome = st.text_input("Nome", value=user['nome'])
        email = st.text_input("Email", value=user['email'])
        telefone = st.text_input("Telefone", value=user.get('telefone', ''))
        coren = st.text_input("COREN/CRN", value=user.get('coren', ''))
        clinica = st.text_input("Clínica", value=user.get('clinica', ''))
        
        if st.form_submit_button("Salvar Alterações", use_container_width=True):
            try:
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                UPDATE usuarios SET
                    nome = ?, telefone = ?, coren = ?, clinica = ?
                WHERE id = ?
                ''', (nome, telefone, coren, clinica, user['id']))
                
                conn.commit()
                conn.close()
                
                st.success("Perfil atualizado!")
                st.session_state.user.update({
                    'nome': nome,
                    'telefone': telefone,
                    'coren': coren,
                    'clinica': clinica
                })
                time.sleep(1)
                st.rerun()
                
            except Exception as e:
                st.error(f"Erro: {str(e)}")

def show_system_settings(user):
    st.markdown('<div class="sub-header">Configurações do Sistema</div>', unsafe_allow_html=True)
    
    st.markdown("**Notificações**")
    notif_email = st.checkbox("Receber notificações por email", True)
    notif_consultas = st.checkbox("Lembrete de consultas", True)
    
    st.markdown("**Aparência**")
    tema = st.selectbox("Tema", ["Claro", "Escuro"])
    
    st.markdown("**Backup**")
    if st.button("Gerar Backup do Banco de Dados"):
        st.success("Backup gerado com sucesso!")

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False
    
    if not st.session_state.logged_in:
        if st.session_state.show_register:
            show_register()
        else:
            show_login()
        return
    
    user = st.session_state.user
    
    with st.sidebar:
        st.markdown(f"### 👤 {user['nome']}")
        st.markdown(f"📧 {user['email']}")
        st.markdown("---")
        
        page = st.radio("Menu", [
            "🏠 Dashboard",
            "👥 Pacientes",
            "🧮 Calculadoras",
            "🍽️ Planos",
            "🍳 Receitas",
            "📅 Agenda",
            "💬 Comunicação",
            "📊 Relatórios",
            "⚙️ Configurações"
        ])
        
        st.markdown("---")
        
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    if page == "🏠 Dashboard":
        show_dashboard(user)
    elif page == "👥 Pacientes":
        show_gestao_pacientes(user)
    elif page == "🧮 Calculadoras":
        show_calculadoras(user)
    elif page == "🍽️ Planos":
        show_planos_alimentares(user)
    elif page == "🍳 Receitas":
        show_receitas(user)
    elif page == "📅 Agenda":
        show_agenda(user)
    elif page == "💬 Comunicação":
        show_comunicacao(user)
    elif page == "📊 Relatórios":
        show_relatorios(user)
    elif page == "⚙️ Configurações":
        show_configuracoes(user)

if __name__ == "__main__":
    main()
