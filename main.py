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

# CSS customizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .sidebar-logo {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .calculator-result {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
    }
    .status-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        text-align: center;
        font-weight: bold;
    }
    .status-normal { background: #d4edda; color: #155724; }
    .status-warning { background: #fff3cd; color: #856404; }
    .status-danger { background: #f8d7da; color: #721c24; }
    .tab-content {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    .food-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .appointment-card {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Banco de dados expandido
ALIMENTOS_DB = {
    # Proteínas
    "Frango grelhado (100g)": {"calorias": 165, "proteinas": 31, "carboidratos": 0, "gorduras": 3.6, "categoria": "Proteína"},
    "Salmão grelhado (100g)": {"calorias": 206, "proteinas": 22, "carboidratos": 0, "gorduras": 12, "categoria": "Proteína"},
    "Ovo cozido (1 unidade)": {"calorias": 68, "proteinas": 6, "carboidratos": 0.6, "gorduras": 4.8, "categoria": "Proteína"},
    "Peito de peru (100g)": {"calorias": 104, "proteinas": 24, "carboidratos": 0, "gorduras": 1, "categoria": "Proteína"},
    "Tilápia grelhada (100g)": {"calorias": 96, "proteinas": 20, "carboidratos": 0, "gorduras": 1.7, "categoria": "Proteína"},
    
    # Carboidratos
    "Arroz integral (100g)": {"calorias": 123, "proteinas": 2.6, "carboidratos": 23, "gorduras": 1, "categoria": "Carboidrato"},
    "Batata doce (100g)": {"calorias": 86, "proteinas": 1.6, "carboidratos": 20, "gorduras": 0.1, "categoria": "Carboidrato"},
    "Aveia (100g)": {"calorias": 389, "proteinas": 17, "carboidratos": 66, "gorduras": 7, "categoria": "Carboidrato"},
    "Quinoa (100g)": {"calorias": 120, "proteinas": 4.4, "carboidratos": 22, "gorduras": 1.9, "categoria": "Carboidrato"},
    "Pão integral (2 fatias)": {"calorias": 160, "proteinas": 6, "carboidratos": 30, "gorduras": 3, "categoria": "Carboidrato"},
    
    # Vegetais
    "Brócolis (100g)": {"calorias": 25, "proteinas": 3, "carboidratos": 5, "gorduras": 0.4, "categoria": "Vegetal"},
    "Espinafre (100g)": {"calorias": 23, "proteinas": 2.9, "carboidratos": 3.6, "gorduras": 0.4, "categoria": "Vegetal"},
    "Alface (100g)": {"calorias": 15, "proteinas": 1.4, "carboidratos": 2.9, "gorduras": 0.2, "categoria": "Vegetal"},
    "Tomate (100g)": {"calorias": 18, "proteinas": 0.9, "carboidratos": 3.9, "gorduras": 0.2, "categoria": "Vegetal"},
    "Cenoura (100g)": {"calorias": 41, "proteinas": 0.9, "carboidratos": 10, "gorduras": 0.2, "categoria": "Vegetal"},
    
    # Frutas
    "Banana (1 unidade)": {"calorias": 89, "proteinas": 1.1, "carboidratos": 23, "gorduras": 0.3, "categoria": "Fruta"},
    "Maçã (1 unidade)": {"calorias": 52, "proteinas": 0.3, "carboidratos": 14, "gorduras": 0.2, "categoria": "Fruta"},
    "Morango (100g)": {"calorias": 32, "proteinas": 0.7, "carboidratos": 7.7, "gorduras": 0.3, "categoria": "Fruta"},
    "Laranja (1 unidade)": {"calorias": 62, "proteinas": 1.2, "carboidratos": 15, "gorduras": 0.2, "categoria": "Fruta"},
    
    # Gorduras boas
    "Abacate (100g)": {"calorias": 160, "proteinas": 2, "carboidratos": 9, "gorduras": 15, "categoria": "Gordura"},
    "Azeite (1 colher sopa)": {"calorias": 119, "proteinas": 0, "carboidratos": 0, "gorduras": 13.5, "categoria": "Gordura"},
    "Castanha do Pará (10g)": {"calorias": 66, "proteinas": 1.4, "carboidratos": 1.2, "gorduras": 6.5, "categoria": "Gordura"}
}

class NutriStock360Pro:
    def __init__(self):
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
            'relatorios_salvos': []
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
            
    def load_default_receitas(self):
        """Carrega receitas padrão"""
        return [
            {
                "id": 1,
                "nome": "Salada Detox Completa",
                "ingredientes": ["Alface", "Rúcula", "Pepino", "Tomate cereja", "Azeite", "Limão"],
                "calorias": 95,
                "proteinas": 3,
                "carboidratos": 8,
                "gorduras": 7,
                "preparo": "Misture todos os vegetais, tempere com azeite e limão",
                "categoria": "Saladas",
                "tempo_preparo": "10 minutos",
                "dificuldade": "Fácil"
            },
            {
                "id": 2,
                "nome": "Smoothie Proteico Verde",
                "ingredientes": ["Espinafre", "Banana", "Whey protein", "Leite de amêndoas", "Aveia"],
                "calorias": 320,
                "proteinas": 25,
                "carboidratos": 35,
                "gorduras": 8,
                "preparo": "Bata tudo no liquidificador até ficar cremoso",
                "categoria": "Bebidas",
                "tempo_preparo": "5 minutos",
                "dificuldade": "Fácil"
            },
            {
                "id": 3,
                "nome": "Salmão com Quinoa",
                "ingredientes": ["Salmão", "Quinoa", "Brócolis", "Azeite", "Temperos"],
                "calorias": 450,
                "proteinas": 35,
                "carboidratos": 25,
                "gorduras": 22,
                "preparo": "Grelhe o salmão, cozinhe a quinoa e refogue o brócolis",
                "categoria": "Pratos Principais",
                "tempo_preparo": "25 minutos",
                "dificuldade": "Médio"
            }
        ]
    
    def load_default_config(self):
        """Configurações padrão"""
        return {
            "empresa_nome": "NutriClinic Pro",
            "empresa_logo": None,
            "cores_tema": "azul",
            "moeda": "BRL",
            "valor_consulta": 150.00,
            "tempo_consulta": 60,
            "horario_inicio": "08:00",
            "horario_fim": "18:00",
            "dias_trabalho": ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"],
            "whatsapp": "",
            "email": "",
            "endereco": ""
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
    
    def login_page(self):
        """Página de login"""
        st.markdown('''
        <div class="main-header">
            <h1>🥗 NutriStock360 Pro</h1>
            <p>Sistema Profissional Completo para Nutricionistas</p>
            <p><em>Versão 2.0 - Todos os Módulos Disponíveis</em></p>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="tab-content">
                <h3 style="text-align: center; color: #667eea;">🔐 Acesso ao Sistema</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
                password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
                remember = st.checkbox("🔄 Lembrar de mim")
                submitted = st.form_submit_button("🚀 Entrar no Sistema", use_container_width=True, type="primary")
                
                if submitted:
                    if self.authenticate_user(username, password):
                        st.success("✅ Login realizado com sucesso!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha incorretos!")
            
            with st.expander("👥 Usuários de Demonstração"):
                st.markdown("""
                **🔑 Credenciais de Teste:**
                - **Admin:** `admin` / `admin123`
                - **Nutricionista:** `nutricionista` / `nutri123`  
                - **Demo:** `demo` / `demo123`
                
                **✨ Módulos Disponíveis:**
                - 📊 Dashboard com métricas avançadas
                - 🧮 Calculadoras nutricionais profissionais
                - 👥 Gestão completa de pacientes
                - 🍽️ Criador inteligente de planos alimentares
                - 🍳 Banco de receitas com análise nutricional
                - 📅 Sistema de agendamentos
                - 📈 Relatórios profissionais
                - 💬 Comunicação integrada
                - ⚙️ Configurações personalizáveis
                """)
    
    def sidebar_menu(self):
        """Menu lateral"""
        with st.sidebar:
            st.markdown(f'''
            <div class="sidebar-logo">
                <h2>🥗 NutriStock360</h2>
                <p>Pro Dashboard</p>
                <small>v2.0 Completo</small>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f"**👤 Usuário:** {st.session_state.current_user}")
            st.markdown(f"**📅 Data:** {datetime.now().strftime('%d/%m/%Y')}")
            
            menu_options = [
                "📊 Dashboard Principal",
                "🧮 Calculadoras Nutricionais", 
                "👥 Gestão de Pacientes",
                "🍽️ Planos Alimentares",
                "🍳 Banco de Receitas",
                "📅 Agendamentos",
                "📈 Relatórios",
                "💬 Comunicação",
                "⚙️ Configurações"
            ]
            
            selected = st.selectbox("🧭 Navegação", menu_options, key="main_menu")
            
            # Estatísticas rápidas
            st.markdown("---")
            st.markdown("**📊 Estatísticas Rápidas**")
            st.metric("👥 Pacientes", len(st.session_state.pacientes))
            st.metric("📅 Consultas Hoje", len([a for a in st.session_state.agendamentos if a.get('data') == datetime.now().strftime('%Y-%m-%d')]))
            st.metric("🍳 Receitas", len(st.session_state.receitas))
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True, type="primary"):
                st.session_state.authenticated = False
                st.session_state.current_user = None
                st.rerun()
            
            return selected
    
    def dashboard_page(self):
        """Dashboard principal"""
        st.markdown('<div class="main-header"><h1>📊 Dashboard Executivo - NutriStock360 Pro</h1></div>', unsafe_allow_html=True)
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        total_pacientes = len(st.session_state.pacientes)
        consultas_hoje = len([a for a in st.session_state.agendamentos if a.get('data') == datetime.now().strftime('%Y-%m-%d')])
        receita_mensal = total_pacientes * st.session_state.configuracoes.get('valor_consulta', 150)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("👥 Pacientes Ativos", total_pacientes, "+3")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("📅 Consultas Hoje", consultas_hoje, "+2")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("💰 Receita Mensal", f"R$ {receita_mensal:,.2f}", "+15%")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("⭐ Satisfação", "4.8/5.0", "+0.2")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📈 Evolução de Pacientes")
            
            # Dados fictícios - corrigido para garantir mesmo tamanho
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            base_patients = [10, 15, 18, 25, 32, 38, 45, 52, 58, 65, 72, max(total_pacientes, 78)]
            
            # Garantir que ambos tenham o mesmo tamanho
            if len(meses) != len(base_patients):
                base_patients = base_patients[:len(meses)]
            
            patients_data = pd.DataFrame({'Mês': meses, 'Pacientes': base_patients})
            
            fig = px.line(patients_data, x='Mês', y='Pacientes', 
                         title="Crescimento de Pacientes 2024",
                         color_discrete_sequence=['#667eea'])
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🎯 Performance das Metas")
            
            categories = ['Novos Pacientes', 'Consultas', 'Receitas', 'Receita', 'Satisfação']
            values = [85, 92, 78, 95, 88]
            colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
            
            fig = go.Figure(data=[
                go.Bar(x=categories, y=values, marker_color=colors, text=values, textposition='auto')
            ])
            fig.update_layout(height=350, title="Progresso das Metas (%)")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Atividades recentes
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🕐 Atividades Recentes")
            
            activities = [
                "✅ 14:30 - Consulta concluída - Maria Silva",
                "ℹ️ 13:15 - Novo paciente: João Santos",
                "✅ 11:45 - Plano alimentar enviado - Ana Costa",
                "ℹ️ 10:30 - Receita adicionada: Salada Proteica",
                "✅ 09:15 - Backup automático realizado"
            ]
            
            for activity in activities:
                st.markdown(activity)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📅 Próximos Compromissos")
            
            if st.session_state.agendamentos:
                hoje = datetime.now().strftime('%Y-%m-%d')
                agendamentos_hoje = [a for a in st.session_state.agendamentos if a.get('data') == hoje]
                
                if agendamentos_hoje:
                    for apt in agendamentos_hoje:
                        st.markdown(f"🕐 {apt['horario']} - {apt['paciente']} - {apt['tipo']}")
                else:
                    st.info("Nenhum agendamento para hoje")
            else:
                st.info("Nenhum agendamento cadastrado")
            st.markdown('</div>', unsafe_allow_html=True)

    def calculadoras_page(self):
        """Página de calculadoras nutricionais"""
        st.markdown('<div class="main-header"><h1>🧮 Calculadoras Nutricionais Profissionais</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["🏋️ Básicas", "🔥 Metabólicas", "📊 Composição Corporal", "🎯 Objetivos"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📏 Calculadora de IMC")
                peso = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)
                altura = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01)
                
                if st.button("Calcular IMC", type="primary"):
                    imc = peso / (altura ** 2)
                    
                    if imc < 18.5:
                        status = "Abaixo do peso"
                        color_class = "status-warning"
                    elif 18.5 <= imc < 25:
                        status = "Peso normal"
                        color_class = "status-normal"
                    elif 25 <= imc < 30:
                        status = "Sobrepeso"
                        color_class = "status-warning"
                    else:
                        status = "Obesidade"
                        color_class = "status-danger"
                    
                    st.markdown(f'<div class="calculator-result">IMC: {imc:.1f}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="status-card {color_class}">Classificação: {status}</div>', unsafe_allow_html=True)
            
            with col2:
                st.subheader("⚖️ Peso Ideal")
                altura_ideal = st.number_input("Altura para peso ideal (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01)
                sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
                
                if st.button("Calcular Peso Ideal", type="primary"):
                    # Fórmula de Robinson
                    if sexo == "Masculino":
                        peso_ideal = 52 + (1.9 * ((altura_ideal * 100) - 152.4))
                    else:
                        peso_ideal = 49 + (1.7 * ((altura_ideal * 100) - 152.4))
                    
                    # Faixa de peso saudável
                    peso_min = 18.5 * (altura_ideal ** 2)
                    peso_max = 24.9 * (altura_ideal ** 2)
                    
                    st.markdown(f'<div class="calculator-result">Peso Ideal: {peso_ideal:.1f} kg</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="status-card status-normal">Faixa Saudável: {peso_min:.1f} - {peso_max:.1f} kg</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🔥 Calculadora Metabólica Completa")
            
            col1, col2 = st.columns(2)
            
            with col1:
                peso_tmb = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1, key="peso_tmb")
                altura_tmb = st.number_input("Altura (cm)", min_value=100, max_value=250, value=170, key="altura_tmb")
                idade = st.number_input("Idade (anos)", min_value=10, max_value=100, value=30)
                sexo_tmb = st.selectbox("Sexo", ["Masculino", "Feminino"], key="sexo_tmb")
            
            with col2:
                atividade = st.selectbox("Nível de Atividade", [
                    "Sedentário (pouco ou nenhum exercício)",
                    "Levemente ativo (exercício leve 1-3 dias/semana)",
                    "Moderadamente ativo (exercício moderado 3-5 dias/semana)",
                    "Muito ativo (exercício pesado 6-7 dias/semana)",
                    "Extremamente ativo (exercício muito pesado, trabalho físico)"
                ])
                
                objetivo = st.selectbox("Objetivo", [
                    "Manter peso",
                    "Perder 0.5 kg/semana",
                    "Perder 1 kg/semana", 
                    "Ganhar 0.5 kg/semana",
                    "Ganhar 1 kg/semana"
                ])
            
            if st.button("Calcular Necessidades Calóricas", type="primary"):
                # Cálculo TMB (Mifflin-St Jeor)
                if sexo_tmb == "Masculino":
                    tmb = (10 * peso_tmb) + (6.25 * altura_tmb) - (5 * idade) + 5
                else:
                    tmb = (10 * peso_tmb) + (6.25 * altura_tmb) - (5 * idade) - 161
                
                # Fator de atividade
                fatores = {
                    "Sedentário (pouco ou nenhum exercício)": 1.2,
                    "Levemente ativo (exercício leve 1-3 dias/semana)": 1.375,
                    "Moderadamente ativo (exercício moderado 3-5 dias/semana)": 1.55,
                    "Muito ativo (exercício pesado 6-7 dias/semana)": 1.725,
                    "Extremamente ativo (exercício muito pesado, trabalho físico)": 1.9
                }
                
                get = tmb * fatores[atividade]
                
                # Ajuste por objetivo
                ajustes = {
                    "Manter peso": 0,
                    "Perder 0.5 kg/semana": -250,
                    "Perder 1 kg/semana": -500,
                    "Ganhar 0.5 kg/semana": 250,
                    "Ganhar 1 kg/semana": 500
                }
                
                calorias_objetivo = get + ajustes[objetivo]
                
                # Distribuição de macronutrientes
                proteinas_g = peso_tmb * 1.6
                proteinas_cal = proteinas_g * 4
                gorduras_cal = calorias_objetivo * 0.25
                gorduras_g = gorduras_cal / 9
                carboidratos_cal = calorias_objetivo - proteinas_cal - gorduras_cal
                carboidratos_g = carboidratos_cal / 4
                
                st.markdown(f'<div class="calculator-result">Taxa Metabólica Basal: {tmb:.0f} kcal/dia</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="calculator-result">Gasto Energético Total: {get:.0f} kcal/dia</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="status-card status-normal">Calorias para o Objetivo: {calorias_objetivo:.0f} kcal/dia</div>', unsafe_allow_html=True)
                
                st.subheader("📊 Distribuição de Macronutrientes")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("🥩 Proteínas", f"{proteinas_g:.0f}g", f"{(proteinas_cal/calorias_objetivo*100):.0f}%")
                with col2:
                    st.metric("🍞 Carboidratos", f"{carboidratos_g:.0f}g", f"{(carboidratos_cal/calorias_objetivo*100):.0f}%")
                with col3:
                    st.metric("🥑 Gorduras", f"{gorduras_g:.0f}g", f"{(gorduras_cal/calorias_objetivo*100):.0f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📊 Análise de Composição Corporal")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Medidas Corporais**")
                peso_comp = st.number_input("Peso atual (kg)", min_value=30.0, max_value=300.0, value=70.0, key="peso_comp")
                altura_comp = st.number_input("Altura (cm)", min_value=100, max_value=250, value=170, key="altura_comp")
                cintura = st.number_input("Circunferência da cintura (cm)", min_value=50, max_value=200, value=80)
                quadril = st.number_input("Circunferência do quadril (cm)", min_value=60, max_value=200, value=95)
                pescoco = st.number_input("Circunferência do pescoço (cm)", min_value=20, max_value=60, value=35)
                
            with col2:
                st.write("**Informações Adicionais**")
                sexo_comp = st.selectbox("Sexo", ["Masculino", "Feminino"], key="sexo_comp")
                idade_comp = st.number_input("Idade (anos)", min_value=10, max_value=100, value=30, key="idade_comp")
                atividade_comp = st.selectbox("Nível de atividade física", [
                    "Sedentário", "Levemente ativo", "Moderadamente ativo", "Muito ativo"
                ])
            
            if st.button("Analisar Composição Corporal", type="primary"):
                # Cálculo do percentual de gordura (Fórmula do US Navy)
                if sexo_comp == "Masculino":
                    bf_percent = 495 / (1.0324 - 0.19077 * math.log10(cintura - pescoco) + 0.15456 * math.log10(altura_comp)) - 450
                else:
                    bf_percent = 495 / (1.29579 - 0.35004 * math.log10(cintura + quadril - pescoco) + 0.22100 * math.log10(altura_comp)) - 450
                
                # Relação cintura-quadril
                rcq = cintura / quadril
                
                # Classificações
                if sexo_comp == "Masculino":
                    if bf_percent < 6:
                        bf_status = "Muito baixo"
                        bf_color = "status-warning"
                    elif bf_percent < 14:
                        bf_status = "Atlético"
                        bf_color = "status-normal"
                    elif bf_percent < 18:
                        bf_status = "Fitness"
                        bf_color = "status-normal"
                    elif bf_percent < 25:
                        bf_status = "Média"
                        bf_color = "status-normal"
                    else:
                        bf_status = "Acima da média"
                        bf_color = "status-warning"
                    
                    rcq_ideal = rcq < 0.9
                else:
                    if bf_percent < 16:
                        bf_status = "Muito baixo"
                        bf_color = "status-warning"
                    elif bf_percent < 20:
                        bf_status = "Atlético"
                        bf_color = "status-normal"
                    elif bf_percent < 25:
                        bf_status = "Fitness"
                        bf_color = "status-normal"
                    elif bf_percent < 32:
                        bf_status = "Média"
                        bf_color = "status-normal"
                    else:
                        bf_status = "Acima da média"
                        bf_color = "status-warning"
                    
                    rcq_ideal = rcq < 0.8
                
                # Massa magra e gorda
                massa_gorda = peso_comp * (bf_percent / 100)
                massa_magra = peso_comp - massa_gorda
                
                st.markdown(f'<div class="calculator-result">Percentual de Gordura: {bf_percent:.1f}%</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="status-card {bf_color}">Classificação: {bf_status}</div>', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("💪 Massa Magra", f"{massa_magra:.1f} kg")
                with col2:
                    st.metric("📊 Massa Gorda", f"{massa_gorda:.1f} kg")
                with col3:
                    rcq_status = "Ideal" if rcq_ideal else "Atenção"
                    st.metric("📏 RCQ", f"{rcq:.2f}", rcq_status)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab4:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🎯 Calculadora de Objetivos e Metas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Situação Atual**")
                peso_atual = st.number_input("Peso atual (kg)", min_value=30.0, max_value=300.0, value=80.0)
                bf_atual = st.number_input("% Gordura atual", min_value=5.0, max_value=50.0, value=25.0)
                
                st.write("**Objetivo**")
                peso_meta = st.number_input("Peso meta (kg)", min_value=30.0, max_value=300.0, value=70.0)
                bf_meta = st.number_input("% Gordura meta", min_value=5.0, max_value=50.0, value=18.0)
                
            with col2:
                st.write("**Parâmetros**")
                velocidade = st.selectbox("Velocidade de perda/ganho", [
                    "Conservadora (0.25 kg/semana)",
                    "Moderada (0.5 kg/semana)",
                    "Acelerada (0.75 kg/semana)",
                    "Agressiva (1 kg/semana)"
                ])
                
                prioridade = st.selectbox("Prioridade", [
                    "Manter massa muscular",
                    "Perda de gordura máxima",
                    "Ganho de massa muscular",
                    "Recomposição corporal"
                ])
            
            if st.button("Calcular Plano de Metas", type="primary"):
                # Cálculos
                diferenca_peso = abs(peso_meta - peso_atual)
                
                velocidades = {
                    "Conservadora (0.25 kg/semana)": 0.25,
                    "Moderada (0.5 kg/semana)": 0.5,
                    "Acelerada (0.75 kg/semana)": 0.75,
                    "Agressiva (1 kg/semana)": 1.0
                }
                
                kg_por_semana = velocidades[velocidade]
                semanas_necessarias = diferenca_peso / kg_por_semana
                data_meta = datetime.now() + timedelta(weeks=semanas_necessarias)
                
                # Massa gorda e magra
                massa_gorda_atual = peso_atual * (bf_atual / 100)
                massa_magra_atual = peso_atual - massa_gorda_atual
                
                massa_gorda_meta = peso_meta * (bf_meta / 100)
                massa_magra_meta = peso_meta - massa_gorda_meta
                
                diferenca_gordura = massa_gorda_atual - massa_gorda_meta
                diferenca_magra = massa_magra_meta - massa_magra_atual
                
                st.markdown(f'<div class="calculator-result">Tempo estimado: {semanas_necessarias:.0f} semanas</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="status-card status-normal">Data prevista: {data_meta.strftime("%d/%m/%Y")}</div>', unsafe_allow_html=True)
                
                st.subheader("📊 Análise Detalhada")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("⚖️ Diferença de Peso", f"{diferenca_peso:.1f} kg")
                with col2:
                    st.metric("🔥 Gordura a Perder", f"{diferenca_gordura:.1f} kg" if diferenca_gordura > 0 else "Mantém")
                with col3:
                    st.metric("💪 Massa Magra", f"+{diferenca_magra:.1f} kg" if diferenca_magra > 0 else f"{diferenca_magra:.1f} kg")
                
                # Recomendações
                st.subheader("💡 Recomendações Personalizadas")
                
                if prioridade == "Manter massa muscular":
                    st.info("🏋️ Foque em treino de força, déficit calórico moderado e alta ingestão proteica (2g/kg)")
                elif prioridade == "Perda de gordura máxima":
                    st.info("🔥 Combine déficit calórico com exercícios aeróbicos e treino de força")
                elif prioridade == "Ganho de massa muscular":
                    st.info("💪 Superávit calórico leve com treino de hipertrofia e proteína adequada")
                else:
                    st.info("⚖️ Recomposição corporal: treino intenso + nutrição precisa + paciência")
            st.markdown('</div>', unsafe_allow_html=True)

    def pacientes_page(self):
        """Página de gestão de pacientes"""
        st.markdown('<div class="main-header"><h1>👥 Gestão Completa de Pacientes</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📋 Lista de Pacientes", "➕ Novo Paciente", "📊 Analytics"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            
            # Filtros
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                filtro_nome = st.text_input("🔍 Buscar por nome")
            with col2:
                filtro_objetivo = st.selectbox("🎯 Objetivo", ["Todos", "Emagrecimento", "Ganho de massa", "Manutenção", "Definição"])
            with col3:
                filtro_status = st.selectbox("📊 Status", ["Todos", "Ativo", "Inativo"])
            with col4:
                ordenar = st.selectbox("📑 Ordenar por", ["Nome", "Data cadastro", "IMC"])
            
            # Lista de pacientes
            pacientes_filtrados = st.session_state.pacientes.copy()
            
            if filtro_nome:
                pacientes_filtrados = [p for p in pacientes_filtrados if filtro_nome.lower() in p['nome'].lower()]
            
            if filtro_objetivo != "Todos":
                pacientes_filtrados = [p for p in pacientes_filtrados if p['objetivo'] == filtro_objetivo]
            
            if pacientes_filtrados:
                st.write(f"📊 **{len(pacientes_filtrados)}** pacientes encontrados")
                
                for i, paciente in enumerate(pacientes_filtrados):
                    with st.expander(f"👤 {paciente['nome']} - {paciente['objetivo']} - IMC: {paciente['imc']:.1f}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write("**📋 Informações Pessoais**")
                            st.write(f"**Idade:** {paciente['idade']} anos")
                            st.write(f"**Email:** {paciente['email']}")
                            st.write(f"**Telefone:** {paciente['telefone']}")
                            st.write(f"**Cadastro:** {paciente['data_cadastro']}")
                        
                        with col2:
                            st.write("**📏 Medidas Atuais**")
                            st.write(f"**Peso:** {paciente['peso']} kg")
                            st.write(f"**Altura:** {paciente['altura']} m")
                            st.write(f"**IMC:** {paciente['imc']:.1f}")
                            
                            # Status do IMC
                            if paciente['imc'] < 18.5:
                                st.markdown('<div class="status-card status-warning">Abaixo do peso</div>', unsafe_allow_html=True)
                            elif 18.5 <= paciente['imc'] < 25:
                                st.markdown('<div class="status-card status-normal">Peso normal</div>', unsafe_allow_html=True)
                            elif 25 <= paciente['imc'] < 30:
                                st.markdown('<div class="status-card status-warning">Sobrepeso</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div class="status-card status-danger">Obesidade</div>', unsafe_allow_html=True)
                        
                        with col3:
                            st.write("**🎯 Objetivos**")
                            st.write(f"**Objetivo:** {paciente['objetivo']}")
                            if paciente.get('observacoes'):
                                st.write(f"**Observações:** {paciente['observacoes']}")
                            
                            # Ações
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("📊 Evolução", key=f"evolucao_{i}"):
                                    st.info("Módulo de evolução em desenvolvimento")
                            with col_b:
                                if st.button("🍽️ Dieta", key=f"dieta_{i}"):
                                    st.info("Redirecionar para criação de plano")
            else:
                st.info("📝 Nenhum paciente encontrado")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("➕ Cadastro de Novo Paciente")
            
            with st.form("novo_paciente"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nome = st.text_input("👤 Nome Completo *")
                    idade = st.number_input("🎂 Idade", min_value=1, max_value=120, value=30)
                    email = st.text_input("📧 Email *")
                    telefone = st.text_input("📱 Telefone *")
                
                with col2:
                    peso = st.number_input("⚖️ Peso (kg)", min_value=1.0, max_value=500.0, value=70.0, step=0.1)
                    altura = st.number_input("📏 Altura (m)", min_value=0.5, max_value=3.0, value=1.70, step=0.01)
                    objetivo = st.selectbox("🎯 Objetivo", ["Emagrecimento", "Ganho de massa", "Manutenção", "Definição"])
                
                observacoes = st.text_area("📝 Observações")
                
                submitted = st.form_submit_button("✅ Cadastrar Paciente", use_container_width=True, type="primary")
                
                if submitted:
                    if nome and email and telefone:
                        imc = peso / (altura ** 2)
                        novo_paciente = {
                            "id": len(st.session_state.pacientes) + 1,
                            "nome": nome,
                            "idade": idade,
                            "email": email,
                            "telefone": telefone,
                            "peso": peso,
                            "altura": altura,
                            "imc": imc,
                            "objetivo": objetivo,
                            "observacoes": observacoes,
                            "data_cadastro": datetime.now().strftime("%d/%m/%Y"),
                            "status": "Ativo"
                        }
                        st.session_state.pacientes.append(novo_paciente)
                        st.success(f"✅ Paciente {nome} cadastrado com sucesso!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Preencha todos os campos obrigatórios!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            if st.session_state.pacientes:
                st.subheader("📊 Analytics da Base de Pacientes")
                
                # Estatísticas
                total = len(st.session_state.pacientes)
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("👥 Total", total)
                with col2:
                    imc_medio = sum([p['imc'] for p in st.session_state.pacientes]) / total
                    st.metric("📊 IMC Médio", f"{imc_medio:.1f}")
                with col3:
                    idade_media = sum([p['idade'] for p in st.session_state.pacientes]) / total
                    st.metric("🎂 Idade Média", f"{idade_media:.0f} anos")
                with col4:
                    peso_medio = sum([p['peso'] for p in st.session_state.pacientes]) / total
                    st.metric("⚖️ Peso Médio", f"{peso_medio:.1f} kg")
                
                # Gráficos
                col1, col2 = st.columns(2)
                
                with col1:
                    objetivos = [p['objetivo'] for p in st.session_state.pacientes]
                    objetivo_counts = pd.Series(objetivos).value_counts()
                    
                    fig = px.pie(values=objetivo_counts.values, names=objetivo_counts.index,
                               title="Distribuição por Objetivo")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    imcs = [p['imc'] for p in st.session_state.pacientes]
                    
                    fig = px.histogram(x=imcs, nbins=20, title="Distribuição de IMC")
                    fig.add_vline(x=18.5, line_dash="dash", line_color="yellow")
                    fig.add_vline(x=25, line_dash="dash", line_color="green")
                    fig.add_vline(x=30, line_dash="dash", line_color="orange")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 Cadastre pacientes para ver analytics")
            st.markdown('</div>', unsafe_allow_html=True)

    def planos_alimentares_page(self):
        """Página de planos alimentares"""
        st.markdown('<div class="main-header"><h1>🍽️ Criador de Planos Alimentares</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🎯 Criar Plano", "📋 Planos Salvos"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            
            if st.session_state.pacientes:
                col1, col2 = st.columns(2)
                
                with col1:
                    paciente_selecionado = st.selectbox(
                        "👤 Selecionar Paciente",
                        ["Plano genérico"] + [p['nome'] for p in st.session_state.pacientes]
                    )
                    
                    calorias_alvo = st.number_input("🔥 Calorias alvo (kcal/dia)", 
                                                  min_value=800, max_value=4000, value=1800)
                
                with col2:
                    tipo_dieta = st.selectbox("🥗 Tipo de Dieta", [
                        "Balanceada (50% Carb, 20% Prot, 30% Gord)",
                        "Low Carb (30% Carb, 30% Prot, 40% Gord)",
                        "High Protein (40% Carb, 35% Prot, 25% Gord)",
                        "Cetogênica (5% Carb, 25% Prot, 70% Gord)"
                    ])
                    
                    num_refeicoes = st.selectbox("🍽️ Número de Refeições", [3, 4, 5, 6])
                
                # Calcular macros
                distribuicoes = {
                    "Balanceada (50% Carb, 20% Prot, 30% Gord)": (50, 20, 30),
                    "Low Carb (30% Carb, 30% Prot, 40% Gord)": (30, 30, 40),
                    "High Protein (40% Carb, 35% Prot, 25% Gord)": (40, 35, 25),
                    "Cetogênica (5% Carb, 25% Prot, 70% Gord)": (5, 25, 70)
                }
                carb_percent, prot_percent, gord_percent = distribuicoes[tipo_dieta]
                
                carb_g = (calorias_alvo * carb_percent / 100) / 4
                prot_g = (calorias_alvo * prot_percent / 100) / 4
                gord_g = (calorias_alvo * gord_percent / 100) / 9
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🍞 Carboidratos", f"{carb_g:.0f}g")
                with col2:
                    st.metric("🥩 Proteínas", f"{prot_g:.0f}g")
                with col3:
                    st.metric("🥑 Gorduras", f"{gord_g:.0f}g")
                
                if st.button("🚀 Gerar Plano Alimentar", type="primary"):
                    with st.spinner("Criando plano personalizado..."):
                        time.sleep(2)
                        
                        # Criar plano básico
                        plano = {
                            "id": len(st.session_state.planos_alimentares) + 1,
                            "paciente": paciente_selecionado,
                            "calorias_alvo": calorias_alvo,
                            "tipo_dieta": tipo_dieta,
                            "num_refeicoes": num_refeicoes,
                            "macros": {"carb": carb_g, "prot": prot_g, "gord": gord_g},
                            "data_criacao": datetime.now().strftime("%d/%m/%Y"),
                            "refeicoes": {}
                        }
                        
                        # Distribuir refeições
                        if num_refeicoes == 3:
                            nomes_refeicoes = ["Café da Manhã", "Almoço", "Jantar"]
                            distribuicao = [0.25, 0.45, 0.30]
                        elif num_refeicoes == 4:
                            nomes_refeicoes = ["Café da Manhã", "Almoço", "Lanche", "Jantar"]
                            distribuicao = [0.25, 0.35, 0.10, 0.30]
                        elif num_refeicoes == 5:
                            nomes_refeicoes = ["Café da Manhã", "Lanche Manhã", "Almoço", "Lanche Tarde", "Jantar"]
                            distribuicao = [0.20, 0.10, 0.35, 0.10, 0.25]
                        else:
                            nomes_refeicoes = ["Café da Manhã", "Lanche Manhã", "Almoço", "Lanche Tarde", "Jantar", "Ceia"]
                            distribuicao = [0.15, 0.10, 0.30, 0.10, 0.25, 0.10]
                        
                        for nome, percent in zip(nomes_refeicoes, distribuicao):
                            calorias_refeicao = int(calorias_alvo * percent)
                            plano["refeicoes"][nome] = {
                                "calorias": calorias_refeicao,
                                "alimentos": ["Personalizar conforme preferências"],
                                "observacoes": "Plano base - ajustar conforme necessidade"
                            }
                        
                        st.session_state.planos_alimentares.append(plano)
                        st.success("🎉 Plano alimentar criado com sucesso!")
                        
                        # Exibir plano
                        for nome_refeicao, dados in plano["refeicoes"].items():
                            st.subheader(f"🍽️ {nome_refeicao} - {dados['calorias']} kcal")
                            st.write(f"Alimentos: {', '.join(dados['alimentos'])}")
            else:
                st.info("👥 Cadastre pacientes primeiro para criar planos personalizados")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            if st.session_state.planos_alimentares:
                st.subheader("📋 Planos Alimentares Salvos")
                
                for plano in st.session_state.planos_alimentares:
                    with st.expander(f"🍽️ Plano de {plano['paciente']} - {plano['calorias_alvo']} kcal"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Paciente:** {plano['paciente']}")
                            st.write(f"**Calorias:** {plano['calorias_alvo']} kcal")
                            st.write(f"**Tipo:** {plano['tipo_dieta']}")
                        
                        with col2:
                            st.write(f"**Refeições:** {plano['num_refeicoes']}")
                            st.write(f"**Criado em:** {plano['data_criacao']}")
                        
                        for nome_refeicao, dados in plano["refeicoes"].items():
                            st.write(f"• **{nome_refeicao}:** {dados['calorias']} kcal")
            else:
                st.info("📝 Nenhum plano alimentar criado ainda")
            st.markdown('</div>', unsafe_allow_html=True)

    def receitas_page(self):
        """Página de receitas"""
        st.markdown('<div class="main-header"><h1>🍳 Banco de Receitas Nutricionais</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📚 Receitas Disponíveis", "➕ Nova Receita"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            
            # Filtros
            col1, col2, col3 = st.columns(3)
            with col1:
                busca = st.text_input("🔍 Buscar receita")
            with col2:
                categoria_filtro = st.selectbox("📂 Categoria", ["Todas", "Saladas", "Bebidas", "Pratos Principais"])
            with col3:
                max_calorias = st.slider("🔥 Máximo de calorias", 0, 1000, 500)
            
            # Lista de receitas
            receitas_filtradas = st.session_state.receitas.copy()
            
            if busca:
                receitas_filtradas = [r for r in receitas_filtradas if busca.lower() in r['nome'].lower()]
            
            if categoria_filtro != "Todas":
                receitas_filtradas = [r for r in receitas_filtradas if r['categoria'] == categoria_filtro]
            
            receitas_filtradas = [r for r in receitas_filtradas if r['calorias'] <= max_calorias]
            
            st.write(f"📊 **{len(receitas_filtradas)}** receitas encontradas")
            
            for receita in receitas_filtradas:
                with st.expander(f"🍳 {receita['nome']} - {receita['calorias']} kcal"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write("**Ingredientes:**")
                        for ingrediente in receita['ingredientes']:
                            st.write(f"• {ingrediente}")
                        
                        st.write(f"**Preparo:** {receita['preparo']}")
                        
                        if 'tempo_preparo' in receita:
                            st.write(f"**Tempo:** {receita['tempo_preparo']}")
                        if 'dificuldade' in receita:
                            st.write(f"**Dificuldade:** {receita['dificuldade']}")
                    
                    with col2:
                        st.metric("🔥 Calorias", f"{receita['calorias']} kcal")
                        if 'proteinas' in receita:
                            st.metric("🥩 Proteínas", f"{receita['proteinas']}g")
                        if 'carboidratos' in receita:
                            st.metric("🍞 Carboidratos", f"{receita['carboidratos']}g")
                        if 'gorduras' in receita:
                            st.metric("🥑 Gorduras", f"{receita['gorduras']}g")
                        
                        st.write(f"**📂 {receita['categoria']}**")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("➕ Adicionar Nova Receita")
            
            with st.form("nova_receita"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nome_receita = st.text_input("🍳 Nome da Receita *")
                    categoria_receita = st.selectbox("📂 Categoria", ["Saladas", "Bebidas", "Pratos Principais", "Sobremesas", "Lanches"])
                    tempo_preparo = st.text_input("⏰ Tempo de Preparo", placeholder="ex: 20 minutos")
                    dificuldade = st.selectbox("📊 Dificuldade", ["Fácil", "Médio", "Difícil"])
                
                with col2:
                    calorias_receita = st.number_input("🔥 Calorias (kcal)", min_value=0, value=200)
                    proteinas_receita = st.number_input("🥩 Proteínas (g)", min_value=0.0, value=10.0, step=0.1)
                    carboidratos_receita = st.number_input("🍞 Carboidratos (g)", min_value=0.0, value=20.0, step=0.1)
                    gorduras_receita = st.number_input("🥑 Gorduras (g)", min_value=0.0, value=5.0, step=0.1)
                
                ingredientes_receita = st.text_area("📝 Ingredientes (um por linha)", placeholder="Ingrediente 1\nIngrediente 2\n...")
                preparo_receita = st.text_area("👨‍🍳 Modo de Preparo", placeholder="Descreva o passo a passo...")
                
                submitted = st.form_submit_button("✅ Adicionar Receita", use_container_width=True, type="primary")
                
                if submitted:
                    if nome_receita and ingredientes_receita and preparo_receita:
                        nova_receita = {
                            "id": len(st.session_state.receitas) + 1,
                            "nome": nome_receita,
                            "categoria": categoria_receita,
                            "ingredientes": [ing.strip() for ing in ingredientes_receita.split('\n') if ing.strip()],
                            "preparo": preparo_receita,
                            "calorias": calorias_receita,
                            "proteinas": proteinas_receita,
                            "carboidratos": carboidratos_receita,
                            "gorduras": gorduras_receita,
                            "tempo_preparo": tempo_preparo,
                            "dificuldade": dificuldade
                        }
                        
                        st.session_state.receitas.append(nova_receita)
                        st.success(f"✅ Receita '{nome_receita}' adicionada com sucesso!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Preencha todos os campos obrigatórios!")
            st.markdown('</div>', unsafe_allow_html=True)

    def agendamentos_page(self):
        """Página de agendamentos"""
        st.markdown('<div class="main-header"><h1>📅 Sistema de Agendamentos</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📅 Agenda", "➕ Novo Agendamento", "📊 Relatório"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            
            # Filtros de data
            col1, col2, col3 = st.columns(3)
            with col1:
                data_filtro = st.date_input("📅 Filtrar por data", value=datetime.now().date())
            with col2:
                status_filtro = st.selectbox("📊 Status", ["Todos", "Agendado", "Realizado", "Cancelado"])
            with col3:
                if st.button("🔄 Atualizar Agenda"):
                    st.rerun()
            
            # Lista de agendamentos
            data_str = data_filtro.strftime('%Y-%m-%d')
            agendamentos_dia = [a for a in st.session_state.agendamentos if a.get('data') == data_str]
            
            if status_filtro != "Todos":
                agendamentos_dia = [a for a in agendamentos_dia if a.get('status') == status_filtro]
            
            st.subheader(f"📅 Agendamentos para {data_filtro.strftime('%d/%m/%Y')}")
            
            if agendamentos_dia:
                agendamentos_dia.sort(key=lambda x: x['horario'])
                
                for i, agendamento in enumerate(agendamentos_dia):
                    status_color = {
                        "Agendado": "status-normal",
                        "Realizado": "status-normal", 
                        "Cancelado": "status-danger"
                    }.get(agendamento.get('status', 'Agendado'), 'status-normal')
                    
                    with st.expander(f"🕐 {agendamento['horario']} - {agendamento['paciente']} - {agendamento['tipo']}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**👤 Paciente:** {agendamento['paciente']}")
                            st.write(f"**📋 Tipo:** {agendamento['tipo']}")
                            st.write(f"**🕐 Horário:** {agendamento['horario']}")
                        
                        with col2:
                            st.markdown(f'<div class="status-card {status_color}">Status: {agendamento.get("status", "Agendado")}</div>', unsafe_allow_html=True)
                            if agendamento.get('observacoes'):
                                st.write(f"**📝 Observações:** {agendamento['observacoes']}")
                        
                        with col3:
                            novo_status = st.selectbox("Alterar Status", 
                                                     ["Agendado", "Realizado", "Cancelado"], 
                                                     index=["Agendado", "Realizado", "Cancelado"].index(agendamento.get('status', 'Agendado')),
                                                     key=f"status_{i}")
                            
                            if st.button("💾 Salvar", key=f"salvar_{i}"):
                                agendamento['status'] = novo_status
                                st.success("Status atualizado!")
                                st.rerun()
            else:
                st.info("📝 Nenhum agendamento para esta data")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("➕ Novo Agendamento")
            
            with st.form("novo_agendamento"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.session_state.pacientes:
                        paciente_agendamento = st.selectbox("👤 Paciente", [p['nome'] for p in st.session_state.pacientes])
                    else:
                        paciente_agendamento = st.text_input("👤 Nome do Paciente")
                    
                    data_agendamento = st.date_input("📅 Data", min_value=datetime.now().date())
                    horario_agendamento = st.time_input("🕐 Horário", value=datetime.now().time())
                
                with col2:
                    tipo_consulta = st.selectbox("📋 Tipo de Consulta", [
                        "Consulta Inicial", "Retorno", "Avaliação", "Online", "Urgência"
                    ])
                    
                    duracao = st.selectbox("⏱️ Duração", ["30 min", "60 min", "90 min"])
                    valor = st.number_input("💰 Valor (R$)", min_value=0.0, value=st.session_state.configuracoes.get('valor_consulta', 150.0))
                
                observacoes_agendamento = st.text_area("📝 Observações")
                
                submitted = st.form_submit_button("✅ Agendar Consulta", use_container_width=True, type="primary")
                
                if submitted:
                    novo_agendamento = {
                        "id": len(st.session_state.agendamentos) + 1,
                        "paciente": paciente_agendamento,
                        "data": data_agendamento.strftime('%Y-%m-%d'),
                        "horario": horario_agendamento.strftime('%H:%M'),
                        "tipo": tipo_consulta,
                        "duracao": duracao,
                        "valor": valor,
                        "observacoes": observacoes_agendamento,
                        "status": "Agendado",
                        "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M")
                    }
                    
                    st.session_state.agendamentos.append(novo_agendamento)
                    st.success(f"✅ Consulta agendada para {paciente_agendamento}!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            if st.session_state.agendamentos:
                st.subheader("📊 Relatório de Agendamentos")
                
                # Estatísticas
                total_agendamentos = len(st.session_state.agendamentos)
                realizados = len([a for a in st.session_state.agendamentos if a.get('status') == 'Realizado'])
                cancelados = len([a for a in st.session_state.agendamentos if a.get('status') == 'Cancelado'])
                receita_total = sum([a.get('valor', 0) for a in st.session_state.agendamentos if a.get('status') == 'Realizado'])
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📅 Total", total_agendamentos)
                with col2:
                    st.metric("✅ Realizados", realizados)
                with col3:
                    st.metric("❌ Cancelados", cancelados)
                with col4:
                    st.metric("💰 Receita", f"R$ {receita_total:.2f}")
                
                # Gráfico de status
                status_counts = pd.Series([a.get('status', 'Agendado') for a in st.session_state.agendamentos]).value_counts()
                
                fig = px.pie(values=status_counts.values, names=status_counts.index,
                           title="Distribuição por Status")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📊 Nenhum agendamento para análise")
            st.markdown('</div>', unsafe_allow_html=True)

    def relatorios_page(self):
        """Página de relatórios"""
        st.markdown('<div class="main-header"><h1>📈 Relatórios Profissionais</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📊 Gerar Relatórios", "📋 Relatórios Salvos"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Relatório de Pacientes")
                
                if st.button("📈 Gerar Relatório de Pacientes", use_container_width=True):
                    if st.session_state.pacientes:
                        # Dados para relatório
                        df_pacientes = pd.DataFrame(st.session_state.pacientes)
                        
                        st.write("**📊 Resumo Estatístico:**")
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            st.metric("Total de Pacientes", len(df_pacientes))
                        with col_b:
                            st.metric("IMC Médio", f"{df_pacientes['imc'].mean():.1f}")
                        with col_c:
                            st.metric("Idade Média", f"{df_pacientes['idade'].mean():.0f} anos")
                        
                        # Gráfico de objetivos
                        fig = px.pie(df_pacientes, names='objetivo', title="Distribuição por Objetivo")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Tabela resumo
                        st.write("**📋 Lista de Pacientes:**")
                        st.dataframe(df_pacientes[['nome', 'idade', 'imc', 'objetivo', 'data_cadastro']], use_container_width=True)
                    else:
                        st.info("Nenhum paciente cadastrado")
            
            with col2:
                st.subheader("📅 Relatório de Agendamentos")
                
                if st.button("📊 Gerar Relatório de Agendamentos", use_container_width=True):
                    if st.session_state.agendamentos:
                        df_agendamentos = pd.DataFrame(st.session_state.agendamentos)
                        
                        st.write("**📊 Resumo Estatístico:**")
                        col_a, col_b, col_c = st.columns(3)
                        
                        with col_a:
                            st.metric("Total", len(df_agendamentos))
                        with col_b:
                            realizados = len(df_agendamentos[df_agendamentos['status'] == 'Realizado'])
                            st.metric("Realizados", realizados)
                        with col_c:
                            receita = df_agendamentos[df_agendamentos['status'] == 'Realizado']['valor'].sum()
                            st.metric("Receita", f"R$ {receita:.2f}")
                        
                        # Gráfico de status
                        fig = px.pie(df_agendamentos, names='status', title="Status dos Agendamentos")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Tabela resumo
                        st.write("**📋 Lista de Agendamentos:**")
                        st.dataframe(df_agendamentos[['paciente', 'data', 'horario', 'tipo', 'status', 'valor']], use_container_width=True)
                    else:
                        st.info("Nenhum agendamento cadastrado")
            
            st.markdown("---")
            st.subheader("📈 Relatório Financeiro")
            
            if st.button("💰 Gerar Relatório Financeiro", use_container_width=True):
                if st.session_state.agendamentos:
                    agendamentos_realizados = [a for a in st.session_state.agendamentos if a.get('status') == 'Realizado']
                    
                    if agendamentos_realizados:
                        receita_total = sum([a.get('valor', 0) for a in agendamentos_realizados])
                        media_consulta = receita_total / len(agendamentos_realizados)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("💰 Receita Total", f"R$ {receita_total:.2f}")
                        with col2:
                            st.metric("📊 Consultas Realizadas", len(agendamentos_realizados))
                        with col3:
                            st.metric("💡 Ticket Médio", f"R$ {media_consulta:.2f}")
                        
                        # Gráfico de receita por tipo
                        df_fin = pd.DataFrame(agendamentos_realizados)
                        receita_por_tipo = df_fin.groupby('tipo')['valor'].sum().reset_index()
                        
                        fig = px.bar(receita_por_tipo, x='tipo', y='valor', 
                                   title="Receita por Tipo de Consulta")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("Nenhuma consulta realizada ainda")
                else:
                    st.info("Nenhum agendamento para análise financeira")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.info("📋 Funcionalidade de relatórios salvos em desenvolvimento")
            st.markdown('</div>', unsafe_allow_html=True)

    def comunicacao_page(self):
        """Página de comunicação"""
        st.markdown('<div class="main-header"><h1>💬 Central de Comunicação</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📱 WhatsApp", "📧 Email"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📱 Envio de Mensagens WhatsApp")
            
            if st.session_state.pacientes:
                paciente_msg = st.selectbox("👤 Selecionar Paciente", [p['nome'] for p in st.session_state.pacientes])
                
                tipo_mensagem = st.selectbox("📋 Tipo de Mensagem", [
                    "Lembrete de Consulta",
                    "Plano Alimentar",
                    "Motivacional",
                    "Personalizada"
                ])
                
                if tipo_mensagem == "Lembrete de Consulta":
                    mensagem = "Olá! Lembrando que você tem consulta marcada. Confirme sua presença."
                elif tipo_mensagem == "Plano Alimentar":
                    mensagem = "Seu novo plano alimentar está pronto! Siga as orientações e qualquer dúvida me procure."
                elif tipo_mensagem == "Motivacional":
                    mensagem = "Parabéns pelo seu progresso! Continue firme no seu objetivo. Você consegue!"
                else:
                    mensagem = ""
                
                mensagem_final = st.text_area("💬 Mensagem", value=mensagem, height=100)
                
                if st.button("📤 Enviar Mensagem", type="primary"):
                    st.success(f"✅ Mensagem enviada para {paciente_msg}!")
                    st.info("💡 Em produção, integraria com API do WhatsApp Business")
            else:
                st.info("👥 Cadastre pacientes primeiro para enviar mensagens")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📧 Envio de Emails")
            
            if st.session_state.pacientes:
                paciente_email = st.selectbox("👤 Selecionar Paciente", [p['nome'] for p in st.session_state.pacientes], key="email_paciente")
                
                assunto = st.text_input("📋 Assunto", value="Acompanhamento Nutricional")
                
                corpo_email = st.text_area("📧 Corpo do Email", 
                                         value="Olá!\n\nEspero que esteja bem.\n\nAtenciosamente,\nSua Nutricionista", 
                                         height=150)
                
                anexar_plano = st.checkbox("📎 Anexar Plano Alimentar")
                
                if st.button("📤 Enviar Email", type="primary"):
                    st.success(f"✅ Email enviado para {paciente_email}!")
                    st.info("💡 Em produção, integraria com serviço de email")
            else:
                st.info("👥 Cadastre pacientes primeiro para enviar emails")
            st.markdown('</div>', unsafe_allow_html=True)

    def configuracoes_page(self):
        """Página de configurações"""
        st.markdown('<div class="main-header"><h1>⚙️ Configurações do Sistema</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🏢 Empresa", "💰 Financeiro", "🔧 Sistema"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🏢 Informações da Empresa")
            
            with st.form("config_empresa"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nome_empresa = st.text_input("🏢 Nome da Empresa", 
                                               value=st.session_state.configuracoes.get('empresa_nome', ''))
                    email_empresa = st.text_input("📧 Email", 
                                                value=st.session_state.configuracoes.get('email', ''))
                    whatsapp_empresa = st.text_input("📱 WhatsApp", 
                                                   value=st.session_state.configuracoes.get('whatsapp', ''))
                
                with col2:
                    endereco_empresa = st.text_area("📍 Endereço", 
                                                  value=st.session_state.configuracoes.get('endereco', ''))
                    
                    cores_tema = st.selectbox("🎨 Tema de Cores", 
                                            ["Azul", "Verde", "Rosa", "Roxo"],
                                            index=["azul", "verde", "rosa", "roxo"].index(st.session_state.configuracoes.get('cores_tema', 'azul')))
                
                logo_upload = st.file_uploader("📷 Upload do Logo", type=['png', 'jpg', 'jpeg'])
                
                if st.form_submit_button("💾 Salvar Configurações", use_container_width=True, type="primary"):
                    st.session_state.configuracoes.update({
                        'empresa_nome': nome_empresa,
                        'email': email_empresa,
                        'whatsapp': whatsapp_empresa,
                        'endereco': endereco_empresa,
                        'cores_tema': cores_tema.lower()
                    })
                    
                    if logo_upload:
                        st.session_state.configuracoes['empresa_logo'] = logo_upload
                    
                    st.success("✅ Configurações salvas com sucesso!")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("💰 Configurações Financeiras")
            
            with st.form("config_financeiro"):
                col1, col2 = st.columns(2)
                
                with col1:
                    valor_consulta = st.number_input("💰 Valor da Consulta (R$)", 
                                                   min_value=0.0, 
                                                   value=st.session_state.configuracoes.get('valor_consulta', 150.0))
                    
                    tempo_consulta = st.selectbox("⏱️ Tempo de Consulta", 
                                                [30, 45, 60, 90], 
                                                index=[30, 45, 60, 90].index(st.session_state.configuracoes.get('tempo_consulta', 60)))
                
                with col2:
                    horario_inicio = st.time_input("🌅 Horário de Início", 
                                                 value=datetime.strptime(st.session_state.configuracoes.get('horario_inicio', '08:00'), '%H:%M').time())
                    
                    horario_fim = st.time_input("🌅 Horário de Fim", 
                                              value=datetime.strptime(st.session_state.configuracoes.get('horario_fim', '18:00'), '%H:%M').time())
                
                dias_trabalho = st.multiselect("📅 Dias de Trabalho", 
                                             ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
                                             default=st.session_state.configuracoes.get('dias_trabalho', ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]))
                
                if st.form_submit_button("💾 Salvar Configurações", use_container_width=True, type="primary"):
                    st.session_state.configuracoes.update({
                        'valor_consulta': valor_consulta,
                        'tempo_consulta': tempo_consulta,
                        'horario_inicio': horario_inicio.strftime('%H:%M'),
                        'horario_fim': horario_fim.strftime('%H:%M'),
                        'dias_trabalho': dias_trabalho
                    })
                    
                    st.success("✅ Configurações financeiras salvas!")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🔧 Configurações do Sistema")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📊 Estatísticas do Sistema**")
                st.metric("👥 Total de Pacientes", len(st.session_state.pacientes))
                st.metric("📅 Total de Agendamentos", len(st.session_state.agendamentos))
                st.metric("🍳 Total de Receitas", len(st.session_state.receitas))
                st.metric("🍽️ Planos Criados", len(st.session_state.planos_alimentares))
                
                st.write("**🔄 Backup e Exportação**")
                if st.button("💾 Backup Completo", use_container_width=True):
                    backup_data = {
                        "pacientes": st.session_state.pacientes,
                        "agendamentos": st.session_state.agendamentos,
                        "receitas": st.session_state.receitas,
                        "planos_alimentares": st.session_state.planos_alimentares,
                        "configuracoes": st.session_state.configuracoes,
                        "data_backup": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    }
                    
                    backup_json = json.dumps(backup_data, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="📥 Baixar Backup",
                        data=backup_json,
                        file_name=f"nutristock360_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                    st.success("✅ Backup gerado com sucesso!")
            
            with col2:
                st.write("**🎨 Personalização**")
                
                # Seletor de tema
                tema_atual = st.session_state.configuracoes.get('cores_tema', 'azul')
                novo_tema = st.selectbox("🎨 Tema de Cores", 
                                       ["Azul", "Verde", "Rosa", "Roxo", "Laranja"],
                                       index=["azul", "verde", "rosa", "roxo", "laranja"].index(tema_atual) if tema_atual in ["azul", "verde", "rosa", "roxo", "laranja"] else 0)
                
                if st.button("🎨 Aplicar Tema", use_container_width=True):
                    st.session_state.configuracoes['cores_tema'] = novo_tema.lower()
                    st.success(f"✅ Tema {novo_tema} aplicado!")
                    st.rerun()
                
                st.write("**🗑️ Limpeza de Dados**")
                if st.button("🗑️ Limpar Dados de Teste", use_container_width=True, type="secondary"):
                    if st.button("⚠️ Confirmar Limpeza", use_container_width=True):
                        st.session_state.pacientes = []
                        st.session_state.agendamentos = []
                        st.session_state.planos_alimentares = []
                        st.success("✅ Dados de teste limpos!")
                        st.rerun()
                
                st.write("**ℹ️ Informações do Sistema**")
                st.info("""
                **NutriStock360 Pro v2.0**
                - Sistema completo para nutricionistas
                - Calculadoras profissionais
                - Gestão integrada de pacientes
                - Relatórios avançados
                - Comunicação automatizada
                """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    def run(self):
        """Executa o aplicativo principal"""
        if not st.session_state.authenticated:
            self.login_page()
        else:
            selected_page = self.sidebar_menu()
            
            if selected_page == "📊 Dashboard Principal":
                self.dashboard_page()
            elif selected_page == "🧮 Calculadoras Nutricionais":
                self.calculadoras_page()
            elif selected_page == "👥 Gestão de Pacientes":
                self.pacientes_page()
            elif selected_page == "🍽️ Planos Alimentares":
                self.planos_alimentares_page()
            elif selected_page == "🍳 Banco de Receitas":
                self.receitas_page()
            elif selected_page == "📅 Agendamentos":
                self.agendamentos_page()
            elif selected_page == "📈 Relatórios":
                self.relatorios_page()
            elif selected_page == "💬 Comunicação":
                self.comunicacao_page()
            elif selected_page == "⚙️ Configurações":
                self.configuracoes_page()

# Executar aplicação
if __name__ == "__main__":
    app = NutriStock360Pro()
    app.run()
