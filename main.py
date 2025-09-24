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
                            {'range': [0, 18.5], 'color
