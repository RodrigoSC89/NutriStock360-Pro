# Estatísticas dos filtros
            if pacientes_filtrados:
                total_filtrados = len(pacientes_filtrados)
                imc_medio_filtrado = sum([p['imc'] for p in pacientes_filtrados]) / total_filtrados
                
                st.markdown(f"""
                <div style="background: #667eea15; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #667eea;">
                    <div style="color: #667eea; font-weight: 600;">
                        Resultados: {total_filtrados} pacientes encontrados | IMC médio: {imc_medio_filtrado:.1f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Lista de pacientes com design melhorado
                for i, paciente in enumerate(pacientes_filtrados):
                    imc_status = self.classificar_imc(paciente['imc'])
                    status_colors = {
                        "Abaixo do peso": "#ed8936",
                        "Normal": "#48bb78",
                        "Sobrepeso": "#ed8936", 
                        "Obesidade": "#e53e3e"
                    }
                    cor_status = status_colors.get(imc_status, "#718096")
                    
                    with st.expander(f"👤 {paciente['nome']} - {paciente['objetivo']} - IMC: {paciente['imc']:.1f}", expanded=False):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("**Informações Pessoais**")
                            st.write(f"**Idade:** {paciente['idade']} anos")
                            st.write(f"**Email:** {paciente['email']}")
                            st.write(f"**Telefone:** {paciente['telefone']}")
                            st.write(f"**Cadastro:** {paciente['data_cadastro']}")
                        
                        with col2:
                            st.markdown("**Medidas Atuais**")
                            st.write(f"**Peso:** {paciente['peso']} kg")
                            st.write(f"**Altura:** {paciente['altura']} m")
                            st.write(f"**IMC:** {paciente['imc']:.1f}")
                            
                            st.markdown(f'''
                            <div style="background: {cor_status}15; padding: 0.8rem; border-radius: 8px; border-left: 4px solid {cor_status};">
                                <div style="color: {cor_status}; font-weight: 600;">Status: {imc_status}</div>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown("**Objetivo e Ações**")
                            st.write(f"**Objetivo:** {paciente['objetivo']}")
                            if paciente.get('observacoes'):
                                st.write(f"**Observações:** {paciente['observacoes']}")
                            
                            # Botões de ação
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("📊 Evolução", key=f"evolucao_{i}"):
                                    st.info("Módulo de evolução em desenvolvimento")
                            with col_b:
                                if st.button("🍽️ Criar Plano", key=f"plano_{i}"):
                                    st.info("Redirecionando para criação de plano alimentar")
            else:
                st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #718096;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">Nenhum paciente encontrado</div>
                    <div>Tente ajustar os filtros ou cadastre novos pacientes</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("Cadastro Rápido de Paciente")
            
            with st.form("novo_paciente_rapido"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nome = st.text_input("Nome Completo *", placeholder="Digite o nome completo")
                    idade = st.number_input("Idade", min_value=1, max_value=120, value=30)
                    email = st.text_input("Email *", placeholder="exemplo@email.com")
                    telefone = st.text_input("Telefone/WhatsApp *", placeholder="(11) 99999-9999")
                
                with col2:
                    peso = st.number_input("Peso (kg)", min_value=1.0, max_value=500.0, value=70.0, step=0.1)
                    altura = st.number_input("Altura (m)", min_value=0.5, max_value=3.0, value=1.70, step=0.01)
                    objetivo = st.selectbox("Objetivo Principal", ["Emagrecimento", "Ganho de massa", "Manutenção", "Definição", "Reabilitação"])
                    atividade_fisica = st.selectbox("Nível de Atividade", [
                        "Sedentário",
                        "Levemente ativo (1-3x/semana)",
                        "Moderadamente ativo (3-5x/semana)", 
                        "Muito ativo (6-7x/semana)"
                    ])
                
                observacoes = st.text_area("Observações", placeholder="Informações adicionais sobre o paciente...")
                
                # Pré-visualização do IMC
                if peso and altura:
                    imc_preview = peso / (altura ** 2)
                    status_preview = self.classificar_imc(imc_preview)
                    
                    status_colors = {
                        "Abaixo do peso": "#ed8936",
                        "Normal": "#48bb78",
                        "Sobrepeso": "#ed8936",
                        "Obesidade": "#e53e3e"
                    }
                    cor_preview = status_colors.get(status_preview, "#718096")
                    
                    st.markdown(f'''
                    <div style="background: {cor_preview}15; padding: 1rem; border-radius: 10px; border-left: 4px solid {cor_preview};">
                        <div style="color: {cor_preview}; font-weight: 600;">
                            Pré-visualização: IMC {imc_preview:.1f} - {status_preview}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                submitted = st.form_submit_button("Cadastrar Paciente", use_container_width=True, type="primary")
                
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
                            "atividade_fisica": atividade_fisica,
                            "observacoes": observacoes,
                            "data_cadastro": datetime.now().strftime("%d/%m/%Y"),
                            "status": "Ativo"
                        }
                        
                        st.session_state.pacientes.append(novo_paciente)
                        st.success(f"Paciente {nome} cadastrado com sucesso!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Preencha todos os campos obrigatórios!")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            if st.session_state.pacientes:
                st.subheader("Analytics da Base de Pacientes")
                
                # Métricas principais
                total = len(st.session_state.pacientes)
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-container">
                            <div class="metric-value" style="color: #667eea;">{total}</div>
                            <div class="metric-label">Total de Pacientes</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    imc_medio = sum([p['imc'] for p in st.session_state.pacientes]) / total
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-container">
                            <div class="metric-value" style="color: #48bb78;">{imc_medio:.1f}</div>
                            <div class="metric-label">IMC Médio</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col3:
                    idade_media = sum([p['idade'] for p in st.session_state.pacientes]) / total
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-container">
                            <div class="metric-value" style="color: #ed8936;">{idade_media:.0f}</div>
                            <div class="metric-label">Idade Média (anos)</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col4:
                    peso_medio = sum([p['peso'] for p in st.session_state.pacientes]) / total
                    st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-container">
                            <div class="metric-value" style="color: #9f7aea;">{peso_medio:.1f} kg</div>
                            <div class="metric-label">Peso Médio</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Gráficos de análise
                col1, col2 = st.columns(2)
                
                with col1:
                    # Distribuição por objetivo
                    objetivos = [p['objetivo'] for p in st.session_state.pacientes]
                    objetivo_counts = pd.Series(objetivos).value_counts()
                    
                    fig = create_interactive_chart(
                        pd.DataFrame({'Objetivo': objetivo_counts.index, 'Quantidade': objetivo_counts.values}),
                        "pie", "Distribuição por Objetivo", 'Objetivo', 'Quantidade'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Distribuição de IMC
                    imcs = [p['imc'] for p in st.session_state.pacientes]
                    
                    fig = px.histogram(
                        x=imcs, 
                        nbins=20, 
                        title="Distribuição de IMC",
                        color_discrete_sequence=['#667eea']
                    )
                    fig.add_vline(x=18.5, line_dash="dash", line_color="#ed8936", annotation_text="Baixo peso")
                    fig.add_vline(x=25, line_dash="dash", line_color="#48bb78", annotation_text="Normal")
                    fig.add_vline(x=30, line_dash="dash", line_color="#e53e3e", annotation_text="Obesidade")
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Análise de faixas de IMC
                st.subheader("Análise Detalhada por Faixas de IMC")
                
                imc_stats = {}
                for paciente in st.session_state.pacientes:
                    categoria = self.classificar_imc(paciente['imc'])
                    imc_stats[categoria] = imc_stats.get(categoria, 0) + 1
                
                col1, col2, col3, col4 = st.columns(4)
                categorias_imc = [
                    ("Abaixo do peso", "#ed8936", col1),
                    ("Normal", "#48bb78", col2), 
                    ("Sobrepeso", "#ed8936", col3),
                    ("Obesidade", "#e53e3e", col4)
                ]
                
                for categoria, cor, col in categorias_imc:
                    quantidade = imc_stats.get(categoria, 0)
                    percentual = (quantidade / total * 100) if total > 0 else 0
                    
                    with col:
                        st.markdown(f'''
                        <div style="background: {cor}15; padding: 1.5rem; border-radius: 15px; text-align: center; border: 2px solid {cor};">
                            <div style="color: {cor}; font-size: 1.5rem; font-weight: 700;">{quantidade}</div>
                            <div style="color: {cor}; font-weight: 600; margin: 0.5rem 0;">{categoria}</div>
                            <div style="color: #718096; font-size: 0.9rem;">{percentual:.1f}% do total</div>
                        </div>
                        ''', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #718096;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">Cadastre pacientes para ver analytics</div>
                    <div>As análises aparecerão aqui conforme você adiciona pacientes</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def classificar_imc(self, imc):
        """Classifica o IMC em categorias"""
        if imc < 18.5:
            return "Abaixo do peso"
        elif imc < 25:
            return "Normal"
        elif imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidade"
    
    def planos_alimentares_page(self):
        """Página de planos alimentares otimizada"""
        st.markdown('<div class="main-header"><h1>🍽️ Criador Inteligente de Planos Alimentares</h1><p>Nutrição personalizada com base científica</p></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🎯 Criar Plano", "📋 Planos Salvos"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            
            if st.session_state.pacientes:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**👤 Seleção do Paciente**")
                    paciente_selecionado = st.selectbox(
                        "Escolha o paciente",
                        ["Plano genérico"] + [p['nome'] for p in st.session_state.pacientes]
                    )
                    
                    if paciente_selecionado != "Plano genérico":
                        paciente = next(p for p in st.session_state.pacientes if p['nome'] == paciente_selecionado)
                        
                        st.markdown(f"""
                        <div style="background: #48bb7815; padding: 1rem; border-radius: 10px; border-left: 4px solid #48bb78;">
                            <div style="color: #48bb78; font-weight: 600;">Paciente Selecionado</div>
                            <div style="color: #2d3748;">
                                <strong>{paciente['nome']}</strong><br>
                                Objetivo: {paciente['objetivo']}<br>
                                IMC: {paciente['imc']:.1f} | Peso: {paciente['peso']} kg
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    calorias_alvo = st.number_input("🔥 Calorias alvo (kcal/dia)", 
                                                  min_value=800, max_value=4000, value=1800)
                
                with col2:
                    st.markdown("**🥗 Configurações Nutricionais**")
                    tipo_dieta = st.selectbox("Tipo de Dieta", [
                        "Balanceada (50% Carb, 20% Prot, 30% Gord)",
                        "Low Carb (30% Carb, 30% Prot, 40% Gord)",
                        "High Protein (40% Carb, 35% Prot, 25% Gord)",
                        "Cetogênica (5% Carb, 25% Prot, 70% Gord)"
                    ])
                    
                    num_refeicoes = st.selectbox("Número de Refeições", [3, 4, 5, 6])
                    
                    restricoes = st.multiselect("Restrições Alimentares", [
                        "Sem lactose", "Sem glúten", "Vegetariano", "Vegano",
                        "Diabetes", "Hipertensão", "Baixo sódio"
                    ])
                
                # Cálculo automático de macros
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
                
                # Exibir macros
                st.markdown("**📊 Distribuição de Macronutrientes**")
                col1, col2, col3 = st.columns(3)
                
                macros_info = [
                    ("🍞 Carboidratos", carb_g, carb_percent, "#3182ce", col1),
                    ("🥩 Proteínas", prot_g, prot_percent, "#e53e3e", col2),
                    ("🥑 Gorduras", gord_g, gord_percent, "#ed8936", col3)
                ]
                
                for nome, gramas, percent, cor, col in macros_info:
                    with col:
                        st.markdown(f'''
                        <div style="background: {cor}15; padding: 1rem; border-radius: 10px; text-align: center; border: 2px solid {cor};">
                            <div style="color: {cor}; font-weight: 600;">{nome}</div>
                            <div style="color: {cor}; font-size: 1.3rem; font-weight: 700;">{gramas:.0f}g</div>
                            <div style="color: #718096; font-size: 0.9rem;">{percent}% das calorias</div>
                        </div>
                        ''', unsafe_allow_html=True)
                
                if st.button("🚀 Gerar Plano Alimentar Inteligente", type="primary", use_container_width=True):
                    with st.spinner("Criando plano personalizado..."):
                        time.sleep(2)
                        
                        # Criar plano
                        plano = {
                            "id": len(st.session_state.planos_alimentares) + 1,
                            "paciente": paciente_selecionado,
                            "calorias_alvo": calorias_alvo,
                            "tipo_dieta": tipo_dieta,
                            "num_refeicoes": num_refeicoes,
                            "restricoes": restricoes,
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
                                "sugestoes": self.gerar_sugestoes_refeicao(nome, calorias_refeicao, restricoes),
                                "observacoes": "Ajustar porções conforme necessidade individual"
                            }
                        
                        st.session_state.planos_alimentares.append(plano)
                        st.success("Plano alimentar criado com sucesso!")
                        
                        # Exibir plano criado
                        st.markdown("**📋 Plano Alimentar Gerado**")
                        
                        for nome_refeicao, dados in plano["refeicoes"].items():
                            with st.expander(f"🍽️ {nome_refeicao} - {dados['calorias']} kcal", expanded=True):
                                st.write("**Sugestões:**")
                                for sugestao in dados['sugestoes']:
                                    st.write(f"• {sugestao}")
                                st.write(f"**Observações:** {dados['observacoes']}")
                        
                        # Resumo nutricional
                        total_calorias_plano = sum([r['calorias'] for r in plano["refeicoes"].values()])
                        st.markdown(f'''
                        <div class="calculator-result">
                            Total do Plano: {total_calorias_plano} kcal (Meta: {calorias_alvo} kcal)
                        </div>
                        ''', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #718096;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">👥</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">Cadastre pacientes primeiro</div>
                    <div>Para criar planos personalizados, você precisa ter pacientes cadastrados</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            if st.session_state.planos_alimentares:
                st.subheader("Planos Alimentares Salvos")
                
                for plano in st.session_state.planos_alimentares:
                    with st.expander(f"🍽️ Plano de {plano['paciente']} - {plano['calorias_alvo']} kcal - {plano['data_criacao']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Paciente:** {plano['paciente']}")
                            st.write(f"**Calorias:** {plano['calorias_alvo']} kcal")
                            st.write(f"**Tipo:** {plano['tipo_dieta']}")
                            if plano.get('restricoes'):
                                st.write(f"**Restrições:** {', '.join(plano['restricoes'])}")
                        
                        with col2:
                            st.write(f"**Refeições:** {plano['num_refeicoes']}")
                            st.write(f"**Criado:** {plano['data_criacao']}")
                            
                            if st.button("📧 Enviar por Email", key=f"email_{plano['id']}"):
                                st.success("Email enviado com sucesso!")
                            
                            if st.button("📱 Enviar WhatsApp", key=f"whats_{plano['id']}"):
                                st.success("Mensagem enviada via WhatsApp!")
                        
                        st.markdown("**Resumo das Refeições:**")
                        for nome_refeicao, dados in plano["refeicoes"].items():
                            st.write(f"• **{nome_refeicao}:** {dados['calorias']} kcal")
            else:
                st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #718096;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📋</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">Nenhum plano criado ainda</div>
                    <div>Crie seu primeiro plano alimentar na aba anterior</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def gerar_sugestoes_refeicao(self, tipo_refeicao, calorias, restricoes):
        """Gera sugestões inteligentes para cada refeição"""
        sugestoes_base = {
            "Café da Manhã": [
                "2 fatias de pão integral + 1 ovo mexido + 1 copo de leite",
                "1 taça de frutas + 2 colheres de aveia + iogurte natural",
                "Vitamina de banana com leite + 1 torrada integral"
            ],
            "Lanche Manhã": [
                "1 fruta da estação + castanhas",
                "Iogurte natural + granola",
                "Água de coco + biscoito integral"
            ],
            "Almoço": [
                "Peito de frango grelhado + arroz integral + brócolis + salada",
                "Peixe assado + batata doce + legumes refogados",
                "Carne magra + quinoa + vegetais variados"
            ],
            "Lanche Tarde": [
                "Smoothie de frutas com leite",
                "Sanduíche natural integral",
                "Frutas + queijo branco"
            ],
            "Jantar": [
                "Sopa de legumes + proteína magra",
                "Salada completa + omelete",
                "Peixe grelhado + vegetais no vapor"
            ],
            "Ceia": [
                "Chá + biscoito integral",
                "Iogurte natural",
                "Leite morno com mel"
            ]
        }
        
        # Ajustar sugestões baseado nas restrições
        sugestoes = sugestoes_base.get(tipo_refeicao, ["Refeição personalizada"])
        
        if "Sem lactose" in restricoes:
            sugestoes = [s.replace("leite", "leite de amêndoas").replace("iogurte", "iogurte vegetal") for s in sugestoes]
        
        if "Vegetariano" in restricoes:
            sugestoes = [s.replace("frango", "tofu").replace("peixe", "leguminosas").replace("carne", "proteína vegetal") for s in sugestoes]
        
        if "Sem glúten" in restricoes:
            sugestoes = [s.replace("pão integral", "tapioca").replace("aveia", "quinoa") for s in sugestoes]
        
        return sugestoes[:2]  # Retornar apenas 2 sugestões
    
    def receitas_page(self):
        """Página de receitas aprimorada"""
        st.markdown('<div class="main-header"><h1>🍳 Banco de Receitas Nutricionais</h1><p>Coleção profissional com análise nutricional completa</p></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📚 Explorar Receitas", "➕ Nova Receita"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            
            # Filtros aprimorados
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                busca = st.text_input("🔍 Buscar receita", placeholder="Nome ou ingrediente...")
            with col2:
                categoria_filtro = st.selectbox("📂 Categoria", ["Todas", "Saladas", "Bebidas", "Pratos Principais", "Sobremesas", "Lanches"])
            with col3:
                max_calorias = st.slider("🔥 Máximo de calorias", 0, 1000, 500)
            with col4:
                dificuldade_filtro = st.selectbox("📊 Dificuldade", ["Todas", "Fácil", "Médio", "Difícil"])
            
            # Aplicar filtros
            receitas_filtradas = st.session_state.receitas.copy()
            
            if busca:
                receitas_filtradas = [r for r in receitas_filtradas 
                                    if busca.lower() in r['nome'].lower() or 
                                    any(busca.lower() in ing.lower() for ing in r['ingredientes'])]
            
            if categoria_filtro != "Todas":
                receitas_filtradas = [r for r in receitas_filtradas if r['categoria'] == categoria_filtro]
            
            if dificuldade_filtro != "Todas":
                receitas_filtradas = [r for r in receitas_filtradas if r.get('dificuldade') == dificuldade_filtro]
            
            receitas_filtradas = [r for r in receitas_filtradas if r['calorias'] <= max_calorias]
            
            # Estatísticas dos resultados
            if receitas_filtradas:
                st.markdown(f"""
                <div style="background: #667eea15; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #667eea;">
                    <div style="color: #667eea; font-weight: 600;">
                        {len(receitas_filtradas)} receitas encontradas | Média: {sum(r['calorias'] for r in receitas_filtradas)/len(receitas_filtradas):.0f} kcal
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Lista de receitas
                for receita in receitas_filtradas:
                    with st.expander(f"🍳 {receita['nome']} - {receita['calorias']} kcal"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown("**📝 Ingredientes:**")
                            for ingrediente in receita['ingredientes']:
                                st.write(f"• {ingrediente}")
                            
                            st.markdown(f"**👨‍🍳 Preparo:**")
                            st.write(receita['preparo'])
                            
                            if receita.get('tempo_preparo'):
                                st.write(f"**⏰ Tempo:** {receita['tempo_preparo']}")
                        
                        with col2:
                            # Card nutricional
                            st.markdown(f'''
                            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 15px; border: 2px solid #e2e8f0;">
                                <div style="text-align: center; margin-bottom: 1rem;">
                                    <div style="color: #667eea; font-size: 1.5rem; font-weight: 700;">{receita['calorias']} kcal</div>
                                    <div style="color: #718096; font-size: 0.9rem;">por porção</div>
                                </div>
                            ''', unsafe_allow_html=True)
                            
                            if 'proteinas' in receita:
                                col_a, col_b, col_c = st.columns(3)
                                with col_a:
                                    st.metric("🥩", f"{receita['proteinas']}g", label="Proteínas")
                                with col_b:
                                    st.metric("🍞", f"{receita['carboidratos']}g", label="Carboidratos")
                                with col_c:
                                    st.metric("🥑", f"{receita['gorduras']}g", label="Gorduras")
                            
                            st.markdown(f"**📂** {receita['categoria']}")
                            if receita.get('dificuldade'):
                                st.markdown(f"**📊** {receita['dificuldade']}")
                            
                            if st.button("📋 Usar na Dieta", key=f"usar_{receita['id']}"):
                                st.success("Receita adicionada ao plano!")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #718096;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">Nenhuma receita encontrada</div>
                    <div>Tente ajustar os filtros de busca</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("Adicionar Nova Receita")
            
            with st.form("nova_receita"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nome_receita = st.text_input("🍳 Nome da Receita *", placeholder="Ex: Salada Caesar Fitness")
                    categoria_receita = st.selectbox("📂 Categoria", ["Saladas", "Bebidas", "Pratos Principais", "Sobremesas", "Lanches"])
                    tempo_preparo = st.text_input("⏰ Tempo de Preparo", placeholder="Ex: 20 minutos")
                    dificuldade = st.selectbox("📊 Dificuldade", ["Fácil", "Médio", "Difícil"])
                
                with col2:
                    calorias_receita = st.number_input("🔥 Calorias (kcal)", min_value=0, value=200)
                    proteinas_receita = st.number_input("🥩 Proteínas (g)", min_value=0.0, value=10.0, step=0.1)
                    carboidratos_receita = st.number_input("🍞 Carboidratos (g)", min_value=0.0, value=20.0, step=0.1)
                    gorduras_receita = st.number_input("🥑 Gorduras (g)", min_value=0.0, value=5.0, step=0.1)
                
                ingredientes_receita = st.text_area("📝 Ingredientes (um por linha)", 
                                                   placeholder="200g de frango\n1 xícara de arroz integral\n2 colheres de azeite\n...")
                preparo_receita = st.text_area("👨‍🍳 Modo de Preparo", 
                                              placeholder="1. Tempere o frango...\n2. Aqueça a panela...\n3. Sirva quente...")
                
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
                            "dificuldade": dificuldade,
                            "data_criacao": datetime.now().strftime("%d/%m/%Y")
                        }
                        
                        st.session_state.receitas.append(nova_receita)
                        st.success(f"Receita '{nome_receita}' adicionada com sucesso!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Preencha todos os campos obrigatórios!")
            
            st.markdown('</div>', unsafe_allow_html=True)

    def agendamentos_page(self):
        """Sistema de agendamentos otimizado"""
        st.markdown('<div class="main-header"><h1>📅 Sistema de Agendamentos</h1><p>Gestão completa de consultas e compromissos</p></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📅 Agenda do Dia", "➕ Novo Agendamento", "📊 Relatórios"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            
            # Seletor de data aprimorado
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                data_filtro = st.date_input("📅 Selecionar data", value=datetime.now().date())
            with col2:
                if st.button("⬅️ Dia Anterior"):
                    data_filtro = data_filtro - timedelta(days=1)
                    st.rerun()
            with col3:
                if st.button("Dia Seguinte ➡️"):
                    data_filtro = data_filtro + timedelta(days=1)
                    st.rerun()
            
            # Verificar ações rápidas
            if st.session_state.get('quick_action') == 'agendar':
                st.session_state.quick_action = None
                st.info("Função de agendamento rápido ativada!")
            
            data_str = data_filtro.strftime('%Y-%m-%d')
            agendamentos_dia = [a for a in st.session_state.agendamentos if a.get('data') == data_str]
            
            st.subheader(f"📋 Agenda para {data_filtro.strftime('%d/%m/%Y')}")
            
            if agendamentos_dia:
                agendamentos_dia.sort(key=lambda x: x['horario'])
                
                for i, agendamento in enumerate(agendamentos_dia):
                    status_colors = {
                        "Agendado": "#667eea",
                        "Realizado": "#48bb78", 
                        "Cancelado": "#e53e3e",
                        "Em andamento": "#ed8936"
                    }
                    cor = status_colors.get(agendamento.get('status', 'Agendado'), '#718096')
                    
                    with st.expander(f"🕐 {agendamento['horario']} - {agendamento['paciente']} - {agendamento['tipo']}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**👤 Paciente:** {agendamento['paciente']}")
                            st.write(f"**📋 Tipo:** {agendamento['tipo']}")
                            st.write(f"**🕐 Horário:** {agendamento['horario']}")
                            if agendamento.get('duracao'):
                                st.write(f"**⏱️ Duração:** {agendamento['duracao']}")
                        
                        with col2:
                            status_atual = agendamento.get('status', 'Agendado')
                            st.markdown(f'''
                            <div style="background: {cor}15; padding: 1rem; border-radius: 10px; border-left: 4px solid {cor};">
                                <div style="color: {cor}; font-weight: 600;">Status: {status_atual}</div>
                            </div>
                            ''', unsafe_allow_html=True)
                            
                            if agendamento.get('valor'):
                                st.write(f"**💰 Valor:** R$ {agendamento['valor']:.2f}")
                            
                            if agendamento.get('observacoes'):
                                st.write(f"**📝 Obs:** {agendamento['observacoes']}")
                        
                        with col3:
                            novo_status = st.selectbox("Alterar Status", 
                                                     ["Agendado", "Em andamento", "Realizado", "Cancelado"], 
                                                     index=["Agendado", "Em andamento", "Realizado", "Cancelado"].index(status_atual),
                                                     key=f"status_{i}")
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("💾 Salvar", key=f"salvar_{i}"):
                                    agendamento['status'] = novo_status
                                    st.success("Status atualizado!")
                                    time.sleep(1)
                                    st.rerun()
                            
                            with col_b:
                                if st.button("📱 WhatsApp", key=f"whats_{i}"):
                                    st.success("Mensagem enviada!")
            else:
                st.markdown(f"""
                <div style="text-align: center; padding: 3rem; color: #718096;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📅</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">Nenhum agendamento para {data_filtro.strftime('%d/%m/%Y')}</div>
                    <div>Que tal aproveitar para planejar ou descansar?</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("Agendar Nova Consulta")
            
            with st.form("novo_agendamento"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.session_state.pacientes:
                        paciente_agendamento = st.selectbox("👤 Selecionar Paciente", 
                                                          ["Novo paciente"] + [p['nome'] for p in st.session_state.pacientes])
                        
                        if paciente_agendamento == "Novo paciente":
                            paciente_agendamento = st.text_input("Nome do novo paciente")
                    else:
                        paciente_agendamento = st.text_input("👤 Nome do Paciente")
                    
                    data_agendamento = st.date_input("📅 Data da Consulta", min_value=datetime.now().date())
                    horario_agendamento = st.time_input("🕐 Horário", value=datetime.now().replace(minute=0, second=0).time())
                
                with col2:
                    tipo_consulta = st.selectbox("📋 Tipo de Consulta", [
                        "Consulta Inicial", "Retorno", "Avaliação Nutricional", 
                        "Consulta Online", "Urgência", "Acompanhamento"
                    ])
                    
                    duracao = st.selectbox("⏱️ Duração", ["30 min", "45 min", "60 min", "90 min", "120 min"])
                    valor = st.number_input("💰 Valor (R$)", min_value=0.0, 
                                          value=st.session_state.configuracoes.get('valor_consulta', 150.0), step=10.0)
                
                observacoes_agendamento = st.text_area("📝 Observações", 
                                                     placeholder="Informações importantes sobre a consulta...")
                
                # Verificar conflitos de horário
                data_hora_str = f"{data_agendamento.strftime('%Y-%m-%d')} {horario_agendamento.strftime('%H:%M')}"
                conflitos = [a for a in st.session_state.agendamentos 
                           if a.get('data') == data_agendamento.strftime('%Y-%m-%d') and 
                           a.get('horario') == horario_agendamento.strftime('%H:%M')]
                
                if conflitos:
                    st.warning(f"⚠️ Conflito de horário detectado! Já existe um agendamento em {horario_agendamento.strftime('%H:%M')}")
                
                submitted = st.form_submit_button("✅ Confirmar Agendamento", use_container_width=True, type="primary")
                
                if submitted and paciente_agendamento:
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
                    st.success(f"Consulta agendada para {paciente_agendamento} em {data_agendamento.strftime('%d/%m/%Y')} às {horario_agendamento.strftime('%H:%M')}!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            if st.session_state.agendamentos:
                st.subheader("Relatório de Agendamentos")
                
                # Métricas de agendamento
                total_agendamentos = len(st.session_state.agendamentos)
                realizados = len([a for a in st.session_state.agendamentos if a.get('status') == 'Realizado'])
                cancelados = len([a for a in st.session_state.agendamentos if a.get('status') == 'Cancelado'])
                receita_total = sum([a.get('valor', 0) for a in st.session_state.agendamentos if a.get('status') == 'Realizado'])
                
                col1, col2, col3, col4 = st.columns(4)
                
                metrics_agendamento = [
                    ("📅 Total de Agendamentos", total_agendamentos, "#667eea"),
                    ("✅ Consultas Realizadas", realizados, "#48bb78"),
                    ("❌ Cancelamentos", cancelados, "#e53e3e"),
                    ("💰 Receita Gerada", f"R$ {receita_total:.2f}", "#ed8936")
                ]
                
                for i, (col, (label, valor, cor)) in enumerate(zip([col1, col2, col3, col4], metrics_agendamento)):
                    with col:
                        st.markdown(f'''
                        <div class="metric-card">
                            <div class="metric-container">
                                <div class="metric-value" style="color: {cor};">{valor}</div>
                                <div class="metric-label">{label}</div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                
                # Gráficos de análise
                col1, col2 = st.columns(2)
                
                with col1:
                    # Status dos agendamentos
                    status_counts = pd.Series([a.get('status', 'Agendado') for a in st.session_state.agendamentos]).value_counts()
                    
                    fig = create_interactive_chart(
                        pd.DataFrame({'Status': status_counts.index, 'Quantidade': status_counts.values}),
                        "pie", "Distribuição por Status", 'Status', 'Quantidade'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Tipos de consulta
                    tipos_counts = pd.Series([a.get('tipo', 'Consulta') for a in st.session_state.agendamentos]).value_counts()
                    
                    fig = create_interactive_chart(
                        pd.DataFrame({'Tipo': tipos_counts.index, 'Quantidade': tipos_counts.values}),
                        "bar", "Tipos de Consulta", 'Tipo', 'Quantidade'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Taxa de conversão
                if total_agendamentos > 0:
                    taxa_realizacao = (realizados / total_agendamentos) * 100
                    taxa_cancelamento = (cancelados / total_agendamentos) * 100
                    
                    st.subheader("📊 Indicadores de Performance")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f'''
                        <div style="background: #48bb7815; padding: 1.5rem; border-radius: 15px; text-align: center; border: 2px solid #48bb78;">
                            <div style="color: #48bb78; font-size: 2rem; font-weight: 700;">{taxa_realizacao:.1f}%</div>
                            <div style="color: #48bb78; font-weight: 600;">Taxa de Realização</div>
                            <div style="color: #718096; margin-top: 0.5rem;">Consultas realizadas vs agendadas</div>
                        </div>
                        ''', unsafe_allow_html=True)
                    
                    with col2:
                        cor_cancelamento = "#e53e3e" if taxa_cancelamento > 15 else "#ed8936" if taxa_cancelamento > 10 else "#48bb78"
                        st.markdown(f'''
                        <div style="background: {cor_cancelamento}15; padding: 1.5rem; border-radius: 15px; text-align: center; border: 2px solid {cor_cancelamento};">
                            <div style="color: {cor_cancelamento}; font-size: 2rem; font-weight: 700;">{taxa_cancelamento:.1f}%</div>
                            <div style="color: {cor_cancelamento}; font-weight: 600;">Taxa de Cancelamento</div>
                            <div style="color: #718096; margin-top: 0.5rem;">Meta: abaixo de 10%</div>
                        </div>
                        ''', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #718096;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">Nenhum dado para análise</div>
                    <div>Agende consultas para ver relatórios detalhados</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    def relatorios_page(self):
        """Relatórios profissionais avançados"""
        st.markdown('<div class="main-header"><h1>📈 Relatórios Profissionais</h1><p>Análises detalhadas e insights estratégicos</p></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["📊 Gerar Relatórios", "📋 Histórico"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Relatório de Pacientes")
                
                if st.button("📈 Gerar Relatório Completo", use_container_width=True, type="primary"):
                    if st.session_state.pacientes:
                        # Análise estatística
                        df_pacientes = pd.DataFrame(st.session_state.pacientes)
                        
                        st.markdown("**📋 Resumo Executivo**")
                        
                        # Métricas principais
                        col_a, col_b, col_c, col_d = st.columns(4)
                        
                        with col_a:
                            st.metric("Total de Pacientes", len(df_pacientes))
                        with col_b:
                            st.metric("IMC Médio", f"{df_pacientes['imc'].mean():.1f}")
                        with col_c:
                            st.metric("Idade Média", f"{df_pacientes['idade'].mean():.0f} anos")
                        with col_d:
                            peso_medio = df_pacientes['peso'].mean()
                            st.metric("Peso Médio", f"{peso_medio:.1f} kg")
                        
                        # Análise de objetivos
                        st.subheader("🎯 Distribuição por Objetivos")
                        objetivo_counts = df_pacientes['objetivo'].value_counts()
                        
                        fig = create_interactive_chart(
                            pd.DataFrame({'Objetivo': objetivo_counts.index, 'Quantidade': objetivo_counts.values}),
                            "pie", "Objetivos dos Pacientes", 'Objetivo', 'Quantidade'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Análise de IMC detalhada
                        st.subheader("📊 Análise de IMC")
                        
                        imc_categorias = df_pacientes['imc'].apply(self.classificar_imc).value_counts()
                        
                        for categoria, quantidade in imc_categorias.items():
                            percentual = (quantidade / len(df_pacientes)) * 100
                            
                            status_colors = {
                                "Abaixo do peso": "#ed8936",
                                "Normal": "#48bb78",
                                "Sobrepeso": "#ed8936",
                                "Obesidade": "#e53e3e"
                            }
                            cor = status_colors.get(categoria, "#718096")
                            
                            st.markdown(f'''
                            <div style="background: {cor}15; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {cor};">
                                <div style="color: {cor}; font-weight: 600;">
                                    {categoria}: {quantidade} pacientes ({percentual:.1f}%)
                                </div>
                            </div>
                            ''', unsafe_allow_html=True)
                        
                        # Tabela detalhada
                        st.subheader("📋 Lista Detalhada de Pacientes")
                        st.dataframe(
                            df_pacientes[['nome', 'idade', 'peso', 'altura', 'imc', 'objetivo', 'data_cadastro']], 
                            use_container_width=True
                        )
                        
                        # Botão de download
                        csv = df_pacientes.to_csv(index=False)
                        st.download_button(
                            label="📥 Baixar Relatório em CSV",
                            data=csv,
                            file_name=f"relatorio_pacientes_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.info("Cadastre pacientes primeiro para gerar relatórios")
            
            with col2:
                st.subheader("📅 Relatório Financeiro")
                
                if st.button("💰 Gerar Análise Financeira", use_container_width=True, type="primary"):
                    if st.session_state.agendamentos:
                        agendamentos_realizados = [a for a in st.session_state.agendamentos if a.get('status') == 'Realizado']
                        
                        if agendamentos_realizados:
                            receita_total = sum([a.get('valor', 0) for a in agendamentos_realizados])
                            media_consulta = receita_total / len(agendamentos_realizados)
                            
                            # Métricas financeiras
                            col_a, col_b, col_c = st.columns(3)
                            
                            with col_a:
                                st.metric("💰 Receita Total", f"R$ {receita_total:.2f}")
                            with col_b:
                                st.metric("📊 Consultas Realizadas", len(agendamentos_realizados))
                            with col_c:
                                st.metric("💡 Ticket Médio", f"R$ {media_consulta:.2f}")
                            
                            # Análise por tipo de consulta
                            df_fin = pd.DataFrame(agendamentos_realizados)
                            receita_por_tipo = df_fin.groupby('tipo')['valor'].agg(['sum', 'count', 'mean']).reset_index()
                            receita_por_tipo.columns = ['Tipo', 'Receita Total', 'Quantidade', 'Ticket Médio']
                            
                            st.subheader("📊 Receita por Tipo de Consulta")
                            
                            fig = create_interactive_chart(
                                receita_por_tipo, "bar", "Receita por Tipo de Consulta", 'Tipo', 'Receita Total'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Tabela detalhada
                            st.subheader("📋 Detalhamento por Tipo")
                            st.dataframe(receita_por_tipo, use_container_width=True)
                            
                            # Projeções
                            st.subheader("📈 Projeções")
                            
                            dias_no_mes = 30
                            consultas_por_dia = len(agendamentos_realizados) / 30  # Assumindo dados do último mês
                            projecao_mensal = consultas_por_dia * dias_no_mes * media_consulta
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.metric("📅 Consultas/dia (média)", f"{consultas_por_dia:.1f}")
                            with col_b:
                                st.metric("📊 Projeção Mensal", f"R$ {projecao_mensal:.2f}")
                        else:
                            st.info("Nenhuma consulta realizada ainda")
                    else:
                        st.info("Nenhum agendamento para análise financeira")
            
            # Relatório consolidado
            st.markdown("---")
            st.subheader("📋 Relatório Consolidado")
            
            if st.button("📊 Gerar Relatório Executivo Completo", use_container_width=True, type="primary"):
                with st.spinner("Gerando relatório consolidado..."):
                    time.sleep(2)
                    
                    # Dados consolidados
                    total_pacientes = len(st.session_state.pacientes)
                    total_agendamentos = len(st.session_state.agendamentos)
                    total_receitas = len(st.session_state.receitas)
                    total_planos = len(st.session_state.planos_alimentares)
                    
                    st.markdown(f"""
                    ## 📊 Relatório Executivo - {datetime.now().strftime('%d/%m/%Y')}
                    
                    ### 📈 Visão Geral do Negócio
                    
                    **Pacientes:** {total_pacientes} cadastrados
                    **Agendamentos:** {total_agendamentos} total
                    **Receitas:** {total_receitas} no banco
                    **Planos Criados:** {total_planos}
                    
                    ### 💼 Insights Estratégicos
                    """)
                    
                    insights = []
                    
                    if total_pacientes > 0:
                        if st.session_state.pacientes:
                            imc_medio = sum([p['imc'] for p in st.session_state.pacientes]) / len(st.session_state.pacientes)
                            if imc_medio > 25:
                                insights.append("🎯 **Oportunidade:** IMC médio elevado - foco em programas de emagrecimento")
                            
                            objetivos = [p['objetivo'] for p in st.session_state.pacientes]
                            objetivo_principal = max(set(objetivos), key=objetivos.count)
                            insights.append(f"📊 **Tendência:** {objetivo_principal} é o objetivo mais comum")
                    
                    if st.session_state.agendamentos:
                        realizados = len([a for a in st.session_state.agendamentos if a.get('status') == 'Realizado'])
                        taxa_realizacao = (realizados / len(st.session_state.agendamentos)) * 100
                        
                        if taxa_realizacao > 90:
                            insights.append("✅ **Excelente:** Alta taxa de realização de consultas")
                        elif taxa_realizacao < 70:
                            insights.append("⚠️ **Atenção:** Taxa de realização baixa - revisar processo")
                    
                    if not insights:
                        insights = ["📈 Continue crescendo sua base de dados para insights mais precisos"]
                    
                    for insight in insights:
                        st.markdown(insight)
                    
                    # Recomendações
                    st.markdown("### 💡 Recomendações")
                    
                    recomendacoes = [
                        "📱 Implementar lembretes automáticos via WhatsApp",
                        "📊 Criar mais receitas para diversificar opções",
                        "🎯 Focar em campanhas para objetivos mais procurados",
                        "📈 Monitorar KPIs semanalmente"
                    ]
                    
                    for rec in recomendacoes:
                        st.markdown(f"• {rec}")
                    
                    st.success("Relatório executivo gerado com sucesso!")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📚 Histórico de Relatórios")
            
            st.info("Funcionalidade de histórico de relatórios em desenvolvimento")
            
            # Simulação de histórico
            historico_simulado = [
                {"data": "15/12/2024", "tipo": "Pacientes", "status": "Gerado"},
                {"data": "10/12/2024", "tipo": "Financeiro", "status": "Gerado"},
                {"data": "05/12/2024", "tipo": "Executivo", "status": "Gerado"}
            ]
            
            for item in historico_simulado:
                st.markdown(f'''
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #667eea;">
                    <div style="font-weight: 600;">📊 Relatório {item['tipo']}</div>
                    <div style="color: #718096; font-size: 0.9rem;">
                        {item['data']} - Status: {item['status']}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    def comunicacao_page(self):
        """Central de comunicação melhorada"""
        st.markdown('<div class="main-header"><h1>💬 Central de Comunicação</h1><p>Mantenha contato direto com seus pacientes</p></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📱 WhatsApp", "📧 Email", "📊 Histórico"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📱 Mensagens WhatsApp")
            
            if st.session_state.pacientes:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    paciente_msg = st.selectbox("👤 Selecionar Paciente", [p['nome'] for p in st.session_state.pacientes])
                    
                    # Mostrar info do paciente
                    paciente_selecionado = next(p for p in st.session_state.pacientes if p['nome'] == paciente_msg)
                    
                    st.markdown(f'''
                    <div style="background: #48bb7815; padding: 1rem; border-radius: 10px; border-left: 4px solid #48bb78;">
                        <div style="color: #48bb78; font-weight: 600;">Paciente Selecionado</div>
                        <div style="color: #2d3748;">
                            📱 {paciente_selecionado.get('telefone', 'Não informado')}<br>
                            🎯 {paciente_selecionado['objetivo']}<br>
                            📅 Cadastro: {paciente_selecionado['data_cadastro']}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    tipo_mensagem = st.selectbox("📋 Tipo de Mensagem", [
                        "Lembrete de Consulta",
                        "Plano Alimentar",
                        "Motivacional",
                        "Resultados",
                        "Personalizada"
                    ])
                    
                    # Templates predefinidos
                    templates = {
                        "Lembrete de Consulta": f"Olá {paciente_msg}! 👋\n\nLembrando que você tem consulta marcada. Por favor, confirme sua presença.\n\nAté logo! 😊",
                        "Plano Alimentar": f"Oi {paciente_msg}! 🍽️\n\nSeu novo plano alimentar está pronto! Siga as orientações e qualquer dúvida me procure.\n\nVamos juntos nessa jornada! 💪",
                        "Motivacional": f"Oi {paciente_msg}! ⭐\n\nParabéns pelo seu progresso! Continue firme no seu objetivo. Você está indo muito bem!\n\nConto com você! 🎯",
                        "Resultados": f"Olá {paciente_msg}! 📊\n\nSeus resultados estão ótimos! Continue seguindo o plano que traçamos.\n\nEstou orgulhosa do seu empenho! 👏",
                        "Personalizada": ""
                    }
                    
                    mensagem_inicial = templates.get(tipo_mensagem, "")
                    mensagem_final = st.text_area("💬 Mensagem", value=mensagem_inicial, height=120)
                    
                    # Preview da mensagem
                    st.markdown("**📱 Preview da Mensagem:**")
                    st.markdown(f'''
                    <div style="background: #25d366; color: white; padding: 1rem; border-radius: 15px 15px 15px 5px; max-width: 300px;">
                        {mensagem_final.replace(chr(10), '<br>')}
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("📤 Enviar Mensagem", type="primary", use_container_width=True):
                            with st.spinner("Enviando mensagem..."):
                                time.sleep(1)
                                st.success(f"✅ Mensagem enviada para {paciente_msg}!")
                                
                                # Simular salvar no histórico
                                if 'historico_comunicacao' not in st.session_state:
                                    st.session_state.historico_comunicacao = []
                                
                                st.session_state.historico_comunicacao.append({
                                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                                    "paciente": paciente_msg,
                                    "tipo": "WhatsApp",
                                    "assunto": tipo_mensagem,
                                    "status": "Enviado"
                                })
                    
                    with col_b:
                        if st.button("👁️ Pré-visualizar", use_container_width=True):
                            st.info("💡 Em produção, abriria o WhatsApp Web")
            else:
                st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #718096;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">👥</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">Cadastre pacientes primeiro</div>
                    <div>Para enviar mensagens, você precisa ter pacientes cadastrados</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📧 Envio de Emails")
            
            if st.session_state.pacientes:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    paciente_email = st.selectbox("👤 Selecionar Paciente", 
                                                [p['nome'] for p in st.session_state.pacientes], key="email_paciente")
                    
                    # Mostrar email do paciente
                    paciente_email_sel = next(p for p in st.session_state.pacientes if p['nome'] == paciente_email)
                    
                    st.markdown(f'''
                    <div style="background: #3182ce15; padding: 1rem; border-radius: 10px; border-left: 4px solid #3182ce;">
                        <div style="color: #3182ce; font-weight: 600;">Email do Paciente</div>
                        <div style="color: #2d3748;">
                            📧 {paciente_email_sel.get('email', 'Email não informado')}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                    
                    anexar_opcoes = st.multiselect("📎 Anexar", [
                        "Plano Alimentar",
                        "Relatório de Progresso", 
                        "Receitas Personalizadas",
                        "Orientações Gerais"
                    ])
                
                with col2:
                    assunto = st.text_input("📋 Assunto", value="Acompanhamento Nutricional - NutriClinic")
                    
                    corpo_email = st.text_area("📧 Corpo do Email", 
                                             value=f"""Olá {paciente_email}!

Espero que esteja bem e seguindo as orientações nutricionais.

Estou enviando este email para acompanhar seu progresso e esclarecer eventuais dúvidas.

Lembre-se:
• Siga o plano alimentar estabelecido
• Mantenha-se hidratado(a)
• Pratique atividades físicas regularmente
• Entre em contato em caso de dúvidas

Estou aqui para te apoiar nessa jornada!

Atenciosamente,
Sua Nutricionista
NutriClinic Pro""", 
                                             height=200)
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("📤 Enviar Email", type="primary", use_container_width=True):
                            with st.spinner("Enviando email..."):
                                time.sleep(1)
                                st.success(f"✅ Email enviado para {paciente_email}!")
                                
                                # Salvar no histórico
                                if 'historico_comunicacao' not in st.session_state:
                                    st.session_state.historico_comunicacao = []
                                
                                st.session_state.historico_comunicacao.append({
                                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                                    "paciente": paciente_email,
                                    "tipo": "Email",
                                    "assunto": assunto,
                                    "anexos": len(anexar_opcoes),
                                    "status": "Enviado"
                                })
                    
                    with col_b:
                        if st.button("💾 Salvar Rascunho", use_container_width=True):
                            st.info("Rascunho salvo com sucesso!")
            else:
                st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #718096;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">👥</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">Cadastre pacientes primeiro</div>
                    <div>Para enviar emails, você precisa ter pacientes cadastrados</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📊 Histórico de Comunicações")
            
            if st.session_state.get('historico_comunicacao'):
                # Filtros do histórico
                col1, col2, col3 = st.columns(3)
                with col1:
                    filtro_tipo = st.selectbox("Filtrar por tipo", ["Todos", "WhatsApp", "Email"])
                with col2:
                    filtro_paciente = st.selectbox("Filtrar por paciente", 
                                                 ["Todos"] + list(set([h['paciente'] for h in st.session_state.historico_comunicacao])))
                with col3:
                    ordenar_por = st.selectbox("Ordenar por", ["Mais recente", "Mais antigo", "Paciente"])
                
                # Aplicar filtros
                historico_filtrado = st.session_state.historico_comunicacao.copy()
                
                if filtro_tipo != "Todos":
                    historico_filtrado = [h for h in historico_filtrado if h['tipo'] == filtro_tipo]
                
                if filtro_paciente != "Todos":
                    historico_filtrado = [h for h in historico_filtrado if h['paciente'] == filtro_paciente]
                
                # Exibir histórico
                if historico_filtrado:
                    for item in historico_filtrado:
                        tipo_icon = "📱" if item['tipo'] == "WhatsApp" else "📧"
                        tipo_color = "#25d366" if item['tipo'] == "WhatsApp" else "#3182ce"
                        
                        st.markdown(f'''
                        <div style="background: {tipo_color}15; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {tipo_color};">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <div style="color: {tipo_color}; font-weight: 600;">
                                        {tipo_icon} {item['tipo']} - {item['paciente']}
                                    </div>
                                    <div style="color: #2d3748; margin: 0.5rem 0;">
                                        <strong>Assunto:</strong> {item['assunto']}
                                    </div>
                                    <div style="color: #718096; font-size: 0.9rem;">
                                        {item['data']} - Status: {item['status']}
                                    </div>
                                </div>
                                <div style="color: {tipo_color}; font-size: 0.9rem;">
                                    ✅ {item['status']}
                                </div>
                            </div>
                        </div>
                        ''', unsafe_allow_html=True)
                else:
                    st.info("Nenhuma comunicação encontrada com os filtros aplicados")
            else:
                st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #718096;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                    <div style="font-size: 1.2rem; font-weight: 600;">Histórico vazio</div>
                    <div>As comunicações enviadas aparecerão aqui</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    def configuracoes_page(self):
        """Página de configurações completa"""
        st.markdown('<div class="main-header"><h1>⚙️ Configurações do Sistema</h1><p>Personalize sua experiência profissional</p></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["🏢 Perfil", "💰 Negócio", "🔧 Sistema"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🏢 Informações Profissionais")
            
            with st.form("config_empresa"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nome_empresa = st.text_input("🏢 Nome da Clínica/Consultório", 
                                               value=st.session_state.configuracoes.get('empresa_nome', ''))
                    email_empresa = st.text_input("📧 Email Profissional", 
                                                value=st.session_state.configuracoes.get('email', ''))
                    whatsapp_empresa = st.text_input("📱 WhatsApp Business", 
                                                   value=st.session_state.configuracoes.get('whatsapp', ''))
                    
                    especializacoes = st.multiselect("🎯 Especializações", [
                        "Emagrecimento", "Ganho de massa", "Nutrição esportiva",
                        "Nutrição clínica", "Pediatria", "Geriatria", 
                        "Vegetarianismo", "Transtornos alimentares"
                    ])
                
                with col2:
                    endereco_empresa = st.text_area("📍 Endereço Completo", 
                                                  value=st.session_state.configuracoes.get('endereco', ''))
                    
                    cidade_empresa = st.text_input("🏙️ Cidade", value=st.session_state.configuracoes.get('cidade', ''))
                    
                    cep_empresa = st.text_input("📮 CEP", value=st.session_state.configuracoes.get('cep', ''))
                    
                    crn_numero = st.text_input("📋 Número do CRN", value=st.session_state.configuracoes.get('crn', ''))
                
                logo_upload = st.file_uploader("📷 Upload do Logo", type=['png', 'jpg', 'jpeg'])
                
                biografia = st.text_area("📝 Biografia Profissional", 
                                       value=st.session_state.configuracoes.get('biografia', ''),
                                       placeholder="Conte um pouco sobre sua formação e experiência...")
                
                if st.form_submit_button("💾 Salvar Informações", use_container_width=True, type="primary"):
                    st.session_state.configuracoes.update({
                        'empresa_nome': nome_empresa,
                        'email': email_empresa,
                        'whatsapp': whatsapp_empresa,
                        'endereco': endereco_empresa,
                        'cidade': cidade_empresa,
                        'cep': cep_empresa,
                        'crn': crn_numero,
                        'especializacoes': especializacoes,
                        'biografia': biografia
                    })
                    
                    if logo_upload:
                        st.session_state.configuracoes['empresa_logo'] = logo_upload
                    
                    st.success("✅ Informações salvas com sucesso!")
                    time.sleep(1)
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("💰 Configurações de Negócio")
            
            with st.form("config_financeiro"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**💰 Valores e Horários**")
                    valor_consulta = st.number_input("💰 Valor da Consulta (R$)", 
                                                   min_value=0.0, 
                                                   value=st.session_state.configuracoes.get('valor_consulta', 150.0))
                    
                    valor_retorno = st.number_input("🔄 Valor do Retorno (R$)", 
                                                  min_value=0.0, 
                                                  value=st.session_state.configuracoes.get('valor_retorno', 100.0))
                    
                    tempo_consulta = st.selectbox("⏱️ Duração da Consulta", 
                                                [30, 45, 60, 90], 
                                                index=[30, 45, 60, 90].index(st.session_state.configuracoes.get('tempo_consulta', 60)))
                    
                    intervalo_consultas = st.selectbox("📅 Intervalo entre Consultas", [15, 30, 45, 60], index=1)
                
                with col2:
                    st.markdown("**🕐 Horário de Funcionamento**")
                    horario_inicio = st.time_input("🌅 Horário de Início", 
                                                 value=datetime.strptime(st.session_state.configuracoes.get('horario_inicio', '08:00'), '%H:%M').time())
                    
                    horario_fim = st.time_input("🌆 Horário de Fim", 
                                              value=datetime.strptime(st.session_state.configuracoes.get('horario_fim', '18:00'), '%H:%M').time())
                    
                    horario_almoco_inicio = st.time_input("🍽️ Início do Almoço", value=datetime.strptime("12:00", '%H:%M').time())
                    horario_almoco_fim = st.time_input("🍽️ Fim do Almoço", value=datetime.strptime("13:00", '%H:%M').time())
                
                dias_trabalho = st.multiselect("📅 Dias de Atendimento", 
                                             ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
                                             default=st.session_state.configuracoes.get('dias_trabalho', ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]))
                
                # Configurações de pagamento
                st.markdown("**💳 Formas de Pagamento Aceitas**")
                formas_pagamento = st.multiselect("Selecione as formas aceitas", [
                    "Dinheiro", "PIX", "Cartão de Débito", "Cartão de Crédito",
                    "Transferência Bancária", "Boleto", "Planos de Saúde"
                ])
                
                politica_cancelamento = st.text_area("📋 Política de Cancelamento", 
                                                   placeholder="Ex: Cancelamentos devem ser feitos com 24h de antecedência...")
                
                if st.form_submit_button("💾 Salvar Configurações", use_container_width=True, type="primary"):
                    st.session_state.configuracoes.update({
                        'valor_consulta': valor_consulta,
                        'valor_retorno': valor_retorno,
                        'tempo_consulta': tempo_consulta,
                        'intervalo_consultas': intervalo_consultas,
                        'horario_inicio': horario_inicio.strftime('%H:%M'),
                        'horario_fim': horario_fim.strftime('%H:%M'),
                        'horario_almoco_inicio': horario_almoco_inicio.strftime('%H:%M'),
                        'horario_almoco_fim': horario_almoco_fim.strftime('%H:%M'),
                        'dias_trabalho': dias_trabalho,
                        'formas_pagamento': formas_pagamento,
                        'politica_cancelamento': politica_cancelamento
                    })
                    
                    st.success("✅ Configurações de negócio salvas!")
                    time.sleep(1)
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🔧 Configurações do Sistema")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Estatísticas do Sistema**")
                
                # Estatísticas em cards
                stats = [
                    ("👥 Pacientes", len(st.session_state.pacientes), "#667eea"),
                    ("📅 Agendamentos", len(st.session_state.agendamentos), "#48bb78"),
                    ("🍳 Receitas", len(st.session_state.receitas), "#ed8936"),
                    ("🍽️ Planos", len(st.session_state.planos_alimentares), "#9f7aea")
                ]
                
                for label, valor, cor in stats:
                    st.markdown(f'''
                    <div style="background: {cor}15; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {cor};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div style="color: {cor}; font-weight: 600;">{label}</div>
                            <div style="color: {cor}; font-size: 1.3rem; font-weight: 700;">{valor}</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown("**🔄 Backup e Exportação**")
                if st.button("💾 Gerar Backup Completo", use_container_width=True):
                    backup_data = {
                        "pacientes": st.session_state.pacientes,
                        "agendamentos": st.session_state.agendamentos,
                        "receitas": st.session_state.receitas,
                        "planos_alimentares": st.session_state.planos_alimentares,
                        "configuracoes": st.session_state.configuracoes,
                        "data_backup": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "versao_sistema": "2.0"
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
                st.markdown("**🎨 Personalização da Interface**")
                
                # Seletor de tema
                tema_atual = st.session_state.configuracoes.get('cores_tema', 'azul')
                novo_tema = st.selectbox("🎨 Tema de Cores", 
                                       ["Azul", "Verde", "Rosa", "Roxo", "Laranja"],
                                       index=["azul", "verde", "rosa", "roxo", "laranja"].index(tema_atual) if tema_atual in ["azul", "verde", "rosa", "roxo", "laranja"] else 0)
                
                if st.button("🎨 Aplicar Novo Tema", use_container_width=True):
                    st.session_state.configuracoes['cores_tema'] = novo_tema.lower()
                    st.success(f"✅ Tema {novo_tema} aplicado!")
                    time.sleep(1)
                    st.rerun()
                
                # Configurações de notificação
                st.markdown("**🔔 Notificações**")
                notif_email = st.checkbox("📧 Notificações por email", value=True)
                notif_whatsapp = st.checkbox("📱 Lembretes WhatsApp", value=True)
                notif_sound = st.checkbox("🔊 Sons do sistema", value=False)
                
                # Configurações de privacidade
                st.markdown("**🔒 Privacidade e Segurança**")
                auto_logout = st.selectbox("⏰ Logout automático", ["15 min", "30 min", "1 hora", "2 horas", "Nunca"])
                backup_auto = st.checkbox("🔄 Backup automático semanal", value=True)
                
                if st.button("💾 Salvar Preferências", use_container_width=True):
                    st.session_state.configuracoes.update({
                        'notif_email': notif_email,
                        'notif_whatsapp': notif_whatsapp,
                        'notif_sound': notif_sound,
                        'auto_logout': auto_logout,
                        'backup_auto': backup_auto
                    })
                    st.success("✅ Preferências salvas!")
                
                st.markdown("**🗑️ Gerenciamento de Dados**")
                
                # Botões de limpeza com confirmação
                if st.button("🗑️ Limpar Dados de Teste", use_container_width=True, type="secondary"):
                    if 'confirm_delete' not in st.session_state:
                        st.session_state.confirm_delete = False
                    st.session_state.confirm_delete = True
                
                if st.session_state.get('confirm_delete', False):
                    st.warning("⚠️ Esta ação não pode ser desfeita!")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("✅ Confirmar", use_container_width=True):
                            st.session_state.pacientes = []
                            st.session_state.agendamentos = []
                            st.session_state.planos_alimentares = []
                            st.session_state.confirm_delete = False
                            st.success("✅ Dados de teste removidos!")
                            time.sleep(1)
                            st.rerun()
                    with col_b:
                        if st.button("❌ Cancelar", use_container_width=True):
                            st.session_state.confirm_delete = False
                            st.rerun()
                
                # Informações do sistema
                st.markdown("**ℹ️ Sobre o Sistema**")
                st.markdown(f'''
                <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 15px; border: 2px solid #e2e8f0;">
                    <div style="text-align: center; color: #667eea; font-weight: 600; margin-bottom: 1rem;">
                        🥗 NutriStock360 Pro
                    </div>
                    <div style="color: #2d3748; font-size: 0.9rem; line-height: 1.5;">
                        <strong>Versão:</strong> 2.0 Premium<br>
                        <strong>Desenvolvido:</strong> 2024<br>
                        <strong>Módulos:</strong> 9 completos<br>
                        <strong>Status:</strong> Totalmente funcional<br>
                        <strong>Suporte:</strong> Profissional<br>
                        <strong>Atualizações:</strong> Automáticas
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def run(self):
        """Executa o aplicativo principal"""
        if not st.session_state.authenticated:
            self.login_page()
        else:
            selected_page = self.sidebar_menu()
            
            # Roteamento das páginas
            if selected_page == "📊 Dashboard Interativo":
                self.dashboard_page()
            elif selected_page == "🧮 Calculadoras Inteligentes":
                self.calculadoras_page()
            elif selected_page == "👥 Gestão de Pacientes":
                self.pacientes_page()
            elif selected_page == "🍽️ Planos Alimentares":
                self.planos_alimentares_page()
            elif selected_page == "🍳 Banco de Receitas":
                self.receitas_page()
            elif selected_page == "📅 Agendamentos":
                self.agendamentos_page()
            elif selected_page == "📈 Relatórios Avançados":
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
        st.info("Recarregue a página ou entre em contato com o suporte.")import streamlit as st
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

# CSS avançado com animações e interatividade
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animações suaves */
    @keyframes slideInFromTop {
        0% { transform: translateY(-100px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes slideInFromLeft {
        0% { transform: translateX(-50px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    /* Header principal com gradiente animado */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 200% 200%;
        animation: gradient 6s ease infinite, slideInFromTop 0.8s ease-out;
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Cards com hover effects */
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        border-left: 6px solid #667eea;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeIn 0.6s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
        border-left-color: #f093fb;
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
    
    /* Sidebar melhorado */
    .sidebar-logo {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        margin-bottom: 1.5rem;
        animation: slideInFromLeft 0.8s ease-out;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* Resultados de calculadora */
    .calculator-result {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
        font-size: 1.2rem;
        animation: pulse 0.6s ease-in-out;
        box-shadow: 0 8px 25px rgba(132, 250, 176, 0.3);
        color: #2d3748;
    }
    
    /* Status cards com cores dinâmicas */
    .status-card {
        padding: 1.2rem;
        border-radius: 15px;
        margin: 0.8rem 0;
        text-align: center;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .status-card:hover {
        transform: scale(1.05);
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
    
    /* Tabs content melhorado */
    .tab-content {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: 1rem;
        animation: fadeIn 0.5s ease-out;
        border: 1px solid #e2e8f0;
    }
    
    /* Food cards */
    .food-card {
        background: linear-gradient(135deg, #f7fafc, #edf2f7);
        border: 2px solid #e2e8f0;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .food-card:hover {
        border-color: #667eea;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15);
    }
    
    /* Appointment cards */
    .appointment-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        animation: slideInFromLeft 0.5s ease-out;
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3);
    }
    
    /* Botões melhorados */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
    }
    
    /* Progress bars */
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #e2e8f0;
        border-radius: 4px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 4px;
        transition: width 1s ease-in-out;
    }
    
    /* Notification styles */
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: linear-gradient(135deg, #48bb78, #38a169);
        color: white;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.3);
        z-index: 1000;
        animation: slideInFromTop 0.5s ease-out;
    }
    
    /* Loading animation */
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive improvements */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem;
            border-radius: 15px;
        }
        
        .metric-card {
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .tab-content {
            padding: 1.5rem;
        }
    }
    
    /* Scrollbar customization */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #f093fb);
    }
    
    /* Input improvements */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Metric improvements */
    .metric-container {
        text-align: center;
        padding: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Success animations */
    .success-animation {
        animation: pulse 0.6s ease-in-out;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .tab-content {
            background: #2d3748;
            color: white;
        }
        
        .metric-card {
            background: #2d3748;
            color: white;
        }
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

# Função para mostrar notificações
def show_notification(message, type="success"):
    """Mostra notificação visual"""
    color = {
        "success": "#48bb78",
        "warning": "#ed8936", 
        "error": "#e53e3e",
        "info": "#3182ce"
    }.get(type, "#48bb78")
    
    st.markdown(f"""
    <div style="
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: {color};
        color: white;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.3);
        z-index: 1000;
        animation: slideInFromTop 0.5s ease-out;
    ">
        {message}
    </div>
    """, unsafe_allow_html=True)

# Função para criar gráficos interativos melhorados
def create_interactive_chart(data, chart_type, title, x_col, y_col):
    """Cria gráficos mais interativos"""
    if chart_type == "line":
        fig = px.line(data, x=x_col, y=y_col, title=title)
        fig.update_traces(
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(size=8)
        )
    elif chart_type == "bar":
        fig = px.bar(data, x=x_col, y=y_col, title=title)
        fig.update_traces(
            marker_color=px.colors.qualitative.Set3,
            textposition='auto'
        )
    elif chart_type == "pie":
        fig = px.pie(data, names=x_col, values=y_col, title=title)
    
    # Configurações avançadas
    fig.update_layout(
        title_font_size=18,
        title_x=0.5,
        showlegend=True,
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(family="Inter, sans-serif", size=18, color="#2d3748")
    )
    
    # Adicionar interatividade
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>%{y}<extra></extra>'
    )
    
    return fig

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
    
    def busca_global(self, termo):
        """Sistema de busca global inteligente"""
        resultados = {
            "pacientes": [],
            "receitas": [],
            "agendamentos": [],
            "planos": []
        }
        
        if not termo:
            return resultados
        
        termo = termo.lower()
        
        # Buscar em pacientes
        for paciente in st.session_state.pacientes:
            if (termo in paciente['nome'].lower() or 
                termo in paciente['email'].lower() or
                termo in paciente['objetivo'].lower()):
                resultados["pacientes"].append(paciente)
        
        # Buscar em receitas
        for receita in st.session_state.receitas:
            if (termo in receita['nome'].lower() or
                termo in receita['categoria'].lower() or
                any(termo in ing.lower() for ing in receita['ingredientes'])):
                resultados["receitas"].append(receita)
        
        # Buscar em agendamentos
        for agendamento in st.session_state.agendamentos:
            if (termo in agendamento['paciente'].lower() or
                termo in agendamento['tipo'].lower()):
                resultados["agendamentos"].append(agendamento)
        
        return resultados
    
    def login_page(self):
        """Página de login com design melhorado"""
        st.markdown('''
        <div class="main-header">
            <h1>🥗 NutriStock360 Pro</h1>
            <p>Sistema Profissional Avançado para Nutricionistas</p>
            <p><em>Versão 2.0 - Experiência Premium</em></p>
        </div>
        ''', unsafe_allow_html=True)
        
        # Busca global sempre visível
        with st.container():
            busca_termo = st.text_input("🔍 Busca Global", placeholder="Pesquisar pacientes, receitas, agendamentos...", key="busca_global_login")
            
            if busca_termo:
                resultados = self.busca_global(busca_termo)
                total_resultados = sum(len(r) for r in resultados.values())
                
                if total_resultados > 0:
                    st.info(f"Encontrados {total_resultados} resultados. Faça login para ver os detalhes.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="tab-content">
                <h3 style="text-align: center; color: #667eea; margin-bottom: 2rem;">🔐 Acesso Seguro ao Sistema</h3>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("login_form"):
                st.markdown("### Credenciais")
                username = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
                password = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    remember = st.checkbox("🔄 Lembrar de mim")
                with col_b:
                    auto_login = st.checkbox("⚡ Login automático")
                
                submitted = st.form_submit_button("🚀 Entrar no Sistema", use_container_width=True, type="primary")
                
                if submitted:
                    with st.spinner("Verificando credenciais..."):
                        time.sleep(1)  # Simular verificação
                        if self.authenticate_user(username, password):
                            st.success("✅ Login realizado com sucesso!")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Usuário ou senha incorretos!")
                            time.sleep(1)
            
            with st.expander("👥 Contas de Demonstração", expanded=False):
                st.markdown("""
                <div style="background: linear-gradient(135deg, #f7fafc, #edf2f7); padding: 1.5rem; border-radius: 15px; margin: 1rem 0;">
                    <h4 style="color: #2d3748; margin-bottom: 1rem;">🔑 Credenciais de Teste</h4>
                    <div style="display: grid; gap: 1rem;">
                        <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 4px solid #667eea;">
                            <strong>👨‍💼 Administrador:</strong> <code>admin</code> / <code>admin123</code>
                        </div>
                        <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 4px solid #48bb78;">
                            <strong>👩‍⚕️ Nutricionista:</strong> <code>nutricionista</code> / <code>nutri123</code>
                        </div>
                        <div style="background: white; padding: 1rem; border-radius: 10px; border-left: 4px solid #ed8936;">
                            <strong>🎯 Demo:</strong> <code>demo</code> / <code>demo123</code>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                **✨ Recursos Disponíveis:**
                
                🧮 **Calculadoras Inteligentes** - TMB, IMC, composição corporal com visualizações
                
                📊 **Dashboard Interativo** - Métricas em tempo real com gráficos animados
                
                👥 **Gestão Avançada** - Pacientes com histórico completo e analytics
                
                🍽️ **IA Nutricional** - Criação automática de planos alimentares
                
                📱 **Comunicação** - WhatsApp e email integrados
                
                📈 **Relatórios Pro** - PDFs personalizados com gráficos interativos
                """)
    
    def sidebar_menu(self):
        """Menu lateral melhorado"""
        with st.sidebar:
            st.markdown(f'''
            <div class="sidebar-logo">
                <h2>🥗 NutriStock360</h2>
                <p>Pro Dashboard</p>
                <small>v2.0 Premium</small>
            </div>
            ''', unsafe_allow_html=True)
            
            # Informações do usuário
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; text-align: center;">
                <div style="color: #667eea; font-weight: 600;">👤 {st.session_state.current_user}</div>
                <div style="color: #718096; font-size: 0.9rem;">📅 {datetime.now().strftime('%d/%m/%Y')}</div>
                <div style="color: #718096; font-size: 0.9rem;">🕐 {datetime.now().strftime('%H:%M')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Busca global no sidebar
            busca_termo = st.text_input("🔍 Busca Rápida", placeholder="Buscar...", key="busca_sidebar")
            
            if busca_termo:
                resultados = self.busca_global(busca_termo)
                total = sum(len(r) for r in resultados.values())
                
                if total > 0:
                    st.success(f"✅ {total} resultados encontrados")
                    for categoria, items in resultados.items():
                        if items:
                            st.write(f"**{categoria.title()}:** {len(items)}")
                else:
                    st.info("Nenhum resultado encontrado")
            
            # Menu principal
            menu_options = [
                "📊 Dashboard Interativo",
                "🧮 Calculadoras Inteligentes", 
                "👥 Gestão de Pacientes",
                "🍽️ Planos Alimentares",
                "🍳 Banco de Receitas",
                "📅 Agendamentos",
                "📈 Relatórios Avançados",
                "💬 Comunicação",
                "⚙️ Configurações"
            ]
            
            selected = st.selectbox("🧭 Navegação Principal", menu_options, key="main_menu")
            
            # Estatísticas em tempo real
            st.markdown("---")
            st.markdown("**📊 Métricas em Tempo Real**")
            
            # Criar métricas com animação
            total_pacientes = len(st.session_state.pacientes)
            consultas_hoje = len([a for a in st.session_state.agendamentos if a.get('data') == datetime.now().strftime('%Y-%m-%d')])
            receitas_total = len(st.session_state.receitas)
            
            # Métricas com cores e ícones
            metrics_data = [
                ("👥", "Pacientes", total_pacientes, "#667eea"),
                ("📅", "Hoje", consultas_hoje, "#48bb78"),
                ("🍳", "Receitas", receitas_total, "#ed8936")
            ]
            
            for icon, label, value, color in metrics_data:
                st.markdown(f"""
                <div style="background: {color}15; padding: 0.8rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid {color};">
                    <div style="color: {color}; font-size: 1.2rem;">{icon} {label}</div>
                    <div style="color: {color}; font-size: 1.5rem; font-weight: 700;">{value}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Ações rápidas
            st.markdown("---")
            st.markdown("**⚡ Ações Rápidas**")
            
            quick_actions = st.columns(1)
            
            if st.button("➕ Novo Paciente", use_container_width=True, key="quick_patient"):
                st.session_state.quick_action = "novo_paciente"
                st.rerun()
            
            if st.button("📅 Agendar", use_container_width=True, key="quick_schedule"):
                st.session_state.quick_action = "agendar"
                st.rerun()
            
            if st.button("🧮 Calcular", use_container_width=True, key="quick_calc"):
                st.session_state.quick_action = "calcular"
                st.rerun()
            
            # Status do sistema
            st.markdown("---")
            st.markdown("**🔧 Status do Sistema**")
            
            st.markdown(f"""
            <div style="background: #48bb7815; padding: 1rem; border-radius: 10px; border-left: 4px solid #48bb78;">
                <div style="color: #48bb78; font-weight: 600;">✅ Sistema Online</div>
                <div style="color: #718096; font-size: 0.9rem;">Todos os módulos funcionando</div>
                <div style="color: #718096; font-size: 0.9rem;">Última sincronização: agora</div>
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
        """Dashboard principal com interatividade avançada"""
        st.markdown('<div class="main-header"><h1>📊 Dashboard Executivo Interativo</h1><p>Visão 360° da sua prática nutricional</p></div>', unsafe_allow_html=True)
        
        # Métricas principais com animação
        st.markdown("### 📈 Métricas Principais")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_pacientes = len(st.session_state.pacientes)
        consultas_hoje = len([a for a in st.session_state.agendamentos if a.get('data') == datetime.now().strftime('%Y-%m-%d')])
        receita_mensal = total_pacientes * st.session_state.configuracoes.get('valor_consulta', 150)
        satisfacao = 4.8  # Simulado
        
        metrics = [
            ("👥 Pacientes Ativos", total_pacientes, "+3", "#667eea"),
            ("📅 Consultas Hoje", consultas_hoje, "+2", "#48bb78"), 
            ("💰 Receita Mensal", f"R$ {receita_mensal:,.2f}", "+15%", "#ed8936"),
            ("⭐ Satisfação", f"{satisfacao}/5.0", "+0.2", "#9f7aea")
        ]
        
        for i, (col, (label, value, delta, color)) in enumerate(zip([col1, col2, col3, col4], metrics)):
            with col:
                st.markdown(f'''
                <div class="metric-card" style="animation-delay: {i*0.1}s;">
                    <div class="metric-container">
                        <div class="metric-value" style="color: {color};">{value}</div>
                        <div class="metric-label">{label}</div>
                        <div style="color: #48bb78; font-size: 0.9rem; margin-top: 0.5rem;">📈 {delta}</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
        
        # Gráficos interativos melhorados
        st.markdown("### 📊 Analytics Visuais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📈 Evolução de Pacientes")
            
            # Dados com crescimento realista
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            base_patients = [10, 15, 18, 25, 32, 38, 45, 52, 58, 65, 72, max(total_pacientes, 78)]
            
            patients_data = pd.DataFrame({'Mês': meses, 'Pacientes': base_patients})
            
            fig = create_interactive_chart(patients_data, "line", "Crescimento de Pacientes 2024", 'Mês', 'Pacientes')
            fig.update_traces(
                line=dict(color='#667eea', width=4),
                marker=dict(color='#f093fb', size=10),
                fill='tonexty',
                fillcolor='rgba(102, 126, 234, 0.1)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🎯 Performance das Metas")
            
            categories = ['Novos Pacientes', 'Consultas', 'Receitas', 'Receita', 'Satisfação']
            values = [85, 92, 78, 95, 88]
            
            performance_data = pd.DataFrame({'Categoria': categories, 'Progresso': values})
            
            fig = create_interactive_chart(performance_data, "bar", "Progresso das Metas (%)", 'Categoria', 'Progresso')
            fig.update_traces(
                marker_color=['#667eea', '#48bb78', '#ed8936', '#f093fb', '#9f7aea'],
                textposition='auto',
                texttemplate='%{y}%'
            )
            
            # Adicionar linha de meta
            fig.add_hline(y=90, line_dash="dash", line_color="red", annotation_text="Meta: 90%")
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Seção de atividades e compromissos
        st.markdown("### 🕐 Painel de Atividades")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🔄 Atividades Recentes")
            
            activities = [
                {"time": "14:30", "activity": "Consulta concluída - Maria Silva", "type": "success", "icon": "✅"},
                {"time": "13:15", "activity": "Novo paciente: João Santos", "type": "info", "icon": "👤"},
                {"time": "11:45", "activity": "Plano alimentar enviado - Ana Costa", "type": "success", "icon": "🍽️"},
                {"time": "10:30", "activity": "Receita adicionada: Salada Proteica", "type": "info", "icon": "🍳"},
                {"time": "09:15", "activity": "Backup automático realizado", "type": "success", "icon": "💾"}
            ]
            
            for activity in activities:
                color = {"success": "#48bb78", "info": "#3182ce", "warning": "#ed8936"}[activity["type"]]
                st.markdown(f"""
                <div style="
                    background: {color}15; 
                    padding: 1rem; 
                    border-radius: 10px; 
                    margin: 0.5rem 0; 
                    border-left: 4px solid {color};
                    transition: all 0.3s ease;
                " onmouseover="this.style.transform='translateX(5px)'" onmouseout="this.style.transform='translateX(0)'">
                    <div style="color: {color}; font-weight: 600;">
                        {activity["icon"]} {activity["time"]} - {activity["activity"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📅 Próximos Compromissos")
            
            if st.session_state.agendamentos:
                hoje = datetime.now().strftime('%Y-%m-%d')
                agendamentos_hoje = [a for a in st.session_state.agendamentos if a.get('data') == hoje]
                
                if agendamentos_hoje:
                    for apt in agendamentos_hoje:
                        tipo_colors = {
                            "Consulta Inicial": "#667eea",
                            "Retorno": "#48bb78", 
                            "Avaliação": "#ed8936",
                            "Online": "#9f7aea",
                            "Urgência": "#e53e3e"
                        }
                        color = tipo_colors.get(apt['tipo'], "#718096")
                        
                        st.markdown(f"""
                        <div class="appointment-card" style="background: linear-gradient(135deg, {color}, {color}dd);">
                            🕐 <strong>{apt['horario']}</strong> - {apt['paciente']}<br>
                            📋 {apt['tipo']}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="text-align: center; padding: 2rem; color: #718096;">
                        📅 Nenhum agendamento para hoje<br>
                        <small>Que tal relaxar ou planejar amanhã?</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; color: #718096;">
                    📝 Nenhum agendamento cadastrado<br>
                    <small>Comece adicionando seus compromissos!</small>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Painel de insights rápidos
        st.markdown("### 💡 Insights Inteligentes")
        
        insights = []
        
        if total_pacientes > 0:
            if st.session_state.pacientes:
                imc_medio = sum([p['imc'] for p in st.session_state.pacientes]) / len(st.session_state.pacientes)
                if imc_medio > 25:
                    insights.append(("⚠️", f"IMC médio dos pacientes: {imc_medio:.1f} - Oportunidade para foco em emagrecimento", "warning"))
                else:
                    insights.append(("✅", f"IMC médio dos pacientes: {imc_medio:.1f} - Pacientes em boa forma!", "success"))
        
        if consultas_hoje == 0:
            insights.append(("📅", "Nenhuma consulta hoje - Ótimo momento para planejamento e estudos", "info"))
        elif consultas_hoje > 5:
            insights.append(("🔥", f"{consultas_hoje} consultas hoje - Dia intenso! Lembre-se de fazer pausas", "warning"))
        
        if receita_mensal > 10000:
            insights.append(("💰", f"Receita mensal projetada: R$ {receita_mensal:,.2f} - Excelente performance!", "success"))
        
        if len(st.session_state.receitas) < 5:
            insights.append(("🍳", "Poucas receitas cadastradas - Que tal adicionar mais opções para seus pacientes?", "info"))
        
        # Exibir insights em cards coloridos
        if insights:
            for insight in insights:
                icon, texto, tipo = insight
                colors = {
                    "success": ("#48bb78", "#48bb7815"),
                    "warning": ("#ed8936", "#ed893615"), 
                    "info": ("#3182ce", "#3182ce15")
                }
                color, bg_color = colors[tipo]
                
                st.markdown(f"""
                <div style="
                    background: {bg_color}; 
                    padding: 1.2rem; 
                    border-radius: 15px; 
                    margin: 0.8rem 0; 
                    border-left: 5px solid {color};
                    transition: all 0.3s ease;
                ">
                    <div style="color: {color}; font-weight: 600; font-size: 1.1rem;">
                        {icon} {texto}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    def calculadoras_page(self):
        """Calculadoras com interface melhorada e interatividade"""
        st.markdown('<div class="main-header"><h1>🧮 Calculadoras Nutricionais Interativas</h1><p>Ferramentas profissionais com resultados em tempo real</p></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["🏋️ Básicas", "🔥 Metabólicas", "📊 Composição Corporal", "🎯 Objetivos"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📏 Calculadora de IMC Interativa")
                
                # Inputs com feedback em tempo real
                peso = st.slider("⚖️ Peso (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
                altura = st.slider("📏 Altura (m)", min_value=1.0, max_value=2.2, value=1.70, step=0.01)
                
                # Cálculo automático em tempo real
                imc = peso / (altura ** 2)
                
                # Classificação com cores
                if imc < 18.5:
                    status = "Abaixo do peso"
                    color_class = "status-warning"
                    cor_imc = "#ed8936"
                    recomendacao = "Considere um plano para ganho de peso saudável"
                elif 18.5 <= imc < 25:
                    status = "Peso normal"
                    color_class = "status-normal"
                    cor_imc = "#48bb78"
                    recomendacao = "Mantenha o peso atual com alimentação equilibrada"
                elif 25 <= imc < 30:
                    status = "Sobrepeso"
                    color_class = "status-warning"
                    cor_imc = "#ed8936"
                    recomendacao = "Plano de emagrecimento gradual recomendado"
                else:
                    status = "Obesidade"
                    color_class = "status-danger"
                    cor_imc = "#e53e3e"
                    recomendacao = "Intervenção nutricional urgente necessária"
                
                # Mostrar resultado com animação
                st.markdown(f'''
                <div style="
                    background: linear-gradient(135deg, {cor_imc}15, {cor_imc}25);
                    padding: 1.5rem;
                    border-radius: 15px;
                    margin: 1rem 0;
                    text-align: center;
                    border: 2px solid {cor_imc};
                    animation: pulse 0.6s ease-in-out;
                ">
                    <div style="color: {cor_imc}; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">
                        {imc:.1f}
                    </div>
                    <div style="color: {cor_imc}; font-weight: 600; font-size: 1.2rem;">
                        {status}
                    </div>
                    <div style="color: #718096; margin-top: 1rem; font-size: 0.9rem;">
                        💡 {recomendacao}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                
                # Gráfico visual do IMC
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = imc,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "IMC"},
                    delta = {'reference': 22.5},
                    gauge = {
                        'axis': {'range': [None, 40]},
                        'bar': {'color': cor_imc},
                        'steps': [
                            {'range': [0, 18.5], 'color': "#fbb6ce"},
                            {'range': [18.5, 25], 'color': "#9ae6b4"},
                            {'range': [25, 30], 'color': "#faf089"},
                            {'range': [30, 40], 'color': "#feb2b2"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 30
                        }
                    }
                ))
                
                fig.update_layout(height=300, font={'size': 14})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("⚖️ Peso Ideal Inteligente")
                
                altura_ideal = st.slider("📏 Altura (m)", min_value=1.0, max_value=2.2, value=1.70, step=0.01, key="altura_ideal")
                sexo = st.radio("👤 Sexo", ["Masculino", "Feminino"], horizontal=True)
                
                # Múltiplas fórmulas
                formulas_peso = {}
                
                # Fórmula de Robinson
                if sexo == "Masculino":
                    robinson = 52 + (1.9 * ((altura_ideal * 100) - 152.4))
                else:
                    robinson = 49 + (1.7 * ((altura_ideal * 100) - 152.4))
                
                # Fórmula de Devine
                if sexo == "Masculino":
                    devine = 50 + (2.3 * ((altura_ideal * 100 / 2.54) - 60))
                else:
                    devine = 45.5 + (2.3 * ((altura_ideal * 100 / 2.54) - 60))
                
                # Faixa de peso saudável (IMC)
                peso_min = 18.5 * (altura_ideal ** 2)
                peso_max = 24.9 * (altura_ideal ** 2)
                
                formulas_peso = {
                    "Robinson": robinson,
                    "Devine": devine,
                    "Faixa Saudável (min)": peso_min,
                    "Faixa Saudável (max)": peso_max
                }
                
                # Exibir resultados em cards
                st.markdown("**🎯 Resultados por Diferentes Métodos:**")
                
                for i, (metodo, peso_calc) in enumerate(formulas_peso.items()):
                    cor = ["#667eea", "#48bb78", "#ed8936", "#9f7aea"][i % 4]
                    st.markdown(f'''
                    <div style="
                        background: {cor}15;
                        padding: 1rem;
                        border-radius: 10px;
                        margin: 0.5rem 0;
                        border-left: 4px solid {cor};
                        animation: slideInFromLeft {0.2 + i*0.1}s ease-out;
                    ">
                        <div style="color: {cor}; font-weight: 600;">{metodo}</div>
                        <div style="color: {cor}; font-size: 1.3rem; font-weight: 700;">{peso_calc:.1f} kg</div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Gráfico comparativo
                metodos = list(formulas_peso.keys())
                pesos = list(formulas_peso.values())
                
                fig = px.bar(
                    x=metodos, 
                    y=pesos,
                    title="Comparação de Métodos",
                    color=pesos,
                    color_continuous_scale="viridis"
                )
                fig.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🔥 Calculadora Metabólica Completa")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📋 Dados Básicos**")
                peso_tmb = st.number_input("⚖️ Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1, key="peso_tmb")
                altura_tmb = st.number_input("📏 Altura (cm)", min_value=100, max_value=250, value=170, key="altura_tmb")
                idade = st.number_input("🎂 Idade (anos)", min_value=10, max_value=100, value=30)
                sexo_tmb = st.selectbox("👤 Sexo", ["Masculino", "Feminino"], key="sexo_tmb")
            
            with col2:
                st.markdown("**🎯 Estilo de Vida**")
                atividade = st.selectbox("🏃 Nível de Atividade", [
                    "Sedentário (pouco ou nenhum exercício)",
                    "Levemente ativo (exercício leve 1-3 dias/semana)",
                    "Moderadamente ativo (exercício moderado 3-5 dias/semana)",
                    "Muito ativo (exercício pesado 6-7 dias/semana)",
                    "Extremamente ativo (exercício muito pesado, trabalho físico)"
                ])
                
                objetivo = st.selectbox("🎯 Objetivo", [
                    "Manter peso",
                    "Perder 0.5 kg/semana",
                    "Perder 1 kg/semana", 
                    "Ganhar 0.5 kg/semana",
                    "Ganhar 1 kg/semana"
                ])
            
            # Cálculos automáticos em tempo real
            # TMB (Mifflin-St Jeor)
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
            
            # Resultados principais
            st.markdown("**🔥 Resultados Metabólicos**")
            
            resultados = [
                ("Taxa Metabólica Basal", f"{tmb:.0f} kcal/dia", "#667eea", "Energia para funções vitais"),
                ("Gasto Energético Total", f"{get:.0f} kcal/dia", "#48bb78", "Energia total gasta por dia"),
                ("Calorias para Objetivo", f"{calorias_objetivo:.0f} kcal/dia", "#f093fb", f"Para {objetivo.lower()}")
            ]
            
            for label, valor, cor, desc in resultados:
                st.markdown(f'''
                <div style="
                    background: linear-gradient(135deg, {cor}15, {cor}25);
                    padding: 1.5rem;
                    border-radius: 15px;
                    margin: 1rem 0;
                    text-align: center;
                    border: 2px solid {cor};
                ">
                    <div style="color: {cor}; font-size: 1.8rem; font-weight: 700;">
                        {valor}
                    </div>
                    <div style="color: {cor}; font-weight: 600; margin-bottom: 0.5rem;">
                        {label}
                    </div>
                    <div style="color: #718096; font-size: 0.9rem;">
                        {desc}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Distribuição de macronutrientes
            st.markdown("**📊 Distribuição de Macronutrientes**")
            
            proteinas_g = peso_tmb * 1.6
            proteinas_cal = proteinas_g * 4
            gorduras_cal = calorias_objetivo * 0.25
            gorduras_g = gorduras_cal / 9
            carboidratos_cal = calorias_objetivo - proteinas_cal - gorduras_cal
            carboidratos_g = carboidratos_cal / 4
            
            # Gráfico de pizza interativo
            macros_data = pd.DataFrame({
                'Macronutriente': ['Proteínas', 'Carboidratos', 'Gorduras'],
                'Gramas': [proteinas_g, carboidratos_g, gorduras_g],
                'Calorias': [proteinas_cal, carboidratos_cal, gorduras_cal],
                'Percentual': [
                    (proteinas_cal/calorias_objetivo*100),
                    (carboidratos_cal/calorias_objetivo*100),
                    (gorduras_cal/calorias_objetivo*100)
                ]
            })
            
            fig = px.pie(
                macros_data, 
                names='Macronutriente', 
                values='Calorias',
                title="Distribuição Calórica dos Macronutrientes",
                color_discrete_map={
                    'Proteínas': '#e53e3e',
                    'Carboidratos': '#3182ce', 
                    'Gorduras': '#ed8936'
                }
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela detalhada de macros
            col1, col2, col3 = st.columns(3)
            
            macros_details = [
                ("🥩 Proteínas", proteinas_g, proteinas_cal, "#e53e3e"),
                ("🍞 Carboidratos", carboidratos_g, carboidratos_cal, "#3182ce"),
                ("🥑 Gorduras", gorduras_g, gorduras_cal, "#ed8936")
            ]
            
            for i, (col, (nome, gramas, cals, cor)) in enumerate(zip([col1, col2, col3], macros_details)):
                with col:
                    percent = (cals/calorias_objetivo*100)
                    st.markdown(f'''
                    <div style="
                        background: {cor}15;
                        padding: 1.5rem;
                        border-radius: 15px;
                        text-align: center;
                        border: 2px solid {cor};
                        animation: fadeIn {0.3 + i*0.2}s ease-out;
                    ">
                        <div style="color: {cor}; font-size: 1.5rem; margin-bottom: 0.5rem;">
                            {nome}
                        </div>
                        <div style="color: {cor}; font-size: 1.3rem; font-weight: 700;">
                            {gramas:.0f}g
                        </div>
                        <div style="color: {cor}; font-size: 1rem;">
                            {cals:.0f} kcal
                        </div>
                        <div style="color: #718096; font-size: 0.9rem; margin-top: 0.5rem;">
                            {percent:.0f}% das calorias
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("📊 Análise de Composição Corporal")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📏 Medidas Corporais**")
                peso_comp = st.slider("⚖️ Peso atual (kg)", min_value=30.0, max_value=200.0, value=70.0, key="peso_comp")
                altura_comp = st.slider("📏 Altura (cm)", min_value=100, max_value=220, value=170, key="altura_comp")
                cintura = st.slider("📐 Circunferência da cintura (cm)", min_value=50, max_value=150, value=80)
                quadril = st.slider("📐 Circunferência do quadril (cm)", min_value=60, max_value=200, value=95)
                pescoco = st.slider("📐 Circunferência do pescoço (cm)", min_value=20, max_value=60, value=35)
                
            with col2:
                st.markdown("**👤 Informações Pessoais**")
                sexo_comp = st.radio("Sexo", ["Masculino", "Feminino"], key="sexo_comp", horizontal=True)
                idade_comp = st.slider("🎂 Idade (anos)", min_value=10, max_value=100, value=30, key="idade_comp")
                atividade_comp = st.selectbox("🏃 Nível de atividade física", [
                    "Sedentário", "Levemente ativo", "Moderadamente ativo", "Muito ativo"
                ])
            
            # Cálculos automáticos
            # Percentual de gordura (Fórmula do US Navy)
            if sexo_comp == "Masculino":
                bf_percent = 495 / (1.0324 - 0.19077 * math.log10(cintura - pescoco) + 0.15456 * math.log10(altura_comp)) - 450
            else:
                bf_percent = 495 / (1.29579 - 0.35004 * math.log10(cintura + quadril - pescoco) + 0.22100 * math.log10(altura_comp)) - 450
            
            # Relação cintura-quadril
            rcq = cintura / quadril
            
            # Classificações detalhadas
            if sexo_comp == "Masculino":
                if bf_percent < 6:
                    bf_status = "Muito baixo"
                    bf_color = "#e53e3e"
                elif bf_percent < 14:
                    bf_status = "Atlético"
                    bf_color = "#48bb78"
                elif bf_percent < 18:
                    bf_status = "Fitness"
                    bf_color = "#48bb78"
                elif bf_percent < 25:
                    bf_status = "Média"
                    bf_color = "#ed8936"
                else:
                    bf_status = "Acima da média"
                    bf_color = "#e53e3e"
                
                rcq_ideal = rcq < 0.9
            else:
                if bf_percent < 16:
                    bf_status = "Muito baixo"
                    bf_color = "#e53e3e"
                elif bf_percent < 20:
                    bf_status = "Atlético"
                    bf_color = "#48bb78"
                elif bf_percent < 25:
                    bf_status = "Fitness"
                    bf_color = "#48bb78"
                elif bf_percent < 32:
                    bf_status = "Média"
                    bf_color = "#ed8936"
                else:
                    bf_status = "Acima da média"
                    bf_color = "#e53e3e"
                
                rcq_ideal = rcq < 0.8
            
            # Massa magra e gorda
            massa_gorda = peso_comp * (bf_percent / 100)
            massa_magra = peso_comp - massa_gorda
            
            # Resultados visuais
            st.markdown("**🎯 Resultados da Análise Corporal**")
            
            # Gráfico de gauge para percentual de gordura
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = bf_percent,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "% Gordura Corporal"},
                gauge = {
                    'axis': {'range': [None, 50]},
                    'bar': {'color': bf_color},
                    'steps': [
                        {'range': [0, 15], 'color': "#c6f6d5"},
                        {'range': [15, 25], 'color': "#faf089"},
                        {'range': [25, 35], 'color': "#fbb6ce"},
                        {'range': [35, 50], 'color': "#fed7d7"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 30
                    }
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Cards de resultados
            resultados_comp = [
                ("Percentual de Gordura", f"{bf_percent:.1f}%", bf_status, bf_color),
                ("Massa Magra", f"{massa_magra:.1f} kg", "Músculos + Ossos + Órgãos", "#48bb78"),
                ("Massa Gorda", f"{massa_gorda:.1f} kg", "Gordura Total", "#ed8936"),
                ("RCQ", f"{rcq:.2f}", "Ideal" if rcq_ideal else "Atenção", "#48bb78" if rcq_ideal else "#ed8936")
            ]
            
            col1, col2, col3, col4 = st.columns(4)
            cols = [col1, col2, col3, col4]
            
            for i, (col, (label, valor, desc, cor)) in enumerate(zip(cols, resultados_comp)):
                with col:
                    st.markdown(f'''
                    <div style="
                        background: {cor}15;
                        padding: 1.5rem;
                        border-radius: 15px;
                        text-align: center;
                        border: 2px solid {cor};
                        animation: fadeIn {0.3 + i*0.1}s ease-out;
                    ">
                        <div style="color: {cor}; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.5rem;">
                            {valor}
                        </div>
                        <div style="color: {cor}; font-weight: 600;">
                            {label}
                        </div>
                        <div style="color: #718096; font-size: 0.8rem; margin-top: 0.5rem;">
                            {desc}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
            
            # Gráfico de composição corporal
            composicao_data = pd.DataFrame({
                'Componente': ['Massa Magra', 'Massa Gorda'],
                'Peso (kg)': [massa_magra, massa_gorda],
                'Percentual': [100-bf_percent, bf_percent]
            })
            
            fig = px.pie(
                composicao_data, 
                names='Componente', 
                values='Peso (kg)',
                title="Composição Corporal",
                color_discrete_map={'Massa Magra': '#48bb78', 'Massa Gorda': '#ed8936'}
            )
            fig.update_traces(textposition='inside', textinfo='percent+label+value')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab4:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            st.subheader("🎯 Planejamento de Objetivos Inteligente")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Situação Atual**")
                peso_atual = st.slider("⚖️ Peso atual (kg)", min_value=30.0, max_value=200.0, value=80.0)
                bf_atual = st.slider("📊 % Gordura atual", min_value=5.0, max_value=50.0, value=25.0)
                
                st.markdown("**🎯 Objetivo Desejado**")
                peso_meta = st.slider("🎯 Peso meta (kg)", min_value=30.0, max_value=200.0, value=70.0)
                bf_meta = st.slider("🎯 % Gordura meta", min_value=5.0, max_value=50.0, value=18.0)
                
            with col2:
                st.markdown("**⚙️ Parâmetros do Plano**")
                velocidade = st.selectbox("🚀 Velocidade de perda/ganho", [
                    "Conservadora (0.25 kg/semana)",
                    "Moderada (0.5 kg/semana)",
                    "Acelerada (0.75 kg/semana)",
                    "Agressiva (1 kg/semana)"
                ])
                
                prioridade = st.selectbox("🎯 Prioridade Principal", [
                    "Manter massa muscular",
                    "Perda de gordura máxima",
                    "Ganho de massa muscular",
                    "Recomposição corporal"
                ])
                
                intensidade_treino = st.selectbox("🏋️ Intensidade do Treino", [
                    "Baixa (2-3x/semana)",
                    "Moderada (4-5x/semana)", 
                    "Alta (6-7x/semana)"
                ])
            
            # Cálculos automáticos do plano
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
            
            # Análise de composição corporal
            massa_gorda_atual = peso_atual * (bf_atual / 100)
            massa_magra_atual = peso_atual - massa_gorda_atual
            
            massa_gorda_meta = peso_meta * (bf_meta / 100)
            massa_magra_meta = peso_meta - massa_gorda_meta
            
            diferenca_gordura = massa_gorda_atual - massa_gorda_meta
            diferenca_magra = massa_magra_meta - massa_magra_atual
            
            # Resultados do planejamento
            st.markdown("**📅 Cronograma do Objetivo**")
            
            timeline_info = [
                ("⏰ Tempo Estimado", f"{semanas_necessarias:.0f} semanas", "#667eea"),
                ("📅 Data Prevista", data_meta.strftime("%d/%m/%Y"), "#48bb78"),
                ("📉 Perda de Peso", f"{diferenca_peso:.1f} kg", "#ed8936"),
                ("🔥 Gordura a Perder", f"{diferenca_gordura:.1f} kg", "#e53e3e" if diferenca_gordura > 0 else "#48bb78")
            ]
            
            for label, valor, cor in timeline_info:
                st.markdown(f'''
                <div style="
                    background: {cor}15;
                    padding: 1rem;
                    border-radius: 10px;
                    margin: 0.5rem 0;
                    border-left: 4px solid {cor};
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <div style="color: {cor}; font-weight: 600;">{label}</div>
                    <div style="color: {cor}; font-size: 1.2rem; font-weight: 700;">{valor}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Gráfico de progresso projetado
            semanas_range = list(range(0, int(semanas_necessarias) + 1, 2))
            pesos_projetados = []
            
            for semana in semanas_range:
                if peso_atual > peso_meta:
                    peso_proj = peso_atual - (kg_por_semana * semana)
                    peso_proj = max(peso_proj, peso_meta)
                else:
                    peso_proj = peso_atual + (kg_por_semana * semana)
                    peso_proj = min(peso_proj, peso_meta)
                pesos_projetados.append(peso_proj)
            
            progresso_data = pd.DataFrame({
                'Semana': semanas_range,
                'Peso Projetado': pesos_projetados
            })
            
            fig = px.line(
                progresso_data, 
                x='Semana', 
                y='Peso Projetado',
                title="Projeção de Progresso",
                markers=True
            )
            
            fig.add_hline(y=peso_meta, line_dash="dash", line_color="green", annotation_text="Meta")
            fig.add_hline(y=peso_atual, line_dash="dash", line_color="blue", annotation_text="Atual")
            
            fig.update_traces(
                line=dict(color='#667eea', width=3),
                marker=dict(color='#f093fb', size=8)
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Recomendações personalizadas
            st.markdown("**💡 Recomendações Personalizadas**")
            
            recomendacoes = []
            
            if prioridade == "Manter massa muscular":
                recomendacoes.append(("🏋️", "Treino de força 3-4x/semana com cargas progressivas", "#667eea"))
                recomendacoes.append(("🥩", "Ingestão proteica: 2-2.5g/kg de peso corporal", "#e53e3e"))
                recomendacoes.append(("⚖️", "Déficit calórico moderado: 300-500 kcal/dia", "#ed8936"))
            
            elif prioridade == "Perda de gordura máxima":
                recomendacoes.append(("🔥", "Cardio 5-6x/semana + treino de força 2-3x", "#e53e3e"))
                recomendacoes.append(("📉", "Déficit calórico agressivo: 500-750 kcal/dia", "#ed8936"))
                recomendacoes.append(("🥗", "Dieta rica em proteínas e fibras", "#48bb78"))
            
            elif prioridade == "Ganho de massa muscular":
                recomendacoes.append(("💪", "Treino de hipertrofia 4-5x/semana", "#667eea"))
                recomendacoes.append(("📈", "Superávit calórico: 300-500 kcal/dia", "#48bb78"))
                recomendacoes.append(("🥛", "Proteína: 2g/kg + carboidratos pós-treino", "#3182ce"))
            
            else:  # Recomposição corporal
                recomendacoes.append(("⚖️", "Treino intenso + nutrição precisa", "#9f7aea"))
                recomendacoes.append(("🎯", "Calorias de manutenção + ciclagem de carbos", "#ed8936"))
                recomendacoes.append(("🔄", "Paciência: processo mais lento mas eficaz", "#48bb78"))
            
            # Adicionar recomendações baseadas na intensidade
            if intensidade_treino == "Alta (6-7x/semana)":
                recomendacoes.append(("⚠️", "Atenção ao descanso: 7-9h de sono obrigatório", "#ed8936"))
                recomendacoes.append(("🧘", "Inclua 1-2 dias de recuperação ativa", "#9f7aea"))
            
            for icon, texto, cor in recomendacoes:
                st.markdown(f'''
                <div style="
                    background: {cor}15;
                    padding: 1.2rem;
                    border-radius: 15px;
                    margin: 0.8rem 0;
                    border-left: 5px solid {cor};
                    animation: slideInFromLeft 0.5s ease-out;
                ">
                    <div style="color: {cor}; font-weight: 600; font-size: 1.1rem;">
                        {icon} {texto}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            # Fases do plano
            st.markdown("**📊 Fases do Plano**")
            
            fases = []
            semanas_por_fase = semanas_necessarias / 3
            
            if diferenca_peso > 0:  # Perda de peso
                fases = [
                    ("Fase 1: Adaptação", f"Semanas 1-{semanas_por_fase:.0f}", "Ajuste inicial, déficit moderado", "#3182ce"),
                    ("Fase 2: Aceleração", f"Semanas {semanas_por_fase:.0f}-{semanas_por_fase*2:.0f}", "Máximo déficit, treinos intensos", "#e53e3e"),
                    ("Fase 3: Finalização", f"Semanas {semanas_por_fase*2:.0f}-{semanas_necessarias:.0f}", "Manutenção, preservar resultados", "#48bb78")
                ]
            else:  # Ganho de peso
                fases = [
                    ("Fase 1: Construção", f"Semanas 1-{semanas_por_fase:.0f}", "Superávit inicial, ganhos lineares", "#48bb78"),
                    ("Fase 2: Intensificação", f"Semanas {semanas_por_fase:.0f}-{semanas_por_fase*2:.0f}", "Treinos pesados, máximo superávit", "#667eea"),
                    ("Fase 3: Refinamento", f"Semanas {semanas_por_fase*2:.0f}-{semanas_necessarias:.0f}", "Definição, manter ganhos", "#9f7aea")
                ]
            
            for i, (fase, periodo, desc, cor) in enumerate(fases):
                st.markdown(f'''
                <div style="
                    background: {cor}15;
                    padding: 1.5rem;
                    border-radius: 15px;
                    margin: 1rem 0;
                    border: 2px solid {cor};
                    animation: fadeIn {0.5 + i*0.2}s ease-out;
                ">
                    <div style="color: {cor}; font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem;">
                        {fase}
                    </div>
                    <div style="color: {cor}; font-weight: 600;">
                        📅 {periodo}
                    </div>
                    <div style="color: #718096; margin-top: 0.5rem;">
                        {desc}
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    def pacientes_page(self):
        """Gestão de pacientes com interface aprimorada"""
        st.markdown('<div class="main-header"><h1>👥 Gestão Inteligente de Pacientes</h1><p>Acompanhamento completo e personalizado</p></div>', unsafe_allow_html=True)
        
        # Verificar ações rápidas
        if st.session_state.get('quick_action') == 'novo_paciente':
            st.session_state.quick_action = None
            # Focar na aba de novo paciente automaticamente
        
        tab1, tab2, tab3 = st.tabs(["📋 Lista Interativa", "➕ Cadastro Rápido", "📊 Analytics Avançados"])
        
        with tab1:
            st.markdown('<div class="tab-content">', unsafe_allow_html=True)
            
            # Filtros avançados com interface melhorada
            st.markdown("**🔍 Filtros Inteligentes**")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                filtro_nome = st.text_input("🔍 Nome do paciente", placeholder="Digite para buscar...")
            with col2:
                filtro_objetivo = st.selectbox("🎯 Objetivo", ["Todos", "Emagrecimento", "Ganho de massa", "Manutenção", "Definição"])
            with col3:
                filtro_imc = st.selectbox("📊 Faixa de IMC", ["Todos", "Abaixo do peso", "Normal", "Sobrepeso", "Obesidade"])
            with col4:
                ordenar = st.selectbox("📑 Ordenar por", ["Nome A-Z", "Nome Z-A", "IMC Crescente", "IMC Decrescente", "Cadastro Recente"])
            
            # Aplicar filtros
            pacientes_filtrados = st.session_state.pacientes.copy()
            
            if filtro_nome:
                pacientes_filtrados = [p for p in pacientes_filtrados if filtro_nome.lower() in p['nome'].lower()]
            
            if filtro_objetivo != "Todos":
                pacientes_filtrados = [p for p in pacientes_filtrados if p['objetivo'] == filtro_objetivo]
            
            if filtro_imc != "Todos":
                pacientes_filtrados = [p for p in pacientes_filtrados if self.classificar_imc(p['imc']) == filtro_imc]
            
            # Ordenação
            if ordenar == "Nome A-Z":
                pacientes_filtrados.sort(key=lambda x: x['nome'])
            elif ordenar == "Nome Z-A":
                pacientes_filtrados.sort(key=lambda x: x['nome'], reverse=True)
            elif ordenar == "IMC Crescente":
                pacientes_filtrados.sort(key=lambda x: x['imc'])
            elif ordenar == "IMC Decrescente":
                pacientes_filtrados.sort(key=lambda x: x['imc'], reverse=True)
            
            # Estatísticas dos filtros
