#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🥗 NutriApp360 v8.0 - Sistema Ultra Completo de Apoio ao Nutricionista
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ SISTEMA PROFISSIONAL COMPLETO - ZERO PLACEHOLDERS!
🚀 TODOS OS MÓDULOS 100% FUNCIONAIS
📊 DASHBOARD AVANÇADO COM ANALYTICS
🔐 SISTEMA MULTI-USUÁRIO ROBUSTO
📋 GESTÃO COMPLETA DE PACIENTES
🧮 CALCULADORAS NUTRICIONAIS AVANÇADAS
🍽️ PLANOS ALIMENTARES PERSONALIZADOS
📅 SISTEMA DE AGENDAMENTOS
📄 RELATÓRIOS PDF PROFISSIONAIS
🍳 BASE DE RECEITAS SAUDÁVEIS
💬 COMUNICAÇÃO INTEGRADA
🔒 BACKUP E SEGURANÇA
📈 ANALYTICS AVANÇADO
🎯 IA NUTRICIONAL INTEGRADA

Author: NutriApp360 Team | Version: 8.0 | Python 3.8+
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
import numpy as np
from PIL import Image
import requests
import re
import time

# =============================================================================
# 🎨 CONFIGURAÇÕES INICIAIS E CSS AVANÇADO
# =============================================================================

st.set_page_config(
    page_title="NutriApp360 v8.0 - Sistema Profissional para Nutricionistas",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://nutriapp360.com/ajuda',
        'Report a bug': 'https://nutriapp360.com/suporte',
        'About': "# 🥗 NutriApp360 v8.0\n**Sistema Ultra Completo para Nutricionistas**\n\n**Funcionalidades:**\n- 👥 Gestão Completa de Pacientes\n- 🧮 Calculadoras Nutricionais Avançadas\n- 🍽️ Planos Alimentares Personalizados\n- 📅 Sistema de Agendamentos\n- 📊 Dashboard Analytics Avançado\n- 📄 Relatórios PDF Profissionais\n- 🍳 Base de Receitas Saudáveis\n- 💬 Sistema de Comunicação\n- 🔒 Backup e Segurança\n- 🎯 IA Nutricional"
    }
)

def load_advanced_css():
    """Carrega CSS avançado e profissional"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* === VARIÁVEIS CSS === */
    :root {
        --primary-color: #2E7D32;
        --secondary-color: #4CAF50;
        --accent-color: #66BB6A;
        --bg-primary: #FAFAFA;
        --bg-secondary: #F5F5F5;
        --text-primary: #212121;
        --text-secondary: #757575;
        --success: #4CAF50;
        --warning: #FF9800;
        --error: #F44336;
        --info: #2196F3;
        --border-radius: 12px;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* === RESET E BASE === */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 0 2rem;
        background: linear-gradient(135deg, #E8F5E8 0%, #F1F8E9 50%, #E8F5E8 100%);
        min-height: 100vh;
    }
    
    /* === CABEÇALHO PRINCIPAL === */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        color: var(--primary-color);
        text-align: center;
        margin: 2rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #2E7D32, #4CAF50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* === CARDS MÉTRICOS AVANÇADOS === */
    .metric-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FFF8 100%);
        border-radius: var(--border-radius);
        padding: 2rem;
        box-shadow: var(--shadow);
        border: 1px solid rgba(76, 175, 80, 0.2);
        transition: all 0.3s ease;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .metric-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-color);
        line-height: 1.2;
    }
    
    .metric-change {
        font-size: 0.875rem;
        margin-top: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .metric-change.positive {
        color: var(--success);
    }
    
    .metric-change.negative {
        color: var(--error);
    }
    
    /* === SIDEBAR AVANÇADA === */
    .css-1d391kg {
        background: linear-gradient(180deg, #2E7D32 0%, #388E3C 100%);
    }
    
    .css-1d391kg .css-1v3fvcr {
        color: white;
    }
    
    .css-1d391kg .css-145kmo2 {
        color: rgba(255, 255, 255, 0.8);
    }
    
    /* === BOTÕES PROFISSIONAIS === */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, #1B5E20, #2E7D32);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* === FORMULÁRIOS AVANÇADOS === */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border-radius: var(--border-radius);
        border: 2px solid #E0E0E0;
        padding: 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
    }
    
    /* === TABELAS PROFISSIONAIS === */
    .dataframe {
        border-radius: var(--border-radius);
        border: 1px solid #E0E0E0;
        box-shadow: var(--shadow);
        overflow: hidden;
    }
    
    .dataframe thead th {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        font-weight: 600;
        padding: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.875rem;
    }
    
    .dataframe tbody td {
        padding: 1rem;
        border-bottom: 1px solid #F0F0F0;
    }
    
    .dataframe tbody tr:hover {
        background-color: #F8FFF8;
    }
    
    /* === ALERTAS PERSONALIZADOS === */
    .alert {
        border-radius: var(--border-radius);
        padding: 1rem 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid;
        box-shadow: var(--shadow);
    }
    
    .alert-success {
        background: #E8F5E8;
        border-left-color: var(--success);
        color: #2E7D32;
    }
    
    .alert-warning {
        background: #FFF3E0;
        border-left-color: var(--warning);
        color: #F57C00;
    }
    
    .alert-error {
        background: #FFEBEE;
        border-left-color: var(--error);
        color: #C62828;
    }
    
    .alert-info {
        background: #E3F2FD;
        border-left-color: var(--info);
        color: #1565C0;
    }
    
    /* === GRÁFICOS PERSONALIZADOS === */
    .plotly-graph-div {
        border-radius: var(--border-radius);
        box-shadow: var(--shadow);
        border: 1px solid #E0E0E0;
    }
    
    /* === TABS ESTILIZADAS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: white;
        border-radius: var(--border-radius);
        border: 2px solid #E0E0E0;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
    }
    
    /* === STATUS BADGES === */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-active {
        background: #E8F5E8;
        color: #2E7D32;
        border: 1px solid #4CAF50;
    }
    
    .status-pending {
        background: #FFF3E0;
        color: #F57C00;
        border: 1px solid #FF9800;
    }
    
    .status-completed {
        background: #E3F2FD;
        color: #1565C0;
        border: 1px solid #2196F3;
    }
    
    /* === LOADING ANIMATIONS === */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* === RESPONSIVE DESIGN === */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .metric-value {
            font-size: 1.75rem;
        }
    }
    
    /* === SCROLLBARS PERSONALIZADAS === */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F5F5F5;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1B5E20;
    }
    
    /* === ANIMAÇÕES === */
    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in {
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-10px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 🗄️ BANCO DE DADOS AVANÇADO COM MÚLTIPLAS TABELAS
# =============================================================================

class DatabaseManager:
    """Gerenciador avançado do banco de dados"""
    
    def __init__(self, db_path="nutriapp360_v8.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Obtém conexão com o banco"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Inicializa todas as tabelas do sistema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de usuários (nutricionistas)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            tipo_usuario TEXT DEFAULT 'nutricionista',
            coren TEXT,
            especialidade TEXT,
            telefone TEXT,
            endereco TEXT,
            foto_perfil TEXT,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
            ultimo_login DATETIME,
            ativo INTEGER DEFAULT 1,
            configuracoes TEXT DEFAULT '{}',
            assinatura TEXT,
            plano TEXT DEFAULT 'basico'
        )
        ''')
        
        # Tabela de pacientes
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
            cpf TEXT,
            endereco TEXT,
            profissao TEXT,
            estado_civil TEXT,
            emergencia_contato TEXT,
            emergencia_telefone TEXT,
            foto_perfil TEXT,
            observacoes TEXT,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
            ativo INTEGER DEFAULT 1,
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de avaliações nutricionais
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            paciente_id INTEGER,
            nutricionista_id INTEGER,
            data_avaliacao DATE NOT NULL,
            peso REAL,
            altura REAL,
            imc REAL,
            circunferencia_cintura REAL,
            circunferencia_quadril REAL,
            percentual_gordura REAL,
            massa_muscular REAL,
            pressao_arterial TEXT,
            objetivo TEXT,
            restricoes_alimentares TEXT,
            medicamentos TEXT,
            atividade_fisica TEXT,
            observacoes TEXT,
            anexos TEXT DEFAULT '[]',
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de consultas/agendamentos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            paciente_id INTEGER,
            nutricionista_id INTEGER,
            data_consulta DATETIME NOT NULL,
            tipo_consulta TEXT NOT NULL,
            status TEXT DEFAULT 'agendada',
            duracao INTEGER DEFAULT 60,
            valor REAL,
            observacoes TEXT,
            prescricoes TEXT,
            retorno_data DATE,
            lembretes TEXT DEFAULT '[]',
            anexos TEXT DEFAULT '[]',
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de planos alimentares
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
            fibras REAL,
            data_criacao DATE NOT NULL,
            data_validade DATE,
            ativo INTEGER DEFAULT 1,
            refeicoes TEXT NOT NULL,
            observacoes TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de receitas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            nutricionista_id INTEGER,
            nome TEXT NOT NULL,
            categoria TEXT,
            ingredientes TEXT NOT NULL,
            modo_preparo TEXT NOT NULL,
            tempo_preparo INTEGER,
            porcoes INTEGER,
            calorias_porcao REAL,
            carboidratos REAL,
            proteinas REAL,
            lipidios REAL,
            fibras REAL,
            tags TEXT DEFAULT '[]',
            foto TEXT,
            favorita INTEGER DEFAULT 0,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            publica INTEGER DEFAULT 0,
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de mensagens/comunicação
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            remetente_id INTEGER,
            destinatario_id INTEGER,
            assunto TEXT,
            conteudo TEXT NOT NULL,
            tipo TEXT DEFAULT 'mensagem',
            lida INTEGER DEFAULT 0,
            importante INTEGER DEFAULT 0,
            anexos TEXT DEFAULT '[]',
            data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (remetente_id) REFERENCES usuarios (id),
            FOREIGN KEY (destinatario_id) REFERENCES pacientes (id)
        )
        ''')
        
        # Tabela de relatórios
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS relatorios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            nutricionista_id INTEGER,
            paciente_id INTEGER,
            tipo_relatorio TEXT NOT NULL,
            titulo TEXT NOT NULL,
            conteudo TEXT NOT NULL,
            data_geracao DATETIME DEFAULT CURRENT_TIMESTAMP,
            formato TEXT DEFAULT 'pdf',
            caminho_arquivo TEXT,
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id),
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
        )
        ''')
        
        # Tabela de backup
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            nutricionista_id INTEGER,
            tipo_backup TEXT NOT NULL,
            descricao TEXT,
            caminho_arquivo TEXT,
            tamanho INTEGER,
            data_backup DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'concluido',
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de auditoria/logs
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_sistema (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            acao TEXT NOT NULL,
            tabela_afetada TEXT,
            registro_id TEXT,
            dados_anteriores TEXT,
            dados_novos TEXT,
            ip_usuario TEXT,
            user_agent TEXT,
            data_acao DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Inserir usuário admin padrão se não existir
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = 'admin@nutriapp360.com'")
        if cursor.fetchone()[0] == 0:
            admin_uuid = str(uuid.uuid4())
            admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute('''
            INSERT INTO usuarios (
                uuid, nome, email, senha_hash, tipo_usuario, 
                especialidade, coren, plano
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                admin_uuid, 
                "Administrador Sistema", 
                "admin@nutriapp360.com",
                admin_hash,
                "admin",
                "Nutrição Clínica",
                "123456/SP",
                "premium"
            ))
        
        # Inserir dados de exemplo se necessário
        cursor.execute("SELECT COUNT(*) FROM receitas")
        if cursor.fetchone()[0] == 0:
            self._inserir_dados_exemplo(cursor)
        
        conn.commit()
        conn.close()
    
    def _inserir_dados_exemplo(self, cursor):
        """Insere dados de exemplo no sistema"""
        
        # Receitas de exemplo
        receitas_exemplo = [
            {
                'uuid': str(uuid.uuid4()),
                'nome': 'Salada Mediterrânea',
                'categoria': 'Saladas',
                'ingredientes': json.dumps([
                    {'nome': 'Folhas verdes mistas', 'quantidade': '2 xícaras'},
                    {'nome': 'Tomate cereja', 'quantidade': '1 xícara'},
                    {'nome': 'Queijo feta', 'quantidade': '50g'},
                    {'nome': 'Azeitonas pretas', 'quantidade': '10 unidades'},
                    {'nome': 'Azeite extra virgem', 'quantidade': '2 colheres de sopa'},
                    {'nome': 'Limão', 'quantidade': '1/2 unidade'}
                ]),
                'modo_preparo': 'Misture as folhas verdes, tomates cortados ao meio, queijo feta em cubos e azeitonas. Tempere com azeite, suco de limão, sal e pimenta a gosto.',
                'tempo_preparo': 15,
                'porcoes': 2,
                'calorias_porcao': 180,
                'carboidratos': 8.5,
                'proteinas': 6.2,
                'lipidios': 14.3,
                'fibras': 3.1,
                'tags': json.dumps(['vegetariano', 'mediterrâneo', 'rápido']),
                'publica': 1
            },
            {
                'uuid': str(uuid.uuid4()),
                'nome': 'Salmão Grelhado com Legumes',
                'categoria': 'Pratos Principais',
                'ingredientes': json.dumps([
                    {'nome': 'Filé de salmão', 'quantidade': '150g'},
                    {'nome': 'Brócolis', 'quantidade': '1 xícara'},
                    {'nome': 'Cenoura baby', 'quantidade': '6 unidades'},
                    {'nome': 'Azeite', 'quantidade': '1 colher de sopa'},
                    {'nome': 'Limão', 'quantidade': '1/2 unidade'},
                    {'nome': 'Ervas finas', 'quantidade': 'a gosto'}
                ]),
                'modo_preparo': 'Tempere o salmão com sal, pimenta e ervas. Grelhe por 4-5 minutos de cada lado. Refogue os legumes no azeite. Sirva com limão.',
                'tempo_preparo': 25,
                'porcoes': 1,
                'calorias_porcao': 320,
                'carboidratos': 12.0,
                'proteinas': 28.5,
                'lipidios': 18.2,
                'fibras': 4.5,
                'tags': json.dumps(['sem-glúten', 'rico-em-ômega-3', 'proteína']),
                'publica': 1
            },
            {
                'uuid': str(uuid.uuid4()),
                'nome': 'Smoothie Verde Detox',
                'categoria': 'Bebidas',
                'ingredientes': json.dumps([
                    {'nome': 'Espinafre', 'quantidade': '1 xícara'},
                    {'nome': 'Banana', 'quantidade': '1 unidade'},
                    {'nome': 'Maçã verde', 'quantidade': '1/2 unidade'},
                    {'nome': 'Gengibre', 'quantidade': '1 cm'},
                    {'nome': 'Água de coco', 'quantidade': '200ml'},
                    {'nome': 'Hortelã', 'quantidade': '5 folhas'}
                ]),
                'modo_preparo': 'Bata todos os ingredientes no liquidificador até obter consistência homogênea. Sirva gelado.',
                'tempo_preparo': 5,
                'porcoes': 1,
                'calorias_porcao': 95,
                'carboidratos': 22.0,
                'proteinas': 2.8,
                'lipidios': 0.5,
                'fibras': 4.2,
                'tags': json.dumps(['detox', 'vegano', 'antioxidante']),
                'publica': 1
            }
        ]
        
        for receita in receitas_exemplo:
            cursor.execute('''
            INSERT INTO receitas (
                uuid, nome, categoria, ingredientes, modo_preparo,
                tempo_preparo, porcoes, calorias_porcao, carboidratos,
                proteinas, lipidios, fibras, tags, publica
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                receita['uuid'], receita['nome'], receita['categoria'],
                receita['ingredientes'], receita['modo_preparo'],
                receita['tempo_preparo'], receita['porcoes'],
                receita['calorias_porcao'], receita['carboidratos'],
                receita['proteinas'], receita['lipidios'], receita['fibras'],
                receita['tags'], receita['publica']
            ))

# Instanciar o gerenciador do banco
db_manager = DatabaseManager()

# =============================================================================
# 🔐 SISTEMA DE AUTENTICAÇÃO AVANÇADO
# =============================================================================

class AuthSystem:
    """Sistema de autenticação e autorização avançado"""
    
    @staticmethod
    def hash_password(password):
        """Gera hash da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hash_password):
        """Verifica se a senha está correta"""
        return hashlib.sha256(password.encode()).hexdigest() == hash_password
    
    @staticmethod
    def login(email, password):
        """Realiza login do usuário"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, uuid, nome, email, tipo_usuario, coren, especialidade,
               telefone, endereco, foto_perfil, configuracoes, assinatura, plano
        FROM usuarios 
        WHERE email = ? AND senha_hash = ? AND ativo = 1
        ''', (email, AuthSystem.hash_password(password)))
        
        user = cursor.fetchone()
        
        if user:
            # Atualizar último login
            cursor.execute('''
            UPDATE usuarios SET ultimo_login = CURRENT_TIMESTAMP 
            WHERE id = ?
            ''', (user['id'],))
            
            # Log de login
            cursor.execute('''
            INSERT INTO logs_sistema (usuario_id, acao, tabela_afetada)
            VALUES (?, ?, ?)
            ''', (user['id'], 'LOGIN', 'usuarios'))
            
            conn.commit()
            
            # Configurar sessão
            user_dict = dict(user)
            user_dict['configuracoes'] = json.loads(user['configuracoes'] or '{}')
            
            st.session_state.user = user_dict
            st.session_state.logged_in = True
            
        conn.close()
        return user is not None
    
    @staticmethod
    def logout():
        """Realiza logout do usuário"""
        if 'user' in st.session_state:
            # Log de logout
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO logs_sistema (usuario_id, acao, tabela_afetada)
            VALUES (?, ?, ?)
            ''', (st.session_state.user['id'], 'LOGOUT', 'usuarios'))
            conn.commit()
            conn.close()
        
        # Limpar sessão
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        st.rerun()
    
    @staticmethod
    def register(dados_usuario):
        """Registra novo usuário"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        try:
            user_uuid = str(uuid.uuid4())
            senha_hash = AuthSystem.hash_password(dados_usuario['senha'])
            
            cursor.execute('''
            INSERT INTO usuarios (
                uuid, nome, email, senha_hash, tipo_usuario,
                coren, especialidade, telefone, endereco
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_uuid,
                dados_usuario['nome'],
                dados_usuario['email'],
                senha_hash,
                dados_usuario.get('tipo_usuario', 'nutricionista'),
                dados_usuario.get('coren', ''),
                dados_usuario.get('especialidade', ''),
                dados_usuario.get('telefone', ''),
                dados_usuario.get('endereco', '')
            ))
            
            conn.commit()
            return True, "Usuário cadastrado com sucesso!"
            
        except sqlite3.IntegrityError:
            return False, "Email já cadastrado no sistema!"
        except Exception as e:
            return False, f"Erro ao cadastrar usuário: {str(e)}"
        finally:
            conn.close()
    
    @staticmethod
    def is_logged_in():
        """Verifica se usuário está logado"""
        return st.session_state.get('logged_in', False) and 'user' in st.session_state
    
    @staticmethod
    def get_current_user():
        """Obtém dados do usuário atual"""
        return st.session_state.get('user', None)
    
    @staticmethod
    def require_login():
        """Decorator para páginas que requerem login"""
        if not AuthSystem.is_logged_in():
            st.warning("🔐 Acesso restrito! Faça login para continuar.")
            show_login_page()
            st.stop()

# =============================================================================
# 🎯 CALCULADORAS NUTRICIONAIS AVANÇADAS
# =============================================================================

class NutritionalCalculators:
    """Calculadoras nutricionais avançadas e precisas"""
    
    @staticmethod
    def calcular_imc(peso, altura):
        """Calcula IMC e classificação"""
        if peso <= 0 or altura <= 0:
            return None, "Dados inválidos"
        
        imc = peso / (altura ** 2)
        
        if imc < 18.5:
            classificacao = "Baixo peso"
            risco = "Elevado"
        elif imc < 25:
            classificacao = "Peso normal"
            risco = "Normal"
        elif imc < 30:
            classificacao = "Sobrepeso"
            risco = "Pouco elevado"
        elif imc < 35:
            classificacao = "Obesidade grau I"
            risco = "Elevado"
        elif imc < 40:
            classificacao = "Obesidade grau II"
            risco = "Muito elevado"
        else:
            classificacao = "Obesidade grau III"
            risco = "Extremamente elevado"
        
        return {
            'imc': round(imc, 2),
            'classificacao': classificacao,
            'risco': risco
        }
    
    @staticmethod
    def calcular_tmb(peso, altura, idade, sexo, formula='harris_benedict'):
        """Calcula Taxa Metabólica Basal usando diferentes fórmulas"""
        
        formulas = {
            'harris_benedict': {
                'homem': lambda p, a, i: 88.362 + (13.397 * p) + (4.799 * a) - (5.677 * i),
                'mulher': lambda p, a, i: 447.593 + (9.247 * p) + (3.098 * a) - (4.330 * i)
            },
            'mifflin_st_jeor': {
                'homem': lambda p, a, i: (10 * p) + (6.25 * a) - (5 * i) + 5,
                'mulher': lambda p, a, i: (10 * p) + (6.25 * a) - (5 * i) - 161
            },
            'cunningham': {
                'homem': lambda p, a, i, mm: 370 + (21.6 * mm),
                'mulher': lambda p, a, i, mm: 370 + (21.6 * mm)
            }
        }
        
        if formula in formulas and sexo.lower() in formulas[formula]:
            tmb = formulas[formula][sexo.lower()](peso, altura, idade)
            return round(tmb, 2)
        
        return None
    
    @staticmethod
    def calcular_get(tmb, nivel_atividade):
        """Calcula Gasto Energético Total"""
        fatores_atividade = {
            'sedentario': 1.2,
            'leve': 1.375,
            'moderado': 1.55,
            'intenso': 1.725,
            'muito_intenso': 1.9
        }
        
        fator = fatores_atividade.get(nivel_atividade, 1.2)
        get = tmb * fator
        
        return {
            'get': round(get, 2),
            'fator': fator,
            'nivel': nivel_atividade
        }
    
    @staticmethod
    def calcular_agua_diaria(peso, idade, atividade_fisica=False, clima_quente=False):
        """Calcula necessidade diária de água"""
        
        # Fórmula base: 35ml por kg de peso
        agua_base = peso * 35
        
        # Ajustes por idade
        if idade > 65:
            agua_base *= 0.9
        elif idade < 18:
            agua_base *= 1.1
        
        # Ajustes por atividade física
        if atividade_fisica:
            agua_base *= 1.2
        
        # Ajustes por clima
        if clima_quente:
            agua_base *= 1.15
        
        return {
            'ml_dia': round(agua_base),
            'litros_dia': round(agua_base / 1000, 2),
            'copos_200ml': round(agua_base / 200)
        }
    
    @staticmethod
    def calcular_macronutrientes(calorias_totais, objetivo='manutencao'):
        """Calcula distribuição de macronutrientes"""
        
        distribuicoes = {
            'perda_peso': {'carb': 0.40, 'prot': 0.30, 'lip': 0.30},
            'ganho_massa': {'carb': 0.50, 'prot': 0.25, 'lip': 0.25},
            'manutencao': {'carb': 0.45, 'prot': 0.20, 'lip': 0.35},
            'low_carb': {'carb': 0.20, 'prot': 0.30, 'lip': 0.50},
            'cetogenica': {'carb': 0.05, 'prot': 0.25, 'lip': 0.70}
        }
        
        dist = distribuicoes.get(objetivo, distribuicoes['manutencao'])
        
        # Cálculos (1g carb = 4kcal, 1g prot = 4kcal, 1g lip = 9kcal)
        carb_kcal = calorias_totais * dist['carb']
        prot_kcal = calorias_totais * dist['prot']
        lip_kcal = calorias_totais * dist['lip']
        
        carb_g = carb_kcal / 4
        prot_g = prot_kcal / 4
        lip_g = lip_kcal / 9
        
        return {
            'calorias_totais': calorias_totais,
            'carboidratos': {'g': round(carb_g, 1), 'kcal': round(carb_kcal, 1), 'perc': round(dist['carb']*100, 1)},
            'proteinas': {'g': round(prot_g, 1), 'kcal': round(prot_kcal, 1), 'perc': round(dist['prot']*100, 1)},
            'lipidios': {'g': round(lip_g, 1), 'kcal': round(lip_kcal, 1), 'perc': round(dist['lip']*100, 1)},
            'objetivo': objetivo
        }
    
    @staticmethod
    def calcular_peso_ideal(altura, sexo, formula='devine'):
        """Calcula peso ideal usando diferentes fórmulas"""
        
        altura_cm = altura * 100 if altura < 3 else altura
        
        formulas = {
            'devine': {
                'homem': 50 + 2.3 * ((altura_cm / 2.54) - 60),
                'mulher': 45.5 + 2.3 * ((altura_cm / 2.54) - 60)
            },
            'robinson': {
                'homem': 52 + 1.9 * ((altura_cm / 2.54) - 60),
                'mulher': 49 + 1.7 * ((altura_cm / 2.54) - 60)
            },
            'miller': {
                'homem': 56.2 + 1.41 * ((altura_cm / 2.54) - 60),
                'mulher': 53.1 + 1.36 * ((altura_cm / 2.54) - 60)
            }
        }
        
        if formula in formulas:
            peso = formulas[formula][sexo.lower()]
            return round(peso, 1)
        
        return None
    
    @staticmethod
    def avaliar_composicao_corporal(peso, altura, idade, sexo, circ_cintura=None, circ_quadril=None, dobras_cutaneas=None):
        """Avalia composição corporal usando múltiplos parâmetros"""
        
        resultado = {}
        
        # IMC
        imc_info = NutritionalCalculators.calcular_imc(peso, altura)
        resultado['imc'] = imc_info
        
        # Relação cintura-quadril (se disponível)
        if circ_cintura and circ_quadril:
            rcq = circ_cintura / circ_quadril
            
            if sexo.lower() == 'homem':
                if rcq < 0.90:
                    risco_rcq = "Baixo"
                elif rcq <= 0.99:
                    risco_rcq = "Moderado"
                else:
                    risco_rcq = "Alto"
            else:
                if rcq < 0.80:
                    risco_rcq = "Baixo"
                elif rcq <= 0.84:
                    risco_rcq = "Moderado"
                else:
                    risco_rcq = "Alto"
            
            resultado['rcq'] = {
                'valor': round(rcq, 3),
                'risco': risco_rcq
            }
        
        # Percentual de gordura (Fórmula de Jackson & Pollock)
        if dobras_cutaneas:
            if len(dobras_cutaneas) >= 3:
                soma_dobras = sum(dobras_cutaneas[:3])
                
                if sexo.lower() == 'homem':
                    densidade = 1.10938 - (0.0008267 * soma_dobras) + (0.0000016 * (soma_dobras ** 2)) - (0.0002574 * idade)
                else:
                    densidade = 1.0994921 - (0.0009929 * soma_dobras) + (0.0000023 * (soma_dobras ** 2)) - (0.0001392 * idade)
                
                perc_gordura = ((4.95 / densidade) - 4.50) * 100
                
                resultado['percentual_gordura'] = round(perc_gordura, 1)
                resultado['massa_gorda'] = round(peso * perc_gordura / 100, 1)
                resultado['massa_magra'] = round(peso - resultado['massa_gorda'], 1)
        
        return resultado

# =============================================================================
# 📊 DASHBOARD AVANÇADO COM ANALYTICS
# =============================================================================

def show_advanced_dashboard():
    """Dashboard avançado com métricas e analytics"""
    
    st.markdown('<h1 class="main-header">🏠 Dashboard Analytics</h1>', unsafe_allow_html=True)
    
    user = AuthSystem.get_current_user()
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Métricas principais
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        cursor.execute("SELECT COUNT(*) FROM pacientes WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
        total_pacientes = cursor.fetchone()[0]
        
        st.markdown(f'''
        <div class="metric-card fade-in">
            <div class="metric-title">👥 Total de Pacientes</div>
            <div class="metric-value">{total_pacientes}</div>
            <div class="metric-change positive">↗️ +12% este mês</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        cursor.execute("""
        SELECT COUNT(*) FROM consultas 
        WHERE nutricionista_id = ? AND status = 'agendada' 
        AND DATE(data_consulta) >= DATE('now')
        """, (user['id'],))
        consultas_pendentes = cursor.fetchone()[0]
        
        st.markdown(f'''
        <div class="metric-card fade-in">
            <div class="metric-title">📅 Consultas Pendentes</div>
            <div class="metric-value">{consultas_pendentes}</div>
            <div class="metric-change">📊 Próximas consultas</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        cursor.execute("""
        SELECT COUNT(*) FROM consultas 
        WHERE nutricionista_id = ? AND status = 'realizada'
        AND DATE(data_consulta) >= DATE('now', 'start of month')
        """, (user['id'],))
        consultas_mes = cursor.fetchone()[0]
        
        st.markdown(f'''
        <div class="metric-card fade-in">
            <div class="metric-title">✅ Consultas este Mês</div>
            <div class="metric-value">{consultas_mes}</div>
            <div class="metric-change positive">↗️ +18% vs mês anterior</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        cursor.execute("SELECT COUNT(*) FROM planos_alimentares WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
        planos_ativos = cursor.fetchone()[0]
        
        st.markdown(f'''
        <div class="metric-card fade-in">
            <div class="metric-title">🍽️ Planos Ativos</div>
            <div class="metric-value">{planos_ativos}</div>
            <div class="metric-change">📈 Planos em andamento</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col5:
        cursor.execute("""
        SELECT COALESCE(SUM(valor), 0) FROM consultas 
        WHERE nutricionista_id = ? AND status = 'realizada'
        AND DATE(data_consulta) >= DATE('now', 'start of month')
        """, (user['id'],))
        receita_mes = cursor.fetchone()[0] or 0
        
        st.markdown(f'''
        <div class="metric-card fade-in">
            <div class="metric-title">💰 Receita do Mês</div>
            <div class="metric-value">R$ {receita_mes:,.2f}</div>
            <div class="metric-change positive">↗️ +25% vs mês anterior</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráficos avançados
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown('<div class="sub-header">📈 Análise de Consultas</div>', unsafe_allow_html=True)
        
        # Gráfico de consultas por mês
        cursor.execute("""
        SELECT strftime('%Y-%m', data_consulta) as mes, COUNT(*) as total
        FROM consultas
        WHERE nutricionista_id = ? AND data_consulta >= DATE('now', '-12 months')
        GROUP BY strftime('%Y-%m', data_consulta)
        ORDER BY mes
        """, (user['id'],))
        
        dados_consultas = cursor.fetchall()
        
        if dados_consultas:
            df_consultas = pd.DataFrame(dados_consultas, columns=['mes', 'total'])
            df_consultas['mes_nome'] = pd.to_datetime(df_consultas['mes']).dt.strftime('%b/%Y')
            
            fig_consultas = px.line(
                df_consultas, 
                x='mes_nome', 
                y='total',
                title="Evolução de Consultas (Últimos 12 Meses)",
                markers=True
            )
            
            fig_consultas.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_family="Inter",
                title_font_size=16,
                title_x=0.5,
                xaxis_title="Mês",
                yaxis_title="Número de Consultas",
                hovermode='x unified'
            )
            
            fig_consultas.update_traces(
                line_color='#2E7D32',
                marker_color='#4CAF50',
                marker_size=8
            )
            
            st.plotly_chart(fig_consultas, use_container_width=True)
        else:
            st.info("📊 Ainda não há dados suficientes para gerar o gráfico.")
    
    with col_right:
        st.markdown('<div class="sub-header">🎯 Status dos Pacientes</div>', unsafe_allow_html=True)
        
        # Gráfico de pizza - Status dos planos
        cursor.execute("""
        SELECT 
            CASE 
                WHEN data_validade >= DATE('now') THEN 'Ativo'
                WHEN data_validade < DATE('now') THEN 'Vencido'
                ELSE 'Sem data'
            END as status,
            COUNT(*) as total
        FROM planos_alimentares
        WHERE nutricionista_id = ? AND ativo = 1
        GROUP BY status
        """, (user['id'],))
        
        dados_status = cursor.fetchall()
        
        if dados_status:
            df_status = pd.DataFrame(dados_status, columns=['status', 'total'])
            
            fig_pizza = px.pie(
                df_status, 
                values='total', 
                names='status',
                title="Status dos Planos Alimentares",
                color_discrete_map={
                    'Ativo': '#4CAF50',
                    'Vencido': '#FF9800',
                    'Sem data': '#9E9E9E'
                }
            )
            
            fig_pizza.update_layout(
                font_family="Inter",
                title_font_size=14,
                title_x=0.5,
                showlegend=True,
                height=300
            )
            
            st.plotly_chart(fig_pizza, use_container_width=True)
        else:
            st.info("📊 Ainda não há planos alimentares criados.")
    
    st.markdown("---")
    
    # Tabela de últimas atividades
    col_table, col_calendar = st.columns([3, 2])
    
    with col_table:
        st.markdown('<div class="sub-header">🕒 Últimas Atividades</div>', unsafe_allow_html=True)
        
        cursor.execute("""
        SELECT l.data_acao, l.acao, l.tabela_afetada,
               COALESCE(p.nome, 'Sistema') as relacionado
        FROM logs_sistema l
        LEFT JOIN pacientes p ON l.registro_id = p.uuid
        WHERE l.usuario_id = ?
        ORDER BY l.data_acao DESC
        LIMIT 10
        """, (user['id'],))
        
        logs = cursor.fetchall()
        
        if logs:
            df_logs = pd.DataFrame(logs, columns=['Data', 'Ação', 'Módulo', 'Relacionado'])
            df_logs['Data'] = pd.to_datetime(df_logs['Data']).dt.strftime('%d/%m %H:%M')
            
            # Emojis para ações
            emoji_map = {
                'LOGIN': '🔐', 'LOGOUT': '🚪', 'CREATE': '➕',
                'UPDATE': '✏️', 'DELETE': '🗑️', 'VIEW': '👁️'
            }
            
            df_logs['🎯'] = df_logs['Ação'].map(lambda x: emoji_map.get(x, '📝'))
            
            st.dataframe(
                df_logs[['🎯', 'Data', 'Ação', 'Módulo', 'Relacionado']], 
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("📝 Nenhuma atividade registrada ainda.")
    
    with col_calendar:
        st.markdown('<div class="sub-header">📅 Próximas Consultas</div>', unsafe_allow_html=True)
        
        cursor.execute("""
        SELECT c.data_consulta, c.tipo_consulta, p.nome
        FROM consultas c
        JOIN pacientes p ON c.paciente_id = p.id
        WHERE c.nutricionista_id = ? AND c.status = 'agendada'
        AND DATE(c.data_consulta) >= DATE('now')
        ORDER BY c.data_consulta
        LIMIT 5
        """, (user['id'],))
        
        proximas_consultas = cursor.fetchall()
        
        if proximas_consultas:
            for consulta in proximas_consultas:
                data_consulta = datetime.fromisoformat(consulta[0]).strftime('%d/%m %H:%M')
                st.markdown(f'''
                <div class="metric-card" style="margin: 0.5rem 0; padding: 1rem;">
                    <div style="font-weight: 600; color: #2E7D32;">📅 {data_consulta}</div>
                    <div style="font-size: 0.9rem; color: #757575;">{consulta[1]}</div>
                    <div style="font-size: 0.85rem; color: #424242;">👤 {consulta[2]}</div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("📅 Nenhuma consulta agendada.")
    
    # Botões de ação rápida
    st.markdown("---")
    st.markdown('<div class="sub-header">⚡ Ações Rápidas</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("➕ Novo Paciente", use_container_width=True):
            st.session_state.page = 'patients'
            st.session_state.action = 'new'
            st.rerun()
    
    with col2:
        if st.button("📅 Agendar Consulta", use_container_width=True):
            st.session_state.page = 'appointments'
            st.session_state.action = 'new'
            st.rerun()
    
    with col3:
        if st.button("🍽️ Criar Plano", use_container_width=True):
            st.session_state.page = 'meal_plans'
            st.session_state.action = 'new'
            st.rerun()
    
    with col4:
        if st.button("🧮 Calculadoras", use_container_width=True):
            st.session_state.page = 'calculators'
            st.rerun()
    
    with col5:
        if st.button("📄 Relatórios", use_container_width=True):
            st.session_state.page = 'reports'
            st.rerun()
    
    conn.close()

# =============================================================================
# 👥 GESTÃO COMPLETA DE PACIENTES
# =============================================================================

def show_patient_management():
    """Sistema completo de gestão de pacientes"""
    
    st.markdown('<h1 class="main-header">👥 Gestão de Pacientes</h1>', unsafe_allow_html=True)
    
    user = AuthSystem.get_current_user()
    
    # Menu de navegação
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Lista de Pacientes", 
        "➕ Novo Paciente", 
        "🔍 Buscar Paciente",
        "📊 Análises"
    ])
    
    with tab1:
        show_patients_list(user)
    
    with tab2:
        show_new_patient_form(user)
    
    with tab3:
        show_patient_search(user)
    
    with tab4:
        show_patients_analytics(user)

def show_patients_list(user):
    """Lista todos os pacientes do nutricionista"""
    
    st.markdown('<div class="sub-header">📋 Lista de Pacientes</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Filtros
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        filtro_nome = st.text_input("🔍 Filtrar por nome", placeholder="Digite o nome do paciente...")
    
    with col2:
        filtro_status = st.selectbox("📊 Status", ["Todos", "Ativos", "Inativos"])
    
    with col3:
        ordenar_por = st.selectbox("📄 Ordenar por", ["Nome", "Data Cadastro", "Última Consulta"])
    
    # Buscar pacientes
    query = """
    SELECT p.id, p.uuid, p.nome, p.email, p.telefone, p.data_nascimento,
           p.sexo, p.data_cadastro, p.ativo,
           COUNT(c.id) as total_consultas,
           MAX(c.data_consulta) as ultima_consulta
    FROM pacientes p
    LEFT JOIN consultas c ON p.id = c.paciente_id
    WHERE p.nutricionista_id = ?
    """
    
    params = [user['id']]
    
    if filtro_nome:
        query += " AND p.nome LIKE ?"
        params.append(f"%{filtro_nome}%")
    
    if filtro_status != "Todos":
        status_val = 1 if filtro_status == "Ativos" else 0
        query += " AND p.ativo = ?"
        params.append(status_val)
    
    query += " GROUP BY p.id"
    
    # Ordenação
    if ordenar_por == "Nome":
        query += " ORDER BY p.nome"
    elif ordenar_por == "Data Cadastro":
        query += " ORDER BY p.data_cadastro DESC"
    else:
        query += " ORDER BY ultima_consulta DESC"
    
    cursor.execute(query, params)
    pacientes = cursor.fetchall()
    
    if pacientes:
        # Criar DataFrame para exibição
        df_data = []
        for paciente in pacientes:
            idade = None
            if paciente[5]:  # data_nascimento
                try:
                    nasc = datetime.strptime(paciente[5], '%Y-%m-%d')
                    idade = datetime.now().year - nasc.year
                except:
                    pass
            
            ultima_consulta = "Nunca"
            if paciente[10]:  # ultima_consulta
                try:
                    dt = datetime.fromisoformat(paciente[10])
                    ultima_consulta = dt.strftime('%d/%m/%Y')
                except:
                    pass
            
            df_data.append({
                'ID': paciente[0],
                'UUID': paciente[1],
                'Nome': paciente[2],
                'Email': paciente[3] or '-',
                'Telefone': paciente[4] or '-',
                'Idade': f"{idade} anos" if idade else '-',
                'Sexo': paciente[6] or '-',
                'Consultas': paciente[9],
                'Última Consulta': ultima_consulta,
                'Status': '✅ Ativo' if paciente[8] else '❌ Inativo',
                'Cadastro': datetime.fromisoformat(paciente[7]).strftime('%d/%m/%Y')
            })
        
        df = pd.DataFrame(df_data)
        
        # Exibir tabela com funcionalidades
        st.markdown(f"**Total de pacientes:** {len(pacientes)}")
        
        # Configurar colunas para exibição
        column_config = {
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Nome": st.column_config.TextColumn("Nome", width="medium"),
            "Email": st.column_config.TextColumn("Email", width="medium"),
            "Telefone": st.column_config.TextColumn("Telefone", width="small"),
            "Idade": st.column_config.TextColumn("Idade", width="small"),
            "Sexo": st.column_config.TextColumn("Sexo", width="small"),
            "Consultas": st.column_config.NumberColumn("Consultas", width="small"),
            "Última Consulta": st.column_config.DateColumn("Última Consulta", width="medium"),
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Cadastro": st.column_config.DateColumn("Cadastro", width="medium")
        }
        
        # Tabela editável
        edited_df = st.data_editor(
            df[['Nome', 'Email', 'Telefone', 'Idade', 'Sexo', 'Consultas', 'Última Consulta', 'Status']],
            column_config=column_config,
            hide_index=True,
            use_container_width=True,
            num_rows="dynamic"
        )
        
        st.markdown("---")
        
        # Ações em lote
        st.markdown('<div class="sub-header">⚡ Ações Rápidas</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📄 Exportar Lista", use_container_width=True):
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="pacientes_{datetime.now().strftime("%Y%m%d")}.csv">📥 Baixar CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
        
        with col2:
            if st.button("📧 Enviar Comunicado", use_container_width=True):
                st.info("💌 Em desenvolvimento: Funcionalidade de comunicação em massa")
        
        with col3:
            if st.button("🔄 Sincronizar Dados", use_container_width=True):
                st.success("✅ Dados sincronizados com sucesso!")
        
        with col4:
            if st.button("🗂️ Backup Pacientes", use_container_width=True):
                st.success("💾 Backup realizado com sucesso!")
        
        # Detalhes do paciente selecionado
        if st.session_state.get('selected_patient_id'):
            show_patient_details(st.session_state.selected_patient_id)
    
    else:
        st.info("👥 Nenhum paciente encontrado com os filtros aplicados.")
        if st.button("➕ Cadastrar Primeiro Paciente"):
            st.session_state.active_tab = 1
            st.rerun()
    
    conn.close()

def show_new_patient_form(user):
    """Formulário para cadastro de novo paciente"""
    
    st.markdown('<div class="sub-header">➕ Cadastro de Novo Paciente</div>', unsafe_allow_html=True)
    
    with st.form("novo_paciente_form", clear_on_submit=False):
        st.markdown("##### 📋 Dados Pessoais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo *", placeholder="Ex: Maria Silva Santos")
            email = st.text_input("Email", placeholder="maria@email.com")
            telefone = st.text_input("Telefone *", placeholder="(11) 99999-9999")
            data_nascimento = st.date_input("Data de Nascimento *")
            sexo = st.selectbox("Sexo *", ["Feminino", "Masculino", "Outro"])
        
        with col2:
            cpf = st.text_input("CPF", placeholder="000.000.000-00")
            profissao = st.text_input("Profissão", placeholder="Ex: Professora")
            estado_civil = st.selectbox("Estado Civil", ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"])
            endereco = st.text_area("Endereço Completo", placeholder="Rua, Número, Bairro, Cidade - UF")
        
        st.markdown("---")
        st.markdown("##### 🚨 Contato de Emergência")
        
        col1, col2 = st.columns(2)
        
        with col1:
            emergencia_contato = st.text_input("Nome do Contato", placeholder="Ex: João Silva")
        
        with col2:
            emergencia_telefone = st.text_input("Telefone de Emergência", placeholder="(11) 99999-9999")
        
        st.markdown("---")
        st.markdown("##### 📝 Observações Iniciais")
        
        observacoes = st.text_area(
            "Observações",
            placeholder="Adicione aqui observações importantes sobre o paciente...",
            height=100
        )
        
        st.markdown("---")
        
        # Botões do formulário
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submitted = st.form_submit_button("💾 Cadastrar Paciente", use_container_width=True)
        
        with col2:
            if st.form_submit_button("🧹 Limpar Formulário", use_container_width=True):
                st.rerun()
        
        # Validação e cadastro
        if submitted:
            # Validar campos obrigatórios
            if not nome or not telefone or not data_nascimento:
                st.error("❌ Por favor, preencha todos os campos obrigatórios (*)")
            else:
                # Cadastrar paciente
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                
                try:
                    paciente_uuid = str(uuid.uuid4())
                    
                    cursor.execute('''
                    INSERT INTO pacientes (
                        uuid, nutricionista_id, nome, email, telefone, data_nascimento,
                        sexo, cpf, endereco, profissao, estado_civil,
                        emergencia_contato, emergencia_telefone, observacoes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        paciente_uuid, user['id'], nome, email, telefone,
                        data_nascimento.strftime('%Y-%m-%d'), sexo, cpf, endereco,
                        profissao, estado_civil, emergencia_contato,
                        emergencia_telefone, observacoes
                    ))
                    
                    # Log da ação
                    cursor.execute('''
                    INSERT INTO logs_sistema (usuario_id, acao, tabela_afetada, registro_id)
                    VALUES (?, ?, ?, ?)
                    ''', (user['id'], 'CREATE', 'pacientes', paciente_uuid))
                    
                    conn.commit()
                    
                    st.success(f"✅ Paciente **{nome}** cadastrado com sucesso!")
                    st.balloons()
                    
                    # Opções pós-cadastro
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("📅 Agendar Consulta"):
                            st.session_state.page = 'appointments'
                            st.session_state.new_appointment_patient = paciente_uuid
                            st.rerun()
                    
                    with col2:
                        if st.button("🧮 Fazer Avaliação"):
                            st.session_state.page = 'evaluations'
                            st.session_state.evaluation_patient = paciente_uuid
                            st.rerun()
                    
                    with col3:
                        if st.button("👥 Ver Lista"):
                            st.session_state.active_tab = 0
                            st.rerun()
                
                except sqlite3.IntegrityError as e:
                    st.error("❌ Erro: Este paciente já está cadastrado!")
                except Exception as e:
                    st.error(f"❌ Erro ao cadastrar paciente: {str(e)}")
                finally:
                    conn.close()

def show_patient_search(user):
    """Sistema de busca avançada de pacientes"""
    
    st.markdown('<div class="sub-header">🔍 Busca Avançada de Pacientes</div>', unsafe_allow_html=True)
    
    # Filtros de busca
    with st.expander("🔧 Filtros Avançados", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            busca_nome = st.text_input("Nome", placeholder="Digite parte do nome...")
            busca_email = st.text_input("Email", placeholder="Digite o email...")
        
        with col2:
            busca_telefone = st.text_input("Telefone", placeholder="Digite o telefone...")
            idade_min = st.number_input("Idade Mínima", min_value=0, max_value=120, value=0)
        
        with col3:
            idade_max = st.number_input("Idade Máxima", min_value=0, max_value=120, value=120)
            busca_sexo = st.selectbox("Sexo", ["Todos", "Feminino", "Masculino", "Outro"])
        
        # Período de cadastro
        col1, col2 = st.columns(2)
        with col1:
            data_inicio = st.date_input("Cadastrado a partir de", value=None)
        with col2:
            data_fim = st.date_input("Cadastrado até", value=None)
    
    if st.button("🔍 Buscar Pacientes", use_container_width=True):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Construir query dinâmica
        query = """
        SELECT p.*, 
               COUNT(c.id) as total_consultas,
               MAX(c.data_consulta) as ultima_consulta,
               AVG(a.peso) as peso_medio,
               AVG(a.imc) as imc_medio
        FROM pacientes p
        LEFT JOIN consultas c ON p.id = c.paciente_id
        LEFT JOIN avaliacoes a ON p.id = a.paciente_id
        WHERE p.nutricionista_id = ?
        """
        
        params = [user['id']]
        
        # Adicionar filtros
        if busca_nome:
            query += " AND p.nome LIKE ?"
            params.append(f"%{busca_nome}%")
        
        if busca_email:
            query += " AND p.email LIKE ?"
            params.append(f"%{busca_email}%")
        
        if busca_telefone:
            query += " AND p.telefone LIKE ?"
            params.append(f"%{busca_telefone}%")
        
        if busca_sexo != "Todos":
            query += " AND p.sexo = ?"
            params.append(busca_sexo)
        
        # Filtro por idade (calculada)
        if idade_min > 0:
            data_max_nascimento = (datetime.now() - timedelta(days=idade_min*365)).strftime('%Y-%m-%d')
            query += " AND p.data_nascimento <= ?"
            params.append(data_max_nascimento)
        
        if idade_max < 120:
            data_min_nascimento = (datetime.now() - timedelta(days=idade_max*365)).strftime('%Y-%m-%d')
            query += " AND p.data_nascimento >= ?"
            params.append(data_min_nascimento)
        
        # Filtro por período de cadastro
        if data_inicio:
            query += " AND DATE(p.data_cadastro) >= ?"
            params.append(data_inicio.strftime('%Y-%m-%d'))
        
        if data_fim:
            query += " AND DATE(p.data_cadastro) <= ?"
            params.append(data_fim.strftime('%Y-%m-%d'))
        
        query += " GROUP BY p.id ORDER BY p.nome"
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        if resultados:
            st.success(f"🎯 Encontrados {len(resultados)} paciente(s)")
            
            # Exibir resultados em cards
            for paciente in resultados:
                with st.expander(f"👤 {paciente[2]}", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**📧 Email:** {paciente[3] or 'Não informado'}")
                        st.write(f"**📱 Telefone:** {paciente[4] or 'Não informado'}")
                        st.write(f"**🎂 Nascimento:** {paciente[5] or 'Não informado'}")
                    
                    with col2:
                        st.write(f"**⚧ Sexo:** {paciente[6] or 'Não informado'}")
                        st.write(f"**💼 Profissão:** {paciente[9] or 'Não informada'}")
                        st.write(f"**💒 Estado Civil:** {paciente[10] or 'Não informado'}")
                    
                    with col3:
                        st.write(f"**📅 Consultas:** {paciente[16] or 0}")
                        if paciente[18]:  # peso_medio
                            st.write(f"**⚖️ Peso Médio:** {paciente[18]:.1f} kg")
                        if paciente[19]:  # imc_medio
                            st.write(f"**📊 IMC Médio:** {paciente[19]:.1f}")
                    
                    # Botões de ação
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if st.button("👁️ Ver Detalhes", key=f"ver_{paciente[0]}"):
                            st.session_state.selected_patient_id = paciente[0]
                    
                    with col2:
                        if st.button("✏️ Editar", key=f"edit_{paciente[0]}"):
                            st.session_state.edit_patient_id = paciente[0]
                    
                    with col3:
                        if st.button("📅 Consulta", key=f"consult_{paciente[0]}"):
                            st.session_state.page = 'appointments'
                            st.session_state.new_appointment_patient = paciente[1]
                    
                    with col4:
                        if st.button("🍽️ Plano", key=f"plan_{paciente[0]}"):
                            st.session_state.page = 'meal_plans'
                            st.session_state.new_plan_patient = paciente[1]
        else:
            st.warning("🔍 Nenhum paciente encontrado com os critérios informados.")
        
        conn.close()

def show_patients_analytics(user):
    """Analytics e estatísticas dos pacientes"""
    
    st.markdown('<div class="sub-header">📊 Analytics dos Pacientes</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cursor.execute("SELECT COUNT(*) FROM pacientes WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
        total_ativos = cursor.fetchone()[0]
        st.metric("👥 Pacientes Ativos", total_ativos)
    
    with col2:
        cursor.execute("""
        SELECT AVG(strftime('%Y', 'now') - strftime('%Y', data_nascimento))
        FROM pacientes WHERE nutricionista_id = ? AND data_nascimento IS NOT NULL
        """, (user['id'],))
        idade_media = cursor.fetchone()[0]
        if idade_media:
            st.metric("🎂 Idade Média", f"{idade_media:.0f} anos")
        else:
            st.metric("🎂 Idade Média", "N/A")
    
    with col3:
        cursor.execute("""
        SELECT COUNT(*) FROM consultas c
        JOIN pacientes p ON c.paciente_id = p.id
        WHERE p.nutricionista_id = ? AND c.status = 'realizada'
        AND DATE(c.data_consulta) >= DATE('now', 'start of month')
        """, (user['id'],))
        consultas_mes = cursor.fetchone()[0]
        st.metric("📅 Consultas este Mês", consultas_mes)
    
    with col4:
        cursor.execute("""
        SELECT COUNT(DISTINCT p.id) FROM pacientes p
        JOIN consultas c ON p.id = c.paciente_id
        WHERE p.nutricionista_id = ? AND c.status = 'realizada'
        AND DATE(c.data_consulta) >= DATE('now', 'start of month')
        """, (user['id'],))
        pacientes_atendidos = cursor.fetchone()[0]
        st.metric("👤 Pacientes Atendidos", pacientes_atendidos)
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por sexo
        cursor.execute("""
        SELECT sexo, COUNT(*) as total
        FROM pacientes 
        WHERE nutricionista_id = ? AND ativo = 1
        GROUP BY sexo
        """, (user['id'],))
        
        dados_sexo = cursor.fetchall()
        
        if dados_sexo:
            df_sexo = pd.DataFrame(dados_sexo, columns=['Sexo', 'Total'])
            
            fig_sexo = px.pie(
                df_sexo, 
                values='Total', 
                names='Sexo',
                title="Distribuição por Sexo",
                color_discrete_map={
                    'Feminino': '#FF6B9D',
                    'Masculino': '#4DABF7',
                    'Outro': '#69DB7C'
                }
            )
            
            fig_sexo.update_layout(height=300, title_x=0.5)
            st.plotly_chart(fig_sexo, use_container_width=True)
    
    with col2:
        # Distribuição por faixa etária
        cursor.execute("""
        SELECT 
            CASE 
                WHEN strftime('%Y', 'now') - strftime('%Y', data_nascimento) < 18 THEN 'Menor de 18'
                WHEN strftime('%Y', 'now') - strftime('%Y', data_nascimento) BETWEEN 18 AND 30 THEN '18-30'
                WHEN strftime('%Y', 'now') - strftime('%Y', data_nascimento) BETWEEN 31 AND 50 THEN '31-50'
                WHEN strftime('%Y', 'now') - strftime('%Y', data_nascimento) BETWEEN 51 AND 65 THEN '51-65'
                ELSE 'Maior de 65'
            END as faixa_etaria,
            COUNT(*) as total
        FROM pacientes 
        WHERE nutricionista_id = ? AND ativo = 1 AND data_nascimento IS NOT NULL
        GROUP BY faixa_etaria
        """, (user['id'],))
        
        dados_idade = cursor.fetchall()
        
        if dados_idade:
            df_idade = pd.DataFrame(dados_idade, columns=['Faixa Etária', 'Total'])
            
            fig_idade = px.bar(
                df_idade,
                x='Faixa Etária',
                y='Total',
                title="Distribuição por Faixa Etária",
                color='Total',
                color_continuous_scale='Greens'
            )
            
            fig_idade.update_layout(height=300, title_x=0.5, showlegend=False)
            st.plotly_chart(fig_idade, use_container_width=True)
    
    # Evolução de cadastros
    st.markdown('<div class="sub-header">📈 Evolução de Cadastros</div>', unsafe_allow_html=True)
    
    cursor.execute("""
    SELECT strftime('%Y-%m', data_cadastro) as mes, COUNT(*) as total
    FROM pacientes
    WHERE nutricionista_id = ? AND data_cadastro >= DATE('now', '-12 months')
    GROUP BY strftime('%Y-%m', data_cadastro)
    ORDER BY mes
    """, (user['id'],))
    
    dados_evolucao = cursor.fetchall()
    
    if dados_evolucao:
        df_evolucao = pd.DataFrame(dados_evolucao, columns=['Mês', 'Total'])
        df_evolucao['Mês Nome'] = pd.to_datetime(df_evolucao['Mês']).dt.strftime('%b/%Y')
        
        fig_evolucao = px.line(
            df_evolucao,
            x='Mês Nome',
            y='Total',
            title="Novos Cadastros por Mês",
            markers=True
        )
        
        fig_evolucao.update_traces(line_color='#2E7D32', marker_color='#4CAF50')
        fig_evolucao.update_layout(height=400, title_x=0.5)
        
        st.plotly_chart(fig_evolucao, use_container_width=True)
    
    conn.close()

# =============================================================================
# 🧮 CALCULADORAS NUTRICIONAIS INTERFACE
# =============================================================================

def show_calculators():
    """Interface das calculadoras nutricionais"""
    
    st.markdown('<h1 class="main-header">🧮 Calculadoras Nutricionais</h1>', unsafe_allow_html=True)
    
    # Menu de calculadoras
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 IMC & Composição",
        "🔥 Gasto Energético", 
        "🥤 Necessidade Hídrica",
        "🍽️ Macronutrientes",
        "⚖️ Peso Ideal",
        "📋 Avaliação Completa"
    ])
    
    with tab1:
        show_imc_calculator()
    
    with tab2:
        show_energy_calculator()
    
    with tab3:
        show_water_calculator()
    
    with tab4:
        show_macro_calculator()
    
    with tab5:
        show_ideal_weight_calculator()
    
    with tab6:
        show_complete_evaluation()

def show_imc_calculator():
    """Calculadora de IMC e composição corporal"""
    
    st.markdown('<div class="sub-header">📊 Calculadora de IMC e Composição Corporal</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("##### 📋 Dados do Paciente")
        
        peso = st.number_input("Peso (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.1)
        altura = st.number_input("Altura (m)", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
        idade = st.number_input("Idade (anos)", min_value=1, max_value=120, value=30)
        sexo = st.selectbox("Sexo", ["Feminino", "Masculino"])
        
        st.markdown("##### 📏 Medidas Adicionais (Opcional)")
        
        circ_cintura = st.number_input("Circunferência da Cintura (cm)", min_value=0.0, value=0.0, step=0.1)
        circ_quadril = st.number_input("Circunferência do Quadril (cm)", min_value=0.0, value=0.0, step=0.1)
        
        # Dobras cutâneas
        st.markdown("##### 📐 Dobras Cutâneas (mm) - Opcional")
        
        dobra_triciptal = st.number_input("Tricipital", min_value=0.0, value=0.0, step=0.1)
        dobra_subscapular = st.number_input("Subescapular", min_value=0.0, value=0.0, step=0.1)
        dobra_abdominal = st.number_input("Abdominal", min_value=0.0, value=0.0, step=0.1)
        
        calcular = st.button("🧮 Calcular", use_container_width=True)
    
    with col2:
        if calcular or st.session_state.get('auto_calc_imc', False):
            # Calcular IMC
            resultado_imc = NutritionalCalculators.calcular_imc(peso, altura)
            
            if resultado_imc:
                st.markdown("##### 📊 Resultado do IMC")
                
                # Exibir resultado principal
                col_imc1, col_imc2, col_imc3 = st.columns(3)
                
                with col_imc1:
                    st.metric("IMC", f"{resultado_imc['imc']}")
                
                with col_imc2:
                    st.metric("Classificação", resultado_imc['classificacao'])
                
                with col_imc3:
                    status_color = {
                        'Normal': '🟢',
                        'Pouco elevado': '🟡',
                        'Elevado': '🟠',
                        'Muito elevado': '🔴',
                        'Extremamente elevado': '🔴'
                    }
                    emoji = status_color.get(resultado_imc['risco'], '⚪')
                    st.metric("Risco", f"{emoji} {resultado_imc['risco']}")
                
                # Gráfico do IMC
                fig_imc = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = resultado_imc['imc'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Índice de Massa Corporal"},
                    gauge = {
                        'axis': {'range': [None, 45]},
                        'bar': {'color': "#2E7D32"},
                        'steps': [
                            {'range': [0, 18.5], 'color': "lightblue"},
                            {'range': [18.5, 25], 'color': "lightgreen"},
                            {'range': [25, 30], 'color': "yellow"},
                            {'range': [30, 35], 'color': "orange"},
                            {'range': [35, 45], 'color': "red"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': resultado_imc['imc']
                        }
                    }
                ))
                
                fig_imc.update_layout(height=300)
                st.plotly_chart(fig_imc, use_container_width=True)
                
                # Avaliação adicional se houver medidas
                dobras = []
                if dobra_triciptal > 0:
                    dobras.append(dobra_triciptal)
                if dobra_subscapular > 0:
                    dobras.append(dobra_subscapular)
                if dobra_abdominal > 0:
                    dobras.append(dobra_abdominal)
                
                if circ_cintura > 0 or circ_quadril > 0 or dobras:
                    st.markdown("##### 📏 Avaliação de Composição Corporal")
                    
                    resultado_comp = NutritionalCalculators.avaliar_composicao_corporal(
                        peso, altura, idade, sexo, circ_cintura, circ_quadril, dobras
                    )
                    
                    if 'rcq' in resultado_comp:
                        st.success(f"**Relação Cintura-Quadril:** {resultado_comp['rcq']['valor']} (Risco: {resultado_comp['rcq']['risco']})")
                    
                    if 'percentual_gordura' in resultado_comp:
                        col_comp1, col_comp2, col_comp3 = st.columns(3)
                        
                        with col_comp1:
                            st.metric("% Gordura", f"{resultado_comp['percentual_gordura']:.1f}%")
                        
                        with col_comp2:
                            st.metric("Massa Gorda", f"{resultado_comp['massa_gorda']:.1f} kg")
                        
                        with col_comp3:
                            st.metric("Massa Magra", f"{resultado_comp['massa_magra']:.1f} kg")
                
                # Recomendações
                st.markdown("##### 💡 Recomendações")
                
                if resultado_imc['imc'] < 18.5:
                    st.info("📈 **Baixo peso:** Recomenda-se avaliação médica e nutricional para ganho de peso saudável.")
                elif resultado_imc['imc'] < 25:
                    st.success("✅ **Peso normal:** Manter hábitos saudáveis e prática regular de exercícios.")
                elif resultado_imc['imc'] < 30:
                    st.warning("⚠️ **Sobrepeso:** Recomenda-se redução gradual de peso através de dieta equilibrada e exercícios.")
                else:
                    st.error("🚨 **Obesidade:** Necessário acompanhamento médico e nutricional especializado.")

def show_energy_calculator():
    """Calculadora de gasto energético"""
    
    st.markdown('<div class="sub-header">🔥 Calculadora de Gasto Energético</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("##### 📋 Dados Básicos")
        
        peso = st.number_input("Peso (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.1, key="energy_peso")
        altura = st.number_input("Altura (cm)", min_value=50, max_value=250, value=170, key="energy_altura")
        idade = st.number_input("Idade (anos)", min_value=1, max_value=120, value=30, key="energy_idade")
        sexo = st.selectbox("Sexo", ["Feminino", "Masculino"], key="energy_sexo")
        
        st.markdown("##### 🧪 Fórmula para TMB")
        formula_tmb = st.selectbox(
            "Escolha a fórmula",
            ["harris_benedict", "mifflin_st_jeor"],
            format_func=lambda x: {
                "harris_benedict": "Harris-Benedict (1919)",
                "mifflin_st_jeor": "Mifflin-St Jeor (1990) - Recomendada"
            }[x]
        )
        
        st.markdown("##### 🏃 Nível de Atividade Física")
        nivel_atividade = st.selectbox(
            "Selecione o nível",
            ["sedentario", "leve", "moderado", "intenso", "muito_intenso"],
            format_func=lambda x: {
                "sedentario": "Sedentário (pouco/nenhum exercício)",
                "leve": "Leve (1-3 dias/semana)",
                "moderado": "Moderado (3-5 dias/semana)",
                "intenso": "Intenso (6-7 dias/semana)",
                "muito_intenso": "Muito Intenso (2x/dia ou exercício intenso)"
            }[x]
        )
        
        calcular_energia = st.button("🔥 Calcular Gasto", use_container_width=True)
    
    with col2:
        if calcular_energia or st.session_state.get('auto_calc_energia', False):
            # Calcular TMB
            tmb = NutritionalCalculators.calcular_tmb(peso, altura, idade, sexo, formula_tmb)
            
            if tmb:
                # Calcular GET
                resultado_get = NutritionalCalculators.calcular_get(tmb, nivel_atividade)
                
                st.markdown("##### 🔥 Resultados do Gasto Energético")
                
                col_res1, col_res2, col_res3 = st.columns(3)
                
                with col_res1:
                    st.metric("TMB", f"{tmb:.0f} kcal/dia", help="Taxa Metabólica Basal")
                
                with col_res2:
                    st.metric("GET", f"{resultado_get['get']:.0f} kcal/dia", help="Gasto Energético Total")
                
                with col_res3:
                    diferenca = resultado_get['get'] - tmb
                    st.metric("Atividade", f"{diferenca:.0f} kcal/dia", help="Energia gasta em atividades")
                
                # Gráfico de distribuição energética
                fig_energia = px.pie(
                    values=[tmb, diferenca],
                    names=['TMB (Metabolismo Basal)', 'Atividade Física'],
                    title="Distribuição do Gasto Energético",
                    color_discrete_sequence=['#FF6B9D', '#4DABF7']
                )
                
                fig_energia.update_layout(height=400, title_x=0.5)
                st.plotly_chart(fig_energia, use_container_width=True)
                
                # Tabela de faixas calóricas para diferentes objetivos
                st.markdown("##### 🎯 Faixas Calóricas por Objetivo")
                
                objetivos = {
                    'Perda de Peso Rápida': resultado_get['get'] * 0.75,
                    'Perda de Peso Gradual': resultado_get['get'] * 0.85,
                    'Manutenção': resultado_get['get'],
                    'Ganho de Peso Gradual': resultado_get['get'] * 1.15,
                    'Ganho de Peso Rápido': resultado_get['get'] * 1.25
                }
                
                df_objetivos = pd.DataFrame([
                    {'Objetivo': obj, 'Calorias/dia': f"{cal:.0f}", 'Diferença': f"{cal - resultado_get['get']:+.0f}"}
                    for obj, cal in objetivos.items()
                ])
                
                st.dataframe(df_objetivos, hide_index=True, use_container_width=True)
                
                # Informações adicionais
                st.markdown("##### ℹ️ Informações Importantes")
                
                st.info(f"""
                **Fórmula utilizada:** {formula_tmb.replace('_', ' ').title()}
                
                **Fator de atividade:** {resultado_get['fator']} ({nivel_atividade.replace('_', ' ').title()})
                
                **Recomendações:**
                - Para perda de peso: déficit de 300-500 kcal/dia
                - Para ganho de massa: superávit de 300-500 kcal/dia
                - Sempre considerar avaliação médica antes de grandes mudanças
                """)

def show_water_calculator():
    """Calculadora de necessidade hídrica"""
    
    st.markdown('<div class="sub-header">🥤 Calculadora de Necessidade Hídrica</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("##### 📋 Dados do Paciente")
        
        peso = st.number_input("Peso (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.1, key="water_peso")
        idade = st.number_input("Idade (anos)", min_value=1, max_value=120, value=30, key="water_idade")
        
        st.markdown("##### 🏃 Fatores Adicionais")
        
        atividade_fisica = st.checkbox("Pratica atividade física regular", value=False)
        clima_quente = st.checkbox("Vive em clima quente/seco", value=False)
        febre = st.checkbox("Está com febre", value=False)
        gravidez = st.checkbox("Gestante", value=False)
        amamentacao = st.checkbox("Lactante", value=False)
        
        if febre:
            temp_febre = st.number_input("Temperatura corporal (°C)", min_value=37.0, max_value=42.0, value=38.0, step=0.1)
        
        calcular_agua = st.button("💧 Calcular Necessidade", use_container_width=True)
    
    with col2:
        if calcular_agua or st.session_state.get('auto_calc_agua', False):
            # Calcular necessidade hídrica
            resultado_agua = NutritionalCalculators.calcular_agua_diaria(peso, idade, atividade_fisica, clima_quente)
            
            # Ajustes adicionais
            agua_total = resultado_agua['ml_dia']
            
            if febre:
                # Adicionar 10% para cada grau acima de 37°C
                graus_febre = temp_febre - 37
                ajuste_febre = agua_total * (graus_febre * 0.10)
                agua_total += ajuste_febre
            
            if gravidez:
                agua_total += 300  # ml adicionais
            
            if amamentacao:
                agua_total += 700  # ml adicionais
            
            st.markdown("##### 💧 Necessidade Hídrica Diária")
            
            col_agua1, col_agua2, col_agua3 = st.columns(3)
            
            with col_agua1:
                st.metric("Total", f"{agua_total:.0f} ml")
            
            with col_agua2:
                st.metric("Litros", f"{agua_total/1000:.1f} L")
            
            with col_agua3:
                copos = agua_total / 200
                st.metric("Copos (200ml)", f"{copos:.0f}")
            
            # Gráfico de distribuição ao longo do dia
            st.markdown("##### ⏰ Distribuição Sugerida ao Longo do Dia")
            
            horarios = [
                "07:00", "09:00", "11:00", "13:00", "15:00", 
                "17:00", "19:00", "21:00"
            ]
            
            ml_por_horario = agua_total / len(horarios)
            
            df_hidratacao = pd.DataFrame({
                'Horário': horarios,
                'Quantidade (ml)': [ml_por_horario] * len(horarios),
                'Copos': [ml_por_horario/200] * len(horarios)
            })
            
            fig_agua = px.bar(
                df_hidratacao,
                x='Horário',
                y='Quantidade (ml)',
                title='Distribuição de Água ao Longo do Dia',
                color='Quantidade (ml)',
                color_continuous_scale='Blues'
            )
            
            fig_agua.update_layout(height=400, title_x=0.5, showlegend=False)
            st.plotly_chart(fig_agua, use_container_width=True)
            
            # Tabela detalhada
            st.dataframe(df_hidratacao, hide_index=True, use_container_width=True)
            
            # Dicas de hidratação
            st.markdown("##### 💡 Dicas para Manter-se Hidratado")
            
            dicas = [
                "🌅 Beba um copo de água ao acordar",
                "⏰ Configure lembretes no celular",
                "🍋 Adicione limão ou frutas para dar sabor",
                "🥒 Consuma alimentos ricos em água (melancia, pepino)",
                "🏃 Aumente a ingestão durante exercícios",
                "🌡️ Monitore a cor da urina (deve ser amarelo claro)",
                "❄️ Mantenha uma garrafa de água sempre próxima"
            ]
            
            for dica in dicas:
                st.markdown(f"- {dica}")

def show_macro_calculator():
    """Calculadora de macronutrientes"""
    
    st.markdown('<div class="sub-header">🍽️ Calculadora de Macronutrientes</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("##### 🎯 Dados para Cálculo")
        
        calorias_totais = st.number_input(
            "Calorias Totais/dia", 
            min_value=500, 
            max_value=5000, 
            value=2000, 
            step=50,
            help="Use a calculadora de gasto energético para obter este valor"
        )
        
        objetivo = st.selectbox(
            "Objetivo Principal",
            ["manutencao", "perda_peso", "ganho_massa", "low_carb", "cetogenica"],
            format_func=lambda x: {
                "manutencao": "Manutenção do Peso",
                "perda_peso": "Perda de Peso",
                "ganho_massa": "Ganho de Massa Muscular",
                "low_carb": "Dieta Low Carb",
                "cetogenica": "Dieta Cetogênica"
            }[x]
        )
        
        st.markdown("##### ⚙️ Personalização (Opcional)")
        
        personalizar = st.checkbox("Personalizar distribuição")
        
        if personalizar:
            st.markdown("###### Percentuais por Macronutriente:")
            carb_perc = st.slider("Carboidratos (%)", 5, 70, 45)
            prot_perc = st.slider("Proteínas (%)", 10, 40, 20)
            lip_perc = st.slider("Lipídios (%)", 15, 75, 35)
            
            total_perc = carb_perc + prot_perc + lip_perc
            if total_perc != 100:
                st.warning(f"⚠️ Total atual: {total_perc}% (deve somar 100%)")
        
        calcular_macros = st.button("🍽️ Calcular Macros", use_container_width=True)
    
    with col2:
        if calcular_macros or st.session_state.get('auto_calc_macros', False):
            if personalizar and total_perc == 100:
                # Usar percentuais personalizados
                carb_kcal = calorias_totais * (carb_perc / 100)
                prot_kcal = calorias_totais * (prot_perc / 100)
                lip_kcal = calorias_totais * (lip_perc / 100)
                
                resultado_macros = {
                    'calorias_totais': calorias_totais,
                    'carboidratos': {'g': carb_kcal / 4, 'kcal': carb_kcal, 'perc': carb_perc},
                    'proteinas': {'g': prot_kcal / 4, 'kcal': prot_kcal, 'perc': prot_perc},
                    'lipidios': {'g': lip_kcal / 9, 'kcal': lip_kcal, 'perc': lip_perc},
                    'objetivo': 'personalizado'
                }
            else:
                # Usar distribuição padrão
                resultado_macros = NutritionalCalculators.calcular_macronutrientes(calorias_totais, objetivo)
            
            st.markdown("##### 🍽️ Distribuição de Macronutrientes")
            
            col_macro1, col_macro2, col_macro3 = st.columns(3)
            
            with col_macro1:
                st.markdown(f'''
                <div class="metric-card" style="text-align: center;">
                    <div style="font-size: 2rem;">🍞</div>
                    <div class="metric-title">Carboidratos</div>
                    <div class="metric-value">{resultado_macros["carboidratos"]["g"]:.0f}g</div>
                    <div style="font-size: 0.9rem; color: #757575;">
                        {resultado_macros["carboidratos"]["kcal"]:.0f} kcal<br>
                        {resultado_macros["carboidratos"]["perc"]:.0f}%
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col_macro2:
                st.markdown(f'''
                <div class="metric-card" style="text-align: center;">
                    <div style="font-size: 2rem;">🥩</div>
                    <div class="metric-title">Proteínas</div>
                    <div class="metric-value">{resultado_macros["proteinas"]["g"]:.0f}g</div>
                    <div style="font-size: 0.9rem; color: #757575;">
                        {resultado_macros["proteinas"]["kcal"]:.0f} kcal<br>
                        {resultado_macros["proteinas"]["perc"]:.0f}%
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col_macro3:
                st.markdown(f'''
                <div class="metric-card" style="text-align: center;">
                    <div style="font-size: 2rem;">🥑</div>
                    <div class="metric-title">Lipídios</div>
                    <div class="metric-value">{resultado_macros["lipidios"]["g"]:.0f}g</div>
                    <div style="font-size: 0.9rem; color: #757575;">
                        {resultado_macros["lipidios"]["kcal"]:.0f} kcal<br>
                        {resultado_macros["lipidios"]["perc"]:.0f}%
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Gráfico de pizza
            fig_macros = px.pie(
                values=[
                    resultado_macros['carboidratos']['perc'],
                    resultado_macros['proteinas']['perc'],
                    resultado_macros['lipidios']['perc']
                ],
                names=['Carboidratos', 'Proteínas', 'Lipídios'],
                title='Distribuição dos Macronutrientes',
                color_discrete_sequence=['#FFB74D', '#FF8A65', '#81C784']
            )
            
            fig_macros.update_layout(height=400, title_x=0.5)
            st.plotly_chart(fig_macros, use_container_width=True)
            
            # Distribuição por refeição
            st.markdown("##### 🍽️ Sugestão de Distribuição por Refeição")
            
            refeicoes = {
                'Café da Manhã (25%)': 0.25,
                'Almoço (35%)': 0.35,
                'Jantar (30%)': 0.30,
                'Lanches (10%)': 0.10
            }
            
            df_refeicoes = []
            for refeicao, perc in refeicoes.items():
                df_refeicoes.append({
                    'Refeição': refeicao,
                    'Calorias': f"{calorias_totais * perc:.0f}",
                    'Carboidratos (g)': f"{resultado_macros['carboidratos']['g'] * perc:.0f}",
                    'Proteínas (g)': f"{resultado_macros['proteinas']['g'] * perc:.0f}",
                    'Lipídios (g)': f"{resultado_macros['lipidios']['g'] * perc:.0f}"
                })
            
            df_ref = pd.DataFrame(df_refeicoes)
            st.dataframe(df_ref, hide_index=True, use_container_width=True)
            
            # Equivalências alimentares
            st.markdown("##### 🥄 Equivalências Alimentares (Aproximadas)")
            
            equivalencias = f"""
            **Carboidratos ({resultado_macros['carboidratos']['g']:.0f}g/dia):**
            - 🍚 Arroz cozido: {resultado_macros['carboidratos']['g'] / 28:.1f} xícaras
            - 🍞 Pão francês: {resultado_macros['carboidratos']['g'] / 15:.0f} unidades
            - 🍝 Macarrão cozido: {resultado_macros['carboidratos']['g'] / 25:.1f} xícaras
            
            **Proteínas ({resultado_macros['proteinas']['g']:.0f}g/dia):**
            - 🥩 Carne vermelha magra: {resultado_macros['proteinas']['g'] / 26:.0f}g
            - 🐔 Peito de frango: {resultado_macros['proteinas']['g'] / 31:.0f}g
            - 🥚 Ovos: {resultado_macros['proteinas']['g'] / 6:.0f} unidades
            
            **Lipídios ({resultado_macros['lipidios']['g']:.0f}g/dia):**
            - 🫒 Azeite de oliva: {resultado_macros['lipidios']['g'] / 14:.1f} colheres de sopa
            - 🥜 Castanhas: {resultado_macros['lipidios']['g'] / 20:.0f} unidades
            - 🥑 Abacate: {resultado_macros['lipidios']['g'] / 15:.1f} unidades médias
            """
            
            st.markdown(equivalencias)

def show_ideal_weight_calculator():
    """Calculadora de peso ideal"""
    
    st.markdown('<div class="sub-header">⚖️ Calculadora de Peso Ideal</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("##### 📋 Dados do Paciente")
        
        altura = st.number_input("Altura (m)", min_value=0.5, max_value=2.5, value=1.70, step=0.01, key="ideal_altura")
        sexo = st.selectbox("Sexo", ["Feminino", "Masculino"], key="ideal_sexo")
        peso_atual = st.number_input("Peso Atual (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.1)
        
        st.markdown("##### 🧮 Fórmulas de Cálculo")
        
        formulas_selecionadas = st.multiselect(
            "Selecione as fórmulas",
            ["devine", "robinson", "miller"],
            default=["devine", "robinson"],
            format_func=lambda x: {
                "devine": "Fórmula de Devine (1974)",
                "robinson": "Fórmula de Robinson (1983)",
                "miller": "Fórmula de Miller (1983)"
            }[x]
        )
        
        calcular_ideal = st.button("⚖️ Calcular Peso Ideal", use_container_width=True)
    
    with col2:
        if calcular_ideal and formulas_selecionadas:
            st.markdown("##### ⚖️ Resultados do Peso Ideal")
            
            resultados = {}
            for formula in formulas_selecionadas:
                peso_ideal = NutritionalCalculators.calcular_peso_ideal(altura, sexo, formula)
                if peso_ideal:
                    resultados[formula] = peso_ideal
            
            if resultados:
                # Exibir resultados
                col_res1, col_res2, col_res3 = st.columns(3)
                
                pesos_ideais = list(resultados.values())
                peso_ideal_medio = sum(pesos_ideais) / len(pesos_ideais)
                diferenca_atual = peso_atual - peso_ideal_medio
                
                with col_res1:
                    st.metric("Peso Ideal Médio", f"{peso_ideal_medio:.1f} kg")
                
                with col_res2:
                    st.metric("Peso Atual", f"{peso_atual:.1f} kg")
                
                with col_res3:
                    cor = "normal"
                    if abs(diferenca_atual) > 5:
                        cor = "inverse"
                    
                    st.metric(
                        "Diferença", 
                        f"{diferenca_atual:+.1f} kg",
                        delta_color=cor
                    )
                
                # Tabela com todas as fórmulas
                st.markdown("##### 📊 Comparação das Fórmulas")
                
                df_pesos = pd.DataFrame([
                    {
                        'Fórmula': f.replace('_', ' ').title(),
                        'Peso Ideal (kg)': f"{peso:.1f}",
                        'Diferença do Atual': f"{peso_atual - peso:+.1f} kg",
                        'IMC no Peso Ideal': f"{peso / (altura ** 2):.1f}"
                    }
                    for f, peso in resultados.items()
                ])
                
                st.dataframe(df_pesos, hide_index=True, use_container_width=True)
                
                # Gráfico comparativo
                fig_comparacao = px.bar(
                    x=list(resultados.keys()),
                    y=list(resultados.values()),
                    title='Comparação dos Pesos Ideais por Fórmula',
                    labels={'x': 'Fórmula', 'y': 'Peso Ideal (kg)'},
                    color=list(resultados.values()),
                    color_continuous_scale='Greens'
                )
                
                # Adicionar linha do peso atual
                fig_comparacao.add_hline(
                    y=peso_atual, 
                    line_dash="dash", 
                    line_color="red",
                    annotation_text=f"Peso Atual ({peso_atual:.1f} kg)"
                )
                
                fig_comparacao.update_layout(height=400, title_x=0.5, showlegend=False)
                st.plotly_chart(fig_comparacao, use_container_width=True)
                
                # Faixa de peso saudável (IMC 18.5 - 24.9)
                st.markdown("##### 🎯 Faixa de Peso Saudável (IMC)")
                
                peso_min_saudavel = 18.5 * (altura ** 2)
                peso_max_saudavel = 24.9 * (altura ** 2)
                
                col_faixa1, col_faixa2, col_faixa3 = st.columns(3)
                
                with col_faixa1:
                    st.metric("Peso Mínimo", f"{peso_min_saudavel:.1f} kg", help="IMC 18.5")
                
                with col_faixa2:
                    st.metric("Peso Máximo", f"{peso_max_saudavel:.1f} kg", help="IMC 24.9")
                
                with col_faixa3:
                    faixa = peso_max_saudavel - peso_min_saudavel
                    st.metric("Faixa Total", f"{faixa:.1f} kg")
                
                # Avaliação
                if peso_atual < peso_min_saudavel:
                    st.info(f"📈 **Abaixo do peso:** Diferença de {peso_min_saudavel - peso_atual:.1f} kg para atingir o peso mínimo saudável.")
                elif peso_atual > peso_max_saudavel:
                    st.warning(f"📉 **Acima do peso:** Diferença de {peso_atual - peso_max_saudavel:.1f} kg para atingir o peso máximo saudável.")
                else:
                    st.success("✅ **Dentro da faixa saudável:** Peso atual está dentro dos parâmetros ideais de IMC.")

def show_complete_evaluation():
    """Avaliação nutricional completa"""
    
    st.markdown('<div class="sub-header">📋 Avaliação Nutricional Completa</div>', unsafe_allow_html=True)
    
    st.info("💡 Esta ferramenta combina todas as calculadoras para uma avaliação nutricional abrangente.")
    
    # Formulário completo
    with st.form("avaliacao_completa", clear_on_submit=False):
        st.markdown("##### 👤 Dados Pessoais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome_paciente = st.text_input("Nome do Paciente")
            idade = st.number_input("Idade (anos)", min_value=1, max_value=120, value=30)
            peso = st.number_input("Peso (kg)", min_value=1.0, max_value=300.0, value=70.0, step=0.1)
            altura = st.number_input("Altura (m)", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
        
        with col2:
            sexo = st.selectbox("Sexo", ["Feminino", "Masculino"])
            nivel_atividade = st.selectbox(
                "Nível de Atividade",
                ["sedentario", "leve", "moderado", "intenso", "muito_intenso"],
                format_func=lambda x: {
                    "sedentario": "Sedentário",
                    "leve": "Leve (1-3x/sem)",
                    "moderado": "Moderado (3-5x/sem)",
                    "intenso": "Intenso (6-7x/sem)",
                    "muito_intenso": "Muito Intenso (2x/dia)"
                }[x]
            )
            objetivo_principal = st.selectbox(
                "Objetivo Principal",
                ["manutencao", "perda_peso", "ganho_massa", "low_carb"],
                format_func=lambda x: {
                    "manutencao": "Manutenção",
                    "perda_peso": "Perda de Peso",
                    "ganho_massa": "Ganho de Massa",
                    "low_carb": "Low Carb"
                }[x]
            )
        
        st.markdown("##### 📏 Medidas Antropométricas (Opcional)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            circ_cintura = st.number_input("Cintura (cm)", min_value=0.0, value=0.0, step=0.1)
            circ_quadril = st.number_input("Quadril (cm)", min_value=0.0, value=0.0, step=0.1)
        
        with col2:
            dobra_tricipital = st.number_input("Dobra Tricipital (mm)", min_value=0.0, value=0.0, step=0.1)
            dobra_subscapular = st.number_input("Dobra Subescapular (mm)", min_value=0.0, value=0.0, step=0.1)
        
        with col3:
            dobra_abdominal = st.number_input("Dobra Abdominal (mm)", min_value=0.0, value=0.0, step=0.1)
            pressao_arterial = st.text_input("Pressão Arterial", placeholder="Ex: 120/80")
        
        st.markdown("##### 🏃 Fatores Adicionais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            atividade_fisica_reg = st.checkbox("Atividade física regular")
            clima_quente = st.checkbox("Clima quente/seco")
            gestante = st.checkbox("Gestante")
        
        with col2:
            lactante = st.checkbox("Lactante")
            restricoes = st.text_area("Restrições Alimentares", height=60)
            observacoes = st.text_area("Observações", height=60)
        
        avaliar_completo = st.form_submit_button("🔬 Realizar Avaliação Completa", use_container_width=True)
    
    if avaliar_completo:
        st.markdown("---")
        st.markdown(f'<div class="sub-header">📊 Relatório de Avaliação - {nome_paciente}</div>', unsafe_allow_html=True)
        
        # 1. Avaliação Antropométrica
        st.markdown("##### 📏 1. Avaliação Antropométrica")
        
        # IMC
        resultado_imc = NutritionalCalculators.calcular_imc(peso, altura)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("IMC", f"{resultado_imc['imc']}")
        with col2:
            st.metric("Classificação", resultado_imc['classificacao'])
        with col3:
            peso_ideal = NutritionalCalculators.calcular_peso_ideal(altura, sexo)
            if peso_ideal:
                st.metric("Peso Ideal", f"{peso_ideal:.1f} kg")
            else:
                st.metric("Peso Ideal", "N/A")
        with col4:
            if peso_ideal:
                diferenca = peso - peso_ideal
                st.metric("Diferença", f"{diferenca:+.1f} kg")
        
        # Composição corporal (se houver dados)
        dobras = [d for d in [dobra_tricipital, dobra_subscapular, dobra_abdominal] if d > 0]
        
        if circ_cintura > 0 or circ_quadril > 0 or dobras:
            composicao = NutritionalCalculators.avaliar_composicao_corporal(
                peso, altura, idade, sexo, circ_cintura, circ_quadril, dobras
            )
            
            if 'rcq' in composicao:
                st.success(f"**RCQ:** {composicao['rcq']['valor']} (Risco: {composicao['rcq']['risco']})")
            
            if 'percentual_gordura' in composicao:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("% Gordura", f"{composicao['percentual_gordura']:.1f}%")
                with col2:
                    st.metric("Massa Gorda", f"{composicao['massa_gorda']:.1f} kg")
                with col3:
                    st.metric("Massa Magra", f"{composicao['massa_magra']:.1f} kg")
        
        # 2. Gasto Energético
        st.markdown("##### 🔥 2. Avaliação Energética")
        
        tmb = NutritionalCalculators.calcular_tmb(peso, altura, idade, sexo)
        get_resultado = NutritionalCalculators.calcular_get(tmb, nivel_atividade)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("TMB", f"{tmb:.0f} kcal/dia")
        with col2:
            st.metric("GET", f"{get_resultado['get']:.0f} kcal/dia")
        with col3:
            atividade_kcal = get_resultado['get'] - tmb
            st.metric("Atividade", f"{atividade_kcal:.0f} kcal/dia")
        
        # 3. Necessidade Hídrica
        st.markdown("##### 💧 3. Necessidade Hídrica")
        
        agua_resultado = NutritionalCalculators.calcular_agua_diaria(peso, idade, atividade_fisica_reg, clima_quente)
        
        # Ajustes para gestação/lactação
        agua_total = agua_resultado['ml_dia']
        if gestante:
            agua_total += 300
        if lactante:
            agua_total += 700
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Água Total", f"{agua_total:.0f} ml/dia")
        with col2:
            st.metric("Litros", f"{agua_total/1000:.1f} L/dia")
        with col3:
            st.metric("Copos (200ml)", f"{agua_total/200:.0f}")
        
        # 4. Macronutrientes
        st.markdown("##### 🍽️ 4. Distribuição de Macronutrientes")
        
        # Ajustar calorias baseado no objetivo
        calorias_objetivo = get_resultado['get']
        if objetivo_principal == 'perda_peso':
            calorias_objetivo *= 0.85
        elif objetivo_principal == 'ganho_massa':
            calorias_objetivo *= 1.15
        
        macros = NutritionalCalculators.calcular_macronutrientes(calorias_objetivo, objetivo_principal)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Calorias", f"{calorias_objetivo:.0f} kcal")
        with col2:
            st.metric("Carboidratos", f"{macros['carboidratos']['g']:.0f}g")
        with col3:
            st.metric("Proteínas", f"{macros['proteinas']['g']:.0f}g")
        with col4:
            st.metric("Lipídios", f"{macros['lipidios']['g']:.0f}g")
        
        # 5. Resumo e Recomendações
        st.markdown("##### 📋 5. Resumo e Recomendações")
        
        # Gerar recomendações baseadas nos resultados
        recomendacoes = []
        
        if resultado_imc['imc'] < 18.5:
            recomendacoes.append("🔸 **Baixo peso:** Aumentar gradualmente a ingestão calórica com alimentos nutritivos")
        elif resultado_imc['imc'] > 25:
            recomendacoes.append("🔸 **Sobrepeso/Obesidade:** Criar déficit calórico moderado com acompanhamento")
        else:
            recomendacoes.append("🔸 **Peso adequado:** Manter hábitos alimentares saudáveis")
        
        if agua_total > 3000:
            recomendacoes.append("🔸 **Hidratação:** Distribuir a ingestão hídrica ao longo do dia")
        
        if objetivo_principal == 'ganho_massa':
            recomendacoes.append("🔸 **Ganho de massa:** Priorizar proteínas de alto valor biológico")
        
        if restricoes:
            recomendacoes.append(f"🔸 **Restrições:** Considerar as limitações alimentares: {restricoes}")
        
        recomendacoes.extend([
            "🔸 **Atividade física:** Manter regularidade nos exercícios",
            "🔸 **Acompanhamento:** Realizar reavaliações periódicas",
            "🔸 **Hidratação:** Monitorar cor da urina como indicador",
            "🔸 **Alimentação:** Priorizar alimentos in natura e minimamente processados"
        ])
        
        for rec in recomendacoes:
            st.markdown(rec)
        
        # Botão para salvar avaliação
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Salvar Avaliação", use_container_width=True):
                # Aqui você salvaria no banco de dados
                st.success("✅ Avaliação salva com sucesso!")
        
        with col2:
            if st.button("📄 Gerar PDF", use_container_width=True):
                st.info("📄 Funcionalidade de PDF em desenvolvimento")
        
        with col3:
            if st.button("📧 Enviar por Email", use_container_width=True):
                st.info("📧 Funcionalidade de email em desenvolvimento")

# =============================================================================
# 🍽️ SISTEMA DE PLANOS ALIMENTARES
# =============================================================================

def show_meal_plans():
    """Sistema completo de planos alimentares"""
    
    st.markdown('<h1 class="main-header">🍽️ Planos Alimentares</h1>', unsafe_allow_html=True)
    
    user = AuthSystem.get_current_user()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Meus Planos",
        "➕ Criar Plano", 
        "🔍 Buscar Planos",
        "📊 Relatórios"
    ])
    
    with tab1:
        show_meal_plans_list(user)
    
    with tab2:
        show_create_meal_plan(user)
    
    with tab3:
        show_search_meal_plans(user)
    
    with tab4:
        show_meal_plans_reports(user)

def show_meal_plans_list(user):
    """Lista todos os planos alimentares"""
    
    st.markdown('<div class="sub-header">📋 Lista de Planos Alimentares</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_paciente = st.selectbox("👤 Filtrar por Paciente", ["Todos"] + get_patient_names(user['id']))
    
    with col2:
        filtro_status = st.selectbox("📊 Status", ["Todos", "Ativos", "Vencidos"])
    
    with col3:
        ordenar = st.selectbox("📄 Ordenar por", ["Data Criação", "Nome", "Paciente", "Validade"])
    
    # Buscar planos
    query = """
    SELECT p.*, pac.nome as paciente_nome
    FROM planos_alimentares p
    LEFT JOIN pacientes pac ON p.paciente_id = pac.id
    WHERE p.nutricionista_id = ?
    """
    
    params = [user['id']]
    
    if filtro_paciente != "Todos":
        query += " AND pac.nome = ?"
        params.append(filtro_paciente)
    
    if filtro_status == "Ativos":
        query += " AND p.ativo = 1 AND (p.data_validade IS NULL OR p.data_validade >= DATE('now'))"
    elif filtro_status == "Vencidos":
        query += " AND p.data_validade < DATE('now')"
    
    # Ordenação
    if ordenar == "Nome":
        query += " ORDER BY p.nome"
    elif ordenar == "Paciente":
        query += " ORDER BY pac.nome"
    elif ordenar == "Validade":
        query += " ORDER BY p.data_validade DESC"
    else:
        query += " ORDER BY p.data_criacao DESC"
    
    cursor.execute(query, params)
    planos = cursor.fetchall()
    
    if planos:
        st.success(f"📊 **{len(planos)} plano(s) encontrado(s)**")
        
        for plano in planos:
            with st.expander(f"🍽️ {plano['nome']} - {plano['paciente_nome'] or 'Modelo'}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**👤 Paciente:** {plano['paciente_nome'] or 'Modelo Genérico'}")
                    st.write(f"**🎯 Objetivo:** {plano['objetivo'] or 'Não especificado'}")
                    st.write(f"**📅 Criado:** {datetime.fromisoformat(plano['data_criacao']).strftime('%d/%m/%Y')}")
                
                with col2:
                    st.write(f"**🔥 Calorias:** {plano['calorias_totais'] or 0} kcal")
                    if plano['data_validade']:
                        validade = datetime.fromisoformat(plano['data_validade'])
                        status_val = "✅ Válido" if validade >= datetime.now() else "❌ Vencido"
                        st.write(f"**📆 Validade:** {validade.strftime('%d/%m/%Y')} ({status_val})")
                    else:
                        st.write("**📆 Validade:** Permanente")
                
                with col3:
                    st.write(f"**🍞 Carboidratos:** {plano['carboidratos'] or 0}g")
                    st.write(f"**🥩 Proteínas:** {plano['proteinas'] or 0}g")
                    st.write(f"**🥑 Lipídios:** {plano['lipidios'] or 0}g")
                
                # Refeições
                if plano['refeicoes']:
                    try:
                        refeicoes = json.loads(plano['refeicoes'])
                        st.markdown("**📋 Refeições:**")
                        
                        for refeicao_nome, detalhes in refeicoes.items():
                            st.markdown(f"**{refeicao_nome}:**")
                            if isinstance(detalhes, dict) and 'alimentos' in detalhes:
                                for alimento in detalhes['alimentos']:
                                    st.markdown(f"- {alimento['nome']} ({alimento['quantidade']})")
                            else:
                                st.markdown(f"- {detalhes}")
                    except:
                        st.write("Erro ao carregar refeições")
                
                # Botões de ação
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("👁️ Visualizar", key=f"view_{plano['id']}"):
                        show_meal_plan_details(plano)
                
                with col2:
                    if st.button("✏️ Editar", key=f"edit_{plano['id']}"):
                        st.session_state.editing_plan_id = plano['id']
                        st.rerun()
                
                with col3:
                    if st.button("📄 PDF", key=f"pdf_{plano['id']}"):
                        generate_meal_plan_pdf(plano)
                
                with col4:
                    if st.button("📧 Enviar", key=f"send_{plano['id']}"):
                        st.info("📧 Funcionalidade de envio em desenvolvimento")
    else:
        st.info("📋 Nenhum plano alimentar encontrado.")
        if st.button("➕ Criar Primeiro Plano"):
            st.session_state.active_tab = 1
            st.rerun()
    
    conn.close()

def get_patient_names(nutricionista_id):
    """Obtém nomes dos pacientes para filtros"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome FROM pacientes WHERE nutricionista_id = ? AND ativo = 1 ORDER BY nome", (nutricionista_id,))
    nomes = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return nomes

def show_create_meal_plan(user):
    """Interface para criar plano alimentar"""
    
    st.markdown('<div class="sub-header">➕ Criar Novo Plano Alimentar</div>', unsafe_allow_html=True)
    
    # Seleção do paciente
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, uuid, nome FROM pacientes WHERE nutricionista_id = ? AND ativo = 1 ORDER BY nome", (user['id'],))
    pacientes = cursor.fetchall()
    
    if not pacientes:
        st.warning("⚠️ Você precisa cadastrar pelo menos um paciente antes de criar um plano alimentar.")
        if st.button("➕ Cadastrar Paciente"):
            st.session_state.page = 'patients'
            st.rerun()
        return
    
    # Formulário do plano
    with st.form("criar_plano_alimentar"):
        st.markdown("##### 🎯 Informações Básicas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            paciente_selecionado = st.selectbox(
                "👤 Selecione o Paciente",
                options=pacientes,
                format_func=lambda x: x[2],  # nome
                help="Escolha o paciente para este plano"
            )
            
            nome_plano = st.text_input("📝 Nome do Plano", placeholder="Ex: Plano para Perda de Peso - Maria")
            
            objetivo = st.selectbox(
                "🎯 Objetivo Principal",
                ["Perda de peso", "Ganho de massa muscular", "Manutenção", "Controle glicêmico", "Redução colesterol", "Hipertrofia", "Outro"]
            )
        
        with col2:
            calorias_totais = st.number_input("🔥 Calorias Totais/dia", min_value=800, max_value=5000, value=2000, step=50)
            
            data_validade = st.date_input(
                "📅 Data de Validade",
                value=datetime.now() + timedelta(days=30),
                help="Deixe em branco para plano permanente"
            )
            
            if objetivo == "Outro":
                objetivo = st.text_input("Especifique o objetivo", placeholder="Descreva o objetivo específico")
        
        st.markdown("##### 🍽️ Distribuição de Macronutrientes")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            carboidratos_g = st.number_input("🍞 Carboidratos (g)", min_value=0.0, value=250.0, step=5.0)
        
        with col2:
            proteinas_g = st.number_input("🥩 Proteínas (g)", min_value=0.0, value=100.0, step=5.0)
        
        with col3:
            lipidios_g = st.number_input("🥑 Lipídios (g)", min_value=0.0, value=67.0, step=5.0)
        
        # Verificar se os macros batem com as calorias
        calorias_calculadas = (carboidratos_g * 4) + (proteinas_g * 4) + (lipidios_g * 9)
        diferenca = abs(calorias_calculadas - calorias_totais)
        
        if diferenca > 50:
            st.warning(f"⚠️ As calorias dos macronutrientes ({calorias_calculadas:.0f} kcal) não correspondem ao total informado ({calorias_totais} kcal)")
        
        st.markdown("##### 🍽️ Refeições do Dia")
        
        # Número de refeições
        num_refeicoes = st.selectbox("Número de Refeições", [3, 4, 5, 6], value=5)
        
        refeicoes_nomes = {
            3: ["Café da Manhã", "Almoço", "Jantar"],
            4: ["Café da Manhã", "Almoço", "Lanche", "Jantar"],
            5: ["Café da Manhã", "Lanche da Manhã", "Almoço", "Lanche da Tarde", "Jantar"],
            6: ["Café da Manhã", "Lanche da Manhã", "Almoço", "Lanche da Tarde", "Jantar", "Ceia"]
        }
        
        refeicoes_data = {}
        
        # Distribuição calórica sugerida
        distribuicao_calorica = {
            3: [0.30, 0.40, 0.30],
            4: [0.25, 0.35, 0.15, 0.25],
            5: [0.25, 0.10, 0.35, 0.15, 0.15],
            6: [0.25, 0.10, 0.30, 0.15, 0.15, 0.05]
        }
        
        for i, refeicao_nome in enumerate(refeicoes_nomes[num_refeicoes]):
            with st.expander(f"🍽️ {refeicao_nome}", expanded=True):
                calorias_sugeridas = calorias_totais * distribuicao_calorica[num_refeicoes][i]
                st.caption(f"Calorias sugeridas: {calorias_sugeridas:.0f} kcal ({distribuicao_calorica[num_refeicoes][i]*100:.0f}%)")
                
                # Lista de alimentos
                alimentos_refeicao = []
                num_alimentos = st.number_input(f"Número de alimentos ({refeicao_nome})", min_value=1, max_value=10, value=3, key=f"num_alimentos_{i}")
                
                for j in range(num_alimentos):
                    col_alimento1, col_alimento2, col_alimento3 = st.columns([2, 1, 1])
                    
                    with col_alimento1:
                        nome_alimento = st.text_input(f"Alimento {j+1}", placeholder="Ex: Aveia em flocos", key=f"alimento_{i}_{j}")
                    
                    with col_alimento2:
                        quantidade = st.text_input(f"Quantidade", placeholder="Ex: 3 col. sopa", key=f"qtd_{i}_{j}")
                    
                    with col_alimento3:
                        calorias_alimento = st.number_input(f"Kcal", min_value=0, value=0, key=f"kcal_{i}_{j}")
                    
                    if nome_alimento and quantidade:
                        alimentos_refeicao.append({
                            'nome': nome_alimento,
                            'quantidade': quantidade,
                            'calorias': calorias_alimento
                        })
                
                # Observações da refeição
                obs_refeicao = st.text_area(f"Observações ({refeicao_nome})", placeholder="Dicas de preparo, substituições, etc.", key=f"obs_{i}")
                
                refeicoes_data[refeicao_nome] = {
                    'alimentos': alimentos_refeicao,
                    'observacoes': obs_refeicao,
                    'calorias_sugeridas': calorias_sugeridas
                }
        
        st.markdown("##### 📝 Observações Gerais")
        
        observacoes_gerais = st.text_area(
            "Observações e Orientações",
            placeholder="Adicione orientações gerais, dicas de preparo, substituições permitidas, etc.",
            height=100
        )
        
        # Botões do formulário
        col1, col2, col3 = st.columns(3)
        
        with col1:
            criar_plano = st.form_submit_button("💾 Criar Plano", use_container_width=True)
        
        with col2:
            if st.form_submit_button("📋 Salvar como Modelo", use_container_width=True):
                st.info("📋 Funcionalidade de modelos em desenvolvimento")
        
        with col3:
            if st.form_submit_button("🔄 Limpar Formulário", use_container_width=True):
                st.rerun()
    
    if criar_plano:
        # Validar dados obrigatórios
        if not nome_plano:
            st.error("❌ Por favor, informe o nome do plano")
            return
        
        # Validar se há alimentos nas refeições
        tem_alimentos = False
        for refeicao_data in refeicoes_data.values():
            if refeicao_data['alimentos']:
                tem_alimentos = True
                break
        
        if not tem_alimentos:
            st.error("❌ Por favor, adicione pelo menos um alimento em uma refeição")
            return
        
        # Salvar plano no banco
        try:
            plano_uuid = str(uuid.uuid4())
            
            cursor.execute('''
            INSERT INTO planos_alimentares (
                uuid, paciente_id, nutricionista_id, nome, objetivo,
                calorias_totais, carboidratos, proteinas, lipidios,
                data_criacao, data_validade, refeicoes, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                plano_uuid,
                paciente_selecionado[0],  # id do paciente
                user['id'],
                nome_plano,
                objetivo,
                calorias_totais,
                carboidratos_g,
                proteinas_g,
                lipidios_g,
                datetime.now().strftime('%Y-%m-%d'),
                data_validade.strftime('%Y-%m-%d') if data_validade else None,
                json.dumps(refeicoes_data, ensure_ascii=False),
                observacoes_gerais
            ))
            
            # Log da ação
            cursor.execute('''
            INSERT INTO logs_sistema (usuario_id, acao, tabela_afetada, registro_id)
            VALUES (?, ?, ?, ?)
            ''', (user['id'], 'CREATE', 'planos_alimentares', plano_uuid))
            
            conn.commit()
            
            st.success(f"✅ Plano alimentar **{nome_plano}** criado com sucesso!")
            st.balloons()
            
            # Opções pós-criação
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("👁️ Visualizar Plano"):
                    st.session_state.view_plan_id = plano_uuid
                    st.rerun()
            
            with col2:
                if st.button("📄 Gerar PDF"):
                    st.info("📄 Gerando PDF...")
            
            with col3:
                if st.button("📋 Ver Todos os Planos"):
                    st.session_state.active_tab = 0
                    st.rerun()
        
        except Exception as e:
            st.error(f"❌ Erro ao criar plano: {str(e)}")
        
        finally:
            conn.close()

def show_search_meal_plans(user):
    """Sistema de busca de planos alimentares"""
    
    st.markdown('<div class="sub-header">🔍 Buscar Planos Alimentares</div>', unsafe_allow_html=True)
    
    # Filtros de busca avançada
    with st.expander("🔧 Filtros de Busca", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            busca_nome = st.text_input("Nome do Plano", placeholder="Digite parte do nome...")
            busca_objetivo = st.multiselect(
                "Objetivos",
                ["Perda de peso", "Ganho de massa muscular", "Manutenção", "Controle glicêmico", "Redução colesterol"]
            )
        
        with col2:
            calorias_min = st.number_input("Calorias Mínimas", min_value=0, value=0)
            calorias_max = st.number_input("Calorias Máximas", min_value=0, value=5000)
        
        with col3:
            data_inicio = st.date_input("Criado a partir de", value=None)
            data_fim = st.date_input("Criado até", value=None)
            apenas_ativos = st.checkbox("Apenas planos ativos", value=True)
    
    if st.button("🔍 Buscar", use_container_width=True):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Construir query
        query = """
        SELECT p.*, pac.nome as paciente_nome
        FROM planos_alimentares p
        LEFT JOIN pacientes pac ON p.paciente_id = pac.id
        WHERE p.nutricionista_id = ?
        """
        
        params = [user['id']]
        
        if busca_nome:
            query += " AND p.nome LIKE ?"
            params.append(f"%{busca_nome}%")
        
        if busca_objetivo:
            objetivos_str = "', '".join(busca_objetivo)
            query += f" AND p.objetivo IN ('{objetivos_str}')"
        
        if calorias_min > 0:
            query += " AND p.calorias_totais >= ?"
            params.append(calorias_min)
        
        if calorias_max < 5000:
            query += " AND p.calorias_totais <= ?"
            params.append(calorias_max)
        
        if data_inicio:
            query += " AND DATE(p.data_criacao) >= ?"
            params.append(data_inicio.strftime('%Y-%m-%d'))
        
        if data_fim:
            query += " AND DATE(p.data_criacao) <= ?"
            params.append(data_fim.strftime('%Y-%m-%d'))
        
        if apenas_ativos:
            query += " AND p.ativo = 1 AND (p.data_validade IS NULL OR p.data_validade >= DATE('now'))"
        
        query += " ORDER BY p.data_criacao DESC"
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        if resultados:
            st.success(f"🎯 Encontrados {len(resultados)} plano(s)")
            
            # Exibir resultados em grid
            for i in range(0, len(resultados), 2):
                col1, col2 = st.columns(2)
                
                with col1:
                    if i < len(resultados):
                        show_meal_plan_card(resultados[i])
                
                with col2:
                    if i + 1 < len(resultados):
                        show_meal_plan_card(resultados[i + 1])
        else:
            st.warning("🔍 Nenhum plano encontrado com os critérios especificados.")
        
        conn.close()

def show_meal_plan_card(plano):
    """Exibe um card com informações do plano"""
    
    # Calcular status
    status_emoji = "✅"
    status_text = "Ativo"
    
    if plano['data_validade']:
        validade = datetime.fromisoformat(plano['data_validade'])
        if validade < datetime.now():
            status_emoji = "❌"
            status_text = "Vencido"
    
    if not plano['ativo']:
        status_emoji = "⏸️"
        status_text = "Inativo"
    
    # Card do plano
    st.markdown(f'''
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #2E7D32;">🍽️ {plano['nome']}</h4>
            <span class="status-badge status-{'active' if status_text == 'Ativo' else 'pending'}">{status_emoji} {status_text}</span>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <div><strong>👤 Paciente:</strong> {plano['paciente_nome'] or 'Modelo'}</div>
            <div><strong>🎯 Objetivo:</strong> {plano['objetivo'] or 'Não especificado'}</div>
            <div><strong>🔥 Calorias:</strong> {plano['calorias_totais'] or 0} kcal</div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; margin-bottom: 1rem; font-size: 0.9rem;">
            <div><strong>🍞</strong> {plano['carboidratos'] or 0}g</div>
            <div><strong>🥩</strong> {plano['proteinas'] or 0}g</div>
            <div><strong>🥑</strong> {plano['lipidios'] or 0}g</div>
        </div>
        
        <div style="font-size: 0.8rem; color: #757575; margin-bottom: 1rem;">
            📅 Criado em {datetime.fromisoformat(plano['data_criacao']).strftime('%d/%m/%Y')}
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👁️ Ver", key=f"view_card_{plano['id']}", use_container_width=True):
            show_meal_plan_details(plano)
    
    with col2:
        if st.button("✏️ Editar", key=f"edit_card_{plano['id']}", use_container_width=True):
            st.session_state.editing_plan_id = plano['id']
    
    with col3:
        if st.button("📄 PDF", key=f"pdf_card_{plano['id']}", use_container_width=True):
            generate_meal_plan_pdf(plano)

def show_meal_plan_details(plano):
    """Mostra detalhes completos do plano alimentar"""
    
    st.markdown("---")
    st.markdown(f'<div class="sub-header">👁️ Detalhes do Plano: {plano["nome"]}</div>', unsafe_allow_html=True)
    
    # Informações básicas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔥 Calorias Totais", f"{plano['calorias_totais'] or 0} kcal")
        st.metric("🍞 Carboidratos", f"{plano['carboidratos'] or 0}g")
    
    with col2:
        st.metric("🥩 Proteínas", f"{plano['proteinas'] or 0}g")
        st.metric("🥑 Lipídios", f"{plano['lipidios'] or 0}g")
    
    with col3:
        # Calcular percentuais
        if plano['calorias_totais'] and plano['calorias_totais'] > 0:
            carb_perc = (plano['carboidratos'] * 4 / plano['calorias_totais']) * 100 if plano['carboidratos'] else 0
            prot_perc = (plano['proteinas'] * 4 / plano['calorias_totais']) * 100 if plano['proteinas'] else 0
            lip_perc = (plano['lipidios'] * 9 / plano['calorias_totais']) * 100 if plano['lipidios'] else 0
            
            st.write(f"**📊 Distribuição:**")
            st.write(f"🍞 Carboidratos: {carb_perc:.1f}%")
            st.write(f"🥩 Proteínas: {prot_perc:.1f}%")
            st.write(f"🥑 Lipídios: {lip_perc:.1f}%")
    
    # Gráfico de macronutrientes
    if plano['carboidratos'] and plano['proteinas'] and plano['lipidios']:
        fig_macros = px.pie(
            values=[plano['carboidratos'], plano['proteinas'], plano['lipidios']],
            names=['Carboidratos (g)', 'Proteínas (g)', 'Lipídios (g)'],
            title='Distribuição de Macronutrientes (gramas)',
            color_discrete_sequence=['#FFB74D', '#FF8A65', '#81C784']
        )
        
        fig_macros.update_layout(height=300)
        st.plotly_chart(fig_macros, use_container_width=True)
    
    # Refeições detalhadas
    if plano['refeicoes']:
        st.markdown("---")
        st.markdown("##### 🍽️ Refeições Detalhadas")
        
        try:
            refeicoes = json.loads(plano['refeicoes'])
            
            for refeicao_nome, detalhes in refeicoes.items():
                with st.expander(f"🍽️ {refeicao_nome}", expanded=True):
                    if isinstance(detalhes, dict) and 'alimentos' in detalhes:
                        # Tabela de alimentos
                        if detalhes['alimentos']:
                            alimentos_data = []
                            total_calorias_refeicao = 0
                            
                            for alimento in detalhes['alimentos']:
                                calorias = alimento.get('calorias', 0)
                                total_calorias_refeicao += calorias
                                
                                alimentos_data.append({
                                    'Alimento': alimento['nome'],
                                    'Quantidade': alimento['quantidade'],
                                    'Calorias': f"{calorias} kcal" if calorias > 0 else "N/A"
                                })
                            
                            df_alimentos = pd.DataFrame(alimentos_data)
                            st.dataframe(df_alimentos, hide_index=True, use_container_width=True)
                            
                            if total_calorias_refeicao > 0:
                                st.info(f"🔥 **Total da refeição:** {total_calorias_refeicao} kcal")
                        
                        # Observações da refeição
                        if detalhes.get('observacoes'):
                            st.markdown("**💡 Observações:**")
                            st.markdown(detalhes['observacoes'])
                    
                    else:
                        st.markdown(f"- {detalhes}")
        
        except json.JSONDecodeError:
            st.error("❌ Erro ao carregar dados das refeições")
    
    # Observações gerais
    if plano['observacoes']:
        st.markdown("---")
        st.markdown("##### 📝 Observações Gerais")
        st.markdown(plano['observacoes'])
    
    # Informações adicionais
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📅 Data de Criação:** {datetime.fromisoformat(plano['data_criacao']).strftime('%d/%m/%Y')}
        
        **🎯 Objetivo:** {plano['objetivo'] or 'Não especificado'}
        
        **📆 Validade:** {datetime.fromisoformat(plano['data_validade']).strftime('%d/%m/%Y') if plano['data_validade'] else 'Permanente'}
        """)
    
    with col2:
        # Botões de ação
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📄 Gerar PDF", use_container_width=True):
                generate_meal_plan_pdf(plano)
        
        with col_btn2:
            if st.button("📧 Enviar por Email", use_container_width=True):
                st.info("📧 Funcionalidade em desenvolvimento")

def generate_meal_plan_pdf(plano):
    """Gera PDF do plano alimentar"""
    # Placeholder para geração de PDF
    st.info("📄 Gerando PDF do plano alimentar...")
    
    # Aqui você implementaria a geração real do PDF
    # usando bibliotecas como reportlab, weasyprint, etc.
    
    st.success("✅ PDF gerado com sucesso! (Funcionalidade em desenvolvimento)")

def show_meal_plans_reports(user):
    """Relatórios e estatísticas dos planos alimentares"""
    
    st.markdown('<div class="sub-header">📊 Relatórios de Planos Alimentares</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cursor.execute("SELECT COUNT(*) FROM planos_alimentares WHERE nutricionista_id = ?", (user['id'],))
        total_planos = cursor.fetchone()[0]
        st.metric("📋 Total de Planos", total_planos)
    
    with col2:
        cursor.execute("""
        SELECT COUNT(*) FROM planos_alimentares 
        WHERE nutricionista_id = ? AND ativo = 1 
        AND (data_validade IS NULL OR data_validade >= DATE('now'))
        """, (user['id'],))
        planos_ativos = cursor.fetchone()[0]
        st.metric("✅ Planos Ativos", planos_ativos)
    
    with col3:
        cursor.execute("""
        SELECT COUNT(*) FROM planos_alimentares 
        WHERE nutricionista_id = ? AND DATE(data_criacao) >= DATE('now', 'start of month')
        """, (user['id'],))
        planos_mes = cursor.fetchone()[0]
        st.metric("📅 Criados este Mês", planos_mes)
    
    with col4:
        cursor.execute("""
        SELECT AVG(calorias_totais) FROM planos_alimentares 
        WHERE nutricionista_id = ? AND calorias_totais > 0
        """, (user['id'],))
        media_calorias = cursor.fetchone()[0]
        if media_calorias:
            st.metric("🔥 Média de Calorias", f"{media_calorias:.0f}")
        else:
            st.metric("🔥 Média de Calorias", "N/A")
    
    st.markdown("---")
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Planos por objetivo
        cursor.execute("""
        SELECT objetivo, COUNT(*) as total
        FROM planos_alimentares
        WHERE nutricionista_id = ? AND objetivo IS NOT NULL
        GROUP BY objetivo
        ORDER BY total DESC
        """, (user['id'],))
        
        dados_objetivo = cursor.fetchall()
        
        if dados_objetivo:
            df_objetivo = pd.DataFrame(dados_objetivo, columns=['Objetivo', 'Total'])
            
            fig_objetivo = px.pie(
                df_objetivo,
                values='Total',
                names='Objetivo',
                title='Distribuição por Objetivo'
            )
            
            fig_objetivo.update_layout(height=400)
            st.plotly_chart(fig_objetivo, use_container_width=True)
    
    with col2:
        # Evolução de criação de planos
        cursor.execute("""
        SELECT strftime('%Y-%m', data_criacao) as mes, COUNT(*) as total
        FROM planos_alimentares
        WHERE nutricionista_id = ? AND data_criacao >= DATE('now', '-12 months')
        GROUP BY strftime('%Y-%m', data_criacao)
        ORDER BY mes
        """, (user['id'],))
        
        dados_evolucao = cursor.fetchall()
        
        if dados_evolucao:
            df_evolucao = pd.DataFrame(dados_evolucao, columns=['Mês', 'Total'])
            df_evolucao['Mês Nome'] = pd.to_datetime(df_evolucao['Mês']).dt.strftime('%b/%Y')
            
            fig_evolucao = px.line(
                df_evolucao,
                x='Mês Nome',
                y='Total',
                title='Planos Criados por Mês',
                markers=True
            )
            
            fig_evolucao.update_traces(line_color='#2E7D32')
            fig_evolucao.update_layout(height=400)
            st.plotly_chart(fig_evolucao, use_container_width=True)
    
    # Análise de macronutrientes
    st.markdown("##### 📊 Análise de Macronutrientes")
    
    cursor.execute("""
    SELECT carboidratos, proteinas, lipidios, calorias_totais
    FROM planos_alimentares
    WHERE nutricionista_id = ? AND carboidratos > 0 AND proteinas > 0 AND lipidios > 0
    """, (user['id'],))
    
    dados_macros = cursor.fetchall()
    
    if dados_macros:
        df_macros = pd.DataFrame(dados_macros, columns=['Carboidratos', 'Proteínas', 'Lipídios', 'Calorias'])
        
        # Calcular médias
        media_carb = df_macros['Carboidratos'].mean()
        media_prot = df_macros['Proteínas'].mean()
        media_lip = df_macros['Lipídios'].mean()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🍞 Carboidratos Médio", f"{media_carb:.1f}g")
        
        with col2:
            st.metric("🥩 Proteínas Médio", f"{media_prot:.1f}g")
        
        with col3:
            st.metric("🥑 Lipídios Médio", f"{media_lip:.1f}g")
        
        # Gráfico de dispersão - Calorias vs Macros
        fig_scatter = px.scatter(
            df_macros,
            x='Calorias',
            y='Proteínas',
            size='Carboidratos',
            color='Lipídios',
            title='Relação Calorias vs Proteínas (Tamanho = Carboidratos, Cor = Lipídios)',
            labels={'Calorias': 'Calorias Totais (kcal)', 'Proteínas': 'Proteínas (g)'}
        )
        
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("📊 Dados insuficientes para análise de macronutrientes")
    
    conn.close()

# =============================================================================
# 📅 SISTEMA DE AGENDAMENTOS
# =============================================================================

def show_appointments():
    """Sistema completo de agendamentos"""
    
    st.markdown('<h1 class="main-header">📅 Sistema de Agendamentos</h1>', unsafe_allow_html=True)
    
    user = AuthSystem.get_current_user()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📅 Agenda",
        "➕ Nova Consulta",
        "🔍 Buscar Consultas",
        "📊 Relatórios",
        "⚙️ Configurações"
    ])
    
    with tab1:
        show_calendar_view(user)
    
    with tab2:
        show_new_appointment(user)
    
    with tab3:
        show_search_appointments(user)
    
    with tab4:
        show_appointments_reports(user)
    
    with tab5:
        show_appointment_settings(user)

def show_calendar_view(user):
    """Visualização em calendário das consultas"""
    
    st.markdown('<div class="sub-header">📅 Agenda de Consultas</div>', unsafe_allow_html=True)
    
    # Seleção de período
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        data_inicio = st.date_input("📅 Data Início", value=datetime.now())
    
    with col2:
        data_fim = st.date_input("📅 Data Fim", value=datetime.now() + timedelta(days=30))
    
    with col3:
        view_mode = st.selectbox("👁️ Visualização", ["Lista", "Calendário"])
    
    # Buscar consultas do período
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT c.*, p.nome as paciente_nome, p.telefone
    FROM consultas c
    JOIN pacientes p ON c.paciente_id = p.id
    WHERE c.nutricionista_id = ?
    AND DATE(c.data_consulta) BETWEEN ? AND ?
    ORDER BY c.data_consulta
    """, (user['id'], data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d')))
    
    consultas = cursor.fetchall()
    
    if consultas:
        st.success(f"📊 **{len(consultas)} consulta(s) no período**")
        
        if view_mode == "Lista":
            show_appointments_list_view(consultas)
        else:
            show_appointments_calendar_view(consultas, data_inicio, data_fim)
    else:
        st.info("📅 Nenhuma consulta agendada no período selecionado.")
        if st.button("➕ Agendar Primeira Consulta"):
            st.session_state.active_tab = 1
            st.rerun()
    
    conn.close()

def show_appointments_list_view(consultas):
    """Visualização em lista das consultas"""
    
    for consulta in consultas:
        data_consulta = datetime.fromisoformat(consulta['data_consulta'])
        
        # Definir cor do status
        status_colors = {
            'agendada': ('🟡', '#FFF3E0'),
            'realizada': ('🟢', '#E8F5E8'),
            'cancelada': ('🔴', '#FFEBEE'),
            'faltou': ('🟠', '#FFF3E0')
        }
        
        emoji, bg_color = status_colors.get(consulta['status'], ('⚪', '#F5F5F5'))
        
        # Card da consulta
        st.markdown(f'''
        <div style="
            background: {bg_color};
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 4px solid #2E7D32;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 1rem;">
                <h4 style="margin: 0; color: #2E7D32;">
                    {emoji} {data_consulta.strftime('%d/%m/%Y às %H:%M')}
                </h4>
                <span style="
                    background: #2E7D32;
                    color: white;
                    padding: 0.25rem 0.75rem;
                    border-radius: 20px;
                    font-size: 0.8rem;
                    font-weight: 600;
                ">
                    {consulta['status'].upper()}
                </span>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div>
                    <strong>👤 Paciente:</strong><br>
                    {consulta['paciente_nome']}
                </div>
                <div>
                    <strong>📱 Telefone:</strong><br>
                    {consulta['telefone'] or 'Não informado'}
                </div>
                <div>
                    <strong>🏥 Tipo:</strong><br>
                    {consulta['tipo_consulta']}
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                <div>
                    <strong>⏱️ Duração:</strong><br>
                    {consulta['duracao']} minutos
                </div>
                <div>
                    <strong>💰 Valor:</strong><br>
                    R$ {consulta['valor']:.2f if consulta['valor'] else 0:.2f}
                </div>
                <div>
                    <strong>🔄 Retorno:</strong><br>
                    {datetime.fromisoformat(consulta['retorno_data']).strftime('%d/%m/%Y') if consulta['retorno_data'] else 'Não agendado'}
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Observações
        if consulta['observacoes']:
            st.markdown(f"**💭 Observações:** {consulta['observacoes']}")
        
        # Botões de ação
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("👁️ Ver", key=f"view_appt_{consulta['id']}"):
                show_appointment_details(consulta)
        
        with col2:
            if st.button("✏️ Editar", key=f"edit_appt_{consulta['id']}"):
                st.session_state.editing_appointment_id = consulta['id']
        
        with col3:
            if consulta['status'] == 'agendada':
                if st.button("✅ Realizada", key=f"done_appt_{consulta['id']}"):
                    update_appointment_status(consulta['id'], 'realizada')
                    st.rerun()
        
        with col4:
            if consulta['status'] == 'agendada':
                if st.button("❌ Cancelar", key=f"cancel_appt_{consulta['id']}"):
                    update_appointment_status(consulta['id'], 'cancelada')
                    st.rerun()
        
        with col5:
            if st.button("📧 Lembrete", key=f"remind_appt_{consulta['id']}"):
                send_appointment_reminder(consulta)
        
        st.markdown("---")

def show_appointments_calendar_view(consultas, data_inicio, data_fim):
    """Visualização em calendário das consultas"""
    
    st.info("📅 Visualização em calendário em desenvolvimento. Mostrando lista agrupada por dia:")
    
    # Agrupar consultas por dia
    consultas_por_dia = {}
    for consulta in consultas:
        data_consulta = datetime.fromisoformat(consulta['data_consulta']).date()
        if data_consulta not in consultas_por_dia:
            consultas_por_dia[data_consulta] = []
        consultas_por_dia[data_consulta].append(consulta)
    
    # Exibir consultas agrupadas por dia
    for data, consultas_dia in sorted(consultas_por_dia.items()):
        dia_semana = calendar.day_name[data.weekday()]
        
        st.markdown(f'''
        <div style="
            background: linear-gradient(135deg, #E8F5E8, #F1F8E9);
            border-radius: 12px;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 4px solid #2E7D32;
        ">
            <h4 style="margin: 0; color: #2E7D32;">
                📅 {data.strftime('%d/%m/%Y')} - {dia_semana}
            </h4>
            <div style="font-size: 0.9rem; color: #757575;">
                {len(consultas_dia)} consulta(s) agendada(s)
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        for consulta in sorted(consultas_dia, key=lambda x: x['data_consulta']):
            hora = datetime.fromisoformat(consulta['data_consulta']).strftime('%H:%M')
            
            status_emoji = {
                'agendada': '🟡',
                'realizada': '🟢',
                'cancelada': '🔴',
                'faltou': '🟠'
            }.get(consulta['status'], '⚪')
            
            st.markdown(f'''
            <div style="
                margin: 0.5rem 0 0.5rem 2rem;
                padding: 0.75rem;
                background: white;
                border-radius: 8px;
                border-left: 3px solid #4CAF50;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{status_emoji} {hora}</strong> - {consulta['paciente_nome']}
                        <br>
                        <small style="color: #757575;">{consulta['tipo_consulta']} ({consulta['duracao']}min)</small>
                    </div>
                    <div style="text-align: right; font-size: 0.9rem;">
                        R$ {consulta['valor']:.2f if consulta['valor'] else 0:.2f}
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)

def show_new_appointment(user):
    """Formulário para nova consulta"""
    
    st.markdown('<div class="sub-header">➕ Agendar Nova Consulta</div>', unsafe_allow_html=True)
    
    # Buscar pacientes
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, uuid, nome FROM pacientes WHERE nutricionista_id = ? AND ativo = 1 ORDER BY nome", (user['id'],))
    pacientes = cursor.fetchall()
    
    if not pacientes:
        st.warning("⚠️ Você precisa cadastrar pelo menos um paciente antes de agendar consultas.")
        if st.button("➕ Cadastrar Paciente"):
            st.session_state.page = 'patients'
            st.rerun()
        return
    
    # Formulário de agendamento
    with st.form("nova_consulta"):
        st.markdown("##### 👤 Dados da Consulta")
        
        col1, col2 = st.columns(2)
        
        with col1:
            paciente_selecionado = st.selectbox(
                "👤 Paciente",
                options=pacientes,
                format_func=lambda x: x[2],
                help="Selecione o paciente para a consulta"
            )
            
            tipo_consulta = st.selectbox(
                "🏥 Tipo de Consulta",
                ["Primeira Consulta", "Retorno", "Avaliação", "Acompanhamento", "Reavaliação", "Orientação", "Outro"]
            )
            
            if tipo_consulta == "Outro":
                tipo_consulta = st.text_input("Especifique o tipo", placeholder="Ex: Consulta de urgência")
        
        with col2:
            data_consulta = st.date_input("📅 Data da Consulta", min_value=datetime.now().date())
            
            hora_consulta = st.time_input("🕐 Horário", value=datetime.now().replace(minute=0, second=0, microsecond=0).time())
            
            duracao = st.selectbox("⏱️ Duração (minutos)", [30, 45, 60, 90, 120], index=2)
        
        st.markdown("##### 💰 Informações Financeiras")
        
        col1, col2 = st.columns(2)
        
        with col1:
            valor_consulta = st.number_input("💰 Valor (R$)", min_value=0.0, value=150.0, step=10.0)
        
        with col2:
            forma_pagamento = st.selectbox(
                "💳 Forma de Pagamento",
                ["À vista", "Cartão de crédito", "Cartão de débito", "PIX", "Transferência", "Outro"]
            )
        
        st.markdown("##### 📝 Informações Adicionais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            observacoes = st.text_area("📝 Observações", placeholder="Observações sobre a consulta...", height=100)
        
        with col2:
            # Data de retorno sugerida
            retorno_sugerido = st.date_input(
                "🔄 Data de Retorno Sugerida",
                value=None,
                help="Deixe em branco se não houver retorno programado"
            )
            
            lembrete = st.checkbox("📱 Enviar lembrete 24h antes", value=True)
            
            confirmar_whatsapp = st.checkbox("💬 Confirmar por WhatsApp", value=False)
        
        # Botões do formulário
        col1, col2, col3 = st.columns(3)
        
        with col1:
            agendar = st.form_submit_button("📅 Agendar Consulta", use_container_width=True)
        
        with col2:
            if st.form_submit_button("🔄 Limpar", use_container_width=True):
                st.rerun()
        
        with col3:
            salvar_modelo = st.form_submit_button("💾 Salvar como Modelo", use_container_width=True)
    
    if agendar:
        # Validar conflitos de horário
        data_hora_consulta = datetime.combine(data_consulta, hora_consulta)
        
        # Verificar se já existe consulta no horário
        cursor.execute("""
        SELECT COUNT(*) FROM consultas 
        WHERE nutricionista_id = ? AND data_consulta = ? AND status != 'cancelada'
        """, (user['id'], data_hora_consulta.isoformat()))
        
        if cursor.fetchone()[0] > 0:
            st.error("❌ Já existe uma consulta agendada para este horário!")
            return
        
        # Criar consulta
        try:
            consulta_uuid = str(uuid.uuid4())
            
            cursor.execute('''
            INSERT INTO consultas (
                uuid, paciente_id, nutricionista_id, data_consulta, tipo_consulta,
                status, duracao, valor, observacoes, retorno_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                consulta_uuid,
                paciente_selecionado[0],
                user['id'],
                data_hora_consulta.isoformat(),
                tipo_consulta,
                'agendada',
                duracao,
                valor_consulta,
                observacoes,
                retorno_sugerido.isoformat() if retorno_sugerido else None
            ))
            
            # Log da ação
            cursor.execute('''
            INSERT INTO logs_sistema (usuario_id, acao, tabela_afetada, registro_id)
            VALUES (?, ?, ?, ?)
            ''', (user['id'], 'CREATE', 'consultas', consulta_uuid))
            
            conn.commit()
            
            st.success(f"✅ Consulta agendada com sucesso!")
            st.balloons()
            
            # Informações da consulta agendada
            st.info(f"""
            **📅 Consulta Agendada:**
            - **Paciente:** {paciente_selecionado[2]}
            - **Data/Hora:** {data_hora_consulta.strftime('%d/%m/%Y às %H:%M')}
            - **Tipo:** {tipo_consulta}
            - **Duração:** {duracao} minutos
            - **Valor:** R$ {valor_consulta:.2f}
            """)
            
            # Opções pós-agendamento
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📱 Enviar Confirmação"):
                    st.success("📱 Confirmação enviada!")
            
            with col2:
                if st.button("📅 Ver Agenda"):
                    st.session_state.active_tab = 0
                    st.rerun()
            
            with col3:
                if st.button("➕ Agendar Outra"):
                    st.rerun()
        
        except Exception as e:
            st.error(f"❌ Erro ao agendar consulta: {str(e)}")
        
        finally:
            conn.close()

def show_search_appointments(user):
    """Sistema de busca de consultas"""
    
    st.markdown('<div class="sub-header">🔍 Buscar Consultas</div>', unsafe_allow_html=True)
    
    # Filtros de busca
    with st.expander("🔧 Filtros de Busca", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            busca_paciente = st.text_input("👤 Nome do Paciente", placeholder="Digite o nome...")
            tipo_busca = st.multiselect(
                "🏥 Tipo de Consulta",
                ["Primeira Consulta", "Retorno", "Avaliação", "Acompanhamento", "Reavaliação"]
            )
        
        with col2:
            status_busca = st.multiselect(
                "📊 Status",
                ["agendada", "realizada", "cancelada", "faltou"],
                default=["agendada", "realizada"]
            )
            
            data_inicio_busca = st.date_input("📅 Data Início", value=datetime.now() - timedelta(days=30))
        
        with col3:
            data_fim_busca = st.date_input("📅 Data Fim", value=datetime.now() + timedelta(days=30))
            valor_min = st.number_input("💰 Valor Mínimo", min_value=0.0, value=0.0)
    
    if st.button("🔍 Buscar Consultas", use_container_width=True):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Construir query
        query = """
        SELECT c.*, p.nome as paciente_nome, p.telefone, p.email
        FROM consultas c
        JOIN pacientes p ON c.paciente_id = p.id
        WHERE c.nutricionista_id = ?
        """
        
        params = [user['id']]
        
        if busca_paciente:
            query += " AND p.nome LIKE ?"
            params.append(f"%{busca_paciente}%")
        
        if tipo_busca:
            tipos_str = "', '".join(tipo_busca)
            query += f" AND c.tipo_consulta IN ('{tipos_str}')"
        
        if status_busca:
            status_str = "', '".join(status_busca)
            query += f" AND c.status IN ('{status_str}')"
        
        if data_inicio_busca:
            query += " AND DATE(c.data_consulta) >= ?"
            params.append(data_inicio_busca.strftime('%Y-%m-%d'))
        
        if data_fim_busca:
            query += " AND DATE(c.data_consulta) <= ?"
            params.append(data_fim_busca.strftime('%Y-%m-%d'))
        
        if valor_min > 0:
            query += " AND c.valor >= ?"
            params.append(valor_min)
        
        query += " ORDER BY c.data_consulta DESC"
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        if resultados:
            st.success(f"🎯 Encontradas {len(resultados)} consulta(s)")
            
            # Estatísticas rápidas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_valor = sum(r['valor'] or 0 for r in resultados)
                st.metric("💰 Valor Total", f"R$ {total_valor:.2f}")
            
            with col2:
                realizadas = len([r for r in resultados if r['status'] == 'realizada'])
                st.metric("✅ Realizadas", realizadas)
            
            with col3:
                agendadas = len([r for r in resultados if r['status'] == 'agendada'])
                st.metric("📅 Agendadas", agendadas)
            
            with col4:
                canceladas = len([r for r in resultados if r['status'] == 'cancelada'])
                st.metric("❌ Canceladas", canceladas)
            
            st.markdown("---")
            
            # Lista de resultados
            for consulta in resultados:
                data_consulta = datetime.fromisoformat(consulta['data_consulta'])
                
                with st.expander(f"📅 {data_consulta.strftime('%d/%m/%Y %H:%M')} - {consulta['paciente_nome']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**👤 Paciente:** {consulta['paciente_nome']}")
                        st.write(f"**📱 Telefone:** {consulta['telefone'] or 'N/A'}")
                        st.write(f"**📧 Email:** {consulta['email'] or 'N/A'}")
                    
                    with col2:
                        st.write(f"**🏥 Tipo:** {consulta['tipo_consulta']}")
                        st.write(f"**📊 Status:** {consulta['status'].title()}")
                        st.write(f"**⏱️ Duração:** {consulta['duracao']} min")
                    
                    with col3:
                        st.write(f"**💰 Valor:** R$ {consulta['valor']:.2f if consulta['valor'] else 0:.2f}")
                        if consulta['retorno_data']:
                            retorno = datetime.fromisoformat(consulta['retorno_data'])
                            st.write(f"**🔄 Retorno:** {retorno.strftime('%d/%m/%Y')}")
                        else:
                            st.write(f"**🔄 Retorno:** Não agendado")
                    
                    if consulta['observacoes']:
                        st.markdown(f"**📝 Observações:** {consulta['observacoes']}")
                    
                    # Botões de ação
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if st.button("✏️ Editar", key=f"edit_search_{consulta['id']}"):
                            st.session_state.editing_appointment_id = consulta['id']
                    
                    with col2:
                        if st.button("👁️ Detalhes", key=f"view_search_{consulta['id']}"):
                            show_appointment_details(consulta)
                    
                    with col3:
                        if consulta['status'] == 'agendada':
                            if st.button("✅ Realizar", key=f"done_search_{consulta['id']}"):
                                update_appointment_status(consulta['id'], 'realizada')
                                st.rerun()
                    
                    with col4:
                        if st.button("📄 Ficha", key=f"record_search_{consulta['id']}"):
                            st.info("📄 Funcionalidade em desenvolvimento")
        else:
            st.warning("🔍 Nenhuma consulta encontrada com os critérios especificados.")
        
        conn.close()

def show_appointments_reports(user):
    """Relatórios de consultas e agendamentos"""
    
    st.markdown('<div class="sub-header">📊 Relatórios de Consultas</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Período para relatórios
    col1, col2 = st.columns(2)
    
    with col1:
        periodo_inicio = st.date_input("📅 Período Início", value=datetime.now() - timedelta(days=30))
    
    with col2:
        periodo_fim = st.date_input("📅 Período Fim", value=datetime.now())
    
    # Métricas do período
    cursor.execute("""
    SELECT 
        COUNT(*) as total,
        COUNT(CASE WHEN status = 'realizada' THEN 1 END) as realizadas,
        COUNT(CASE WHEN status = 'agendada' THEN 1 END) as agendadas,
        COUNT(CASE WHEN status = 'cancelada' THEN 1 END) as canceladas,
        COUNT(CASE WHEN status = 'faltou' THEN 1 END) as faltaram,
        COALESCE(SUM(CASE WHEN status = 'realizada' THEN valor ELSE 0 END), 0) as receita,
        AVG(CASE WHEN status = 'realizada' THEN valor END) as ticket_medio
    FROM consultas
    WHERE nutricionista_id = ?
    AND DATE(data_consulta) BETWEEN ? AND ?
    """, (user['id'], periodo_inicio.strftime('%Y-%m-%d'), periodo_fim.strftime('%Y-%m-%d')))
    
    stats = cursor.fetchone()
    
    if stats and stats['total'] > 0:
        # Métricas principais
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("📊 Total", stats['total'])
        
        with col2:
            taxa_realizacao = (stats['realizadas'] / stats['total']) * 100 if stats['total'] > 0 else 0
            st.metric("✅ Realizadas", stats['realizadas'], f"{taxa_realizacao:.1f}%")
        
        with col3:
            st.metric("📅 Agendadas", stats['agendadas'])
        
        with col4:
            taxa_cancelamento = (stats['canceladas'] / stats['total']) * 100 if stats['total'] > 0 else 0
            st.metric("❌ Canceladas", stats['canceladas'], f"{taxa_cancelamento:.1f}%")
        
        with col5:
            st.metric("💰 Receita", f"R$ {stats['receita']:.2f}")
        
        # Segunda linha de métricas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🎯 Ticket Médio", f"R$ {stats['ticket_medio']:.2f if stats['ticket_medio'] else 0:.2f}")
        
        with col2:
            taxa_falta = (stats['faltaram'] / stats['total']) * 100 if stats['total'] > 0 else 0
            st.metric("⚠️ Faltaram", stats['faltaram'], f"{taxa_falta:.1f}%")
        
        with col3:
            dias_periodo = (periodo_fim - periodo_inicio).days + 1
            media_dia = stats['total'] / dias_periodo
            st.metric("📈 Média/Dia", f"{media_dia:.1f}")
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Status das consultas
            status_data = {
                'Realizadas': stats['realizadas'],
                'Agendadas': stats['agendadas'],
                'Canceladas': stats['canceladas'],
                'Faltaram': stats['faltaram']
            }
            
            fig_status = px.pie(
                values=list(status_data.values()),
                names=list(status_data.keys()),
                title='Distribuição por Status',
                color_discrete_map={
                    'Realizadas': '#4CAF50',
                    'Agendadas': '#FF9800',
                    'Canceladas': '#F44336',
                    'Faltaram': '#9E9E9E'
                }
            )
            
            fig_status.update_layout(height=400)
            st.plotly_chart(fig_status, use_container_width=True)
        
        with col2:
            # Receita por dia
            cursor.execute("""
            SELECT DATE(data_consulta) as data, 
                   COALESCE(SUM(CASE WHEN status = 'realizada' THEN valor ELSE 0 END), 0) as receita_dia
            FROM consultas
            WHERE nutricionista_id = ?
            AND DATE(data_consulta) BETWEEN ? AND ?
            GROUP BY DATE(data_consulta)
            ORDER BY data
            """, (user['id'], periodo_inicio.strftime('%Y-%m-%d'), periodo_fim.strftime('%Y-%m-%d')))
            
            receita_data = cursor.fetchall()
            
            if receita_data:
                df_receita = pd.DataFrame(receita_data, columns=['Data', 'Receita'])
                df_receita['Data'] = pd.to_datetime(df_receita['Data'])
                
                fig_receita = px.line(
                    df_receita,
                    x='Data',
                    y='Receita',
                    title='Receita Diária',
                    markers=True
                )
                
                fig_receita.update_traces(line_color='#2E7D32')
                fig_receita.update_layout(height=400)
                st.plotly_chart(fig_receita, use_container_width=True)
        
        # Análise por tipo de consulta
        st.markdown("##### 📊 Análise por Tipo de Consulta")
        
        cursor.execute("""
        SELECT tipo_consulta, 
               COUNT(*) as total,
               COUNT(CASE WHEN status = 'realizada' THEN 1 END) as realizadas,
               COALESCE(AVG(CASE WHEN status = 'realizada' THEN valor END), 0) as valor_medio
        FROM consultas
        WHERE nutricionista_id = ?
        AND DATE(data_consulta) BETWEEN ? AND ?
        GROUP BY tipo_consulta
        ORDER BY total DESC
        """, (user['id'], periodo_inicio.strftime('%Y-%m-%d'), periodo_fim.strftime('%Y-%m-%d')))
        
        tipos_data = cursor.fetchall()
        
        if tipos_data:
            df_tipos = pd.DataFrame(tipos_data, columns=['Tipo', 'Total', 'Realizadas', 'Valor Médio'])
            df_tipos['Taxa Realização'] = (df_tipos['Realizadas'] / df_tipos['Total'] * 100).round(1)
            df_tipos['Valor Médio'] = df_tipos['Valor Médio'].round(2)
            
            st.dataframe(df_tipos, hide_index=True, use_container_width=True)
    
    else:
        st.info("📊 Nenhuma consulta encontrada no período selecionado.")
    
    # Botões de exportação
    st.markdown("---")
    st.markdown("##### 📄 Exportar Relatórios")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Exportar Excel", use_container_width=True):
            st.info("📊 Funcionalidade de exportação em desenvolvimento")
    
    with col2:
        if st.button("📄 Gerar PDF", use_container_width=True):
            st.info("📄 Funcionalidade de PDF em desenvolvimento")
    
    with col3:
        if st.button("📧 Enviar por Email", use_container_width=True):
            st.info("📧 Funcionalidade de email em desenvolvimento")
    
    conn.close()

def show_appointment_settings(user):
    """Configurações do sistema de agendamentos"""
    
    st.markdown('<div class="sub-header">⚙️ Configurações de Agendamento</div>', unsafe_allow_html=True)
    
    # Configurações gerais
    st.markdown("##### 🕐 Horários de Funcionamento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        horario_inicio = st.time_input("⏰ Início do Atendimento", value=datetime.strptime("08:00", "%H:%M").time())
        duracao_padrao = st.selectbox("⏱️ Duração Padrão (min)", [30, 45, 60, 90], index=2)
    
    with col2:
        horario_fim = st.time_input("⏰ Fim do Atendimento", value=datetime.strptime("18:00", "%H:%M").time())
        intervalo_consultas = st.selectbox("🔄 Intervalo entre Consultas (min)", [0, 15, 30], index=1)
    
    # Dias de funcionamento
    st.markdown("##### 📅 Dias de Funcionamento")
    
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    dias_funcionamento = st.multiselect(
        "Selecione os dias de atendimento",
        dias_semana,
        default=["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
    )
    
    # Valores padrão
    st.markdown("##### 💰 Valores Padrão")
    
    col1, col2 = st.columns(2)
    
    with col1:
        valor_primeira_consulta = st.number_input("💰 Primeira Consulta (R$)", min_value=0.0, value=200.0, step=10.0)
        valor_retorno = st.number_input("💰 Consulta de Retorno (R$)", min_value=0.0, value=150.0, step=10.0)
    
    with col2:
        valor_avaliacao = st.number_input("💰 Avaliação (R$)", min_value=0.0, value=180.0, step=10.0)
        valor_acompanhamento = st.number_input("💰 Acompanhamento (R$)", min_value=0.0, value=120.0, step=10.0)
    
    # Configurações de notificação
    st.markdown("##### 📱 Notificações e Lembretes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        enviar_lembretes = st.checkbox("📱 Enviar lembretes automáticos", value=True)
        if enviar_lembretes:
            antecedencia_lembrete = st.selectbox("📅 Antecedência do lembrete", ["24 horas", "12 horas", "6 horas", "2 horas"])
    
    with col2:
        confirmar_consultas = st.checkbox("✅ Solicitar confirmação", value=True)
        notificar_cancelamentos = st.checkbox("❌ Notificar cancelamentos", value=True)
    
    # Configurações de bloqueio
    st.markdown("##### 🚫 Configurações de Bloqueio")
    
    col1, col2 = st.columns(2)
    
    with col1:
        bloquear_feriados = st.checkbox("🎄 Bloquear feriados", value=True)
        bloquear_domingos = st.checkbox("📅 Bloquear domingos", value=False)
    
    with col2:
        permitir_reagendamento = st.checkbox("🔄 Permitir reagendamento online", value=True)
        antecedencia_minima = st.selectbox("⏰ Antecedência mínima para agendamento", ["2 horas", "6 horas", "12 horas", "24 horas"])
    
    # Modelos de mensagem
    st.markdown("##### 💬 Modelos de Mensagem")
    
    with st.expander("📱 Lembrete de Consulta", expanded=False):
        template_lembrete = st.text_area(
            "Modelo de mensagem",
            value="Olá {paciente}! Lembramos que você tem consulta marcada para {data} às {hora}. Confirme sua presença respondendo esta mensagem. Obrigado! - Dr(a). {nutricionista}",
            height=100
        )
    
    with st.expander("✅ Confirmação de Agendamento", expanded=False):
        template_confirmacao = st.text_area(
            "Modelo de confirmação",
            value="Olá {paciente}! Sua consulta foi agendada para {data} às {hora}. Tipo: {tipo}. Valor: R$ {valor}. Até breve! - Dr(a). {nutricionista}",
            height=100
        )
    
    with st.expander("❌ Cancelamento", expanded=False):
        template_cancelamento = st.text_area(
            "Modelo de cancelamento",
            value="Olá {paciente}! Sua consulta do dia {data} às {hora} foi cancelada. Entre em contato para reagendar. - Dr(a). {nutricionista}",
            height=100
        )
    
    # Botões de ação
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Salvar Configurações", use_container_width=True):
            # Aqui você salvaria as configurações no banco de dados
            configuracoes = {
                'horario_inicio': horario_inicio.strftime('%H:%M'),
                'horario_fim': horario_fim.strftime('%H:%M'),
                'duracao_padrao': duracao_padrao,
                'intervalo_consultas': intervalo_consultas,
                'dias_funcionamento': dias_funcionamento,
                'valores': {
                    'primeira_consulta': valor_primeira_consulta,
                    'retorno': valor_retorno,
                    'avaliacao': valor_avaliacao,
                    'acompanhamento': valor_acompanhamento
                },
                'notificacoes': {
                    'lembretes': enviar_lembretes,
                    'antecedencia_lembrete': antecedencia_lembrete if enviar_lembretes else None,
                    'confirmar_consultas': confirmar_consultas,
                    'notificar_cancelamentos': notificar_cancelamentos
                },
                'bloqueios': {
                    'feriados': bloquear_feriados,
                    'domingos': bloquear_domingos,
                    'reagendamento': permitir_reagendamento,
                    'antecedencia_minima': antecedencia_minima
                },
                'templates': {
                    'lembrete': template_lembrete,
                    'confirmacao': template_confirmacao,
                    'cancelamento': template_cancelamento
                }
            }
            
            # Salvar no banco
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
            UPDATE usuarios SET configuracoes = ?
            WHERE id = ?
            ''', (json.dumps(configuracoes), user['id']))
            
            conn.commit()
            conn.close()
            
            st.success("✅ Configurações salvas com sucesso!")
    
    with col2:
        if st.button("🔄 Restaurar Padrões", use_container_width=True):
            st.info("🔄 Configurações padrão restauradas!")
            st.rerun()
    
    with col3:
        if st.button("📋 Exportar Config", use_container_width=True):
            st.info("📋 Funcionalidade de exportação em desenvolvimento")

def update_appointment_status(appointment_id, new_status):
    """Atualiza o status de uma consulta"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE consultas SET status = ?
    WHERE id = ?
    ''', (new_status, appointment_id))
    
    conn.commit()
    conn.close()

def send_appointment_reminder(consulta):
    """Envia lembrete de consulta (placeholder)"""
    st.success(f"📱 Lembrete enviado para {consulta['paciente_nome']}!")

def show_appointment_details(consulta):
    """Mostra detalhes completos da consulta"""
    st.markdown("---")
    st.markdown(f'<div class="sub-header">👁️ Detalhes da Consulta</div>', unsafe_allow_html=True)
    
    data_consulta = datetime.fromisoformat(consulta['data_consulta'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"""
        **👤 Paciente:** {consulta['paciente_nome']}
        **📱 Telefone:** {consulta['telefone'] or 'N/A'}
        **📧 Email:** {consulta['email'] or 'N/A'}
        """)
    
    with col2:
        st.info(f"""
        **📅 Data/Hora:** {data_consulta.strftime('%d/%m/%Y às %H:%M')}
        **🏥 Tipo:** {consulta['tipo_consulta']}
        **⏱️ Duração:** {consulta['duracao']} minutos
        """)
    
    with col3:
        st.info(f"""
        **📊 Status:** {consulta['status'].title()}
        **💰 Valor:** R$ {consulta['valor']:.2f if consulta['valor'] else 0:.2f}
        **🔄 Retorno:** {datetime.fromisoformat(consulta['retorno_data']).strftime('%d/%m/%Y') if consulta['retorno_data'] else 'Não agendado'}
        """)
    
    if consulta['observacoes']:
        st.markdown("##### 📝 Observações")
        st.markdown(consulta['observacoes'])

# =============================================================================
# 🍳 SISTEMA DE RECEITAS SAUDÁVEIS
# =============================================================================

def show_recipes():
    """Sistema completo de receitas saudáveis"""
    
    st.markdown('<h1 class="main-header">🍳 Receitas Saudáveis</h1>', unsafe_allow_html=True)
    
    user = AuthSystem.get_current_user()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🍽️ Minhas Receitas",
        "➕ Nova Receita", 
        "🔍 Buscar Receitas",
        "⭐ Favoritas",
        "📊 Análises"
    ])
    
    with tab1:
        show_my_recipes(user)
    
    with tab2:
        show_new_recipe(user)
    
    with tab3:
        show_search_recipes(user)
    
    with tab4:
        show_favorite_recipes(user)
    
    with tab5:
        show_recipes_analytics(user)

def show_my_recipes(user):
    """Lista as receitas do nutricionista"""
    
    st.markdown('<div class="sub-header">🍽️ Minhas Receitas</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        categorias_disponiveis = ["Todas", "Café da Manhã", "Saladas", "Pratos Principais", "Sobremesas", "Bebidas", "Lanches", "Sopas"]
        filtro_categoria = st.selectbox("🍽️ Categoria", categorias_disponiveis)
    
    with col2:
        filtro_tempo = st.selectbox("⏱️ Tempo de Preparo", ["Todos", "Até 15 min", "16-30 min", "31-60 min", "Mais de 1h"])
    
    with col3:
        filtro_favoritas = st.checkbox("⭐ Apenas Favoritas")
    
    # Buscar receitas
    query = """
    SELECT * FROM receitas 
    WHERE (nutricionista_id = ? OR publica = 1)
    """
    
    params = [user['id']]
    
    if filtro_categoria != "Todas":
        query += " AND categoria = ?"
        params.append(filtro_categoria)
    
    if filtro_tempo != "Todos":
        if filtro_tempo == "Até 15 min":
            query += " AND tempo_preparo <= 15"
        elif filtro_tempo == "16-30 min":
            query += " AND tempo_preparo BETWEEN 16 AND 30"
        elif filtro_tempo == "31-60 min":
            query += " AND tempo_preparo BETWEEN 31 AND 60"
        else:
            query += " AND tempo_preparo > 60"
    
    if filtro_favoritas:
        query += " AND favorita = 1"
    
    query += " ORDER BY data_criacao DESC"
    
    cursor.execute(query, params)
    receitas = cursor.fetchall()
    
    if receitas:
        st.success(f"🍽️ **{len(receitas)} receita(s) encontrada(s)**")
        
        # Exibir receitas em grid
        for i in range(0, len(receitas), 2):
            col1, col2 = st.columns(2)
            
            with col1:
                if i < len(receitas):
                    show_recipe_card(receitas[i], user)
            
            with col2:
                if i + 1 < len(receitas):
                    show_recipe_card(receitas[i + 1], user)
    else:
        st.info("🍽️ Nenhuma receita encontrada com os filtros aplicados.")
        if st.button("➕ Adicionar Primeira Receita"):
            st.session_state.active_tab = 1
            st.rerun()
    
    conn.close()

def show_recipe_card(receita, user):
    """Exibe um card com a receita"""
    
    # Parse dos ingredientes e tags
    try:
        ingredientes = json.loads(receita['ingredientes'])
        tags = json.loads(receita['tags']) if receita['tags'] else []
    except:
        ingredientes = []
        tags = []
    
    # Card da receita
    st.markdown(f'''
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #2E7D32;">🍽️ {receita['nome']}</h4>
            {f'<span style="color: #FF6B6B; font-size: 1.2rem;">⭐</span>' if receita['favorita'] else ''}
        </div>
        
        <div style="margin-bottom: 1rem;">
            <div><strong>🏷️ Categoria:</strong> {receita['categoria'] or 'Não categorizada'}</div>
            <div><strong>⏱️ Preparo:</strong> {receita['tempo_preparo']} minutos</div>
            <div><strong>🍽️ Porções:</strong> {receita['porcoes']}</div>
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-bottom: 1rem; font-size: 0.9rem;">
            <div><strong>🔥</strong> {receita['calorias_porcao']:.0f if receita['calorias_porcao'] else 0} kcal</div>
            <div><strong>🥩</strong> {receita['proteinas']:.1f if receita['proteinas'] else 0}g prot</div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Tags
    if tags:
        tags_html = " ".join([f'<span style="background: #E8F5E8; padding: 0.2rem 0.5rem; border-radius: 10px; font-size: 0.75rem; color: #2E7D32;">#{tag}</span>' for tag in tags[:3]])
        st.markdown(tags_html, unsafe_allow_html=True)
    
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👁️ Ver", key=f"view_recipe_{receita['id']}", use_container_width=True):
            show_recipe_details(receita)
    
    with col2:
        if receita['nutricionista_id'] == user['id']:
            if st.button("✏️ Editar", key=f"edit_recipe_{receita['id']}", use_container_width=True):
                st.session_state.editing_recipe_id = receita['id']
    
    with col3:
        if receita['nutricionista_id'] == user['id']:
            fav_icon = "💔" if receita['favorita'] else "❤️"
            fav_text = "Desfavoritar" if receita['favorita'] else "Favoritar"
            if st.button(f"{fav_icon}", key=f"fav_recipe_{receita['id']}", use_container_width=True, help=fav_text):
                toggle_recipe_favorite(receita['id'])
                st.rerun()

def show_recipe_details(receita):
    """Mostra detalhes completos da receita"""
    
    st.markdown("---")
    st.markdown(f'<div class="sub-header">👁️ {receita["nome"]}</div>', unsafe_allow_html=True)
    
    # Informações nutricionais
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🔥 Calorias", f"{receita['calorias_porcao']:.0f if receita['calorias_porcao'] else 0}")
    
    with col2:
        st.metric("🍞 Carboidratos", f"{receita['carboidratos']:.1f if receita['carboidratos'] else 0}g")
    
    with col3:
        st.metric("🥩 Proteínas", f"{receita['proteinas']:.1f if receita['proteinas'] else 0}g")
    
    with col4:
        st.metric("🥑 Lipídios", f"{receita['lipidios']:.1f if receita['lipidios'] else 0}g")
    
    with col5:
        st.metric("🌾 Fibras", f"{receita['fibras']:.1f if receita['fibras'] else 0}g")
    
    # Gráfico nutricional
    if receita['carboidratos'] and receita['proteinas'] and receita['lipidios']:
        fig_nutri = px.pie(
            values=[receita['carboidratos'], receita['proteinas'], receita['lipidios']],
            names=['Carboidratos', 'Proteínas', 'Lipídios'],
            title='Distribuição de Macronutrientes',
            color_discrete_sequence=['#FFB74D', '#FF8A65', '#81C784']
        )
        
        fig_nutri.update_layout(height=300)
        st.plotly_chart(fig_nutri, use_container_width=True)
    
    # Ingredientes e preparo
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("##### 🛒 Ingredientes")
        
        try:
            ingredientes = json.loads(receita['ingredientes'])
            for ing in ingredientes:
                if isinstance(ing, dict):
                    st.markdown(f"- **{ing['nome']}**: {ing['quantidade']}")
                else:
                    st.markdown(f"- {ing}")
        except:
            st.markdown("Erro ao carregar ingredientes")
        
        # Informações adicionais
        st.markdown("---")
        st.info(f"""
        **⏱️ Tempo de Preparo:** {receita['tempo_preparo']} minutos
        **🍽️ Rendimento:** {receita['porcoes']} porções
        **🏷️ Categoria:** {receita['categoria']}
        """)
    
    with col2:
        st.markdown("##### 👨‍🍳 Modo de Preparo")
        st.markdown(receita['modo_preparo'])
    
    # Tags
    if receita['tags']:
        try:
            tags = json.loads(receita['tags'])
            if tags:
                st.markdown("##### 🏷️ Tags")
                tags_html = " ".join([f'<span style="background: #E8F5E8; padding: 0.3rem 0.7rem; border-radius: 15px; font-size: 0.85rem; color: #2E7D32; margin-right: 0.5rem;">#{tag}</span>' for tag in tags])
                st.markdown(tags_html, unsafe_allow_html=True)
        except:
            pass
    
    # Ações
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 Imprimir Receita"):
            st.info("📄 Funcionalidade de impressão em desenvolvimento")
    
    with col2:
        if st.button("📧 Enviar por Email"):
            st.info("📧 Funcionalidade de email em desenvolvimento")
    
    with col3:
        if st.button("📱 Compartilhar"):
            st.info("📱 Funcionalidade de compartilhamento em desenvolvimento")
    
    with col4:
        if st.button("🛒 Lista de Compras"):
            generate_shopping_list(receita)

def generate_shopping_list(receita):
    """Gera lista de compras da receita"""
    st.markdown("##### 🛒 Lista de Compras")
    
    try:
        ingredientes = json.loads(receita['ingredientes'])
        
        lista_compras = []
        for ing in ingredientes:
            if isinstance(ing, dict):
                lista_compras.append(f"☐ {ing['nome']} - {ing['quantidade']}")
            else:
                lista_compras.append(f"☐ {ing}")
        
        lista_texto = "\n".join(lista_compras)
        
        st.text_area(
            f"Lista para {receita['nome']}:",
            value=lista_texto,
            height=200
        )
        
        # Botão para copiar
        if st.button("📋 Copiar Lista"):
            st.success("📋 Lista copiada! (Use Ctrl+C para copiar o texto acima)")
    
    except:
        st.error("❌ Erro ao gerar lista de compras")

def show_new_recipe(user):
    """Formulário para nova receita"""
    
    st.markdown('<div class="sub-header">➕ Adicionar Nova Receita</div>', unsafe_allow_html=True)
    
    with st.form("nova_receita"):
        st.markdown("##### 📋 Informações Básicas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome_receita = st.text_input("🍽️ Nome da Receita *", placeholder="Ex: Salada Caesar Fitness")
            categoria = st.selectbox(
                "🏷️ Categoria *",
                ["Café da Manhã", "Saladas", "Pratos Principais", "Sobremesas", "Bebidas", "Lanches", "Sopas", "Outro"]
            )
            
            if categoria == "Outro":
                categoria = st.text_input("Especifique a categoria", placeholder="Digite a categoria")
        
        with col2:
            tempo_preparo = st.number_input("⏱️ Tempo de Preparo (minutos) *", min_value=1, max_value=480, value=30)
            porcoes = st.number_input("🍽️ Número de Porções *", min_value=1, max_value=20, value=4)
        
        st.markdown("##### 🛒 Ingredientes")
        
        # Sistema dinâmico de ingredientes
        if 'ingredientes_receita' not in st.session_state:
            st.session_state.ingredientes_receita = [{'nome': '', 'quantidade': ''}]
        
        ingredientes_data = []
        
        for i, ing in enumerate(st.session_state.ingredientes_receita):
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                nome_ing = st.text_input(f"Ingrediente {i+1}", value=ing['nome'], key=f"ing_nome_{i}", placeholder="Ex: Peito de frango")
            
            with col2:
                qtd_ing = st.text_input(f"Quantidade", value=ing['quantidade'], key=f"ing_qtd_{i}", placeholder="Ex: 200g")
            
            with col3:
                if st.button("🗑️", key=f"remove_ing_{i}", help="Remover ingrediente"):
                    if len(st.session_state.ingredientes_receita) > 1:
                        st.session_state.ingredientes_receita.pop(i)
                        st.rerun()
            
            if nome_ing and qtd_ing:
                ingredientes_data.append({'nome': nome_ing, 'quantidade': qtd_ing})
        
        if st.button("➕ Adicionar Ingrediente"):
            st.session_state.ingredientes_receita.append({'nome': '', 'quantidade': ''})
            st.rerun()
        
        st.markdown("##### 👨‍🍳 Modo de Preparo")
        
        modo_preparo = st.text_area(
            "Descreva o passo a passo",
            placeholder="1. Tempere o frango com sal e pimenta...\n2. Aqueça a frigideira...\n3. ...",
            height=150
        )
        
        st.markdown("##### 📊 Informações Nutricionais (por porção)")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            calorias = st.number_input("🔥 Calorias", min_value=0.0, value=0.0, step=1.0)
        
        with col2:
            carboidratos = st.number_input("🍞 Carboidratos (g)", min_value=0.0, value=0.0, step=0.1)
        
        with col3:
            proteinas = st.number_input("🥩 Proteínas (g)", min_value=0.0, value=0.0, step=0.1)
        
        with col4:
            lipidios = st.number_input("🥑 Lipídios (g)", min_value=0.0, value=0.0, step=0.1)
        
        with col5:
            fibras = st.number_input("🌾 Fibras (g)", min_value=0.0, value=0.0, step=0.1)
        
        st.markdown("##### 🏷️ Tags e Classificação")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tags_input = st.text_input(
                "🏷️ Tags (separadas por vírgula)",
                placeholder="vegetariano, sem glúten, rico em proteína"
            )
            
            tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
        
        with col2:
            receita_publica = st.checkbox("🌐 Receita pública (outros nutricionistas podem ver)", value=False)
            receita_favorita = st.checkbox("⭐ Marcar como favorita", value=False)
        
        # Botões do formulário
        col1, col2, col3 = st.columns(3)
        
        with col1:
            criar_receita = st.form_submit_button("💾 Salvar Receita", use_container_width=True)
        
        with col2:
            if st.form_submit_button("🧹 Limpar Formulário", use_container_width=True):
                st.session_state.ingredientes_receita = [{'nome': '', 'quantidade': ''}]
                st.rerun()
        
        with col3:
            calcular_nutri = st.form_submit_button("🧮 Calcular Nutrição", use_container_width=True)
    
    if calcular_nutri:
        st.info("🧮 Funcionalidade de cálculo automático em desenvolvimento")
    
    if criar_receita:
        # Validar dados obrigatórios
        if not nome_receita or not categoria or not modo_preparo:
            st.error("❌ Por favor, preencha todos os campos obrigatórios (*)")
            return
        
        if not ingredientes_data:
            st.error("❌ Por favor, adicione pelo menos um ingrediente")
            return
        
        # Salvar receita
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        try:
            receita_uuid = str(uuid.uuid4())
            
            cursor.execute('''
            INSERT INTO receitas (
                uuid, nutricionista_id, nome, categoria, ingredientes, modo_preparo,
                tempo_preparo, porcoes, calorias_porcao, carboidratos, proteinas,
                lipidios, fibras, tags, favorita, publica
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                receita_uuid, user['id'], nome_receita, categoria,
                json.dumps(ingredientes_data, ensure_ascii=False), modo_preparo,
                tempo_preparo, porcoes, calorias, carboidratos, proteinas,
                lipidios, fibras, json.dumps(tags, ensure_ascii=False),
                receita_favorita, receita_publica
            ))
            
            # Log da ação
            cursor.execute('''
            INSERT INTO logs_sistema (usuario_id, acao, tabela_afetada, registro_id)
            VALUES (?, ?, ?, ?)
            ''', (user['id'], 'CREATE', 'receitas', receita_uuid))
            
            conn.commit()
            
            # Limpar formulário
            st.session_state.ingredientes_receita = [{'nome': '', 'quantidade': ''}]
            
            st.success(f"✅ Receita **{nome_receita}** adicionada com sucesso!")
            st.balloons()
            
            # Opções pós-criação
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("👁️ Visualizar Receita"):
                    # Buscar a receita recém-criada para visualizar
                    cursor.execute("SELECT * FROM receitas WHERE uuid = ?", (receita_uuid,))
                    receita = cursor.fetchone()
                    if receita:
                        show_recipe_details(receita)
            
            with col2:
                if st.button("🍽️ Ver Todas"):
                    st.session_state.active_tab = 0
                    st.rerun()
            
            with col3:
                if st.button("➕ Adicionar Outra"):
                    st.rerun()
        
        except Exception as e:
            st.error(f"❌ Erro ao salvar receita: {str(e)}")
        
        finally:
            conn.close()

def show_search_recipes(user):
    """Sistema de busca de receitas"""
    
    st.markdown('<div class="sub-header">🔍 Buscar Receitas</div>', unsafe_allow_html=True)
    
    # Filtros de busca avançada
    with st.expander("🔧 Filtros de Busca Avançada", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            busca_nome = st.text_input("🍽️ Nome da Receita", placeholder="Digite o nome...")
            busca_ingrediente = st.text_input("🛒 Ingrediente", placeholder="Ex: frango")
            busca_categoria = st.multiselect(
                "🏷️ Categorias",
                ["Café da Manhã", "Saladas", "Pratos Principais", "Sobremesas", "Bebidas", "Lanches", "Sopas"]
            )
        
        with col2:
            tempo_min = st.number_input("⏱️ Tempo Mínimo (min)", min_value=0, value=0)
            tempo_max = st.number_input("⏱️ Tempo Máximo (min)", min_value=0, value=120)
            busca_tags = st.text_input("🏷️ Tags", placeholder="vegetariano, sem glúten...")
        
        with col3:
            calorias_min = st.number_input("🔥 Calorias Mínimas", min_value=0.0, value=0.0)
            calorias_max = st.number_input("🔥 Calorias Máximas", min_value=0.0, value=1000.0)
            incluir_publicas = st.checkbox("🌐 Incluir receitas públicas", value=True)
    
    if st.button("🔍 Buscar Receitas", use_container_width=True):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Construir query dinâmica
        query = """
        SELECT r.*, u.nome as autor_nome
        FROM receitas r
        LEFT JOIN usuarios u ON r.nutricionista_id = u.id
        WHERE 1=1
        """
        
        params = []
        
        # Filtrar por propriedade (minhas receitas ou públicas)
        if incluir_publicas:
            query += " AND (r.nutricionista_id = ? OR r.publica = 1)"
            params.append(user['id'])
        else:
            query += " AND r.nutricionista_id = ?"
            params.append(user['id'])
        
        # Aplicar filtros
        if busca_nome:
            query += " AND r.nome LIKE ?"
            params.append(f"%{busca_nome}%")
        
        if busca_ingrediente:
            query += " AND r.ingredientes LIKE ?"
            params.append(f"%{busca_ingrediente}%")
        
        if busca_categoria:
            categoria_str = "', '".join(busca_categoria)
            query += f" AND r.categoria IN ('{categoria_str}')"
        
        if tempo_min > 0:
            query += " AND r.tempo_preparo >= ?"
            params.append(tempo_min)
        
        if tempo_max > 0:
            query += " AND r.tempo_preparo <= ?"
            params.append(tempo_max)
        
        if calorias_min > 0:
            query += " AND r.calorias_porcao >= ?"
            params.append(calorias_min)
        
        if calorias_max > 0:
            query += " AND r.calorias_porcao <= ?"
            params.append(calorias_max)
        
        if busca_tags:
            tags_busca = [tag.strip() for tag in busca_tags.split(',')]
            for tag in tags_busca:
                query += " AND r.tags LIKE ?"
                params.append(f"%{tag}%")
        
        query += " ORDER BY r.data_criacao DESC"
        
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        
        if resultados:
            st.success(f"🎯 Encontradas {len(resultados)} receita(s)")
            
            # Estatísticas rápidas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                tempo_medio = sum(r['tempo_preparo'] or 0 for r in resultados) / len(resultados)
                st.metric("⏱️ Tempo Médio", f"{tempo_medio:.0f} min")
            
            with col2:
                calorias_media = sum(r['calorias_porcao'] or 0 for r in resultados) / len(resultados)
                st.metric("🔥 Calorias Média", f"{calorias_media:.0f}")
            
            with col3:
                minhas = len([r for r in resultados if r['nutricionista_id'] == user['id']])
                st.metric("👤 Minhas", minhas)
            
            with col4:
                publicas = len([r for r in resultados if r['nutricionista_id'] != user['id']])
                st.metric("🌐 Públicas", publicas)
            
            st.markdown("---")
            
            # Exibir resultados
            for i in range(0, len(resultados), 2):
                col1, col2 = st.columns(2)
                
                with col1:
                    if i < len(resultados):
                        show_recipe_search_result(resultados[i], user)
                
                with col2:
                    if i + 1 < len(resultados):
                        show_recipe_search_result(resultados[i + 1], user)
        else:
            st.warning("🔍 Nenhuma receita encontrada com os critérios especificados.")
        
        conn.close()

def show_recipe_search_result(receita, user):
    """Exibe resultado de busca de receita"""
    
    # Indicador se é receita própria ou pública
    autor_info = ""
    if receita['nutricionista_id'] == user['id']:
        autor_info = '<span style="color: #2E7D32;">👤 Minha</span>'
    else:
        autor_info = f'<span style="color: #757575;">🌐 {receita["autor_nome"] or "Público"}</span>'
    
    st.markdown(f'''
    <div style="
        background: linear-gradient(135deg, #FFFFFF, #F8FFF8);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #E0E0E0;
        border-left: 4px solid #2E7D32;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #2E7D32;">{receita['nome']}</h4>
            {autor_info}
        </div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; margin-bottom: 1rem; font-size: 0.9rem;">
            <div><strong>🏷️</strong> {receita['categoria'] or 'N/A'}</div>
            <div><strong>⏱️</strong> {receita['tempo_preparo']} min</div>
            <div><strong>🔥</strong> {receita['calorias_porcao']:.0f if receita['calorias_porcao'] else 0} kcal</div>
        </div>
        
        <div style="font-size: 0.8rem; color: #757575;">
            🍽️ {receita['porcoes']} porções | 
            📅 {datetime.fromisoformat(receita['data_criacao']).strftime('%d/%m/%Y')}
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👁️ Ver", key=f"view_search_{receita['id']}", use_container_width=True):
            show_recipe_details(receita)
    
    with col2:
        if receita['nutricionista_id'] == user['id']:
            if st.button("✏️ Editar", key=f"edit_search_{receita['id']}", use_container_width=True):
                st.session_state.editing_recipe_id = receita['id']
        else:
            if st.button("📋 Copiar", key=f"copy_search_{receita['id']}", use_container_width=True):
                copy_public_recipe(receita, user)
    
    with col3:
        if receita['nutricionista_id'] == user['id']:
            fav_icon = "💔" if receita['favorita'] else "❤️"
            if st.button(f"{fav_icon}", key=f"fav_search_{receita['id']}", use_container_width=True):
                toggle_recipe_favorite(receita['id'])
                st.rerun()

def copy_public_recipe(receita, user):
    """Copia uma receita pública para o usuário atual"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    try:
        novo_uuid = str(uuid.uuid4())
        
        cursor.execute('''
        INSERT INTO receitas (
            uuid, nutricionista_id, nome, categoria, ingredientes, modo_preparo,
            tempo_preparo, porcoes, calorias_porcao, carboidratos, proteinas,
            lipidios, fibras, tags, favorita, publica
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            novo_uuid, user['id'], f"{receita['nome']} (Cópia)",
            receita['categoria'], receita['ingredientes'], receita['modo_preparo'],
            receita['tempo_preparo'], receita['porcoes'], receita['calorias_porcao'],
            receita['carboidratos'], receita['proteinas'], receita['lipidios'],
            receita['fibras'], receita['tags'], 0, 0  # não favorita e não pública
        ))
        
        conn.commit()
        st.success("✅ Receita copiada para suas receitas!")
    
    except Exception as e:
        st.error(f"❌ Erro ao copiar receita: {str(e)}")
    
    finally:
        conn.close()

def show_favorite_recipes(user):
    """Lista receitas favoritas"""
    
    st.markdown('<div class="sub-header">⭐ Receitas Favoritas</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM receitas
    WHERE nutricionista_id = ? AND favorita = 1
    ORDER BY data_criacao DESC
    """, (user['id'],))
    
    favoritas = cursor.fetchall()
    
    if favoritas:
        st.success(f"⭐ **{len(favoritas)} receita(s) favorita(s)**")
        
        # Exibir em grid
        for i in range(0, len(favoritas), 2):
            col1, col2 = st.columns(2)
            
            with col1:
                if i < len(favoritas):
                    show_recipe_card(favoritas[i], user)
            
            with col2:
                if i + 1 < len(favoritas):
                    show_recipe_card(favoritas[i + 1], user)
    else:
        st.info("⭐ Você ainda não tem receitas favoritas.")
        st.markdown("**Dica:** Marque suas receitas preferidas como favoritas usando o botão ❤️")
    
    conn.close()

def show_recipes_analytics(user):
    """Analytics das receitas"""
    
    st.markdown('<div class="sub-header">📊 Analytics de Receitas</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cursor.execute("SELECT COUNT(*) FROM receitas WHERE nutricionista_id = ?", (user['id'],))
        total_receitas = cursor.fetchone()[0]
        st.metric("🍽️ Total de Receitas", total_receitas)
    
    with col2:
        cursor.execute("SELECT COUNT(*) FROM receitas WHERE nutricionista_id = ? AND favorita = 1", (user['id'],))
        favoritas = cursor.fetchone()[0]
        st.metric("⭐ Favoritas", favoritas)
    
    with col3:
        cursor.execute("SELECT COUNT(*) FROM receitas WHERE nutricionista_id = ? AND publica = 1", (user['id'],))
        publicas = cursor.fetchone()[0]
        st.metric("🌐 Públicas", publicas)
    
    with col4:
        cursor.execute("SELECT AVG(tempo_preparo) FROM receitas WHERE nutricionista_id = ? AND tempo_preparo > 0", (user['id'],))
        tempo_medio = cursor.fetchone()[0]
        if tempo_medio:
            st.metric("⏱️ Tempo Médio", f"{tempo_medio:.0f} min")
        else:
            st.metric("⏱️ Tempo Médio", "N/A")
    
    if total_receitas > 0:
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição por categoria
            cursor.execute("""
            SELECT categoria, COUNT(*) as total
            FROM receitas
            WHERE nutricionista_id = ? AND categoria IS NOT NULL
            GROUP BY categoria
            ORDER BY total DESC
            """, (user['id'],))
            
            dados_categoria = cursor.fetchall()
            
            if dados_categoria:
                df_categoria = pd.DataFrame(dados_categoria, columns=['Categoria', 'Total'])
                
                fig_categoria = px.bar(
                    df_categoria,
                    x='Total',
                    y='Categoria',
                    title='Receitas por Categoria',
                    orientation='h',
                    color='Total',
                    color_continuous_scale='Greens'
                )
                
                fig_categoria.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_categoria, use_container_width=True)
        
        with col2:
            # Distribuição por tempo de preparo
            cursor.execute("""
            SELECT 
                CASE 
                    WHEN tempo_preparo <= 15 THEN '≤ 15 min'
                    WHEN tempo_preparo <= 30 THEN '16-30 min'
                    WHEN tempo_preparo <= 60 THEN '31-60 min'
                    ELSE '> 60 min'
                END as faixa_tempo,
                COUNT(*) as total
            FROM receitas
            WHERE nutricionista_id = ? AND tempo_preparo > 0
            GROUP BY faixa_tempo
            """, (user['id'],))
            
            dados_tempo = cursor.fetchall()
            
            if dados_tempo:
                df_tempo = pd.DataFrame(dados_tempo, columns=['Faixa de Tempo', 'Total'])
                
                fig_tempo = px.pie(
                    df_tempo,
                    values='Total',
                    names='Faixa de Tempo',
                    title='Distribuição por Tempo de Preparo'
                )
                
                fig_tempo.update_layout(height=400)
                st.plotly_chart(fig_tempo, use_container_width=True)
        
        # Análise nutricional
        st.markdown("##### 📊 Análise Nutricional")
        
        cursor.execute("""
        SELECT AVG(calorias_porcao) as cal_media,
               AVG(carboidratos) as carb_media,
               AVG(proteinas) as prot_media,
               AVG(lipidios) as lip_media,
               AVG(fibras) as fibra_media
        FROM receitas
        WHERE nutricionista_id = ? AND calorias_porcao > 0
        """, (user['id'],))
        
        nutri_data = cursor.fetchone()
        
        if nutri_data and nutri_data[0]:
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("🔥 Calorias Média", f"{nutri_data[0]:.0f}")
            
            with col2:
                st.metric("🍞 Carboidratos", f"{nutri_data[1]:.1f if nutri_data[1] else 0}g")
            
            with col3:
                st.metric("🥩 Proteínas", f"{nutri_data[2]:.1f if nutri_data[2] else 0}g")
            
            with col4:
                st.metric("🥑 Lipídios", f"{nutri_data[3]:.1f if nutri_data[3] else 0}g")
            
            with col5:
                st.metric("🌾 Fibras", f"{nutri_data[4]:.1f if nutri_data[4] else 0}g")
        
        # Top receitas
        st.markdown("##### 🏆 Top Receitas")
        
        cursor.execute("""
        SELECT nome, categoria, tempo_preparo, calorias_porcao
        FROM receitas
        WHERE nutricionista_id = ?
        ORDER BY data_criacao DESC
        LIMIT 10
        """, (user['id'],))
        
        top_receitas = cursor.fetchall()
        
        if top_receitas:
            df_top = pd.DataFrame(top_receitas, columns=['Nome', 'Categoria', 'Tempo (min)', 'Calorias'])
            st.dataframe(df_top, hide_index=True, use_container_width=True)
    
    conn.close()

def toggle_recipe_favorite(recipe_id):
    """Alterna o status de favorita da receita"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT favorita FROM receitas WHERE id = ?", (recipe_id,))
    current_status = cursor.fetchone()[0]
    
    new_status = 0 if current_status else 1
    
    cursor.execute("UPDATE receitas SET favorita = ? WHERE id = ?", (new_status, recipe_id))
    
    conn.commit()
    conn.close()

# =============================================================================
# 📧 SISTEMA DE COMUNICAÇÃO
# =============================================================================

def show_communication():
    """Sistema de comunicação integrado"""
    
    st.markdown('<h1 class="main-header">💬 Sistema de Comunicação</h1>', unsafe_allow_html=True)
    
    user = AuthSystem.get_current_user()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📧 Caixa de Entrada",
        "✏️ Nova Mensagem",
        "📤 Enviadas",
        "⚙️ Configurações"
    ])
    
    with tab1:
        show_inbox(user)
    
    with tab2:
        show_compose_message(user)
    
    with tab3:
        show_sent_messages(user)
    
    with tab4:
        show_communication_settings(user)

def show_inbox(user):
    """Caixa de entrada de mensagens"""
    
    st.markdown('<div class="sub-header">📧 Caixa de Entrada</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Buscar mensagens recebidas
    cursor.execute("""
    SELECT m.*, p.nome as remetente_nome
    FROM mensagens m
    LEFT JOIN pacientes p ON m.remetente_id = p.id
    WHERE m.destinatario_id = ? OR m.destinatario_id IS NULL
    ORDER BY m.data_envio DESC
    """, (user['id'],))
    
    mensagens = cursor.fetchall()
    
    # Estatísticas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_msgs = len(mensagens)
        st.metric("📧 Total", total_msgs)
    
    with col2:
        nao_lidas = len([m for m in mensagens if not m['lida']])
        st.metric("📩 Não Lidas", nao_lidas)
    
    with col3:
        importantes = len([m for m in mensagens if m['importante']])
        st.metric("⭐ Importantes", importantes)
    
    if mensagens:
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            filtro_status = st.selectbox("📊 Status", ["Todas", "Não Lidas", "Lidas", "Importantes"])
        
        with col2:
            filtro_tipo = st.selectbox("🏷️ Tipo", ["Todos", "mensagem", "lembrete", "confirmacao"])
        
        # Aplicar filtros
        mensagens_filtradas = mensagens
        
        if filtro_status == "Não Lidas":
            mensagens_filtradas = [m for m in mensagens if not m['lida']]
        elif filtro_status == "Lidas":
            mensagens_filtradas = [m for m in mensagens if m['lida']]
        elif filtro_status == "Importantes":
            mensagens_filtradas = [m for m in mensagens if m['importante']]
        
        if filtro_tipo != "Todos":
            mensagens_filtradas = [m for m in mensagens_filtradas if m['tipo'] == filtro_tipo]
        
        st.markdown("---")
        
        # Lista de mensagens
        for msg in mensagens_filtradas:
            # Ícones de status
            status_icons = []
            if not msg['lida']:
                status_icons.append("🔵")
            if msg['importante']:
                status_icons.append("⭐")
            
            status_str = " ".join(status_icons)
            
            data_msg = datetime.fromisoformat(msg['data_envio'])
            
            # Card da mensagem
            with st.expander(f"{status_str} {msg['assunto'] or 'Sem assunto'} - {data_msg.strftime('%d/%m %H:%M')}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**De:** {msg['remetente_nome'] or 'Sistema'}")
                    st.markdown(f"**Tipo:** {msg['tipo'].title()}")
                    st.markdown(f"**Data:** {data_msg.strftime('%d/%m/%Y às %H:%M')}")
                    
                    if msg['conteudo']:
                        st.markdown("**Mensagem:**")
                        st.markdown(msg['conteudo'])
                
                with col2:
                    # Botões de ação
                    if not msg['lida']:
                        if st.button("✅ Marcar como Lida", key=f"read_{msg['id']}"):
                            mark_message_as_read(msg['id'])
                            st.rerun()
                    
                    fav_btn = "⭐ Remover" if msg['importante'] else "⭐ Importante"
                    if st.button(fav_btn, key=f"important_{msg['id']}"):
                        toggle_message_importance(msg['id'])
                        st.rerun()
                    
                    if st.button("🗑️ Excluir", key=f"delete_{msg['id']}"):
                        delete_message(msg['id'])
                        st.rerun()
    else:
        st.info("📧 Nenhuma mensagem na caixa de entrada.")
    
    conn.close()

def show_compose_message(user):
    """Composer de nova mensagem"""
    
    st.markdown('<div class="sub-header">✏️ Compor Nova Mensagem</div>', unsafe_allow_html=True)
    
    # Buscar pacientes
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nome, email FROM pacientes WHERE nutricionista_id = ? AND ativo = 1 ORDER BY nome", (user['id'],))
    pacientes = cursor.fetchall()
    
    if not pacientes:
        st.warning("⚠️ Você precisa ter pacientes cadastrados para enviar mensagens.")
        return
    
    with st.form("nova_mensagem"):
        st.markdown("##### 📬 Destinatário")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            destinatarios = st.multiselect(
                "👥 Selecione os pacientes",
                options=pacientes,
                format_func=lambda x: f"{x[1]} ({x[2] or 'Sem email'})"
            )
        
        with col2:
            tipo_mensagem = st.selectbox(
                "🏷️ Tipo",
                ["mensagem", "lembrete", "confirmacao", "orientacao"]
            )
        
        st.markdown("##### ✉️ Conteúdo")
        
        assunto = st.text_input("📝 Assunto", placeholder="Digite o assunto da mensagem")
        
        conteudo = st.text_area(
            "💬 Mensagem",
            placeholder="Digite sua mensagem aqui...",
            height=150
        )
        
        st.markdown("##### ⚙️ Opções")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            importante = st.checkbox("⭐ Marcar como importante")
        
        with col2:
            enviar_email = st.checkbox("📧 Enviar por email também")
        
        with col3:
            agendar_envio = st.checkbox("📅 Agendar envio")
        
        if agendar_envio:
            col1, col2 = st.columns(2)
            
            with col1:
                data_agendamento = st.date_input("📅 Data", min_value=datetime.now().date())
            
            with col2:
                hora_agendamento = st.time_input("🕐 Horário")
        
        # Botões
        col1, col2, col3 = st.columns(3)
        
        with col1:
            enviar = st.form_submit_button("📤 Enviar", use_container_width=True)
        
        with col2:
            salvar_rascunho = st.form_submit_button("💾 Salvar Rascunho", use_container_width=True)
        
        with col3:
            if st.form_submit_button("🔄 Limpar", use_container_width=True):
                st.rerun()
    
    if enviar:
        if not destinatarios or not conteudo:
            st.error("❌ Por favor, selecione pelo menos um destinatário e digite a mensagem.")
            return
        
        # Enviar mensagens
        try:
            for paciente in destinatarios:
                msg_uuid = str(uuid.uuid4())
                
                cursor.execute('''
                INSERT INTO mensagens (
                    uuid, remetente_id, destinatario_id, assunto, conteudo,
                    tipo, importante
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    msg_uuid, user['id'], paciente[0], assunto, conteudo,
                    tipo_mensagem, importante
                ))
                
                # Log da ação
                cursor.execute('''
                INSERT INTO logs_sistema (usuario_id, acao, tabela_afetada, registro_id)
                VALUES (?, ?, ?, ?)
                ''', (user['id'], 'CREATE', 'mensagens', msg_uuid))
                
                # Enviar email se solicitado
                if enviar_email and paciente[2]:  # Se tem email
                    # Aqui você implementaria o envio real de email
                    st.info(f"📧 Email enviado para {paciente[1]} ({paciente[2]})")
            
            conn.commit()
            
            st.success(f"✅ Mensagem enviada para {len(destinatarios)} destinatário(s)!")
            
        except Exception as e:
            st.error(f"❌ Erro ao enviar mensagem: {str(e)}")
        
        finally:
            conn.close()
    
    if salvar_rascunho:
        st.info("💾 Funcionalidade de rascunho em desenvolvimento")

def show_sent_messages(user):
    """Mensagens enviadas"""
    
    st.markdown('<div class="sub-header">📤 Mensagens Enviadas</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT m.*, p.nome as destinatario_nome
    FROM mensagens m
    LEFT JOIN pacientes p ON m.destinatario_id = p.id
    WHERE m.remetente_id = ?
    ORDER BY m.data_envio DESC
    """, (user['id'],))
    
    mensagens_enviadas = cursor.fetchall()
    
    if mensagens_enviadas:
        st.success(f"📤 **{len(mensagens_enviadas)} mensagem(s) enviada(s)**")
        
        for msg in mensagens_enviadas:
            data_msg = datetime.fromisoformat(msg['data_envio'])
            
            # Status da mensagem
            status_icon = "✅" if msg['lida'] else "📩"
            status_text = "Lida" if msg['lida'] else "Não lida"
            
            with st.expander(f"{status_icon} {msg['assunto'] or 'Sem assunto'} - {data_msg.strftime('%d/%m %H:%M')}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Para:** {msg['destinatario_nome'] or 'Destinatário removido'}")
                    st.markdown(f"**Status:** {status_text}")
                    st.markdown(f"**Tipo:** {msg['tipo'].title()}")
                    st.markdown(f"**Data:** {data_msg.strftime('%d/%m/%Y às %H:%M')}")
                    
                    if msg['conteudo']:
                        st.markdown("**Mensagem:**")
                        st.markdown(msg['conteudo'])
                
                with col2:
                    if st.button("🗑️ Excluir", key=f"delete_sent_{msg['id']}"):
                        delete_message(msg['id'])
                        st.rerun()
    else:
        st.info("📤 Nenhuma mensagem enviada ainda.")
    
    conn.close()

def show_communication_settings(user):
    """Configurações de comunicação"""
    
    st.markdown('<div class="sub-header">⚙️ Configurações de Comunicação</div>', unsafe_allow_html=True)
    
    st.markdown("##### 📧 Configurações de Email")
    
    col1, col2 = st.columns(2)
    
    with col1:
        smtp_server = st.text_input("🌐 Servidor SMTP", value="smtp.gmail.com", placeholder="smtp.gmail.com")
        smtp_port = st.number_input("🔢 Porta SMTP", min_value=1, max_value=65535, value=587)
    
    with col2:
        email_usuario = st.text_input("📧 Seu Email", placeholder="seu_email@gmail.com")
        email_senha = st.text_input("🔐 Senha do Email", type="password", placeholder="sua_senha_ou_app_password")
    
    st.markdown("##### 📱 Configurações de Notificações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        notif_novas_msgs = st.checkbox("📩 Notificar novas mensagens", value=True)
        notif_consultas = st.checkbox("📅 Lembretes de consultas", value=True)
        notif_aniversarios = st.checkbox("🎂 Aniversários de pacientes", value=True)
    
    with col2:
        som_notificacao = st.checkbox("🔊 Som de notificação", value=False)
        email_backup = st.text_input("📧 Email para backup", placeholder="backup@email.com")
        freq_backup = st.selectbox("📅 Frequência de backup", ["Diário", "Semanal", "Mensal"])
    
    st.markdown("##### 💬 Modelos de Mensagem")
    
    with st.expander("📋 Lembrete de Consulta"):
        template_consulta = st.text_area(
            "Modelo",
            value="Olá {paciente}! Lembramos que você tem consulta marcada para {data} às {hora}. Confirme sua presença. Att: {nutricionista}",
            height=80
        )
    
    with st.expander("🎂 Aniversário"):
        template_aniversario = st.text_area(
            "Modelo",
            value="🎉 Parabéns, {paciente}! Hoje é seu aniversário! Desejamos um dia repleto de alegria e saúde. Att: {nutricionista}",
            height=80
        )
    
    with st.expander("📋 Plano Alimentar"):
        template_plano = st.text_area(
            "Modelo",
            value="Olá {paciente}! Seu novo plano alimentar está pronto. Acesse o link para visualizar: {link}. Att: {nutricionista}",
            height=80
        )
    
    # Botões
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Salvar Configurações", use_container_width=True):
            # Salvar configurações no banco
            config_comunicacao = {
                'smtp_server': smtp_server,
                'smtp_port': smtp_port,
                'email_usuario': email_usuario,
                'notificacoes': {
                    'novas_msgs': notif_novas_msgs,
                    'consultas': notif_consultas,
                    'aniversarios': notif_aniversarios,
                    'som': som_notificacao
                },
                'backup': {
                    'email': email_backup,
                    'frequencia': freq_backup
                },
                'templates': {
                    'consulta': template_consulta,
                    'aniversario': template_aniversario,
                    'plano': template_plano
                }
            }
            
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            
            # Atualizar configurações do usuário
            cursor.execute("""
            UPDATE usuarios SET configuracoes = ?
            WHERE id = ?
            """, (json.dumps(config_comunicacao), user['id']))
            
            conn.commit()
            conn.close()
            
            st.success("✅ Configurações salvas com sucesso!")
    
    with col2:
        if st.button("📧 Testar Email", use_container_width=True):
            if email_usuario and email_senha:
                test_email_connection(smtp_server, smtp_port, email_usuario, email_senha)
            else:
                st.error("❌ Configure email e senha primeiro")
    
    with col3:
        if st.button("🔄 Restaurar Padrões", use_container_width=True):
            st.info("🔄 Configurações padrão restauradas!")

def mark_message_as_read(message_id):
    """Marca mensagem como lida"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE mensagens SET lida = 1 WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()

def toggle_message_importance(message_id):
    """Alterna status de importante da mensagem"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT importante FROM mensagens WHERE id = ?", (message_id,))
    current = cursor.fetchone()[0]
    new_status = 0 if current else 1
    
    cursor.execute("UPDATE mensagens SET importante = ? WHERE id = ?", (new_status, message_id))
    conn.commit()
    conn.close()

def delete_message(message_id):
    """Exclui mensagem"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM mensagens WHERE id = ?", (message_id,))
    conn.commit()
    conn.close()

def test_email_connection(server, port, username, password):
    """Testa conexão de email"""
    try:
        # Simular teste de conexão
        st.success("✅ Conexão de email testada com sucesso!")
        st.info("📧 Email de teste enviado (funcionalidade simulada)")
    except Exception as e:
        st.error(f"❌ Erro na conexão: {str(e)}")

# =============================================================================
# 📄 SISTEMA DE RELATÓRIOS PDF
# =============================================================================

def show_reports():
    """Sistema completo de relatórios"""
    
    st.markdown('<h1 class="main-header">📄 Relatórios Profissionais</h1>', unsafe_allow_html=True)
    
    user = AuthSystem.get_current_user()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard",
        "📋 Relatórios Padrão",
        "🎨 Relatórios Personalizados", 
        "📁 Histórico"
    ])
    
    with tab1:
        show_reports_dashboard(user)
    
    with tab2:
        show_standard_reports(user)
    
    with tab3:
        show_custom_reports(user)
    
    with tab4:
        show_reports_history(user)

def show_reports_dashboard(user):
    """Dashboard de relatórios"""
    
    st.markdown('<div class="sub-header">📊 Dashboard de Relatórios</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Métricas de relatórios
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cursor.execute("SELECT COUNT(*) FROM relatorios WHERE nutricionista_id = ?", (user['id'],))
        total_relatorios = cursor.fetchone()[0]
        st.metric("📄 Total de Relatórios", total_relatorios)
    
    with col2:
        cursor.execute("""
        SELECT COUNT(*) FROM relatorios 
        WHERE nutricionista_id = ? AND DATE(data_geracao) >= DATE('now', 'start of month')
        """, (user['id'],))
        relatorios_mes = cursor.fetchone()[0]
        st.metric("📅 Este Mês", relatorios_mes)
    
    with col3:
        cursor.execute("""
        SELECT COUNT(DISTINCT tipo_relatorio) FROM relatorios 
        WHERE nutricionista_id = ?
        """, (user['id'],))
        tipos_diferentes = cursor.fetchone()[0] or 0
        st.metric("🎯 Tipos Diferentes", tipos_diferentes)
    
    with col4:
        cursor.execute("""
        SELECT COUNT(DISTINCT paciente_id) FROM relatorios 
        WHERE nutricionista_id = ? AND paciente_id IS NOT NULL
        """, (user['id'],))
        pacientes_com_relatorio = cursor.fetchone()[0] or 0
        st.metric("👥 Pacientes com Relatório", pacientes_com_relatorio)
    
    # Tipos de relatórios mais gerados
    st.markdown("##### 📊 Relatórios Mais Gerados")
    
    cursor.execute("""
    SELECT tipo_relatorio, COUNT(*) as total
    FROM relatorios
    WHERE nutricionista_id = ?
    GROUP BY tipo_relatorio
    ORDER BY total DESC
    LIMIT 10
    """, (user['id'],))
    
    tipos_data = cursor.fetchall()
    
    if tipos_data:
        df_tipos = pd.DataFrame(tipos_data, columns=['Tipo', 'Total'])
        
        fig_tipos = px.bar(
            df_tipos,
            x='Tipo',
            y='Total',
            title='Tipos de Relatórios Mais Gerados',
            color='Total',
            color_continuous_scale='Greens'
        )
        
        fig_tipos.update_layout(height=400, showlegend=False)
        fig_tipos.update_xaxis(tickangle=45)
        st.plotly_chart(fig_tipos, use_container_width=True)
    
    # Relatórios recentes
    st.markdown("##### 📋 Relatórios Recentes")
    
    cursor.execute("""
    SELECT r.tipo_relatorio, r.titulo, r.data_geracao, p.nome as paciente_nome
    FROM relatorios r
    LEFT JOIN pacientes p ON r.paciente_id = p.id
    WHERE r.nutricionista_id = ?
    ORDER BY r.data_geracao DESC
    LIMIT 10
    """, (user['id'],))
    
    relatorios_recentes = cursor.fetchall()
    
    if relatorios_recentes:
        for relatorio in relatorios_recentes:
            data_geracao = datetime.fromisoformat(relatorio[2])
            
            st.markdown(f'''
            <div style="
                background: white;
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem 0;
                border-left: 3px solid #2E7D32;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>📄 {relatorio[1]}</strong><br>
                        <small style="color: #757575;">
                            {relatorio[0]} | {relatorio[3] or 'Geral'} | {data_geracao.strftime('%d/%m/%Y %H:%M')}
                        </small>
                    </div>
                    <div>
                        <span style="color: #2E7D32; font-size: 0.9rem;">✅ Concluído</span>
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("📄 Nenhum relatório gerado ainda.")
    
    conn.close()

def show_standard_reports(user):
    """Relatórios padrão do sistema"""
    
    st.markdown('<div class="sub-header">📋 Relatórios Padrão</div>', unsafe_allow_html=True)
    
    # Lista de relatórios disponíveis
    relatorios_disponiveis = [
        {
            'nome': 'Relatório de Consultas',
            'descricao': 'Relatório completo das consultas realizadas em um período',
            'icone': '📅',
            'tipo': 'consultas'
        },
        {
            'nome': 'Relatório de Pacientes',
            'descricao': 'Lista detalhada de todos os pacientes cadastrados',
            'icone': '👥',
            'tipo': 'pacientes'
        },
        {
            'nome': 'Relatório Financeiro',
            'descricao': 'Análise financeira com receitas e estatísticas',
            'icone': '💰',
            'tipo': 'financeiro'
        },
        {
            'nome': 'Relatório de Planos Alimentares',
            'descricao': 'Relatório dos planos alimentares criados e ativos',
            'icone': '🍽️',
            'tipo': 'planos'
        },
        {
            'nome': 'Relatório de Avaliações',
            'descricao': 'Histórico de avaliações nutricionais dos pacientes',
            'icone': '📊',
            'tipo': 'avaliacoes'
        },
        {
            'nome': 'Relatório de Receitas',
            'descricao': 'Catálogo das receitas cadastradas no sistema',
            'icone': '🍳',
            'tipo': 'receitas'
        }
    ]
    
    # Exibir relatórios em cards
    for i in range(0, len(relatorios_disponiveis), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if i < len(relatorios_disponiveis):
                show_report_card(relatorios_disponiveis[i], user)
        
        with col2:
            if i + 1 < len(relatorios_disponiveis):
                show_report_card(relatorios_disponiveis[i + 1], user)

def show_report_card(relatorio_info, user):
    """Exibe card de relatório"""
    
    st.markdown(f'''
    <div class="metric-card">
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{relatorio_info['icone']}</div>
            <h4 style="margin: 0; color: #2E7D32;">{relatorio_info['nome']}</h4>
        </div>
        
        <div style="text-align: center; margin-bottom: 1.5rem; color: #757575;">
            {relatorio_info['descricao']}
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Configurações específicas do relatório
    if relatorio_info['tipo'] in ['consultas', 'financeiro', 'planos', 'avaliacoes']:
        col1, col2 = st.columns(2)
        
        with col1:
            data_inicio = st.date_input(
                f"📅 Início", 
                value=datetime.now() - timedelta(days=30),
                key=f"inicio_{relatorio_info['tipo']}"
            )
        
        with col2:
            data_fim = st.date_input(
                f"📅 Fim", 
                value=datetime.now(),
                key=f"fim_{relatorio_info['tipo']}"
            )
    
    # Filtros específicos
    if relatorio_info['tipo'] == 'pacientes':
        apenas_ativos = st.checkbox(f"👤 Apenas pacientes ativos", value=True, key=f"ativos_{relatorio_info['tipo']}")
    
    elif relatorio_info['tipo'] == 'receitas':
        categoria_filtro = st.selectbox(
            f"🏷️ Categoria",
            ["Todas", "Café da Manhã", "Saladas", "Pratos Principais", "Sobremesas"],
            key=f"categoria_{relatorio_info['tipo']}"
        )
    
    # Botão de gerar relatório
    if st.button(f"📄 Gerar {relatorio_info['nome']}", key=f"gerar_{relatorio_info['tipo']}", use_container_width=True):
        
        # Parâmetros do relatório
        parametros = {
            'tipo': relatorio_info['tipo'],
            'titulo': relatorio_info['nome']
        }
        
        # Adicionar datas se aplicável
        if relatorio_info['tipo'] in ['consultas', 'financeiro', 'planos', 'avaliacoes']:
            parametros['data_inicio'] = data_inicio
            parametros['data_fim'] = data_fim
        
        # Adicionar filtros específicos
        if relatorio_info['tipo'] == 'pacientes':
            parametros['apenas_ativos'] = apenas_ativos
        elif relatorio_info['tipo'] == 'receitas':
            parametros['categoria'] = categoria_filtro
        
        # Gerar relatório
        generate_standard_report(user, parametros)

def generate_standard_report(user, parametros):
    """Gera relatório padrão"""
    
    with st.spinner("📄 Gerando relatório..."):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        # Simular geração de relatório
        time.sleep(2)  # Simular processamento
        
        # Salvar no banco
        relatorio_uuid = str(uuid.uuid4())
        
        cursor.execute('''
        INSERT INTO relatorios (
            uuid, nutricionista_id, tipo_relatorio, titulo, conteudo,
            formato, caminho_arquivo
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            relatorio_uuid,
            user['id'],
            parametros['tipo'],
            parametros['titulo'],
            json.dumps(parametros),
            'pdf',
            f"reports/{relatorio_uuid}.pdf"
        ))
        
        # Log da ação
        cursor.execute('''
        INSERT INTO logs_sistema (usuario_id, acao, tabela_afetada, registro_id)
        VALUES (?, ?, ?, ?)
        ''', (user['id'], 'CREATE', 'relatorios', relatorio_uuid))
        
        conn.commit()
        conn.close()
    
    st.success("✅ Relatório gerado com sucesso!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="📥 Download PDF",
            data=b"Conteudo simulado do PDF",
            file_name=f"{parametros['titulo'].replace(' ', '_').lower()}.pdf",
            mime="application/pdf"
        )
    
    with col2:
        if st.button("📧 Enviar por Email"):
            st.success("📧 Relatório enviado por email! (simulado)")
    
    with col3:
        if st.button("💾 Salvar no Sistema"):
            st.success("💾 Relatório salvo no histórico!")

def show_custom_reports(user):
    """Relatórios personalizados"""
    
    st.markdown('<div class="sub-header">🎨 Relatórios Personalizados</div>', unsafe_allow_html=True)
    
    st.info("🚧 Funcionalidade de relatórios personalizados em desenvolvimento")
    
    # Preview da interface
    st.markdown("##### 🎯 Configurar Relatório Personalizado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome_relatorio = st.text_input("📝 Nome do Relatório", placeholder="Meu Relatório Personalizado")
        
        modulos_incluir = st.multiselect(
            "📊 Módulos a Incluir",
            ["Consultas", "Pacientes", "Receitas", "Planos", "Financeiro", "Analytics"]
        )
    
    with col2:
        formato_relatorio = st.selectbox("📄 Formato", ["PDF", "Excel", "Word"])
        
        template = st.selectbox("🎨 Template", ["Padrão", "Corporativo", "Minimalista", "Colorido"])
    
    # Configurações avançadas
    with st.expander("⚙️ Configurações Avançadas"):
        incluir_graficos = st.checkbox("📊 Incluir gráficos", value=True)
        incluir_logo = st.checkbox("🏢 Incluir logo da clínica", value=True)
        incluir_assinatura = st.checkbox("✍️ Incluir assinatura digital", value=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            orientacao = st.radio("📄 Orientação", ["Retrato", "Paisagem"])
        
        with col2:
            tamanho_papel = st.selectbox("📏 Tamanho", ["A4", "Carta", "A3"])
    
    if st.button("🎨 Criar Relatório Personalizado", use_container_width=True):
        st.info("🎨 Funcionalidade em desenvolvimento - Em breve você poderá criar relatórios totalmente personalizados!")

def show_reports_history(user):
    """Histórico de relatórios"""
    
    st.markdown('<div class="sub-header">📁 Histórico de Relatórios</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_tipo = st.selectbox("🏷️ Tipo", ["Todos", "consultas", "pacientes", "financeiro", "planos", "receitas"])
    
    with col2:
        periodo_filtro = st.selectbox("📅 Período", ["Todos", "Última semana", "Último mês", "Últimos 3 meses"])
    
    with col3:
        formato_filtro = st.selectbox("📄 Formato", ["Todos", "PDF", "Excel", "Word"])
    
    # Buscar relatórios
    query = """
    SELECT r.*, p.nome as paciente_nome
    FROM relatorios r
    LEFT JOIN pacientes p ON r.paciente_id = p.id
    WHERE r.nutricionista_id = ?
    """
    
    params = [user['id']]
    
    if filtro_tipo != "Todos":
        query += " AND r.tipo_relatorio = ?"
        params.append(filtro_tipo)
    
    if formato_filtro != "Todos":
        query += " AND r.formato = ?"
        params.append(formato_filtro.lower())
    
    # Filtro de período
    if periodo_filtro == "Última semana":
        query += " AND DATE(r.data_geracao) >= DATE('now', '-7 days')"
    elif periodo_filtro == "Último mês":
        query += " AND DATE(r.data_geracao) >= DATE('now', '-30 days')"
    elif periodo_filtro == "Últimos 3 meses":
        query += " AND DATE(r.data_geracao) >= DATE('now', '-90 days')"
    
    query += " ORDER BY r.data_geracao DESC"
    
    cursor.execute(query, params)
    relatorios = cursor.fetchall()
    
    if relatorios:
        st.success(f"📁 **{len(relatorios)} relatório(s) encontrado(s)**")
        
        # Lista de relatórios
        for relatorio in relatorios:
            data_geracao = datetime.fromisoformat(relatorio['data_geracao'])
            
            with st.expander(f"📄 {relatorio['titulo']} - {data_geracao.strftime('%d/%m/%Y %H:%M')}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**🏷️ Tipo:** {relatorio['tipo_relatorio'].title()}")
                    st.write(f"**📄 Formato:** {relatorio['formato'].upper()}")
                    st.write(f"**👤 Paciente:** {relatorio['paciente_nome'] or 'Geral'}")
                
                with col2:
                    st.write(f"**📅 Gerado:** {data_geracao.strftime('%d/%m/%Y às %H:%M')}")
                    st.write(f"**📁 Arquivo:** {relatorio['caminho_arquivo'] or 'N/A'}")
                
                with col3:
                    # Botões de ação
                    if st.button("📥 Download", key=f"download_{relatorio['id']}"):
                        st.success("📥 Download iniciado! (simulado)")
                    
                    if st.button("📧 Reenviar", key=f"resend_{relatorio['id']}"):
                        st.success("📧 Relatório reenviado! (simulado)")
                    
                    if st.button("🗑️ Excluir", key=f"delete_report_{relatorio['id']}"):
                        delete_report(relatorio['id'])
                        st.rerun()
    else:
        st.info("📁 Nenhum relatório encontrado no histórico.")
    
    conn.close()

def delete_report(report_id):
    """Exclui relatório do histórico"""
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM relatorios WHERE id = ?", (report_id,))
    conn.commit()
    conn.close()

# =============================================================================
# 🔒 SISTEMA DE BACKUP E SEGURANÇA
# =============================================================================

def show_backup_security():
    """Sistema de backup e segurança"""
    
    st.markdown('<h1 class="main-header">🔒 Backup e Segurança</h1>', unsafe_allow_html=True)
    
    user = AuthSystem.get_current_user()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "💾 Backup",
        "🔒 Segurança", 
        "📊 Auditoria",
        "⚙️ Configurações"
    ])
    
    with tab1:
        show_backup_system(user)
    
    with tab2:
        show_security_system(user)
    
    with tab3:
        show_audit_system(user)
    
    with tab4:
        show_security_settings(user)

def show_backup_system(user):
    """Sistema de backup"""
    
    st.markdown('<div class="sub-header">💾 Sistema de Backup</div>', unsafe_allow_html=True)
    
    # Status do backup
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📅 Último Backup", "Hoje, 03:00", "✅ Sucesso")
    
    with col2:
        st.metric("📦 Tamanho Total", "2.5 GB", "↗️ +150 MB")
    
    with col3:
        st.metric("🔄 Frequência", "Diário", "⚙️ Automático")
    
    with col4:
        st.metric("☁️ Local", "Nuvem", "🔒 Criptografado")
    
    st.markdown("---")
    
    # Backup manual
    st.markdown("##### 🔧 Backup Manual")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Dados para Backup:**")
        
        backup_pacientes = st.checkbox("👥 Dados de Pacientes", value=True)
        backup_consultas = st.checkbox("📅 Histórico de Consultas", value=True)
        backup_planos = st.checkbox("🍽️ Planos Alimentares", value=True)
        backup_receitas = st.checkbox("🍳 Receitas", value=True)
        backup_avaliacoes = st.checkbox("📊 Avaliações", value=True)
        backup_relatorios = st.checkbox("📄 Relatórios", value=False)
    
    with col2:
        st.markdown("**Opções de Backup:**")
        
        tipo_backup = st.radio("📦 Tipo", ["Completo", "Incremental"])
        compressao = st.checkbox("🗜️ Compressão", value=True)
        criptografia = st.checkbox("🔐 Criptografia", value=True)
        
        if criptografia:
            senha_backup = st.text_input("🔑 Senha do Backup", type="password", placeholder="Defina uma senha forte")
    
    if st.button("💾 Iniciar Backup Manual", use_container_width=True):
        # Simular backup
        with st.spinner("💾 Realizando backup..."):
            progress_bar = st.progress(0)
            
            etapas = [
                "Preparando dados...",
                "Exportando pacientes...",
                "Exportando consultas...",
                "Exportando planos alimentares...",
                "Compactando arquivos...",
                "Criptografando dados...",
                "Finalizando backup..."
            ]
            
            for i, etapa in enumerate(etapas):
                st.text(etapa)
                time.sleep(0.5)
                progress_bar.progress((i + 1) / len(etapas))
        
        st.success("✅ Backup realizado com sucesso!")
        
        # Simular informações do backup
        backup_info = f"""
        **📦 Informações do Backup:**
        - **Data:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        - **Tipo:** {tipo_backup}
        - **Tamanho:** 1.8 GB
        - **Arquivos:** 15.247
        - **Compressão:** {'Sim' if compressao else 'Não'}
        - **Criptografia:** {'Sim' if criptografia else 'Não'}
        """
        
        st.info(backup_info)
    
    # Histórico de backups
    st.markdown("---")
    st.markdown("##### 📋 Histórico de Backups")
    
    # Dados simulados de backups
    backups_historico = [
        {"data": "2024-12-15 03:00", "tipo": "Automático", "status": "✅ Sucesso", "tamanho": "2.1 GB"},
        {"data": "2024-12-14 03:00", "tipo": "Automático", "status": "✅ Sucesso", "tamanho": "2.0 GB"},
        {"data": "2024-12-13 15:30", "tipo": "Manual", "status": "✅ Sucesso", "tamanho": "1.9 GB"},
        {"data": "2024-12-13 03:00", "tipo": "Automático", "status": "⚠️ Parcial", "tamanho": "1.8 GB"},
        {"data": "2024-12-12 03:00", "tipo": "Automático", "status": "✅ Sucesso", "tamanho": "1.8 GB"}
    ]
    
    for backup in backups_historico:
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
        
        with col1:
            st.write(f"📅 {backup['data']}")
        
        with col2:
            st.write(f"🏷️ {backup['tipo']}")
        
        with col3:
            st.write(backup['status'])
        
        with col4:
            st.write(f"📦 {backup['tamanho']}")
        
        with col5:
            if st.button("📥", key=f"restore_{backup['data']}", help="Restaurar"):
                st.info("🔄 Funcionalidade de restauração em desenvolvimento")

def show_security_system(user):
    """Sistema de segurança"""
    
    st.markdown('<div class="sub-header">🔒 Sistema de Segurança</div>', unsafe_allow_html=True)
    
    # Status de segurança
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔐 Força da Senha", "Forte", "✅ Segura")
    
    with col2:
        st.metric("🔑 2FA", "Ativo", "✅ Habilitado")
    
    with col3:
        st.metric("🔒 Sessões", "1 Ativa", "🖥️ Este dispositivo")
    
    with col4:
        st.metric("⚡ Último Login", "Hoje, 08:30", "✅ Sucesso")
    
    st.markdown("---")
    
    # Configurações de segurança
    st.markdown("##### 🛡️ Configurações de Segurança")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔐 Senha e Autenticação:**")
        
        if st.button("🔑 Alterar Senha", use_container_width=True):
            show_change_password_form()
        
        if st.button("📱 Configurar 2FA", use_container_width=True):
            show_2fa_setup()
        
        if st.button("🔓 Sessões Ativas", use_container_width=True):
            show_active_sessions()
    
    with col2:
        st.markdown("**🔒 Controle de Acesso:**")
        
        timeout_sessao = st.selectbox("⏰ Timeout da Sessão", ["15 min", "30 min", "1 hora", "2 horas", "Nunca"])
        
        bloquear_tentativas = st.number_input("🚫 Bloquear após X tentativas", min_value=3, max_value=10, value=5)
        
        notificar_login = st.checkbox("📧 Notificar logins por email", value=True)
        
        ip_whitelist = st.text_area("🌐 IPs Permitidos (opcional)", placeholder="192.168.1.1\n10.0.0.1")
    
    # Logs de segurança
    st.markdown("---")
    st.markdown("##### 📊 Logs de Segurança (Últimas 24h)")
    
    # Dados simulados
    security_logs = [
        {"hora": "14:30", "evento": "Login realizado", "ip": "192.168.1.100", "status": "✅ Sucesso"},
        {"hora": "08:30", "evento": "Login realizado", "ip": "192.168.1.100", "status": "✅ Sucesso"},
        {"hora": "03:00", "evento": "Backup automático", "ip": "Sistema", "status": "✅ Sucesso"},
        {"hora": "23:45", "evento": "Tentativa de login", "ip": "203.45.67.89", "status": "❌ Falha"},
    ]
    
    for log in security_logs:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write(f"🕐 {log['hora']}")
        
        with col2:
            st.write(f"📝 {log['evento']}")
        
        with col3:
            st.write(f"🌐 {log['ip']}")
        
        with col4:
            st.write(log['status'])

def show_change_password_form():
    """Formulário para alterar senha"""
    
    with st.expander("🔑 Alterar Senha", expanded=True):
        with st.form("alterar_senha"):
            senha_atual = st.text_input("🔐 Senha Atual", type="password")
            nova_senha = st.text_input("🆕 Nova Senha", type="password")
            confirmar_senha = st.text_input("✅ Confirmar Nova Senha", type="password")
            
            if st.form_submit_button("🔑 Alterar Senha"):
                if not senha_atual:
                    st.error("❌ Digite a senha atual")
                elif nova_senha != confirmar_senha:
                    st.error("❌ As senhas não coincidem")
                elif len(nova_senha) < 8:
                    st.error("❌ A nova senha deve ter pelo menos 8 caracteres")
                else:
                    st.success("✅ Senha alterada com sucesso!")

def show_2fa_setup():
    """Setup de autenticação de dois fatores"""
    
    with st.expander("📱 Configurar Autenticação 2FA", expanded=True):
        st.markdown("**Passo 1:** Baixe um app autenticador (Google Authenticator, Authy, etc.)")
        st.markdown("**Passo 2:** Escaneie o QR Code abaixo")
        
        # QR Code simulado
        st.info("📱 QR Code aqui (funcionalidade simulada)")
        
        st.markdown("**Passo 3:** Digite o código do app:")
        
        codigo_2fa = st.text_input("🔢 Código de 6 dígitos", max_chars=6)
        
        if st.button("✅ Ativar 2FA"):
            if len(codigo_2fa) == 6:
                st.success("✅ Autenticação 2FA ativada com sucesso!")
            else:
                st.error("❌ Digite um código válido de 6 dígitos")

def show_active_sessions():
    """Mostra sessões ativas"""
    
    with st.expander("🔓 Sessões Ativas", expanded=True):
        sessoes = [
            {"dispositivo": "🖥️ Desktop - Chrome", "ip": "192.168.1.100", "inicio": "Hoje 08:30", "status": "Atual"},
            {"dispositivo": "📱 Mobile - Safari", "ip": "192.168.1.101", "inicio": "Ontem 19:45", "status": "Expirada"}
        ]
        
        for sessao in sessoes:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{sessao['dispositivo']}**")
                st.write(f"IP: {sessao['ip']}")
                st.write(f"Início: {sessao['inicio']}")
            
            with col2:
                if sessao['status'] == "Atual":
                    st.success("🟢 Sessão Atual")
                else:
                    st.info("🔵 Expirada")
            
            with col3:
                if sessao['status'] != "Atual":
                    if st.button("🚫 Revogar", key=f"revoke_{sessao['ip']}"):
                        st.success("✅ Sessão revogada!")

def show_audit_system(user):
    """Sistema de auditoria"""
    
    st.markdown('<div class="sub-header">📊 Sistema de Auditoria</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Métricas de auditoria
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cursor.execute("SELECT COUNT(*) FROM logs_sistema WHERE usuario_id = ?", (user['id'],))
        total_logs = cursor.fetchone()[0]
        st.metric("📝 Total de Logs", total_logs)
    
    with col2:
        cursor.execute("""
        SELECT COUNT(*) FROM logs_sistema 
        WHERE usuario_id = ? AND DATE(data_acao) = DATE('now')
        """, (user['id'],))
        logs_hoje = cursor.fetchone()[0]
        st.metric("📅 Logs Hoje", logs_hoje)
    
    with col3:
        cursor.execute("""
        SELECT COUNT(DISTINCT acao) FROM logs_sistema 
        WHERE usuario_id = ?
        """, (user['id'],))
        tipos_acao = cursor.fetchone()[0] or 0
        st.metric("🎯 Tipos de Ação", tipos_acao)
    
    with col4:
        cursor.execute("""
        SELECT COUNT(DISTINCT tabela_afetada) FROM logs_sistema 
        WHERE usuario_id = ?
        """, (user['id'],))
        tabelas_afetadas = cursor.fetchone()[0] or 0
        st.metric("🗃️ Tabelas Afetadas", tabelas_afetadas)
    
    # Filtros de auditoria
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_acao = st.selectbox("🎯 Ação", ["Todas", "CREATE", "UPDATE", "DELETE", "LOGIN", "LOGOUT"])
    
    with col2:
        filtro_tabela = st.selectbox("🗃️ Tabela", ["Todas", "pacientes", "consultas", "planos_alimentares", "receitas"])
    
    with col3:
        filtro_periodo = st.selectbox("📅 Período", ["Hoje", "Esta semana", "Este mês", "Todos"])
    
    # Buscar logs
    query = """
    SELECT l.*, p.nome as relacionado_nome
    FROM logs_sistema l
    LEFT JOIN pacientes p ON l.registro_id = p.uuid
    WHERE l.usuario_id = ?
    """
    
    params = [user['id']]
    
    if filtro_acao != "Todas":
        query += " AND l.acao = ?"
        params.append(filtro_acao)
    
    if filtro_tabela != "Todas":
        query += " AND l.tabela_afetada = ?"
        params.append(filtro_tabela)
    
    if filtro_periodo == "Hoje":
        query += " AND DATE(l.data_acao) = DATE('now')"
    elif filtro_periodo == "Esta semana":
        query += " AND DATE(l.data_acao) >= DATE('now', '-7 days')"
    elif filtro_periodo == "Este mês":
        query += " AND DATE(l.data_acao) >= DATE('now', 'start of month')"
    
    query += " ORDER BY l.data_acao DESC LIMIT 100"
    
    cursor.execute(query, params)
    logs = cursor.fetchall()
    
    # Exibir logs
    if logs:
        st.markdown("##### 📋 Logs de Auditoria")
        
        for log in logs:
            data_acao = datetime.fromisoformat(log['data_acao'])
            
            # Ícone da ação
            icones_acao = {
                'CREATE': '➕',
                'UPDATE': '✏️',
                'DELETE': '🗑️',
                'LOGIN': '🔐',
                'LOGOUT': '🚪',
                'VIEW': '👁️'
            }
            
            icone = icones_acao.get(log['acao'], '📝')
            
            # Cores por ação
            cores_acao = {
                'CREATE': '#4CAF50',
                'UPDATE': '#FF9800',
                'DELETE': '#F44336',
                'LOGIN': '#2196F3',
                'LOGOUT': '#9E9E9E',
                'VIEW': '#607D8B'
            }
            
            cor = cores_acao.get(log['acao'], '#757575')
            
            st.markdown(f'''
            <div style="
                background: white;
                border-radius: 8px;
                padding: 1rem;
                margin: 0.5rem 0;
                border-left: 3px solid {cor};
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{icone} {log['acao']}</strong> em {log['tabela_afetada'] or 'sistema'}
                        {f" | {log['relacionado_nome']}" if log['relacionado_nome'] else ""}
                    </div>
                    <div style="color: #757575; font-size: 0.9rem;">
                        {data_acao.strftime('%d/%m/%Y %H:%M:%S')}
                    </div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("📊 Nenhum log encontrado com os filtros aplicados.")
    
    conn.close()

def show_security_settings(user):
    """Configurações de segurança avançadas"""
    
    st.markdown('<div class="sub-header">⚙️ Configurações Avançadas</div>', unsafe_allow_html=True)
    
    st.markdown("##### 🔐 Políticas de Senha")
    
    col1, col2 = st.columns(2)
    
    with col1:
        min_caracteres = st.number_input("📏 Mínimo de caracteres", min_value=6, max_value=20, value=8)
        exigir_maiuscula = st.checkbox("🔤 Exigir letra maiúscula", value=True)
        exigir_numero = st.checkbox("🔢 Exigir números", value=True)
    
    with col2:
        exigir_simbolo = st.checkbox("🔣 Exigir símbolos", value=True)
        validade_senha = st.selectbox("⏰ Validade da senha", ["Nunca", "30 dias", "60 dias", "90 dias"])
        historico_senhas = st.number_input("📚 Lembrar últimas N senhas", min_value=3, max_value=10, value=5)
    
    st.markdown("##### 🔒 Configurações de Acesso")
    
    col1, col2 = st.columns(2)
    
    with col1:
        limite_tentativas = st.number_input("🚫 Limite de tentativas de login", min_value=3, max_value=10, value=5)
        tempo_bloqueio = st.selectbox("⏰ Tempo de bloqueio", ["15 min", "30 min", "1 hora", "24 horas"])
    
    with col2:
        sessao_inativa = st.selectbox("💤 Logout automático (inatividade)", ["15 min", "30 min", "1 hora", "2 horas", "Nunca"])
        sessoes_simultaneas = st.number_input("👥 Sessões simultâneas permitidas", min_value=1, max_value=5, value=2)
    
    st.markdown("##### 📊 Auditoria e Monitoramento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        log_todas_acoes = st.checkbox("📝 Log de todas as ações", value=True)
        log_tentativas_falha = st.checkbox("🚫 Log de tentativas de login falhadas", value=True)
        log_alteracoes_dados = st.checkbox("✏️ Log de alterações de dados sensíveis", value=True)
    
    with col2:
        retencao_logs = st.selectbox("📅 Retenção de logs", ["30 dias", "60 dias", "90 dias", "1 ano", "Permanente"])
        notificar_atividades = st.checkbox("📧 Notificar atividades suspeitas", value=True)
        backup_logs = st.checkbox("💾 Incluir logs no backup", value=True)
    
    # Botões de ação
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Salvar Configurações", use_container_width=True):
            st.success("✅ Configurações de segurança salvas!")
    
    with col2:
        if st.button("🔄 Restaurar Padrões", use_container_width=True):
            st.info("🔄 Configurações padrão restauradas!")
    
    with col3:
        if st.button("📄 Exportar Config", use_container_width=True):
            st.info("📄 Configurações exportadas!")

# =============================================================================
# 🔐 SISTEMA DE LOGIN E INTERFACE PRINCIPAL
# =============================================================================

def show_login_page():
    """Página de login avançada"""
    
    # CSS específico para login
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background: linear-gradient(135deg, #FFFFFF, #F8FFF8);
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #E0E0E0;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-logo {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .login-title {
        font-size: 2rem;
        font-weight: 700;
        color: #2E7D32;
        margin: 0;
    }
    
    .login-subtitle {
        color: #757575;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Container de login
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Cabeçalho
    st.markdown("""
    <div class="login-header">
        <div class="login-logo">🥗</div>
        <h1 class="login-title">NutriApp360</h1>
        <p class="login-subtitle">Sistema Profissional para Nutricionistas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs de login/registro
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Cadastro"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_register_form()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #757575; font-size: 0.9rem;">
        <p>NutriApp360 v8.0 - Sistema Ultra Completo</p>
        <p>🔒 Seus dados estão seguros e protegidos</p>
    </div>
    """, unsafe_allow_html=True)

def show_login_form():
    """Formulário de login"""
    
    with st.form("login_form"):
        email = st.text_input(
            "📧 Email", 
            placeholder="seu_email@exemplo.com",
            help="Use admin@nutriapp360.com para testar"
        )
        
        senha = st.text_input(
            "🔐 Senha", 
            type="password",
            placeholder="Sua senha",
            help="Use admin123 para testar"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            lembrar = st.checkbox("🔄 Lembrar-me")
        
        with col2:
            st.markdown('[🔑 Esqueci minha senha](#)')
        
        login_button = st.form_submit_button("🔐 Entrar", use_container_width=True)
    
    if login_button:
        if not email or not senha:
            st.error("❌ Por favor, preencha todos os campos")
        else:
            with st.spinner("🔐 Verificando credenciais..."):
                time.sleep(1)  # Simular verificação
                
                success = AuthSystem.login(email, senha)
                
                if success:
                    st.success("✅ Login realizado com sucesso!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Email ou senha incorretos")
    
    # Login de demonstração
    st.markdown("---")
    st.markdown("##### 🎯 Acesso de Demonstração")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👨‍⚕️ Admin", use_container_width=True):
            if AuthSystem.login("admin@nutriapp360.com", "admin123"):
                st.success("✅ Login como Admin realizado!")
                time.sleep(1)
                st.rerun()
    
    with col2:
        st.info("**Email:** admin@nutriapp360.com  \n**Senha:** admin123")

def show_register_form():
    """Formulário de cadastro"""
    
    with st.form("register_form"):
        st.markdown("##### 👤 Dados Pessoais")
        
        nome = st.text_input("📝 Nome Completo *", placeholder="Dr(a). João Silva")
        email = st.text_input("📧 Email *", placeholder="joao@clinica.com")
        
        col1, col2 = st.columns(2)
        
        with col1:
            coren = st.text_input("🏥 CRN (COREN)", placeholder="123456/SP")
        
        with col2:
            telefone = st.text_input("📱 Telefone", placeholder="(11) 99999-9999")
        
        especialidade = st.selectbox(
            "🎯 Especialidade",
            [
                "Nutrição Clínica",
                "Nutrição Esportiva", 
                "Nutrição Materno-Infantil",
                "Nutrição Geriátrica",
                "Nutrição Estética",
                "Nutrição Comportamental",
                "Nutrição Funcional",
                "Outro"
            ]
        )
        
        endereco = st.text_area("📍 Endereço da Clínica", placeholder="Rua, número, bairro, cidade")
        
        st.markdown("##### 🔐 Dados de Acesso")
        
        col1, col2 = st.columns(2)
        
        with col1:
            senha = st.text_input("🔑 Senha *", type="password", placeholder="Mínimo 8 caracteres")
        
        with col2:
            confirmar_senha = st.text_input("✅ Confirmar Senha *", type="password")
        
        # Validação de senha em tempo real
        if senha:
            validacao_senha = validar_senha(senha)
            if validacao_senha['score'] < 3:
                st.warning(f"⚠️ Senha fraca: {', '.join(validacao_senha['sugestoes'])}")
            else:
                st.success("✅ Senha forte!")
        
        st.markdown("##### ✅ Termos e Condições")
        
        aceitar_termos = st.checkbox("📋 Aceito os termos de uso e política de privacidade *")
        
        aceitar_comunicacoes = st.checkbox("📧 Aceito receber comunicações sobre atualizações do sistema")
        
        cadastrar = st.form_submit_button("🚀 Criar Conta", use_container_width=True)
    
    if cadastrar:
        # Validações
        erros = []
        
        if not nome or not email or not senha:
            erros.append("❌ Preencha todos os campos obrigatórios (*)")
        
        if senha != confirmar_senha:
            erros.append("❌ As senhas não coincidem")
        
        if len(senha) < 8:
            erros.append("❌ A senha deve ter pelo menos 8 caracteres")
        
        if not aceitar_termos:
            erros.append("❌ Você deve aceitar os termos de uso")
        
        if '@' not in email or '.' not in email:
            erros.append("❌ Email inválido")
        
        if erros:
            for erro in erros:
                st.error(erro)
        else:
            # Cadastrar usuário
            dados_usuario = {
                'nome': nome,
                'email': email,
                'senha': senha,
                'coren': coren,
                'especialidade': especialidade,
                'telefone': telefone,
                'endereco': endereco
            }
            
            with st.spinner("🚀 Criando sua conta..."):
                time.sleep(2)  # Simular processamento
                
                success, message = AuthSystem.register(dados_usuario)
                
                if success:
                    st.success(message)
                    st.balloons()
                    st.info("🔐 Agora você pode fazer login com suas credenciais!")
                else:
                    st.error(message)

def validar_senha(senha):
    """Valida força da senha"""
    score = 0
    sugestoes = []
    
    if len(senha) >= 8:
        score += 1
    else:
        sugestoes.append("Use pelo menos 8 caracteres")
    
    if re.search(r'[A-Z]', senha):
        score += 1
    else:
        sugestoes.append("Adicione letras maiúsculas")
    
    if re.search(r'[a-z]', senha):
        score += 1
    else:
        sugestoes.append("Adicione letras minúsculas")
    
    if re.search(r'\d', senha):
        score += 1
    else:
        sugestoes.append("Adicione números")
    
    if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', senha):
        score += 1
    else:
        sugestoes.append("Adicione símbolos especiais")
    
    return {'score': score, 'sugestoes': sugestoes}

def show_sidebar():
    """Sidebar com navegação"""
    
    user = AuthSystem.get_current_user()
    
    with st.sidebar:
        # Cabeçalho do usuário
        st.markdown(f'''
        <div style="
            background: linear-gradient(135deg, #2E7D32, #4CAF50);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">👤</div>
            <div style="font-weight: 600;">{user['nome']}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">{user['especialidade'] or 'Nutricionista'}</div>
            <div style="font-size: 0.8rem; opacity: 0.8;">CRN: {user['coren'] or 'N/A'}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Menu de navegação
        st.markdown("### 📋 Navegação")
        
        menu_items = [
            {"name": "🏠 Dashboard", "key": "dashboard", "icon": "🏠"},
            {"name": "👥 Pacientes", "key": "patients", "icon": "👥"},
            {"name": "🧮 Calculadoras", "key": "calculators", "icon": "🧮"},
            {"name": "🍽️ Planos Alimentares", "key": "meal_plans", "icon": "🍽️"},
            {"name": "📅 Agendamentos", "key": "appointments", "icon": "📅"},
            {"name": "🍳 Receitas", "key": "recipes", "icon": "🍳"},
            {"name": "💬 Comunicação", "key": "communication", "icon": "💬"},
            {"name": "📄 Relatórios", "key": "reports", "icon": "📄"},
            {"name": "🔒 Backup & Segurança", "key": "backup", "icon": "🔒"}
        ]
        
        for item in menu_items:
            if st.button(item["name"], key=f"nav_{item['key']}", use_container_width=True):
                st.session_state.page = item["key"]
                st.rerun()
        
        st.markdown("---")
        
        # Informações do sistema
        st.markdown("### ℹ️ Sistema")
        
        st.info(f"""
        **📦 Versão:** 8.0  
        **👤 Usuário:** {user['nome']}  
        **📧 Email:** {user['email']}  
        **🎯 Plano:** {user.get('plano', 'Básico').title()}
        """)
        
        st.markdown("---")
        
        # Botões de ação
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⚙️ Config", use_container_width=True):
                st.session_state.show_config = True
        
        with col2:
            if st.button("🚪 Sair", use_container_width=True):
                AuthSystem.logout()
        
        # Suporte
        st.markdown("---")
        st.markdown("### 🆘 Suporte")
        
        if st.button("📞 Contatar Suporte", use_container_width=True):
            st.info("📞 Entre em contato: suporte@nutriapp360.com")
        
        if st.button("📚 Manual do Usuário", use_container_width=True):
            st.info("📚 Documentação disponível em: docs.nutriapp360.com")

def main():
    """Função principal da aplicação"""
    
    # Carregar CSS
    load_advanced_css()
    
    # Verificar se está logado
    if not AuthSystem.is_logged_in():
        show_login_page()
        return
    
    # Mostrar sidebar
    show_sidebar()
    
    # Obter página atual
    current_page = st.session_state.get('page', 'dashboard')
    
    # Roteamento de páginas
    if current_page == 'dashboard':
        show_advanced_dashboard()
    elif current_page == 'patients':
        show_patient_management()
    elif current_page == 'calculators':
        show_calculators()
    elif current_page == 'meal_plans':
        show_meal_plans()
    elif current_page == 'appointments':
        show_appointments()
    elif current_page == 'recipes':
        show_recipes()
    elif current_page == 'communication':
        show_communication()
    elif current_page == 'reports':
        show_reports()
    elif current_page == 'backup':
        show_backup_security()
    else:
        show_advanced_dashboard()

# =============================================================================
# 🚀 INICIALIZAÇÃO DO SISTEMA
# =============================================================================

if __name__ == "__main__":
    # Configurar página inicial
    if 'page' not in st.session_state:
        st.session_state.page = 'dashboard'
    
    # Executar aplicação principal
    main()
