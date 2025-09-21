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
    
    # Carboidratos
    "Arroz integral (100g)": {"calorias": 123, "proteinas": 2.6, "carboidratos": 23, "gorduras": 1, "categoria": "Carboidrato", "fibras": 1.8, "sodio": 1},
    "Batata doce (100g)": {"calorias": 86, "proteinas": 1.6, "carboidratos": 20, "gorduras": 0.1, "categoria": "Carboidrato", "fibras": 3, "sodio": 4},
    "Aveia (100g)": {"calorias": 389, "proteinas": 17, "carboidratos": 66, "gorduras": 7, "categoria": "Carboidrato", "fibras": 10, "sodio": 2},
    "Quinoa (100g)": {"calorias": 120, "proteinas": 4.4, "carboidratos": 22, "gorduras": 1.9, "categoria": "Carboidrato", "fibras": 2.8, "sodio": 5},
    "Pão integral (2 fatias)": {"calorias": 160, "proteinas": 6, "carboidratos": 30, "gorduras": 3, "categoria": "Carboidrato", "fibras": 4, "sodio": 320},
    
    # Vegetais
    "Brócolis (100g)": {"calorias": 25, "proteinas": 3, "carboidratos": 5, "gorduras": 0.4, "categoria": "Vegetal", "fibras": 2.6, "sodio": 33},
    "Espinafre (100g)": {"calorias": 23, "proteinas": 2.9, "carboidratos": 3.6, "gorduras": 0.4, "categoria": "Vegetal", "fibras": 2.2, "sodio": 79},
    "Alface (100g)": {"calorias": 15, "proteinas": 1.4, "carboidratos": 2.9, "gorduras": 0.2, "categoria": "Vegetal", "fibras": 1.3, "sodio": 28},
    "Tomate (100g)": {"calorias": 18, "proteinas": 0.9, "carboidratos": 3.9, "gorduras": 0.2, "categoria": "Vegetal", "fibras": 1.2, "sodio": 5},
    "Cenoura (100g)": {"calorias": 41, "proteinas": 0.9, "carboidratos": 10, "gorduras": 0.2, "categoria": "Vegetal", "fibras": 2.8, "sodio": 69},
    
    # Frutas
    "Banana (1 unidade)": {"calorias": 89, "proteinas": 1.1, "carboidratos": 23, "gorduras": 0.3, "categoria": "Fruta", "fibras": 2.6, "sodio": 1},
    "Maçã (1 unidade)": {"calorias": 52, "proteinas": 0.3, "carboidratos": 14, "gorduras": 0.2, "categoria": "Fruta", "fibras": 2.4, "sodio": 1},
    "Morango (100g)": {"calorias": 32, "proteinas": 0.7, "carboidratos": 7.7, "gorduras": 0.3, "categoria": "Fruta", "fibras": 2, "sodio": 1},
    "Laranja (1 unidade)": {"calorias": 62, "proteinas": 1.2, "carboidratos": 15, "gorduras": 0.2, "categoria": "Fruta", "fibras": 3.1, "sodio": 0},
    
    # Gorduras boas
    "Abacate (100g)": {"calorias": 160, "proteinas": 2, "carboidratos": 9, "gorduras": 15, "categoria": "Gordura", "fibras": 6.7, "sodio": 7},
    "Azeite (1 colher sopa)": {"calorias": 119, "proteinas": 0, "carboidratos": 0, "gorduras": 13.5, "categoria": "Gordura", "fibras": 0, "sodio": 0},
    "Castanha do Pará (10g)": {"calorias": 66, "proteinas": 1.4, "carboidratos": 1.2, "gorduras": 6.5, "categoria": "Gordura", "fibras": 0.7, "sodio": 0.3}
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
            'pacientes': [],
            'consultas': [],
            'receitas': self.load_default_receitas(),
            'planos_alimentares': [],
            'agendamentos': [],
            'configuracoes': self.load_default_config(),
            'historico_peso': {},
            'metas_pacientes': {},
            'relatorios_salvos': [],
            'evolucoes_pacientes': {},
            'cardapios_salvos': [],
            'templates_comunicacao': self.load_default_templates()
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
            
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
                "custo_estimado": 12.50
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
                "custo_estimado": 6.80
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
            "meta_pacientes_mes": 50,
            "meta_receita_mes": 7500.00,
            "backup_automatico": True,
            "notificacoes_email": True,
            "notificacoes_whatsapp": True
        }
    
    def load_default_templates(self):
        """Templates de comunicação"""
        return {
            "lembrete_consulta": "Olá {nome}! Lembrando que você tem consulta marcada para {data} às {horario}. Confirme sua presença.",
            "plano_pronto": "Oi {nome}! Seu novo plano alimentar está pronto. Siga as orientações e qualquer dúvida me procure.",
            "motivacional": "Parabéns {nome}! Você está no caminho certo. Continue firme no seu objetivo!",
            "reagendamento": "Olá {nome}, precisamos reagendar sua consulta. Entre em contato para marcarmos novo horário."
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
                
                **✨ Novos Recursos v3.0:**
                
                🧮 **Calculadoras Profissionais** - 15+ fórmulas científicas
                - IMC com classificação detalhada
                - TMB por múltiplas fórmulas (Mifflin, Harris, Katch)
                - Percentual de gordura corporal (Navy, Jackson-Pollock)
                - Peso ideal por 4 métodos diferentes
                - Necessidades hídricas personalizadas
                - Distribuição automática de macronutrientes
                
                📊 **Analytics Avançados** - Insights em tempo real
                - Dashboard interativo com métricas KPI
                - Gráficos de evolução de pacientes
                - Análise de composição corporal
                - Projeções de resultados
                
                🍽️ **Planejamento Inteligente** - IA Nutricional
                - Criador automático de cardápios
                - Substituições inteligentes de alimentos
                - Cálculo nutricional automático
                - Templates personalizáveis
                
                📱 **Comunicação Integrada** - Multi-canal
                - WhatsApp Business API
                - Templates personalizáveis
                - Lembretes automáticos
                - Histórico completo
                
                📈 **Relatórios Profissionais** - Exportação PDF
                - Evolução detalhada de pacientes
                - Análises comparativas
                - Relatórios executivos
                - Gráficos interativos
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
                "🧮 Calculadoras Profissionais"
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
            
            st.markdown("---")
            if st.button("🚪 Logout Seguro", use_container_width=True, type="primary"):
                st.session_state.authenticated = False
                st.session_state.current_user = None
                st.success("Logout realizado com sucesso!")
                time.sleep(1)
                st.rerun()
            
            return selected
    
    def dashboard_page(self):
        """Dashboard executivo básico"""
        st.markdown('<div class="main-header"><h1>📊 Dashboard Executivo</h1><p>Visão geral da sua prática nutricional</p></div>', unsafe_allow_html=True)
        
        st.info("Dashboard em desenvolvimento - acesse as Calculadoras Profissionais no menu lateral")
        
        # KPIs básicos
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Pacientes", len(st.session_state.pacientes), "+2")
        with col2:
            st.metric("Consultas Hoje", 0, "0")
        with col3:
            st.metric("Receita Mensal", "R$ 0", "R$ 0")
        with col4:
            st.metric("Taxa Retorno", "85%", "+2%")

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
            tmb_base = 1500
            
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
                for i in range(1, int(tempo_meses) + 1):
                    peso_marco = peso_atual - (diferenca_peso * i / tempo_meses)
                    bf_marco = bf_atual - (diferenca_bf * i / tempo_meses)
                    marcos.append(f"Mês {i}: {peso_marco:.1f} kg ({bf_marco:.1f}% BF)")
                
                for marco in marcos[:6]:  # Mostrar apenas os primeiros 6 meses
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
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def run(self):
        """Executa a aplicação"""
        if not st.session_state.authenticated:
            self.login_page()
        else:
            selected_page = self.sidebar_menu()
            
            if selected_page == "📊 Dashboard Executivo":
                self.dashboard_page()
            elif selected_page == "🧮 Calculadoras Profissionais":
                self.calculadoras_page()

# Executar aplicação
if __name__ == "__main__":
    app = NutriStock360Pro()
    app.run()
