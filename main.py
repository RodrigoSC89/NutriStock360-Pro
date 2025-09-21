import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import base64
import hashlib
import time
import io
import uuid
from typing import Dict, List, Optional

# Importações opcionais com tratamento de erro
try:
    import jwt
    JWT_AVAILABLE = True
except ImportError:
    JWT_AVAILABLE = False
    st.warning("⚠️ Biblioteca JWT não disponível. Usando autenticação básica.")

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
        background: linear-gradient(90deg, #4CAF50, #45a049);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #4CAF50;
    }
    .sidebar-logo {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(45deg, #4CAF50, #45a049);
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Classe principal do sistema
class NutriStock360:
    def __init__(self):
        self.init_session_state()
        
    def init_session_state(self):
        """Inicializa o estado da sessão"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'current_user' not in st.session_state:
            st.session_state.current_user = None
        if 'pacientes' not in st.session_state:
            st.session_state.pacientes = []
        if 'consultas' not in st.session_state:
            st.session_state.consultas = []
        if 'receitas' not in st.session_state:
            st.session_state.receitas = self.load_default_receitas()
            
    def load_default_receitas(self):
        """Carrega receitas padrão"""
        return [
            {
                "id": 1,
                "nome": "Salada Verde Detox",
                "ingredientes": ["Alface", "Rúcula", "Pepino", "Tomate cereja", "Azeite"],
                "calorias": 120,
                "preparo": "Misture todos os ingredientes e tempere com azeite",
                "categoria": "Saladas"
            },
            {
                "id": 2,
                "nome": "Smoothie Proteico",
                "ingredientes": ["Banana", "Whey protein", "Leite de amêndoas", "Aveia"],
                "calorias": 280,
                "preparo": "Bata tudo no liquidificador até ficar homogêneo",
                "categoria": "Bebidas"
            }
        ]
    
    def hash_password(self, password: str) -> str:
        """Hash da senha"""
        if BCRYPT_AVAILABLE:
            return bcrypt.hash(password)
        else:
            # Fallback simples
            return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verifica senha"""
        if BCRYPT_AVAILABLE:
            return bcrypt.verify(password, hashed)
        else:
            return hashlib.sha256(password.encode()).hexdigest() == hashed
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Autentica usuário"""
        # Usuários padrão (em produção, usar banco de dados)
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
        st.markdown('<div class="main-header"><h1>🥗 NutriStock360 Pro</h1><p>Sistema Profissional para Nutricionistas</p></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔐 Login do Sistema")
            
            with st.form("login_form"):
                username = st.text_input("👤 Usuário")
                password = st.text_input("🔒 Senha", type="password")
                submitted = st.form_submit_button("🚀 Entrar", use_container_width=True)
                
                if submitted:
                    if self.authenticate_user(username, password):
                        st.success("✅ Login realizado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Usuário ou senha incorretos!")
            
            st.markdown("---")
            st.info("""
            **👥 Usuários de Teste:**
            - Admin: `admin` / `admin123`
            - Nutricionista: `nutricionista` / `nutri123`
            - Demo: `demo` / `demo123`
            """)
    
    def sidebar_menu(self):
        """Menu lateral"""
        with st.sidebar:
            st.markdown('<div class="sidebar-logo"><h2>🥗 NutriStock360</h2><p>Pro Dashboard</p></div>', unsafe_allow_html=True)
            
            st.markdown(f"**👤 Usuário:** {st.session_state.current_user}")
            
            menu_options = [
                "📊 Dashboard",
                "👥 Pacientes", 
                "🍽️ Planos Alimentares",
                "📅 Agendamentos",
                "🍳 Receitas",
                "📈 Relatórios",
                "⚙️ Configurações"
            ]
            
            selected = st.selectbox("🧭 Navegação", menu_options)
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.current_user = None
                st.rerun()
            
            return selected
    
    def dashboard_page(self):
        """Página principal do dashboard"""
        st.markdown('<div class="main-header"><h1>📊 Dashboard - NutriStock360 Pro</h1></div>', unsafe_allow_html=True)
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Pacientes Ativos", len(st.session_state.pacientes), "2")
        with col2:
            st.metric("📅 Consultas Hoje", len([c for c in st.session_state.consultas if c.get('data') == datetime.now().strftime('%Y-%m-%d')]), "5")
        with col3:
            st.metric("🍳 Receitas Cadastradas", len(st.session_state.receitas), "1")
        with col4:
            st.metric("💰 Receita Mensal", "R$ 12.500", "8%")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Evolução de Pacientes")
            # Dados fictícios para demonstração
            dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='M')
            patients = np.cumsum(np.random.randint(5, 15, len(dates)))
            
            fig = px.line(x=dates, y=patients, title="Crescimento de Pacientes")
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Metas do Mês")
            # Gráfico de progresso
            categories = ['Novos Pacientes', 'Consultas', 'Receitas', 'Receita']
            values = [75, 85, 60, 90]
            
            fig = go.Figure(data=[
                go.Bar(x=categories, y=values, marker_color=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0'])
            ])
            fig.update_layout(height=300, title="Progresso das Metas (%)")
            st.plotly_chart(fig, use_container_width=True)
        
        # Atividades recentes
        st.subheader("🕐 Atividades Recentes")
        recent_activities = [
            {"time": "10:30", "activity": "Consulta com Maria Silva", "type": "consulta"},
            {"time": "09:15", "activity": "Novo paciente cadastrado: João Santos", "type": "paciente"},
            {"time": "08:45", "activity": "Plano alimentar criado para Ana Costa", "type": "plano"},
            {"time": "08:30", "activity": "Receita 'Smoothie Verde' adicionada", "type": "receita"}
        ]
        
        for activity in recent_activities:
            icon = {"consulta": "👥", "paciente": "🆕", "plano": "🍽️", "receita": "🍳"}[activity["type"]]
            st.markdown(f"**{activity['time']}** {icon} {activity['activity']}")
    
    def pacientes_page(self):
        """Página de gestão de pacientes"""
        st.markdown('<div class="main-header"><h1>👥 Gestão de Pacientes</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📋 Lista de Pacientes", "➕ Novo Paciente"])
        
        with tab1:
            if st.session_state.pacientes:
                for paciente in st.session_state.pacientes:
                    with st.expander(f"👤 {paciente['nome']} - {paciente['idade']} anos"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Email:** {paciente['email']}")
                            st.write(f"**Telefone:** {paciente['telefone']}")
                            st.write(f"**Peso:** {paciente['peso']} kg")
                        with col2:
                            st.write(f"**Altura:** {paciente['altura']} m")
                            st.write(f"**IMC:** {paciente['imc']:.1f}")
                            st.write(f"**Objetivo:** {paciente['objetivo']}")
            else:
                st.info("📝 Nenhum paciente cadastrado ainda.")
        
        with tab2:
            with st.form("novo_paciente"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nome = st.text_input("👤 Nome Completo")
                    idade = st.number_input("🎂 Idade", min_value=1, max_value=120, value=30)
                    email = st.text_input("📧 Email")
                    telefone = st.text_input("📱 Telefone")
                
                with col2:
                    peso = st.number_input("⚖️ Peso (kg)", min_value=1.0, max_value=500.0, value=70.0, step=0.1)
                    altura = st.number_input("📏 Altura (m)", min_value=0.5, max_value=3.0, value=1.70, step=0.01)
                    objetivo = st.selectbox("🎯 Objetivo", ["Emagrecimento", "Ganho de massa", "Manutenção", "Definição"])
                
                observacoes = st.text_area("📝 Observações")
                
                if st.form_submit_button("✅ Cadastrar Paciente", use_container_width=True):
                    if nome and email:
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
                            "data_cadastro": datetime.now().strftime("%d/%m/%Y")
                        }
                        st.session_state.pacientes.append(novo_paciente)
                        st.success(f"✅ Paciente {nome} cadastrado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Nome e email são obrigatórios!")
    
    def receitas_page(self):
        """Página de receitas"""
        st.markdown('<div class="main-header"><h1>🍳 Banco de Receitas</h1></div>', unsafe_allow_html=True)
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            busca = st.text_input("🔍 Buscar receita", placeholder="Digite o nome da receita...")
        with col2:
            categoria = st.selectbox("📂 Categoria", ["Todas", "Saladas", "Bebidas", "Pratos principais", "Sobremesas"])
        with col3:
            max_calorias = st.slider("🔥 Máximo de calorias", 0, 1000, 500)
        
        # Lista de receitas
        receitas_filtradas = st.session_state.receitas
        
        if busca:
            receitas_filtradas = [r for r in receitas_filtradas if busca.lower() in r['nome'].lower()]
        
        if categoria != "Todas":
            receitas_filtradas = [r for r in receitas_filtradas if r['categoria'] == categoria]
        
        receitas_filtradas = [r for r in receitas_filtradas if r['calorias'] <= max_calorias]
        
        st.write(f"📊 **{len(receitas_filtradas)}** receitas encontradas")
        
        for receita in receitas_filtradas:
            with st.expander(f"🍳 {receita['nome']} - {receita['calorias']} kcal"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("**Ingredientes:**")
                    for ingrediente in receita['ingredientes']:
                        st.write(f"• {ingrediente}")
                    
                    st.write("**Modo de preparo:**")
                    st.write(receita['preparo'])
                
                with col2:
                    st.metric("🔥 Calorias", f"{receita['calorias']} kcal")
                    st.write(f"**📂 Categoria:** {receita['categoria']}")
                    
                    if st.button(f"📋 Usar na dieta", key=f"usar_{receita['id']}"):
                        st.success("✅ Receita adicionada ao plano!")
    
    def run(self):
        """Executa o aplicativo principal"""
        if not st.session_state.authenticated:
            self.login_page()
        else:
            selected_page = self.sidebar_menu()
            
            if selected_page == "📊 Dashboard":
                self.dashboard_page()
            elif selected_page == "👥 Pacientes":
                self.pacientes_page()
            elif selected_page == "🍳 Receitas":
                self.receitas_page()
            elif selected_page == "🍽️ Planos Alimentares":
                st.markdown('<div class="main-header"><h1>🍽️ Planos Alimentares</h1></div>', unsafe_allow_html=True)
                st.info("🚧 Módulo em desenvolvimento")
            elif selected_page == "📅 Agendamentos":
                st.markdown('<div class="main-header"><h1>📅 Agendamentos</h1></div>', unsafe_allow_html=True)
                st.info("🚧 Módulo em desenvolvimento")
            elif selected_page == "📈 Relatórios":
                st.markdown('<div class="main-header"><h1>📈 Relatórios</h1></div>', unsafe_allow_html=True)
                st.info("🚧 Módulo em desenvolvimento")
            elif selected_page == "⚙️ Configurações":
                st.markdown('<div class="main-header"><h1>⚙️ Configurações</h1></div>', unsafe_allow_html=True)
                st.info("🚧 Módulo em desenvolvimento")

# Executar aplicação
if __name__ == "__main__":
    app = NutriStock360()
    app.run()
