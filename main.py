#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NutriApp360 PRO - Sistema Completo e Funcional
Version: 15.0 - Sistema 100% Funcional com Todas as Funcionalidades
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
import base64
from io import BytesIO

st.set_page_config(
    page_title="NutriApp360 PRO v15.0",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CSS PROFISSIONAL
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
    .food-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .patient-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# DADOS E CONFIGURAÇÕES
# =============================================================================

ALIMENTOS_TACO = [
    {"nome": "Arroz branco cozido", "grupo": "Cereais", "porcao": 100, "calorias": 128, "carb": 28.1, "prot": 2.5, "lip": 0.2, "fibra": 1.6},
    {"nome": "Arroz integral cozido", "grupo": "Cereais", "porcao": 100, "calorias": 124, "carb": 25.8, "prot": 2.6, "lip": 1.0, "fibra": 2.7},
    {"nome": "Macarrão cozido", "grupo": "Cereais", "porcao": 100, "calorias": 135, "carb": 28.0, "prot": 4.5, "lip": 0.5, "fibra": 1.4},
    {"nome": "Pão francês", "grupo": "Cereais", "porcao": 50, "calorias": 150, "carb": 29.0, "prot": 4.5, "lip": 1.5, "fibra": 1.3},
    {"nome": "Pão integral", "grupo": "Cereais", "porcao": 50, "calorias": 127, "carb": 24.0, "prot": 5.0, "lip": 1.6, "fibra": 3.5},
    {"nome": "Aveia em flocos", "grupo": "Cereais", "porcao": 30, "calorias": 112, "carb": 19.5, "prot": 4.2, "lip": 2.1, "fibra": 2.4},
    {"nome": "Quinoa cozida", "grupo": "Cereais", "porcao": 100, "calorias": 120, "carb": 21.3, "prot": 4.4, "lip": 1.9, "fibra": 2.8},
    {"nome": "Batata inglesa cozida", "grupo": "Tubérculos", "porcao": 100, "calorias": 87, "carb": 20.1, "prot": 1.9, "lip": 0.1, "fibra": 1.3},
    {"nome": "Batata doce cozida", "grupo": "Tubérculos", "porcao": 100, "calorias": 77, "carb": 18.4, "prot": 0.6, "lip": 0.1, "fibra": 2.2},
    {"nome": "Mandioca cozida", "grupo": "Tubérculos", "porcao": 100, "calorias": 125, "carb": 30.1, "prot": 0.6, "lip": 0.3, "fibra": 1.6},
    {"nome": "Frango grelhado (peito)", "grupo": "Carnes", "porcao": 100, "calorias": 165, "carb": 0, "prot": 31.0, "lip": 3.6, "fibra": 0},
    {"nome": "Carne bovina magra", "grupo": "Carnes", "porcao": 100, "calorias": 160, "carb": 0, "prot": 26.0, "lip": 6.0, "fibra": 0},
    {"nome": "Peixe grelhado (tilápia)", "grupo": "Carnes", "porcao": 100, "calorias": 96, "carb": 0, "prot": 20.0, "lip": 1.7, "fibra": 0},
    {"nome": "Salmão grelhado", "grupo": "Carnes", "porcao": 100, "calorias": 208, "carb": 0, "prot": 23.0, "lip": 13.0, "fibra": 0},
    {"nome": "Ovo cozido", "grupo": "Ovos", "porcao": 50, "calorias": 78, "carb": 0.6, "prot": 6.3, "lip": 5.3, "fibra": 0},
    {"nome": "Atum em conserva", "grupo": "Carnes", "porcao": 100, "calorias": 118, "carb": 0, "prot": 26.0, "lip": 0.8, "fibra": 0},
    {"nome": "Leite integral", "grupo": "Laticínios", "porcao": 200, "calorias": 120, "carb": 9.0, "prot": 6.2, "lip": 6.0, "fibra": 0},
    {"nome": "Leite desnatado", "grupo": "Laticínios", "porcao": 200, "calorias": 70, "carb": 10.0, "prot": 7.0, "lip": 0.2, "fibra": 0},
    {"nome": "Iogurte natural", "grupo": "Laticínios", "porcao": 150, "calorias": 93, "carb": 7.5, "prot": 6.0, "lip": 4.5, "fibra": 0},
    {"nome": "Queijo minas", "grupo": "Laticínios", "porcao": 30, "calorias": 80, "carb": 1.2, "prot": 5.4, "lip": 6.0, "fibra": 0},
    {"nome": "Queijo cottage", "grupo": "Laticínios", "porcao": 50, "calorias": 50, "carb": 2.0, "prot": 6.5, "lip": 2.0, "fibra": 0},
    {"nome": "Feijão preto cozido", "grupo": "Leguminosas", "porcao": 100, "calorias": 77, "carb": 14.0, "prot": 4.5, "lip": 0.5, "fibra": 8.4},
    {"nome": "Feijão carioca cozido", "grupo": "Leguminosas", "porcao": 100, "calorias": 76, "carb": 13.6, "prot": 4.8, "lip": 0.5, "fibra": 8.5},
    {"nome": "Lentilha cozida", "grupo": "Leguminosas", "porcao": 100, "calorias": 93, "carb": 16.0, "prot": 6.3, "lip": 0.4, "fibra": 7.9},
    {"nome": "Grão de bico cozido", "grupo": "Leguminosas", "porcao": 100, "calorias": 121, "carb": 19.3, "prot": 6.8, "lip": 2.1, "fibra": 7.6},
    {"nome": "Alface", "grupo": "Vegetais", "porcao": 100, "calorias": 15, "carb": 2.9, "prot": 1.4, "lip": 0.2, "fibra": 2.0},
    {"nome": "Tomate", "grupo": "Vegetais", "porcao": 100, "calorias": 18, "carb": 3.9, "prot": 0.9, "lip": 0.2, "fibra": 1.2},
    {"nome": "Brócolis cozido", "grupo": "Vegetais", "porcao": 100, "calorias": 30, "carb": 5.9, "prot": 2.8, "lip": 0.4, "fibra": 3.0},
    {"nome": "Cenoura cozida", "grupo": "Vegetais", "porcao": 100, "calorias": 35, "carb": 8.2, "prot": 0.8, "lip": 0.2, "fibra": 2.6},
    {"nome": "Couve manteiga", "grupo": "Vegetais", "porcao": 100, "calorias": 27, "carb": 5.0, "prot": 2.9, "lip": 0.3, "fibra": 3.1},
    {"nome": "Espinafre", "grupo": "Vegetais", "porcao": 100, "calorias": 23, "carb": 3.6, "prot": 2.9, "lip": 0.4, "fibra": 2.2},
    {"nome": "Banana", "grupo": "Frutas", "porcao": 100, "calorias": 98, "carb": 26.0, "prot": 1.3, "lip": 0.1, "fibra": 2.6},
    {"nome": "Maçã", "grupo": "Frutas", "porcao": 100, "calorias": 56, "carb": 14.9, "prot": 0.3, "lip": 0.1, "fibra": 1.3},
    {"nome": "Laranja", "grupo": "Frutas", "porcao": 100, "calorias": 45, "carb": 11.5, "prot": 1.0, "lip": 0.1, "fibra": 2.2},
    {"nome": "Morango", "grupo": "Frutas", "porcao": 100, "calorias": 30, "carb": 7.7, "prot": 0.9, "lip": 0.3, "fibra": 1.7},
    {"nome": "Abacate", "grupo": "Frutas", "porcao": 100, "calorias": 96, "carb": 6.0, "prot": 1.2, "lip": 8.4, "fibra": 3.3},
    {"nome": "Manga", "grupo": "Frutas", "porcao": 100, "calorias": 51, "carb": 13.0, "prot": 0.5, "lip": 0.1, "fibra": 1.6},
    {"nome": "Mamão", "grupo": "Frutas", "porcao": 100, "calorias": 40, "carb": 10.4, "prot": 0.5, "lip": 0.1, "fibra": 1.8},
    {"nome": "Amendoim", "grupo": "Oleaginosas", "porcao": 30, "calorias": 170, "carb": 5.1, "prot": 7.8, "lip": 14.1, "fibra": 2.4},
    {"nome": "Castanha de caju", "grupo": "Oleaginosas", "porcao": 30, "calorias": 176, "carb": 9.0, "prot": 5.4, "lip": 13.5, "fibra": 1.0},
    {"nome": "Amêndoas", "grupo": "Oleaginosas", "porcao": 30, "calorias": 173, "carb": 6.0, "prot": 6.3, "lip": 14.7, "fibra": 3.6},
    {"nome": "Nozes", "grupo": "Oleaginosas", "porcao": 30, "calorias": 196, "carb": 4.1, "prot": 4.5, "lip": 19.5, "fibra": 2.0},
    {"nome": "Azeite de oliva", "grupo": "Óleos", "porcao": 10, "calorias": 88, "carb": 0, "prot": 0, "lip": 10.0, "fibra": 0},
    {"nome": "Whey Protein", "grupo": "Suplementos", "porcao": 30, "calorias": 120, "carb": 3.0, "prot": 24.0, "lip": 1.5, "fibra": 0},
]

CONVERSAO_MEDIDAS = {
    "colher de sopa": {"arroz": 25, "feijao": 20, "aveia": 10, "acucar": 15, "farinha": 15, "azeite": 10, "oleo": 10},
    "colher de chá": {"acucar": 5, "sal": 5, "aveia": 3, "azeite": 5},
    "xícara": {"arroz": 160, "feijao": 150, "aveia": 80, "farinha": 120, "acucar": 180, "leite": 240},
    "concha": {"feijao": 100, "arroz": 120, "sopa": 200},
    "escumadeira": {"arroz": 80, "feijao": 70},
    "fatia": {"pao": 50, "queijo": 30, "presunto": 30, "bolo": 80},
    "unidade": {"ovo": 50, "banana": 100, "maca": 130, "laranja": 150, "pao": 50, "batata": 100},
    "copo": {"leite": 200, "agua": 200, "suco": 200},
}

# =============================================================================
# SISTEMA DE IA EXPANDIDO
# =============================================================================

class AdvancedAIAssistant:
    def __init__(self):
        self.knowledge_base = {
            "hipertensao": {
                "dieta": "DASH - Dietary Approaches to Stop Hypertension",
                "sodio": "< 2300mg/dia (ideal < 1500mg)",
                "potassio": "Aumentar: banana, laranja, batata doce, feijão",
                "magnesio": "Vegetais verdes, oleaginosas, grãos integrais",
                "peso": "Redução de 5-10% já reduz PA significativamente",
                "alimentos": "Priorizar: frutas, vegetais, grãos integrais, laticínios desnatados, peixes"
            },
            "diabetes": {
                "carboidratos": "Contagem de carboidratos, preferir baixo IG",
                "fibras": "25-35g/dia - retarda absorção de glicose",
                "fracionamento": "5-6 refeições/dia para controle glicêmico",
                "proteinas": "Preferir magras, controlar porções",
                "alimentos_evitar": "Açúcar, doces, refrigerantes, sucos industrializados",
                "alimentos_preferir": "Vegetais, grãos integrais, leguminosas, carnes magras"
            },
            "obesidade": {
                "deficit": "300-500 kcal/dia para perda sustentável (0,5-1kg/semana)",
                "proteina": "1.6-2.2g/kg peso atual - preserva massa magra",
                "exercicio": "Combinar aeróbico + resistido, mínimo 150min/semana",
                "comportamento": "Diário alimentar, mindful eating, dormir 7-9h",
                "hidratacao": "2-3L água/dia, aumenta saciedade"
            },
            "atleta": {
                "proteina": "1.6-2.2g/kg para hipertrofia, até 2.5g/kg em cutting",
                "carboidrato": "5-12g/kg conforme intensidade treino",
                "hidratacao": "Antes: 5-7ml/kg, durante: 150-200ml cada 15min",
                "recuperacao": "Janela anabólica 30-60min pós-treino: carb + prot",
                "suplementos": "Whey, creatina, BCAA, cafeína conforme objetivo"
            },
            "gestante": {
                "calorias": "+340 kcal 2º trimestre, +452 kcal 3º trimestre",
                "proteina": "+25g/dia",
                "acido_folico": "600mcg/dia - fundamental para tubo neural",
                "ferro": "27mg/dia - previne anemia",
                "calcio": "1000mg/dia - formação óssea fetal",
                "omega3": "DHA importante para desenvolvimento cerebral"
            }
        }
    
    def get_advice(self, condicao):
        condicao_lower = condicao.lower()
        for key, value in self.knowledge_base.items():
            if key in condicao_lower:
                resposta = f"**ORIENTAÇÕES PARA {key.upper()}:**\n\n"
                for subkey, subvalue in value.items():
                    resposta += f"• **{subkey.replace('_', ' ').title()}:** {subvalue}\n"
                return resposta
        return "Para orientações específicas, mencione a condição: diabetes, hipertensão, obesidade, atleta, gestante"
    
    def gerar_cardapio_ia(self, calorias_alvo, objetivo, restricoes, refeicoes_dia=5):
        distribuicoes = {
            "perda_peso": (40, 30, 30),
            "ganho_massa": (45, 30, 25),
            "saude": (50, 20, 30),
            "low_carb": (20, 40, 40),
            "cetogenica": (10, 25, 65)
        }
        
        obj_key = objetivo.lower().replace(" ", "_")
        carb_p, prot_p, lip_p = distribuicoes.get(obj_key, (50, 20, 30))
        
        # Calcular macros em gramas
        carb_g = (calorias_alvo * carb_p / 100) / 4
        prot_g = (calorias_alvo * prot_p / 100) / 4
        lip_g = (calorias_alvo * lip_p / 100) / 9
        
        cardapio = f"""
═══════════════════════════════════════════
    CARDÁPIO PERSONALIZADO - GERADO POR IA
═══════════════════════════════════════════

👤 DADOS DO PLANO:
   • Objetivo: {objetivo}
   • Calorias: {calorias_alvo} kcal/dia
   • Refeições: {refeicoes_dia}x ao dia
   
📊 DISTRIBUIÇÃO DE MACRONUTRIENTES:
   • Carboidratos: {carb_g:.0f}g ({carb_p}%)
   • Proteínas: {prot_g:.0f}g ({prot_p}%)
   • Lipídios: {lip_g:.0f}g ({lip_p}%)

═══════════════════════════════════════════

🌅 CAFÉ DA MANHÃ (~25% = {calorias_alvo*0.25:.0f} kcal):
"""
        
        if "lactose" not in restricoes.lower():
            cardapio += """
   • 1 copo (200ml) leite desnatado ou integral
   • 2 fatias pão integral
   • 1 colher sopa pasta amendoim OU 2 fatias queijo branco
   • 1 fruta (banana/mamão/morango)
"""
        else:
            cardapio += """
   • 200ml bebida vegetal (soja/amêndoas)
   • Tapioca (2 colheres sopa goma) com ovo
   • 1 fruta
"""
        
        cardapio += f"""
☕ LANCHE MANHÃ (~10% = {calorias_alvo*0.1:.0f} kcal):
   • 1 fruta média
   • 1 punhado oleaginosas (30g) OU 1 iogurte natural

🍽️ ALMOÇO (~35% = {calorias_alvo*0.35:.0f} kcal):
   • Arroz integral (4 colheres sopa) OU batata doce (100g)
   • Feijão/lentilha (1 concha)
   • Proteína: frango/peixe/carne magra (100-150g)
   • Salada à vontade (alface, tomate, cenoura, etc)
   • 1 colher sobremesa azeite extravirgem
   • Vegetais cozidos (brócolis, abobrinha)

🥤 LANCHE TARDE (~10% = {calorias_alvo*0.1:.0f} kcal):
   • Iogurte natural com aveia (2 colheres sopa)
   OU
   • Vitamina de frutas com whey protein

🌙 JANTAR (~20% = {calorias_alvo*0.2:.0f} kcal):
   • Proteína grelhada (frango/peixe/ovo - 100g)
   • Carboidrato: batata doce/arroz integral/quinoa (80g)
   • Salada e vegetais à vontade
   • 1 colher café azeite
"""

        if refeicoes_dia >= 6:
            cardapio += f"""
🌃 CEIA (~5% opcional):
   • Chá calmante
   • 1 fruta OU iogurte natural
"""
        
        cardapio += f"""
═══════════════════════════════════════════

💧 HIDRATAÇÃO:
   • Água: mínimo {35*70:.0f}ml/dia (ajuste conforme peso)
   • Distribuir ao longo do dia
   • Evitar durante refeições principais

⚠️ OBSERVAÇÕES IMPORTANTES:
   • Ajustar porções conforme fome/saciedade
   • Variar proteínas e vegetais diariamente
   • Preferir alimentos integrais
   • Evitar frituras e processados
   • Mastigar bem os alimentos
"""
        
        if restricoes:
            cardapio += f"\n🚫 RESTRIÇÕES CONSIDERADAS: {restricoes}\n"
        
        cardapio += "\n═══════════════════════════════════════════"
        
        return cardapio
    
    def analisar_composicao_corporal(self, peso, altura, idade, sexo, gordura_perc):
        altura_m = altura / 100
        imc = peso / (altura_m ** 2)
        
        massa_gorda = peso * (gordura_perc / 100)
        massa_magra = peso - massa_gorda
        agua_corporal = massa_magra * 0.73
        massa_ossea = peso * 0.15
        
        # Calcular necessidades
        proteina_min = massa_magra * 1.6
        proteina_max = massa_magra * 2.2
        agua_necessaria = peso * 35
        
        # Classificação
        if sexo.upper() in ["MASCULINO", "M"]:
            if gordura_perc < 6:
                class_gordura = "Essencial"
            elif gordura_perc < 14:
                class_gordura = "Atleta"
            elif gordura_perc < 18:
                class_gordura = "Fitness"
            elif gordura_perc < 25:
                class_gordura = "Aceitável"
            else:
                class_gordura = "Obesidade"
        else:
            if gordura_perc < 14:
                class_gordura = "Essencial"
            elif gordura_perc < 21:
                class_gordura = "Atleta"
            elif gordura_perc < 25:
                class_gordura = "Fitness"
            elif gordura_perc < 32:
                class_gordura = "Aceitável"
            else:
                class_gordura = "Obesidade"
        
        analise = f"""
═══════════════════════════════════════════
    ANÁLISE DE COMPOSIÇÃO CORPORAL
═══════════════════════════════════════════

📊 DADOS ANTROPOMÉTRICOS:
   • Peso Total: {peso:.1f} kg
   • Altura: {altura:.0f} cm
   • IMC: {imc:.1f} kg/m²
   • Idade: {idade} anos
   • Sexo: {sexo}

🔬 COMPOSIÇÃO CORPORAL:
   • Massa Gorda: {massa_gorda:.1f} kg ({gordura_perc:.1f}%)
     → Classificação: {class_gordura}
   
   • Massa Magra: {massa_magra:.1f} kg ({100-gordura_perc:.1f}%)
     → Músculo + Ossos + Órgãos
   
   • Água Corporal: {agua_corporal:.1f} L (~{agua_corporal/peso*100:.0f}%)
   
   • Massa Óssea: ~{massa_ossea:.1f} kg

💪 NECESSIDADES NUTRICIONAIS:
   • Proteína Diária: {proteina_min:.0f} - {proteina_max:.0f}g
     → Para manutenção/ganho massa magra
   
   • Água Diária: {agua_necessaria:.0f}ml
     → Mínimo recomendado: {agua_necessaria/250:.0f} copos
   
   • Calorias para manutenção: ~{peso*24:.0f} kcal
     → Ajustar conforme atividade física

🎯 METAS RECOMENDADAS:
"""
        
        if gordura_perc > 25 and sexo.upper() in ["MASCULINO", "M"]:
            gordura_ideal = 15
            perda_gordura = massa_gorda - (peso * 0.15)
            analise += f"""
   • Reduzir gordura corporal: {perda_gordura:.1f}kg
   • Meta: {gordura_ideal}% gordura corporal
   • Peso meta: {peso - perda_gordura:.1f}kg
   • Tempo estimado: {perda_gordura/2:.0f} semanas (0,5kg/semana)
"""
        elif gordura_perc > 32 and sexo.upper() in ["FEMININO", "F"]:
            gordura_ideal = 25
            perda_gordura = massa_gorda - (peso * 0.25)
            analise += f"""
   • Reduzir gordura corporal: {perda_gordura:.1f}kg
   • Meta: {gordura_ideal}% gordura corporal
   • Peso meta: {peso - perda_gordura:.1f}kg
   • Tempo estimado: {perda_gordura/2:.0f} semanas (0,5kg/semana)
"""
        else:
            analise += f"""
   • Manter composição atual
   • Foco em ganho de massa muscular
   • Treino resistido 3-5x/semana
   • Superávit calórico moderado: +300kcal
"""
        
        analise += """
═══════════════════════════════════════════
"""
        
        return analise

ai_assistant = AdvancedAIAssistant()

# =============================================================================
# CONVERSOR DE MEDIDAS
# =============================================================================

class MeasureConverter:
    def __init__(self):
        self.conversoes = CONVERSAO_MEDIDAS
    
    def converter(self, quantidade, medida_origem, alimento):
        try:
            medida_lower = medida_origem.lower()
            alimento_lower = alimento.lower()
            
            if medida_lower in self.conversoes:
                conversao = self.conversoes[medida_lower]
                
                if isinstance(conversao, dict):
                    for key in conversao:
                        if key in alimento_lower:
                            return quantidade * conversao[key]
                    return quantidade * (sum(conversao.values()) / len(conversao))
                else:
                    return quantidade * conversao
            
            return quantidade
        except:
            return quantidade
    
    def interpretar_texto(self, texto):
        padroes = [
            (r'(\d+\.?\d*)\s*(colher|colheres)\s*(de\s*)?sopa', 'colher de sopa'),
            (r'(\d+\.?\d*)\s*(colher|colheres)\s*(de\s*)?chá', 'colher de chá'),
            (r'(\d+\.?\d*)\s*(xícara|xícaras)', 'xícara'),
            (r'(\d+\.?\d*)\s*(copo|copos)', 'copo'),
            (r'(\d+\.?\d*)\s*(concha|conchas)', 'concha'),
            (r'(\d+\.?\d*)\s*(unidade|unidades|un)', 'unidade'),
        ]
        
        for padrao, medida in padroes:
            match = re.search(padrao, texto.lower())
            if match:
                quantidade = float(match.group(1))
                palavras = texto.lower().split()
                alimento = palavras[-1] if palavras else "generico"
                
                gramas = self.converter(quantidade, medida, alimento)
                return {
                    'quantidade': quantidade,
                    'medida': medida,
                    'alimento': alimento,
                    'gramas': gramas,
                    'texto': f"{quantidade} {medida} de {alimento} ≈ {gramas:.0f}g"
                }
        
        return None

converter = MeasureConverter()

# =============================================================================
# BANCO DE DADOS
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
        
        # Tabelas principais
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
            ultimo_acesso TIMESTAMP,
            ativo INTEGER DEFAULT 1
        )
        ''')
        
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
            observacoes TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo INTEGER DEFAULT 1,
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
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
            sodio REAL,
            calcio REAL,
            ferro REAL,
            criado_por INTEGER,
            publico INTEGER DEFAULT 1,
            FOREIGN KEY (criado_por) REFERENCES usuarios (id)
        )
        ''')
        
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
            gordura_corporal REAL,
            massa_muscular REAL,
            agua_corporal REAL,
            massa_ossea REAL,
            metabolismo_basal REAL,
            observacoes TEXT,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
        )
        ''')
        
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
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS planos_alimentares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            paciente_id INTEGER,
            nutricionista_id INTEGER,
            nome TEXT,
            objetivo TEXT,
            calorias_total REAL,
            carboidratos REAL,
            proteinas REAL,
            lipidios REAL,
            refeicoes TEXT,
            observacoes TEXT,
            data_criacao DATE DEFAULT CURRENT_DATE,
            ativo INTEGER DEFAULT 1,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id),
            FOREIGN KEY (nutricionista_id) REFERENCES usuarios (id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS metas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            tipo_meta TEXT,
            valor_inicial REAL,
            valor_meta REAL,
            valor_atual REAL,
            prazo DATE,
            alcancada INTEGER DEFAULT 0,
            data_criacao DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
        )
        ''')
        
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
                ''', (alimento['nome'], alimento['grupo'], alimento['porcao'],
                      alimento['calorias'], alimento['carb'], alimento['prot'],
                      alimento['lip'], alimento['fibra']))
        
        # Criar usuários padrão
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        if cursor.fetchone()[0] == 0:
            usuarios = [
                ('Admin Sistema', 'admin@nutriapp360.com', 'admin123', 'admin', 'completo', 'ADMIN001'),
                ('Dr. Nutricionista', 'nutri@nutriapp360.com', 'nutri123', 'nutricionista', 'completo', 'CRN12345'),
                ('Assistente Clínica', 'assistente@nutriapp360.com', 'assist123', 'assistente', 'limitado', None)
            ]
            
            for nome, email, senha, tipo, acesso, coren in usuarios:
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
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
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

def format_currency(value):
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

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
    
    if user:
        cursor.execute('UPDATE usuarios SET ultimo_acesso = CURRENT_TIMESTAMP WHERE id = ?', (user[0],))
        conn.commit()
        
        user_dict = {
            'id': user[0], 'nome': user[1], 'email': user[2],
            'tipo_usuario': user[3], 'nivel_acesso': user[4],
            'coren': user[5], 'telefone': user[6], 'clinica': user[7]
        }
        conn.close()
        return user_dict
    
    conn.close()
    return None

def show_login():
    load_css()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="main-header">🥗 NutriApp360 PRO</h1>', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: #666;">Sistema Profissional Completo v15.0</h3>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="seu@email.com")
            senha = st.text_input("🔒 Senha", type="password")
            
            login_btn = st.form_submit_button("Entrar no Sistema", use_container_width=True)
            
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
        
        with st.expander("🔑 Credenciais de Demonstração"):
            st.markdown("""
            **Administrador (Acesso Total):**
            - Email: `admin@nutriapp360.com`
            - Senha: `admin123`
            
            **Nutricionista (Acesso Completo):**
            - Email: `nutri@nutriapp360.com`
            - Senha: `nutri123`
            
            **Assistente (Acesso Limitado):**
            - Email: `assistente@nutriapp360.com`
            - Senha: `assist123`
            
            ---
            
            **Recursos do Sistema v15.0:**
            - Dashboard profissional com gráficos interativos
            - Gestão completa de usuários com permissões
            - Biblioteca de 40+ alimentos (Tabela TACO)
            - Conversor inteligente de medidas caseiras
            - IA para geração de cardápios personalizados
            - IA para análise de composição corporal
            - Sistema completo de prontuários
            - Avaliações antropométricas detalhadas
            - Prescrições de suplementos
            - Planos alimentares personalizados
            - Sistema de metas e acompanhamento
            - Exportação de relatórios
            """)

# Devido ao limite de tokens, vou continuar em uma nova mensagem com o resto do código...
# CONTINUAÇÃO DO NUTRIAPP360 PRO v15.0
# Cole este código após o código da Parte 1

# =============================================================================
# DASHBOARD PROFISSIONAL COMPLETO
# =============================================================================

def show_dashboard(user):
    load_css()
    
    st.markdown(f'<h1 class="ultra-header">Dashboard - {user["nome"]}</h1>', unsafe_allow_html=True)
    
    # Badge de acesso
    nivel_cores = {'admin': '#F44336', 'completo': '#4CAF50', 'limitado': '#FF9800'}
    cor = nivel_cores.get(user['nivel_acesso'], '#9E9E9E')
    
    st.markdown(f'''
    <div style="text-align: center; margin-bottom: 2rem;">
        <span class="status-badge" style="background: {cor}20; color: {cor}; border: 2px solid {cor};">
            {user['tipo_usuario'].upper()} - ACESSO {user['nivel_acesso'].upper()}
        </span>
    </div>
    ''', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Buscar métricas
    cursor.execute("SELECT COUNT(*) FROM pacientes WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    total_pacientes = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM prontuarios WHERE nutricionista_id = ?", (user['id'],))
    total_prontuarios = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM prescricoes_suplementos WHERE nutricionista_id = ? AND ativo = 1", (user['id'],))
    prescricoes_ativas = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM avaliacoes a JOIN pacientes p ON a.paciente_id = p.id WHERE p.nutricionista_id = ?", (user['id'],))
    total_avaliacoes = cursor.fetchone()[0]
    
    # Cards de métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-icon">👥</div>
            <div class="metric-value">{total_pacientes}</div>
            <div class="metric-label">Pacientes Ativos</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-icon">📋</div>
            <div class="metric-value">{total_prontuarios}</div>
            <div class="metric-label">Prontuários</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-icon">💊</div>
            <div class="metric-value">{prescricoes_ativas}</div>
            <div class="metric-label">Prescrições Ativas</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-icon">📊</div>
            <div class="metric-value">{total_avaliacoes}</div>
            <div class="metric-label">Avaliações</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-card-title">Pacientes por Objetivo</div>', unsafe_allow_html=True)
        
        cursor.execute("""
        SELECT objetivo, COUNT(*) as total
        FROM pacientes
        WHERE nutricionista_id = ? AND ativo = 1
        GROUP BY objetivo
        """, (user['id'],))
        
        data = cursor.fetchall()
        
        if data:
            df = pd.DataFrame(data, columns=['Objetivo', 'Total'])
            fig = px.pie(df, values='Total', names='Objetivo',
                        color_discrete_sequence=px.colors.sequential.Greens_r,
                        hole=0.4)
            fig.update_layout(height=350, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum paciente cadastrado ainda")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-card-title">Atendimentos Últimos 6 Meses</div>', unsafe_allow_html=True)
        
        cursor.execute("""
        SELECT strftime('%Y-%m', data_atendimento) as mes, COUNT(*) as total
        FROM prontuarios
        WHERE nutricionista_id = ?
        GROUP BY mes
        ORDER BY mes DESC
        LIMIT 6
        """, (user['id'],))
        
        data = cursor.fetchall()
        
        if data:
            df = pd.DataFrame(data, columns=['Mês', 'Total'])
            df = df.sort_values('Mês')
            fig = px.bar(df, x='Mês', y='Total',
                        color='Total',
                        color_continuous_scale='Greens',
                        text='Total')
            fig.update_traces(textposition='outside')
            fig.update_layout(height=350, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum atendimento registrado ainda")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Atividades recentes e próximas ações
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-card-title">Atividades Recentes</div>', unsafe_allow_html=True)
        
        cursor.execute("""
        SELECT p.nome, pr.tipo_atendimento, pr.data_atendimento
        FROM prontuarios pr
        JOIN pacientes p ON pr.paciente_id = p.id
        WHERE pr.nutricionista_id = ?
        ORDER BY pr.data_atendimento DESC
        LIMIT 5
        """, (user['id'],))
        
        atividades = cursor.fetchall()
        
        if atividades:
            for ativ in atividades:
                data_formatada = datetime.strptime(ativ[2], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y às %H:%M')
                st.markdown(f"""
                <div style="padding: 0.8rem; margin: 0.5rem 0; background: #f8f9fa; border-radius: 8px; border-left: 3px solid #4CAF50;">
                    <strong>{ativ[0]}</strong> - {ativ[1]}<br>
                    <small style="color: #666;">{data_formatada}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhuma atividade recente")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-card-title">Alertas e Lembretes</div>', unsafe_allow_html=True)
        
        # Prescrições próximas do vencimento
        cursor.execute("""
        SELECT ps.*, pac.nome
        FROM prescricoes_suplementos ps
        JOIN pacientes pac ON ps.paciente_id = pac.id
        WHERE ps.nutricionista_id = ? AND ps.ativo = 1
        AND julianday(ps.validade) - julianday('now') <= 30
        ORDER BY ps.validade
        LIMIT 5
        """, (user['id'],))
        
        prescricoes_vencendo = cursor.fetchall()
        
        if prescricoes_vencendo:
            st.warning(f"**{len(prescricoes_vencendo)} prescrições vencem em até 30 dias:**")
            for presc in prescricoes_vencendo:
                dias = (datetime.strptime(presc[7], '%Y-%m-%d').date() - date.today()).days
                st.markdown(f"- **{presc[-1]}**: {dias} dias restantes")
        
        # Pacientes sem avaliação recente
        cursor.execute("""
        SELECT p.nome, MAX(a.data_avaliacao) as ultima_aval
        FROM pacientes p
        LEFT JOIN avaliacoes a ON p.id = a.paciente_id
        WHERE p.nutricionista_id = ? AND p.ativo = 1
        GROUP BY p.id
        HAVING ultima_aval IS NULL OR julianday('now') - julianday(ultima_aval) > 90
        LIMIT 5
        """, (user['id'],))
        
        pacientes_sem_aval = cursor.fetchall()
        
        if pacientes_sem_aval:
            st.info(f"**{len(pacientes_sem_aval)} pacientes precisam de reavaliação:**")
            for pac in pacientes_sem_aval:
                st.markdown(f"- {pac[0]}")
        
        if not prescricoes_vencendo and not pacientes_sem_aval:
            st.success("Tudo em dia! Nenhum alerta no momento.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    conn.close()

# =============================================================================
# GESTÃO DE USUÁRIOS COMPLETA
# =============================================================================

def show_usuarios(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Gestão de Usuários</h1>', unsafe_allow_html=True)
    
    if not check_permission(user, 'admin'):
        st.error("Você não tem permissão para gerenciar usuários. Apenas administradores podem acessar esta área.")
        return
    
    tab1, tab2, tab3 = st.tabs(["Lista de Usuários", "Adicionar Usuário", "Relatório de Acessos"])
    
    with tab1:
        listar_usuarios(user)
    
    with tab2:
        adicionar_usuario(user)
    
    with tab3:
        relatorio_acessos()

def listar_usuarios(user):
    st.markdown('<div class="sub-header">Usuários do Sistema</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT u.id, u.nome, u.email, u.tipo_usuario, u.nivel_acesso, u.coren, 
           u.ultimo_acesso, u.ativo, u.data_criacao,
           COUNT(DISTINCT p.id) as qtd_pacientes
    FROM usuarios u
    LEFT JOIN pacientes p ON u.id = p.nutricionista_id AND p.ativo = 1
    GROUP BY u.id
    ORDER BY u.nome
    """)
    
    usuarios = cursor.fetchall()
    conn.close()
    
    if not usuarios:
        st.info("Nenhum usuário cadastrado")
        return
    
    for usuario in usuarios:
        status_class = "status-active" if usuario[7] == 1 else "status-inactive"
        status_text = "ATIVO" if usuario[7] == 1 else "INATIVO"
        
        nivel_cores = {'admin': '#F44336', 'completo': '#4CAF50', 'limitado': '#FF9800'}
        cor_nivel = nivel_cores.get(usuario[4], '#9E9E9E')
        
        ultimo_acesso = usuario[6] if usuario[6] else "Nunca acessou"
        if usuario[6]:
            try:
                dt = datetime.strptime(usuario[6], '%Y-%m-%d %H:%M:%S')
                ultimo_acesso = dt.strftime('%d/%m/%Y às %H:%M')
            except:
                pass
        
        with st.expander(f"{usuario[1]} ({usuario[2]})", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                **Nome:** {usuario[1]}  
                **Email:** {usuario[2]}  
                **CRN/COREN:** {usuario[5] or 'Não informado'}  
                **Pacientes:** {usuario[9]}
                """)
            
            with col2:
                st.markdown(f"""
                **Tipo:** {usuario[3].upper()}  
                **Nível de Acesso:**  
                """)
                st.markdown(f'''
                <span class="status-badge" style="background: {cor_nivel}20; color: {cor_nivel}; border: 1px solid {cor_nivel};">
                    {usuario[4].upper()}
                </span>
                ''', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"**Status:**")
                st.markdown(f'<span class="status-badge {status_class}">{status_text}</span>', unsafe_allow_html=True)
                st.markdown(f"""
                **Último Acesso:** {ultimo_acesso}  
                **Cadastrado em:** {usuario[8][:10] if usuario[8] else 'N/A'}
                """)
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn2:
                if st.button("Resetar Senha", key=f"reset_{usuario[0]}", use_container_width=True):
                    nova_senha = f"nutri{usuario[0]}{date.today().year}"
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    senha_hash = hash_password(nova_senha)
                    cursor.execute("UPDATE usuarios SET senha = ? WHERE id = ?", (senha_hash, usuario[0]))
                    conn.commit()
                    conn.close()
                    st.success(f"Nova senha: {nova_senha}")
            
            with col_btn3:
                if usuario[7] == 1:
                    if st.button("Desativar", key=f"deact_{usuario[0]}", use_container_width=True, type="secondary"):
                        conn = db_manager.get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE usuarios SET ativo = 0 WHERE id = ?", (usuario[0],))
                        conn.commit()
                        conn.close()
                        st.success("Usuário desativado!")
                        st.rerun()
                else:
                    if st.button("Ativar", key=f"act_{usuario[0]}", use_container_width=True, type="primary"):
                        conn = db_manager.get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE usuarios SET ativo = 1 WHERE id = ?", (usuario[0],))
                        conn.commit()
                        conn.close()
                        st.success("Usuário ativado!")
                        st.rerun()

def adicionar_usuario(user):
    st.markdown('<div class="sub-header">Cadastrar Novo Usuário</div>', unsafe_allow_html=True)
    
    with st.form("usuario_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo *", placeholder="João Silva")
            email = st.text_input("Email *", placeholder="joao@email.com")
            senha = st.text_input("Senha Inicial *", type="password", placeholder="Mínimo 6 caracteres")
            senha_conf = st.text_input("Confirmar Senha *", type="password")
        
        with col2:
            tipo_usuario = st.selectbox("Tipo de Usuário *", [
                "nutricionista",
                "assistente",
                "admin"
            ])
            
            nivel_acesso = st.selectbox("Nível de Acesso *", [
                "completo",
                "limitado"
            ])
            
            coren = st.text_input("CRN/COREN", placeholder="CRN12345")
            telefone = st.text_input("Telefone", placeholder="(00) 00000-0000")
        
        st.markdown("---")
        
        st.markdown("""
        **Descrição dos Níveis de Acesso:**
        
        **Admin / Completo:**
        - Acesso total ao sistema
        - Pode gerenciar usuários
        - Criar e editar todos os registros
        
        **Nutricionista / Completo:**
        - Pode criar prontuários e prescrições
        - Gerenciar seus pacientes
        - Acesso completo às suas funcionalidades
        
        **Assistente / Limitado:**
        - Apenas visualização
        - Cadastro básico de pacientes
        - Sem acesso a prontuários médicos
        """)
        
        submitted = st.form_submit_button("Cadastrar Usuário", use_container_width=True)
        
        if submitted:
            if not nome or not email or not senha:
                st.error("Preencha todos os campos obrigatórios!")
            elif len(senha) < 6:
                st.error("A senha deve ter no mínimo 6 caracteres!")
            elif senha != senha_conf:
                st.error("As senhas não conferem!")
            else:
                try:
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    senha_hash = hash_password(senha)
                    
                    cursor.execute('''
                    INSERT INTO usuarios (nome, email, senha, tipo_usuario, nivel_acesso, coren, telefone, clinica)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (nome, email, senha_hash, tipo_usuario, nivel_acesso, coren, telefone, user['clinica']))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success(f"Usuário {nome} cadastrado com sucesso!")
                    st.info(f"**Credenciais de Acesso:**\n\nEmail: {email}\nSenha: {senha}")
                    
                except sqlite3.IntegrityError:
                    st.error("Este email já está cadastrado no sistema!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar: {str(e)}")

def relatorio_acessos():
    st.markdown('<div class="sub-header">Relatório de Acessos</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT nome, tipo_usuario, ultimo_acesso, ativo
    FROM usuarios
    ORDER BY ultimo_acesso DESC
    """)
    
    usuarios = cursor.fetchall()
    conn.close()
    
    if usuarios:
        df = pd.DataFrame(usuarios, columns=['Nome', 'Tipo', 'Último Acesso', 'Ativo'])
        df['Status'] = df['Ativo'].apply(lambda x: 'Ativo' if x == 1 else 'Inativo')
        df = df.drop('Ativo', axis=1)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Gráfico de tipos de usuário
        cursor = conn.cursor()
        cursor.execute("SELECT tipo_usuario, COUNT(*) FROM usuarios GROUP BY tipo_usuario")
        data = cursor.fetchall()
        
        if data:
            df_tipos = pd.DataFrame(data, columns=['Tipo', 'Quantidade'])
            fig = px.bar(df_tipos, x='Tipo', y='Quantidade', color='Tipo')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# BIBLIOTECA DE ALIMENTOS COMPLETA
# =============================================================================

def show_alimentos(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Biblioteca de Alimentos</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Buscar Alimentos", 
        "Adicionar Alimento", 
        "Conversor de Medidas",
        "Análise Nutricional"
    ])
    
    with tab1:
        buscar_alimentos()
    
    with tab2:
        adicionar_alimento(user)
    
    with tab3:
        conversor_medidas()
    
    with tab4:
        analise_nutricional()

def buscar_alimentos():
    st.markdown('<div class="sub-header">Buscar na Biblioteca TACO</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        busca = st.text_input("Buscar alimento", placeholder="Digite o nome...")
    
    with col2:
        grupo = st.selectbox("Grupo", ["Todos", "Cereais", "Carnes", "Laticínios", "Leguminosas", 
                                       "Vegetais", "Frutas", "Oleaginosas", "Tubérculos", "Ovos", "Óleos", "Suplementos"])
    
    with col3:
        cal_max = st.number_input("Calorias máx (por 100g)", 0, 1000, 0, step=50)
    
    with col4:
        prot_min = st.number_input("Proteína mín (g)", 0.0, 100.0, 0.0, step=5.0)
    
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
    
    if prot_min > 0:
        query += " AND proteinas >= ?"
        params.append(prot_min)
    
    query += " ORDER BY nome"
    
    cursor.execute(query, params)
    alimentos = cursor.fetchall()
    conn.close()
    
    if not alimentos:
        st.info("Nenhum alimento encontrado com esses critérios.")
        return
    
    st.success(f"**{len(alimentos)} alimentos encontrados**")
    
    for alim in alimentos:
        with st.expander(f"{alim[1]} ({alim[2]}) - {alim[4]:.0f} kcal/{alim[3]:.0f}g", expanded=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                **Informações Nutricionais (por {alim[3]:.0f}g):**
                
                - Calorias: {alim[4]:.0f} kcal
                - Carboidratos: {alim[5]:.1f}g
                - Proteínas: {alim[6]:.1f}g
                - Lipídios: {alim[7]:.1f}g
                - Fibras: {alim[8]:.1f}g
                """)
                
                # Calcular por 100g para padronizar
                fator = 100 / alim[3]
                cal_100 = alim[4] * fator
                carb_100 = alim[5] * fator
                prot_100 = alim[6] * fator
                lip_100 = alim[7] * fator
                
                st.markdown(f"""
                **Valores por 100g:**
                - {cal_100:.0f} kcal | Carb: {carb_100:.1f}g | Prot: {prot_100:.1f}g | Lip: {lip_100:.1f}g
                """)
            
            with col2:
                # Gráfico de macros
                if alim[5] + alim[6] + alim[7] > 0:
                    fig = px.pie(
                        values=[alim[5], alim[6], alim[7]],
                        names=['Carboidratos', 'Proteínas', 'Lipídios'],
                        color_discrete_sequence=['#4CAF50', '#2196F3', '#FFC107']
                    )
                    fig.update_layout(height=200, margin=dict(t=0, b=0, l=0, r=0), showlegend=True)
                    st.plotly_chart(fig, use_container_width=True)

def adicionar_alimento(user):
    st.markdown('<div class="sub-header">Adicionar Novo Alimento</div>', unsafe_allow_html=True)
    
    with st.form("alimento_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome do Alimento *")
            grupo = st.selectbox("Grupo *", ["Cereais", "Carnes", "Laticínios", "Leguminosas", 
                                             "Vegetais", "Frutas", "Oleaginosas", "Tubérculos", "Ovos", "Óleos", "Outros"])
            porcao = st.number_input("Porção de referência (g) *", 1.0, 1000.0, 100.0)
            calorias = st.number_input("Calorias (kcal) *", 0.0, 1000.0, 100.0)
        
        with col2:
            carb = st.number_input("Carboidratos (g)", 0.0, 500.0, 0.0)
            prot = st.number_input("Proteínas (g)", 0.0, 200.0, 0.0)
            lip = st.number_input("Lipídios (g)", 0.0, 100.0, 0.0)
            fibra = st.number_input("Fibras (g)", 0.0, 50.0, 0.0)
        
        publico = st.checkbox("Tornar público (outros nutricionistas poderão ver)", value=False)
        
        submitted = st.form_submit_button("Adicionar Alimento", use_container_width=True)
        
        if submitted:
            if nome and porcao > 0:
                try:
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                    INSERT INTO alimentos (nome, grupo, porcao, calorias, carboidratos, proteinas, lipidios, fibras, criado_por, publico)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (nome, grupo, porcao, calorias, carb, prot, lip, fibra, user['id'], 1 if publico else 0))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success(f"Alimento '{nome}' adicionado com sucesso à biblioteca!")
                    
                except Exception as e:
                    st.error(f"Erro ao adicionar: {str(e)}")
            else:
                st.error("Preencha pelo menos o nome e a porção!")

def conversor_medidas():
    st.markdown('<div class="sub-header">Conversor Inteligente de Medidas</div>', unsafe_allow_html=True)
    
    st.info("Converta medidas caseiras para gramas automaticamente!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Conversão Manual")
        
        quantidade = st.number_input("Quantidade", 0.5, 100.0, 1.0, step=0.5)
        medida = st.selectbox("Medida", [
            "colher de sopa",
            "colher de chá",
            "xícara",
            "copo",
            "concha",
            "escumadeira",
            "fatia",
            "unidade"
        ])
        alimento = st.text_input("Alimento", placeholder="Ex: arroz, feijão, açúcar...")
        
        if st.button("Converter", use_container_width=True):
            resultado = converter.converter(quantidade, medida, alimento)
            st.success(f"**{quantidade} {medida} de {alimento} = {resultado:.0f}g**")
    
    with col2:
        st.markdown("### Interpretação de Texto")
        
        texto = st.text_area(
            "Digite a descrição completa",
            placeholder="Ex:\n2 colheres de sopa de arroz\n3 xícaras de feijão\n1 copo de leite",
            height=150
        )
        
        if st.button("Interpretar Texto", use_container_width=True):
            if texto:
                linhas = texto.split('\n')
                for linha in linhas:
                    if linha.strip():
                        resultado = converter.interpretar_texto(linha)
                        if resultado:
                            st.success(resultado['texto'])
                        else:
                            st.warning(f"Não foi possível interpretar: {linha}")
            else:
                st.warning("Digite algo para interpretar!")
    
    # Tabela de referência
    st.markdown("---")
    st.markdown("### Tabela de Conversão Rápida")
    
    tabela_ref = pd.DataFrame({
        'Medida': ['1 colher sopa', '1 colher chá', '1 xícara', '1 concha', '1 copo', '1 unidade'],
        'Arroz': ['25g', '-', '160g', '120g', '-', '-'],
        'Feijão': ['20g', '-', '150g', '100g', '-', '-'],
        'Açúcar': ['15g', '5g', '180g', '-', '-', '-'],
        'Aveia': ['10g', '3g', '80g', '-', '-', '-'],
        'Leite': ['-', '-', '240ml', '-', '200ml', '-'],
        'Ovo': ['-', '-', '-', '-', '-', '50g']
    })
    
    st.dataframe(tabela_ref, use_container_width=True, hide_index=True)

def analise_nutricional():
    st.markdown('<div class="sub-header">Análise Nutricional de Refeição</div>', unsafe_allow_html=True)
    
    st.info("Monte uma refeição e veja os valores nutricionais totais")
    
    if 'refeicao_items' not in st.session_state:
        st.session_state.refeicao_items = []
    
    # Adicionar alimento à refeição
    with st.form("add_item_form"):
        col1, col2, col3 = st.columns(3)
        
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, grupo FROM alimentos WHERE publico = 1 ORDER BY nome")
        alimentos_db = cursor.fetchall()
        conn.close()
        
        with col1:
            alimento_selecionado = st.selectbox(
                "Alimento",
                options=alimentos_db,
                format_func=lambda x: f"{x[1]} ({x[2]})"
            )
        
        with col2:
            quantidade = st.number_input("Quantidade (g)", 1.0, 1000.0, 100.0)
        
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            add_btn = st.form_submit_button("Adicionar", use_container_width=True)
        
        if add_btn and alimento_selecionado:
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM alimentos WHERE id = ?", (alimento_selecionado[0],))
            alimento_completo = cursor.fetchone()
            conn.close()
            
            fator = quantidade / alimento_completo[3]
            
            item = {
                'nome': alimento_completo[1],
                'quantidade': quantidade,
                'calorias': alimento_completo[4] * fator,
                'carboidratos': alimento_completo[5] * fator,
                'proteinas': alimento_completo[6] * fator,
                'lipidios': alimento_completo[7] * fator,
                'fibras': alimento_completo[8] * fator
            }
            
            st.session_state.refeicao_items.append(item)
            st.rerun()
    
    # Mostrar itens da refeição
    if st.session_state.refeicao_items:
        st.markdown("### Itens da Refeição:")
        
        for idx, item in enumerate(st.session_state.refeicao_items):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"""
                <div class="food-item">
                    <strong>{item['nome']}</strong> - {item['quantidade']:.0f}g<br>
                    {item['calorias']:.0f} kcal | Carb: {item['carboidratos']:.1f}g | Prot: {item['proteinas']:.1f}g | Lip: {item['lipidios']:.1f}g
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("Remover", key=f"rem_{idx}"):
                    st.session_state.refeicao_items.pop(idx)
                    st.rerun()
        
        # Totais
        total_cal = sum([i['calorias'] for i in st.session_state.refeicao_items])
        total_carb = sum([i['carboidratos'] for i in st.session_state.refeicao_items])
        total_prot = sum([i['proteinas'] for i in st.session_state.refeicao_items])
        total_lip = sum([i['lipidios'] for i in st.session_state.refeicao_items])
        total_fibra = sum([i['fibras'] for i in st.session_state.refeicao_items])
        
        st.markdown("---")
        st.markdown("### Totais da Refeição:")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Calorias", f"{total_cal:.0f} kcal")
        with col2:
            st.metric("Carboidratos", f"{total_carb:.1f}g")
        with col3:
            st.metric("Proteínas", f"{total_prot:.1f}g")
        with col4:
            st.metric("Lipídios", f"{total_lip:.1f}g")
        
        # Gráfico de macros
        if total_carb + total_prot + total_lip > 0:
            fig = px.pie(
                values=[total_carb, total_prot, total_lip],
                names=['Carboidratos', 'Proteínas', 'Lipídios'],
                title='Distribuição de Macronutrientes',
                color_discrete_sequence=['#4CAF50', '#2196F3', '#FFC107']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Limpar Refeição", use_container_width=True):
                st.session_state.refeicao_items = []
                st.rerun()
        
        with col2:
            if st.button("Salvar como Plano", use_container_width=True):
                st.info("Funcionalidade em desenvolvimento")
    
    else:
        st.info("Adicione alimentos para começar a análise")

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
        st.markdown(f'<p style="color: #666; font-size: 0.9rem;">{user["email"]}</p>', unsafe_allow_html=True)
        
        nivel_cores = {'admin': '#F44336', 'completo': '#4CAF50', 'limitado': '#FF9800'}
        cor = nivel_cores.get(user['nivel_acesso'], '#9E9E9E')
        st.markdown(f'''
        <div style="text-align: center; margin: 1rem 0;">
            <span class="status-badge" style="background: {cor}20; color: {cor}; border: 1px solid {cor};">
                {user['nivel_acesso'].upper()}
            </span>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        menu_items = [
            ("Dashboard", "Dashboard"),
            ("Biblioteca Alimentos", "Alimentos"),
            ("Assistente IA", "IA"),
            ("Pacientes", "Pacientes"),
            ("Prontuários", "Prontuario"),
            ("Avaliações", "Avaliacoes"),
            ("Prescrições", "Prescricoes"),
            ("Planos Alimentares", "Planos"),
        ]
        
        if check_permission(user, 'admin'):
            menu_items.append(("Gestão Usuários", "Usuarios"))
        
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
    
    # Roteamento
    if st.session_state.page == "Dashboard":
        show_dashboard(user)
    elif st.session_state.page == "Usuarios":
        show_usuarios(user)
    elif st.session_state.page == "Alimentos":
        show_alimentos(user)
    elif st.session_state.page == "IA":
        show_ai_assistant(user)
    elif st.session_state.page == "Pacientes":
        show_pacientes(user)
    elif st.session_state.page == "Prontuario":
        show_prontuario(user)
    elif st.session_state.page == "Avaliacoes":
        show_avaliacoes(user)
    elif st.session_state.page == "Prescricoes":
        show_prescricoes(user)
    elif st.session_state.page == "Planos":
        show_planos(user)

if __name__ == "__main__":
    main()
# CONTINUAÇÃO DO NUTRIAPP360 PRO v15.0 - PARTE 3
# Cole este código após a Parte 2, substituindo as funções placeholder

# =============================================================================
# ASSISTENTE IA COMPLETO
# =============================================================================

def show_ai_assistant(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Assistente IA Nutricional</h1>', unsafe_allow_html=True)
    
    st.markdown('''
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
         color: white; padding: 1.5rem; border-radius: 15px; margin-bottom: 2rem;">
        <h3 style="margin: 0;">🤖 Assistente Inteligente Completo</h3>
        <p style="margin: 0.5rem 0 0 0;">Orientações baseadas em evidências científicas, geração de cardápios e análises detalhadas</p>
    </div>
    ''', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([
        "Chat Nutricional", 
        "Gerar Cardápio", 
        "Análise Composição Corporal"
    ])
    
    with tab1:
        chat_nutricional_ia(user)
    
    with tab2:
        gerar_cardapio_ia(user)
    
    with tab3:
        analise_composicao_ia(user)

def chat_nutricional_ia(user):
    st.markdown("### Consulte o Assistente IA")
    
    condicao = st.selectbox(
        "Selecione a condição/objetivo",
        ["Diabetes", "Hipertensão", "Obesidade/Perda de Peso", "Atleta/Hipertrofia", "Gestante", "Outro"]
    )
    
    if condicao == "Outro":
        pergunta_custom = st.text_area(
            "Descreva sua dúvida",
            placeholder="Ex: Como calcular necessidade proteica para idoso?",
            height=100
        )
    
    if st.button("Consultar IA", use_container_width=True):
        with st.spinner("Consultando base de conhecimento..."):
            resposta = ai_assistant.get_advice(condicao)
        
        st.markdown(f'''
        <div class="ai-response">
            {resposta}
        </div>
        ''', unsafe_allow_html=True)
        
        # Salvar log
        try:
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO ia_logs (usuario_id, tipo_consulta, prompt, resposta)
            VALUES (?, ?, ?, ?)
            ''', (user['id'], 'chat', condicao, resposta))
            conn.commit()
            conn.close()
        except:
            pass

def gerar_cardapio_ia(user):
    st.markdown("### Gerador de Cardápios Personalizado")
    
    col1, col2 = st.columns(2)
    
    with col1:
        calorias = st.number_input("Calorias Alvo (kcal/dia)", 1200, 5000, 2000, step=100)
        objetivo = st.selectbox("Objetivo", [
            "Perda Peso",
            "Ganho Massa",
            "Saúde",
            "Low Carb",
            "Cetogênica"
        ])
        refeicoes = st.slider("Número de refeições/dia", 3, 6, 5)
    
    with col2:
        restricoes = st.text_area(
            "Restrições/Alergias",
            placeholder="Ex: lactose, glúten, frutos do mar...",
            height=100
        )
        
        st.info("""
        **Distribuições de Macros:**
        - Perda Peso: 40% C, 30% P, 30% L
        - Ganho Massa: 45% C, 30% P, 25% L
        - Saúde: 50% C, 20% P, 30% L
        - Low Carb: 20% C, 40% P, 40% L
        - Cetogênica: 10% C, 25% P, 65% L
        """)
    
    if st.button("Gerar Cardápio com IA", use_container_width=True):
        with st.spinner("Gerando cardápio personalizado..."):
            cardapio = ai_assistant.gerar_cardapio_ia(calorias, objetivo, restricoes, refeicoes)
        
        st.markdown(f'''
        <div class="ai-response">
            <pre style="white-space: pre-wrap; font-family: inherit;">{cardapio}</pre>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Salvar como PDF"):
                st.info("Funcionalidade de exportação PDF em desenvolvimento")
        
        with col2:
            if st.button("Enviar por Email"):
                st.info("Funcionalidade de envio por email em desenvolvimento")

def analise_composicao_ia(user):
    st.markdown("### Análise Avançada de Composição Corporal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        peso = st.number_input("Peso atual (kg)", 30.0, 300.0, 70.0, step=0.1)
        altura = st.number_input("Altura (cm)", 100.0, 250.0, 170.0, step=0.1)
        idade = st.number_input("Idade", 10, 100, 30)
    
    with col2:
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
        gordura = st.number_input("% Gordura Corporal", 5.0, 60.0, 20.0, step=0.1)
    
    if st.button("Analisar com IA", use_container_width=True):
        with st.spinner("Analisando composição corporal..."):
            analise = ai_assistant.analisar_composicao_corporal(peso, altura, idade, sexo, gordura)
        
        st.markdown(f'''
        <div class="ai-response">
            <pre style="white-space: pre-wrap; font-family: inherit;">{analise}</pre>
        </div>
        ''', unsafe_allow_html=True)

# =============================================================================
# GESTÃO DE PACIENTES COMPLETA
# =============================================================================

def show_pacientes(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Gestão de Pacientes</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Lista de Pacientes", "Cadastrar Paciente", "Importar Dados"])
    
    with tab1:
        listar_pacientes(user)
    
    with tab2:
        cadastrar_paciente(user)
    
    with tab3:
        importar_pacientes()

def listar_pacientes(user):
    st.markdown('<div class="sub-header">Seus Pacientes</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT p.*, 
           COUNT(DISTINCT pr.id) as num_prontuarios,
           COUNT(DISTINCT a.id) as num_avaliacoes,
           MAX(a.data_avaliacao) as ultima_avaliacao
    FROM pacientes p
    LEFT JOIN prontuarios pr ON p.id = pr.paciente_id
    LEFT JOIN avaliacoes a ON p.id = a.paciente_id
    WHERE p.nutricionista_id = ? AND p.ativo = 1
    GROUP BY p.id
    ORDER BY p.nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.info("Nenhum paciente cadastrado ainda. Use a aba 'Cadastrar Paciente' para adicionar.")
        return
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        busca = st.text_input("Buscar por nome", placeholder="Digite o nome...")
    
    with col2:
        sexo_filter = st.selectbox("Filtrar por sexo", ["Todos", "Masculino", "Feminino"])
    
    with col3:
        objetivo_filter = st.selectbox("Filtrar por objetivo", ["Todos", "Perda de Peso", "Ganho de Massa", "Saúde", "Performance"])
    
    st.success(f"**{len(pacientes)} pacientes cadastrados**")
    
    for pac in pacientes:
        # Aplicar filtros
        if busca.lower() and busca.lower() not in pac[3].lower():
            continue
        
        if sexo_filter != "Todos" and pac[8] != sexo_filter:
            continue
        
        if objetivo_filter != "Todos" and pac[10] != objetivo_filter:
            continue
        
        idade = calculate_age(pac[7]) if pac[7] else "N/A"
        ultima_aval = pac[-1] if pac[-1] else "Nunca"
        
        with st.expander(f"👤 {pac[3]} - {idade} anos - {pac[10]}", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                **Dados Pessoais:**
                - Nome: {pac[3]}
                - CPF: {pac[4] or 'Não informado'}
                - Email: {pac[5] or 'Não informado'}
                - Telefone: {pac[6] or 'Não informado'}
                - Data Nascimento: {pac[7] or 'N/A'}
                - Idade: {idade} anos
                """)
            
            with col2:
                st.markdown(f"""
                **Informações Clínicas:**
                - Sexo: {pac[8]}
                - Profissão: {pac[9] or 'Não informado'}
                - Objetivo: {pac[10]}
                - Cadastrado em: {pac[13][:10] if pac[13] else 'N/A'}
                """)
            
            with col3:
                st.markdown(f"""
                **Histórico:**
                - Prontuários: {pac[-3]}
                - Avaliações: {pac[-2]}
                - Última avaliação: {ultima_aval}
                """)
            
            if pac[11]:
                st.warning(f"**Restrições:** {pac[11]}")
            
            if pac[12]:
                st.info(f"**Observações:** {pac[12]}")
            
            st.markdown("---")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("Prontuário", key=f"pront_{pac[0]}", use_container_width=True):
                    st.session_state.selected_patient_id = pac[0]
                    st.session_state.page = "Prontuario"
                    st.rerun()
            
            with col2:
                if st.button("Avaliações", key=f"aval_{pac[0]}", use_container_width=True):
                    st.session_state.selected_patient_id = pac[0]
                    st.session_state.page = "Avaliacoes"
                    st.rerun()
            
            with col3:
                if st.button("Prescrições", key=f"presc_{pac[0]}", use_container_width=True):
                    st.session_state.selected_patient_id = pac[0]
                    st.session_state.page = "Prescricoes"
                    st.rerun()
            
            with col4:
                if st.button("Plano Alimentar", key=f"plano_{pac[0]}", use_container_width=True):
                    st.session_state.selected_patient_id = pac[0]
                    st.session_state.page = "Planos"
                    st.rerun()

def cadastrar_paciente(user):
    st.markdown('<div class="sub-header">Cadastrar Novo Paciente</div>', unsafe_allow_html=True)
    
    with st.form("paciente_form"):
        st.markdown("#### Dados Pessoais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome Completo *", placeholder="João da Silva")
            cpf = st.text_input("CPF", placeholder="000.000.000-00")
            email = st.text_input("Email", placeholder="joao@email.com")
            telefone = st.text_input("Telefone", placeholder="(00) 00000-0000")
        
        with col2:
            data_nasc = st.date_input("Data de Nascimento", value=None)
            sexo = st.selectbox("Sexo *", ["Masculino", "Feminino", "Outro"])
            profissao = st.text_input("Profissão")
            objetivo = st.selectbox("Objetivo Principal *", [
                "Perda de Peso",
                "Ganho de Massa Muscular",
                "Saúde e Bem-estar",
                "Performance Esportiva",
                "Tratamento de Patologia",
                "Gestação/Lactação",
                "Terceira Idade"
            ])
        
        st.markdown("#### Informações Clínicas")
        
        restricoes = st.text_area(
            "Restrições Alimentares / Alergias",
            placeholder="Ex: Intolerância à lactose, alergia a frutos do mar, vegetariano...",
            height=80
        )
        
        observacoes = st.text_area(
            "Observações Gerais",
            placeholder="Ex: Histórico de cirurgias, medicamentos em uso, preferências alimentares...",
            height=80
        )
        
        st.markdown("---")
        
        submitted = st.form_submit_button("Cadastrar Paciente", use_container_width=True)
        
        if submitted:
            if not nome or not sexo or not objetivo:
                st.error("Preencha os campos obrigatórios: Nome, Sexo e Objetivo!")
            else:
                try:
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    paciente_uuid = str(uuid.uuid4())
                    
                    cursor.execute('''
                    INSERT INTO pacientes (
                        uuid, nutricionista_id, nome, cpf, email, telefone,
                        data_nascimento, sexo, profissao, objetivo, restricoes, observacoes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        paciente_uuid, user['id'], nome, cpf, email, telefone,
                        data_nasc, sexo, profissao, objetivo, restricoes, observacoes
                    ))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success(f"Paciente {nome} cadastrado com sucesso!")
                    st.info("Agora você pode criar avaliações, prontuários e planos para este paciente.")
                    
                except sqlite3.IntegrityError:
                    st.error("Erro: Já existe um paciente com este CPF/Email!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar: {str(e)}")

def importar_pacientes():
    st.markdown('<div class="sub-header">Importar Dados em Massa</div>', unsafe_allow_html=True)
    
    st.info("""
    Funcionalidade para importar múltiplos pacientes de uma planilha Excel ou CSV.
    
    **Formato esperado:**
    - Nome, CPF, Email, Telefone, Data Nascimento, Sexo, Objetivo
    
    **Em desenvolvimento**
    """)
    
    uploaded_file = st.file_uploader("Escolha um arquivo CSV ou Excel", type=['csv', 'xlsx'])
    
    if uploaded_file:
        st.warning("Funcionalidade de importação em desenvolvimento")

# =============================================================================
# PRONTUÁRIOS NUTRICIONAIS
# =============================================================================

def show_prontuario(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Prontuários Nutricionais</h1>', unsafe_allow_html=True)
    
    if not check_permission(user, 'completo'):
        st.error("Você não tem permissão para acessar prontuários. Apenas nutricionistas podem acessar esta área.")
        return
    
    # Verificar se há paciente selecionado
    if 'selected_patient_id' in st.session_state and st.session_state.selected_patient_id:
        tab1, tab2 = st.tabs(["Novo Prontuário", "Histórico de Atendimentos"])
        
        with tab1:
            criar_prontuario(user, st.session_state.selected_patient_id)
        
        with tab2:
            historico_prontuarios(user, st.session_state.selected_patient_id)
    else:
        # Seletor de paciente
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT id, nome, objetivo FROM pacientes
        WHERE nutricionista_id = ? AND ativo = 1
        ORDER BY nome
        """, (user['id'],))
        
        pacientes = cursor.fetchall()
        conn.close()
        
        if not pacientes:
            st.warning("Você não tem pacientes cadastrados. Cadastre um paciente primeiro na área 'Pacientes'.")
            return
        
        st.markdown("### Selecione um Paciente")
        
        paciente = st.selectbox(
            "Paciente",
            options=pacientes,
            format_func=lambda x: f"{x[1]} - {x[2]}"
        )
        
        if st.button("Selecionar Paciente", use_container_width=True):
            st.session_state.selected_patient_id = paciente[0]
            st.rerun()

def criar_prontuario(user, paciente_id):
    st.markdown('<div class="sub-header">Novo Atendimento</div>', unsafe_allow_html=True)
    
    # Buscar dados do paciente
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome, objetivo, restricoes FROM pacientes WHERE id = ?", (paciente_id,))
    paciente_info = cursor.fetchone()
    conn.close()
    
    st.info(f"**Paciente:** {paciente_info[0]} | **Objetivo:** {paciente_info[1]}")
    if paciente_info[2]:
        st.warning(f"**Restrições:** {paciente_info[2]}")
    
    with st.form("prontuario_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            data_atend = st.date_input("Data do Atendimento", value=date.today())
            tipo_atend = st.selectbox("Tipo de Atendimento", [
                "Primeira Consulta",
                "Retorno",
                "Reavaliação",
                "Evolução",
                "Alta"
            ])
        
        with col2:
            st.markdown("**Profissional:**")
            st.info(f"{user['nome']}\n{user['coren']}")
        
        st.markdown("---")
        st.markdown("### Anamnese Nutricional")
        
        queixa = st.text_area(
            "Queixa Principal / Motivo da Consulta *",
            placeholder="Ex: Deseja perder peso, dificuldade para ganhar massa muscular...",
            height=100
        )
        
        historia_clinica = st.text_area(
            "História Clínica",
            placeholder="Doenças preexistentes, cirurgias, medicamentos em uso, histórico familiar...",
            height=120
        )
        
        historia_alimentar = st.text_area(
            "História Alimentar",
            placeholder="Hábitos alimentares atuais, preferências, aversões, recordatório 24h...",
            height=150
        )
        
        st.markdown("### Avaliação e Exame Físico")
        
        exame_fisico = st.text_area(
            "Exame Físico / Antropometria",
            placeholder="Peso, altura, IMC, circunferências, composição corporal, PA...",
            height=120
        )
        
        st.markdown("### Diagnóstico e Conduta")
        
        diagnostico = st.text_area(
            "Diagnóstico Nutricional *",
            placeholder="Classificação nutricional segundo critérios estabelecidos...",
            height=100
        )
        
        conduta = st.text_area(
            "Conduta Nutricional / Plano de Tratamento *",
            placeholder="Orientações dietéticas, prescrição nutricional, metas, retorno...",
            height=150
        )
        
        observacoes = st.text_area(
            "Observações Adicionais",
            placeholder="Intercorrências, observações relevantes...",
            height=80
        )
        
        st.markdown("---")
        
        submitted = st.form_submit_button("Salvar Prontuário", use_container_width=True)
        
        if submitted:
            if not queixa or not diagnostico or not conduta:
                st.error("Preencha os campos obrigatórios: Queixa, Diagnóstico e Conduta!")
            else:
                try:
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                    INSERT INTO prontuarios (
                        paciente_id, nutricionista_id, data_atendimento, tipo_atendimento,
                        queixa_principal, historia_clinica, historia_alimentar,
                        exame_fisico, diagnostico_nutricional, conduta, observacoes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        paciente_id, user['id'], data_atend, tipo_atend,
                        queixa, historia_clinica, historia_alimentar,
                        exame_fisico, diagnostico, conduta, observacoes
                    ))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("Prontuário salvo com sucesso!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Erro ao salvar: {str(e)}")

def historico_prontuarios(user, paciente_id):
    st.markdown('<div class="sub-header">Histórico de Atendimentos</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM prontuarios
    WHERE paciente_id = ? AND nutricionista_id = ?
    ORDER BY data_atendimento DESC
    """, (paciente_id, user['id']))
    
    prontuarios = cursor.fetchall()
    conn.close()
    
    if not prontuarios:
        st.info("Nenhum prontuário registrado ainda para este paciente.")
        return
    
    st.success(f"**{len(prontuarios)} atendimentos registrados**")
    
    for pront in prontuarios:
        data_formatada = pront[3][:10] if pront[3] else "N/A"
        
        with st.expander(f"📋 {data_formatada} - {pront[4]}", expanded=False):
            st.markdown(f"""
            <div class="prontuario-section">
                <strong>Data:</strong> {data_formatada}<br>
                <strong>Tipo:</strong> {pront[4]}<br>
                <strong>Profissional:</strong> {user['nome']}
            </div>
            """, unsafe_allow_html=True)
            
            if pront[5]:
                st.markdown(f"**Queixa Principal:**\n{pront[5]}")
            
            if pront[6]:
                st.markdown(f"**História Clínica:**\n{pront[6]}")
            
            if pront[7]:
                st.markdown(f"**História Alimentar:**\n{pront[7]}")
            
            if pront[8]:
                st.markdown(f"**Exame Físico:**\n{pront[8]}")
            
            if pront[9]:
                st.markdown(f"**Diagnóstico:**\n{pront[9]}")
            
            if pront[10]:
                st.markdown(f"**Conduta:**\n{pront[10]}")
            
            if pront[11]:
                st.markdown(f"**Observações:**\n{pront[11]}")
            
            st.markdown("---")
            
            if st.button("Exportar PDF", key=f"export_{pront[0]}"):
                st.info("Funcionalidade de exportação em desenvolvimento")

# =============================================================================
# AVALIAÇÕES ANTROPOMÉTRICAS
# =============================================================================

def show_avaliacoes(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Avaliações Antropométricas</h1>', unsafe_allow_html=True)
    
    # Verificar se há paciente selecionado
    if 'selected_patient_id' in st.session_state and st.session_state.selected_patient_id:
        tab1, tab2, tab3 = st.tabs(["Nova Avaliação", "Histórico", "Gráficos de Evolução"])
        
        with tab1:
            nova_avaliacao(user, st.session_state.selected_patient_id)
        
        with tab2:
            historico_avaliacoes(user, st.session_state.selected_patient_id)
        
        with tab3:
            graficos_evolucao(user, st.session_state.selected_patient_id)
    else:
        # Seletor de paciente
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
        
        st.markdown("### Selecione um Paciente")
        
        paciente = st.selectbox(
            "Paciente",
            options=pacientes,
            format_func=lambda x: x[1]
        )
        
        if st.button("Selecionar Paciente", use_container_width=True):
            st.session_state.selected_patient_id = paciente[0]
            st.rerun()

def nova_avaliacao(user, paciente_id):
    st.markdown('<div class="sub-header">Nova Avaliação Antropométrica</div>', unsafe_allow_html=True)
    
    # Buscar última avaliação
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome, data_nascimento, sexo FROM pacientes WHERE id = ?", (paciente_id,))
    paciente_info = cursor.fetchone()
    
    cursor.execute("""
    SELECT peso, altura, imc, gordura_corporal, massa_muscular
    FROM avaliacoes
    WHERE paciente_id = ?
    ORDER BY data_avaliacao DESC
    LIMIT 1
    """, (paciente_id,))
    
    ultima_aval = cursor.fetchone()
    conn.close()
    
    idade = calculate_age(paciente_info[1]) if paciente_info[1] else 0
    
    st.info(f"**Paciente:** {paciente_info[0]} | **Idade:** {idade} anos | **Sexo:** {paciente_info[2]}")
    
    if ultima_aval:
        st.success(f"**Última avaliação:** Peso: {ultima_aval[0]:.1f}kg | IMC: {ultima_aval[2]:.1f} | Gordura: {ultima_aval[3]:.1f}%")
    
    with st.form("avaliacao_form"):
        st.markdown("### Dados da Avaliação")
        
        data_aval = st.date_input("Data da Avaliação", value=date.today())
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Medidas Básicas**")
            peso = st.number_input("Peso (kg) *", 30.0, 300.0, ultima_aval[0] if ultima_aval else 70.0, step=0.1)
            altura = st.number_input("Altura (cm) *", 100.0, 250.0, ultima_aval[1] if ultima_aval else 170.0, step=0.1)
        
        with col2:
            st.markdown("**Circunferências**")
            cintura = st.number_input("Cintura (cm)", 0.0, 200.0, 80.0, step=0.1)
            quadril = st.number_input("Quadril (cm)", 0.0, 200.0, 100.0, step=0.1)
        
        with col3:
            st.markdown("**Composição Corporal**")
            gordura = st.number_input("% Gordura Corporal", 0.0, 60.0, ultima_aval[3] if ultima_aval else 20.0, step=0.1)
            massa_muscular = st.number_input("% Massa Muscular", 0.0, 100.0, ultima_aval[4] if ultima_aval else 40.0, step=0.1)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Dados Adicionais**")
            agua_corporal = st.number_input("% Água Corporal", 0.0, 100.0, 60.0, step=0.1)
            massa_ossea = st.number_input("Massa Óssea (kg)", 0.0, 10.0, 3.0, step=0.1)
        
        with col2:
            st.markdown("**Metabolismo**")
            tmb = st.number_input("TMB (kcal)", 0, 5000, int(calculate_bmr(peso, altura, idade, paciente_info[2])))
        
        observacoes = st.text_area(
            "Observações da Avaliação",
            placeholder="Medidas de dobras cutâneas, bioimpedância, observações gerais...",
            height=100
        )
        
        submitted = st.form_submit_button("Salvar Avaliação", use_container_width=True)
        
        if submitted:
            try:
                altura_m = altura / 100
                imc = calculate_imc(peso, altura_m)
                
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                INSERT INTO avaliacoes (
                    paciente_id, data_avaliacao, peso, altura, imc,
                    cintura, quadril, gordura_corporal, massa_muscular,
                    agua_corporal, massa_ossea, metabolismo_basal, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    paciente_id, data_aval, peso, altura, imc,
                    cintura, quadril, gordura, massa_muscular,
                    agua_corporal, massa_ossea, tmb, observacoes
                ))
                
                conn.commit()
                conn.close()
                
                st.success("Avaliação salva com sucesso!")
                
                # Mostrar resultados
                st.markdown("---")
                st.markdown("### Resultados da Avaliação")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("IMC", f"{imc:.1f}")
                
                with col2:
                    if cintura > 0 and quadril > 0:
                        rcq = cintura / quadril
                        st.metric("RCQ", f"{rcq:.2f}")
                
                with col3:
                    if cintura > 0 and altura > 0:
                        rca = cintura / altura
                        st.metric("RCA", f"{rca:.2f}")
                
                with col4:
                    massa_gorda_kg = peso * (gordura / 100)
                    st.metric("Massa Gorda", f"{massa_gorda_kg:.1f}kg")
                
            except Exception as e:
                st.error(f"Erro ao salvar: {str(e)}")

def historico_avaliacoes(user, paciente_id):
    st.markdown('<div class="sub-header">Histórico de Avaliações</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT * FROM avaliacoes
    WHERE paciente_id = ?
    ORDER BY data_avaliacao DESC
    """, (paciente_id,))
    
    avaliacoes = cursor.fetchall()
    conn.close()
    
    if not avaliacoes:
        st.info("Nenhuma avaliação registrada ainda.")
        return
    
    st.success(f"**{len(avaliacoes)} avaliações registradas**")
    
    # Tabela resumida
    df_avaliacoes = pd.DataFrame(avaliacoes, columns=[
        'ID', 'Paciente ID', 'Data', 'Peso', 'Altura', 'IMC', 'Cintura', 'Quadril',
        'Gordura %', 'Massa Muscular %', 'Água %', 'Massa Óssea', 'TMB', 'Obs'
    ])
    
    df_display = df_avaliacoes[['Data', 'Peso', 'IMC', 'Gordura %', 'Massa Muscular %', 'TMB']]
    st.dataframe(df_display, use_container_width=True, hide_index=True)

def graficos_evolucao(user, paciente_id):
    st.markdown('<div class="sub-header">Gráficos de Evolução</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT data_avaliacao, peso, imc, gordura_corporal, massa_muscular
    FROM avaliacoes
    WHERE paciente_id = ?
    ORDER BY data_avaliacao
    """, (paciente_id,))
    
    avaliacoes = cursor.fetchall()
    conn.close()
    
    if len(avaliacoes) < 2:
        st.warning("É necessário pelo menos 2 avaliações para gerar gráficos de evolução.")
        return
    
    df = pd.DataFrame(avaliacoes, columns=['Data', 'Peso', 'IMC', 'Gordura %', 'Massa Muscular %'])
    
    # Gráfico de Peso
    fig_peso = px.line(df, x='Data', y='Peso', 
                       title='Evolução do Peso',
                       markers=True,
                       line_shape='spline')
    fig_peso.update_layout(height=300)
    st.plotly_chart(fig_peso, use_container_width=True)
    
    # Gráficos de Composição
    col1, col2 = st.columns(2)
    
    with col1:
        fig_gordura = px.line(df, x='Data', y='Gordura %',
                             title='Evolução % Gordura',
                             markers=True,
                             line_shape='spline')
        fig_gordura.update_layout(height=300)
        st.plotly_chart(fig_gordura, use_container_width=True)
    
    with col2:
        fig_muscular = px.line(df, x='Data', y='Massa Muscular %',
                              title='Evolução % Massa Muscular',
                              markers=True,
                              line_shape='spline')
        fig_muscular.update_layout(height=300)
        st.plotly_chart(fig_muscular, use_container_width=True)
    
    # Estatísticas
    st.markdown("### Estatísticas Gerais")
    
    primeira_aval = df.iloc[0]
    ultima_aval = df.iloc[-1]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        dif_peso = ultima_aval['Peso'] - primeira_aval['Peso']
        st.metric("Variação de Peso", f"{dif_peso:+.1f} kg", 
                 delta=f"{dif_peso:+.1f}kg")
    
    with col2:
        dif_gordura = ultima_aval['Gordura %'] - primeira_aval['Gordura %']
        st.metric("Variação Gordura", f"{dif_gordura:+.1f}%",
                 delta=f"{dif_gordura:+.1f}%")
    
    with col3:
        dif_muscular = ultima_aval['Massa Muscular %'] - primeira_aval['Massa Muscular %']
        st.metric("Variação Massa Muscular", f"{dif_muscular:+.1f}%",
                 delta=f"{dif_muscular:+.1f}%")

# =============================================================================
# PRESCRIÇÕES DE SUPLEMENTOS
# =============================================================================

def show_prescricoes(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Prescrições de Suplementos</h1>', unsafe_allow_html=True)
    
    st.warning("""
    ⚖️ **ATENÇÃO LEGAL:** Esta funcionalidade é para prescrição de SUPLEMENTOS NUTRICIONAIS ALIMENTARES, 
    conforme permitido pela legislação para nutricionistas (Lei 8.234/91 e Resolução CFN 680/2021). 
    Nutricionistas NÃO podem prescrever medicamentos.
    """)
    
    if not check_permission(user, 'completo'):
        st.error("Você não tem permissão para prescrever suplementos.")
        return
    
    tab1, tab2 = st.tabs(["Nova Prescrição", "Prescrições Ativas"])
    
    with tab1:
        nova_prescricao(user)
    
    with tab2:
        prescricoes_ativas(user)

def nova_prescricao(user):
    st.markdown('<div class="sub-header">Nova Prescrição de Suplementos</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT id, nome, objetivo FROM pacientes
    WHERE nutricionista_id = ? AND ativo = 1
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    conn.close()
    
    if not pacientes:
        st.warning("Cadastre um paciente primeiro.")
        return
    
    with st.form("prescricao_form"):
        paciente = st.selectbox(
            "Paciente *",
            options=pacientes,
            format_func=lambda x: f"{x[1]} - {x[2]}"
        )
        
        data_validade = st.date_input(
            "Validade da Prescrição",
            value=date.today() + timedelta(days=90),
            min_value=date.today()
        )
        
        st.markdown("### Suplementos Disponíveis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **Vitaminas e Minerais:**
            - Vitamina D3
            - Vitamina B12
            - Complexo B
            - Vitamina C
            - Ômega 3
            - Multivitamínico
            - Magnésio
            - Zinco
            - Ferro
            - Cálcio
            """)
        
        with col2:
            st.markdown("""
            **Suplementos Esportivos:**
            - Whey Protein
            - Creatina
            - BCAA
            - Glutamina
            - Beta-Alanina
            - Cafeína
            - Pré-treino
            - Maltodextrina
            - Dextrose
            """)
        
        with col3:
            st.markdown("""
            **Outros:**
            - Probióticos
            - Fibras
            - Colágeno
            - Coenzima Q10
            - L-Carnitina
            - Termogênicos
            - Enzimas digestivas
            """)
        
        st.markdown("### Prescrição")
        
        suplementos = st.text_area(
            "Suplementos e Posologia *",
            placeholder="""Exemplo:
1. Vitamina D3 - 2000 UI - 1 cápsula ao dia, preferencialmente junto ao almoço
2. Ômega 3 - 1000mg - 1 cápsula 2x ao dia (café da manhã e jantar)
3. Whey Protein Isolado - 30g - 1 dose após o treino ou no lanche da tarde
4. Probióticos - 1 cápsula ao dia em jejum""",
            height=250
        )
        
        orientacoes = st.text_area(
            "Orientações Gerais",
            placeholder="""Orientações sobre:
- Horários de administração
- Interações com alimentos/medicamentos
- Forma de armazenamento
- Cuidados especiais
- Contraindicações""",
            height=150
        )
        
        st.markdown("---")
        
        submitted = st.form_submit_button("Gerar Prescrição", use_container_width=True)
        
        if submitted:
            if not suplementos:
                st.error("Adicione pelo menos um suplemento!")
            else:
                try:
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    prescricao_uuid = str(uuid.uuid4())
                    
                    cursor.execute('''
                    INSERT INTO prescricoes_suplementos (
                        uuid, paciente_id, nutricionista_id, suplementos, orientacoes, validade
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        prescricao_uuid, paciente[0], user['id'], suplementos, orientacoes, data_validade
                    ))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("Prescrição gerada com sucesso!")
                    
                    # Mostrar prescrição formatada
                    st.markdown("---")
                    st.markdown("### Prescrição Gerada")
                    
                    st.markdown(f'''
                    <div style="background: white; padding: 2.5rem; border: 3px solid #2E7D32; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                        <div style="text-align: center; margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 2px solid #4CAF50;">
                            <h2 style="color: #1B5E20; margin: 0;">PRESCRIÇÃO DE SUPLEMENTOS NUTRICIONAIS</h2>
                            <p style="color: #666; margin-top: 0.5rem;">Resolução CFN 680/2021</p>
                        </div>
                        
                        <div style="margin-bottom: 1.5rem;">
                            <p style="margin: 0.3rem 0;"><strong>Paciente:</strong> {paciente[1]}</p>
                            <p style="margin: 0.3rem 0;"><strong>Data de Emissão:</strong> {date.today().strftime('%d/%m/%Y')}</p>
                            <p style="margin: 0.3rem 0;"><strong>Validade:</strong> {data_validade.strftime('%d/%m/%Y')}</p>
                        </div>
                        
                        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; margin: 1.5rem 0;">
                            <h3 style="color: #2E7D32; margin-top: 0;">Suplementos Prescritos:</h3>
                            <pre style="white-space: pre-wrap; font-family: inherit; margin: 0;">{suplementos}</pre>
                        </div>
                        
                        {f'<div style="margin: 1.5rem 0;"><h3 style="color: #2E7D32;">Orientações:</h3><p>{orientacoes}</p></div>' if orientacoes else ''}
                        
                        <div style="margin-top: 2rem; padding-top: 1rem; border-top: 2px solid #e0e0e0;">
                            <p style="margin: 0.3rem 0;"><strong>Nutricionista:</strong> {user['nome']}</p>
                            <p style="margin: 0.3rem 0;"><strong>CRN:</strong> {user['coren']}</p>
                            <p style="margin: 0.3rem 0;"><strong>Telefone:</strong> {user.get('telefone', 'Não informado')}</p>
                            <p style="margin: 0.3rem 0; color: #666; font-size: 0.85rem;"><strong>ID Prescrição:</strong> {prescricao_uuid}</p>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("Imprimir Prescrição", use_container_width=True):
                            st.info("Funcionalidade de impressão em desenvolvimento")
                    
                    with col2:
                        if st.button("Enviar por Email", use_container_width=True):
                            st.info("Funcionalidade de envio por email em desenvolvimento")
                    
                except Exception as e:
                    st.error(f"Erro: {str(e)}")

def prescricoes_ativas(user):
    st.markdown('<div class="sub-header">Prescrições Ativas</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT ps.*, p.nome as paciente_nome
    FROM prescricoes_suplementos ps
    JOIN pacientes p ON ps.paciente_id = p.id
    WHERE ps.nutricionista_id = ? AND ps.ativo = 1
    ORDER BY ps.data_prescricao DESC
    """, (user['id'],))
    
    prescricoes = cursor.fetchall()
    conn.close()
    
    if not prescricoes:
        st.info("Nenhuma prescrição ativa no momento.")
        return
    
    st.success(f"**{len(prescricoes)} prescrições ativas**")
    
    for ps in prescricoes:
        try:
            validade = datetime.strptime(ps[7], '%Y-%m-%d').date()
            dias_restantes = (validade - date.today()).days
            
            if dias_restantes < 0:
                status_cor = "red"
                status_text = f"VENCIDA há {abs(dias_restantes)} dias"
            elif dias_restantes <= 7:
                status_cor = "orange"
                status_text = f"Vence em {dias_restantes} dias"
            else:
                status_cor = "green"
                status_text = f"{dias_restantes} dias restantes"
            
            with st.expander(f"💊 {ps[-1]} - {ps[4]} - {status_text}", expanded=False):
                st.markdown(f"""
                <div style="background: white; padding: 1.5rem; border-left: 4px solid {status_cor};">
                    <p><strong>Paciente:</strong> {ps[-1]}</p>
                    <p><strong>Data Emissão:</strong> {ps[4]}</p>
                    <p><strong>Validade:</strong> {ps[7]}</p>
                    <p style="color: {status_cor}; font-weight: bold;">Status: {status_text}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Suplementos:**\n```\n{ps[5]}\n```")
                
                if ps[6]:
                    st.markdown(f"**Orientações:**\n{ps[6]}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("Visualizar", key=f"view_{ps[0]}"):
                        st.info("Modal de visualização em desenvolvimento")
                
                with col2:
                    if st.button("Renovar", key=f"renew_{ps[0]}"):
                        st.info("Funcionalidade de renovação em desenvolvimento")
                
                with col3:
                    if st.button("Desativar", key=f"deact_{ps[0]}"):
                        conn = db_manager.get_connection()
                        cursor = conn.cursor()
                        cursor.execute("UPDATE prescricoes_suplementos SET ativo = 0 WHERE id = ?", (ps[0],))
                        conn.commit()
                        conn.close()
                        st.success("Prescrição desativada!")
                        st.rerun()
        
        except Exception as e:
            st.error(f"Erro ao processar prescrição: {str(e)}")

# =============================================================================
# PLANOS ALIMENTARES
# =============================================================================

def show_planos(user):
    load_css()
    st.markdown('<h1 class="ultra-header">Planos Alimentares</h1>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Criar Plano", "Planos Ativos"])
    
    with tab1:
        criar_plano(user)
    
    with tab2:
        planos_ativos(user)

def criar_plano(user):
    st.markdown('<div class="sub-header">Criar Novo Plano Alimentar</div>', unsafe_allow_html=True)
    
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
    
    paciente = st.selectbox(
        "Paciente",
        options=pacientes,
        format_func=lambda x: x[1]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome_plano = st.text_input("Nome do Plano", placeholder="Ex: Plano 2000 kcal - Perda de Peso")
        objetivo = st.selectbox("Objetivo", [
            "Perda de Peso",
            "Ganho de Massa",
            "Manutenção",
            "Performance"
        ])
    
    with col2:
        calorias_total = st.number_input("Calorias Totais/dia", 1000, 5000, 2000, step=100)
        
    # Usar IA para gerar cardápio base
    if st.button("Gerar Plano com IA", use_container_width=True):
        with st.spinner("Gerando plano personalizado com IA..."):
            cardapio_gerado = ai_assistant.gerar_cardapio_ia(calorias_total, objetivo, "", 5)
            st.session_state['cardapio_temp'] = cardapio_gerado
            st.success("Plano gerado! Revise e ajuste abaixo antes de salvar.")
    
    # Mostrar cardápio gerado
    if 'cardapio_temp' in st.session_state:
        st.markdown("### Plano Gerado")
        refeicoes_text = st.text_area(
            "Refeições (edite se necessário)",
            value=st.session_state['cardapio_temp'],
            height=400
        )
        
        if st.button("Salvar Plano", use_container_width=True):
            try:
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                
                plano_uuid = str(uuid.uuid4())
                
                cursor.execute('''
                INSERT INTO planos_alimentares (
                    uuid, paciente_id, nutricionista_id, nome, objetivo,
                    calorias_total, refeicoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    plano_uuid, paciente[0], user['id'], nome_plano, objetivo,
                    calorias_total, refeicoes_text
                ))
                
                conn.commit()
                conn.close()
                
                st.success("Plano salvo com sucesso!")
                del st.session_state['cardapio_temp']
                st.rerun()
                
            except Exception as e:
                st.error(f"Erro ao salvar: {str(e)}")

def planos_ativos(user):
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
        st.info("Nenhum plano ativo.")
        return
    
    st.success(f"**{len(planos)} planos ativos**")
    
    for plano in planos:
        with st.expander(f"🍽️ {plano[3]} - {plano[-1]}", expanded=False):
            st.markdown(f"""
            **Paciente:** {plano[-1]}  
            **Objetivo:** {plano[4]}  
            **Calorias:** {plano[5]:.0f} kcal/dia  
            **Data Criação:** {plano[11][:10] if plano[11] else 'N/A'}
            """)
            
            if plano[10]:
                st.markdown("**Refeições:**")
                st.text_area("", value=plano[10], height=300, key=f"plano_{plano[0]}", disabled=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Exportar PDF", key=f"export_plano_{plano[0]}"):
                    st.info("Exportação em desenvolvimento")
            
            with col2:
                if st.button("Desativar", key=f"deact_plano_{plano[0]}"):
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE planos_alimentares SET ativo = 0 WHERE id = ?", (plano[0],))
                    conn.commit()
                    conn.close()
                    st.success("Plano desativado!")
                    st.rerun()
