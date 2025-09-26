#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NutriApp360 PRO - Sistema Completo com IA Avançada
Version: 13.0 - Biblioteca de Alimentos + IA Expandida
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
import re

st.set_page_config(
    page_title="NutriApp360 PRO v13.0",
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
    .ai-response {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
    .food-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# BANCO DE DADOS DE ALIMENTOS (TACO)
# =============================================================================

ALIMENTOS_TACO = [
    # Cereais e derivados
    {"nome": "Arroz branco cozido", "grupo": "Cereais", "porcao": 100, "calorias": 128, "carb": 28.1, "prot": 2.5, "lip": 0.2, "fibra": 1.6},
    {"nome": "Arroz integral cozido", "grupo": "Cereais", "porcao": 100, "calorias": 124, "carb": 25.8, "prot": 2.6, "lip": 1.0, "fibra": 2.7},
    {"nome": "Macarrão cozido", "grupo": "Cereais", "porcao": 100, "calorias": 135, "carb": 28.0, "prot": 4.5, "lip": 0.5, "fibra": 1.4},
    {"nome": "Pão francês", "grupo": "Cereais", "porcao": 50, "calorias": 150, "carb": 29.0, "prot": 4.5, "lip": 1.5, "fibra": 1.3},
    {"nome": "Pão integral", "grupo": "Cereais", "porcao": 50, "calorias": 127, "carb": 24.0, "prot": 5.0, "lip": 1.6, "fibra": 3.5},
    {"nome": "Aveia em flocos", "grupo": "Cereais", "porcao": 30, "calorias": 112, "carb": 19.5, "prot": 4.2, "lip": 2.1, "fibra": 2.4},
    
    # Carnes e ovos
    {"nome": "Frango grelhado (peito)", "grupo": "Carnes", "porcao": 100, "calorias": 165, "carb": 0, "prot": 31.0, "lip": 3.6, "fibra": 0},
    {"nome": "Carne bovina magra", "grupo": "Carnes", "porcao": 100, "calorias": 160, "carb": 0, "prot": 26.0, "lip": 6.0, "fibra": 0},
    {"nome": "Peixe grelhado (tilápia)", "grupo": "Carnes", "porcao": 100, "calorias": 96, "carb": 0, "prot": 20.0, "lip": 1.7, "fibra": 0},
    {"nome": "Ovo cozido", "grupo": "Carnes", "porcao": 50, "calorias": 78, "carb": 0.6, "prot": 6.3, "lip": 5.3, "fibra": 0},
    {"nome": "Atum em conserva", "grupo": "Carnes", "porcao": 100, "calorias": 118, "carb": 0, "prot": 26.0, "lip": 0.8, "fibra": 0},
    
    # Leites e derivados
    {"nome": "Leite integral", "grupo": "Laticínios", "porcao": 200, "calorias": 120, "carb": 9.0, "prot": 6.2, "lip": 6.0, "fibra": 0},
    {"nome": "Leite desnatado", "grupo": "Laticínios", "porcao": 200, "calorias": 70, "carb": 10.0, "prot": 7.0, "lip": 0.2, "fibra": 0},
    {"nome": "Iogurte natural", "grupo": "Laticínios", "porcao": 150, "calorias": 93, "carb": 7.5, "prot": 6.0, "lip": 4.5, "fibra": 0},
    {"nome": "Queijo minas", "grupo": "Laticínios", "porcao": 30, "calorias": 80, "carb": 1.2, "prot": 5.4, "lip": 6.0, "fibra": 0},
    {"nome": "Queijo cottage", "grupo": "Laticínios", "porcao": 50, "calorias": 50, "carb": 2.0, "prot": 6.5, "lip": 2.0, "fibra": 0},
    
    # Leguminosas
    {"nome": "Feijão preto cozido", "grupo": "Leguminosas", "porcao": 100, "calorias": 77, "carb": 14.0, "prot": 4.5, "lip": 0.5, "fibra": 8.4},
    {"nome": "Feijão carioca cozido", "grupo": "Leguminosas", "porcao": 100, "calorias": 76, "carb": 13.6, "prot": 4.8, "lip": 0.5, "fibra": 8.5},
    {"nome": "Lentilha cozida", "grupo": "Leguminosas", "porcao": 100, "calorias": 93, "carb": 16.0, "prot": 6.3, "lip": 0.4, "fibra": 7.9},
    {"nome": "Grão de bico cozido", "grupo": "Leguminosas", "porcao": 100, "calorias": 121, "carb": 19.3, "prot": 6.8, "lip": 2.1, "fibra": 7.6},
    
    # Verduras e legumes
    {"nome": "Alface", "grupo": "Vegetais", "porcao": 100, "calorias": 15, "carb": 2.9, "prot": 1.4, "lip": 0.2, "fibra": 2.0},
    {"nome": "Tomate", "grupo": "Vegetais", "porcao": 100, "calorias": 18, "carb": 3.9, "prot": 0.9, "lip": 0.2, "fibra": 1.2},
    {"nome": "Brócolis cozido", "grupo": "Vegetais", "porcao": 100, "calorias": 30, "carb": 5.9, "prot": 2.8, "lip": 0.4, "fibra": 3.0},
    {"nome": "Cenoura cozida", "grupo": "Vegetais", "porcao": 100, "calorias": 35, "carb": 8.2, "prot": 0.8, "lip": 0.2, "fibra": 2.6},
    {"nome": "Batata inglesa cozida", "grupo": "Vegetais", "porcao": 100, "calorias": 87, "carb": 20.1, "prot": 1.9, "lip": 0.1, "fibra": 1.3},
    {"nome": "Batata doce cozida", "grupo": "Vegetais", "porcao": 100, "calorias": 77, "carb": 18.4, "prot": 0.6, "lip": 0.1, "fibra": 2.2},
    
    # Frutas
    {"nome": "Banana", "grupo": "Frutas", "porcao": 100, "calorias": 98, "carb": 26.0, "prot": 1.3, "lip": 0.1, "fibra": 2.6},
    {"nome": "Maçã", "grupo": "Frutas", "porcao": 100, "calorias": 56, "carb": 14.9, "prot": 0.3, "lip": 0.1, "fibra": 1.3},
    {"nome": "Laranja", "grupo": "Frutas", "porcao": 100, "calorias": 45, "carb": 11.5, "prot": 1.0, "lip": 0.1, "fibra": 2.2},
    {"nome": "Morango", "grupo": "Frutas", "porcao": 100, "calorias": 30, "carb": 7.7, "prot": 0.9, "lip": 0.3, "fibra": 1.7},
    {"nome": "Abacate", "grupo": "Frutas", "porcao": 100, "calorias": 96, "carb": 6.0, "prot": 1.2, "lip": 8.4, "fibra": 3.3},
    {"nome": "Manga", "grupo": "Frutas", "porcao": 100, "calorias": 51, "carb": 13.0, "prot": 0.5, "lip": 0.1, "fibra": 1.6},
    
    # Oleaginosas
    {"nome": "Amendoim", "grupo": "Oleaginosas", "porcao": 30, "calorias": 170, "carb": 5.1, "prot": 7.8, "lip": 14.1, "fibra": 2.4},
    {"nome": "Castanha de caju", "grupo": "Oleaginosas", "porcao": 30, "calorias": 176, "carb": 9.0, "prot": 5.4, "lip": 13.5, "fibra": 1.0},
    {"nome": "Amêndoas", "grupo": "Oleaginosas", "porcao": 30, "calorias": 173, "carb": 6.0, "prot": 6.3, "lip": 14.7, "fibra": 3.6},
    {"nome": "Nozes", "grupo": "Oleaginosas", "porcao": 30, "calorias": 196, "carb": 4.1, "prot": 4.5, "lip": 19.5, "fibra": 2.0},
]

# Tabela de conversão de medidas caseiras
CONVERSAO_MEDIDAS = {
    # Sólidos (g)
    "colher de sopa": {"arroz": 25, "feijao": 20, "aveia": 10, "acucar": 15, "farinha": 15, "pasta amendoim": 20},
    "colher de chá": {"acucar": 5, "sal": 5, "aveia": 3, "farinha": 3},
    "xícara": {"arroz": 160, "feijao": 150, "aveia": 80, "farinha": 120, "acucar": 180},
    "concha": {"feijao": 100, "arroz": 120},
    "escumadeira": {"arroz": 80, "feijao": 70},
    "fatia": {"pao": 50, "queijo": 30, "presunto": 30},
    "unidade": {"ovo": 50, "banana": 100, "maça": 130, "laranja": 150, "pao": 50},
    
    # Líquidos (ml)
    "copo": 200,
    "xícara_liquido": 240,
    "colher sopa_liquido": 15,
    "colher chá_liquido": 5,
}

# =============================================================================
# SISTEMA DE IA AVANÇADO
# =============================================================================

class AdvancedAIAssistant:
    def __init__(self):
        self.knowledge_base = {
            "hipertensao": {
                "dieta": "DASH - Dietary Approaches to Stop Hypertension",
                "sodio": "< 2300mg/dia (ideal < 1500mg)",
                "potassio": "Aumentar: banana, laranja, batata doce, feijão",
                "magnesio": "Vegetais verdes, oleaginosas, grãos integrais",
                "peso": "Redução de 5-10% já reduz PA significativamente"
            },
            "diabetes": {
                "carboidratos": "Contagem de carboidratos, preferir baixo IG",
                "fibras": "25-35g/dia - retarda absorção de glicose",
                "fracionamento": "5-6 refeições/dia para controle glicêmico",
                "proteinas": "Preferir magras, controlar porções"
            },
            "obesidade": {
                "deficit": "300-500 kcal/dia para perda sustentável",
                "proteina": "1.6-2.2g/kg peso atual - preserva massa magra",
                "exercicio": "Combinar aeróbico + resistido",
                "comportamento": "Diário alimentar, mindful eating"
            },
            "atleta": {
                "proteina": "1.6-2.2g/kg para hipertrofia",
                "carboidrato": "5-12g/kg conforme intensidade treino",
                "hidratacao": "Antes: 5-7ml/kg, durante: 150-200ml cada 15min",
                "recuperacao": "Janela anabólica 30-60min pós-treino"
            }
        }
    
    def analisar_diario_alimentar(self, refeicoes):
        """Analisa um diário alimentar com IA"""
        total_cal = sum([r.get('calorias', 0) for r in refeicoes])
        total_prot = sum([r.get('proteinas', 0) for r in refeicoes])
        total_carb = sum([r.get('carboidratos', 0) for r in refeicoes])
        
        analise = f"""
        ANÁLISE INTELIGENTE DO DIÁRIO ALIMENTAR
        
        Totais Diários:
        - Calorias: {total_cal:.0f} kcal
        - Proteínas: {total_prot:.1f}g ({total_prot*4/total_cal*100:.1f}%)
        - Carboidratos: {total_carb:.1f}g ({total_carb*4/total_cal*100:.1f}%)
        
        Observações IA:
        """
        
        if total_prot < 50:
            analise += "\n- Proteína BAIXA: Risco de perda de massa muscular"
        elif total_prot > 150:
            analise += "\n- Proteína ALTA: Atenção à função renal"
        
        if len(refeicoes) < 3:
            analise += "\n- POUCAS refeições: Considere fracionar mais"
        
        return analise
    
    def gerar_cardapio_ia(self, calorias_alvo, objetivo, restricoes):
        """Gera cardápio personalizado com IA"""
        
        # Distribuição de macros baseada no objetivo
        distribuicoes = {
            "perda_peso": (40, 30, 30),  # carb, prot, lip
            "ganho_massa": (45, 30, 25),
            "saude": (50, 20, 30),
            "low_carb": (20, 40, 40)
        }
        
        carb_p, prot_p, lip_p = distribuicoes.get(objetivo.lower().replace(" ", "_"), (50, 20, 30))
        
        cardapio = f"""
        CARDÁPIO PERSONALIZADO - GERADO POR IA
        
        Objetivo: {objetivo}
        Calorias: {calorias_alvo} kcal/dia
        Distribuição: {carb_p}% Carb | {prot_p}% Prot | {lip_p}% Lip
        
        CAFÉ DA MANHÃ (~25% calorias):
        """
        
        cal_cafe = calorias_alvo * 0.25
        
        if "lactose" not in restricoes.lower():
            cardapio += f"\n- 1 copo (200ml) de leite desnatado"
            cardapio += f"\n- 2 fatias de pão integral"
            cardapio += f"\n- 1 colher (sopa) de pasta de amendoim"
            cardapio += f"\n- 1 banana"
        else:
            cardapio += f"\n- 200ml de bebida vegetal"
            cardapio += f"\n- Tapioca com ovo"
            cardapio += f"\n- 1 fruta"
        
        cardapio += f"""
        
        LANCHE MANHÃ (~10% calorias):
        - 1 fruta + 1 castanha (30g)
        
        ALMOÇO (~35% calorias):
        - Arroz integral (4 colheres sopa)
        - Feijão (1 concha)
        - Frango grelhado (100g)
        - Salada à vontade
        - 1 colher (sopa) de azeite
        
        LANCHE TARDE (~10% calorias):
        - Iogurte natural + aveia
        
        JANTAR (~20% calorias):
        - Peixe grelhado ou frango
        - Batata doce (100g) ou salada com quinoa
        - Vegetais cozidos
        
        OBSERVAÇÕES IA:
        - Hidratação: Mínimo 2L água/dia
        - Evitar frituras e ultraprocessados
        - Variar fontes proteicas
        - Consumir vegetais em todas refeições
        """
        
        return cardapio
    
    def interpretar_exame(self, tipo_exame, valores):
        """Interpreta exames laboratoriais"""
        
        interpretacoes = {
            "hemograma": {
                "hemoglobina_baixa": "Anemia - aumentar ferro, B12, ácido fólico",
                "hemoglobina_alta": "Policitemia - avaliar hidratação"
            },
            "lipidograma": {
                "colesterol_alto": "Reduzir gorduras saturadas, aumentar fibras solúveis",
                "triglicerides_alto": "Reduzir carboidratos simples e álcool"
            },
            "glicemia": {
                "glicemia_alta": "Controlar carboidratos, aumentar fibras",
                "hba1c_alta": "Controle glicêmico inadequado - revisar dieta"
            }
        }
        
        return f"Interpretação nutricional: {interpretacoes.get(tipo_exame, 'Solicite avaliação médica')}"
    
    def sugestao_substituicoes(self, alimento_original):
        """Sugere substituições saudáveis"""
        
        substituicoes = {
            "arroz branco": ["arroz integral", "quinoa", "batata doce"],
            "pão francês": ["pão integral", "tapioca", "panqueca de aveia"],
            "açúcar": ["stevia", "xilitol", "eritritol"],
            "leite integral": ["leite desnatado", "leite vegetal"],
            "macarrão": ["macarrão integral", "abobrinha espaguete", "shirataki"],
            "carne vermelha": ["frango", "peixe", "proteína vegetal"],
        }
        
        return substituicoes.get(alimento_original.lower(), ["Consulte nutricionista"])

ai_assistant = AdvancedAIAssistant()

# =============================================================================
# CONVERSOR INTELIGENTE DE MEDIDAS
# =============================================================================

class MeasureConverter:
    def __init__(self):
        self.conversoes = CONVERSAO_MEDIDAS
    
    def converter(self, quantidade, medida_origem, alimento, medida_destino="gramas"):
        """Converte medidas caseiras para gramas"""
        
        try:
            medida_lower = medida_origem.lower()
            alimento_lower = alimento.lower()
            
            # Busca na tabela de conversão
            if medida_lower in self.conversoes:
                if isinstance(self.conversoes[medida_lower], dict):
                    # Busca específica do alimento
                    for key in self.conversoes[medida_lower]:
                        if key in alimento_lower:
                            peso_unitario = self.conversoes[medida_lower][key]
                            return quantidade * peso_unitario
                    # Usa média se não encontrar específico
                    peso_unitario = sum(self.conversoes[medida_lower].values()) / len(self.conversoes[medida_lower])
                    return quantidade * peso_unitario
                else:
                    return quantidade * self.conversoes[medida_lower]
            
            return quantidade  # Retorna quantidade original se não converter
            
        except:
            return quantidade
    
    def interpretar_texto(self, texto):
        """Interpreta texto e converte automaticamente"""
        # Ex: "2 colheres de sopa de arroz" -> 50g
        
        padroes = [
            (r'(\d+\.?\d*)\s*(colher|colheres)\s*de\s*sopa', 'colher de sopa'),
            (r'(\d+\.?\d*)\s*(colher|colheres)\s*de\s*chá', 'colher de chá'),
            (r'(\d+\.?\d*)\s*(xícara|xícaras)', 'xícara'),
            (r'(\d+\.?\d*)\s*(copo|copos)', 'copo'),
            (r'(\d+\.?\d*)\s*(unidade|unidades)', 'unidade'),
        ]
        
        for padrao, medida in padroes:
            match = re.search(padrao, texto.lower())
            if match:
                quantidade = float(match.group(1))
                # Tenta extrair nome do alimento
                palavras = texto.lower().split()
                alimento = palavras[-1] if palavras else "generico"
                
                gramas = self.converter(quantidade, medida, alimento)
                return {
                    'quantidade': quantidade,
                    'medida': medida,
                    'gramas': gramas,
                    'texto': f"{quantidade} {medida} ≈ {gramas:.0f}g"
                }
        
        return None

converter = MeasureConverter()

# =============================================================================
# GERENCIADOR DE BANCO DE DADOS
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
        
        # Tabela de Usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
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
            ativo INTEGER DEFAULT 1
        )
        ''')
        
        # Tabela de Pacientes
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
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
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo INTEGER DEFAULT 1,
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de Alimentos (Biblioteca)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS alimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            grupo TEXT,
            porcao REAL,
            calorias REAL,
            carboidratos REAL,
            proteinas REAL,
            lipidios REAL,
            fibras REAL,
            calcio REAL,
            ferro REAL,
            sodio REAL,
            criado_por INTEGER,
            publico INTEGER DEFAULT 1,
            FOREIGN KEY (criado_por) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de Diário Alimentar
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS diario_alimentar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            data_registro DATE,
            refeicao TEXT,
            alimento_id INTEGER,
            quantidade REAL,
            medida TEXT,
            observacoes TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (alimento_id) REFERENCES alimentos (id)
        )
        ''')
        
        # Tabela de Prontuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prontuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            nutricionista_id INTEGER,
            data_atendimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tipo_atendimento TEXT,
            queixa_principal TEXT,
            historia_clinica TEXT,
            historia_alimentar TEXT,
            exame_fisico TEXT,
            diagnostico_nutricional TEXT,
            conduta TEXT,
            observacoes TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de Prescrições
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescricoes_suplementos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            paciente_id INTEGER,
            nutricionista_id INTEGER,
            data_prescricao DATE DEFAULT CURRENT_DATE,
            suplementos TEXT,
            orientacoes TEXT,
            validade DATE,
            ativo INTEGER DEFAULT 1,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Tabela de Avaliações
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
        
        # Tabela de Consultas IA
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ia_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            tipo_consulta TEXT,
            prompt TEXT,
            resposta TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
        ''')
        
        # Popular alimentos TACO
        cursor.execute("SELECT COUNT(*) FROM alimentos")
        if cursor.fetchone()[0] == 0:
            for alimento in ALIMENTOS_TACO:
                cursor.execute('''
                INSERT INTO alimentos (nome, grupo, porcao, calorias, carboidratos, proteinas, lipidios, fibras, publico)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
                ''', (
                    alimento['nome'], alimento['grupo'], alimento['porcao'],
                    alimento['calorias'], alimento['carb'], alimento['prot'],
                    alimento['lip'], alimento['fibra']
                ))
        
        # Criar usuários padrão
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            usuarios_padrao = [
                ('Administrador', 'admin@nutriapp360.com', 'admin123', 'admin', 'completo', 'ADMIN001'),
                ('Dr. Nutricionista', 'nutri@nutriapp360.com', 'nutri123', 'nutricionista', 'completo', 'CRN12345'),
                ('Assistente', 'assistente@nutriapp360.com', 'assist123', 'assistente', 'limitado', None)
            ]
            
            for nome, email, senha, tipo, acesso, coren in usuarios_padrao:
                senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                cursor.execute('''
                INSERT INTO usuarios (nome, email, senha, tipo_usuario, nivel_acesso, coren, clinica)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (nome, email, senha_hash, tipo, acesso, coren, 'NutriApp360 PRO'))
        
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

def check_permission(user, required_level):
    levels = {'admin': 3, 'completo': 2, 'limitado': 1}
    user_level = levels.get(user.get('nivel_acesso', 'limitado'), 1)
    req_level = levels.get(required_level, 2)
    return user_level >= req_level

# =============================================================================
# AUTENTICAÇÃO
# =============================================================================

def authenticate_user(email, password):
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    cursor.execute('''
    SELECT id, nome, email, tipo_usuario, nivel_acesso, coren, telefone, clinica
    FROM usuarios 
    WHERE email = ? AND senha = ? AND ativo = 1
    ''', (email, password_hash))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            'id': user[0], 'nome': user[1], 'email': user[2],
            'tipo_usuario': user[3], 'nivel_acesso': user[4],
            'coren': user[5], 'telefone': user[6], 'clinica': user[7]
        }
    return None

def show_login():
    load_css()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="main-header">NutriApp360 PRO</h1>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center;">Sistema com IA Avançada v13.0</h3>', unsafe_allow_html=True)
        
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
            Admin: admin@nutriapp360.com / admin123
            Nutricionista: nutri@nutriapp360.com / nutri123
            Assistente: assistente@nutriapp360.com / assist123
            
            Novos Recursos v13.0:
            - Biblioteca de 30+ alimentos (TACO)
            - Conversor inteligente de medidas
            - IA para análise de diário alimentar
            - Gerador de cardápios personalizado
            - Interpretação de exames com IA
            - Chat nutricional inteligente
            - Sugestões de substituições
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
    
    cursor.execute("SELECT COUNT(*) FROM prescricoes_suplementos WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    prescricoes_ativas = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM alimentos WHERE publico = 1")
    total_alimentos = cursor.fetchone()[0]
    
    conn.close()
    
    col1, col2, col3, col4 = st.columns(4)
    
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
            <h2 style="color: #2E7D32; margin:0;">📋</h2>
            <h3 style="margin:0;">{total_prontuarios}</h3>
            <p style="margin:0;">Prontuários</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <h2 style="color: #2E7D32; margin:0;">💊</h2>
            <h3 style="margin:0;">{prescricoes_ativas}</h3>
            <p style="margin:0;">Prescrições</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="metric-card">
            <h2 style="color: #2E7D32; margin:0;">🍎</h2>
            <h3 style="margin:0;">{total_alimentos}</h3>
            <p style="margin:0;">Alimentos</p>
        </div>
        ''', unsafe_allow_html=True)

# =============================================================================
# BIBLIOTECA DE ALIMENTOS
# =============================================================================

def show_alimentos(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Biblioteca de Alimentos</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Buscar Alimentos", "Adicionar Alimento", "Conversor de Medidas"])
    
    with tab1:
        buscar_alimentos()
    
    with tab2:
        adicionar_alimento(user)
    
    with tab3:
        conversor_medidas()

def buscar_alimentos():
    st.markdown('<div class="sub-header">Buscar na Biblioteca</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        busca = st.text_input("Buscar alimento", placeholder="Digite o nome...")
    
    with col2:
        grupo = st.selectbox("Grupo", ["Todos", "Cereais", "Carnes", "Laticínios", "Leguminosas", "Vegetais", "Frutas", "Oleaginosas"])
    
    with col3:
        cal_max = st.number_input("Calorias máx", 0, 1000, 0, step=50)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM alimentos WHERE publico = 1"
    params = []
    
    if busca:
        query += " AND nome LIKE ?"
        params.append(f"%{busca}%")
    
    if grupo != "Todos":
        query += " AND grupo = ?"
        params.append(grupo)
    
    if cal_max > 0:
        query += " AND calorias <= ?"
        params.append(cal_max)
    
    query += " ORDER BY nome"
    
    cursor.execute(query, params)
    alimentos = cursor.fetchall()
    conn.close()
    
    if not alimentos:
        st.info("Nenhum alimento encontrado.")
        return
    
    st.markdown(f"**{len(alimentos)} alimentos encontrados**")
    
    for alim in alimentos:
        with st.expander(f"🍽️ {alim[1]} ({alim[2]})", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Porção:** {alim[3]:.0f}g  
                **Calorias:** {alim[4]:.0f} kcal  
                **Carboidratos:** {alim[5]:.1f}g  
                **Proteínas:** {alim[6]:.1f}g  
                **Lipídios:** {alim[7]:.1f}g  
                **Fibras:** {alim[8]:.1f}g
                """)
            
            with col2:
                # Gráfico de macros
                fig = px.pie(
                    values=[alim[5], alim[6], alim[7]],
                    names=['Carboidratos', 'Proteínas', 'Lipídios'],
                    color_discrete_sequence=['#4CAF50', '#2196F3', '#FFC107']
                )
                fig.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)

def adicionar_alimento(user):
    st.markdown('<div class="sub-header">Adicionar Novo Alimento</div>', unsafe_allow_html=True)
    
    with st.form("alimento_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome do Alimento *")
            grupo = st.selectbox("Grupo", ["Cereais", "Carnes", "Laticínios", "Leguminosas", "Vegetais", "Frutas", "Oleaginosas", "Outros"])
            porcao = st.number_input("Porção (g)", 0.0, 1000.0, 100.0)
            calorias = st.number_input("Calorias (kcal)", 0.0, 1000.0, 100.0)
        
        with col2:
            carb = st.number_input("Carboidratos (g)", 0.0, 500.0, 20.0)
            prot = st.number_input("Proteínas (g)", 0.0, 200.0, 5.0)
            lip = st.number_input("Lipídios (g)", 0.0, 100.0, 2.0)
            fibra = st.number_input("Fibras (g)", 0.0, 50.0, 1.0)
        
        publico = st.checkbox("Tornar público (outros nutricionistas poderão ver)")
        
        submitted = st.form_submit_button("Adicionar Alimento", use_container_width=True)
        
        if submitted:
            if nome:
                try:
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                    INSERT INTO alimentos (nome, grupo, porcao, calorias, carboidratos, proteinas, lipidios, fibras, criado_por, publico)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (nome, grupo, porcao, calorias, carb, prot, lip, fibra, user['id'], 1 if publico else 0))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success(f"Alimento '{nome}' adicionado com sucesso!")
                    
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
            else:
                st.error("Nome é obrigatório!")

def conversor_medidas():
    st.markdown('<div class="sub-header">Conversor Inteligente de Medidas</div>', unsafe_allow_html=True)
    
    st.info("Converta medidas caseiras para gramas/ml automaticamente!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Converter Manualmente")
        
        quantidade = st.number_input("Quantidade", 1.0, 100.0, 1.0, step=0.5)
        medida = st.selectbox("Medida", [
            "colher de sopa",
            "colher de chá",
            "xícara",
            "concha",
            "escumadeira",
            "fatia",
            "unidade",
            "copo"
        ])
        alimento = st.text_input("Alimento", placeholder="Ex: arroz, feijão, açúcar...")
        
        if st.button("Converter"):
            resultado = converter.converter(quantidade, medida, alimento)
            st.success(f"{quantidade} {medida} de {alimento} = **{resultado:.0f}g**")
    
    with col2:
        st.markdown("### Interpretar Texto")
        
        texto = st.text_area(
            "Digite a descrição",
            placeholder="Ex: 2 colheres de sopa de arroz\n3 xícaras de feijão\n1 copo de leite",
            height=150
        )
        
        if st.button("Interpretar"):
            linhas = texto.split('\n')
            for linha in linhas:
                if linha.strip():
                    resultado = converter.interpretar_texto(linha)
                    if resultado:
                        st.success(resultado['texto'])
                    else:
                        st.warning(f"Não foi possível interpretar: {linha}")
    
    st.markdown("---")
    st.markdown("### Tabela de Referência Rápida")
    
    tabela_ref = pd.DataFrame({
        'Medida': ['1 col sopa', '1 col chá', '1 xícara', '1 concha', '1 copo', '1 unidade'],
        'Arroz': ['25g', '-', '160g', '120g', '-', '-'],
        'Feijão': ['20g', '-', '150g', '100g', '-', '-'],
        'Açúcar': ['15g', '5g', '180g', '-', '-', '-'],
        'Leite': ['15ml', '5ml', '240ml', '-', '200ml', '-'],
        'Ovo': ['-', '-', '-', '-', '-', '50g']
    })
    
    st.dataframe(tabela_ref, use_container_width=True)

# =============================================================================
# ASSISTENTE IA AVANÇADO
# =============================================================================

def show_ai_assistant(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Assistente IA Avançado</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Chat Nutricional",
        "Gerar Cardápio",
        "Analisar Diário",
        "Interpretar Exames"
    ])
    
    with tab1:
        chat_nutricional(user)
    
    with tab2:
        gerar_cardapio(user)
    
    with tab3:
        analisar_diario(user)
    
    with tab4:
        interpretar_exames(user)

def chat_nutricional(user):
    st.markdown("### Chat Nutricional Inteligente")
    
    st.info("Faça perguntas sobre nutrição, condutas, patologias e mais!")
    
    pergunta = st.text_area(
        "Sua pergunta",
        placeholder="Ex: Como tratar diabetes tipo 2 com dieta?\nQual a melhor distribuição de macros para hipertrofia?",
        height=100
    )
    
    if st.button("Consultar IA", use_container_width=True):
        if pergunta:
            resposta = ai_assistant.knowledge_base
            
            # Busca na base de conhecimento
            texto_resposta = "Baseado em evidências científicas:\n\n"
            
            if "diabetes" in pergunta.lower():
                info = ai_assistant.knowledge_base['diabetes']
                texto_resposta += f"**DIABETES:**\n"
                for key, value in info.items():
                    texto_resposta += f"- {key.upper()}: {value}\n"
            
            elif "hipertensão" in pergunta.lower() or "hipertensao" in pergunta.lower() or "pressão" in pergunta.lower():
                info = ai_assistant.knowledge_base['hipertensao']
                texto_resposta += f"**HIPERTENSÃO:**\n"
                for key, value in info.items():
                    texto_resposta += f"- {key.upper()}: {value}\n"
            
            elif "obesidade" in pergunta.lower() or "perda de peso" in pergunta.lower() or "emagrecer" in pergunta.lower():
                info = ai_assistant.knowledge_base['obesidade']
                texto_resposta += f"**PERDA DE PESO:**\n"
                for key, value in info.items():
                    texto_resposta += f"- {key.upper()}: {value}\n"
            
            elif "atleta" in pergunta.lower() or "hipertrofia" in pergunta.lower() or "massa muscular" in pergunta.lower():
                info = ai_assistant.knowledge_base['atleta']
                texto_resposta += f"**ATLETAS/HIPERTROFIA:**\n"
                for key, value in info.items():
                    texto_resposta += f"- {key.upper()}: {value}\n"
            
            else:
                texto_resposta += "Para uma resposta mais específica, mencione a condição (diabetes, hipertensão, obesidade, atleta)."
            
            st.markdown(f'''
            <div class="ai-response">
                {texto_resposta}
            </div>
            ''', unsafe_allow_html=True)
            
            # Salvar log
            try:
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO ia_logs (usuario_id, tipo_consulta, prompt, resposta)
                VALUES (?, ?, ?, ?)
                ''', (user['id'], 'chat', pergunta, texto_resposta))
                conn.commit()
                conn.close()
            except:
                pass
        else:
            st.warning("Digite uma pergunta!")

def gerar_cardapio(user):
    st.markdown("### Gerador de Cardápios Personalizado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        calorias = st.number_input("Calorias Alvo (kcal/dia)", 1200, 4000, 2000, step=100)
        objetivo = st.selectbox("Objetivo", [
            "Perda Peso",
            "Ganho Massa",
            "Saúde",
            "Low Carb"
        ])
    
    with col2:
        restricoes = st.text_area(
            "Restrições Alimentares",
            placeholder="Ex: lactose, glúten, vegano...",
            height=100
        )
    
    if st.button("Gerar Cardápio com IA", use_container_width=True):
        cardapio = ai_assistant.gerar_cardapio_ia(calorias, objetivo, restricoes)
        
        st.markdown(f'''
        <div class="ai-response">
            <pre style="white-space: pre-wrap; font-family: inherit;">{cardapio}</pre>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("Salvar Cardápio"):
            st.success("Funcionalidade de salvamento em desenvolvimento")

def analisar_diario(user):
    st.markdown("### Análise de Diário Alimentar")
    
    st.info("Registre o que comeu hoje e a IA irá analisar!")
    
    refeicoes = []
    
    for i, refeicao in enumerate(["Café da Manhã", "Lanche Manhã", "Almoço", "Lanche Tarde", "Jantar", "Ceia"]):
        with st.expander(f"{refeicao}", expanded=(i==0)):
            alimentos = st.text_area(
                f"Alimentos de {refeicao}",
                placeholder="Ex: 2 pães, 1 ovo, 1 copo de leite",
                height=60,
                key=f"ref_{i}"
            )
            
            if alimentos:
                # Estimativa simples
                cal = len(alimentos.split(',')) * 150  # Estimativa básica
                refeicoes.append({
                    'nome': refeicao,
                    'alimentos': alimentos,
                    'calorias': cal,
                    'proteinas': cal * 0.15 / 4,
                    'carboidratos': cal * 0.55 / 4
                })
    
    if st.button("Analisar com IA", use_container_width=True):
        if refeicoes:
            analise = ai_assistant.analisar_diario_alimentar(refeicoes)
            
            st.markdown(f'''
            <div class="ai-response">
                <pre style="white-space: pre-wrap; font-family: inherit;">{analise}</pre>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.warning("Registre pelo menos uma refeição!")

def interpretar_exames(user):
    st.markdown("### Interpretação Nutricional de Exames")
    
    st.warning("Esta é uma interpretação nutricional. Sempre consulte um médico para diagnóstico.")
    
    tipo_exame = st.selectbox("Tipo de Exame", [
        "Hemograma",
        "Lipidograma",
        "Glicemia/HbA1c",
        "Vitaminas",
        "Minerais"
    ])
    
    valores = st.text_area(
        "Cole os resultados do exame",
        placeholder="Ex: Hemoglobina: 11.5 g/dL\nColesterol Total: 250 mg/dL",
        height=150
    )
    
    if st.button("Interpretar com IA", use_container_width=True):
        if valores:
            interpretacao = f"""
            INTERPRETAÇÃO NUTRICIONAL - {tipo_exame}
            
            """
            
            if tipo_exame == "Hemograma":
                if "11" in valores or "10" in valores:
                    interpretacao += """
                    HEMOGLOBINA BAIXA detectada:
                    
                    Conduta Nutricional:
                    - Aumentar ferro heme: carnes vermelhas, fígado
                    - Ferro não-heme: feijão, lentilha, vegetais verde-escuros
                    - Vitamina C: potencializa absorção de ferro
                    - Ácido fólico: vegetais folhosos
                    - Vitamina B12: carnes, ovos, laticínios
                    - Evitar: chá e café junto às refeições
                    """
            
            elif tipo_exame == "Lipidograma":
                interpretacao += """
                PERFIL LIPÍDICO:
                
                Para reduzir colesterol:
                - Reduzir gorduras saturadas (carnes gordas, laticínios integrais)
                - Aumentar fibras solúveis (aveia, maçã, feijão)
                - Ômega-3: peixes, linhaça, chia
                - Fitosteróis: oleaginosas, óleos vegetais
                
                Para triglicérides:
                - Reduzir carboidratos simples
                - Evitar álcool
                - Aumentar ômega-3
                - Controlar peso
                """
            
            elif tipo_exame == "Glicemia/HbA1c":
                interpretacao += """
                CONTROLE GLICÊMICO:
                
                - Carboidratos de baixo IG
                - 25-35g fibras/dia
                - Fracionamento: 5-6 refeições
                - Evitar açúcares simples
                - Proteínas magras em todas refeições
                - Atividade física regular
                """
            
            st.markdown(f'''
            <div class="ai-response">
                <pre style="white-space: pre-wrap; font-family: inherit;">{interpretacao}</pre>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.warning("Cole os resultados do exame!")

# =============================================================================
# GESTÃO DE PACIENTES
# =============================================================================

def show_pacientes(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Gestão de Pacientes</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Lista de Pacientes", "Novo Paciente"])
    
    with tab1:
        list_pacientes(user)
    
    with tab2:
        create_paciente(user)

def list_pacientes(user):
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, nome, email, telefone, data_nascimento, sexo, objetivo
    FROM pacientes
    WHERE nutricionista_id = ? AND ativo = 1
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.info("Nenhum paciente cadastrado ainda.")
        return
    
    busca = st.text_input("Buscar paciente", placeholder="Digite o nome...")
    
    for pac in pacientes:
        if busca.lower() not in pac[1].lower():
            continue
        
        idade = calculate_age(pac[4]) if pac[4] else "N/A"
        
        with st.expander(f"{pac[1]} - {idade} anos", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Email:** {pac[2] or 'Não informado'}  
                **Telefone:** {pac[3] or 'Não informado'}  
                **Data Nascimento:** {pac[4] or 'Não informado'}
                """)
            
            with col2:
                st.markdown(f"""
                **Sexo:** {pac[5] or 'Não informado'}  
                **Objetivo:** {pac[6] or 'Não informado'}
                """)

def create_paciente(user):
    with st.form("paciente_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo *")
            email = st.text_input("Email")
            telefone = st.text_input("Telefone")
        
        with col2:
            data_nasc = st.date_input("Data de Nascimento", value=None)
            sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
            objetivo = st.selectbox("Objetivo", [
                "Perda de Peso",
                "Ganho de Massa",
                "Saúde",
                "Performance",
                "Tratamento Patologia"
            ])
        
        restricoes = st.text_area("Restrições Alimentares")
        
        submitted = st.form_submit_button("Cadastrar", use_container_width=True)
        
        if submitted:
            if nome:
                try:
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                    INSERT INTO pacientes (uuid, nutricionista_id, nome, email, telefone, data_nascimento, sexo, objetivo, restricoes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (str(uuid.uuid4()), user['id'], nome, email, telefone, data_nasc, sexo, objetivo, restricoes))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success(f"Paciente {nome} cadastrado!")
                    
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
            else:
                st.error("Nome é obrigatório!")

# =============================================================================
# PRONTUÁRIO
# =============================================================================

def show_prontuario(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Prontuário Nutricional</h1>', unsafe_allow_html=True)
    
    if not check_permission(user, 'completo'):
        st.error("Você não tem permissão.")
        return
    
    tab1, tab2 = st.tabs(["Novo Prontuário", "Histórico"])
    
    with tab1:
        create_prontuario(user)
    
    with tab2:
        view_prontuarios(user)

def create_prontuario(user):
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, nome FROM pacientes WHERE nutricionista_id = ? AND ativo = 1 ORDER BY nome", (user['id'],))
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.warning("Cadastre um paciente primeiro.")
        return
    
    with st.form("prontuario_form"):
        paciente = st.selectbox("Paciente", options=pacientes, format_func=lambda x: x[1])
        
        tipo = st.selectbox("Tipo", ["Primeira Consulta", "Retorno", "Reavaliação"])
        queixa = st.text_area("Queixa Principal", height=80)
        diagnostico = st.text_area("Diagnóstico Nutricional", height=80)
        conduta = st.text_area("Conduta", height=120)
        
        submitted = st.form_submit_button("Salvar", use_container_width=True)
        
        if submitted and queixa and diagnostico:
            try:
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO prontuarios (paciente_id, nutricionista_id, tipo_atendimento, queixa_principal, diagnostico_nutricional, conduta)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (paciente[0], user['id'], tipo, queixa, diagnostico, conduta))
                conn.commit()
                conn.close()
                st.success("Prontuário salvo!")
            except Exception as e:
                st.error(f"Erro: {str(e)}")

def view_prontuarios(user):
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT p.*, pac.nome FROM prontuarios p
    JOIN pacientes pac ON p.paciente_id = pac.id
    WHERE p.nutricionista_id = ?
    ORDER BY p.data_atendimento DESC
    LIMIT 20
    """, (user['id'],))
    
    prontuarios = cursor.fetchall()
    conn.close()
    
    if not prontuarios:
        st.info("Nenhum prontuário.")
        return
    
    for p in prontuarios:
        with st.expander(f"{p[-1]} - {p[3]} - {p[4]}", expanded=False):
            if p[5]:
                st.markdown(f"**Queixa:** {p[5]}")
            if p[9]:
                st.markdown(f"**Diagnóstico:** {p[9]}")
            if p[10]:
                st.markdown(f"**Conduta:** {p[10]}")

# =============================================================================
# PRESCRIÇÕES
# =============================================================================

def show_prescricoes(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Prescrição de Suplementos</h1>', unsafe_allow_html=True)
    
    if not check_permission(user, 'completo'):
        st.error("Sem permissão.")
        return
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM pacientes WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.warning("Cadastre um paciente primeiro.")
        return
    
    with st.form("prescricao_form"):
        paciente = st.selectbox("Paciente", options=pacientes, format_func=lambda x: x[1])
        
        suplementos = st.text_area(
            "Suplementos e Posologia",
            placeholder="1. Vitamina D3 - 2000 UI - 1x/dia\n2. Ômega 3 - 1000mg - 2x/dia",
            height=200
        )
        
        submitted = st.form_submit_button("Gerar Prescrição", use_container_width=True)
        
        if submitted and suplementos:
            try:
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO prescricoes_suplementos (uuid, paciente_id, nutricionista_id, suplementos, validade)
                VALUES (?, ?, ?, ?, ?)
                ''', (str(uuid.uuid4()), paciente[0], user['id'], suplementos, date.today() + timedelta(days=90)))
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
        st.markdown(f'<h2 style="color: #2E7D32;">{user["nome"]}</h2>', unsafe_allow_html=True)
        st.markdown("---")
        
        menu_items = [
            ("Dashboard", "Dashboard"),
            ("Biblioteca de Alimentos", "Alimentos"),
            ("Assistente IA", "Assistente IA"),
            ("Prontuário", "Prontuário"),
            ("Prescrições", "Prescrições"),
            ("Pacientes", "Pacientes")
        ]
        
        for label, page in menu_items:
            if st.button(label, use_container_width=True, 
                        key=f"menu_{page}",
                        type="primary" if st.session_state.page == page else "secondary"):
                st.session_state.page = page
                st.rerun()
        
        st.markdown("---")
        
        if st.button("Sair", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    if st.session_state.page == "Dashboard":
        show_dashboard(user)
    elif st.session_state.page == "Alimentos":
        show_alimentos(user)
    elif st.session_state.page == "Assistente IA":
        show_ai_assistant(user)
    elif st.session_state.page == "Prontuário":
        show_prontuario(user)
    elif st.session_state.page == "Prescrições":
        show_prescricoes(user)
    elif st.session_state.page == "Pacientes":
        show_pacientes(user)

if __name__ == "__main__":
    main()
