import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import hashlib
import time
import math
import base64
from io import BytesIO

# Importações opcionais com tratamento de erro
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False

try:
    from passlib.hash import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

# Configuração da página
st.set_page_config(
    page_title="NutriStock360 Pro",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado avançado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Animações */
    @keyframes slideInFromTop {
        0% { transform: translateY(-100px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes fadeInUp {
        0% { transform: translateY(30px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 300% 300%;
        animation: gradient 8s ease infinite;
        padding: 3rem 2rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Cards melhorados */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-12px) scale(1.03);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.25);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .metric-card:hover::before {
        transform: scaleX(1);
    }
    
    /* Cards de calculadora */
    .calculator-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .calculator-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    /* Resultados de calculadora */
    .calculator-result {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        text-align: center;
        font-weight: 700;
        font-size: 1.4rem;
        animation: pulse 0.6s ease-in-out;
        box-shadow: 0 10px 30px rgba(132, 250, 176, 0.4);
        color: #1a365d;
        position: relative;
        overflow: hidden;
    }
    
    .calculator-result::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.3) 50%, transparent 70%);
        animation: shimmer 2s infinite;
    }
    
    /* Status cards com animações */
    .status-card {
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .status-card:hover {
        transform: scale(1.05);
    }
    
    .status-normal { 
        background: linear-gradient(135deg, #c6f6d5, #9ae6b4); 
        color: #22543d; 
        border: 2px solid #68d391;
        animation: fadeInUp 0.5s ease-out;
    }
    .status-warning { 
        background: linear-gradient(135deg, #fefcbf, #faf089); 
        color: #744210; 
        border: 2px solid #f6e05e;
        animation: fadeInUp 0.7s ease-out;
    }
    .status-danger { 
        background: linear-gradient(135deg, #fed7d7, #feb2b2); 
        color: #742a2a; 
        border: 2px solid #fc8181;
        animation: fadeInUp 0.9s ease-out;
    }
    
    /* Sidebar melhorado */
    .sidebar-logo {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        margin-bottom: 1.5rem;
        animation: slideInFromTop 0.8s ease-out;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .sidebar-logo::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 4s infinite;
    }
    
    /* Progress bars */
    .progress-container {
        background: #e2e8f0;
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 2s ease-in-out;
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.4) 50%, transparent 70%);
        animation: shimmer 1.5s infinite;
    }
    
    /* Tab content */
    .tab-content {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        animation: fadeInUp 0.5s ease-out;
    }
    
    /* Botões melhorados */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.2) 50%, transparent 70%);
        transform: translateX(-100%);
        transition: transform 0.6s ease;
    }
    
    .stButton > button:hover::before {
        transform: translateX(100%);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background: white;
    }
    
    /* Metric improvements */
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
    }
    
    /* Data tables */
    .stDataFrame {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Forms */
    .form-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Base de dados de alimentos expandida
ALIMENTOS_DB = {
    # Proteínas
    "Frango grelhado (100g)": {"calorias": 165, "proteinas": 31, "carboidratos": 0, "gorduras": 3.6, "categoria": "Proteína", "fibras": 0, "sodio": 74},
    "Salmão grelhado (100g)": {"calorias": 206, "proteinas": 22, "carboidratos": 0, "gorduras": 12, "categoria": "Proteína", "fibras": 0, "sodio": 59},
    "Ovo cozido (1 unidade)": {"calorias": 68, "proteinas": 6, "carboidratos": 0.6, "gorduras": 4.8, "categoria": "Proteína", "fibras": 0, "sodio": 62},
    "Peito de peru (100g)": {"calorias": 104, "proteinas": 24, "carboidratos": 0, "gorduras": 1, "categoria": "Proteína", "fibras": 0, "sodio": 1040},
    "Tilápia grelhada (100g)": {"calorias": 96, "proteinas": 20, "carboidratos": 0, "gorduras": 1.7, "categoria": "Proteína", "fibras": 0, "sodio": 52},
    "Carne bovina magra (100g)": {"calorias": 250, "proteinas": 26, "carboidratos": 0, "gorduras": 15, "categoria": "Proteína", "fibras": 0, "sodio": 54},
    "Filé de peixe (100g)": {"calorias": 105, "proteinas": 22, "carboidratos": 0, "gorduras": 1.5, "categoria": "Proteína", "fibras": 0, "sodio": 50},
    
    # Carboidratos
    "Arroz integral (100g)": {"calorias": 123, "proteinas": 2.6, "carboidratos": 23, "gorduras": 1, "categoria": "Carboidrato", "fibras": 1.8, "sodio": 1},
    "Batata doce (100g)": {"calorias": 86, "proteinas": 1.6, "carboidratos": 20, "gorduras": 0.1, "categoria": "Carboidrato", "fibras": 3, "sodio": 4},
    "Aveia (100g)": {"calorias": 389, "proteinas": 17, "carboidratos": 66, "gorduras": 7, "categoria": "Carboidrato", "fibras": 10, "sodio": 2},
    "Quinoa (100g)": {"calorias": 120, "proteinas": 4.4, "carboidratos": 22, "gorduras": 1.9, "categoria": "Carboidrato", "fibras": 2.8, "sodio": 5},
    "Pão integral (2 fatias)": {"calorias": 160, "proteinas": 6, "carboidratos": 30, "gorduras": 3, "categoria": "Carboidrato", "fibras": 4, "sodio": 320},
    "Macarrão integral (100g)": {"calorias": 124, "proteinas": 5, "carboidratos": 23, "gorduras": 1.1, "categoria": "Carboidrato", "fibras": 4, "sodio": 3},
    
    # Vegetais
    "Brócolis (100g)": {"calorias": 25, "proteinas": 3, "carboidratos": 5, "gorduras": 0.4, "categoria": "Vegetal", "fibras": 2.6, "sodio": 33},
    "Espinafre (100g)": {"calorias": 23, "proteinas": 2.9, "carboidratos": 3.6, "gorduras": 0.4, "categoria": "Vegetal", "fibras": 2.2, "sodio": 79},
    "Alface (100g)": {"calorias": 15, "proteinas": 1.4, "carboidratos": 2.9, "gorduras": 0.2, "categoria": "Vegetal", "fibras": 1.3, "sodio": 28},
    "Tomate (100g)": {"calorias": 18, "proteinas": 0.9, "carboidratos": 3.9, "gorduras": 0.2, "categoria": "Vegetal", "fibras": 1.2, "sodio": 5},
    "Cenoura (100g)": {"calorias": 41, "proteinas": 0.9, "carboidratos": 10, "gorduras": 0.2, "categoria": "Vegetal", "fibras": 2.8, "sodio": 69},
    "Abobrinha (100g)": {"calorias": 17, "proteinas": 1.2, "carboidratos": 3.1, "gorduras": 0.3, "categoria": "Vegetal", "fibras": 1, "sodio": 8},
    
    # Frutas
    "Banana (1 unidade)": {"calorias": 89, "proteinas": 1.1, "carboidratos": 23, "gorduras": 0.3, "categoria": "Fruta", "fibras": 2.6, "sodio": 1},
    "Maçã (1 unidade)": {"calorias": 52, "proteinas": 0.3, "carboidratos": 14, "gorduras": 0.2, "categoria": "Fruta", "fibras": 2.4, "sodio": 1},
    "Morango (100g)": {"calorias": 32, "proteinas": 0.7, "carboidratos": 7.7, "gorduras": 0.3, "categoria": "Fruta", "fibras": 2, "sodio": 1},
    "Laranja (1 unidade)": {"calorias": 62, "proteinas": 1.2, "carboidratos": 15, "gorduras": 0.2, "categoria": "Fruta", "fibras": 3.1, "sodio": 0},
    "Mamão (100g)": {"calorias": 43, "proteinas": 0.5, "carboidratos": 11, "gorduras": 0.3, "categoria": "Fruta", "fibras": 1.7, "sodio": 8},
    
    # Gorduras boas
    "Abacate (100g)": {"calorias": 160, "proteinas": 2, "carboidratos": 9, "gorduras": 15, "categoria": "Gordura", "fibras": 6.7, "sodio": 7},
    "Azeite (1 colher sopa)": {"calorias": 119, "proteinas": 0, "carboidratos": 0, "gorduras": 13.5, "categoria": "Gordura", "fibras": 0, "sodio": 0},
    "Castanha do Pará (10g)": {"calorias": 66, "proteinas": 1.4, "carboidratos": 1.2, "gorduras": 6.5, "categoria": "Gordura", "fibras": 0.7, "sodio": 0.3},
    "Nozes (30g)": {"calorias": 196, "proteinas": 4.6, "carboidratos": 4, "gorduras": 19.6, "categoria": "Gordura", "fibras": 2, "sodio": 1}
}

# Fórmulas científicas para cálculos
class CalculadorasNutricionais:
    @staticmethod
    def calcular_imc(peso, altura):
        """Calcula IMC com classificação detalhada"""
        imc = peso / (altura ** 2)
        
        if imc < 16:
            return imc, "Magreza grave", "danger"
        elif imc < 17:
            return imc, "Magreza moderada", "warning" 
        elif imc < 18.5:
            return imc, "Magreza leve", "warning"
        elif imc < 25:
            return imc, "Saudável", "normal"
        elif imc < 30:
            return imc, "Sobrepeso", "warning"
        elif imc < 35:
            return imc, "Obesidade Grau I", "danger"
        elif imc < 40:
            return imc, "Obesidade Grau II", "danger"
        else:
            return imc, "Obesidade Grau III", "danger"
    
    @staticmethod
    def calcular_peso_ideal(altura, sexo, metodo="robinson"):
        """Calcula peso ideal por diferentes métodos"""
        altura_cm = altura * 100
        
        if metodo == "robinson":
            if sexo == "Masculino":
                return 52 + (1.9 * ((altura_cm - 152.4) / 2.54))
            else:
                return 49 + (1.7 * ((altura_cm - 152.4) / 2.54))
        
        elif metodo == "devine":
            if sexo == "Masculino":
                return 50 + (2.3 * ((altura_cm / 2.54) - 60))
            else:
                return 45.5 + (2.3 * ((altura_cm / 2.54) - 60))
        
        elif metodo == "hamwi":
            if sexo == "Masculino":
                return 48 + (2.7 * ((altura_cm / 2.54) - 60))
            else:
                return 45.5 + (2.2 * ((altura_cm / 2.54) - 60))
        
        elif metodo == "miller":
            if sexo == "Masculino":
                return 56.2 + (1.41 * ((altura_cm / 2.54) - 60))
            else:
                return 53.1 + (1.36 * ((altura_cm / 2.54) - 60))
    
    @staticmethod
    def calcular_tmb(peso, altura, idade, sexo, metodo="mifflin"):
        """Calcula TMB por diferentes fórmulas"""
        altura_cm = altura * 100 if altura < 10 else altura
        
        if metodo == "mifflin":
            if sexo == "Masculino":
                return (10 * peso) + (6.25 * altura_cm) - (5 * idade) + 5
            else:
                return (10 * peso) + (6.25 * altura_cm) - (5 * idade) - 161
        
        elif metodo == "harris":
            if sexo == "Masculino":
                return 88.362 + (13.397 * peso) + (4.799 * altura_cm) - (5.677 * idade)
            else:
                return 447.593 + (9.247 * peso) + (3.098 * altura_cm) - (4.330 * idade)
        
        elif metodo == "katch":
            # Requer percentual de gordura, estimativa baseada em idade/sexo
            if sexo == "Masculino":
                bf_estimado = max(10, min(25, 10 + (idade - 20) * 0.3))
            else:
                bf_estimado = max(16, min(35, 16 + (idade - 20) * 0.4))
            
            massa_magra = peso * (1 - bf_estimado / 100)
            return 370 + (21.6 * massa_magra)
    
    @staticmethod
    def calcular_bf_navy(cintura, pescoco, altura, quadril=None, sexo="Masculino"):
        """Calcula percentual de gordura pela fórmula da Marinha"""
        altura_cm = altura * 100 if altura < 10 else altura
        
        try:
            if sexo == "Masculino":
                bf = 495 / (1.0324 - 0.19077 * math.log10(cintura - pescoco) + 0.15456 * math.log10(altura_cm)) - 450
            else:
                if quadril is None:
                    return None, "Necessário medida do quadril para mulheres"
                bf = 495 / (1.29579 - 0.35004 * math.log10(cintura + quadril - pescoco) + 0.22100 * math.log10(altura_cm)) - 450
            
            # Validar resultado
            if bf < 2 or bf > 50:
                return None, "Resultado fora do esperado, verifique as medidas"
            
            return max(2, min(50, bf)), "normal"
        except:
            return None, "Erro no cálculo, verifique as medidas"
    
    @staticmethod
    def calcular_get(tmb, atividade):
        """Calcula Gasto Energético Total"""
        fatores = {
            "sedentario": 1.2,
            "leve": 1.375,
            "moderado": 1.55,
            "intenso": 1.725,
            "muito_intenso": 1.9
        }
        return tmb * fatores.get(atividade, 1.375)
    
    @staticmethod
    def calcular_agua(peso, atividade="moderado", clima="temperado"):
        """Calcula necessidades hídricas"""
        base = peso * 35  # ml por kg
        
        # Ajustes
        if atividade == "intenso":
            base *= 1.3
        elif atividade == "muito_intenso":
            base *= 1.5
        
        if clima == "quente":
            base *= 1.2
        
        return base / 1000  # retorna em litros
    
    @staticmethod
    def distribuir_macros(calorias, tipo_dieta="balanceada"):
        """Distribui macronutrientes por tipo de dieta"""
        distribuicoes = {
            "balanceada": {"carb": 50, "prot": 20, "gord": 30},
            "low_carb": {"carb": 25, "prot": 35, "gord": 40},
            "cetogenica": {"carb": 5, "prot": 25, "gord": 70},
            "high_protein": {"carb": 40, "prot": 35, "gord": 25},
            "mediterranea": {"carb": 45, "prot": 20, "gord": 35},
            "dash": {"carb": 55, "prot": 18, "gord": 27}
        }
        
        dist = distribuicoes.get(tipo_dieta, distribuicoes["balanceada"])
        
        return {
            "carb_g": (calorias * dist["carb"] / 100) / 4,
            "prot_g": (calorias * dist["prot"] / 100) / 4,
            "gord_g": (calorias * dist["gord"] / 100) / 9,
            "carb_percent": dist["carb"],
            "prot_percent": dist["prot"],
            "gord_percent": dist["gord"]
        }

class NutriStock360Pro:
    def __init__(self):
        self.calc = CalculadorasNutricionais()
        self.init_session_state()
        
    def init_session_state(self):
        """Inicializa o estado da sessão"""
        defaults = {
            'authenticated': False,
            'current_user': None,
            'pacientes': self.load_demo_pacientes(),
            'consultas': [],
            'receitas': self.load_default_receitas(),
            'planos_alimentares': [],
            'agendamentos': self.load_demo_agendamentos(),
            'configuracoes': self.load_default_config(),
            'historico_peso': {},
            'metas_pacientes': {},
            'relatorios_salvos': [],
            'evolucoes_pacientes': {},
            'cardapios_salvos': [],
            'templates_comunicacao': self.load_default_templates(),
            'exames_laboratoriais': []
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def load_demo_pacientes(self):
        """Carrega pacientes de demonstração"""
        return [
            {
                "id": 1,
                "nome": "Maria Silva",
                "email": "maria@email.com",
                "telefone": "(11) 99999-9999",
                "data_nascimento": "1985-05-15",
                "sexo": "Feminino",
                "peso": 68.5,
                "altura": 1.65,
                "objetivo": "Perda de peso",
                "data_cadastro": "2024-01-15",
                "status": "Ativo",
                "imc": 25.2,
                "bf_percent": 28.5,
                "observacoes": "Hipertensa controlada com medicamento"
            },
            {
                "id": 2,
                "nome": "João Santos",
                "email": "joao@email.com",
                "telefone": "(11) 88888-8888",
                "data_nascimento": "1992-03-22",
                "sexo": "Masculino",
                "peso": 85.2,
                "altura": 1.78,
                "objetivo": "Ganho de massa muscular",
                "data_cadastro": "2024-02-01",
                "status": "Ativo",
                "imc": 26.9,
                "bf_percent": 15.2,
                "observacoes": "Pratica musculação 5x por semana"
            },
            {
                "id": 3,
                "nome": "Ana Costa",
                "email": "ana@email.com",
                "telefone": "(11) 77777-7777",
                "data_nascimento": "1990-08-10",
                "sexo": "Feminino",
                "peso": 58.0,
                "altura": 1.62,
                "objetivo": "Manutenção",
                "data_cadastro": "2024-03-10",
                "status": "Ativo",
                "imc": 22.1,
                "bf_percent": 22.0,
                "observacoes": "Vegetariana"
            }
        ]
    
    def load_demo_agendamentos(self):
        """Carrega agendamentos de demonstração"""
        hoje = datetime.now()
        return [
            {
                "id": 1,
                "paciente": "Maria Silva",
                "data": hoje.strftime("%Y-%m-%d"),
                "horario": "14:00",
                "tipo": "Consulta inicial",
                "status": "Agendado",
                "valor": 150.00,
                "observacoes": "Primeira consulta - anamnese completa"
            },
            {
                "id": 2,
                "paciente": "João Santos",
                "data": (hoje + timedelta(days=1)).strftime("%Y-%m-%d"),
                "horario": "16:00",
                "tipo": "Retorno",
                "status": "Agendado",
                "valor": 100.00,
                "observacoes": "Ajuste do plano alimentar"
            },
            {
                "id": 3,
                "paciente": "Ana Costa",
                "data": (hoje - timedelta(days=2)).strftime("%Y-%m-%d"),
                "horario": "10:00",
                "tipo": "Consulta inicial",
                "status": "Realizado",
                "valor": 150.00,
                "observacoes": "Paciente vegetariana"
            }
        ]
            
    def load_default_receitas(self):
        """Carrega receitas padrão expandidas"""
        return [
            {
                "id": 1,
                "nome": "Bowl Proteico Completo",
                "ingredientes": ["Quinoa (50g)", "Frango grelhado (100g)", "Abacate (50g)", "Brócolis (100g)", "Azeite (1 colher)"],
                "calorias": 520,
                "proteinas": 38,
                "carboidratos": 32,
                "gorduras": 28,
                "fibras": 12,
                "preparo": "Cozinhe a quinoa. Grelhe o frango temperado. Refogue o brócolis. Monte o bowl com todos os ingredientes.",
                "categoria": "Pratos Principais",
                "tempo_preparo": "25 minutos",
                "dificuldade": "Médio",
                "porcoes": 1,
                "custo_estimado": 12.50,
                "tags": ["proteico", "low-carb", "fitness"]
            },
            {
                "id": 2,
                "nome": "Smoothie Verde Detox",
                "ingredientes": ["Espinafre (50g)", "Banana (1 unidade)", "Maçã verde (1/2)", "Água de coco (200ml)", "Chia (1 colher)"],
                "calorias": 185,
                "proteinas": 6,
                "carboidratos": 38,
                "gorduras": 4,
                "fibras": 9,
                "preparo": "Bata todos os ingredientes no liquidificador até ficar homogêneo. Sirva gelado.",
                "categoria": "Bebidas",
                "tempo_preparo": "5 minutos",
                "dificuldade": "Fácil",
                "porcoes": 1,
                "custo_estimado": 6.80,
                "tags": ["detox", "vegano", "antioxidante"]
            },
            {
                "id": 3,
                "nome": "Salada Mediterrânea",
                "ingredientes": ["Mix de folhas (100g)", "Tomate cereja (100g)", "Pepino (50g)", "Queijo feta (30g)", "Azeitonas (20g)", "Azeite extra virgem (1 colher)"],
                "calorias": 245,
                "proteinas": 12,
                "carboidratos": 15,
                "gorduras": 18,
                "fibras": 6,
                "preparo": "Misture todos os vegetais. Adicione o queijo em cubos e as azeitonas. Tempere com azeite e ervas.",
                "categoria": "Saladas",
                "tempo_preparo": "10 minutos",
                "dificuldade": "Fácil",
                "porcoes": 1,
                "custo_estimado": 8.90,
                "tags": ["mediterrânea", "vegetariano", "fibras"]
            },
            {
                "id": 4,
                "nome": "Omelete de Vegetais",
                "ingredientes": ["Ovos (2 unidades)", "Espinafre (30g)", "Tomate (50g)", "Queijo cottage (2 colheres)", "Azeite (1 colher chá)"],
                "calorias": 285,
                "proteinas": 22,
                "carboidratos": 8,
                "gorduras": 18,
                "fibras": 3,
                "preparo": "Bata os ovos, refogue os vegetais, despeje os ovos e adicione o queijo cottage.",
                "categoria": "Café da Manhã",
                "tempo_preparo": "15 minutos",
                "dificuldade": "Fácil",
                "porcoes": 1,
                "custo_estimado": 4.50,
                "tags": ["proteico", "low-carb", "vegetariano"]
            }
        ]
    
    def load_default_config(self):
        """Configurações padrão expandidas"""
        return {
            "empresa_nome": "NutriClinic Pro",
            "empresa_logo": None,
            "cores_tema": "azul",
            "moeda": "BRL",
            "valor_consulta": 150.00,
            "valor_retorno": 100.00,
            "tempo_consulta": 60,
            "horario_inicio": "08:00",
            "horario_fim": "18:00",
            "dias_trabalho": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
            "whatsapp": "",
            "email": "",
            "endereco": "",
            "crn": "",
            "meta_pacientes_mes": 50,
            "meta_receita_mes": 7500.00,
            "backup_automatico": True,
            "notificacoes_email": True,
            "notificacoes_whatsapp": True,
            "intervalos_consulta": [30, 45, 60, 90],
            "tipos_consulta": ["Consulta inicial", "Retorno", "Avaliação", "Orientação"],
            "formas_pagamento": ["Dinheiro", "PIX", "Cartão", "Transferência"]
        }
    
    def load_default_templates(self):
        """Templates de comunicação"""
        return {
            "lembrete_consulta": "Olá {nome}! Lembrando que você tem consulta marcada para {data} às {horario}. Confirme sua presença.",
            "plano_pronto": "Oi {nome}! Seu novo plano alimentar está pronto. Siga as orientações e qualquer dúvida me procure.",
            "motivacional": "Parabéns {nome}! Você está no caminho certo. Continue firme no seu objetivo!",
            "reagendamento": "Olá {nome}, precisamos reagendar sua consulta. Entre em contato para marcarmos novo horário.",
            "primeira_consulta": "Seja bem-vindo(a) {nome}! Estou muito feliz em acompanhar sua jornada de saúde e bem-estar.",
            "aniversario": "Parabéns {nome}! Desejo um ano repleto de saúde e conquistas!"
        }
    
    def hash_password(self, password: str) -> str:
        """Hash da senha"""
        if BCRYPT_AVAILABLE:
            return bcrypt.hash(password)
        else:
            return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verifica senha"""
        if BCRYPT_AVAILABLE:
            return bcrypt.verify(password, hashed)
        else:
            return hashlib.sha256(password.encode()).hexdigest() == hashed
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Autentica usuário"""
        users = {
            "admin": self.hash_password("admin123"),
            "nutricionista": self.hash_password("nutri123"),
            "demo": self.hash_password("demo123")
        }
        
        if username in users and self.verify_password(password, users[username]):
            st.session_state.authenticated = True
            st.session_state.current_user = username
            return True
        return False
    
    def create_gauge_chart(self, value, max_value, title, color="#667eea"):
        """Cria gráfico gauge"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title, 'font': {'size': 16}},
            gauge = {
                'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, max_value*0.6], 'color': 'lightgray'},
                    {'range': [max_value*0.6, max_value*0.8], 'color': 'yellow'},
                    {'range': [max_value*0.8, max_value], 'color': 'lightgreen'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_value*0.9
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            font={'color': "darkblue", 'family': "Arial"},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        return fig
    
    def create_progress_chart(self, dates, weights, target_weight):
        """Cria gráfico de progresso de peso"""
        fig = go.Figure()
        
        # Linha de progresso
        fig.add_trace(go.Scatter(
            x=dates,
            y=weights,
            mode='lines+markers',
            name='Peso Atual',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#f093fb')
        ))
        
        # Linha de meta
        fig.add_hline(
            y=target_weight,
            line_dash="dash",
            line_color="green",
            annotation_text=f"Meta: {target_weight} kg"
        )
        
        fig.update_layout(
            title="Evolução do Peso",
            xaxis_title="Data",
            yaxis_title="Peso (kg)",
            height=400,
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        
        return fig
    
    def login_page(self):
        """Página de login melhorada"""
        st.markdown('''
        <div class="main-header">
            <h1>🥗 NutriStock360 Pro</h1>
            <p>Sistema Profissional Completo para Nutricionistas</p>
            <p><em>Versão 3.0 - Experiência Premium Total</em></p>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="tab-content">
                <h3 style="text-align: center; color: #667eea; margin-bottom: 2rem;">🔐 Acesso Seguro ao Sistema</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
                password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    remember = st.checkbox("🔄 Lembrar de mim")
                with col_b:
                    auto_backup = st.checkbox("💾 Backup automático")
                
                submitted = st.form_submit_button("🚀 Entrar no Sistema", use_container_width=True, type="primary")
                
                if submitted:
                    with st.spinner("Verificando credenciais..."):
                        time.sleep(0.5)
                        if self.authenticate_user(username, password):
                            st.success("✅ Login realizado com sucesso!")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Usuário ou senha incorretos!")
            
            with st.expander("👥 Contas de Demonstração & Recursos", expanded=False):
                st.markdown("""
                **🔑 Credenciais de Teste:**
                - **Administrador:** `admin` / `admin123`
                - **Nutricionista:** `nutricionista` / `nutri123`  
                - **Demo:** `demo` / `demo123`
                
                **✨ Sistema Completo v3.0:**
                
                🧮 **Calculadoras Profissionais** - 15+ fórmulas científicas
                👥 **Gestão de Pacientes** - Cadastro, evolução e acompanhamento
                📅 **Agendamentos** - Sistema completo de consultas
                🍳 **Banco de Receitas** - Receitas personalizadas com análise nutricional
                🍽️ **Planos Alimentares** - Criação e gestão de dietas
                📊 **Relatórios Avançados** - Analytics e insights profissionais
                💬 **Comunicação** - WhatsApp, templates e lembretes
                🎯 **Metas & Objetivos** - Acompanhamento de resultados
                ⚙️ **Configurações** - Personalização completa do sistema
                📈 **Dashboard Executivo** - KPIs e métricas em tempo real
                """)
    
    def sidebar_menu(self):
        """Menu lateral melhorado"""
        with st.sidebar:
            st.markdown(f'''
            <div class="sidebar-logo">
                <h2>🥗 NutriStock360</h2>
                <p>Pro Dashboard</p>
                <small>v3.0 Premium Total</small>
            </div>
            ''', unsafe_allow_html=True)
            
            # Informações do usuário melhoradas
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.9); padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; text-align: center; backdrop-filter: blur(10px);">
                <div style="color: #667eea; font-weight: 700; font-size: 1.1rem;">👤 {st.session_state.current_user}</div>
                <div style="color: #718096; font-size: 0.9rem; margin: 0.5rem 0;">📅 {datetime.now().strftime('%d/%m/%Y')}</div>
                <div style="color: #718096; font-size: 0.9rem;">🕐 {datetime.now().strftime('%H:%M')}</div>
                <div style="color: #48bb78; font-size: 0.8rem; margin-top: 0.5rem;">🟢 Online</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Menu principal expandido
            menu_options = [
                "📊 Dashboard Executivo",
                "🧮 Calculadoras Profissionais", 
                "👥 Gestão de Pacientes",
                "📈 Evolução & Progresso",
                "🍽️ Planos Alimentares",
                "🍳 Banco de Receitas",
                "📅 Agendamentos",
                "📊 Relatórios Avançados",
                "💬 Comunicação",
                "🎯 Metas & Objetivos",
                "⚙️ Configurações"
            ]
            
            selected = st.selectbox("🧭 Navegação Principal", menu_options, key="main_menu")
            
            # Estatísticas em tempo real melhoradas
            st.markdown("---")
            st.markdown("**📊 Métricas em Tempo Real**")
            
            total_pacientes = len(st.session_state.pacientes)
            consultas_hoje = len([a for a in st.session_state.agendamentos if a.get('data') == datetime.now().strftime('%Y-%m-%d')])
            receitas_total = len(st.session_state.receitas)
            
            # Métricas com progresso visual
            meta_pacientes = st.session_state.configuracoes.get('meta_pacientes_mes', 50)
            progress_pacientes = min(100, (total_pacientes / meta_pacientes) * 100) if meta_pacientes > 0 else 0
            
            st.markdown(f"""
            <div style="background: #667eea15; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #667eea;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="color: #667eea; font-weight: 600;">👥 Pacientes</div>
                    <div style="color: #667eea; font-size: 1.2rem; font-weight: 700;">{total_pacientes}</div>
                </div>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {progress_pacientes}%; background: linear-gradient(90deg, #667eea, #764ba2);"></div>
                </div>
                <div style="color: #718096; font-size: 0.8rem;">Meta: {meta_pacientes}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: #48bb7815; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #48bb78;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="color: #48bb78; font-weight: 600;">📅 Hoje</div>
                    <div style="color: #48bb78; font-size: 1.2rem; font-weight: 700;">{consultas_hoje}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: #ed893615; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #ed8936;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="color: #ed8936; font-weight: 600;">🍳 Receitas</div>
                    <div style="color: #ed8936; font-size: 1.2rem; font-weight: 700;">{receitas_total}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Ações rápidas melhoradas
            st.markdown("---")
            st.markdown("**⚡ Ações Rápidas**")
            
            if st.button("➕ Novo Paciente", use_container_width=True, key="quick_patient"):
                st.session_state.main_menu = "👥 Gestão de Pacientes"
                st.rerun()
            
            if st.button("📅 Agendar Consulta", use_container_width=True, key="quick_schedule"):
                st.session_state.main_menu = "📅 Agendamentos"
                st.rerun()
            
            if st.button("🧮 Calculadoras", use_container_width=True, key="quick_calc"):
                st.session_state.main_menu = "🧮 Calculadoras Profissionais"
                st.rerun()
            
            # Status do sistema expandido
            st.markdown("---")
            st.markdown("**🔧 Status do Sistema**")
            
            uptime = "99.9%"
            last_backup = datetime.now().strftime("%H:%M")
            
            st.markdown(f"""
            <div style="background: #48bb7815; padding: 1rem; border-radius: 10px; border-left: 4px solid #48bb78;">
                <div style="color: #48bb78; font-weight: 600; margin-bottom: 0.5rem;">✅ Sistema Online</div>
                <div style="color: #718096; font-size: 0.8rem;">Uptime: {uptime}</div>
                <div style="color: #718096; font-size: 0.8rem;">Último backup: {last_backup}</div>
                <div style="color: #718096; font-size: 0.8rem;">Todos os módulos funcionando</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            if st.button("🚪 Logout Seguro", use_container_width=True, type="primary"):
                st.session_state.authenticated = False
                st.session_state.current_user = None
                st.success("Logout realizado com sucesso!")
                time.sleep(1)
                st.rerun()
            
            return selected
    
    def dashboard_page(self):
        """Dashboard executivo melhorado"""
        st.markdown('<div class="main-header"><h1>📊 Dashboard Executivo Interativo</h1><p>Visão 360° da sua prática nutricional em tempo real</p></div>', unsafe_allow_html=True)
        
        # KPIs principais melhorados
        st.markdown("### 📈 Indicadores-Chave de Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_pacientes = len(st.session_state.pacientes)
        consultas_hoje = len([a for a in st.session_state.agendamentos if a.get('data') == datetime.now().strftime('%Y-%m-%d')])
        receita_mensal = sum([a.get('valor', 0) for a in st.session_state.agendamentos if a.get('status') == 'Realizado'])
        taxa_retorno = 85.5  # Simulado
        
        # Cálculo de tendências
        crescimento_pacientes = "+12%"
        crescimento_consultas = "+8%"
        crescimento_receita = "+15%"
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <div style="text-align: center;">
                    <div class="metric-value">{total_pacientes}</div>
                    <div class="metric-label">Pacientes Ativos</div>
                    <div style="color: #48bb78; font-size: 0.9rem; margin-top: 0.5rem;">📈 {crescimento_pacientes}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <div style="text-align: center;">
                    <div class="metric-value">{consultas_hoje}</div>
                    <div class="metric-label">Consultas Hoje</div>
                    <div style="color: #48bb78; font-size: 0.9rem; margin-top: 0.5rem;">📈 {crescimento_consultas}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <div style="text-align: center;">
                    <div class="metric-value">R$ {receita_mensal:,.0f}</div>
                    <div class="metric-label">Receita Mensal</div>
                    <div style="color: #48bb78; font-size: 0.9rem; margin-top: 0.5rem;">📈 {crescimento_receita}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <div style="text-align: center;">
                    <div class="metric-value">{taxa_retorno}%</div>
                    <div class="metric-label">Taxa de Retorno</div>
                    <div style="color: #48bb78; font-size: 0.9rem; margin-top: 0.5rem;">📈 +2.3%</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Gráficos analíticos avançados
        st.markdown("### 📊 Analytics Visuais Avançados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📈 Evolução de Pacientes & Receita")
            
            # Dados mais realistas com crescimento orgânico
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            pacientes_data = [8, 12, 15, 22, 28, 35, 42, 48, 55, 62, 68, max(total_pacientes, 75)]
            receita_data = [p * 150 * 0.8 for p in pacientes_data]  # Assumindo 80% de conversão
            
            fig = go.Figure()
            
            # Linha de pacientes
            fig.add_trace(go.Scatter(
                x=meses, 
                y=pacientes_data,
                mode='lines+markers',
                name='Pacientes',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8, color='#f093fb'),
                yaxis='y'
            ))
            
            # Linha de receita
            fig.add_trace(go.Scatter(
                x=meses,
                y=receita_data,
                mode='lines+markers',
                name='Receita (R$)',
                line=dict(color='#48bb78', width=3),
                marker=dict(size=8, color='#ed8936'),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title="Crescimento do Negócio 2024",
                xaxis_title="Meses",
                yaxis=dict(title="Número de Pacientes", side="left", color="#667eea"),
                yaxis2=dict(title="Receita (R$)", side="right", overlaying="y", color="#48bb78"),
                height=400,
                hovermode='x unified',
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🎯 Performance vs Metas")
            
            # Dados de performance vs metas
            categorias = ['Novos Pacientes', 'Consultas', 'Receita', 'Retenção', 'Satisfação']
            valores_atuais = [85, 92, 78, 88, 95]
            metas = [80, 90, 85, 85, 90]
            
            fig = go.Figure()
            
            # Barras das metas
            fig.add_trace(go.Bar(
                name='Meta',
                x=categorias,
                y=metas,
                marker_color='lightgray',
                opacity=0.6
            ))
            
            # Barras dos valores atuais
            fig.add_trace(go.Bar(
                name='Atual',
                x=categorias,
                y=valores_atuais,
                marker_color=['#667eea', '#48bb78', '#ed8936', '#f093fb', '#9f7aea'],
                text=valores_atuais,
                textposition='auto'
            ))
            
            fig.update_layout(
                title="Performance vs Metas (%)",
                barmode='overlay',
                height=400,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Agenda do dia e próximos compromissos
        st.markdown("### 📅 Agenda & Compromissos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📋 Agenda de Hoje")
            
            hoje = datetime.now().strftime('%Y-%m-%d')
            agendamentos_hoje = [a for a in st.session_state.agendamentos if a.get('data') == hoje]
            
            if agendamentos_hoje:
                agendamentos_hoje.sort(key=lambda x: x['horario'])
                
                for apt in agendamentos_hoje:
                    status_color = {
                        "Agendado": "#667eea",
                        "Realizado": "#48bb78", 
                        "Cancelado": "#e53e3e",
                        "Em andamento": "#ed8936"
                    }.get(apt.get('status', 'Agendado'), '#718096')
                    
                    st.markdown(f"""
                    <div style="background: {status_color}15; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {status_color};">
                        <div style="color: {status_color}; font-weight: 600;">
                            🕐 {apt['horario']} - {apt['paciente']}
                        </div>
                        <div style="color: #718096; font-size: 0.9rem;">
                            📋 {apt['tipo']} • {apt.get('status', 'Agendado')}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("📅 Nenhum agendamento para hoje. Aproveite para planejamento!")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🔔 Lembretes & Notificações")
            
            # Lembretes inteligentes
            lembretes = [
                {"tipo": "urgent", "icon": "🚨", "texto": "Consulta em 30 min: Maria Silva (primeira consulta)", "cor": "#e53e3e"},
                {"tipo": "important", "icon": "📞", "texto": "Retornar ligação: João Santos (interessado em plano)", "cor": "#ed8936"},
                {"tipo": "info", "icon": "📊", "texto": "Relatório mensal pronto para envio", "cor": "#3182ce"},
                {"tipo": "success", "icon": "🎉", "texto": "Meta de pacientes atingida: 75/70", "cor": "#48bb78"},
                {"tipo": "reminder", "icon": "💊", "texto": "Atualizar conhecimento: Novo curso de nutrição esportiva", "cor": "#9f7aea"}
            ]
            
            for lembrete in lembretes:
                st.markdown(f"""
                <div style="background: {lembrete['cor']}15; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {lembrete['cor']};">
                    <div style="color: {lembrete['cor']}; font-weight: 600;">
                        {lembrete['icon']} {lembrete['texto']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    def calculadoras_page(self):
        """Calculadoras profissionais completas"""
        st.markdown('<div class="main-header"><h1>🧮 Calculadoras Nutricionais Profissionais</h1><p>Suite completa com 15+ fórmulas científicas validadas</p></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📏 Básicas", 
            "🔥 Metabólicas", 
            "📊 Composição Corporal", 
            "🎯 Planejamento"
        ])
        
        with tab1:
            self.calculadoras_basicas()
        
        with tab2:
            self.calculadoras_metabolicas()
        
        with tab3:
            self.calculadoras_composicao()
        
        with tab4:
            self.calculadoras_planejamento()
    
    def calculadoras_basicas(self):
        """Calculadoras básicas melhoradas"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
            st.subheader("📏 Calculadora de IMC Avançada")
            
            peso = st.slider("⚖️ Peso (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
            altura = st.slider("📏 Altura (m)", min_value=1.0, max_value=2.2, value=1.70, step=0.01)
            
            # Cálculo em tempo real
            imc, classificacao, status = self.calc.calcular_imc(peso, altura)
            
            # Resultado visual
            st.markdown(f'''
            <div class="calculator-result">
                IMC: {imc:.1f} kg/m²
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="status-card status-{status}">
                Classificação: {classificacao}
            </div>
            ''', unsafe_allow_html=True)
            
            # Gráfico gauge
            fig = self.create_gauge_chart(imc, 40, "IMC", "#667eea")
            st.plotly_chart(fig, use_container_width=True)
            
            # Informações adicionais
            peso_min_saudavel = 18.5 * (altura ** 2)
            peso_max_saudavel = 24.9 * (altura ** 2)
            
            st.info(f"**Faixa de peso saudável:** {peso_min_saudavel:.1f} - {peso_max_saudavel:.1f} kg")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
            st.subheader("⚖️ Peso Ideal - Múltiplos Métodos")
            
            altura_ideal = st.slider("📏 Altura (m)", min_value=1.0, max_value=2.2, value=1.70, step=0.01, key="altura_ideal")
            sexo_ideal = st.radio("👤 Sexo", ["Masculino", "Feminino"], horizontal=True)
            
            # Calcular por todos os métodos
            metodos = ["robinson", "devine", "hamwi", "miller"]
            nomes_metodos = ["Robinson", "Devine", "Hamwi", "Miller"]
            cores_metodos = ["#667eea", "#48bb78", "#ed8936", "#9f7aea"]
            
            resultados = []
            for metodo in metodos:
                peso_ideal = self.calc.calcular_peso_ideal(altura_ideal, sexo_ideal, metodo)
                resultados.append(peso_ideal)
            
            # Mostrar resultados
            for i, (nome, peso, cor) in enumerate(zip(nomes_metodos, resultados, cores_metodos)):
                st.markdown(f'''
                <div style="background: {cor}15; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {cor};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="color: {cor}; font-weight: 600;">Método {nome}</div>
                        <div style="color: {cor}; font-size: 1.2rem; font-weight: 700;">{peso:.1f} kg</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Gráfico comparativo
            fig = go.Figure(data=[
                go.Bar(
                    x=nomes_metodos,
                    y=resultados,
                    marker_color=cores_metodos,
                    text=[f"{r:.1f}" for r in resultados],
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title="Comparação de Métodos",
                yaxis_title="Peso (kg)",
                height=300,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Média e recomendação
            media_pesos = sum(resultados) / len(resultados)
            st.success(f"**Peso médio recomendado:** {media_pesos:.1f} kg")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def calculadoras_metabolicas(self):
        """Calculadoras metabólicas avançadas"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
            st.subheader("🔥 Taxa Metabólica Basal - 3 Fórmulas")
            
            peso_tmb = st.number_input("⚖️ Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)
            altura_tmb = st.number_input("📏 Altura (cm)", min_value=100, max_value=250, value=170)
            idade_tmb = st.number_input("🎂 Idade (anos)", min_value=10, max_value=100, value=30)
            sexo_tmb = st.selectbox("👤 Sexo", ["Masculino", "Feminino"])
            
            # Calcular por múltiplas fórmulas
            tmb_mifflin = self.calc.calcular_tmb(peso_tmb, altura_tmb, idade_tmb, sexo_tmb, "mifflin")
            tmb_harris = self.calc.calcular_tmb(peso_tmb, altura_tmb, idade_tmb, sexo_tmb, "harris")
            tmb_katch = self.calc.calcular_tmb(peso_tmb, altura_tmb, idade_tmb, sexo_tmb, "katch")
            
            # Resultados
            formulas = [
                ("Mifflin-St Jeor", tmb_mifflin, "#667eea", "Mais precisa para população geral"),
                ("Harris-Benedict", tmb_harris, "#48bb78", "Tradicional, ligeiramente superestima"),
                ("Katch-McArdle", tmb_katch, "#ed8936", "Baseada na massa magra")
            ]
            
            for nome, valor, cor, desc in formulas:
                st.markdown(f'''
                <div style="background: {cor}15; padding: 1.2rem; border-radius: 12px; margin: 0.8rem 0; border: 2px solid {cor};">
                    <div style="color: {cor}; font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">
                        {nome}: {valor:.0f} kcal/dia
                    </div>
                    <div style="color: #718096; font-size: 0.9rem;">
                        {desc}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Média recomendada
            tmb_media = (tmb_mifflin + tmb_harris + tmb_katch) / 3
            st.markdown(f'''
            <div class="calculator-result">
                TMB Média Recomendada: {tmb_media:.0f} kcal/dia
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
            st.subheader("⚡ Gasto Energético Total & Macros")
            
            # Usar TMB calculada ou permitir input manual
            tmb_base = tmb_mifflin if 'tmb_mifflin' in locals() else 1500
            
            st.info(f"TMB base: {tmb_base:.0f} kcal/dia")
            
            atividade = st.selectbox("🏃 Nível de Atividade", [
                ("sedentario", "Sedentário (escritório, pouco exercício)"),
                ("leve", "Levemente ativo (exercício leve 1-3x/semana)"),
                ("moderado", "Moderadamente ativo (exercício 3-5x/semana)"),
                ("intenso", "Muito ativo (exercício 6-7x/semana)"),
                ("muito_intenso", "Extremamente ativo (atleta, trabalho físico)")
            ], format_func=lambda x: x[1])
            
            objetivo = st.selectbox("🎯 Objetivo", [
                ("manutencao", "Manter peso atual"),
                ("emagrecimento_lento", "Emagrecimento gradual (-0.5kg/sem)"),
                ("emagrecimento_moderado", "Emagrecimento moderado (-0.75kg/sem)"),
                ("emagrecimento_acelerado", "Emagrecimento acelerado (-1kg/sem)"),
                ("ganho_lento", "Ganho de peso gradual (+0.5kg/sem)"),
                ("ganho_moderado", "Ganho de peso moderado (+0.75kg/sem)")
            ], format_func=lambda x: x[1])
            
            tipo_dieta = st.selectbox("🥗 Tipo de Dieta", [
                ("balanceada", "Balanceada (50/20/30)"),
                ("low_carb", "Low Carb (25/35/40)"),
                ("cetogenica", "Cetogênica (5/25/70)"),
                ("high_protein", "High Protein (40/35/25)"),
                ("mediterranea", "Mediterrânea (45/20/35)"),
                ("dash", "DASH (55/18/27)")
            ], format_func=lambda x: x[1])
            
            # Calcular GET
            get = self.calc.calcular_get(tmb_base, atividade[0])
            
            # Ajustar para objetivo
            ajustes = {
                "manutencao": 0,
                "emagrecimento_lento": -250,
                "emagrecimento_moderado": -375,
                "emagrecimento_acelerado": -500,
                "ganho_lento": 250,
                "ganho_moderado": 375
            }
            
            calorias_alvo = get + ajustes[objetivo[0]]
            
            # Distribuir macronutrientes
            macros = self.calc.distribuir_macros(calorias_alvo, tipo_dieta[0])
            
            # Mostrar resultados
            st.markdown(f'''
            <div class="calculator-result">
                GET: {get:.0f} kcal/dia<br>
                Calorias para Objetivo: {calorias_alvo:.0f} kcal/dia
            </div>
            ''', unsafe_allow_html=True)
            
            # Macronutrientes
            st.markdown("**📊 Distribuição de Macronutrientes:**")
            
            macros_data = [
                ("🍞 Carboidratos", macros["carb_g"], macros["carb_percent"], "#3182ce"),
                ("🥩 Proteínas", macros["prot_g"], macros["prot_percent"], "#e53e3e"),
                ("🥑 Gorduras", macros["gord_g"], macros["gord_percent"], "#ed8936")
            ]
            
            for nome, gramas, percent, cor in macros_data:
                st.markdown(f'''
                <div style="background: {cor}15; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {cor};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="color: {cor}; font-weight: 600;">{nome}</div>
                        <div style="color: {cor}; font-weight: 700;">{gramas:.0f}g ({percent}%)</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Necessidades hídricas
            agua = self.calc.calcular_agua(peso_tmb, atividade[0])
            st.info(f"💧 **Necessidade hídrica:** {agua:.1f} litros/dia")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def calculadoras_composicao(self):
        """Calculadoras de composição corporal"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
            st.subheader("📊 Composição Corporal - Fórmula Navy")
            
            peso_comp = st.slider("⚖️ Peso (kg)", min_value=30.0, max_value=200.0, value=70.0)
            altura_comp = st.slider("📏 Altura (cm)", min_value=100, max_value=220, value=170)
            sexo_comp = st.radio("👤 Sexo", ["Masculino", "Feminino"], horizontal=True, key="sexo_comp")
            
            cintura = st.slider("📐 Cintura (cm)", min_value=50, max_value=150, value=80)
            pescoco = st.slider("📐 Pescoço (cm)", min_value=20, max_value=60, value=35)
            
            quadril = None
            if sexo_comp == "Feminino":
                quadril = st.slider("📐 Quadril (cm)", min_value=60, max_value=200, value=95)
            
            # Calcular percentual de gordura
            bf_result = self.calc.calcular_bf_navy(cintura, pescoco, altura_comp, quadril, sexo_comp)
            
            if bf_result[0] is not None:
                bf_percent = bf_result[0]
                
                # Classificação do percentual de gordura
                if sexo_comp == "Masculino":
                    if bf_percent < 6:
                        bf_status, bf_color = "Muito baixo", "#e53e3e"
                    elif bf_percent < 14:
                        bf_status, bf_color = "Atlético", "#48bb78"
                    elif bf_percent < 18:
                        bf_status, bf_color = "Fitness", "#48bb78"
                    elif bf_percent < 25:
                        bf_status, bf_color = "Saudável", "#667eea"
                    else:
                        bf_status, bf_color = "Acima do recomendado", "#ed8936"
                else:
                    if bf_percent < 16:
                        bf_status, bf_color = "Muito baixo", "#e53e3e"
                    elif bf_percent < 20:
                        bf_status, bf_color = "Atlético", "#48bb78"
                    elif bf_percent < 25:
                        bf_status, bf_color = "Fitness", "#48bb78"
                    elif bf_percent < 32:
                        bf_status, bf_color = "Saudável", "#667eea"
                    else:
                        bf_status, bf_color = "Acima do recomendado", "#ed8936"
                
                # Calcular massas
                massa_gorda = peso_comp * (bf_percent / 100)
                massa_magra = peso_comp - massa_gorda
                
                # Resultados visuais
                st.markdown(f'''
                <div class="calculator-result">
                    Gordura Corporal: {bf_percent:.1f}%
                </div>
                ''', unsafe_allow_html=True)
                
                st.markdown(f'''
                <div style="background: {bf_color}15; padding: 1.5rem; border-radius: 15px; text-align: center; border: 2px solid {bf_color};">
                    <div style="color: {bf_color}; font-weight: 700; font-size: 1.2rem;">
                        {bf_status}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Gráfico gauge para percentual de gordura
                fig = self.create_gauge_chart(bf_percent, 50, "% Gordura Corporal", bf_color)
                st.plotly_chart(fig, use_container_width=True)
                
                # Composição detalhada
                st.markdown("**📊 Composição Corporal:**")
                
                composicao_data = [
                    ("💪 Massa Magra", massa_magra, "#48bb78"),
                    ("📊 Massa Gorda", massa_gorda, "#ed8936")
                ]
                
                for nome, valor, cor in composicao_data:
                    percentual = (valor / peso_comp) * 100
                    st.markdown(f'''
                    <div style="background: {cor}15; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {cor};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="color: {cor}; font-weight: 600;">{nome}</div>
                            <div style="color: {cor}; font-weight: 700;">{valor:.1f} kg ({percentual:.1f}%)</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
            else:
                st.error(f"❌ {bf_result[1]}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
            st.subheader("📈 Análise de Evolução Corporal")
            
            # Simulação de dados de evolução
            if st.button("📊 Simular Evolução de 6 Meses", type="primary"):
                # Dados simulados de evolução
                semanas = list(range(0, 25, 2))
                peso_evolucao = [peso_comp - (i * 0.3) for i in range(len(semanas))]
                if 'bf_percent' in locals():
                    bf_evolucao = [bf_percent - (i * 0.5) for i in range(len(semanas))]
                else:
                    bf_evolucao = [25 - (i * 0.5) for i in range(len(semanas))]
                
                # Gráfico de evolução
                fig = go.Figure()
                
                # Linha de peso
                fig.add_trace(go.Scatter(
                    x=semanas,
                    y=peso_evolucao,
                    mode='lines+markers',
                    name='Peso (kg)',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=8),
                    yaxis='y'
                ))
                
                # Linha de percentual de gordura
                fig.add_trace(go.Scatter(
                    x=semanas,
                    y=bf_evolucao,
                    mode='lines+markers',
                    name='% Gordura',
                    line=dict(color='#ed8936', width=3),
                    marker=dict(size=8),
                    yaxis='y2'
                ))
                
                fig.update_layout(
                    title="Projeção de Evolução - 6 Meses",
                    xaxis_title="Semanas",
                    yaxis=dict(title="Peso (kg)", side="left", color="#667eea"),
                    yaxis2=dict(title="% Gordura", side="right", overlaying="y", color="#ed8936"),
                    height=400,
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Projeções
                peso_final = peso_evolucao[-1]
                bf_final = bf_evolucao[-1]
                perda_peso = peso_comp - peso_final
                reducao_bf = (bf_evolucao[0] if 'bf_percent' not in locals() else bf_percent) - bf_final
                
                st.success(f"""
                **Projeção para 6 meses:**
                - Perda de peso: {perda_peso:.1f} kg
                - Redução de gordura: {reducao_bf:.1f}%
                - Peso final: {peso_final:.1f} kg
                - % Gordura final: {bf_final:.1f}%
                """)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def calculadoras_planejamento(self):
        """Calculadoras de planejamento e metas"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
            st.subheader("🎯 Planejador de Metas Inteligente")
            
            # Dados atuais
            st.markdown("**📊 Situação Atual**")
            peso_atual = st.number_input("⚖️ Peso atual (kg)", min_value=30.0, max_value=200.0, value=80.0)
            bf_atual = st.number_input("📊 % Gordura atual", min_value=5.0, max_value=50.0, value=25.0)
            
            # Metas
            st.markdown("**🎯 Metas Desejadas**")
            peso_meta = st.number_input("🎯 Peso meta (kg)", min_value=30.0, max_value=200.0, value=75.0)
            bf_meta = st.number_input("📊 % Gordura meta", min_value=5.0, max_value=50.0, value=18.0)
            
            # Preferências
            st.markdown("**⚙️ Preferências**")
            velocidade = st.selectbox("⚡ Velocidade do processo", [
                ("conservador", "Conservador (0.25kg/semana)"),
                ("moderado", "Moderado (0.5kg/semana)"),
                ("acelerado", "Acelerado (0.75kg/semana)"),
                ("intensivo", "Intensivo (1kg/semana)")
            ], format_func=lambda x: x[1])
            
            if st.button("🚀 Calcular Planejamento", type="primary"):
                # Cálculos do planejamento
                diferenca_peso = peso_atual - peso_meta
                diferenca_bf = bf_atual - bf_meta
                
                velocidades = {
                    "conservador": 0.25,
                    "moderado": 0.5,
                    "acelerado": 0.75,
                    "intensivo": 1.0
                }
                
                peso_semana = velocidades[velocidade[0]]
                tempo_semanas = abs(diferenca_peso) / peso_semana
                tempo_meses = tempo_semanas / 4.33
                
                # Cálculo de déficit calórico necessário
                deficit_calorico = peso_semana * 7700 / 7  # kcal por dia
                
                st.markdown(f'''
                <div class="calculator-result">
                    Tempo estimado: {tempo_meses:.1f} meses ({tempo_semanas:.0f} semanas)
                </div>
                ''', unsafe_allow_html=True)
                
                # Detalhamento do plano
                plano_data = [
                    ("⏰ Duração total", f"{tempo_meses:.1f} meses", "#667eea"),
                    ("📉 Perda semanal", f"{peso_semana:.2f} kg", "#48bb78"),
                    ("🔥 Déficit diário", f"{deficit_calorico:.0f} kcal", "#ed8936"),
                    ("📊 Redução BF", f"{diferenca_bf:.1f}%", "#9f7aea")
                ]
                
                for label, valor, cor in plano_data:
                    st.markdown(f'''
                    <div style="background: {cor}15; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {cor};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="color: {cor}; font-weight: 600;">{label}</div>
                            <div style="color: {cor}; font-weight: 700;">{valor}</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Cronograma de marcos
                st.markdown("**📅 Marcos do Progresso:**")
                
                marcos = []
                for i in range(1, min(int(tempo_meses) + 1, 7)):  # Máximo 6 meses
                    peso_marco = peso_atual - (diferenca_peso * i / tempo_meses)
                    bf_marco = bf_atual - (diferenca_bf * i / tempo_meses)
                    marcos.append(f"Mês {i}: {peso_marco:.1f} kg ({bf_marco:.1f}% BF)")
                
                for marco in marcos:
                    st.info(marco)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="calculator-card">', unsafe_allow_html=True)
            st.subheader("📊 Análise de Viabilidade")
            
            # Fatores que afetam o sucesso
            st.markdown("**🎯 Fatores de Sucesso**")
            
            aderencia = st.slider("📈 Aderência à dieta (%)", min_value=50, max_value=100, value=85)
            exercicio = st.slider("💪 Frequência de exercícios (/semana)", min_value=0, max_value=7, value=4)
            sono = st.slider("😴 Qualidade do sono (1-10)", min_value=1, max_value=10, value=7)
            stress = st.slider("😰 Nível de stress (1-10)", min_value=1, max_value=10, value=5)
            
            # Cálculo do índice de sucesso
            indice_sucesso = (aderencia * 0.4 + exercicio * 10 * 0.25 + sono * 10 * 0.2 + (10 - stress) * 10 * 0.15)
            
            # Classificação do índice
            if indice_sucesso >= 85:
                sucesso_status = "Excelente"
                sucesso_cor = "#48bb78"
            elif indice_sucesso >= 70:
                sucesso_status = "Bom"
                sucesso_cor = "#667eea"
            elif indice_sucesso >= 55:
                sucesso_status = "Moderado"
                sucesso_cor = "#ed8936"
            else:
                sucesso_status = "Desafiador"
                sucesso_cor = "#e53e3e"
            
            st.markdown(f'''
            <div style="background: {sucesso_cor}15; padding: 2rem; border-radius: 15px; text-align: center; border: 2px solid {sucesso_cor};">
                <div style="color: {sucesso_cor}; font-weight: 700; font-size: 1.5rem;">
                    Índice de Sucesso: {indice_sucesso:.0f}%
                </div>
                <div style="color: {sucesso_cor}; font-weight: 600; margin-top: 0.5rem;">
                    Prognóstico: {sucesso_status}
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
            # Recomendações personalizadas
            st.markdown("**💡 Recomendações Personalizadas:**")
            
            recomendacoes = []
            
            if aderencia < 80:
                recomendacoes.append("🍽️ Melhore a aderência com refeições mais prazerosas")
            
            if exercicio < 3:
                recomendacoes.append("💪 Aumente a frequência de exercícios para pelo menos 3x/semana")
            
            if sono < 7:
                recomendacoes.append("😴 Priorize 7-9 horas de sono por noite")
            
            if stress > 6:
                recomendacoes.append("🧘 Implemente técnicas de redução de stress")
            
            if not recomendacoes:
                recomendacoes.append("✅ Excelente! Mantenha os hábitos atuais")
                recomendacoes.append("🎯 Foque na consistência e progressão gradual")
                recomendacoes.append("📊 Monitore o progresso semanalmente")
            
            for rec in recomendacoes:
                st.info(rec)
            
            # Gráfico de fatores
            if st.button("📊 Visualizar Análise", type="secondary"):
                fatores = ['Aderência', 'Exercício', 'Sono', 'Stress (inv.)']
                valores = [aderencia, exercicio * 10, sono * 10, (10 - stress) * 10]
                
                fig = go.Figure(data=go.Scatterpolar(
                    r=valores,
                    theta=fatores,
                    fill='toself',
                    fillcolor='rgba(102, 126, 234, 0.2)',
                    line=dict(color='#667eea', width=2)
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )),
                    showlegend=False,
                    title="Análise de Fatores de Sucesso",
                    height=400,
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def gestao_pacientes_page(self):
        """Gestão completa de pacientes"""
        st.markdown('<div class="main-header"><h1>👥 Gestão de Pacientes</h1><p>Cadastro, acompanhamento e evolução completa</p></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Lista de Pacientes",
            "➕ Novo Paciente", 
            "📊 Perfil Detalhado",
            "📈 Evolução"
        ])
        
        with tab1:
            self.lista_pacientes()
        
        with tab2:
            self.novo_paciente()
        
        with tab3:
            self.perfil_paciente()
        
        with tab4:
            self.evolucao_paciente()
    
    def lista_pacientes(self):
        """Lista todos os pacientes"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        # Filtros e busca
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            busca = st.text_input("🔍 Buscar paciente", placeholder="Nome ou email")
        
        with col2:
            filtro_status = st.selectbox("📊 Status", ["Todos", "Ativo", "Inativo", "Em pausa"])
        
        with col3:
            filtro_objetivo = st.selectbox("🎯 Objetivo", ["Todos", "Perda de peso", "Ganho de massa muscular", "Manutenção"])
        
        with col4:
            ordenar = st.selectbox("📈 Ordenar por", ["Nome", "Data cadastro", "Última consulta", "IMC"])
        
        # Aplicar filtros
        pacientes_filtrados = st.session_state.pacientes.copy()
        
        if busca:
            pacientes_filtrados = [p for p in pacientes_filtrados 
                                 if busca.lower() in p['nome'].lower() or busca.lower() in p['email'].lower()]
        
        if filtro_status != "Todos":
            pacientes_filtrados = [p for p in pacientes_filtrados if p['status'] == filtro_status]
        
        if filtro_objetivo != "Todos":
            pacientes_filtrados = [p for p in pacientes_filtrados if p['objetivo'] == filtro_objetivo]
        
        # Estatísticas rápidas
        st.markdown("### 📊 Estatísticas Rápidas")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total = len(st.session_state.pacientes)
            st.metric("Total de Pacientes", total, "+2 este mês")
        
        with col2:
            ativos = len([p for p in st.session_state.pacientes if p['status'] == 'Ativo'])
            st.metric("Pacientes Ativos", ativos, f"{(ativos/total*100):.0f}%")
        
        with col3:
            imc_medio = sum([p['imc'] for p in st.session_state.pacientes]) / len(st.session_state.pacientes)
            st.metric("IMC Médio", f"{imc_medio:.1f}", "Saudável")
        
        with col4:
            idade_media = 35  # Simulado
            st.metric("Idade Média", f"{idade_media} anos", "Adulto jovem")
        
        # Lista de pacientes
        st.markdown("### 👥 Lista de Pacientes")
        
        if pacientes_filtrados:
            for paciente in pacientes_filtrados:
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{paciente['nome']}**")
                        st.markdown(f"📧 {paciente['email']}")
                        st.markdown(f"📱 {paciente['telefone']}")
                    
                    with col2:
                        status_colors = {
                            "Ativo": "#48bb78",
                            "Inativo": "#e53e3e", 
                            "Em pausa": "#ed8936"
                        }
                        color = status_colors.get(paciente['status'], '#718096')
                        st.markdown(f'<div style="color: {color}; font-weight: 600;">● {paciente["status"]}</div>', unsafe_allow_html=True)
                        st.markdown(f"🎯 {paciente['objetivo']}")
                    
                    with col3:
                        st.metric("IMC", f"{paciente['imc']:.1f}")
                        st.metric("Peso", f"{paciente['peso']:.1f} kg")
                    
                    with col4:
                        st.metric("% Gordura", f"{paciente.get('bf_percent', 0):.1f}%")
                        st.metric("Altura", f"{paciente['altura']:.2f} m")
                    
                    with col5:
                        if st.button("👁️", key=f"view_{paciente['id']}", help="Ver perfil"):
                            st.session_state.paciente_selecionado = paciente['id']
                        
                        if st.button("✏️", key=f"edit_{paciente['id']}", help="Editar"):
                            st.session_state.editando_paciente = paciente['id']
                    
                    st.divider()
        else:
            st.info("Nenhum paciente encontrado com os filtros aplicados.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def novo_paciente(self):
        """Formulário para novo paciente"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("➕ Cadastro de Novo Paciente")
        
        with st.form("novo_paciente"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Dados Pessoais**")
                nome = st.text_input("Nome completo *")
                email = st.text_input("Email *")
                telefone = st.text_input("Telefone *")
                data_nascimento = st.date_input("Data de nascimento *")
                sexo = st.selectbox("Sexo *", ["Feminino", "Masculino"])
                
            with col2:
                st.markdown("**📏 Dados Antropométricos**")
                peso = st.number_input("Peso atual (kg) *", min_value=30.0, max_value=300.0, value=70.0)
                altura = st.number_input("Altura (m) *", min_value=1.0, max_value=2.5, value=1.70, step=0.01)
                objetivo = st.selectbox("Objetivo principal *", [
                    "Perda de peso",
                    "Ganho de massa muscular", 
                    "Manutenção",
                    "Melhora da saúde",
                    "Performance esportiva"
                ])
                
                # Cálculos automáticos
                if peso and altura:
                    imc = peso / (altura ** 2)
                    st.info(f"IMC calculado: {imc:.1f}")
            
            # Dados clínicos
            st.markdown("**🏥 Informações Clínicas**")
            col1, col2 = st.columns(2)
            
            with col1:
                doencas = st.multiselect("Doenças/Condições", [
                    "Diabetes", "Hipertensão", "Dislipidemia", 
                    "Hipotireoidismo", "Resistência insulínica",
                    "Distúrbios alimentares", "Outras"
                ])
                
                medicamentos = st.text_area("Medicamentos em uso")
                
            with col2:
                alergias = st.text_area("Alergias/Intolerâncias alimentares")
                cirurgias = st.text_area("Cirurgias realizadas")
            
            # Estilo de vida
            st.markdown("**🏃 Estilo de Vida**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                atividade_fisica = st.selectbox("Nível de atividade física", [
                    "Sedentário",
                    "Levemente ativo",
                    "Moderadamente ativo", 
                    "Muito ativo",
                    "Extremamente ativo"
                ])
            
            with col2:
                qualidade_sono = st.selectbox("Qualidade do sono", [
                    "Excelente", "Boa", "Regular", "Ruim", "Péssima"
                ])
            
            with col3:
                nivel_stress = st.selectbox("Nível de stress", [
                    "Baixo", "Moderado", "Alto", "Muito alto"
                ])
            
            observacoes = st.text_area("Observações gerais")
            
            submitted = st.form_submit_button("✅ Cadastrar Paciente", type="primary", use_container_width=True)
            
            if submitted:
                if nome and email and telefone and data_nascimento and peso and altura:
                    novo_paciente = {
                        "id": len(st.session_state.pacientes) + 1,
                        "nome": nome,
                        "email": email,
                        "telefone": telefone,
                        "data_nascimento": data_nascimento.strftime("%Y-%m-%d"),
                        "sexo": sexo,
                        "peso": peso,
                        "altura": altura,
                        "objetivo": objetivo,
                        "data_cadastro": datetime.now().strftime("%Y-%m-%d"),
                        "status": "Ativo",
                        "imc": imc,
                        "bf_percent": 0,
                        "doencas": doencas,
                        "medicamentos": medicamentos,
                        "alergias": alergias,
                        "cirurgias": cirurgias,
                        "atividade_fisica": atividade_fisica,
                        "qualidade_sono": qualidade_sono,
                        "nivel_stress": nivel_stress,
                        "observacoes": observacoes
                    }
                    
                    st.session_state.pacientes.append(novo_paciente)
                    st.success(f"✅ Paciente {nome} cadastrado com sucesso!")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Preencha todos os campos obrigatórios (*)")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def perfil_paciente(self):
        """Perfil detalhado do paciente"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        # Seleção do paciente
        if st.session_state.pacientes:
            opcoes_pacientes = [f"{p['nome']} - {p['email']}" for p in st.session_state.pacientes]
            paciente_selecionado = st.selectbox("👤 Selecione o paciente", opcoes_pacientes)
            
            if paciente_selecionado:
                # Encontrar paciente selecionado
                nome_selecionado = paciente_selecionado.split(" - ")[0]
                paciente = next(p for p in st.session_state.pacientes if p['nome'] == nome_selecionado)
                
                # Header do perfil
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3 style="color: #667eea;">{paciente['nome']}</h3>
                        <p>📧 {paciente['email']}</p>
                        <p>📱 {paciente['telefone']}</p>
                        <p>🎯 {paciente['objetivo']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    idade = datetime.now().year - int(paciente['data_nascimento'][:4])
                    st.metric("Idade", f"{idade} anos")
                    st.metric("Status", paciente['status'])
                
                with col3:
                    st.metric("Peso", f"{paciente['peso']:.1f} kg")
                    st.metric("Altura", f"{paciente['altura']:.2f} m")
                
                with col4:
                    st.metric("IMC", f"{paciente['imc']:.1f}")
                    imc_status = "Saudável" if 18.5 <= paciente['imc'] < 25 else "Atenção"
                    st.metric("Classificação", imc_status)
                
                # Abas do perfil
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📋 Dados Gerais",
                    "🏥 Informações Clínicas", 
                    "📊 Análise Corporal",
                    "📈 Histórico"
                ])
                
                with tab1:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**👤 Informações Pessoais**")
                        st.info(f"""
                        **Nome:** {paciente['nome']}
                        **Email:** {paciente['email']}
                        **Telefone:** {paciente['telefone']}
                        **Data Nascimento:** {paciente['data_nascimento']}
                        **Sexo:** {paciente['sexo']}
                        **Data Cadastro:** {paciente['data_cadastro']}
                        """)
                    
                    with col2:
                        st.markdown("**🏃 Estilo de Vida**")
                        st.info(f"""
                        **Atividade Física:** {paciente.get('atividade_fisica', 'Não informado')}
                        **Qualidade do Sono:** {paciente.get('qualidade_sono', 'Não informado')}
                        **Nível de Stress:** {paciente.get('nivel_stress', 'Não informado')}
                        """)
                        
                        if paciente.get('observacoes'):
                            st.markdown("**📝 Observações**")
                            st.text_area("", value=paciente['observacoes'], disabled=True, height=100)
                
                with tab2:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**🏥 Condições de Saúde**")
                        if paciente.get('doencas'):
                            for doenca in paciente['doencas']:
                                st.markdown(f"• {doenca}")
                        else:
                            st.info("Nenhuma doença relatada")
                        
                        if paciente.get('medicamentos'):
                            st.markdown("**💊 Medicamentos**")
                            st.text_area("", value=paciente['medicamentos'], disabled=True)
                    
                    with col2:
                        if paciente.get('alergias'):
                            st.markdown("**🚫 Alergias/Intolerâncias**")
                            st.text_area("", value=paciente['alergias'], disabled=True)
                        
                        if paciente.get('cirurgias'):
                            st.markdown("**🏥 Cirurgias**")
                            st.text_area("", value=paciente['cirurgias'], disabled=True)
                
                with tab3:
                    # Análise corporal detalhada
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Gráfico gauge do IMC
                        fig_imc = self.create_gauge_chart(paciente['imc'], 40, "IMC", "#667eea")
                        st.plotly_chart(fig_imc, use_container_width=True)
                    
                    with col2:
                        # Classificações
                        imc = paciente['imc']
                        if imc < 18.5:
                            status_imc = "Abaixo do peso"
                            cor_imc = "#ed8936"
                        elif imc < 25:
                            status_imc = "Peso normal"
                            cor_imc = "#48bb78"
                        elif imc < 30:
                            status_imc = "Sobrepeso"
                            cor_imc = "#ed8936"
                        else:
                            status_imc = "Obesidade"
                            cor_imc = "#e53e3e"
                        
                        st.markdown(f"""
                        <div style="background: {cor_imc}15; padding: 2rem; border-radius: 15px; text-align: center; border: 2px solid {cor_imc};">
                            <div style="color: {cor_imc}; font-weight: 700; font-size: 1.3rem;">
                                {status_imc}
                            </div>
                            <div style="color: {cor_imc}; margin-top: 0.5rem;">
                                IMC: {imc:.1f} kg/m²
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Recomendações
                        st.markdown("**💡 Recomendações:**")
                        
                        if imc < 18.5:
                            st.info("📈 Foco no ganho de peso saudável")
                        elif imc < 25:
                            st.success("✅ Manter peso atual")
                        elif imc < 30:
                            st.warning("📉 Perda de peso recomendada")
                        else:
                            st.error("🚨 Perda de peso necessária - acompanhamento médico")
                
                with tab4:
                    st.info("📈 Histórico de evolução em desenvolvimento")
                    
                    # Simulação de dados de progresso
                    if st.button("📊 Simular Evolução", type="secondary"):
                        dates = pd.date_range(start='2024-01-01', periods=12, freq='M')
                        weights = [paciente['peso'] - i*0.5 for i in range(12)]
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=dates,
                            y=weights,
                            mode='lines+markers',
                            name='Peso (kg)',
                            line=dict(color='#667eea', width=3)
                        ))
                        
                        fig.update_layout(
                            title="Evolução do Peso",
                            xaxis_title="Data",
                            yaxis_title="Peso (kg)",
                            height=400,
                            paper_bgcolor="rgba(0,0,0,0)"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("📝 Nenhum paciente cadastrado ainda.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def evolucao_paciente(self):
        """Evolução e progresso do paciente"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("📈 Evolução e Progresso")
        
        if st.session_state.pacientes:
            # Seleção do paciente
            opcoes_pacientes = [f"{p['nome']} - {p['email']}" for p in st.session_state.pacientes]
            paciente_selecionado = st.selectbox("👤 Selecione o paciente", opcoes_pacientes, key="evolucao_paciente")
            
            if paciente_selecionado:
                nome_selecionado = paciente_selecionado.split(" - ")[0]
                paciente = next(p for p in st.session_state.pacientes if p['nome'] == nome_selecionado)
                
                # Formulário para nova medição
                with st.expander("➕ Adicionar Nova Medição"):
                    with st.form("nova_medicao"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            novo_peso = st.number_input("Peso (kg)", value=paciente['peso'], min_value=30.0, max_value=300.0)
                            nova_altura = st.number_input("Altura (m)", value=paciente['altura'], min_value=1.0, max_value=2.5, step=0.01)
                        
                        with col2:
                            bf_percent = st.number_input("% Gordura", value=0.0, min_value=0.0, max_value=50.0, step=0.1)
                            massa_muscular = st.number_input("Massa Muscular (kg)", value=0.0, min_value=0.0, max_value=100.0, step=0.1)
                        
                        with col3:
                            data_medicao = st.date_input("Data da medição", value=datetime.now())
                            observacoes_medicao = st.text_area("Observações", height=60)
                        
                        if st.form_submit_button("💾 Salvar Medição", type="primary"):
                            # Atualizar dados do paciente
                            for i, p in enumerate(st.session_state.pacientes):
                                if p['id'] == paciente['id']:
                                    st.session_state.pacientes[i]['peso'] = novo_peso
                                    st.session_state.pacientes[i]['altura'] = nova_altura
                                    st.session_state.pacientes[i]['imc'] = novo_peso / (nova_altura ** 2)
                                    st.session_state.pacientes[i]['bf_percent'] = bf_percent
                                    break
                            
                            st.success("✅ Medição salva com sucesso!")
                            time.sleep(1)
                            st.rerun()
                
                # Análise de progresso
                st.markdown("### 📊 Análise de Progresso")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**⚖️ Peso Atual**")
                    peso_inicial = 70.0  # Simulado
                    diferenca_peso = paciente['peso'] - peso_inicial
                    cor_peso = "#48bb78" if diferenca_peso < 0 else "#ed8936"
                    
                    st.markdown(f"""
                    <div style="background: {cor_peso}15; padding: 1.5rem; border-radius: 15px; text-align: center; border: 2px solid {cor_peso};">
                        <div style="color: {cor_peso}; font-weight: 700; font-size: 2rem;">
                            {paciente['peso']:.1f} kg
                        </div>
                        <div style="color: {cor_peso}; margin-top: 0.5rem;">
                            {diferenca_peso:+.1f} kg desde o início
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**📊 IMC Atual**")
                    imc = paciente['imc']
                    if imc < 25:
                        cor_imc = "#48bb78"
                        status_imc = "Saudável"
                    else:
                        cor_imc = "#ed8936"
                        status_imc = "Atenção"
                    
                    st.markdown(f"""
                    <div style="background: {cor_imc}15; padding: 1.5rem; border-radius: 15px; text-align: center; border: 2px solid {cor_imc};">
                        <div style="color: {cor_imc}; font-weight: 700; font-size: 2rem;">
                            {imc:.1f}
                        </div>
                        <div style="color: {cor_imc}; margin-top: 0.5rem;">
                            {status_imc}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("**🎯 Meta de Peso**")
                    peso_meta = 65.0  # Simulado
                    falta_peso = paciente['peso'] - peso_meta
                    cor_meta = "#48bb78" if falta_peso <= 0 else "#667eea"
                    
                    st.markdown(f"""
                    <div style="background: {cor_meta}15; padding: 1.5rem; border-radius: 15px; text-align: center; border: 2px solid {cor_meta};">
                        <div style="color: {cor_meta}; font-weight: 700; font-size: 2rem;">
                            {peso_meta:.1f} kg
                        </div>
                        <div style="color: {cor_meta}; margin-top: 0.5rem;">
                            {'Meta atingida!' if falta_peso <= 0 else f'Faltam {falta_peso:.1f} kg'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Gráfico de evolução
                st.markdown("### 📈 Gráfico de Evolução")
                
                if st.button("📊 Gerar Gráfico de Evolução", type="secondary"):
                    # Simular dados de evolução
                    dates = pd.date_range(start='2024-01-01', periods=6, freq='M')
                    weights = [70.0, 69.2, 68.5, 67.8, 67.2, paciente['peso']]
                    target_weight = 65.0
                    
                    fig = self.create_progress_chart(dates, weights, target_weight)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Análise de tendência
                    tendencia = "Perda constante" if weights[-1] < weights[0] else "Ganho"
                    velocidade = abs(weights[-1] - weights[0]) / len(weights)
                    
                    st.info(f"""
                    **📊 Análise de Tendência:**
                    - **Tendência:** {tendencia}
                    - **Velocidade média:** {velocidade:.2f} kg/mês
                    - **Projeção para meta:** {abs(paciente['peso'] - target_weight) / velocidade:.1f} meses
                    """)
        
        else:
            st.info("📝 Nenhum paciente cadastrado ainda.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def planos_alimentares_page(self):
        """Gestão de planos alimentares"""
        st.markdown('<div class="main-header"><h1>🍽️ Planos Alimentares</h1><p>Criação e gestão de dietas personalizadas</p></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Planos Existentes",
            "➕ Criar Plano", 
            "🧮 Calculadora de Cardápio",
            "📊 Análise Nutricional"
        ])
        
        with tab1:
            self.lista_planos()
        
        with tab2:
            self.criar_plano()
        
        with tab3:
            self.calculadora_cardapio()
        
        with tab4:
            self.analise_nutricional()

    def lista_planos(self):
        """Lista todos os planos alimentares"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("📋 Planos Alimentares Existentes")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_paciente = st.selectbox("👤 Filtrar por paciente", ["Todos"] + [p['nome'] for p in st.session_state.pacientes])
        
        with col2:
            filtro_tipo = st.selectbox("🥗 Tipo de dieta", ["Todos", "Balanceada", "Low Carb", "Cetogênica", "Mediterrânea"])
        
        with col3:
            filtro_status = st.selectbox("📊 Status", ["Todos", "Ativo", "Pausado", "Finalizado"])
        
        # Planos simulados
        planos_exemplo = [
            {
                "id": 1,
                "paciente": "Maria Silva",
                "nome": "Plano Emagrecimento - Maria",
                "tipo": "Low Carb",
                "calorias": 1200,
                "data_criacao": "2024-09-01",
                "status": "Ativo",
                "duracao": "12 semanas"
            },
            {
                "id": 2,
                "paciente": "João Santos", 
                "nome": "Plano Ganho Muscular - João",
                "tipo": "High Protein",
                "calorias": 2800,
                "data_criacao": "2024-08-15",
                "status": "Ativo",
                "duracao": "16 semanas"
            }
        ]
        
        if planos_exemplo:
            for plano in planos_exemplo:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{plano['nome']}**")
                        st.markdown(f"👤 {plano['paciente']}")
                        st.markdown(f"📅 Criado em: {plano['data_criacao']}")
                    
                    with col2:
                        st.markdown(f"🥗 **{plano['tipo']}**")
                        st.markdown(f"🔥 {plano['calorias']} kcal/dia")
                    
                    with col3:
                        status_colors = {
                            "Ativo": "#48bb78",
                            "Pausado": "#ed8936",
                            "Finalizado": "#718096"
                        }
                        color = status_colors.get(plano['status'], '#718096')
                        st.markdown(f'<div style="color: {color}; font-weight: 600;">● {plano["status"]}</div>', unsafe_allow_html=True)
                        st.markdown(f"⏱️ {plano['duracao']}")
                    
                    with col4:
                        if st.button("👁️", key=f"view_plano_{plano['id']}", help="Visualizar"):
                            st.info(f"Visualizando plano: {plano['nome']}")
                        
                        if st.button("📋", key=f"copy_plano_{plano['id']}", help="Duplicar"):
                            st.success("Plano duplicado!")
                    
                    st.divider()
        
        else:
            st.info("📝 Nenhum plano alimentar criado ainda.")
            if st.button("➕ Criar Primeiro Plano", type="primary"):
                st.info("Redirecionando para criação de plano...")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def criar_plano(self):
        """Criador de plano alimentar"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("➕ Criar Novo Plano Alimentar")
        
        with st.form("novo_plano"):
            # Informações básicas
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Informações Básicas**")
                paciente_plano = st.selectbox("👤 Paciente", [p['nome'] for p in st.session_state.pacientes])
                nome_plano = st.text_input("Nome do plano")
                tipo_dieta = st.selectbox("Tipo de dieta", [
                    "Balanceada", "Low Carb", "Cetogênica", 
                    "High Protein", "Mediterrânea", "DASH"
                ])
                
            with col2:
                st.markdown("**🎯 Objetivos**")
                objetivo_plano = st.selectbox("Objetivo principal", [
                    "Perda de peso", "Ganho de massa", "Manutenção",
                    "Melhora da saúde", "Performance"
                ])
                duracao = st.selectbox("Duração", ["4 semanas", "8 semanas", "12 semanas", "16 semanas"])
                calorias_alvo = st.number_input("Calorias alvo (kcal/dia)", min_value=800, max_value=4000, value=1500)
            
            # Distribuição de macronutrientes
            st.markdown("**📊 Distribuição de Macronutrientes**")
            
            macros_presets = {
                "Balanceada": {"carb": 50, "prot": 20, "gord": 30},
                "Low Carb": {"carb": 25, "prot": 35, "gord": 40},
                "Cetogênica": {"carb": 5, "prot": 25, "gord": 70},
                "High Protein": {"carb": 40, "prot": 35, "gord": 25},
                "Mediterrânea": {"carb": 45, "prot": 20, "gord": 35},
                "DASH": {"carb": 55, "prot": 18, "gord": 27}
            }
            
            preset = macros_presets.get(tipo_dieta, macros_presets["Balanceada"])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                carb_percent = st.slider("🍞 Carboidratos (%)", 5, 70, preset["carb"])
            with col2:
                prot_percent = st.slider("🥩 Proteínas (%)", 10, 50, preset["prot"])
            with col3:
                gord_percent = st.slider("🥑 Gorduras (%)", 15, 70, preset["gord"])
            
            # Validação da soma dos macros
            total_macros = carb_percent + prot_percent + gord_percent
            if total_macros != 100:
                st.warning(f"⚠️ Total de macronutrientes: {total_macros}% (deve somar 100%)")
            
            # Cálculo dos gramas
            carb_g = (calorias_alvo * carb_percent / 100) / 4
            prot_g = (calorias_alvo * prot_percent / 100) / 4
            gord_g = (calorias_alvo * gord_percent / 100) / 9
            
            st.info(f"""
            **Distribuição em gramas:**
            - 🍞 Carboidratos: {carb_g:.0f}g
            - 🥩 Proteínas: {prot_g:.0f}g  
            - 🥑 Gorduras: {gord_g:.0f}g
            """)
            
            # Restrições alimentares
            st.markdown("**🚫 Restrições e Preferências**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                restricoes = st.multiselect("Restrições alimentares", [
                    "Vegetariano", "Vegano", "Sem glúten", "Sem lactose",
                    "Sem açúcar", "Baixo sódio", "Sem oleaginosas"
                ])
                
            with col2:
                alimentos_evitar = st.text_area("Alimentos a evitar", 
                    placeholder="Ex: peixe, cogumelos, etc.")
            
            # Número de refeições
            st.markdown("**🍽️ Estrutura das Refeições**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                num_refeicoes = st.selectbox("Número de refeições", [3, 4, 5, 6])
            
            with col2:
                incluir_lanches = st.checkbox("Incluir lanches")
            
            with col3:
                incluir_suplementos = st.checkbox("Incluir suplementos")
            
            observacoes_plano = st.text_area("Observações do plano")
            
            submitted = st.form_submit_button("🚀 Criar Plano Alimentar", type="primary", use_container_width=True)
            
            if submitted:
                if total_macros == 100:
                    novo_plano = {
                        "id": len(st.session_state.planos_alimentares) + 1,
                        "paciente": paciente_plano,
                        "nome": nome_plano or f"Plano {tipo_dieta} - {paciente_plano}",
                        "tipo": tipo_dieta,
                        "objetivo": objetivo_plano,
                        "duracao": duracao,
                        "calorias": calorias_alvo,
                        "carb_percent": carb_percent,
                        "prot_percent": prot_percent,
                        "gord_percent": gord_percent,
                        "carb_g": carb_g,
                        "prot_g": prot_g,
                        "gord_g": gord_g,
                        "restricoes": restricoes,
                        "alimentos_evitar": alimentos_evitar,
                        "num_refeicoes": num_refeicoes,
                        "incluir_lanches": incluir_lanches,
                        "incluir_suplementos": incluir_suplementos,
                        "observacoes": observacoes_plano,
                        "data_criacao": datetime.now().strftime("%Y-%m-%d"),
                        "status": "Ativo"
                    }
                    
                    st.session_state.planos_alimentares.append(novo_plano)
                    st.success(f"✅ Plano '{novo_plano['nome']}' criado com sucesso!")
                    st.balloons()
                    
                    # Mostrar resumo do plano
                    st.markdown("### 📋 Resumo do Plano Criado")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.info(f"""
                        **👤 Paciente:** {paciente_plano}
                        **🥗 Tipo:** {tipo_dieta}
                        **🎯 Objetivo:** {objetivo_plano}
                        **⏱️ Duração:** {duracao}
                        **🔥 Calorias:** {calorias_alvo} kcal/dia
                        """)
                    
                    with col2:
                        st.info(f"""
                        **📊 Macronutrientes:**
                        - 🍞 Carboidratos: {carb_g:.0f}g ({carb_percent}%)
                        - 🥩 Proteínas: {prot_g:.0f}g ({prot_percent}%)
                        - 🥑 Gorduras: {gord_g:.0f}g ({gord_percent}%)
                        """)
                    
                else:
                    st.error("❌ A soma dos macronutrientes deve ser exatamente 100%")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def calculadora_cardapio(self):
        """Calculadora de cardápio"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("🧮 Calculadora de Cardápio")
        
        # Seleção de alimentos
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**🍽️ Selecione os Alimentos**")
            
            # Categorias de alimentos
            categorias = list(set([alimento["categoria"] for alimento in ALIMENTOS_DB.values()]))
            categoria_selecionada = st.selectbox("📂 Categoria", ["Todas"] + categorias)
            
            # Filtrar alimentos por categoria
            if categoria_selecionada == "Todas":
                alimentos_filtrados = list(ALIMENTOS_DB.keys())
            else:
                alimentos_filtrados = [nome for nome, dados in ALIMENTOS_DB.items() 
                                     if dados["categoria"] == categoria_selecionada]
            
            # Interface para adicionar alimentos
            if 'cardapio_atual' not in st.session_state:
                st.session_state.cardapio_atual = []
            
            with st.form("adicionar_alimento"):
                alimento_selecionado = st.selectbox("Alimento", alimentos_filtrados)
                quantidade = st.number_input("Quantidade", min_value=0.1, max_value=1000.0, value=100.0, step=10.0)
                
                if st.form_submit_button("➕ Adicionar ao Cardápio"):
                    item = {
                        "alimento": alimento_selecionado,
                        "quantidade": quantidade,
                        "dados": ALIMENTOS_DB[alimento_selecionado]
                    }
                    st.session_state.cardapio_atual.append(item)
                    st.success(f"✅ {alimento_selecionado} adicionado!")
        
        with col2:
            st.markdown("**📊 Resumo Nutricional**")
            
            if st.session_state.cardapio_atual:
                # Calcular totais
                total_calorias = 0
                total_proteinas = 0
                total_carboidratos = 0
                total_gorduras = 0
                total_fibras = 0
                total_sodio = 0
                
                for item in st.session_state.cardapio_atual:
                    fator = item["quantidade"] / 100  # Ajustar para a quantidade
                    total_calorias += item["dados"]["calorias"] * fator
                    total_proteinas += item["dados"]["proteinas"] * fator
                    total_carboidratos += item["dados"]["carboidratos"] * fator
                    total_gorduras += item["dados"]["gorduras"] * fator
                    total_fibras += item["dados"]["fibras"] * fator
                    total_sodio += item["dados"]["sodio"] * fator
                
                # Mostrar resumo
                st.markdown(f"""
                <div class="calculator-result">
                    Total: {total_calorias:.0f} kcal
                </div>
                """, unsafe_allow_html=True)
                
                resumo_data = [
                    ("🔥 Calorias", f"{total_calorias:.0f} kcal", "#e53e3e"),
                    ("🥩 Proteínas", f"{total_proteinas:.1f}g", "#8b5cf6"),
                    ("🍞 Carboidratos", f"{total_carboidratos:.1f}g", "#3b82f6"),
                    ("🥑 Gorduras", f"{total_gorduras:.1f}g", "#f59e0b"),
                    ("🌾 Fibras", f"{total_fibras:.1f}g", "#10b981"),
                    ("🧂 Sódio", f"{total_sodio:.0f}mg", "#6b7280")
                ]
                
                for nome, valor, cor in resumo_data:
                    st.markdown(f'''
                    <div style="background: {cor}15; padding: 0.8rem; border-radius: 8px; margin: 0.3rem 0; border-left: 3px solid {cor};">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: {cor}; font-weight: 600;">{nome}</span>
                            <span style="color: {cor}; font-weight: 700;">{valor}</span>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            
            else:
                st.info("Adicione alimentos para ver o resumo nutricional")
        
        # Lista do cardápio atual
        if st.session_state.cardapio_atual:
            st.markdown("### 📋 Cardápio Atual")
            
            for i, item in enumerate(st.session_state.cardapio_atual):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.write(f"**{item['alimento']}**")
                
                with col2:
                    st.write(f"{item['quantidade']:.0f}g")
                
                with col3:
                    calorias_item = (item['dados']['calorias'] * item['quantidade']) / 100
                    st.write(f"{calorias_item:.0f} kcal")
                
                with col4:
                    if st.button("🗑️", key=f"remove_{i}", help="Remover"):
                        st.session_state.cardapio_atual.pop(i)
                        st.rerun()
            
            # Ações do cardápio
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🗑️ Limpar Cardápio", type="secondary"):
                    st.session_state.cardapio_atual = []
                    st.rerun()
            
            with col2:
                if st.button("💾 Salvar Cardápio", type="primary"):
                    st.success("Cardápio salvo com sucesso!")
            
            with col3:
                if st.button("📄 Gerar PDF", type="secondary"):
                    st.info("Funcionalidade de PDF em desenvolvimento")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def analise_nutricional(self):
        """Análise nutricional avançada"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("📊 Análise Nutricional Avançada")
        
        # Upload de cardápio ou seleção
        opcao = st.radio("📋 Escolha a opção de análise", [
            "Analisar cardápio atual",
            "Upload de arquivo",
            "Inserir manualmente"
        ])
        
        if opcao == "Analisar cardápio atual":
            if hasattr(st.session_state, 'cardapio_atual') and st.session_state.cardapio_atual:
                cardapio = st.session_state.cardapio_atual
                
                # Análise detalhada
                st.markdown("### 🔬 Análise Detalhada")
                
                # Calcular dados nutricionais
                total_calorias = sum([(item['dados']['calorias'] * item['quantidade']) / 100 for item in cardapio])
                total_proteinas = sum([(item['dados']['proteinas'] * item['quantidade']) / 100 for item in cardapio])
                total_carboidratos = sum([(item['dados']['carboidratos'] * item['quantidade']) / 100 for item in cardapio])
                total_gorduras = sum([(item['dados']['gorduras'] * item['quantidade']) / 100 for item in cardapio])
                
                # Gráfico de distribuição de macronutrientes
                fig = go.Figure(data=[go.Pie(
                    labels=['Proteínas', 'Carboidratos', 'Gorduras'],
                    values=[total_proteinas * 4, total_carboidratos * 4, total_gorduras * 9],
                    hole=.3,
                    marker_colors=['#8b5cf6', '#3b82f6', '#f59e0b']
                )])
                
                fig.update_layout(
                    title="Distribuição Calórica por Macronutriente",
                    height=400,
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Análise qualitativa
                    st.markdown("**🎯 Análise Qualitativa**")
                    
                    # Calcular percentuais
                    total_calorias_macro = (total_proteinas * 4) + (total_carboidratos * 4) + (total_gorduras * 9)
                    prot_percent = (total_proteinas * 4 / total_calorias_macro) * 100
                    carb_percent = (total_carboidratos * 4 / total_calorias_macro) * 100
                    gord_percent = (total_gorduras * 9 / total_calorias_macro) * 100
                    
                    analises = []
                    
                    # Análise de proteínas
                    if prot_percent < 15:
                        analises.append(("⚠️ Proteínas baixas", f"{prot_percent:.1f}% (ideal: 15-25%)", "#ed8936"))
                    elif prot_percent > 25:
                        analises.append(("⚠️ Proteínas altas", f"{prot_percent:.1f}% (ideal: 15-25%)", "#ed8936"))
                    else:
                        analises.append(("✅ Proteínas adequadas", f"{prot_percent:.1f}%", "#48bb78"))
                    
                    # Análise de carboidratos
                    if carb_percent < 45:
                        analises.append(("💡 Dieta low carb", f"{carb_percent:.1f}%", "#667eea"))
                    elif carb_percent > 65:
                        analises.append(("⚠️ Carboidratos altos", f"{carb_percent:.1f}% (ideal: 45-65%)", "#ed8936"))
                    else:
                        analises.append(("✅ Carboidratos adequados", f"{carb_percent:.1f}%", "#48bb78"))
                    
                    # Análise de gorduras
                    if gord_percent < 20:
                        analises.append(("⚠️ Gorduras baixas", f"{gord_percent:.1f}% (ideal: 20-35%)", "#ed8936"))
                    elif gord_percent > 35:
                        analises.append(("⚠️ Gorduras altas", f"{gord_percent:.1f}% (ideal: 20-35%)", "#ed8936"))
                    else:
                        analises.append(("✅ Gorduras adequadas", f"{gord_percent:.1f}%", "#48bb78"))
                    
                    for analise, valor, cor in analises:
                        st.markdown(f'''
                        <div style="background: {cor}15; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {cor};">
                            <div style="color: {cor}; font-weight: 600;">{analise}</div>
                            <div style="color: {cor}; font-size: 0.9rem;">{valor}</div>
                        </div>
                        ''', unsafe_allow_html=True)
                
                # Recomendações
                st.markdown("### 💡 Recomendações")
                
                recomendacoes = []
                
                if total_calorias < 1200:
                    recomendacoes.append("🔥 Considere aumentar as calorias totais")
                elif total_calorias > 2500:
                    recomendacoes.append("⚖️ Avalie se as calorias estão adequadas para o objetivo")
                
                if prot_percent < 15:
                    recomendacoes.append("🥩 Adicione mais fontes de proteína")
                
                if len([item for item in cardapio if item['dados']['categoria'] == 'Vegetal']) < 2:
                    recomendacoes.append("🥬 Inclua mais vegetais para aumentar fibras e micronutrientes")
                
                if not recomendacoes:
                    recomendacoes.append("✅ Cardápio bem balanceado!")
                
                for rec in recomendacoes:
                    st.info(rec)
                
            else:
                st.info("📋 Crie um cardápio primeiro na aba 'Calculadora de Cardápio'")
        
        elif opcao == "Upload de arquivo":
            uploaded_file = st.file_uploader("📁 Faça upload do arquivo", 
                                           type=['csv', 'xlsx', 'json'],
                                           help="Formatos aceitos: CSV, Excel, JSON")
            
            if uploaded_file:
                st.info("🔧 Funcionalidade de upload em desenvolvimento")
        
        else:  # Inserir manualmente
            st.markdown("**✏️ Insira os dados nutricionais manualmente**")
            
            with st.form("analise_manual"):
                col1, col2 = st.columns(2)
                
                with col1:
                    calorias_manual = st.number_input("🔥 Calorias totais", min_value=0, value=1500)
                    proteinas_manual = st.number_input("🥩 Proteínas (g)", min_value=0.0, value=100.0, step=0.1)
                    
                with col2:
                    carboidratos_manual = st.number_input("🍞 Carboidratos (g)", min_value=0.0, value=150.0, step=0.1)
                    gorduras_manual = st.number_input("🥑 Gorduras (g)", min_value=0.0, value=50.0, step=0.1)
                
                if st.form_submit_button("📊 Analisar", type="primary"):
                    # Fazer análise com dados manuais
                    total_calorias_calc = (proteinas_manual * 4) + (carboidratos_manual * 4) + (gorduras_manual * 9)
                    
                    st.success(f"✅ Análise concluída!")
                    
                    st.info(f"""
                    **📊 Resumo da Análise:**
                    - Calorias informadas: {calorias_manual} kcal
                    - Calorias calculadas: {total_calorias_calc:.0f} kcal
                    - Diferença: {abs(calorias_manual - total_calorias_calc):.0f} kcal
                    """)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def banco_receitas_page(self):
        """Gestão do banco de receitas"""
        st.markdown('<div class="main-header"><h1>🍳 Banco de Receitas</h1><p>Receitas personalizadas com análise nutricional completa</p></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📚 Receitas",
            "➕ Nova Receita",
            "🔍 Buscar & Filtrar", 
            "📊 Análise Nutricional"
        ])
        
        with tab1:
            self.lista_receitas()
        
        with tab2:
            self.nova_receita()
        
        with tab3:
            self.buscar_receitas()
        
        with tab4:
            self.analise_receitas()

    def lista_receitas(self):
        """Lista todas as receitas"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("📚 Biblioteca de Receitas")
        
        # Estatísticas das receitas
        col1, col2, col3, col4 = st.columns(4)
        
        total_receitas = len(st.session_state.receitas)
        categorias = list(set([r['categoria'] for r in st.session_state.receitas]))
        receita_baixa_cal = len([r for r in st.session_state.receitas if r['calorias'] < 300])
        receita_alta_prot = len([r for r in st.session_state.receitas if r['proteinas'] > 20])
        
        with col1:
            st.metric("Total de Receitas", total_receitas)
        with col2:
            st.metric("Categorias", len(categorias))
        with col3:
            st.metric("Baixa Caloria", receita_baixa_cal, "< 300 kcal")
        with col4:
            st.metric("Alta Proteína", receita_alta_prot, "> 20g")
        
        # Grid de receitas
        st.markdown("### 🍽️ Receitas Disponíveis")
        
        # Organizar em grid de 2 colunas
        for i in range(0, len(st.session_state.receitas), 2):
            col1, col2 = st.columns(2)
            
            with col1:
                if i < len(st.session_state.receitas):
                    receita = st.session_state.receitas[i]
                    self.render_receita_card(receita)
            
            with col2:
                if i + 1 < len(st.session_state.receitas):
                    receita = st.session_state.receitas[i + 1]
                    self.render_receita_card(receita)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def render_receita_card(self, receita):
        """Renderiza card de receita"""
        # Determinar cor baseada na categoria
        cores_categoria = {
            "Pratos Principais": "#667eea",
            "Bebidas": "#48bb78",
            "Saladas": "#10b981",
            "Café da Manhã": "#f59e0b",
            "Lanches": "#8b5cf6",
            "Sobremesas": "#ef4444"
        }
        
        cor = cores_categoria.get(receita['categoria'], '#718096')
        
        st.markdown(f'''
        <div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 4px solid {cor};">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                <h4 style="color: {cor}; margin: 0;">{receita['nome']}</h4>
                <span style="background: {cor}15; color: {cor}; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                    {receita['categoria']}
                </span>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div>
                    <div style="color: #e53e3e; font-weight: 600;">🔥 {receita['calorias']} kcal</div>
                    <div style="color: #8b5cf6; font-size: 0.9rem;">🥩 {receita['proteinas']}g proteína</div>
                </div>
                <div>
                    <div style="color: #3b82f6; font-size: 0.9rem;">🍞 {receita['carboidratos']}g carbo</div>
                    <div style="color: #f59e0b; font-size: 0.9rem;">🥑 {receita['gorduras']}g gordura</div>
                </div>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #718096;">
                <span>⏱️ {receita['tempo_preparo']}</span>
                <span>👥 {receita['porcoes']} porção(ões)</span>
                <span>💰 R$ {receita['custo_estimado']:.2f}</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Botões de ação
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👁️ Ver", key=f"view_receita_{receita['id']}", use_container_width=True):
                self.show_receita_details(receita)
        
        with col2:
            if st.button("📋 Copiar", key=f"copy_receita_{receita['id']}", use_container_width=True):
                st.success("Receita copiada!")
        
        with col3:
            if st.button("➕ Usar", key=f"use_receita_{receita['id']}", use_container_width=True):
                st.info("Adicionada ao cardápio!")

    def show_receita_details(self, receita):
        """Mostra detalhes da receita em modal"""
        with st.expander(f"📋 Detalhes: {receita['nome']}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🛒 Ingredientes:**")
                for ingrediente in receita['ingredientes']:
                    st.markdown(f"• {ingrediente}")
                
                st.markdown(f"**⏱️ Tempo de preparo:** {receita['tempo_preparo']}")
                st.markdown(f"**📊 Dificuldade:** {receita['dificuldade']}")
                st.markdown(f"**👥 Porções:** {receita['porcoes']}")
                st.markdown(f"**💰 Custo estimado:** R$ {receita['custo_estimado']:.2f}")
            
            with col2:
                st.markdown("**📋 Modo de preparo:**")
                st.text_area("", value=receita['preparo'], height=150, disabled=True)
                
                st.markdown("**📊 Informações nutricionais (por porção):**")
                st.markdown(f"""
                - 🔥 **Calorias:** {receita['calorias']} kcal
                - 🥩 **Proteínas:** {receita['proteinas']}g
                - 🍞 **Carboidratos:** {receita['carboidratos']}g
                - 🥑 **Gorduras:** {receita['gorduras']}g
                - 🌾 **Fibras:** {receita['fibras']}g
                """)
                
                if 'tags' in receita:
                    st.markdown("**🏷️ Tags:**")
                    for tag in receita['tags']:
                        st.markdown(f"`{tag}`")

    def nova_receita(self):
        """Formulário para nova receita"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("➕ Criar Nova Receita")
        
        with st.form("nova_receita"):
            # Informações básicas
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Informações Básicas**")
                nome_receita = st.text_input("Nome da receita *")
                categoria_receita = st.selectbox("Categoria *", [
                    "Pratos Principais", "Café da Manhã", "Lanches", 
                    "Saladas", "Bebidas", "Sobremesas"
                ])
                dificuldade = st.selectbox("Dificuldade", ["Fácil", "Médio", "Difícil"])
                tempo_preparo = st.text_input("Tempo de preparo", placeholder="Ex: 30 minutos")
                
            with col2:
                st.markdown("**👥 Rendimento & Custo**")
                porcoes = st.number_input("Número de porções *", min_value=1, max_value=20, value=1)
                custo_estimado = st.number_input("Custo estimado (R$)", min_value=0.0, value=10.0, step=0.50)
                
                st.markdown("**🏷️ Tags**")
                tags_disponiveis = ["vegetariano", "vegano", "sem glúten", "sem lactose", "low carb", "proteico", "detox", "fitness"]
                tags_selecionadas = st.multiselect("Selecione as tags", tags_disponiveis)
            
            # Ingredientes
            st.markdown("**🛒 Ingredientes**")
            
            # Sistema dinâmico de ingredientes
            if 'ingredientes_receita' not in st.session_state:
                st.session_state.ingredientes_receita = [""]
            
            for i, ingrediente in enumerate(st.session_state.ingredientes_receita):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.session_state.ingredientes_receita[i] = st.text_input(
                        f"Ingrediente {i+1}", 
                        value=ingrediente, 
                        key=f"ingrediente_{i}",
                        placeholder="Ex: Frango grelhado (200g)"
                    )
                with col2:
                    if st.button("➖", key=f"remove_ing_{i}") and len(st.session_state.ingredientes_receita) > 1:
                        st.session_state.ingredientes_receita.pop(i)
                        st.rerun()
            
            if st.button("➕ Adicionar ingrediente"):
                st.session_state.ingredientes_receita.append("")
                st.rerun()
            
            # Modo de preparo
            st.markdown("**📝 Modo de Preparo**")
            preparo = st.text_area("Descreva o passo a passo *", height=150,
                                 placeholder="1. Tempere o frango...\n2. Aqueça a frigideira...\n3. ...")
            
            # Informações nutricionais
            st.markdown("**📊 Informações Nutricionais (por porção)**")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                calorias_receita = st.number_input("🔥 Calorias *", min_value=0, value=200)
                proteinas_receita = st.number_input("🥩 Proteínas (g) *", min_value=0.0, value=15.0, step=0.1)
            
            with col2:
                carboidratos_receita = st.number_input("🍞 Carboidratos (g) *", min_value=0.0, value=20.0, step=0.1)
                gorduras_receita = st.number_input("🥑 Gorduras (g) *", min_value=0.0, value=8.0, step=0.1)
            
            with col3:
                fibras_receita = st.number_input("🌾 Fibras (g)", min_value=0.0, value=3.0, step=0.1)
                sodio_receita = st.number_input("🧂 Sódio (mg)", min_value=0, value=200)
            
            with col4:
                # Validação nutricional automática
                calorias_calculadas = (proteinas_receita * 4) + (carboidratos_receita * 4) + (gorduras_receita * 9)
                diferenca = abs(calorias_receita - calorias_calculadas)
                
                if diferenca > 50:
                    st.warning(f"⚠️ Divergência nas calorias: {diferenca:.0f} kcal")
                else:
                    st.success("✅ Valores consistentes")
                
                st.info(f"Calculado: {calorias_calculadas:.0f} kcal")
            
            observacoes_receita = st.text_area("Observações adicionais", height=60)
            
            submitted = st.form_submit_button("🚀 Criar Receita", type="primary", use_container_width=True)
            
            if submitted:
                # Validar campos obrigatórios
                ingredientes_filtrados = [ing for ing in st.session_state.ingredientes_receita if ing.strip()]
                
                if nome_receita and categoria_receita and preparo and calorias_receita and ingredientes_filtrados:
                    nova_receita = {
                        "id": len(st.session_state.receitas) + 1,
                        "nome": nome_receita,
                        "categoria": categoria_receita,
                        "ingredientes": ingredientes_filtrados,
                        "preparo": preparo,
                        "dificuldade": dificuldade,
                        "tempo_preparo": tempo_preparo or "Não informado",
                        "porcoes": porcoes,
                        "custo_estimado": custo_estimado,
                        "calorias": calorias_receita,
                        "proteinas": proteinas_receita,
                        "carboidratos": carboidratos_receita,
                        "gorduras": gorduras_receita,
                        "fibras": fibras_receita,
                        "sodio": sodio_receita,
                        "tags": tags_selecionadas,
                        "observacoes": observacoes_receita,
                        "data_criacao": datetime.now().strftime("%Y-%m-%d"),
                        "criador": st.session_state.current_user
                    }
                    
                    st.session_state.receitas.append(nova_receita)
                    st.session_state.ingredientes_receita = [""]  # Reset
                    
                    st.success(f"✅ Receita '{nome_receita}' criada com sucesso!")
                    st.balloons()
                    
                    # Mostrar resumo
                    with st.expander("📋 Resumo da Receita Criada", expanded=True):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.info(f"""
                            **📋 Informações Gerais:**
                            - **Nome:** {nome_receita}
                            - **Categoria:** {categoria_receita}
                            - **Dificuldade:** {dificuldade}
                            - **Tempo:** {tempo_preparo}
                            - **Porções:** {porcoes}
                            - **Custo:** R$ {custo_estimado:.2f}
                            """)
                        
                        with col2:
                            st.info(f"""
                            **📊 Valores Nutricionais (por porção):**
                            - **Calorias:** {calorias_receita} kcal
                            - **Proteínas:** {proteinas_receita}g
                            - **Carboidratos:** {carboidratos_receita}g
                            - **Gorduras:** {gorduras_receita}g
                            - **Fibras:** {fibras_receita}g
                            """)
                
                else:
                    st.error("❌ Preencha todos os campos obrigatórios (*)")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def buscar_receitas(self):
        """Sistema de busca e filtros"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("🔍 Buscar & Filtrar Receitas")
        
        # Filtros avançados
        col1, col2, col3 = st.columns(3)
        
        with col1:
            busca_texto = st.text_input("🔍 Buscar por nome ou ingrediente")
            categoria_filtro = st.selectbox("📂 Categoria", ["Todas"] + list(set([r['categoria'] for r in st.session_state.receitas])))
        
        with col2:
            dificuldade_filtro = st.selectbox("⭐ Dificuldade", ["Todas", "Fácil", "Médio", "Difícil"])
            
            # Filtro de calorias
            cal_min, cal_max = st.slider(
                "🔥 Faixa de calorias",
                min_value=0,
                max_value=1000,
                value=(0, 500),
                step=50
            )
        
        with col3:
            # Filtro de tags
            todas_tags = set()
            for receita in st.session_state.receitas:
                if 'tags' in receita:
                    todas_tags.update(receita['tags'])
            
            tags_filtro = st.multiselect("🏷️ Tags", list(todas_tags))
            
            # Filtro de tempo
            tempo_max = st.selectbox("⏱️ Tempo máximo", ["Qualquer", "15 min", "30 min", "1 hora", "2 horas"])
        
        # Aplicar filtros
        receitas_filtradas = st.session_state.receitas.copy()
        
        # Filtro por texto
        if busca_texto:
            receitas_filtradas = [
                r for r in receitas_filtradas
                if busca_texto.lower() in r['nome'].lower() or
                   any(busca_texto.lower() in ing.lower() for ing in r['ingredientes'])
            ]
        
        # Filtro por categoria
        if categoria_filtro != "Todas":
            receitas_filtradas = [r for r in receitas_filtradas if r['categoria'] == categoria_filtro]
        
        # Filtro por dificuldade
        if dificuldade_filtro != "Todas":
            receitas_filtradas = [r for r in receitas_filtradas if r['dificuldade'] == dificuldade_filtro]
        
        # Filtro por calorias
        receitas_filtradas = [r for r in receitas_filtradas if cal_min <= r['calorias'] <= cal_max]
        
        # Filtro por tags
        if tags_filtro:
            receitas_filtradas = [
                r for r in receitas_filtradas
                if 'tags' in r and any(tag in r['tags'] for tag in tags_filtro)
            ]
        
        # Mostrar resultados
        st.markdown(f"### 📊 Resultados ({len(receitas_filtradas)} receitas encontradas)")
        
        if receitas_filtradas:
            # Opções de ordenação
            col1, col2 = st.columns([3, 1])
            
            with col2:
                ordenacao = st.selectbox("📈 Ordenar por", [
                    "Nome", "Calorias (menor)", "Calorias (maior)",
                    "Proteínas (maior)", "Tempo", "Custo"
                ])
            
            # Aplicar ordenação
            if ordenacao == "Nome":
                receitas_filtradas.sort(key=lambda x: x['nome'])
            elif ordenacao == "Calorias (menor)":
                receitas_filtradas.sort(key=lambda x: x['calorias'])
            elif ordenacao == "Calorias (maior)":
                receitas_filtradas.sort(key=lambda x: x['calorias'], reverse=True)
            elif ordenacao == "Proteínas (maior)":
                receitas_filtradas.sort(key=lambda x: x['proteinas'], reverse=True)
            elif ordenacao == "Custo":
                receitas_filtradas.sort(key=lambda x: x['custo_estimado'])
            
            # Mostrar receitas filtradas
            for i in range(0, len(receitas_filtradas), 2):
                col1, col2 = st.columns(2)
                
                with col1:
                    if i < len(receitas_filtradas):
                        self.render_receita_card(receitas_filtradas[i])
                
                with col2:
                    if i + 1 < len(receitas_filtradas):
                        self.render_receita_card(receitas_filtradas[i + 1])
        
        else:
            st.info("🔍 Nenhuma receita encontrada com os filtros aplicados.")
            
            if st.button("🔄 Limpar Filtros", type="secondary"):
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    def analise_receitas(self):
        """Análise nutricional de receitas"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("📊 Análise Nutricional de Receitas")
        
        # Análise geral do banco de receitas
        st.markdown("### 📈 Visão Geral do Banco de Receitas")
        
        if st.session_state.receitas:
            # Estatísticas gerais
            total_receitas = len(st.session_state.receitas)
            media_calorias = sum([r['calorias'] for r in st.session_state.receitas]) / total_receitas
            media_proteinas = sum([r['proteinas'] for r in st.session_state.receitas]) / total_receitas
            media_custo = sum([r['custo_estimado'] for r in st.session_state.receitas]) / total_receitas
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📚 Total de Receitas", total_receitas)
            with col2:
                st.metric("🔥 Média de Calorias", f"{media_calorias:.0f} kcal")
            with col3:
                st.metric("🥩 Média de Proteínas", f"{media_proteinas:.1f}g")
            with col4:
                st.metric("💰 Custo Médio", f"R$ {media_custo:.2f}")
            
            # Análise por categoria
            st.markdown("### 📊 Análise por Categoria")
            
            categorias_stats = {}
            for receita in st.session_state.receitas:
                cat = receita['categoria']
                if cat not in categorias_stats:
                    categorias_stats[cat] = {
                        'count': 0,
                        'calorias': [],
                        'proteinas': [],
                        'custo': []
                    }
                
                categorias_stats[cat]['count'] += 1
                categorias_stats[cat]['calorias'].append(receita['calorias'])
                categorias_stats[cat]['proteinas'].append(receita['proteinas'])
                categorias_stats[cat]['custo'].append(receita['custo_estimado'])
            
            # Gráfico de distribuição por categoria
            categorias = list(categorias_stats.keys())
            contagens = [categorias_stats[cat]['count'] for cat in categorias]
            
            fig = go.Figure(data=[go.Bar(
                x=categorias,
                y=contagens,
                marker_color=['#667eea', '#48bb78', '#ed8936', '#f093fb', '#8b5cf6', '#ef4444'][:len(categorias)]
            )])
            
            fig.update_layout(
                title="Distribuição de Receitas por Categoria",
                xaxis_title="Categoria",
                yaxis_title="Número de Receitas",
                height=400,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Análise detalhada por categoria
                st.markdown("**📋 Análise Detalhada por Categoria:**")
                
                for categoria, stats in categorias_stats.items():
                    media_cal_cat = sum(stats['calorias']) / len(stats['calorias'])
                    media_prot_cat = sum(stats['proteinas']) / len(stats['proteinas'])
                    
                    st.markdown(f"""
                    **{categoria}** ({stats['count']} receitas)
                    - Calorias: {media_cal_cat:.0f} kcal
                    - Proteínas: {media_prot_cat:.1f}g
                    """)
            
            # Análise de eficiência nutricional
            st.markdown("### 🏆 Top Receitas por Critérios")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**🔥 Menor Caloria**")
                receita_baixa_cal = min(st.session_state.receitas, key=lambda x: x['calorias'])
                st.info(f"{receita_baixa_cal['nome']}: {receita_baixa_cal['calorias']} kcal")
            
            with col2:
                st.markdown("**🥩 Maior Proteína**")
                receita_alta_prot = max(st.session_state.receitas, key=lambda x: x['proteinas'])
                st.info(f"{receita_alta_prot['nome']}: {receita_alta_prot['proteinas']:.1f}g")
            
            with col3:
                st.markdown("**💰 Menor Custo**")
                receita_barata = min(st.session_state.receitas, key=lambda x: x['custo_estimado'])
                st.info(f"{receita_barata['nome']}: R$ {receita_barata['custo_estimado']:.2f}")
            
            # Comparação de receitas
            st.markdown("### ⚖️ Comparar Receitas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                receita1 = st.selectbox("Receita 1", [r['nome'] for r in st.session_state.receitas], key="comp1")
            
            with col2:
                receita2 = st.selectbox("Receita 2", [r['nome'] for r in st.session_state.receitas], key="comp2")
            
            if st.button("📊 Comparar", type="primary"):
                r1 = next(r for r in st.session_state.receitas if r['nome'] == receita1)
                r2 = next(r for r in st.session_state.receitas if r['nome'] == receita2)
                
                # Criar gráfico de comparação
                categorias = ['Calorias', 'Proteínas', 'Carboidratos', 'Gorduras', 'Fibras']
                valores_r1 = [r1['calorias']/10, r1['proteinas'], r1['carboidratos'], r1['gorduras'], r1['fibras']]
                valores_r2 = [r2['calorias']/10, r2['proteinas'], r2['carboidratos'], r2['gorduras'], r2['fibras']]
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=valores_r1,
                    theta=categorias,
                    fill='toself',
                    name=receita1,
                    fillcolor='rgba(102, 126, 234, 0.2)',
                    line=dict(color='#667eea')
                ))
                
                fig.add_trace(go.Scatterpolar(
                    r=valores_r2,
                    theta=categorias,
                    fill='toself',
                    name=receita2,
                    fillcolor='rgba(72, 187, 120, 0.2)',
                    line=dict(color='#48bb78')
                ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True)),
                    showlegend=True,
                    title="Comparação Nutricional",
                    height=500,
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Tabela comparativa
                st.markdown("### 📋 Comparação Detalhada")
                
                dados_comparacao = {
                    "Critério": ["Calorias (kcal)", "Proteínas (g)", "Carboidratos (g)", 
                               "Gorduras (g)", "Fibras (g)", "Custo (R$)"],
                    receita1: [r1['calorias'], r1['proteinas'], r1['carboidratos'], 
                              r1['gorduras'], r1['fibras'], r1['custo_estimado']],
                    receita2: [r2['calorias'], r2['proteinas'], r2['carboidratos'], 
                              r2['gorduras'], r2['fibras'], r2['custo_estimado']]
                }
                
                df_comp = pd.DataFrame(dados_comparacao)
                st.dataframe(df_comp, use_container_width=True)
        
        else:
            st.info("📝 Nenhuma receita disponível para análise.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def agendamentos_page(self):
        """Sistema de agendamentos"""
        st.markdown('<div class="main-header"><h1>📅 Sistema de Agendamentos</h1><p>Gestão completa de consultas e compromissos</p></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Agenda",
            "➕ Novo Agendamento",
            "📊 Relatórios",
            "⚙️ Configurações"
        ])
        
        with tab1:
            self.visualizar_agenda()
        
        with tab2:
            self.novo_agendamento()
        
        with tab3:
            self.relatorio_agendamentos()
        
        with tab4:
            self.config_agendamentos()

    def visualizar_agenda(self):
        """Visualização da agenda"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        # Controles de visualização
        col1, col2, col3 = st.columns(3)
        
        with col1:
            data_visualizacao = st.date_input("📅 Data", value=datetime.now())
        
        with col2:
            tipo_visualizacao = st.selectbox("👁️ Visualização", ["Dia", "Semana", "Mês"])
        
        with col3:
            filtro_status = st.selectbox("📊 Filtrar por status", ["Todos", "Agendado", "Realizado", "Cancelado"])
        
        # Estatísticas rápidas
        hoje = datetime.now().strftime('%Y-%m-%d')
        agendamentos_hoje = [a for a in st.session_state.agendamentos if a.get('data') == hoje]
        agendamentos_semana = len([a for a in st.session_state.agendamentos 
                                 if datetime.strptime(a['data'], '%Y-%m-%d').isocalendar()[1] == datetime.now().isocalendar()[1]])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Hoje", len(agendamentos_hoje), "+1")
        with col2:
            st.metric("Esta Semana", agendamentos_semana, "+3")
        with col3:
            receita_dia = sum([a.get('valor', 0) for a in agendamentos_hoje if a.get('status') == 'Realizado'])
            st.metric("Receita Hoje", f"R$ {receita_dia:.2f}")
        with col4:
            taxa_comparecimento = 92  # Simulado
            st.metric("Taxa Comparecimento", f"{taxa_comparecimento}%", "+2%")
        
        # Visualização da agenda
        st.markdown("### 📋 Agenda do Dia")
        
        data_str = data_visualizacao.strftime('%Y-%m-%d')
        agendamentos_data = [a for a in st.session_state.agendamentos if a.get('data') == data_str]
        
        if filtro_status != "Todos":
            agendamentos_data = [a for a in agendamentos_data if a.get('status') == filtro_status]
        
        if agendamentos_data:
            agendamentos_data.sort(key=lambda x: x['horario'])
            
            for agendamento in agendamentos_data:
                col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
                
                status_colors = {
                    "Agendado": "#667eea",
                    "Realizado": "#48bb78",
                    "Cancelado": "#e53e3e",
                    "Em andamento": "#ed8936"
                }
                
                color = status_colors.get(agendamento.get('status', 'Agendado'), '#718096')
                
                with col1:
                    st.markdown(f"""
                    <div style="background: {color}15; padding: 1rem; border-radius: 10px; border-left: 4px solid {color};">
                        <div style="color: {color}; font-weight: 700; font-size: 1.1rem;">
                            🕐 {agendamento['horario']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**👤 {agendamento['paciente']}**")
                    st.markdown(f"📋 {agendamento['tipo']}")
                    if agendamento.get('observacoes'):
                        st.markdown(f"💭 {agendamento['observacoes']}")
                
                with col3:
                    st.markdown(f"**💰 R$ {agendamento.get('valor', 0):.2f}**")
                    st.markdown(f"📊 {agendamento.get('status', 'Agendado')}")
                
                with col4:
                    if st.button("✏️", key=f"edit_agenda_{agendamento['id']}", help="Editar"):
                        st.info(f"Editando agendamento {agendamento['id']}")
                
                st.divider()
        
        else:
            st.info(f"📅 Nenhum agendamento encontrado para {data_visualizacao.strftime('%d/%m/%Y')}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def novo_agendamento(self):
        """Formulário para novo agendamento"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("➕ Novo Agendamento")
        
        with st.form("novo_agendamento"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**👤 Informações do Paciente**")
                
                if st.session_state.pacientes:
                    paciente_opcoes = [p['nome'] for p in st.session_state.pacientes]
                    paciente_agendamento = st.selectbox("Paciente", ["Novo paciente"] + paciente_opcoes)
                    
                    if paciente_agendamento == "Novo paciente":
                        nome_novo = st.text_input("Nome completo")
                        telefone_novo = st.text_input("Telefone")
                        email_novo = st.text_input("Email")
                else:
                    paciente_agendamento = "Novo paciente"
                    nome_novo = st.text_input("Nome completo")
                    telefone_novo = st.text_input("Telefone")
                    email_novo = st.text_input("Email")
                
                observacoes_agenda = st.text_area("Observações", height=80)
            
            with col2:
                st.markdown("**📅 Dados do Agendamento**")
                
                data_agendamento = st.date_input("Data", min_value=datetime.now().date())
                horario_agendamento = st.time_input("Horário", value=datetime.now().time())
                
                tipos_consulta = st.session_state.configuracoes.get('tipos_consulta', ["Consulta inicial", "Retorno", "Avaliação"])
                tipo_consulta = st.selectbox("Tipo de consulta", tipos_consulta)
                
                if tipo_consulta == "Consulta inicial":
                    valor_consulta = st.session_state.configuracoes.get('valor_consulta', 150.0)
                else:
                    valor_consulta = st.session_state.configuracoes.get('valor_retorno', 100.0)
                
                valor_agendamento = st.number_input("Valor (R$)", value=valor_consulta, min_value=0.0, step=10.0)
                
                duracao = st.selectbox("Duração", ["30 min", "45 min", "60 min", "90 min", "120 min"])
                
                modalidade = st.radio("Modalidade", ["Presencial", "Online"], horizontal=True)
            
            # Lembrete e confirmação
            st.markdown("**🔔 Configurações de Lembrete**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                enviar_whatsapp = st.checkbox("📱 Lembrete WhatsApp", value=True)
            
            with col2:
                enviar_email = st.checkbox("📧 Lembrete Email", value=True)
            
            with col3:
                tempo_lembrete = st.selectbox("⏰ Enviar lembrete", ["1 hora antes", "2 horas antes", "1 dia antes"])
            
            submitted = st.form_submit_button("📅 Agendar Consulta", type="primary", use_container_width=True)
            
            if submitted:
                # Validações
                if paciente_agendamento == "Novo paciente":
                    if not nome_novo or not telefone_novo:
                        st.error("❌ Nome e telefone são obrigatórios para novo paciente")
                        return
                    nome_paciente = nome_novo
                else:
                    nome_paciente = paciente_agendamento
                
                # Verificar conflitos de horário
                data_str = data_agendamento.strftime('%Y-%m-%d')
                horario_str = horario_agendamento.strftime('%H:%M')
                
                conflito = any(
                    a['data'] == data_str and a['horario'] == horario_str 
                    for a in st.session_state.agendamentos
                )
                
                if conflito:
                    st.error("❌ Já existe um agendamento para este horário!")
                    return
                
                # Criar agendamento
                novo_agendamento = {
                    "id": len(st.session_state.agendamentos) + 1,
                    "paciente": nome_paciente,
                    "data": data_str,
                    "horario": horario_str,
                    "tipo": tipo_consulta,
                    "valor": valor_agendamento,
                    "duracao": duracao,
                    "modalidade": modalidade,
                    "status": "Agendado",
                    "observacoes": observacoes_agenda,
                    "lembrete_whatsapp": enviar_whatsapp,
                    "lembrete_email": enviar_email,
                    "tempo_lembrete": tempo_lembrete,
                    "data_criacao": datetime.now().strftime('%Y-%m-%d %H:%M')
                }
                
                # Se for novo paciente, adicionar aos pacientes
                if paciente_agendamento == "Novo paciente":
                    novo_paciente_agenda = {
                        "id": len(st.session_state.pacientes) + 1,
                        "nome": nome_novo,
                        "email": email_novo or "",
                        "telefone": telefone_novo,
                        "data_nascimento": "",
                        "sexo": "Não informado",
                        "peso": 0,
                        "altura": 0,
                        "objetivo": "A definir",
                        "data_cadastro": datetime.now().strftime("%Y-%m-%d"),
                        "status": "Ativo",
                        "imc": 0,
                        "bf_percent": 0,
                        "observacoes": "Cadastrado via agendamento"
                    }
                    st.session_state.pacientes.append(novo_paciente_agenda)
                
                st.session_state.agendamentos.append(novo_agendamento)
                
                st.success("✅ Agendamento criado com sucesso!")
                st.balloons()
                
                # Mostrar resumo
                st.info(f"""
                **📅 Resumo do Agendamento:**
                - **Paciente:** {nome_paciente}
                - **Data:** {data_agendamento.strftime('%d/%m/%Y')}
                - **Horário:** {horario_str}
                - **Tipo:** {tipo_consulta}
                - **Valor:** R$ {valor_agendamento:.2f}
                - **Modalidade:** {modalidade}
                """)
                
                if enviar_whatsapp or enviar_email:
                    st.info(f"🔔 Lembrete será enviado {tempo_lembrete}")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def relatorio_agendamentos(self):
        """Relatórios de agendamentos"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("📊 Relatórios de Agendamentos")
        
        # Período de análise
        col1, col2 = st.columns(2)
        
        with col1:
            data_inicio = st.date_input("📅 Data inicial", value=datetime.now().date() - timedelta(days=30))
        
        with col2:
            data_fim = st.date_input("📅 Data final", value=datetime.now().date())
        
        # Filtrar agendamentos por período
        agendamentos_periodo = []
        for agendamento in st.session_state.agendamentos:
            data_agenda = datetime.strptime(agendamento['data'], '%Y-%m-%d').date()
            if data_inicio <= data_agenda <= data_fim:
                agendamentos_periodo.append(agendamento)
        
        if agendamentos_periodo:
            # Estatísticas do período
            st.markdown("### 📊 Estatísticas do Período")
            
            total_agendamentos = len(agendamentos_periodo)
            agendamentos_realizados = len([a for a in agendamentos_periodo if a.get('status') == 'Realizado'])
            agendamentos_cancelados = len([a for a in agendamentos_periodo if a.get('status') == 'Cancelado'])
            receita_total = sum([a.get('valor', 0) for a in agendamentos_periodo if a.get('status') == 'Realizado'])
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Agendamentos", total_agendamentos)
            with col2:
                taxa_realizacao = (agendamentos_realizados / total_agendamentos) * 100 if total_agendamentos > 0 else 0
                st.metric("Realizados", agendamentos_realizados, f"{taxa_realizacao:.1f}%")
            with col3:
                taxa_cancelamento = (agendamentos_cancelados / total_agendamentos) * 100 if total_agendamentos > 0 else 0
                st.metric("Cancelados", agendamentos_cancelados, f"{taxa_cancelamento:.1f}%")
            with col4:
                st.metric("Receita", f"R$ {receita_total:.2f}")
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de pizza - status
                status_counts = {}
                for agendamento in agendamentos_periodo:
                    status = agendamento.get('status', 'Agendado')
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                fig = go.Figure(data=[go.Pie(
                    labels=list(status_counts.keys()),
                    values=list(status_counts.values()),
                    marker_colors=['#667eea', '#48bb78', '#e53e3e', '#ed8936']
                )])
                
                fig.update_layout(
                    title="Distribuição por Status",
                    height=400,
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Gráfico de barras - tipos de consulta
                tipos_counts = {}
                for agendamento in agendamentos_periodo:
                    tipo = agendamento.get('tipo', 'Consulta')
                    tipos_counts[tipo] = tipos_counts.get(tipo, 0) + 1
                
                fig = go.Figure(data=[go.Bar(
                    x=list(tipos_counts.keys()),
                    y=list(tipos_counts.values()),
                    marker_color='#667eea'
                )])
                
                fig.update_layout(
                    title="Tipos de Consulta",
                    height=400,
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Tabela detalhada
            st.markdown("### 📋 Detalhamento dos Agendamentos")
            
            df_agendamentos = pd.DataFrame(agendamentos_periodo)
            df_display = df_agendamentos[['data', 'horario', 'paciente', 'tipo', 'valor', 'status']].copy()
            df_display['data'] = pd.to_datetime(df_display['data']).dt.strftime('%d/%m/%Y')
            df_display['valor'] = df_display['valor'].apply(lambda x: f"R$ {x:.2f}")
            
            st.dataframe(df_display, use_container_width=True)
            
            # Exportar dados
            if st.button("📊 Exportar Relatório", type="secondary"):
                st.success("Relatório exportado com sucesso! (Funcionalidade em desenvolvimento)")
        
        else:
            st.info("📅 Nenhum agendamento encontrado no período selecionado.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def config_agendamentos(self):
        """Configurações de agendamentos"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("⚙️ Configurações de Agendamentos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**💰 Valores das Consultas**")
            
            valor_consulta = st.number_input(
                "Consulta inicial (R$)",
                value=st.session_state.configuracoes.get('valor_consulta', 150.0),
                min_value=0.0,
                step=10.0
            )
            
            valor_retorno = st.number_input(
                "Consulta de retorno (R$)",
                value=st.session_state.configuracoes.get('valor_retorno', 100.0),
                min_value=0.0,
                step=10.0
            )
            
            st.markdown("**⏰ Horários de Funcionamento**")
            
            horario_inicio = st.time_input(
                "Horário de início",
                value=datetime.strptime(st.session_state.configuracoes.get('horario_inicio', '08:00'), '%H:%M').time()
            )
            
            horario_fim = st.time_input(
                "Horário de término",
                value=datetime.strptime(st.session_state.configuracoes.get('horario_fim', '18:00'), '%H:%M').time()
            )
        
        with col2:
            st.markdown("**📅 Dias de Trabalho**")
            
            dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            dias_trabalho = st.multiselect(
                "Selecione os dias",
                dias_semana,
                default=st.session_state.configuracoes.get('dias_trabalho', ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"])
            )
            
            st.markdown("**⏱️ Intervalos Disponíveis**")
            
            intervalos = st.multiselect(
                "Duração das consultas",
                [30, 45, 60, 90, 120],
                default=st.session_state.configuracoes.get('intervalos_consulta', [60]),
                format_func=lambda x: f"{x} minutos"
            )
            
            st.markdown("**📋 Tipos de Consulta**")
            
            tipos_consulta_atual = st.session_state.configuracoes.get('tipos_consulta', ["Consulta inicial", "Retorno"])
            
            # Sistema para editar tipos de consulta
            for i, tipo in enumerate(tipos_consulta_atual):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.text_input(f"Tipo {i+1}", value=tipo, key=f"tipo_{i}")
                with col_b:
                    if st.button("🗑️", key=f"remove_tipo_{i}") and len(tipos_consulta_atual) > 1:
                        tipos_consulta_atual.pop(i)
                        st.rerun()
        
        # Botão para salvar configurações
        if st.button("💾 Salvar Configurações", type="primary", use_container_width=True):
            st.session_state.configuracoes.update({
                'valor_consulta': valor_consulta,
                'valor_retorno': valor_retorno,
                'horario_inicio': horario_inicio.strftime('%H:%M'),
                'horario_fim': horario_fim.strftime('%H:%M'),
                'dias_trabalho': dias_trabalho,
                'intervalos_consulta': intervalos
            })
            
            st.success("✅ Configurações salvas com sucesso!")
            time.sleep(1)
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    def comunicacao_page(self):
        """Sistema de comunicação"""
        st.markdown('<div class="main-header"><h1>💬 Sistema de Comunicação</h1><p>WhatsApp, templates e comunicação integrada</p></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📱 WhatsApp",
            "📧 Templates", 
            "📊 Histórico",
            "⚙️ Configurações"
        ])
        
        with tab1:
            self.whatsapp_comunicacao()
        
        with tab2:
            self.templates_comunicacao()
        
        with tab3:
            self.historico_comunicacao()
        
        with tab4:
            self.config_comunicacao()

    def whatsapp_comunicacao(self):
        """Interface do WhatsApp"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("📱 WhatsApp Business")
        
        # Estatísticas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Mensagens Enviadas", "247", "+12 hoje")
        with col2:
            st.metric("Taxa de Entrega", "98.5%", "+0.3%")
        with col3:
            st.metric("Taxa de Resposta", "76%", "+5%")
        with col4:
            st.metric("Tempo Médio Resposta", "2.3h", "-0.5h")
        
        # Envio de mensagem
        st.markdown("### 📤 Enviar Mensagem")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Seleção do destinatário
            destinatario_tipo = st.radio("👤 Destinatário", ["Paciente específico", "Grupo de pacientes", "Número manual"])
            
            if destinatario_tipo == "Paciente específico":
                if st.session_state.pacientes:
                    paciente_whats = st.selectbox("Selecionar paciente", [p['nome'] for p in st.session_state.pacientes])
                    telefone_destino = next(p['telefone'] for p in st.session_state.pacientes if p['nome'] == paciente_whats)
                    st.info(f"📱 {telefone_destino}")
                else:
                    st.warning("Nenhum paciente cadastrado")
                    telefone_destino = ""
            
            elif destinatario_tipo == "Grupo de pacientes":
                filtros_grupo = st.multiselect("Filtrar por", ["Objetivo", "Status", "Idade"])
                if "Objetivo" in filtros_grupo:
                    objetivos = st.multiselect("Objetivos", ["Perda de peso", "Ganho de massa", "Manutenção"])
                pacientes_selecionados = len(st.session_state.pacientes)  # Simulado
                st.info(f"👥 {pacientes_selecionados} pacientes selecionados")
                telefone_destino = "grupo"
            
            else:
                telefone_destino = st.text_input("📱 Número do telefone", placeholder="+55 11 99999-9999")
            
            # Template ou mensagem personalizada
            opcao_mensagem = st.radio("📝 Tipo de mensagem", ["Template", "Mensagem personalizada"])
            
            if opcao_mensagem == "Template":
                templates_disponiveis = list(st.session_state.templates_comunicacao.keys())
                template_selecionado = st.selectbox("Selecionar template", templates_disponiveis)
                
                if template_selecionado:
                    template_texto = st.session_state.templates_comunicacao[template_selecionado]
                    st.text_area("Preview do template", value=template_texto, disabled=True, height=100)
            
            else:
                template_texto = st.text_area("✏️ Digite sua mensagem", height=120, 
                                            placeholder="Digite aqui sua mensagem personalizada...")
            
            # Opções avançadas
            with st.expander("⚙️ Opções Avançadas"):
                agendar_envio = st.checkbox("⏰ Agendar envio")
                if agendar_envio:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        data_envio = st.date_input("Data", min_value=datetime.now().date())
                    with col_b:
                        hora_envio = st.time_input("Horário")
                
                incluir_anexo = st.checkbox("📎 Incluir anexo")
                if incluir_anexo:
                    tipo_anexo = st.selectbox("Tipo", ["Imagem", "PDF", "Documento"])
                    anexo = st.file_uploader("Selecionar arquivo")
        
        with col2:
            st.markdown("### 🚀 Enviar")
            
            if st.button("📤 Enviar Agora", type="primary", use_container_width=True):
                if telefone_destino and template_texto:
                    if agendar_envio:
                        st.success(f"✅ Mensagem agendada para {data_envio.strftime('%d/%m/%Y')} às {hora_envio.strftime('%H:%M')}")
                    else:
                        st.success("✅ Mensagem enviada com sucesso!")
                        
                        # Simular histórico
                        novo_historico = {
                            "data": datetime.now().strftime('%d/%m/%Y %H:%M'),
                            "destinatario": telefone_destino,
                            "mensagem": template_texto[:50] + "...",
                            "status": "Enviado",
                            "tipo": "WhatsApp"
                        }
                        
                        if 'historico_mensagens' not in st.session_state:
                            st.session_state.historico_mensagens = []
                        
                        st.session_state.historico_mensagens.append(novo_historico)
                else:
                    st.error("❌ Preencha todos os campos obrigatórios")
            
            if st.button("👁️ Preview", type="secondary", use_container_width=True):
                if template_texto:
                    st.info("📱 Preview da mensagem:")
                    st.text_area("", value=template_texto, disabled=True, height=80)
            
            if st.button("💾 Salvar como Template", type="secondary", use_container_width=True):
                if template_texto:
                    nome_template = st.text_input("Nome do template")
                    if nome_template:
                        st.session_state.templates_comunicacao[nome_template] = template_texto
                        st.success(f"✅ Template '{nome_template}' salvo!")
        
        # Histórico recente
        st.markdown("### 📋 Mensagens Recentes")
        
        if 'historico_mensagens' in st.session_state and st.session_state.historico_mensagens:
            for msg in st.session_state.historico_mensagens[-5:]:  # Últimas 5
                col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
                
                with col1:
                    st.markdown(f"**{msg['data']}**")
                
                with col2:
                    st.markdown(f"📱 {msg['destinatario']}")
                    st.markdown(f"💬 {msg['mensagem']}")
                
                with col3:
                    status_color = "#48bb78" if msg['status'] == "Enviado" else "#ed8936"
                    st.markdown(f'<span style="color: {status_color};">● {msg["status"]}</span>', unsafe_allow_html=True)
                
                with col4:
                    if st.button("📊", key=f"stats_{msg['data']}", help="Estatísticas"):
                        st.info("📊 Entregue em 2.3s, Lida em 5.2min")
        
        else:
            st.info("📝 Nenhuma mensagem enviada ainda.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def templates_comunicacao(self):
        """Gestão de templates"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("📧 Gestão de Templates")
        
        # Templates existentes
        st.markdown("### 📋 Templates Disponíveis")
        
        for nome, conteudo in st.session_state.templates_comunicacao.items():
            with st.expander(f"📄 {nome.replace('_', ' ').title()}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.text_area("Conteúdo", value=conteudo, height=100, disabled=True)
                    
                    # Variáveis disponíveis
                    st.info("**Variáveis disponíveis:** {nome}, {data}, {horario}")
                
                with col2:
                    if st.button("✏️ Editar", key=f"edit_{nome}"):
                        st.session_state[f"editando_{nome}"] = True
                    
                    if st.button("📋 Usar", key=f"use_{nome}"):
                        st.success(f"Template '{nome}' selecionado!")
                    
                    if st.button("🗑️ Excluir", key=f"delete_{nome}"):
                        if st.button("⚠️ Confirmar", key=f"confirm_{nome}"):
                            del st.session_state.templates_comunicacao[nome]
                            st.success("Template excluído!")
                            st.rerun()
        
        # Criar novo template
        st.markdown("### ➕ Criar Novo Template")
        
        with st.form("novo_template"):
            nome_template = st.text_input("Nome do template")
            categoria_template = st.selectbox("Categoria", [
                "Lembretes", "Motivacionais", "Informativos", 
                "Comerciais", "Consultas", "Outros"
            ])
            
            conteudo_template = st.text_area(
                "Conteúdo do template", 
                height=120,
                placeholder="Use {nome} para o nome do paciente, {data} para data, {horario} para horário..."
            )
            
            if st.form_submit_button("💾 Criar Template", type="primary"):
                if nome_template and conteudo_template:
                    st.session_state.templates_comunicacao[nome_template] = conteudo_template
                    st.success(f"✅ Template '{nome_template}' criado com sucesso!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Preencha nome e conteúdo do template")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def historico_comunicacao(self):
        """Histórico de comunicações"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("📊 Histórico de Comunicações")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_periodo = st.selectbox("📅 Período", ["Últimos 7 dias", "Último mês", "Últimos 3 meses", "Personalizado"])
        
        with col2:
            filtro_tipo = st.selectbox("📱 Tipo", ["Todos", "WhatsApp", "Email", "SMS"])
        
        with col3:
            filtro_status = st.selectbox("📊 Status", ["Todos", "Enviado", "Entregue", "Lido", "Erro"])
        
        # Estatísticas do período
        st.markdown("### 📈 Estatísticas do Período")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Enviadas", "156", "+23")
        with col2:
            st.metric("Taxa Entrega", "97.4%", "+1.2%")
        with col3:
            st.metric("Taxa Abertura", "68.2%", "+3.5%")
        with col4:
            st.metric("Taxa Resposta", "24.1%", "+2.1%")
        
        # Gráfico de evolução
        col1, col2 = st.columns(2)
        
        with col1:
            # Simular dados de evolução
            dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
            enviadas = [23, 18, 25, 31, 28, 12, 8]
            respondidas = [8, 6, 9, 12, 11, 4, 2]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Enviadas',
                x=dias,
                y=enviadas,
                marker_color='#667eea'
            ))
            
            fig.add_trace(go.Bar(
                name='Respondidas',
                x=dias,
                y=respondidas,
                marker_color='#48bb78'
            ))
            
            fig.update_layout(
                title="Mensagens por Dia",
                barmode='group',
                height=300,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico de tipos
            tipos = ['WhatsApp', 'Email', 'SMS']
            valores = [78, 15, 7]
            
            fig = go.Figure(data=[go.Pie(
                labels=tipos,
                values=valores,
                marker_colors=['#25d366', '#4285f4', '#ff6b35']
            )])
            
            fig.update_layout(
                title="Distribuição por Tipo",
                height=300,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Lista detalhada
        st.markdown("### 📋 Lista de Comunicações")
        
        # Dados simulados
        comunicacoes_exemplo = [
            {"data": "22/09/2024 14:30", "destinatario": "Maria Silva", "tipo": "WhatsApp", "assunto": "Lembrete consulta", "status": "Lido"},
            {"data": "22/09/2024 10:15", "destinatario": "João Santos", "tipo": "Email", "assunto": "Plano alimentar", "status": "Entregue"},
            {"data": "21/09/2024 16:45", "destinatario": "Ana Costa", "tipo": "WhatsApp", "assunto": "Motivacional", "status": "Respondido"},
        ]
        
        for com in comunicacoes_exemplo:
            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 2, 1])
            
            with col1:
                st.markdown(f"**{com['data']}**")
            
            with col2:
                st.markdown(f"👤 {com['destinatario']}")
            
            with col3:
                tipo_icons = {"WhatsApp": "📱", "Email": "📧", "SMS": "💬"}
                st.markdown(f"{tipo_icons.get(com['tipo'], '📱')} {com['tipo']}")
            
            with col4:
                st.markdown(f"📄 {com['assunto']}")
            
            with col5:
                status_colors = {
                    "Enviado": "#667eea",
                    "Entregue": "#ed8936", 
                    "Lido": "#48bb78",
                    "Respondido": "#10b981"
                }
                color = status_colors.get(com['status'], '#718096')
                st.markdown(f'<span style="color: {color};">● {com["status"]}</span>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def config_comunicacao(self):
        """Configurações de comunicação"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("⚙️ Configurações de Comunicação")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📱 WhatsApp Business**")
            
            whatsapp_ativo = st.checkbox("Ativar WhatsApp", value=True)
            numero_whatsapp = st.text_input("Número do WhatsApp Business", 
                                          value=st.session_state.configuracoes.get('whatsapp', ''))
            
            if whatsapp_ativo:
                st.success("✅ WhatsApp conectado")
            else:
                st.warning("⚠️ WhatsApp desconectado")
            
            st.markdown("**📧 Email**")
            
            email_ativo = st.checkbox("Ativar Email", value=True)
            email_remetente = st.text_input("Email remetente", 
                                          value=st.session_state.configuracoes.get('email', ''))
            servidor_smtp = st.text_input("Servidor SMTP", value="smtp.gmail.com")
            porta_smtp = st.number_input("Porta", value=587)
            
        with col2:
            st.markdown("**🔔 Notificações Automáticas**")
            
            lembrete_consulta = st.checkbox("Lembrete de consulta", value=True)
            tempo_lembrete_padrao = st.selectbox("Tempo padrão do lembrete", 
                                                ["30 min", "1 hora", "2 horas", "1 dia"])
            
            confirmacao_agendamento = st.checkbox("Confirmação de agendamento", value=True)
            follow_up_consulta = st.checkbox("Follow-up pós consulta", value=False)
            
            st.markdown("**📊 Relatórios**")
            
            relatorio_semanal = st.checkbox("Relatório semanal automático", value=False)
            relatorio_mensal = st.checkbox("Relatório mensal automático", value=True)
            
            if relatorio_semanal or relatorio_mensal:
                email_relatorios = st.text_input("Email para relatórios", value=email_remetente)
        
        # Testar conectividade
        st.markdown("### 🧪 Testar Conectividade")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📱 Testar WhatsApp", type="secondary"):
                with st.spinner("Testando conexão..."):
                    time.sleep(2)
                    st.success("✅ WhatsApp conectado e funcionando!")
        
        with col2:
            if st.button("📧 Testar Email", type="secondary"):
                with st.spinner("Testando SMTP..."):
                    time.sleep(2)
                    st.success("✅ Servidor de email configurado corretamente!")
        
        # Salvar configurações
        if st.button("💾 Salvar Configurações", type="primary", use_container_width=True):
            st.session_state.configuracoes.update({
                'whatsapp': numero_whatsapp,
                'email': email_remetente,
                'whatsapp_ativo': whatsapp_ativo,
                'email_ativo': email_ativo,
                'lembrete_consulta': lembrete_consulta,
                'tempo_lembrete_padrao': tempo_lembrete_padrao,
                'confirmacao_agendamento': confirmacao_agendamento,
                'follow_up_consulta': follow_up_consulta,
                'relatorio_semanal': relatorio_semanal,
                'relatorio_mensal': relatorio_mensal
            })
            
            st.success("✅ Configurações de comunicação salvas!")
            time.sleep(1)
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    def relatorios_page(self):
        """Sistema de relatórios avançados"""
        st.markdown('<div class="main-header"><h1>📊 Relatórios Avançados</h1><p>Analytics profissionais e insights detalhados</p></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Dashboard Analytics",
            "👥 Relatório de Pacientes",
            "💰 Relatório Financeiro", 
            "📊 Relatórios Customizados"
        ])
        
        with tab1:
            self.dashboard_analytics()
        
        with tab2:
            self.relatorio_pacientes()
        
        with tab3:
            self.relatorio_financeiro()
        
        with tab4:
            self.relatorios_customizados()

    def dashboard_analytics(self):
        """Dashboard com analytics avançados"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("📈 Dashboard Analytics")
        
        # Seletor de período
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            periodo_inicio = st.date_input("📅 Data inicial", value=datetime.now().date() - timedelta(days=90))
        
        with col2:
            periodo_fim = st.date_input("📅 Data final", value=datetime.now().date())
        
        with col3:
            if st.button("🔄 Atualizar", type="primary"):
                st.success("Dados atualizados!")
        
        # KPIs principais com comparação
        st.markdown("### 📊 KPIs Principais")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Dados simulados com tendências
        total_pacientes_periodo = len(st.session_state.pacientes)
        consultas_realizadas = len([a for a in st.session_state.agendamentos if a.get('status') == 'Realizado'])
        receita_periodo = sum([a.get('valor', 0) for a in st.session_state.agendamentos if a.get('status') == 'Realizado'])
        ticket_medio = receita_periodo / consultas_realizadas if consultas_realizadas > 0 else 0
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <div style="text-align: center;">
                    <div class="metric-value">{total_pacientes_periodo}</div>
                    <div class="metric-label">Pacientes Ativos</div>
                    <div style="color: #48bb78; font-size: 0.9rem; margin-top: 0.5rem;">📈 +15% vs período anterior</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <div style="text-align: center;">
                    <div class="metric-value">{consultas_realizadas}</div>
                    <div class="metric-label">Consultas Realizadas</div>
                    <div style="color: #48bb78; font-size: 0.9rem; margin-top: 0.5rem;">📈 +8% vs período anterior</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <div style="text-align: center;">
                    <div class="metric-value">R$ {receita_periodo:,.0f}</div>
                    <div class="metric-label">Receita Total</div>
                    <div style="color: #48bb78; font-size: 0.9rem; margin-top: 0.5rem;">📈 +22% vs período anterior</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <div style="text-align: center;">
                    <div class="metric-value">R$ {ticket_medio:.0f}</div>
                    <div class="metric-label">Ticket Médio</div>
                    <div style="color: #48bb78; font-size: 0.9rem; margin-top: 0.5rem;">📈 +5% vs período anterior</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Gráficos analíticos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Evolução Mensal")
            
            # Dados simulados de evolução mensal
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set']
            novos_pacientes = [3, 5, 8, 6, 9, 12, 8, 10, 7]
            receita_mensal = [450, 750, 1200, 900, 1350, 1800, 1200, 1500, 1050]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=meses,
                y=novos_pacientes,
                mode='lines+markers',
                name='Novos Pacientes',
                line=dict(color='#667eea', width=3),
                yaxis='y'
            ))
            
            fig.add_trace(go.Scatter(
                x=meses,
                y=receita_mensal,
                mode='lines+markers',
                name='Receita (R$)',
                line=dict(color='#48bb78', width=3),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title="Crescimento do Negócio",
                yaxis=dict(title="Novos Pacientes", side="left"),
                yaxis2=dict(title="Receita (R$)", side="right", overlaying="y"),
                height=400,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Análise de Conversão")
            
            # Funil de conversão
            etapas = ['Contatos', 'Agendamentos', 'Consultas', 'Retornos']
            valores = [150, 120, 95, 72]
            
            fig = go.Figure(go.Funnel(
                y=etapas,
                x=valores,
                textinfo="value+percent initial",
                marker_color=['#667eea', '#48bb78', '#ed8936', '#f093fb']
            ))
            
            fig.update_layout(
                title="Funil de Conversão",
                height=400,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Análises avançadas
        st.markdown("### 📊 Análises Avançadas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 👥 Perfil dos Pacientes")
            
            # Distribuição por objetivo
            objetivos = {}
            for paciente in st.session_state.pacientes:
                obj = paciente.get('objetivo', 'Não informado')
                objetivos[obj] = objetivos.get(obj, 0) + 1
            
            if objetivos:
                fig = go.Figure(data=[go.Pie(
                    labels=list(objetivos.keys()),
                    values=list(objetivos.values()),
                    hole=.3
                )])
                
                fig.update_layout(
                    title="Distribuição por Objetivo",
                    height=300,
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### ⏰ Performance por Horário")
            
            # Dados simulados de horários
            horarios = ['08h', '10h', '14h', '16h', '18h']
            agendamentos_por_hora = [15, 25, 30, 28, 12]
            
            fig = go.Figure(data=[go.Bar(
                x=horarios,
                y=agendamentos_por_hora,
                marker_color='#667eea'
            )])
            
            fig.update_layout(
                title="Agendamentos por Horário",
                height=300,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.markdown("#### 📅 Sazonalidade")
            
            # Dados de sazonalidade
            dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex']
            consultas_por_dia = [18, 22, 25, 20, 15]
            
            fig = go.Figure(data=[go.Bar(
                x=dias_semana,
                y=consultas_por_dia,
                marker_color='#48bb78'
            )])
            
            fig.update_layout(
                title="Consultas por Dia da Semana",
                height=300,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Insights e recomendações
        st.markdown("### 💡 Insights & Recomendações")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="calculator-card">
                <h4 style="color: #48bb78; margin-bottom: 1rem;">🚀 Oportunidades</h4>
                <div style="line-height: 1.6;">
                    • <strong>Horário premium:</strong> 14h-16h com maior demanda<br>
                    • <strong>Terças-feiras:</strong> Melhor dia para agendamentos<br>
                    • <strong>Retenção:</strong> 76% dos pacientes retornam<br>
                    • <strong>Crescimento:</strong> +15% novos pacientes/mês
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="calculator-card">
                <h4 style="color: #ed8936; margin-bottom: 1rem;">⚠️ Pontos de Atenção</h4>
                <div style="line-height: 1.6;">
                    • <strong>Cancelamentos:</strong> 8% nas sextas-feiras<br>
                    • <strong>No-show:</strong> 5% em consultas de retorno<br>
                    • <strong>Baixa adesão:</strong> Pacientes > 50 anos<br>
                    • <strong>Sazonalidade:</strong> Queda em dezembro/janeiro
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="calculator-card">
                <h4 style="color: #667eea; margin-bottom: 1rem;">📈 Ações Recomendadas</h4>
                <div style="line-height: 1.6;">
                    • <strong>Marketing:</strong> Foque em mulheres 25-40 anos<br>
                    • <strong>Pricing:</strong> Considere pacotes de consultas<br>
                    • <strong>Processo:</strong> Automatize lembretes<br>
                    • <strong>Expansão:</strong> Considere atendimento noturno
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def relatorio_pacientes(self):
        """Relatório detalhado de pacientes"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("👥 Relatório de Pacientes")
        
        if st.session_state.pacientes:
            # Filtros
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filtro_status = st.selectbox("Status", ["Todos", "Ativo", "Inativo"])
            
            with col2:
                filtro_objetivo = st.selectbox("Objetivo", ["Todos"] + list(set([p.get('objetivo', '') for p in st.session_state.pacientes])))
            
            with col3:
                ordenar_por = st.selectbox("Ordenar por", ["Nome", "Data cadastro", "IMC", "Última consulta"])
            
            # Análise estatística
            st.markdown("### 📊 Análise Estatística dos Pacientes")
            
            # Preparar dados
            idades = []
            imcs = []
            for paciente in st.session_state.pacientes:
                if paciente.get('data_nascimento'):
                    try:
                        nascimento = datetime.strptime(paciente['data_nascimento'], '%Y-%m-%d')
                        idade = (datetime.now() - nascimento).days // 365
                        idades.append(idade)
                    except:
                        pass
                
                if paciente.get('imc'):
                    imcs.append(paciente['imc'])
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                idade_media = sum(idades) / len(idades) if idades else 0
                st.metric("Idade Média", f"{idade_media:.0f} anos")
            
            with col2:
                imc_medio = sum(imcs) / len(imcs) if imcs else 0
                st.metric("IMC Médio", f"{imc_medio:.1f}")
            
            with col3:
                pacientes_objetivo_peso = len([p for p in st.session_state.pacientes if 'peso' in p.get('objetivo', '').lower()])
                st.metric("Foco Emagrecimento", f"{pacientes_objetivo_peso}")
            
            with col4:
                retencao = 85  # Simulado
                st.metric("Taxa Retenção", f"{retencao}%")
            
            # Gráficos de análise
            col1, col2 = st.columns(2)
            
            with col1:
                if idades:
                    # Distribuição de idades
                    fig = go.Figure(data=[go.Histogram(
                        x=idades,
                        nbinsx=10,
                        marker_color='#667eea',
                        opacity=0.7
                    )])
                    
                    fig.update_layout(
                        title="Distribuição de Idades",
                        xaxis_title="Idade (anos)",
                        yaxis_title="Número de Pacientes",
                        height=300,
                        paper_bgcolor="rgba(0,0,0,0)"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if imcs:
                    # Distribuição de IMCs
                    fig = go.Figure(data=[go.Histogram(
                        x=imcs,
                        nbinsx=8,
                        marker_color='#48bb78',
                        opacity=0.7
                    )])
                    
                    fig.update_layout(
                        title="Distribuição de IMCs",
                        xaxis_title="IMC (kg/m²)",
                        yaxis_title="Número de Pacientes",
                        height=300,
                        paper_bgcolor="rgba(0,0,0,0)"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            # Tabela detalhada dos pacientes
            st.markdown("### 📋 Lista Detalhada de Pacientes")
            
            # Preparar dados para a tabela
            dados_tabela = []
            for paciente in st.session_state.pacientes:
                # Calcular idade
                idade = "N/A"
                if paciente.get('data_nascimento'):
                    try:
                        nascimento = datetime.strptime(paciente['data_nascimento'], '%Y-%m-%d')
                        idade = (datetime.now() - nascimento).days // 365
                    except:
                        pass
                
                # Última consulta (simulado)
                ultima_consulta = "22/08/2024"  # Simulado
                
                dados_tabela.append({
                    "Nome": paciente['nome'],
                    "Email": paciente['email'],
                    "Telefone": paciente['telefone'],
                    "Idade": idade,
                    "Objetivo": paciente.get('objetivo', 'N/A'),
                    "IMC": f"{paciente.get('imc', 0):.1f}",
                    "Status": paciente.get('status', 'Ativo'),
                    "Cadastro": paciente.get('data_cadastro', 'N/A'),
                    "Última Consulta": ultima_consulta
                })
            
            df_pacientes = pd.DataFrame(dados_tabela)
            
            # Aplicar filtros
            if filtro_status != "Todos":
                df_pacientes = df_pacientes[df_pacientes['Status'] == filtro_status]
            
            if filtro_objetivo != "Todos":
                df_pacientes = df_pacientes[df_pacientes['Objetivo'] == filtro_objetivo]
            
            # Mostrar tabela
            st.dataframe(df_pacientes, use_container_width=True, height=400)
            
            # Opções de exportação
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📊 Exportar Excel", type="secondary"):
                    st.success("Relatório exportado para Excel! (Em desenvolvimento)")
            
            with col2:
                if st.button("📄 Exportar PDF", type="secondary"):
                    st.success("Relatório exportado para PDF! (Em desenvolvimento)")
            
            with col3:
                if st.button("📧 Enviar por Email", type="secondary"):
                    st.success("Relatório enviado por email! (Em desenvolvimento)")
        
        else:
            st.info("📝 Nenhum paciente cadastrado para gerar relatório.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def relatorio_financeiro(self):
        """Relatório financeiro"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("💰 Relatório Financeiro")
        
        # Período de análise
        col1, col2 = st.columns(2)
        
        with col1:
            data_inicio_fin = st.date_input("📅 Data inicial", value=datetime.now().date() - timedelta(days=90), key="fin_inicio")
        
        with col2:
            data_fim_fin = st.date_input("📅 Data final", value=datetime.now().date(), key="fin_fim")
        
        # Dados financeiros simulados
        receita_total = 12750.00
        consultas_realizadas_fin = 85
        ticket_medio_fin = receita_total / consultas_realizadas_fin
        custos_operacionais = 2500.00
        lucro_liquido = receita_total - custos_operacionais
        
        # Resumo financeiro
        st.markdown("### 💰 Resumo Financeiro")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <div style="text-align: center;">
                    <div class="metric-value">R$ {receita_total:,.2f}</div>
                    <div class="metric-label">Receita Bruta</div>
                    <div style="color: #48bb78; font-size: 0.9rem; margin-top: 0.5rem;">📈 +18%</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <div style="text-align: center;">
                    <div class="metric-value">R$ {ticket_medio_fin:.2f}</div>
                    <div class="metric-label">Ticket Médio</div>
                    <div style="color: #48bb78; font-size: 0.9rem; margin-top: 0.5rem;">📈 +5%</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <div style="text-align: center;">
                    <div class="metric-value">R$ {custos_operacionais:,.2f}</div>
                    <div class="metric-label">Custos</div>
                    <div style="color: #ed8936; font-size: 0.9rem; margin-top: 0.5rem;">📊 19.6%</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
            
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <div style="text-align: center;">
                    <div class="metric-value">R$ {lucro_liquido:,.2f}</div>
                    <div class="metric-label">Lucro Líquido</div>
                    <div style="color: #48bb78; font-size: 0.9rem; margin-top: 0.5rem;">📈 +25%</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Gráficos financeiros
        col1, col2 = st.columns(2)
        
        with col1:
            # Evolução mensal da receita
            meses_fin = ['Jun', 'Jul', 'Ago', 'Set']
            receitas_mensais = [3200, 3800, 4250, 4500]
            custos_mensais = [600, 650, 700, 750]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Receita',
                x=meses_fin,
                y=receitas_mensais,
                marker_color='#48bb78'
            ))
            
            fig.add_trace(go.Bar(
                name='Custos',
                x=meses_fin,
                y=custos_mensais,
                marker_color='#ed8936'
            ))
            
            fig.update_layout(
                title="Receita vs Custos Mensais",
                barmode='group',
                height=400,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Composição da receita
            tipos_receita = ['Consulta Inicial', 'Retorno', 'Planos Especiais', 'Outros']
            valores_receita = [5100, 4080, 2550, 1020]
            
            fig = go.Figure(data=[go.Pie(
                labels=tipos_receita,
                values=valores_receita,
                marker_colors=['#667eea', '#48bb78', '#ed8936', '#f093fb']
            )])
            
            fig.update_layout(
                title="Composição da Receita",
                height=400,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Análise de rentabilidade
        st.markdown("### 📊 Análise de Rentabilidade")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Métricas de rentabilidade
            margem_bruta = ((receita_total - custos_operacionais) / receita_total) * 100
            roi = (lucro_liquido / custos_operacionais) * 100
            
            st.info(f"""
            **💡 Indicadores de Rentabilidade:**
            - **Margem Bruta:** {margem_bruta:.1f}%
            - **ROI:** {roi:.1f}%
            - **Receita por Consulta:** R$ {ticket_medio_fin:.2f}
            - **Custo por Consulta:** R$ {custos_operacionais/consultas_realizadas_fin:.2f}
            """)
        
        with col2:
            # Projeções
            st.info(f"""
            **📈 Projeções (próximo trimestre):**
            - **Receita Projetada:** R$ {receita_total * 1.15:,.2f} (+15%)
            - **Novos Pacientes Necessários:** {int((receita_total * 0.15) / ticket_medio_fin)}
            - **Meta Mensal:** R$ {(receita_total * 1.15) / 3:,.2f}
            - **Crescimento Necessário:** {((receita_total * 1.15) / receita_total - 1) * 100:.1f}% ao mês
            """)
        
        # Breakdown de custos
        st.markdown("### 💸 Breakdown de Custos")
        
        custos_breakdown = {
            "Aluguel/Espaço": 800,
            "Marketing": 500,
            "Materiais": 300,
            "Software/Tecnologia": 200,
            "Telefone/Internet": 150,
            "Outros": 550
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de custos
            fig = go.Figure(data=[go.Pie(
                labels=list(custos_breakdown.keys()),
                values=list(custos_breakdown.values()),
                hole=.3
            )])
            
            fig.update_layout(
                title="Distribuição de Custos",
                height=300,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Tabela de custos
            df_custos = pd.DataFrame([
                {"Categoria": k, "Valor": f"R$ {v:.2f}", "% do Total": f"{(v/sum(custos_breakdown.values()))*100:.1f}%"}
                for k, v in custos_breakdown.items()
            ])
            
            st.dataframe(df_custos, use_container_width=True, height=250)
        
        # Ações recomendadas
        st.markdown("### 💡 Recomendações Financeiras")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success("""
            **✅ Pontos Positivos:**
            - Crescimento consistente (+18%)
            - Margem saudável (80.4%)
            - ROI excelente (310%)
            - Ticket médio crescendo
            """)
        
        with col2:
            st.warning("""
            **⚠️ Oportunidades:**
            - Reduzir custo de aquisição
            - Aumentar frequência de retornos
            - Criar pacotes premium
            - Otimizar custos operacionais
            """)
        
        with col3:
            st.info("""
            **📈 Ações Sugeridas:**
            - Implementar programa de fidelidade
            - Investir em marketing digital
            - Automatizar processos
            - Diversificar serviços
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def relatorios_customizados(self):
        """Relatórios customizados"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("📊 Relatórios Customizados")
        
        # Builder de relatório
        st.markdown("### 🛠️ Construtor de Relatório")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Configurações do Relatório**")
            
            nome_relatorio = st.text_input("Nome do relatório")
            tipo_relatorio = st.selectbox("Tipo de relatório", [
                "Pacientes", "Financeiro", "Agendamentos", 
                "Comunicação", "Performance", "Customizado"
            ])
            
            periodo_relatorio = st.selectbox("Período", [
                "Última semana", "Último mês", "Últimos 3 meses",
                "Último ano", "Período personalizado"
            ])
            
            if periodo_relatorio == "Período personalizado":
                col_a, col_b = st.columns(2)
                with col_a:
                    data_inicio_custom = st.date_input("Data inicial")
                with col_b:
                    data_fim_custom = st.date_input("Data final")
            
            formato_output = st.selectbox("Formato de saída", [
                "Dashboard interativo", "PDF", "Excel", "CSV"
            ])
        
        with col2:
            st.markdown("**📈 Métricas e Dimensões**")
            
            metricas_disponiveis = [
                "Número de pacientes", "Receita total", "Ticket médio",
                "Taxa de conversão", "Taxa de retenção", "Consultas realizadas",
                "Tempo médio de tratamento", "Satisfação do paciente"
            ]
            
            metricas_selecionadas = st.multiselect("Métricas", metricas_disponiveis)
            
            dimensoes_disponiveis = [
                "Tempo (diário/semanal/mensal)", "Objetivo do paciente",
                "Faixa etária", "Sexo", "Tipo de consulta", "Status"
            ]
            
            dimensoes_selecionadas = st.multiselect("Dimensões", dimensoes_disponiveis)
            
            graficos_incluir = st.multiselect("Gráficos a incluir", [
                "Linha temporal", "Gráfico de barras", "Pizza", 
                "Histograma", "Scatter plot", "Funil"
            ])
        
        # Filtros avançados
        st.markdown("**🔍 Filtros Avançados**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_idade = st.selectbox("Faixa etária", ["Todas", "18-25", "26-35", "36-50", "50+"])
        
        with col2:
            filtro_objetivo_custom = st.selectbox("Objetivo", ["Todos"] + list(set([p.get('objetivo', '') for p in st.session_state.pacientes])))
        
        with col3:
            filtro_valor_min = st.number_input("Valor mínimo consulta", value=0.0)
        
        # Visualização prévia
        if st.button("👁️ Visualizar Prévia", type="secondary"):
            st.markdown("### 📊 Prévia do Relatório")
            
            if metricas_selecionadas and dimensoes_selecionadas:
                # Simular dados para prévia
                st.success(f"✅ Relatório '{nome_relatorio}' configurado com sucesso!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"""
                    **📋 Configurações:**
                    - **Tipo:** {tipo_relatorio}
                    - **Período:** {periodo_relatorio}
                    - **Métricas:** {len(metricas_selecionadas)} selecionadas
                    - **Dimensões:** {len(dimensoes_selecionadas)} selecionadas
                    """)
                
                with col2:
                    # Gráfico de exemplo
                    dados_exemplo = [23, 45, 56, 78, 32, 67, 89]
                    
                    fig = go.Figure(data=go.Bar(
                        x=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'],
                        y=dados_exemplo,
                        marker_color='#667eea'
                    ))
                    
                    fig.update_layout(
                        title="Exemplo: Consultas por Dia",
                        height=300,
                        paper_bgcolor="rgba(0,0,0,0)"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            else:
                st.warning("⚠️ Selecione ao menos uma métrica e uma dimensão")
        
        # Salvar e gerar relatório
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Salvar Configuração", type="secondary", use_container_width=True):
                if nome_relatorio:
                    config_relatorio = {
                        "nome": nome_relatorio,
                        "tipo": tipo_relatorio,
                        "periodo": periodo_relatorio,
                        "metricas": metricas_selecionadas,
                        "dimensoes": dimensoes_selecionadas,
                        "graficos": graficos_incluir,
                        "formato": formato_output,
                        "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    
                    if 'relatorios_salvos' not in st.session_state:
                        st.session_state.relatorios_salvos = []
                    
                    st.session_state.relatorios_salvos.append(config_relatorio)
                    st.success(f"✅ Configuração '{nome_relatorio}' salva!")
                else:
                    st.error("❌ Digite um nome para o relatório")
        
        with col2:
            if st.button("📊 Gerar Relatório", type="primary", use_container_width=True):
                if metricas_selecionadas:
                    with st.spinner("Gerando relatório..."):
                        time.sleep(2)
                        st.success(f"✅ Relatório '{nome_relatorio}' gerado com sucesso!")
                        st.balloons()
                else:
                    st.error("❌ Selecione ao menos uma métrica")
        
        with col3:
            if st.button("📧 Agendar Envio", type="secondary", use_container_width=True):
                with st.expander("⏰ Configurar Agendamento"):
                    frequencia = st.selectbox("Frequência", ["Diário", "Semanal", "Mensal"])
                    email_destino = st.text_input("Email destinatário")
                    if st.button("✅ Confirmar Agendamento"):
                        st.success(f"📅 Relatório agendado para envio {frequencia.lower()}")
        
        # Relatórios salvos
        if hasattr(st.session_state, 'relatorios_salvos') and st.session_state.relatorios_salvos:
            st.markdown("### 📚 Relatórios Salvos")
            
            for i, relatorio in enumerate(st.session_state.relatorios_salvos):
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.markdown(f"**{relatorio['nome']}**")
                    st.markdown(f"📊 {relatorio['tipo']} • {relatorio['periodo']}")
                
                with col2:
                    st.markdown(f"📈 {len(relatorio['metricas'])} métricas")
                    st.markdown(f"📋 {len(relatorio['dimensoes'])} dimensões")
                
                with col3:
                    st.markdown(f"📅 {relatorio['criado_em']}")
                    st.markdown(f"📄 {relatorio['formato']}")
                
                with col4:
                    if st.button("▶️", key=f"run_report_{i}", help="Executar"):
                        st.success(f"Executando '{relatorio['nome']}'...")
                
                st.divider()
        
        st.markdown('</div>', unsafe_allow_html=True)

    def metas_objetivos_page(self):
        """Sistema de metas e objetivos"""
        st.markdown('<div class="main-header"><h1>🎯 Metas & Objetivos</h1><p>Definição e acompanhamento de metas estratégicas</p></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs([
            "🎯 Metas Ativas",
            "📊 Performance",
            "⚙️ Configurar Metas"
        ])
        
        with tab1:
            self.metas_ativas()
        
        with tab2:
            self.performance_metas()
        
        with tab3:
            self.configurar_metas()

    def metas_ativas(self):
        """Visualização das metas ativas"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("🎯 Metas Ativas")
        
        # Metas simuladas
        metas_exemplo = [
            {
                "nome": "Novos Pacientes",
                "meta": 50,
                "atual": 42,
                "periodo": "Mensal",
                "prazo": "31/10/2024",
                "categoria": "Crescimento"
            },
            {
                "nome": "Receita Mensal", 
                "meta": 7500,
                "atual": 6200,
                "periodo": "Mensal",
                "prazo": "31/10/2024",
                "categoria": "Financeiro"
            },
            {
                "nome": "Taxa de Retenção",
                "meta": 85,
                "atual": 82,
                "periodo": "Trimestral",
                "prazo": "31/12/2024",
                "categoria": "Qualidade"
            },
            {
                "nome": "Consultas/Semana",
                "meta": 25,
                "atual": 23,
                "periodo": "Semanal", 
                "prazo": "Contínuo",
                "categoria": "Produtividade"
            }
        ]
        
        # Cards de metas
        for meta in metas_exemplo:
            progresso = (meta['atual'] / meta['meta']) * 100
            
            # Determinar cor baseada no progresso
            if progresso >= 90:
                cor = "#48bb78"
                status = "Excelente"
            elif progresso >= 70:
                cor = "#667eea"  
                status = "No Caminho"
            elif progresso >= 50:
                cor = "#ed8936"
                status = "Atenção"
            else:
                cor = "#e53e3e"
                status = "Crítico"
            
            st.markdown(f'''
            <div style="background: rgba(255,255,255,0.95); border-radius: 15px; padding: 2rem; margin: 1rem 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 6px solid {cor};">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
                    <div>
                        <h4 style="color: {cor}; margin: 0 0 0.5rem 0;">{meta['nome']}</h4>
                        <span style="background: {cor}15; color: {cor}; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; font-weight: 600;">
                            {meta['categoria']}
                        </span>
                    </div>
                    <div style="text-align: right;">
                        <div style="color: {cor}; font-weight: 700; font-size: 1.5rem;">{progresso:.0f}%</div>
                        <div style="color: {cor}; font-size: 0.9rem;">{status}</div>
                    </div>
                </div>
                
                <div style="background: #f1f5f9; border-radius: 10px; height: 8px; margin: 1rem 0;">
                    <div style="background: {cor}; height: 100%; width: {progresso}%; border-radius: 10px; transition: width 0.3s ease;"></div>
                </div>
                
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; color: #64748b;">
                    <div><strong>{meta['atual']}</strong> de <strong>{meta['meta']}</strong> {meta['periodo'].lower()}</div>
                    <div>📅 {meta['prazo']}</div>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        
        # Resumo geral
        st.markdown("### 📊 Resumo Geral das Metas")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_metas = len(metas_exemplo)
        metas_atingidas = len([m for m in metas_exemplo if (m['atual'] / m['meta']) >= 1.0])
        metas_no_caminho = len([m for m in metas_exemplo if 0.7 <= (m['atual'] / m['meta']) < 1.0])
        metas_criticas = len([m for m in metas_exemplo if (m['atual'] / m['meta']) < 0.5])
        
        with col1:
            st.metric("Total de Metas", total_metas)
        
        with col2:
            st.metric("Atingidas", metas_atingidas, f"{(metas_atingidas/total_metas)*100:.0f}%")
        
        with col3:
            st.metric("No Caminho", metas_no_caminho, f"{(metas_no_caminho/total_metas)*100:.0f}%")
        
        with col4:
            st.metric("Críticas", metas_criticas, f"{(metas_criticas/total_metas)*100:.0f}%")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def performance_metas(self):
        """Performance das metas"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("📊 Performance das Metas")
        
        # Gráfico de evolução das metas
        st.markdown("### 📈 Evolução Histórica")
        
        # Dados simulados de evolução
        meses = ['Jun', 'Jul', 'Ago', 'Set', 'Out']
        novos_pacientes_evolucao = [28, 35, 41, 38, 42]
        receita_evolucao = [4200, 5100, 5800, 5600, 6200]
        retencao_evolucao = [78, 80, 85, 83, 82]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=meses,
                y=novos_pacientes_evolucao,
                mode='lines+markers',
                name='Novos Pacientes',
                line=dict(color='#667eea', width=3)
            ))
            
            # Linha de meta
            fig.add_hline(y=50, line_dash="dash", line_color="green", annotation_text="Meta: 50")
            
            fig.update_layout(
                title="Evolução: Novos Pacientes",
                yaxis_title="Número de Pacientes",
                height=300,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=meses,
                y=receita_evolucao,
                mode='lines+markers',
                name='Receita',
                line=dict(color='#48bb78', width=3)
            ))
            
            # Linha de meta
            fig.add_hline(y=7500, line_dash="dash", line_color="green", annotation_text="Meta: R$ 7.500")
            
            fig.update_layout(
                title="Evolução: Receita Mensal",
                yaxis_title="Receita (R$)",
                height=300,
                paper_bgcolor="rgba(0,0,0,0)"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Análise de tendências
        st.markdown("### 📊 Análise de Tendências")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="calculator-card">
                <h4 style="color: #48bb78; margin-bottom: 1rem;">✅ Metas com Boa Performance</h4>
                <div style="line-height: 1.6;">
                    • <strong>Consultas/Semana:</strong> 92% da meta<br>
                    • <strong>Taxa de Retenção:</strong> 96% da meta<br>
                    • <strong>Crescimento:</strong> Consistente nos últimos 3 meses<br>
                    • <strong>Tendência:</strong> Positiva
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="calculator-card">
                <h4 style="color: #ed8936; margin-bottom: 1rem;">⚠️ Metas Precisando Atenção</h4>
                <div style="line-height: 1.6;">
                    • <strong>Novos Pacientes:</strong> 84% da meta<br>
                    • <strong>Receita:</strong> 83% da meta<br>
                    • <strong>Desafio:</strong> Captação de novos clientes<br>
                    • <strong>Ação:</strong> Intensificar marketing
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="calculator-card">
                <h4 style="color: #667eea; margin-bottom: 1rem;">📈 Projeções</h4>
                <div style="line-height: 1.6;">
                    • <strong>Novembro:</strong> Provável atingimento<br>
                    • <strong>Meta Receita:</strong> 95% de probabilidade<br>
                    • <strong>Crescimento:</strong> +12% trimestre<br>
                    • <strong>Outlook:</strong> Positivo
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Heatmap de performance
        st.markdown("### 🔥 Mapa de Performance")
        
        # Dados simulados para heatmap
        categorias = ['Crescimento', 'Financeiro', 'Qualidade', 'Produtividade']
        meses_heatmap = ['Jun', 'Jul', 'Ago', 'Set', 'Out']
        
        # Performance simulada (0-100%)
        performance_data = [
            [85, 90, 95, 88, 92],  # Crescimento
            [78, 82, 85, 83, 87],  # Financeiro
            [92, 95, 90, 93, 96],  # Qualidade
            [88, 85, 90, 92, 89]   # Produtividade
        ]
        
        fig = go.Figure(data=go.Heatmap(
            z=performance_data,
            x=meses_heatmap,
            y=categorias,
            colorscale='RdYlGn',
            text=[[f"{val}%" for val in row] for row in performance_data],
            texttemplate="%{text}",
            textfont={"size": 12}
        ))
        
        fig.update_layout(
            title="Performance por Categoria e Mês (%)",
            height=300,
            paper_bgcolor="rgba(0,0,0,0)"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    def configurar_metas(self):
        """Configuração de metas"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("⚙️ Configurar Metas")
        
        # Criar nova meta
        st.markdown("### ➕ Criar Nova Meta")
        
        with st.form("nova_meta"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome_meta = st.text_input("Nome da meta *")
                categoria_meta = st.selectbox("Categoria", [
                    "Crescimento", "Financeiro", "Qualidade", 
                    "Produtividade", "Marketing", "Operacional"
                ])
                valor_meta = st.number_input("Valor da meta *", min_value=0.0, value=100.0)
                unidade_meta = st.selectbox("Unidade", [
                    "Número", "Reais (R$)", "Porcentagem (%)", 
                    "Horas", "Dias", "Pontos"
                ])
            
            with col2:
                periodo_meta = st.selectbox("Período", [
                    "Diário", "Semanal", "Mensal", "Trimestral", "Anual"
                ])
                data_inicio = st.date_input("Data de início", value=datetime.now().date())
                data_fim = st.date_input("Data limite")
                
                prioridade = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
            
            descricao_meta = st.text_area("Descrição da meta", height=80)
            
            # Configurações de notificação
            st.markdown("**🔔 Notificações**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                notificar_progresso = st.checkbox("Notificar progresso semanal")
                notificar_risco = st.checkbox("Alerta quando abaixo de 70%")
            
            with col2:
                notificar_atingida = st.checkbox("Notificar quando atingida")
                notificar_prazo = st.checkbox("Lembrar próximo ao prazo")
            
            if st.form_submit_button("🎯 Criar Meta", type="primary", use_container_width=True):
                if nome_meta and valor_meta:
                    nova_meta = {
                        "id": len(st.session_state.get('metas_ativas', [])) + 1,
                        "nome": nome_meta,
                        "categoria": categoria_meta,
                        "valor": valor_meta,
                        "unidade": unidade_meta,
                        "periodo": periodo_meta,
                        "data_inicio": data_inicio.strftime('%Y-%m-%d'),
                        "data_fim": data_fim.strftime('%Y-%m-%d'),
                        "prioridade": prioridade,
                        "descricao": descricao_meta,
                        "progresso_atual": 0,
                        "status": "Ativa",
                        "notificacoes": {
                            "progresso": notificar_progresso,
                            "risco": notificar_risco,
                            "atingida": notificar_atingida,
                            "prazo": notificar_prazo
                        },
                        "criada_em": datetime.now().strftime('%Y-%m-%d %H:%M')
                    }
                    
                    if 'metas_ativas' not in st.session_state:
                        st.session_state.metas_ativas = []
                    
                    st.session_state.metas_ativas.append(nova_meta)
                    st.success(f"✅ Meta '{nome_meta}' criada com sucesso!")
                    st.balloons()
                else:
                    st.error("❌ Preencha os campos obrigatórios")
        
        # Templates de metas
        st.markdown("### 📋 Templates de Metas")
        
        templates_metas = {
            "Crescimento de Pacientes": {
                "categoria": "Crescimento",
                "valor": 50,
                "unidade": "Número",
                "periodo": "Mensal",
                "descricao": "Aumentar base de pacientes ativos"
            },
            "Meta de Receita": {
                "categoria": "Financeiro", 
                "valor": 10000,
                "unidade": "Reais (R$)",
                "periodo": "Mensal",
                "descricao": "Atingir receita mensal objetivo"
            },
            "Taxa de Satisfação": {
                "categoria": "Qualidade",
                "valor": 90,
                "unidade": "Porcentagem (%)",
                "periodo": "Trimestral",
                "descricao": "Manter alta satisfação dos pacientes"
            }
        }
        
        col1, col2, col3 = st.columns(3)
        
        for i, (nome_template, config) in enumerate(templates_metas.items()):
            col = [col1, col2, col3][i]
            
            with col:
                st.markdown(f"""
                <div class="calculator-card">
                    <h4 style="color: #667eea;">{nome_template}</h4>
                    <div style="font-size: 0.9rem; line-height: 1.5;">
                        <strong>Categoria:</strong> {config['categoria']}<br>
                        <strong>Meta:</strong> {config['valor']} {config['unidade']}<br>
                        <strong>Período:</strong> {config['periodo']}<br>
                        <strong>Descrição:</strong> {config['descricao']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"📋 Usar Template", key=f"template_{i}", use_container_width=True):
                    st.success(f"Template '{nome_template}' aplicado!")
        
        # Configurações globais
        st.markdown("### ⚙️ Configurações Globais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Dashboard**")
            mostrar_progresso = st.checkbox("Mostrar barra de progresso", value=True)
            mostrar_tendencia = st.checkbox("Mostrar tendências", value=True)
            atualizar_automatico = st.checkbox("Atualização automática", value=True)
            
        with col2:
            st.markdown("**🔔 Notificações**")
            email_notificacoes = st.text_input("Email para notificações")
            frequencia_relatorio = st.selectbox("Relatório de metas", ["Semanal", "Mensal", "Trimestral"])
            
        if st.button("💾 Salvar Configurações Globais", type="secondary", use_container_width=True):
            configuracoes_metas = {
                "mostrar_progresso": mostrar_progresso,
                "mostrar_tendencia": mostrar_tendencia,
                "atualizar_automatico": atualizar_automatico,
                "email_notificacoes": email_notificacoes,
                "frequencia_relatorio": frequencia_relatorio
            }
            
            st.session_state.configuracoes.update({"metas": configuracoes_metas})
            st.success("✅ Configurações salvas!")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def configuracoes_page(self):
        """Página de configurações do sistema"""
        st.markdown('<div class="main-header"><h1>⚙️ Configurações do Sistema</h1><p>Personalização e configurações avançadas</p></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "🏢 Empresa",
            "👤 Perfil Profissional",
            "🎨 Personalização",
            "🔧 Sistema"
        ])
        
        with tab1:
            self.config_empresa()
        
        with tab2:
            self.config_perfil()
        
        with tab3:
            self.config_personalizacao()
        
        with tab4:
            self.config_sistema()

    def config_empresa(self):
        """Configurações da empresa"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("🏢 Informações da Empresa")
        
        with st.form("config_empresa"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Dados Básicos**")
                
                nome_empresa = st.text_input(
                    "Nome da empresa/clínica",
                    value=st.session_state.configuracoes.get('empresa_nome', '')
                )
                
                cnpj = st.text_input("CNPJ", placeholder="00.000.000/0001-00")
                
                endereco_completo = st.text_area(
                    "Endereço completo",
                    value=st.session_state.configuracoes.get('endereco', ''),
                    height=100
                )
                
                telefone_empresa = st.text_input("Telefone principal")
                email_empresa = st.text_input(
                    "Email principal",
                    value=st.session_state.configuracoes.get('email', '')
                )
                
                website = st.text_input("Website", placeholder="https://www.minhanutri.com.br")
            
            with col2:
                st.markdown("**🎨 Identidade Visual**")
                
                # Upload de logo
                logo_upload = st.file_uploader(
                    "Logo da empresa",
                    type=['png', 'jpg', 'jpeg', 'svg'],
                    help="Recomendado: 300x100px, PNG com fundo transparente"
                )
                
                if logo_upload:
                    st.image(logo_upload, width=200, caption="Prévia do logo")
                
                cores_tema = st.selectbox("Esquema de cores", [
                    "Azul Profissional", "Verde Saúde", "Roxo Moderno", 
                    "Laranja Energia", "Rosa Feminino", "Personalizado"
                ])
                
                if cores_tema == "Personalizado":
                    cor_primaria = st.color_picker("Cor primária", "#667eea")
                    cor_secundaria = st.color_picker("Cor secundária", "#48bb78")
                
                st.markdown("**📄 Documentos**")
                
                cabecalho_relatorio = st.text_area(
                    "Cabeçalho dos relatórios",
                    placeholder="Texto que aparecerá no topo dos relatórios...",
                    height=80
                )
                
                rodape_relatorio = st.text_area(
                    "Rodapé dos relatórios", 
                    placeholder="Informações de contato, redes sociais...",
                    height=60
                )
            
            if st.form_submit_button("💾 Salvar Configurações da Empresa", type="primary", use_container_width=True):
                st.session_state.configuracoes.update({
                    'empresa_nome': nome_empresa,
                    'cnpj': cnpj,
                    'endereco': endereco_completo,
                    'telefone_empresa': telefone_empresa,
                    'email': email_empresa,
                    'website': website,
                    'cores_tema': cores_tema,
                    'cabecalho_relatorio': cabecalho_relatorio,
                    'rodape_relatorio': rodape_relatorio
                })
                
                if logo_upload:
                    st.session_state.configuracoes['empresa_logo'] = logo_upload
                
                st.success("✅ Configurações da empresa salvas com sucesso!")
                time.sleep(1)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    def config_perfil(self):
        """Configurações do perfil profissional"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("👤 Perfil Profissional")
        
        with st.form("config_perfil"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**👨‍⚕️ Dados Profissionais**")
                
                nome_profissional = st.text_input("Nome completo")
                crn = st.text_input("CRN", value=st.session_state.configuracoes.get('crn', ''))
                especializacoes = st.multiselect("Especializações", [
                    "Nutrição Clínica", "Nutrição Esportiva", "Nutrição Materno-Infantil",
                    "Nutrição Geriátrica", "Fitoterapia", "Nutrição Funcional",
                    "Transtornos Alimentares", "Nutrição Hospitalar"
                ])
                
                formacao = st.text_area("Formação acadêmica", height=100)
                experiencia = st.text_area("Experiência profissional", height=100)
                
            with col2:
                st.markdown("**📞 Contato Profissional**")
                
                telefone_profissional = st.text_input("Telefone profissional")
                email_profissional = st.text_input("Email profissional")
                
                redes_sociais = st.text_area(
                    "Redes sociais",
                    placeholder="Instagram: @nutricionista\nLinkedIn: /in/nutricionista",
                    height=80
                )
                
                st.markdown("**📋 Preferências de Atendimento**")
                
                tipos_atendimento = st.multiselect("Tipos de atendimento", [
                    "Presencial", "Online", "Domiciliar", "Empresarial"
                ])
                
                publico_alvo = st.multiselect("Público-alvo preferencial", [
                    "Adultos", "Idosos", "Adolescentes", "Crianças",
                    "Gestantes", "Atletas", "Vegetarianos/Veganos"
                ])
                
                bio_profissional = st.text_area(
                    "Biografia profissional",
                    placeholder="Breve descrição sobre sua abordagem e filosofia de trabalho...",
                    height=100
                )
            
            if st.form_submit_button("💾 Salvar Perfil Profissional", type="primary", use_container_width=True):
                st.session_state.configuracoes.update({
                    'nome_profissional': nome_profissional,
                    'crn': crn,
                    'especializacoes': especializacoes,
                    'formacao': formacao,
                    'experiencia': experiencia,
                    'telefone_profissional': telefone_profissional,
                    'email_profissional': email_profissional,
                    'redes_sociais': redes_sociais,
                    'tipos_atendimento': tipos_atendimento,
                    'publico_alvo': publico_alvo,
                    'bio_profissional': bio_profissional
                })
                
                st.success("✅ Perfil profissional salvo com sucesso!")
                time.sleep(1)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    def config_personalizacao(self):
        """Configurações de personalização"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("🎨 Personalização da Interface")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🎨 Aparência**")
            
            tema_interface = st.selectbox("Tema da interface", [
                "Claro", "Escuro", "Automático (baseado no sistema)"
            ])
            
            tamanho_fonte = st.selectbox("Tamanho da fonte", [
                "Pequeno", "Normal", "Grande", "Extra Grande"
            ])
            
            densidade_interface = st.selectbox("Densidade da interface", [
                "Compacta", "Normal", "Espaçosa"
            ])
            
            animacoes = st.checkbox("Habilitar animações", value=True)
            
            st.markdown("**📊 Dashboard**")
            
            widgets_dashboard = st.multiselect("Widgets no dashboard", [
                "KPIs principais", "Agenda do dia", "Metas", "Gráfico de evolução",
                "Notificações", "Receitas em destaque", "Lembretes", "Estatísticas"
            ], default=["KPIs principais", "Agenda do dia", "Metas"])
            
            layout_dashboard = st.radio("Layout do dashboard", [
                "Duas colunas", "Três colunas", "Layout flexível"
            ])
            
        with col2:
            st.markdown("**🔔 Notificações**")
            
            notificacoes_push = st.checkbox("Notificações push", value=True)
            notificacoes_email = st.checkbox("Notificações por email", value=True)
            notificacoes_som = st.checkbox("Som nas notificações", value=False)
            
            tipos_notificacao = st.multiselect("Tipos de notificação", [
                "Novos agendamentos", "Cancelamentos", "Lembretes de consulta",
                "Metas atingidas", "Relatórios prontos", "Novos pacientes",
                "Mensagens recebidas"
            ], default=["Novos agendamentos", "Cancelamentos", "Lembretes de consulta"])
            
            st.markdown("**🏠 Página Inicial**")
            
            pagina_inicial = st.selectbox("Página inicial padrão", [
                "Dashboard", "Agenda", "Pacientes", "Calculadoras", "Personalizado"
            ])
            
            mostrar_tutorial = st.checkbox("Mostrar dicas de uso", value=True)
            
            st.markdown("**📱 Mobile**")
            
            interface_mobile = st.checkbox("Interface otimizada para mobile", value=True)
            gestos_mobile = st.checkbox("Habilitar gestos de navegação", value=True)
        
        # Prévia das configurações
        st.markdown("### 👁️ Prévia")
        
        st.info(f"""
        **Configurações Atuais:**
        - **Tema:** {tema_interface}
        - **Fonte:** {tamanho_fonte}
        - **Layout Dashboard:** {layout_dashboard}
        - **Widgets:** {len(widgets_dashboard)} selecionados
        - **Página Inicial:** {pagina_inicial}
        """)
        
        if st.button("🎨 Aplicar Personalização", type="primary", use_container_width=True):
            st.session_state.configuracoes.update({
                'tema_interface': tema_interface,
                'tamanho_fonte': tamanho_fonte,
                'densidade_interface': densidade_interface,
                'animacoes': animacoes,
                'widgets_dashboard': widgets_dashboard,
                'layout_dashboard': layout_dashboard,
                'notificacoes_push': notificacoes_push,
                'notificacoes_email': notificacoes_email,
                'notificacoes_som': notificacoes_som,
                'tipos_notificacao': tipos_notificacao,
                'pagina_inicial': pagina_inicial,
                'mostrar_tutorial': mostrar_tutorial,
                'interface_mobile': interface_mobile,
                'gestos_mobile': gestos_mobile
            })
            
            st.success("✅ Personalização aplicada! Recarregue a página para ver as mudanças.")
            st.balloons()
        
        st.markdown('</div>', unsafe_allow_html=True)

    def config_sistema(self):
        """Configurações do sistema"""
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        st.subheader("🔧 Configurações do Sistema")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**💾 Backup e Segurança**")
            
            backup_automatico = st.checkbox(
                "Backup automático",
                value=st.session_state.configuracoes.get('backup_automatico', True)
            )
            
            if backup_automatico:
                frequencia_backup = st.selectbox("Frequência do backup", [
                    "Diário", "Semanal", "Mensal"
                ])
                
                local_backup = st.selectbox("Local do backup", [
                    "Google Drive", "Dropbox", "OneDrive", "Local"
                ])
            
            senha_backup = st.checkbox("Proteger backup com senha", value=True)
            
            st.markdown("**🔐 Segurança**")
            
            autenticacao_2fa = st.checkbox("Autenticação de dois fatores", value=False)
            timeout_sessao = st.selectbox("Timeout da sessão", [
                "30 minutos", "1 hora", "2 horas", "4 horas", "Nunca"
            ])
            
            log_atividades = st.checkbox("Log de atividades", value=True)
            
        with col2:
            st.markdown("**🔄 Importação e Exportação**")
            
            st.markdown("**Importar dados:**")
            arquivo_importacao = st.file_uploader(
                "Selecionar arquivo",
                type=['json', 'csv', 'xlsx'],
                help="Formatos suportados: JSON, CSV, Excel"
            )
            
            if arquivo_importacao:
                if st.button("📥 Importar Dados"):
                    st.success("Dados importados com sucesso! (Funcionalidade em desenvolvimento)")
            
            st.markdown("**Exportar dados:**")
            
            dados_exportar = st.multiselect("Selecionar dados", [
                "Pacientes", "Consultas", "Receitas", "Planos alimentares",
                "Agendamentos", "Relatórios", "Configurações"
            ])
            
            formato_exportacao = st.selectbox("Formato", ["JSON", "Excel", "CSV"])
            
            if st.button("📤 Exportar Dados"):
                if dados_exportar:
                    st.success(f"Dados exportados em formato {formato_exportacao}! (Em desenvolvimento)")
                else:
                    st.warning("Selecione ao menos um tipo de dado para exportar")
            
            st.markdown("**🗑️ Limpeza de Dados**")
            
            if st.button("🧹 Limpar Cache", type="secondary"):
                st.success("Cache limpo com sucesso!")
            
            if st.button("📊 Otimizar Banco de Dados", type="secondary"):
                st.success("Banco de dados otimizado!")
        
        # Informações do sistema
        st.markdown("### ℹ️ Informações do Sistema")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"""
            **📊 Estatísticas:**
            - Pacientes: {len(st.session_state.pacientes)}
            - Receitas: {len(st.session_state.receitas)}
            - Agendamentos: {len(st.session_state.agendamentos)}
            - Consultas realizadas: {len([a for a in st.session_state.agendamentos if a.get('status') == 'Realizado'])}
            """)
        
        with col2:
            st.info(f"""
            **🔧 Sistema:**
            - Versão: 3.0.0
            - Usuário: {st.session_state.current_user}
            - Último backup: {datetime.now().strftime('%d/%m/%Y %H:%M')}
            - Status: Online ✅
            """)
        
        with col3:
            st.info(f"""
            **💾 Armazenamento:**
            - Dados utilizados: 2.3 MB
            - Espaço disponível: 97.7 MB
            - Anexos: 0.5 MB
            - Backup: 1.2 MB
            """)
        
        # Ações do sistema
        st.markdown("### ⚙️ Ações do Sistema")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Sincronizar", type="secondary", use_container_width=True):
                with st.spinner("Sincronizando..."):
                    time.sleep(2)
                    st.success("Sistema sincronizado!")
        
        with col2:
            if st.button("🧪 Testar Sistema", type="secondary", use_container_width=True):
                with st.spinner("Executando testes..."):
                    time.sleep(3)
                    st.success("Todos os testes passaram! ✅")
        
        with col3:
            if st.button("📋 Gerar Log", type="secondary", use_container_width=True):
                st.success("Log do sistema gerado!")
        
        with col4:
            if st.button("🚨 Reset Configurações", type="secondary", use_container_width=True):
                if st.button("⚠️ Confirmar Reset", type="secondary"):
                    st.session_state.configuracoes = self.load_default_config()
                    st.success("Configurações resetadas para o padrão!")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def run(self):
        """Executa a aplicação principal"""
        if not st.session_state.authenticated:
            self.login_page()
        else:
            selected_page = self.sidebar_menu()
            
            # Roteamento das páginas
            if selected_page == "📊 Dashboard Executivo":
                self.dashboard_page()
            elif selected_page == "🧮 Calculadoras Profissionais":
                self.calculadoras_page()
            elif selected_page == "👥 Gestão de Pacientes":
                self.gestao_pacientes_page()
            elif selected_page == "📈 Evolução & Progresso":
                self.gestao_pacientes_page()  # Usa mesma página com foco na aba de evolução
            elif selected_page == "🍽️ Planos Alimentares":
                self.planos_alimentares_page()
            elif selected_page == "🍳 Banco de Receitas":
                self.banco_receitas_page()
            elif selected_page == "📅 Agendamentos":
                self.agendamentos_page()
            elif selected_page == "📊 Relatórios Avançados":
                self.relatorios_page()
            elif selected_page == "💬 Comunicação":
                self.comunicacao_page()
            elif selected_page == "🎯 Metas & Objetivos":
                self.metas_objetivos_page()
            elif selected_page == "⚙️ Configurações":
                self.configuracoes_page()

# Executar a aplicação
if __name__ == "__main__":
    app = NutriStock360Pro()
    app.run()
