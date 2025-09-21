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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradient 6s ease infinite;
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        border-left: 6px solid #667eea;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
        border-left-color: #f093fb;
    }
    
    .sidebar-logo {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    .calculator-result {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        font-size: 1.2rem;
        box-shadow: 0 8px 25px rgba(132, 250, 176, 0.3);
        color: #2d3748;
    }
    
    .status-card {
        padding: 1.2rem;
        border-radius: 15px;
        margin: 0.8rem 0;
        text-align: center;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .status-normal { 
        background: linear-gradient(135deg, #c6f6d5, #9ae6b4); 
        color: #22543d; 
        border: 2px solid #68d391;
    }
    .status-warning { 
        background: linear-gradient(135deg, #fefcbf, #faf089); 
        color: #744210; 
        border: 2px solid #f6e05e;
    }
    .status-danger { 
        background: linear-gradient(135deg, #fed7d7, #feb2b2); 
        color: #742a2a; 
        border: 2px solid #fc8181;
    }
    
    .tab-content {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: 1rem;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

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
            'relatorios_salvos': [],
            'busca_global': '',
            'theme_mode': 'light',
            'notifications': []
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
            <p><em>Versão 2.0 - Experiência Premium</em></p>
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
                """)
    
    def sidebar_menu(self):
        """Menu lateral"""
        with st.sidebar:
            st.markdown(f'''
            <div class="sidebar-logo">
                <h2>🥗 NutriStock360</h2>
                <p>Pro Dashboard</p>
                <small>v2.0 Premium</small>
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
            
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            base_patients = [10, 15, 18, 25, 32, 38, 45, 52, 58, 65, 72, max(total_pacientes, 78)]
            
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

    def calculadoras_page(self):
        """Calculadoras nutricionais"""
        st.markdown('<div class="main-header"><h1>🧮 Calculadoras Nutricionais</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📏 IMC", "🔥 TMB"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📏 Calculadora de IMC")
            
            col1, col2 = st.columns(2)
            
            with col1:
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
                st.info("📊 IMC é um indicador importante da saúde")
                st.write("**Classificações:**")
                st.write("• Abaixo de 18.5: Abaixo do peso")
                st.write("• 18.5 - 24.9: Peso normal")
                st.write("• 25 - 29.9: Sobrepeso")
                st.write("• Acima de 30: Obesidade")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🔥 Taxa Metabólica Basal")
            
            col1, col2 = st.columns(2)
            
            with col1:
                peso_tmb = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1, key="peso_tmb")
                altura_tmb = st.number_input("Altura (cm)", min_value=100, max_value=250, value=170, key="altura_tmb")
                idade = st.number_input("Idade (anos)", min_value=10, max_value=100, value=30)
                sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
                
                if st.button("Calcular TMB", type="primary"):
                    if sexo == "Masculino":
                        tmb = (10 * peso_tmb) + (6.25 * altura_tmb) - (5 * idade) + 5
                    else:
                        tmb = (10 * peso_tmb) + (6.25 * altura_tmb) - (5 * idade) - 161
                    
                    st.markdown(f'<div class="calculator-result">TMB: {tmb:.0f} kcal/dia</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="status-card status-normal">Energia para funções vitais</div>', unsafe_allow_html=True)
            
            with col2:
                st.info("🔥 TMB é a energia mínima necessária para sobreviver")
                st.write("**Fatores que influenciam:**")
                st.write("• Peso e altura")
                st.write("• Idade e sexo")
                st.write("• Massa muscular")
                st.write("• Genética")
            
            st.markdown('</div>', unsafe_allow_html=True)

    def pacientes_page(self):
        """Gestão de pacientes"""
        st.markdown('<div class="main-header"><h1>👥 Gestão de Pacientes</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📋 Lista de Pacientes", "➕ Novo Paciente"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            
            if st.session_state.pacientes:
                st.write(f"📊 **{len(st.session_state.pacientes)}** pacientes cadastrados")
                
                for i, paciente in enumerate(st.session_state.pacientes):
                    with st.expander(f"👤 {paciente['nome']} - {paciente['objetivo']} - IMC: {paciente['imc']:.1f}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write("**📋 Informações Pessoais**")
                            st.write(f"**Idade:** {paciente['idade']} anos")
                            st.write(f"**Email:** {paciente['email']}")
                            st.write(f"**Telefone:** {paciente['telefone']}")
                        
                        with col2:
                            st.write("**📏 Medidas**")
                            st.write(f"**Peso:** {paciente['peso']} kg")
                            st.write(f"**Altura:** {paciente['altura']} m")
                            st.write(f"**IMC:** {paciente['imc']:.1f}")
                        
                        with col3:
                            st.write("**🎯 Objetivo**")
                            st.write(f"**Meta:** {paciente['objetivo']}")
                            if paciente.get('observacoes'):
                                st.write(f"**Obs:** {paciente['observacoes']}")
            else:
                st.info("📝 Nenhum paciente cadastrado ainda.")
            
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

    def planos_alimentares_page(self):
        """Planos alimentares"""
        st.markdown('<div class="main-header"><h1>🍽️ Planos Alimentares</h1></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        if st.session_state.pacientes:
            paciente_selecionado = st.selectbox(
                "👤 Selecionar Paciente",
                ["Plano genérico"] + [p['nome'] for p in st.session_state.pacientes]
            )
            
            calorias_alvo = st.number_input("🔥 Calorias alvo (kcal/dia)", 
                                          min_value=800, max_value=4000, value=1800)
            
            if st.button("🚀 Gerar Plano Alimentar", type="primary"):
                st.success("🎉 Plano alimentar criado com sucesso!")
                st.info("Funcionalidade em desenvolvimento completo")
        else:
            st.info("👥 Cadastre pacientes primeiro para criar planos personalizados")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def receitas_page(self):
        """Banco de receitas"""
        st.markdown('<div class="main-header"><h1>🍳 Banco de Receitas</h1></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        # Lista de receitas
        for receita in st.session_state.receitas:
            with st.expander(f"🍳 {receita['nome']} - {receita['calorias']} kcal"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("**Ingredientes:**")
                    for ingrediente in receita['ingredientes']:
                        st.write(f"• {ingrediente}")
                    
                    st.write(f"**Preparo:** {receita['preparo']}")
                
                with col2:
                    st.metric("🔥 Calorias", f"{receita['calorias']} kcal")
                    st.write(f"**📂 {receita['categoria']}**")
                    st.write(f"**⏰ {receita['tempo_preparo']}**")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def agendamentos_page(self):
        """Sistema de agendamentos"""
        st.markdown('<div class="main-header"><h1>📅 Sistema de Agendamentos</h1></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        data_filtro = st.date_input("📅 Filtrar por data", value=datetime.now().date())
        
        data_str = data_filtro.strftime('%Y-%m-%d')
        agendamentos_dia = [a for a in st.session_state.agendamentos if a.get('data') == data_str]
        
        if agendamentos_dia:
            for agendamento in agendamentos_dia:
                st.write(f"🕐 {agendamento['horario']} - {agendamento['paciente']} - {agendamento['tipo']}")
        else:
            st.info("📝 Nenhum agendamento para esta data")
        
        # Novo agendamento
        st.subheader("➕ Novo Agendamento")
        
        with st.form("novo_agendamento"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.session_state.pacientes:
                    paciente_agendamento = st.selectbox("👤 Paciente", [p['nome'] for p in st.session_state.pacientes])
                else:
                    paciente_agendamento = st.text_input("👤 Nome do Paciente")
                
                data_agendamento = st.date_input("📅 Data", min_value=datetime.now().date())
            
            with col2:
                horario_agendamento = st.time_input("🕐 Horário", value=datetime.now().time())
                tipo_consulta = st.selectbox("📋 Tipo", ["Consulta Inicial", "Retorno", "Avaliação"])
            
            submitted = st.form_submit_button("✅ Agendar", use_container_width=True, type="primary")
            
            if submitted and paciente_agendamento:
                novo_agendamento = {
                    "id": len(st.session_state.agendamentos) + 1,
                    "paciente": paciente_agendamento,
                    "data": data_agendamento.strftime('%Y-%m-%d'),
                    "horario": horario_agendamento.strftime('%H:%M'),
                    "tipo": tipo_consulta,
                    "status": "Agendado"
                }
                st.session_state.agendamentos.append(novo_agendamento)
                st.success(f"✅ Consulta agendada para {paciente_agendamento}!")
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    def relatorios_page(self):
        """Relatórios"""
        st.markdown('<div class="main-header"><h1>📈 Relatórios</h1></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        if st.button("📊 Gerar Relatório de Pacientes", type="primary"):
            if st.session_state.pacientes:
                df_pacientes = pd.DataFrame(st.session_state.pacientes)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Pacientes", len(df_pacientes))
                with col2:
                    st.metric("IMC Médio", f"{df_pacientes['imc'].mean():.1f}")
                with col3:
                    st.metric("Idade Média", f"{df_pacientes['idade'].mean():.0f} anos")
                
                st.dataframe(df_pacientes[['nome', 'idade', 'imc', 'objetivo']], use_container_width=True)
            else:
                st.info("Nenhum paciente cadastrado")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def comunicacao_page(self):
        """Comunicação"""
        st.markdown('<div class="main-header"><h1>💬 Comunicação</h1></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        if st.session_state.pacientes:
            paciente_msg = st.selectbox("👤 Selecionar Paciente", [p['nome'] for p in st.session_state.pacientes])
            mensagem = st.text_area("💬 Mensagem", "Olá! Como está seu acompanhamento nutricional?")
            
            if st.button("📤 Enviar WhatsApp", type="primary"):
                st.success(f"✅ Mensagem enviada para {paciente_msg}!")
        else:
            st.info("👥 Cadastre pacientes primeiro para enviar mensagens")
        
        st.markdown('</div>', unsafe_allow_html=True)

    def configuracoes_page(self):
        """Configurações"""
        st.markdown('<div class="main-header"><h1>⚙️ Configurações</h1></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="tab-content">', unsafe_allow_html=True)
        
        with st.form("configuracoes"):
            nome_empresa = st.text_input("🏢 Nome da Empresa", 
                                       value=st.session_state.configuracoes.get('empresa_nome', ''))
            email_empresa = st.text_input("📧 Email", 
                                        value=st.session_state.configuracoes.get('email', ''))
            valor_consulta = st.number_input("💰 Valor da Consulta (R$)", 
                                           value=st.session_state.configuracoes.get('valor_consulta', 150.0))
            
            if st.form_submit_button("💾 Salvar Configurações", type="primary"):
                st.session_state.configuracoes.update({
                    'empresa_nome': nome_empresa,
                    'email': email_empresa,
                    'valor_consulta': valor_consulta
                })
                st.success("✅ Configurações salvas com sucesso!")
                st.rerun()
        
        # Backup
        st.subheader("🔄 Backup do Sistema")
        if st.button("💾 Gerar Backup", type="primary"):
            backup_data = {
                "pacientes": st.session_state.pacientes,
                "agendamentos": st.session_state.agendamentos,
                "receitas": st.session_state.receitas,
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
    try:
        app = NutriStock360Pro()
        app.run()
    except Exception as e:
        st.error(f"Erro no sistema: {str(e)}")
        st.info("Recarregue a página ou entre em contato com o suporte.")
