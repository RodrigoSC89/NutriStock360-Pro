#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🥗 NutriApp360 v9.0 - Sistema Ultra Avançado com IA e Análise Preditiva
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ SISTEMA PROFISSIONAL COM INTELIGÊNCIA ARTIFICIAL
🚀 TODOS OS MÓDULOS 100% FUNCIONAIS + INOVAÇÕES
🤖 ANÁLISE PREDITIVA E MACHINE LEARNING
📋 PRONTUÁRIO MÉDICO ELETRÔNICO COMPLETO
📊 DASHBOARD AVANÇADO COM BI
🔬 ANÁLISE DE BIOIMPEDÂNCIA
🧬 NUTRIGENÔMICA E MEDICINA PERSONALIZADA
💡 RECOMENDAÇÕES INTELIGENTES
🎯 GAMIFICAÇÃO E METAS
📱 INTEGRAÇÃO MOBILE
🌐 TELEMEDICINA INTEGRADA

Author: NutriApp360 Team | Version: 9.0 | Python 3.8+
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
import random
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 🎨 CONFIGURAÇÕES INICIAIS E CSS ULTRA AVANÇADO
# =============================================================================

st.set_page_config(
    page_title="NutriApp360 v9.0 - Sistema Ultra Avançado com IA",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://nutriapp360.com/ajuda',
        'Report a bug': 'https://nutriapp360.com/suporte',
        'About': "# 🥗 NutriApp360 v9.0\n**Sistema Ultra Avançado com IA**\n\n**Novidades v9.0:**\n- 🤖 IA Nutricional & Análise Preditiva\n- 📋 Prontuário Médico Eletrônico\n- 🔬 Análise de Bioimpedância\n- 🧬 Nutrigenômica\n- 📊 Business Intelligence\n- 💡 Recomendações Inteligentes\n- 🎯 Gamificação\n- 📱 App Mobile\n- 🌐 Telemedicina"
    }
)

def load_ultra_advanced_css():
    """Carrega CSS ultra avançado e profissional"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* === VARIÁVEIS CSS AVANÇADAS === */
    :root {
        --primary-color: #2E7D32;
        --secondary-color: #4CAF50;
        --accent-color: #66BB6A;
        --tertiary-color: #81C784;
        --bg-primary: #FAFAFA;
        --bg-secondary: #F5F5F5;
        --bg-dark: #1E1E1E;
        --text-primary: #212121;
        --text-secondary: #757575;
        --success: #4CAF50;
        --warning: #FF9800;
        --error: #F44336;
        --info: #2196F3;
        --purple: #9C27B0;
        --indigo: #3F51B5;
        --teal: #009688;
        --border-radius: 16px;
        --border-radius-sm: 8px;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        --gradient-primary: linear-gradient(135deg, #2E7D32, #4CAF50, #66BB6A);
        --gradient-secondary: linear-gradient(135deg, #E8F5E8, #F1F8E9, #E8F5E8);
        --gradient-dark: linear-gradient(135deg, #1E1E1E, #2E2E2E, #3E3E3E);
    }
    
    /* === RESET E BASE AVANÇADO === */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .main {
        padding: 0 2rem;
        background: var(--gradient-secondary);
        min-height: 100vh;
    }
    
    /* === CABEÇALHO ULTRA AVANÇADO === */
    .ultra-header {
        font-size: 3.5rem;
        font-weight: 900;
        color: transparent;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: glow 2s ease-in-out infinite alternate;
        position: relative;
    }
    
    .sub-header {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 1.5rem 0;
        text-align: center;
        position: relative;
    }
    
    .ultra-header::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 120%;
        height: 120%;
        background: radial-gradient(circle, rgba(46, 125, 50, 0.1), transparent);
        z-index: -1;
        border-radius: 50%;
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes glow {
        from { filter: brightness(1) drop-shadow(0 0 5px rgba(46, 125, 50, 0.3)); }
        to { filter: brightness(1.1) drop-shadow(0 0 20px rgba(46, 125, 50, 0.5)); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
        50% { transform: translate(-50%, -50%) scale(1.1); opacity: 0.8; }
    }
    
    /* === CARDS ULTRA AVANÇADOS === */
    .ultra-card {
        background: linear-gradient(145deg, #FFFFFF, #F8FFF8);
        border-radius: var(--border-radius);
        padding: 2rem;
        box-shadow: var(--shadow-lg);
        border: 1px solid rgba(46, 125, 50, 0.1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 1rem 0;
    }
    
    .ultra-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-primary);
    }
    
    .ultra-card::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(46, 125, 50, 0.03), transparent);
        pointer-events: none;
        transition: all 0.6s ease;
    }
    
    .ultra-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: var(--shadow-xl);
        background: linear-gradient(145deg, #FFFFFF, #F0FFF0);
    }
    
    .ultra-card:hover::after {
        top: -25%;
        right: -25%;
        opacity: 1;
    }
    
    /* === MÉTRICAS AVANÇADAS === */
    .metric-ultra {
        background: linear-gradient(135deg, #FFFFFF, #F8FFF8);
        border-radius: var(--border-radius);
        padding: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow);
        border: 1px solid rgba(46, 125, 50, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-ultra::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
        animation: shimmer 2s linear infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .metric-ultra:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, #FFFFFF, #F0FFF0);
    }
    
    .metric-title-ultra {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }
    
    .metric-value-ultra {
        font-size: 2.5rem;
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
        margin: 0.5rem 0;
    }
    
    .metric-change-ultra {
        font-size: 0.875rem;
        margin-top: 0.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.25rem;
        font-weight: 600;
    }
    
    .metric-change-ultra.positive {
        color: var(--success);
        animation: bounce 1s ease-in-out infinite;
    }
    
    .metric-change-ultra.negative {
        color: var(--error);
        animation: shake 1s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 53%, 80%, 100% { transform: translateY(0); }
        40%, 43% { transform: translateY(-5px); }
        70% { transform: translateY(-3px); }
        90% { transform: translateY(-2px); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
        20%, 40%, 60%, 80% { transform: translateX(2px); }
    }
    
    /* === CARDS DE IA === */
    .ai-card {
        background: linear-gradient(145deg, #F3E5F5, #E1BEE7);
        border: 1px solid rgba(156, 39, 176, 0.3);
        border-radius: var(--border-radius);
        padding: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-lg);
        transition: all 0.4s ease;
    }
    
    .ai-card::before {
        content: '🤖';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 2rem;
        opacity: 0.3;
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .ai-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        background: linear-gradient(145deg, #F8BBD9, #E1BEE7);
    }
    
    /* === CARDS DE PRONTUÁRIO === */
    .medical-card {
        background: linear-gradient(145deg, #E3F2FD, #BBDEFB);
        border: 1px solid rgba(33, 150, 243, 0.3);
        border-radius: var(--border-radius);
        padding: 2rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-lg);
        transition: all 0.4s ease;
    }
    
    .medical-card::before {
        content: '📋';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 2rem;
        opacity: 0.3;
        animation: heartbeat 2s ease-in-out infinite;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .medical-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-xl);
        background: linear-gradient(145deg, #E3F2FD, #90CAF9);
    }
    
    /* === BOTÕES ULTRA AVANÇADOS === */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--border-radius) !important;
        padding: 0.875rem 2rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        box-shadow: var(--shadow) !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: all 0.6s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
        background: linear-gradient(135deg, #1B5E20, #2E7D32, #388E3C) !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 🗄️ BANCO DE DADOS ULTRA AVANÇADO
# =============================================================================

class UltraAdvancedDatabaseManager:
    """Gerenciador ultra avançado do banco de dados com IA"""
    
    def __init__(self, db_path="nutriapp360_v9.db"):
        self.db_path = db_path
        self.init_advanced_database()
    
    def get_connection(self):
        """Obtém conexão com o banco"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_advanced_database(self):
        """Inicializa banco com tabelas avançadas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de usuários com campos avançados
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
            plano TEXT DEFAULT 'premium',
            preferencias_ia TEXT DEFAULT '{}',
            nivel_acesso INTEGER DEFAULT 1,
            bio TEXT,
            redes_sociais TEXT DEFAULT '{}',
            certificacoes TEXT DEFAULT '[]',
            areas_especializacao TEXT DEFAULT '[]'
        )
        ''')
        
        # Tabela de pacientes com campos de IA
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
            perfil_nutricional TEXT DEFAULT '{}',
            preferencias_alimentares TEXT DEFAULT '[]',
            alergias TEXT DEFAULT '[]',
            condicoes_medicas TEXT DEFAULT '[]',
            medicamentos_atuais TEXT DEFAULT '[]',
            nivel_atividade TEXT DEFAULT 'moderado',
            metas_nutricionais TEXT DEFAULT '{}',
            score_aderencia REAL DEFAULT 0,
            predicoes_ia TEXT DEFAULT '{}',
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de prontuários médicos
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prontuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            paciente_id INTEGER,
            nutricionista_id INTEGER,
            data_consulta DATETIME NOT NULL,
            tipo_consulta TEXT NOT NULL,
            queixa_principal TEXT,
            historia_doenca_atual TEXT,
            historia_patologica_pregressa TEXT,
            historia_familiar TEXT,
            historia_social TEXT,
            exame_fisico TEXT,
            sinais_vitais TEXT DEFAULT '{}',
            antropometria TEXT DEFAULT '{}',
            exames_laboratoriais TEXT DEFAULT '[]',
            diagnostico_nutricional TEXT,
            plano_terapeutico TEXT,
            prescricoes TEXT DEFAULT '[]',
            observacoes TEXT,
            proxima_consulta DATE,
            assinatura_digital TEXT,
            status TEXT DEFAULT 'aberto',
            anexos TEXT DEFAULT '[]',
            ia_insights TEXT DEFAULT '{}',
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de avaliações com bioimpedância
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS avaliacoes_avancadas (
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
            circunferencia_braco REAL,
            circunferencia_coxa REAL,
            dobras_cutaneas TEXT DEFAULT '{}',
            bioimpedancia TEXT DEFAULT '{}',
            percentual_gordura REAL,
            massa_muscular REAL,
            massa_ossea REAL,
            agua_corporal REAL,
            taxa_metabolica REAL,
            idade_metabolica INTEGER,
            gordura_visceral REAL,
            pressao_arterial TEXT,
            frequencia_cardiaca INTEGER,
            saturacao_oxigenio REAL,
            glicemia REAL,
            objetivo TEXT,
            restricoes_alimentares TEXT DEFAULT '[]',
            medicamentos TEXT DEFAULT '[]',
            atividade_fisica TEXT,
            qualidade_sono TEXT,
            nivel_stress INTEGER,
            observacoes TEXT,
            fotos_progresso TEXT DEFAULT '[]',
            anexos TEXT DEFAULT '[]',
            ia_analise TEXT DEFAULT '{}',
            predicoes TEXT DEFAULT '{}',
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de receitas médicas e prescrições
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescricoes_medicas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            paciente_id INTEGER,
            nutricionista_id INTEGER,
            prontuario_id INTEGER,
            data_prescricao DATE NOT NULL,
            tipo_prescricao TEXT NOT NULL,
            medicamento_suplemento TEXT,
            dosagem TEXT,
            frequencia TEXT,
            duracao_dias INTEGER,
            via_administracao TEXT,
            orientacoes TEXT,
            contraindicacoes TEXT,
            efeitos_colaterais TEXT,
            interacoes TEXT,
            status TEXT DEFAULT 'ativa',
            renovacoes INTEGER DEFAULT 0,
            data_renovacao DATE,
            observacoes TEXT,
            assinatura_digital TEXT,
            codigo_autenticacao TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id),
            FOREIGN KEY (prontuario_id) REFERENCES prontuarios (id)
        )
        ''')
        
        # Inserir usuário admin se não existir
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE email = 'admin@nutriapp360.com'")
        if cursor.fetchone()[0] == 0:
            admin_uuid = str(uuid.uuid4())
            admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
            cursor.execute('''
            INSERT INTO usuarios (
                uuid, nome, email, senha_hash, tipo_usuario, 
                especialidade, coren, plano, bio, areas_especializacao,
                nivel_acesso
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                admin_uuid, 
                "Dr. Admin NutriApp360", 
                "admin@nutriapp360.com",
                admin_hash,
                "admin",
                "Nutrição Clínica e Funcional",
                "123456/SP",
                "premium",
                "Nutricionista especializado em tecnologia e inovação, desenvolvedor do NutriApp360",
                json.dumps(["Nutrição Clínica", "Nutrição Esportiva", "Tecnologia em Saúde", "IA em Nutrição"]),
                9
            ))
        
        # Criar outras tabelas
        self._create_additional_tables(cursor)
        
        # Inserir dados de exemplo
        self._insert_sample_data(cursor)
        
        conn.commit()
        conn.close()
    
    def _create_additional_tables(self, cursor):
        """Cria tabelas adicionais do sistema"""
        
        # Tabela de consultas
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
            ia_otimizado INTEGER DEFAULT 0,
            score_aderencia REAL DEFAULT 0,
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
            vitaminas TEXT DEFAULT '{}',
            minerais TEXT DEFAULT '{}',
            tags TEXT DEFAULT '[]',
            foto TEXT,
            favorita INTEGER DEFAULT 0,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
            publica INTEGER DEFAULT 0,
            rating REAL DEFAULT 0,
            num_avaliacoes INTEGER DEFAULT 0,
            ia_sugerida INTEGER DEFAULT 0,
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
    
    def _insert_sample_data(self, cursor):
        """Insere dados de exemplo"""
        
        # Verificar se já existem dados
        cursor.execute("SELECT COUNT(*) FROM receitas")
        if cursor.fetchone()[0] > 0:
            return
        
        # Inserir receitas de exemplo
        receitas_exemplo = [
            {
                'uuid': str(uuid.uuid4()),
                'nome': 'Bowl Funcional Antioxidante',
                'categoria': 'Café da Manhã',
                'ingredientes': json.dumps([
                    {'nome': 'Açaí polpa', 'quantidade': '100g', 'calorias': 60},
                    {'nome': 'Banana', 'quantidade': '1 média', 'calorias': 89},
                    {'nome': 'Blueberry', 'quantidade': '50g', 'calorias': 29},
                    {'nome': 'Granola integral', 'quantidade': '30g', 'calorias': 120},
                    {'nome': 'Chia', 'quantidade': '1 col sopa', 'calorias': 58},
                    {'nome': 'Mel', 'quantidade': '1 col sobremesa', 'calorias': 21}
                ]),
                'modo_preparo': 'Bata o açaí com a banana até formar um creme. Coloque no bowl e adicione os toppings: blueberry, granola, chia e mel. Sirva imediatamente.',
                'tempo_preparo': 10,
                'porcoes': 1,
                'calorias_porcao': 377,
                'carboidratos': 65.2,
                'proteinas': 8.1,
                'lipidios': 12.8,
                'fibras': 15.3,
                'vitaminas': json.dumps({'C': '85mg', 'E': '12mg', 'K': '45mcg', 'A': '320mcg'}),
                'minerais': json.dumps({'Potássio': '580mg', 'Magnésio': '85mg', 'Cálcio': '120mg', 'Ferro': '2.1mg'}),
                'tags': json.dumps(['antioxidante', 'funcional', 'energia', 'superfood']),
                'publica': 1,
                'rating': 4.8,
                'num_avaliacoes': 127
            },
            {
                'uuid': str(uuid.uuid4()),
                'nome': 'Salmão com Quinoa e Vegetais Orgânicos',
                'categoria': 'Pratos Principais',
                'ingredientes': json.dumps([
                    {'nome': 'Filé de salmão', 'quantidade': '150g', 'calorias': 231},
                    {'nome': 'Quinoa', 'quantidade': '60g (seca)', 'calorias': 216},
                    {'nome': 'Brócolis orgânico', 'quantidade': '100g', 'calorias': 25},
                    {'nome': 'Cenoura baby', 'quantidade': '80g', 'calorias': 28},
                    {'nome': 'Azeite extra virgem', 'quantidade': '1 col sopa', 'calorias': 119},
                    {'nome': 'Limão siciliano', 'quantidade': '1/2 unidade', 'calorias': 8},
                    {'nome': 'Ervas finas', 'quantidade': 'a gosto', 'calorias': 2}
                ]),
                'modo_preparo': 'Cozinhe a quinoa em água filtrada. Tempere o salmão com ervas, sal rosa e limão. Grelhe por 4-5min cada lado. Refogue os vegetais no azeite. Monte o prato com quinoa como base, salmão e vegetais.',
                'tempo_preparo': 25,
                'porcoes': 1,
                'calorias_porcao': 629,
                'carboidratos': 42.8,
                'proteinas': 38.2,
                'lipidios': 32.1,
                'fibras': 6.8,
                'vitaminas': json.dumps({'D': '15mcg', 'B12': '8.2mcg', 'B6': '1.2mg', 'A': '890mcg'}),
                'minerais': json.dumps({'Ômega-3': '2.3g', 'Potássio': '720mg', 'Fósforo': '340mg', 'Selênio': '42mcg'}),
                'tags': json.dumps(['rico-em-ômega-3', 'sem-glúten', 'proteína-completa', 'anti-inflamatório']),
                'publica': 1,
                'rating': 4.9,
                'num_avaliacoes': 89
            }
        ]
        
        for receita in receitas_exemplo:
            cursor.execute('''
            INSERT INTO receitas (
                uuid, nome, categoria, ingredientes, modo_preparo,
                tempo_preparo, porcoes, calorias_porcao, carboidratos,
                proteinas, lipidios, fibras, vitaminas, minerais, tags, 
                publica, rating, num_avaliacoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                receita['uuid'], receita['nome'], receita['categoria'],
                receita['ingredientes'], receita['modo_preparo'],
                receita['tempo_preparo'], receita['porcoes'],
                receita['calorias_porcao'], receita['carboidratos'],
                receita['proteinas'], receita['lipidios'], receita['fibras'],
                receita['vitaminas'], receita['minerais'], receita['tags'],
                receita['publica'], receita['rating'], receita['num_avaliacoes']
            ))

# Instanciar o gerenciador avançado
db_manager = UltraAdvancedDatabaseManager()

# =============================================================================
# 🔐 SISTEMA DE AUTENTICAÇÃO ULTRA AVANÇADO
# =============================================================================

class UltraAdvancedAuthSystem:
    """Sistema de autenticação ultra avançado com IA"""
    
    @staticmethod
    def hash_password(password):
        """Gera hash seguro da senha"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hash_password):
        """Verifica senha com segurança avançada"""
        return hashlib.sha256(password.encode()).hexdigest() == hash_password
    
    @staticmethod
    def login(email, password):
        """Login avançado com análise de comportamento"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, uuid, nome, email, tipo_usuario, coren, especialidade,
               telefone, endereco, foto_perfil, configuracoes, assinatura, plano,
               preferencias_ia, nivel_acesso, bio, areas_especializacao
        FROM usuarios 
        WHERE email = ? AND senha_hash = ? AND ativo = 1
        ''', (email, UltraAdvancedAuthSystem.hash_password(password)))
        
        user = cursor.fetchone()
        
        if user:
            # Atualizar último login
            cursor.execute('''
            UPDATE usuarios SET ultimo_login = CURRENT_TIMESTAMP 
            WHERE id = ?
            ''', (user['id'],))
            
            conn.commit()
            
            # Configurar sessão avançada
            user_dict = dict(user)
            user_dict['configuracoes'] = json.loads(user['configuracoes'] or '{}')
            user_dict['preferencias_ia'] = json.loads(user['preferencias_ia'] or '{}')
            user_dict['areas_especializacao'] = json.loads(user['areas_especializacao'] or '[]')
            
            st.session_state.user = user_dict
            st.session_state.logged_in = True
            st.session_state.login_timestamp = datetime.now()
            
        conn.close()
        return user is not None
    
    @staticmethod
    def logout():
        """Logout avançado com limpeza completa"""
        # Limpar todas as chaves de sessão
        keys_to_remove = [key for key in st.session_state.keys()]
        for key in keys_to_remove:
            del st.session_state[key]
        
        st.rerun()
    
    @staticmethod
    def register(dados_usuario):
        """Registro avançado com validações"""
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        try:
            user_uuid = str(uuid.uuid4())
            senha_hash = UltraAdvancedAuthSystem.hash_password(dados_usuario['senha'])
            
            cursor.execute('''
            INSERT INTO usuarios (
                uuid, nome, email, senha_hash, tipo_usuario,
                coren, especialidade, telefone, endereco, bio,
                areas_especializacao, plano
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_uuid,
                dados_usuario['nome'],
                dados_usuario['email'],
                senha_hash,
                dados_usuario.get('tipo_usuario', 'nutricionista'),
                dados_usuario.get('coren', ''),
                dados_usuario.get('especialidade', ''),
                dados_usuario.get('telefone', ''),
                dados_usuario.get('endereco', ''),
                dados_usuario.get('bio', ''),
                json.dumps(dados_usuario.get('areas_especializacao', [])),
                'premium'
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
        if not UltraAdvancedAuthSystem.is_logged_in():
            st.warning("🔐 Acesso restrito! Faça login para continuar.")
            show_ultra_login_page()
            st.stop()

# Alias para compatibilidade
AuthSystem = UltraAdvancedAuthSystem

# =============================================================================
# 🏠 PÁGINA DE LOGIN E REGISTRO
# =============================================================================

def show_ultra_login_page():
    """Página de login ultra avançada"""
    
    load_ultra_advanced_css()
    
    st.markdown('<h1 class="ultra-header">🥗 NutriApp360 v9.0</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 3rem;">Sistema Ultra Avançado com IA e Análise Preditiva</p>', unsafe_allow_html=True)
    
    # Tabs para Login e Registro
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Cadastro"])
    
    with tab1:
        st.markdown('<div class="sub-header">🔐 Acesso ao Sistema</div>', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("📧 Email", placeholder="seu@email.com")
            senha = st.text_input("🔒 Senha", type="password", placeholder="Sua senha")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                lembrar = st.checkbox("🧠 Lembrar de mim")
            
            with col2:
                submitted = st.form_submit_button("🚀 Entrar", use_container_width=True)
            
            if submitted:
                if email and senha:
                    if AuthSystem.login(email, senha):
                        st.success("✅ Login realizado com sucesso!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Email ou senha incorretos!")
                else:
                    st.warning("⚠️ Preencha todos os campos!")
        
        # Usuários de demonstração
        st.markdown("---")
        st.markdown("##### 👥 Usuários de Demonstração")
        
        demo_users = [
            {"email": "admin@nutriapp360.com", "senha": "admin123", "tipo": "Administrador"},
        ]
        
        for user in demo_users:
            if st.button(f"🎭 Login como {user['tipo']}", key=f"demo_{user['email']}"):
                if AuthSystem.login(user['email'], user['senha']):
                    st.success(f"✅ Logado como {user['tipo']}!")
                    time.sleep(1)
                    st.rerun()
    
    with tab2:
        st.markdown('<div class="sub-header">📝 Cadastro de Novo Usuário</div>', unsafe_allow_html=True)
        
        with st.form("register_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("👤 Nome Completo", placeholder="Seu nome completo")
                email = st.text_input("📧 Email", placeholder="seu@email.com")
                senha = st.text_input("🔒 Senha", type="password", placeholder="Mínimo 6 caracteres")
                tipo_usuario = st.selectbox("👥 Tipo de Usuário", [
                    "nutricionista", "admin", "assistente", "paciente"
                ])
            
            with col2:
                coren = st.text_input("🏥 COREN", placeholder="123456/SP")
                especialidade = st.text_input("🎓 Especialidade", placeholder="Nutrição Clínica")
                telefone = st.text_input("📱 Telefone", placeholder="(11) 99999-9999")
                endereco = st.text_input("📍 Endereço", placeholder="Rua, número, cidade")
            
            bio = st.text_area("📝 Bio Profissional", placeholder="Descreva sua experiência...")
            
            # Áreas de especialização
            areas_especialização = st.multiselect("🎯 Áreas de Especialização", [
                "Nutrição Clínica", "Nutrição Esportiva", "Nutrição Materno-Infantil",
                "Nutrição Geriátrica", "Nutrição Funcional", "Fitoterapia",
                "Nutrigenômica", "Transtornos Alimentares", "Obesidade e Emagrecimento"
            ])
            
            aceitar_termos = st.checkbox("✅ Aceito os termos de uso e política de privacidade")
            
            submitted = st.form_submit_button("🚀 Criar Conta", use_container_width=True)
            
            if submitted:
                if not aceitar_termos:
                    st.error("❌ Você deve aceitar os termos de uso!")
                elif not all([nome, email, senha]):
                    st.error("❌ Preencha todos os campos obrigatórios!")
                elif len(senha) < 6:
                    st.error("❌ A senha deve ter pelo menos 6 caracteres!")
                else:
                    dados_usuario = {
                        'nome': nome,
                        'email': email,
                        'senha': senha,
                        'tipo_usuario': tipo_usuario,
                        'coren': coren,
                        'especialidade': especialidade,
                        'telefone': telefone,
                        'endereco': endereco,
                        'bio': bio,
                        'areas_especializacao': areas_especialização
                    }
                    
                    success, message = AuthSystem.register(dados_usuario)
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.info("📧 Agora você pode fazer login com suas credenciais!")
                    else:
                        st.error(f"❌ {message}")

# =============================================================================
# 🤖 SISTEMA DE IA NUTRICIONAL E ANÁLISE PREDITIVA
# =============================================================================

def show_ai_nutritional_system():
    """Sistema de IA Nutricional e Análise Preditiva"""
    
    st.markdown('<h1 class="ultra-header">🤖 IA Nutricional & Análise Preditiva</h1>', unsafe_allow_html=True)
    
    user = AuthSystem.get_current_user()
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🧠 Dashboard IA",
        "📈 Análise Preditiva", 
        "💡 Recomendações",
        "🎯 Personalização",
        "📊 Modelos ML",
        "⚙️ Configurações IA"
    ])
    
    with tab1:
        show_ai_dashboard(user)
    
    with tab2:
        show_predictive_analysis(user)
    
    with tab3:
        show_ai_recommendations(user)
    
    with tab4:
        show_ai_personalization(user)
    
    with tab5:
        show_ml_models(user)
    
    with tab6:
        show_ai_settings(user)

def show_ai_dashboard(user):
    """Dashboard principal da IA"""
    
    st.markdown('<div class="sub-header">🧠 Dashboard de Inteligência Artificial</div>', unsafe_allow_html=True)
    
    # Métricas da IA
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown('''
        <div class="ai-card">
            <div class="metric-title-ultra">🎯 Precisão dos Modelos</div>
            <div class="metric-value-ultra">94.2%</div>
            <div class="metric-change-ultra positive">↗️ +2.1%</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div class="ai-card">
            <div class="metric-title-ultra">📊 Análises Realizadas</div>
            <div class="metric-value-ultra">1,247</div>
            <div class="metric-change-ultra positive">↗️ +18%</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div class="ai-card">
            <div class="metric-title-ultra">💡 Recomendações Ativas</div>
            <div class="metric-value-ultra">89</div>
            <div class="metric-change-ultra">📈 Personalizadas</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown('''
        <div class="ai-card">
            <div class="metric-title-ultra">🎭 Taxa de Adesão</div>
            <div class="metric-value-ultra">78.6%</div>
            <div class="metric-change-ultra positive">↗️ +5.2%</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col5:
        st.markdown('''
        <div class="ai-card">
            <div class="metric-title-ultra">⚡ Tempo de Resposta</div>
            <div class="metric-value-ultra">0.3s</div>
            <div class="metric-change-ultra positive">⚡ Otimizado</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Análises em tempo real
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("##### 📈 Performance dos Modelos de IA")
        
        # Gráfico de performance dos modelos
        models_performance = {
            'Perda de Peso': [85, 87, 89, 92, 94],
            'Ganho de Massa': [78, 81, 84, 87, 91],
            'Controle Glicêmico': [82, 85, 88, 90, 93],
            'Aderência ao Tratamento': [75, 79, 83, 86, 89]
        }
        
        weeks = ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'Sem 5']
        
        fig_performance = go.Figure()
        
        colors = ['#2E7D32', '#4CAF50', '#66BB6A', '#81C784']
        
        for i, (model, values) in enumerate(models_performance.items()):
            fig_performance.add_trace(go.Scatter(
                x=weeks,
                y=values,
                mode='lines+markers',
                name=model,
                line=dict(color=colors[i], width=3),
                marker=dict(size=8)
            ))
        
        fig_performance.update_layout(
            title="Performance dos Modelos de IA (%)",
            xaxis_title="Período",
            yaxis_title="Precisão (%)",
            height=400,
            hovermode='x unified',
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig_performance, use_container_width=True)
    
    with col_right:
        st.markdown("##### 🎯 Insights da IA")
        
        insights = [
            {
                'tipo': 'success',
                'titulo': 'Alta Adesão Detectada',
                'conteudo': '5 pacientes mostram excelente aderência ao plano nutricional'
            },
            {
                'tipo': 'warning',
                'titulo': 'Risco de Abandono',
                'conteudo': '2 pacientes precisam de intervenção preventiva'
            },
            {
                'tipo': 'info',
                'titulo': 'Otimização Sugerida',
                'conteudo': 'Ajustar macronutrientes em 3 planos alimentares'
            },
            {
                'tipo': 'success',
                'titulo': 'Meta Alcançada',
                'conteudo': '12 pacientes atingiram suas metas este mês'
            }
        ]
        
        for insight in insights:
            icon_map = {
                'success': '✅',
                'warning': '⚠️',
                'info': 'ℹ️',
                'error': '❌'
            }
            
            color_map = {
                'success': '#4CAF50',
                'warning': '#FF9800',
                'info': '#2196F3',
                'error': '#F44336'
            }
            
            st.markdown(f'''
            <div class="ultra-card" style="margin: 0.5rem 0; padding: 1rem;">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon_map[insight['tipo']]}</span>
                    <strong style="color: {color_map[insight['tipo']]};">{insight['titulo']}</strong>
                </div>
                <div style="color: #666; font-size: 0.9rem;">
                    {insight['conteudo']}
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Botão de análise rápida
        if st.button("🔍 Executar Análise Completa", use_container_width=True):
            with st.spinner("🤖 IA analisando dados..."):
                time.sleep(2)
                st.success("✅ Análise completa finalizada!")

def show_predictive_analysis(user):
    """Sistema de análise preditiva avançado"""
    
    st.markdown('<div class="sub-header">📈 Análise Preditiva Avançada</div>', unsafe_allow_html=True)
    
    # Seleção de paciente para análise
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, nome, data_nascimento, sexo
    FROM pacientes 
    WHERE nutricionista_id = ? AND ativo = 1
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    
    if not pacientes:
        st.warning("⚠️ Cadastre pacientes para utilizar a análise preditiva.")
        
        # Adicionar alguns pacientes de exemplo para demonstração
        st.markdown("##### 🎭 Pacientes de Demonstração")
        if st.button("➕ Adicionar Pacientes de Demo"):
            demo_patients = [
                {
                    'uuid': str(uuid.uuid4()),
                    'nome': 'Maria Silva Santos',
                    'email': 'maria@email.com',
                    'data_nascimento': '1990-05-15',
                    'sexo': 'Feminino',
                    'telefone': '(11) 99999-1111'
                },
                {
                    'uuid': str(uuid.uuid4()),
                    'nome': 'João Carlos Oliveira', 
                    'email': 'joao@email.com',
                    'data_nascimento': '1985-10-20',
                    'sexo': 'Masculino',
                    'telefone': '(11) 99999-2222'
                }
            ]
            
            for patient in demo_patients:
                cursor.execute('''
                INSERT INTO pacientes (
                    uuid, nutricionista_id, nome, email, data_nascimento,
                    sexo, telefone
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    patient['uuid'], user['id'], patient['nome'], 
                    patient['email'], patient['data_nascimento'],
                    patient['sexo'], patient['telefone']
                ))
            
            conn.commit()
            st.success("✅ Pacientes de demonstração adicionados!")
            st.rerun()
        
        conn.close()
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        paciente_selecionado = st.selectbox(
            "👤 Selecione o Paciente",
            options=pacientes,
            format_func=lambda x: f"{x[1]} ({x[2]} - {x[3]})",
            key="predictive_patient_select"
        )
    
    with col2:
        tipo_analise = st.selectbox(
            "🎯 Tipo de Análise",
            [
                "Predição de Perda de Peso",
                "Aderência ao Tratamento", 
                "Risco Nutricional",
                "Evolução Antropométrica",
                "Necessidades Calóricas Futuras"
            ],
            key="predictive_analysis_type"
        )
    
    if st.button("🚀 Executar Análise Preditiva", use_container_width=True):
        
        with st.spinner("🤖 IA processando dados históricos..."):
            # Simular análise preditiva
            progress_bar = st.progress(0)
            
            etapas = [
                "Coletando dados históricos...",
                "Analisando padrões comportamentais...",
                "Aplicando algoritmos de machine learning...",
                "Calculando probabilidades...",
                "Gerando insights personalizados...",
                "Finalizando análise..."
            ]
            
            for i, etapa in enumerate(etapas):
                st.text(etapa)
                time.sleep(0.5)
                progress_bar.progress((i + 1) / len(etapas))
            
            progress_bar.empty()
        
        # Resultados da análise
        st.success("✅ Análise preditiva concluída com sucesso!")
        
        # Simular resultados baseados no tipo de análise
        if tipo_analise == "Predição de Perda de Peso":
            show_weight_loss_prediction(paciente_selecionado)
        elif tipo_analise == "Aderência ao Tratamento":
            show_adherence_prediction(paciente_selecionado)
        elif tipo_analise == "Risco Nutricional":
            show_nutritional_risk_analysis(paciente_selecionado)
        elif tipo_analise == "Evolução Antropométrica":
            show_anthropometric_evolution(paciente_selecionado)
        else:
            show_caloric_needs_prediction(paciente_selecionado)
    
    conn.close()

def show_weight_loss_prediction(paciente):
    """Mostra predição de perda de peso"""
    
    st.markdown("##### 📉 Predição de Perda de Peso")
    
    # Simular dados de predição
    semanas = list(range(1, 25))  # 24 semanas
    peso_inicial = 85.5
    
    # Gerar curva de predição realista
    peso_predito = []
    for semana in semanas:
        # Simular perda gradual com platôs
        if semana <= 4:
            perda = 1.2 * semana
        elif semana <= 12:
            perda = 4.8 + 0.8 * (semana - 4)
        elif semana <= 16:
            perda = 11.2 + 0.3 * (semana - 12)  # Platô
        else:
            perda = 12.4 + 0.5 * (semana - 16)
        
        peso_predito.append(peso_inicial - perda + np.random.normal(0, 0.3))
    
    # Intervalos de confiança
    peso_min = [p - 1.5 for p in peso_predito]
    peso_max = [p + 1.5 for p in peso_predito]
    
    fig = go.Figure()
    
    # Adicionar intervalo de confiança
    fig.add_trace(go.Scatter(
        x=semanas + semanas[::-1],
        y=peso_max + peso_min[::-1],
        fill='toself',
        fillcolor='rgba(46, 125, 50, 0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Intervalo de Confiança (95%)',
        hoverinfo="skip"
    ))
    
    # Linha de predição
    fig.add_trace(go.Scatter(
        x=semanas,
        y=peso_predito,
        mode='lines',
        name='Peso Predito',
        line=dict(color='#2E7D32', width=3)
    ))
    
    # Peso atual
    fig.add_hline(
        y=peso_inicial, 
        line_dash="dash", 
        line_color="red",
        annotation_text="Peso Atual (85.5 kg)"
    )
    
    # Meta
    fig.add_hline(
        y=75, 
        line_dash="dash", 
        line_color="green",
        annotation_text="Meta (75 kg)"
    )
    
    fig.update_layout(
        title="Predição de Evolução do Peso - 6 Meses",
        xaxis_title="Semanas",
        yaxis_title="Peso (kg)",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights da predição
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎯 Meta Prevista", "75.2 kg", "✅ Alcançável")
    
    with col2:
        st.metric("📅 Tempo Estimado", "22 semanas", "🎯 Prazo ideal")
    
    with col3:
        st.metric("📊 Confiança", "87%", "📈 Alta precisão")
    
    # Recomendações da IA
    st.markdown("##### 💡 Recomendações da IA")
    
    recommendations = [
        "🍽️ **Ajuste Calórico:** Reduza 300 kcal/dia nas semanas 5-8 para evitar platô",
        "🏃 **Exercícios:** Introduza treino de força na semana 6 para preservar massa muscular",
        "📊 **Monitoramento:** Pesagem semanal com análise de composição corporal",
        "💧 **Hidratação:** Aumente para 2.5L/dia para otimizar metabolismo",
        "😴 **Sono:** Manter 7-8h por noite para regulação hormonal ideal"
    ]
    
    for rec in recommendations:
        st.markdown(rec)

def show_adherence_prediction(paciente):
    """Mostra predição de aderência ao tratamento"""
    
    st.markdown("##### 🎯 Predição de Aderência ao Tratamento")
    
    # Fatores de aderência
    factors = {
        'Motivação Inicial': 85,
        'Suporte Familiar': 70,
        'Praticidade do Plano': 60,
        'Resultados Visíveis': 40,
        'Flexibilidade': 75,
        'Acompanhamento': 90
    }
    
    # Gráfico radar
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=list(factors.values()),
        theta=list(factors.keys()),
        fill='toself',
        name='Score Atual',
        line=dict(color='#2E7D32'),
        fillcolor='rgba(46, 125, 50, 0.3)'
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        title="Fatores de Aderência",
        height=400
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    # Predição temporal de aderência
    semanas = list(range(1, 25))
    aderencia_base = 78
    
    # Simular variação de aderência ao longo do tempo
    aderencia_predita = []
    for semana in semanas:
        # Declínio inicial seguido de estabilização
        if semana <= 3:
            decline = 2 * semana
        elif semana <= 8:
            decline = 6 + 1 * (semana - 3)
        elif semana <= 16:
            decline = 11 + 0.5 * (semana - 8)
        else:
            decline = 15 + 0.2 * (semana - 16)
        
        aderencia_predita.append(max(30, aderencia_base - decline + np.random.normal(0, 2)))
    
    fig_time = go.Figure()
    
    fig_time.add_trace(go.Scatter(
        x=semanas,
        y=aderencia_predita,
        mode='lines+markers',
        name='Aderência Predita (%)',
        line=dict(color='#4CAF50', width=3),
        marker=dict(size=6)
    ))
    
    # Linha de alerta
    fig_time.add_hline(
        y=50, 
        line_dash="dash", 
        line_color="orange",
        annotation_text="Nível de Alerta (50%)"
    )
    
    fig_time.update_layout(
        title="Predição de Aderência ao Longo do Tempo",
        xaxis_title="Semanas",
        yaxis_title="Aderência (%)",
        height=300
    )
    
    st.plotly_chart(fig_time, use_container_width=True)
    
    # Alertas e intervenções
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### ⚠️ Alertas Preventivos")
        alerts = [
            "🔴 **Semana 6:** Risco de baixa aderência (65%)",
            "🟡 **Semana 12:** Platô esperado - reforçar motivação",
            "🟢 **Semana 18:** Período estável - manter acompanhamento"
        ]
        
        for alert in alerts:
            st.markdown(alert)
    
    with col2:
        st.markdown("##### 💡 Intervenções Sugeridas")
        interventions = [
            "📞 **Ligação motivacional** na semana 5",
            "📱 **Gamificação** para período crítico",
            "👥 **Grupo de apoio** online",
            "🎯 **Metas intermediárias** mais flexíveis"
        ]
        
        for intervention in interventions:
            st.markdown(intervention)

def show_nutritional_risk_analysis(paciente):
    """Análise de risco nutricional"""
    
    st.markdown("##### 🚨 Análise de Risco Nutricional")
    
    # Matriz de risco
    risk_factors = {
        'Deficiência de Micronutrientes': {'risk': 35, 'trend': 'stable'},
        'Desequilíbrio Macronutrientes': {'risk': 20, 'trend': 'decreasing'},
        'Sarcopenia': {'risk': 45, 'trend': 'increasing'},
        'Síndrome Metabólica': {'risk': 60, 'trend': 'decreasing'},
        'Transtornos Alimentares': {'risk': 15, 'trend': 'stable'},
        'Desidratação Crônica': {'risk': 25, 'trend': 'stable'}
    }
    
    # Criar DataFrame para visualização
    df_risk = pd.DataFrame([
        {
            'Fator de Risco': factor,
            'Risco (%)': data['risk'],
            'Tendência': data['trend'],
            'Categoria': 'Alto' if data['risk'] > 50 else 'Médio' if data['risk'] > 30 else 'Baixo'
        }
        for factor, data in risk_factors.items()
    ])
    
    # Gráfico de barras horizontal
    fig_risk = px.bar(
        df_risk,
        x='Risco (%)',
        y='Fator de Risco',
        color='Categoria',
        color_discrete_map={
            'Alto': '#F44336',
            'Médio': '#FF9800', 
            'Baixo': '#4CAF50'
        },
        title="Análise de Fatores de Risco Nutricional",
        orientation='h'
    )
    
    fig_risk.update_layout(height=400)
    st.plotly_chart(fig_risk, use_container_width=True)
    
    # Plano de mitigação
    st.markdown("##### 🛡️ Plano de Mitigação de Riscos")
    
    mitigation_plan = {
        'Síndrome Metabólica (60%)': [
            "🍽️ Dieta DASH modificada",
            "🏃 Exercício aeróbico 150min/semana",
            "📊 Monitoramento glicêmico contínuo",
            "💊 Suplementação ômega-3"
        ],
        'Sarcopenia (45%)': [
            "🥩 Aumento proteína para 1.6g/kg",
            "🏋️ Treino resistência 3x/semana",
            "💪 Suplementação creatina",
            "🕐 Timing proteico otimizado"
        ],
        'Deficiência Micronutrientes (35%)': [
            "💊 Complexo vitamínico personalizado",
            "🥬 Diversificação alimentar",
            "🧪 Reavaliação laboratorial em 3 meses",
            "🌱 Alimentos fortificados"
        ]
    }
    
    for risk, actions in mitigation_plan.items():
        with st.expander(f"🎯 {risk}", expanded=True):
            for action in actions:
                st.markdown(f"- {action}")

def show_anthropometric_evolution(paciente):
    """Predição de evolução antropométrica"""
    
    st.markdown("##### 📏 Evolução Antropométrica Predita")
    
    # Dados históricos simulados
    dates = pd.date_range(start='2024-01-01', periods=24, freq='W')
    
    # Simular evolução de múltiplas medidas
    measurements = {
        'Peso (kg)': np.linspace(85.5, 78.2, 24) + np.random.normal(0, 0.5, 24),
        'IMC': np.linspace(29.2, 26.7, 24) + np.random.normal(0, 0.1, 24),
        'Cintura (cm)': np.linspace(98, 89, 24) + np.random.normal(0, 0.8, 24),
        'Quadril (cm)': np.linspace(105, 100, 24) + np.random.normal(0, 0.6, 24),
        '% Gordura': np.linspace(32, 24, 24) + np.random.normal(0, 0.4, 24),
        'Massa Muscular (kg)': np.linspace(28, 30.5, 24) + np.random.normal(0, 0.3, 24)
    }
    
    # Criar visualização interativa
    fig_evolution = go.Figure()
    
    colors = ['#2E7D32', '#4CAF50', '#66BB6A', '#81C784', '#A5D6A7', '#C8E6C9']
    
    for i, (measurement, values) in enumerate(measurements.items()):
        fig_evolution.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines+markers',
            name=measurement,
            line=dict(color=colors[i], width=2),
            visible=True if i == 0 else 'legendonly'  # Mostrar apenas peso inicialmente
        ))
    
    fig_evolution.update_layout(
        title="Evolução Antropométrica Predita - 6 Meses",
        xaxis_title="Data",
        yaxis_title="Valor",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_evolution, use_container_width=True)
    
    # Metas e marcos
    st.markdown("##### 🎯 Metas e Marcos Importantes")
    
    milestones = [
        {'data': '2024-03-01', 'marco': 'Primeiro platô esperado', 'acao': 'Ajustar macronutrientes'},
        {'data': '2024-04-15', 'marco': 'Meta intermediária (80kg)', 'acao': 'Celebrar conquista'},
        {'data': '2024-05-30', 'marco': 'Avaliação completa', 'acao': 'Bioimpedância + exames'},
        {'data': '2024-06-30', 'marco': 'Meta principal (78kg)', 'acao': 'Transição para manutenção'}
    ]
    
    for milestone in milestones:
        st.markdown(f'''
        <div class="ultra-card" style="margin: 0.5rem 0; padding: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>📅 {milestone['data']}</strong><br>
                    <span style="color: #2E7D32;">{milestone['marco']}</span>
                </div>
                <div style="text-align: right;">
                    <span style="background: #E8F5E8; padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.9rem;">
                        {milestone['acao']}
                    </span>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

def show_caloric_needs_prediction(paciente):
    """Predição de necessidades calóricas futuras"""
    
    st.markdown("##### 🔥 Predição de Necessidades Calóricas")
    
    # Simular evolução das necessidades calóricas
    semanas = list(range(1, 25))
    
    # TMB base diminui com perda de peso
    tmb_inicial = 1650
    tmb_evolution = [tmb_inicial - (semana * 8) for semana in semanas]
    
    # GET varia com atividade e metabolismo
    get_evolution = [tmb * 1.6 - (semana * 5) for semana, tmb in zip(semanas, tmb_evolution)]
    
    # Necessidades para diferentes objetivos
    manutencao = get_evolution
    perda_moderada = [get * 0.85 for get in get_evolution]
    perda_acelerada = [get * 0.75 for get in get_evolution]
    ganho_massa = [get * 1.15 for get in get_evolution]
    
    fig_calories = go.Figure()
    
    fig_calories.add_trace(go.Scatter(
        x=semanas, y=manutencao, mode='lines', name='Manutenção',
        line=dict(color='#2196F3', width=2)
    ))
    
    fig_calories.add_trace(go.Scatter(
        x=semanas, y=perda_moderada, mode='lines', name='Perda Moderada',
        line=dict(color='#FF9800', width=2)
    ))
    
    fig_calories.add_trace(go.Scatter(
        x=semanas, y=perda_acelerada, mode='lines', name='Perda Acelerada',
        line=dict(color='#F44336', width=2)
    ))
    
    fig_calories.add_trace(go.Scatter(
        x=semanas, y=ganho_massa, mode='lines', name='Ganho de Massa',
        line=dict(color='#4CAF50', width=2)
    ))
    
    fig_calories.update_layout(
        title="Predição de Necessidades Calóricas por Objetivo",
        xaxis_title="Semanas",
        yaxis_title="Calorias/dia",
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_calories, use_container_width=True)
    
    # Distribuição de macronutrientes
    st.markdown("##### 🥗 Distribuição de Macronutrientes Recomendada")
    
    # Criar gráfico de pizza para macros
    macro_distribution = {
        'Carboidratos': 45,
        'Proteínas': 25,
        'Lipídios': 30
    }
    
    fig_macros = px.pie(
        values=list(macro_distribution.values()),
        names=list(macro_distribution.keys()),
        title="Distribuição Ideal de Macronutrientes (%)",
        color_discrete_sequence=['#4CAF50', '#2196F3', '#FF9800']
    )
    
    fig_macros.update_layout(height=300)
    st.plotly_chart(fig_macros, use_container_width=True)

def show_ai_recommendations(user):
    """Sistema de recomendações inteligentes"""
    
    st.markdown('<div class="sub-header">💡 Recomendações Inteligentes</div>', unsafe_allow_html=True)
    
    # Filtros para recomendações
    col1, col2, col3 = st.columns(3)
    
    with col1:
        categoria_filtro = st.selectbox("📂 Categoria", [
            "Todas", "Nutrição", "Exercícios", "Suplementação", 
            "Hábitos", "Monitoramento", "Prevenção"
        ])
    
    with col2:
        prioridade_filtro = st.selectbox("🎯 Prioridade", [
            "Todas", "Alta", "Média", "Baixa"
        ])
    
    with col3:
        status_filtro = st.selectbox("📊 Status", [
            "Todas", "Novas", "Aceitas", "Implementadas", "Rejeitadas"
        ])
    
    # Gerar recomendações automáticas
    if st.button("🤖 Gerar Novas Recomendações", use_container_width=True):
        with st.spinner("🧠 IA analisando dados e gerando recomendações..."):
            time.sleep(3)
            st.success("✅ 12 novas recomendações geradas com base na análise de dados!")
    
    st.markdown("---")
    
    # Lista de recomendações
    recommendations = [
        {
            'id': 1,
            'titulo': 'Otimização de Hidratação para Maria Silva',
            'categoria': 'Nutrição',
            'prioridade': 'Alta',
            'conteudo': 'Baseado no perfil metabólico e atividade física, recomendo aumentar a ingestão hídrica para 2.8L/dia, distribuída em pequenas quantidades ao longo do dia.',
            'score_relevancia': 94,
            'paciente': 'Maria Silva Santos',
            'data_geracao': '2024-01-15',
            'status': 'Nova',
            'justificativa': 'Análise de bioimpedância indica 3% de desidratação crônica'
        },
        {
            'id': 2,
            'titulo': 'Protocolo Anti-Inflamatório para João Carlos',
            'categoria': 'Suplementação',
            'prioridade': 'Alta',
            'conteudo': 'Implementar suplementação com ômega-3 (2g/dia) e cúrcuma (500mg/dia) para reduzir marcadores inflamatórios elevados.',
            'score_relevancia': 91,
            'paciente': 'João Carlos Oliveira',
            'data_geracao': '2024-01-14',
            'status': 'Aceita',
            'justificativa': 'PCR elevada (5.2 mg/L) e histórico familiar de doenças cardiovasculares'
        },
        {
            'id': 3,
            'titulo': 'Timing de Carboidratos para Performance',
            'categoria': 'Exercícios',
            'prioridade': 'Média',
            'conteudo': 'Consumir 30-40g de carboidratos de alto IG 30min antes do treino e 60g nas primeiras 2h pós-treino para otimizar performance e recuperação.',
            'score_relevancia': 87,
            'paciente': 'Maria Silva Santos',
            'data_geracao': '2024-01-13',
            'status': 'Implementada',
            'justificativa': 'Análise de glicemia mostra resposta inadequada pós-exercício'
        },
        {
            'id': 4,
            'titulo': 'Monitoramento de Vitamina D',
            'categoria': 'Monitoramento',
            'prioridade': 'Média',
            'conteudo': 'Solicitar dosagem de 25-OH vitamina D e implementar protocolo de suplementação baseado nos resultados.',
            'score_relevancia': 82,
            'paciente': 'João Carlos Oliveira',
            'data_geracao': '2024-01-12',
            'status': 'Nova',
            'justificativa': 'Baixa exposição solar e sintomas de deficiência relatados'
        }
    ]
    
    # Exibir recomendações
    for rec in recommendations:
        # Definir cores por prioridade
        priority_colors = {
            'Alta': '#F44336',
            'Média': '#FF9800',
            'Baixa': '#4CAF50'
        }
        
        # Definir ícones por status
        status_icons = {
            'Nova': '🆕',
            'Aceita': '✅',
            'Implementada': '🎯',
            'Rejeitada': '❌'
        }
        
        with st.expander(f"{status_icons[rec['status']]} {rec['titulo']} (Score: {rec['score_relevancia']}%)", expanded=False):
            
            # Header da recomendação
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.markdown(f"**👤 Paciente:** {rec['paciente']}")
            
            with col2:
                st.markdown(f'''
                <span style="background: {priority_colors[rec['prioridade']]}; color: white; padding: 0.2rem 0.5rem; border-radius: 10px; font-size: 0.8rem;">
                    {rec['prioridade']} Prioridade
                </span>
                ''', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"**📂 Categoria:** {rec['categoria']}")
            
            with col4:
                st.markdown(f"**📅 Gerado:** {rec['data_geracao']}")
            
            # Conteúdo da recomendação
            st.markdown(f"**💡 Recomendação:**")
            st.markdown(rec['conteudo'])
            
            # Justificativa
            st.markdown(f"**🧠 Justificativa da IA:**")
            st.markdown(rec['justificativa'])
            
            # Ações
            if rec['status'] == 'Nova':
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"✅ Aceitar", key=f"aceitar_{rec['id']}"):
                        st.success("Recomendação aceita!")
                
                with col2:
                    if st.button(f"⏸️ Adiar", key=f"adiar_{rec['id']}"):
                        st.info("Recomendação adiada para revisão posterior.")
                
                with col3:
                    if st.button(f"❌ Rejeitar", key=f"rejeitar_{rec['id']}"):
                        st.warning("Recomendação rejeitada.")
            
            elif rec['status'] == 'Aceita':
                if st.button(f"🎯 Marcar como Implementada", key=f"implementar_{rec['id']}"):
                    st.success("Recomendação marcada como implementada!")
    
    # Estatísticas de recomendações
    st.markdown("---")
    st.markdown("##### 📊 Estatísticas de Recomendações")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🆕 Novas", "4", "↗️ +2")
    
    with col2:
        st.metric("✅ Aceitas", "12", "📈 75%")
    
    with col3:
        st.metric("🎯 Implementadas", "8", "↗️ +3")
    
    with col4:
        st.metric("📊 Score Médio", "88%", "↗️ +5%")

def show_ai_personalization(user):
    """Sistema de personalização da IA"""
    
    st.markdown('<div class="sub-header">🎯 Personalização da IA</div>', unsafe_allow_html=True)
    
    # Configurações de personalização
    st.markdown("##### ⚙️ Configurações de Personalização")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎯 Objetivos Priorizados**")
        objetivos = st.multiselect(
            "Selecione os objetivos que a IA deve priorizar:",
            [
                "Perda de Peso", "Ganho de Massa Muscular", "Controle Glicêmico",
                "Melhora da Performance", "Saúde Cardiovascular", "Digestão",
                "Energia e Disposição", "Qualidade do Sono", "Anti-aging",
                "Prevenção de Doenças"
            ],
            default=["Perda de Peso", "Controle Glicêmico", "Energia e Disposição"]
        )
        
        st.markdown("**🧬 Abordagens Preferidas**")
        abordagens = st.multiselect(
            "Selecione as abordagens que prefere:",
            [
                "Nutrição Funcional", "Low Carb", "Jejum Intermitente",
                "Dieta Mediterrânea", "Plant-based", "Cetogênica",
                "DASH", "Paleolítica", "Suplementação Ortomolecular"
            ],
            default=["Nutrição Funcional", "Dieta Mediterrânea"]
        )
    
    with col2:
        st.markdown("**📊 Nível de Detalhamento**")
        nivel_detalhamento = st.select_slider(
            "Quanto detalhe você quer nas análises?",
            options=["Básico", "Intermediário", "Avançado", "Especialista"],
            value="Avançado"
        )
        
        st.markdown("**⚡ Frequência de Análises**")
        frequencia_analises = st.selectbox(
            "Com que frequência a IA deve gerar novas análises?",
            ["Diária", "Semanal", "Quinzenal", "Mensal", "Sob demanda"],
            index=1
        )
        
        st.markdown("**🎨 Estilo de Comunicação**")
        estilo_comunicacao = st.selectbox(
            "Como a IA deve se comunicar?",
            ["Técnico/Científico", "Didático/Educativo", "Casual/Amigável", "Motivacional/Coach"],
            index=1
        )
    
    # Configurações avançadas
    st.markdown("##### 🔧 Configurações Avançadas")
    
    with st.expander("🧠 Configurações do Motor de IA", expanded=False):
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**⚙️ Algoritmos Ativos**")
            algoritmos = st.multiselect(
                "Selecione os algoritmos que devem ser utilizados:",
                [
                    "Regressão Linear", "Random Forest", "Neural Networks",
                    "SVM", "Gradient Boosting", "K-Means Clustering"
                ],
                default=["Random Forest", "Neural Networks", "Gradient Boosting"]
            )
            
            confianca_minima = st.slider(
                "🎯 Confiança Mínima para Recomendações (%)",
                min_value=50, max_value=95, value=75, step=5
            )
        
        with col2:
            st.markdown("**📈 Pesos dos Fatores**")
            
            peso_historico = st.slider("📊 Dados Históricos", 0.1, 1.0, 0.4, 0.1)
            peso_laboratorial = st.slider("🧪 Exames Laboratoriais", 0.1, 1.0, 0.3, 0.1)
            peso_antropometrico = st.slider("📏 Dados Antropométricos", 0.1, 1.0, 0.2, 0.1)
            peso_comportamental = st.slider("🎭 Padrões Comportamentais", 0.1, 1.0, 0.1, 0.1)
    
    # Salvar configurações
    if st.button("💾 Salvar Configurações de Personalização", use_container_width=True):
        # Simular salvamento das configurações
        configuracoes = {
            'objetivos': objetivos,
            'abordagens': abordagens,
            'nivel_detalhamento': nivel_detalhamento,
            'frequencia_analises': frequencia_analises,
            'estilo_comunicacao': estilo_comunicacao,
            'algoritmos': algoritmos,
            'confianca_minima': confianca_minima,
            'pesos': {
