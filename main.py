def show_active_meal_plans(user):
    st.markdown('<div class="sub-header">📋 Planos Alimentares Ativos</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT pa.*, p.nome as paciente_nome
    FROM planos_alimentares pa
    JOIN pacientes p ON pa.paciente_id = p.id
    WHERE pa.nutricionista_id = ? AND pa.ativo = 1
    ORDER BY pa.data_criacao DESC
    """, (user['id'],))
    
    planos_ativos = cursor.fetchall()
    conn.close()
    
    if not planos_ativos:
        st.info("📋 Nenhum plano alimentar ativo no momento.")
        if st.button("➕ Criar Primeiro Plano", use_container_width=True):
            st.session_state.active_meal_tab = 1
            st.rerun()
        return
    
    # Estatísticas dos planos ativos
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Planos Ativos", len(planos_ativos))
    
    with col2:
        planos_vencendo = [p for p in planos_ativos if p[11] and 
                          (datetime.strptime(p[11], '%Y-%m-%d').date() - date.today()).days <= 7]
        st.metric("⚠️ Vencendo em 7 dias", len(planos_vencendo))
    
    with col3:
        calorias_media = sum([p[6] for p in planos_ativos if p[6]]) / len(planos_ativos) if planos_ativos else 0
        st.metric("🔥 Calorias Média", f"{calorias_media:.0f}")
    
    with col4:
        planos_ia = len([p for p in planos_ativos if p[17]])  # ia_otimizado
        st.metric("🤖 Otimizados por IA", planos_ia)
    
    # Lista de planos ativos
    for plano in planos_ativos:
        validade = plano[11]
        dias_restantes = (datetime.strptime(validade, '%Y-%m-%d').date() - date.today()).days if validade else None
        
        # Cor baseada na validade
        if not validade:
            status_color = "#4CAF50"
            status_text = "Sem prazo"
        elif dias_restantes <= 0:
            status_color = "#F44336"
            status_text = "Vencido"
        elif dias_restantes <= 7:
            status_color = "#FF9800"
            status_text = f"{dias_restantes} dias restantes"
        else:
            status_color = "#4CAF50"
            status_text = f"{dias_restantes} dias restantes"
        
        with st.expander(f"📋 {plano[4]} - {plano[-1]} ({status_text})", expanded=False):
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**📊 Informações Nutricionais:**")
                st.markdown(f"• **Calorias:** {plano[6] or 'N/E'} kcal/dia")
                st.markdown(f"• **Carboidratos:** {plano[7] or 'N/E'}g")
                st.markdown(f"• **Proteínas:** {plano[8] or 'N/E'}g")
                st.markdown(f"• **Lipídios:** {plano[9] or 'N/E'}g")
                st.markdown(f"• **Fibras:** {plano[10] or 'N/E'}g")
            
            with col2:
                st.markdown("**🎯 Detalhes do Plano:**")
                st.markdown(f"• **Objetivo:** {plano[5] or 'N/E'}")
                st.markdown(f"• **Criado em:** {plano[10]}")
                st.markdown(f"• **Validade:** {plano[11] or 'Indefinida'}")
                if plano[18]:  # score_aderencia
                    st.markdown(f"• **Score Adesão:** {plano[18]:.1f}/10")
                if plano[17]:  # ia_otimizado
                    st.markdown("• **🤖 Otimizado por IA**")
            
            with col3:
                st.markdown("**🔧 Ações:**")
                
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    if st.button("👁️ Ver", key=f"view_plan_{plano[0]}"):
                        st.session_state.viewing_plan_id = plano[0]
                        st.session_state.active_meal_tab = 3
                        st.rerun()
                
                with col_btn2:
                    if st.button("✏️ Editar", key=f"edit_plan_{plano[0]}"):
                        st.session_state.editing_plan_id = plano[0]
                        st.session_state.active_meal_tab = 1
                        st.rerun()
                
                with col_btn3:
                    if st.button("📄 PDF", key=f"pdf_plan_{plano[0]}"):
                        st.session_state.pdf_plan_id = plano[0]
                        st.session_state.active_meal_tab = 4
                        st.rerun()

def show_create_meal_plan(user):
    st.markdown('<div class="sub-header">➕ Criar/Editar Plano Alimentar</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Verificar se está editando
    editing_plan_id = st.session_state.get('editing_plan_id', None)
    plan_data = None
    
    if editing_plan_id:
        cursor.execute("SELECT * FROM planos_alimentares WHERE id = ?", (editing_plan_id,))
        plan_data = cursor.fetchone()
        st.info(f"✏️ Editando plano: {plan_data[4] if plan_data else 'N/A'}")
    
    # Buscar pacientes
    cursor.execute("""
    SELECT id, nome FROM pacientes 
    WHERE nutricionista_id = ? AND ativo = 1
    ORDER BY nome
    """, (user['id'],))
    
    pacientes = cursor.fetchall()
    
    if not pacientes:
        st.warning("⚠️ Nenhum paciente cadastrado. Cadastre um paciente primeiro.")
        return
    
    with st.form("meal_plan_form"):
        
        # Informações básicas do plano
        st.markdown("##### 📋 Informações Básicas do Plano")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Selecionar paciente
            paciente_index = 0
            if plan_data and plan_data[2]:  # paciente_id
                for i, p in enumerate(pacientes):
                    if p[0] == plan_data[2]:
                        paciente_index = i
                        break
            
            paciente_selecionado = st.selectbox(
                "👤 Paciente *",
                options=pacientes,
                format_func=lambda x: x[1],
                index=paciente_index
            )
            
            nome_plano = st.text_input("📝 Nome do Plano *", 
                value=plan_data[4] if plan_data else "")
            
            objetivo_plano = st.selectbox("🎯 Objetivo do Plano", [
                "", "Perda de Peso", "Ganho de Peso", "Manutenção",
                "Ganho de Massa Muscular", "Controle Glicêmico",
                "Redução do Colesterol", "Hipertensão", "Performance Esportiva"
            ], index=0)
        
        with col2:
            data_validade = st.date_input("📅 Data de Validade",
                value=datetime.strptime(plan_data[11], '%Y-%m-%d').date() if plan_data and plan_data[11] 
                else date.today() + timedelta(days=30))
            
            calorias_totais = st.number_input("🔥 Calorias Totais (kcal) *", 
                0, 5000, plan_data[6] if plan_data and plan_data[6] else 2000, step=50)
            
            usar_calculadora = st.checkbox("🧮 Usar calculadora automática", 
                help="Calcula automaticamente baseado no perfil do paciente")
        
        # Distribuição de macronutrientes
        st.markdown("##### 🥗 Distribuição de Macronutrientes")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            carboidratos_g = st.number_input("🍞 Carboidratos (g)", 
                0.0, 1000.0, plan_data[7] if plan_data and plan_data[7] else 250.0, step=5.0)
            carboidratos_perc = (carboidratos_g * 4 / calorias_totais * 100) if calorias_totais > 0 else 0
            st.info(f"{carboidratos_perc:.1f}% das calorias")
        
        with col2:
            proteinas_g = st.number_input("🥩 Proteínas (g)", 
                0.0, 500.0, plan_data[8] if plan_data and plan_data[8] else 150.0, step=5.0)
            proteinas_perc = (proteinas_g * 4 / calorias_totais * 100) if calorias_totais > 0 else 0
            st.info(f"{proteinas_perc:.1f}% das calorias")
        
        with col3:
            lipidios_g = st.number_input("🥑 Lipídios (g)", 
                0.0, 300.0, plan_data[9] if plan_data and plan_data[9] else 67.0, step=5.0)
            lipidios_perc = (lipidios_g * 9 / calorias_totais * 100) if calorias_totais > 0 else 0
            st.info(f"{lipidios_perc:.1f}% das calorias")
        
        # Outros nutrientes
        col1, col2 = st.columns(2)
        
        with col1:
            fibras_g = st.number_input("🌾 Fibras (g)", 
                0.0, 100.0, plan_data[10] if plan_data and plan_data[10] else 25.0, step=1.0)
        
        with col2:
            sodio_mg = st.number_input("🧂 Sódio (mg)", 
                0.0, 5000.0, plan_data[11] if plan_data and plan_data[11] else 2000.0, step=50.0)
        
        # Estrutura das refeições
        st.markdown("##### 🍽️ Estrutura das Refeições")
        
        num_refeicoes = st.selectbox("Número de Refeições", [3, 4, 5, 6, 7], index=2)
        
        refeicoes_padrao = {
            3: ["Café da Manhã", "Almoço", "Jantar"],
            4: ["Café da Manhã", "Almoço", "Lanche da Tarde", "Jantar"],
            5: ["Café da Manhã", "Lanche da Manhã", "Almoço", "Lanche da Tarde", "Jantar"],
            6: ["Café da Manhã", "Lanche da Manhã", "Almoço", "Lanche da Tarde", "Jantar", "Ceia"],
            7: ["Café da Manhã", "Lanche da Manhã", "Almoço", "Lanche da Tarde", "Jantar", "Lanche da Noite", "Ceia"]
        }
        
        refeicoes_nomes = refeicoes_padrao[num_refeicoes]
        refeicoes_data = {}
        
        # Para cada refeição, definir detalhes
        for i, refeicao_nome in enumerate(refeicoes_nomes):
            with st.expander(f"🍽️ {refeicao_nome}", expanded=False):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    horario = st.time_input(f"⏰ Horário", 
                        value=datetime.strptime(f"{7+i*2}:00", "%H:%M").time(),
                        key=f"horario_{i}")
                    
                    percentual_calorias = st.slider(f"📊 % das Calorias", 
                        0, 50, 15 if i in [1, 3] else 25 if i == 2 else 20, 
                        key=f"perc_{i}")
                
                with col2:
                    alimentos = st.text_area(f"🥗 Alimentos/Preparações", 
                        placeholder="Ex: 1 fatia de pão integral, 1 ovo mexido, 1 copo de leite...",
                        key=f"alimentos_{i}",
                        height=100)
                
                calorias_refeicao = int(calorias_totais * percentual_calorias / 100)
                st.info(f"🔥 Calorias desta refeição: {calorias_refeicao} kcal")
                
                refeicoes_data[refeicao_nome] = {
                    'horario': horario.strftime('%H:%M'),
                    'percentual': percentual_calorias,
                    'calorias': calorias_refeicao,
                    'alimentos': alimentos
                }
        
        # Orientações gerais
        st.markdown("##### 📝 Orientações e Observações")
        
        col1, col2 = st.columns(2)
        
        with col1:
            orientacoes_gerais = st.text_area("💡 Orientações Gerais",
                placeholder="Orientações sobre hidratação, suplementação, preparo dos alimentos...",
                value=plan_data[14] if plan_data and plan_data[14] else "",
                height=150)
        
        with col2:
            observacoes_plan = st.text_area("📋 Observações do Plano",
                placeholder="Observações específicas, substituições permitidas, restrições...",
                value=plan_data[13] if plan_data and plan_data[13] else "",
                height=150)
        
        # Botões de submissão
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if editing_plan_id and st.form_submit_button("❌ Cancelar", use_container_width=True):
                st.session_state.editing_plan_id = None
                st.rerun()
        
        with col2:
            if st.form_submit_button("💾 Salvar Rascunho", use_container_width=True):
                st.info("💾 Funcionalidade de rascunho em desenvolvimento")
        
        with col3:
            submitted = st.form_submit_button(
                "✏️ Atualizar Plano" if editing_plan_id else "💾 Criar Plano", 
                use_container_width=True
            )
        
        if submitted:
            if not nome_plano or not paciente_selecionado or calorias_totais <= 0:
                st.error("❌ Preencha todos os campos obrigatórios!")
                return
            
            # Verificar se a soma dos percentuais é aproximadamente 100%
            soma_percentuais = sum([r['percentual'] for r in refeicoes_data.values()])
            if abs(soma_percentuais - 100) > 5:
                st.warning(f"⚠️ A soma dos percentuais das refeições é {soma_percentuais}%. Recomenda-se que seja próximo de 100%.")
            
            try:
                # Serializar dados das refeições
                refeicoes_json = json.dumps(refeicoes_data, ensure_ascii=False)
                
                if editing_plan_id:
                    # Atualizar plano existente
                    cursor.execute('''
                    UPDATE planos_alimentares SET
                        nome = ?, objetivo = ?, calorias_totais = ?, carboidratos = ?,
                        proteinas = ?, lipidios = ?, fibras = ?, sodio = ?,
                        data_validade = ?, refeicoes = ?, observacoes = ?, orientacoes = ?
                    WHERE id = ?
                    ''', (
                        nome_plano, objetivo_plano, calorias_totais, carboidratos_g,
                        proteinas_g, lipidios_g, fibras_g, sodio_mg,
                        data_validade, refeicoes_json, observacoes_plan, orientacoes_gerais,
                        editing_plan_id
                    ))
                    
                    st.success("✅ Plano alimentar atualizado com sucesso!")
                    st.session_state.editing_plan_id = None
                else:
                    # Criar novo plano
                    plano_uuid = str(uuid.uuid4())
                    
                    cursor.execute('''
                    INSERT INTO planos_alimentares (
                        uuid, paciente_id, nutricionista_id, nome, objetivo,
                        calorias_totais, carboidratos, proteinas, lipidios, fibras, sodio,
                        data_validade, refeicoes, observacoes, orientacoes, ativo
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                    ''', (
                        plano_uuid, paciente_selecionado[0], user['id'], nome_plano, objetivo_plano,
                        calorias_totais, carboidratos_g, proteinas_g, lipidios_g, fibras_g, sodio_mg,
                        data_validade, refeicoes_json, observacoes_plan, orientacoes_gerais
                    ))
                    
                    st.success("✅ Plano alimentar criado com sucesso!")
                
                conn.commit()
                
                # Mostrar resumo
                st.markdown("##### 📊 Resumo do Plano Criado")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.info(f"👤 **Paciente:** {paciente_selecionado[1]}")
                    st.info(f"📋 **Nome:** {nome_plano}")
                    st.info(f"🎯 **Objetivo:** {objetivo_plano}")
                
                with col2:
                    st.info(f"🔥 **Calorias:** {calorias_totais} kcal")
                    st.info(f"🍞 **Carboidratos:** {carboidratos_g}g ({carboidratos_perc:.1f}%)")
                    st.info(f"🥩 **Proteínas:** {proteinas_g}g ({proteinas_perc:.1f}%)")
                
                with col3:
                    st.info(f"🥑 **Lipídios:** {lipidios_g}g ({lipidios_perc:.1f}%)")
                    st.info(f"🌾 **Fibras:** {fibras_g}g")
                    st.info(f"🍽️ **Refeições:** {num_refeicoes}")
                
                time.sleep(2)
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Erro ao processar plano: {str(e)}")
            finally:
                conn.close()

def show_ai_meal_planner(user):
    st.markdown('<div class="sub-header">🤖 Assistente IA para Planos Alimentares</div>', unsafe_allow_html=True)
    
    st.info("🤖 **IA Nutricional Avançada** - Cria planos personalizados baseados em evidências científicas e perfil do paciente")
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT p.id, p.nome, p.sexo, p.data_nascimento, p.objetivo, p.restricoes_alimentares,
           a.peso, a.altura, a.imc, a.percentual_gordura
    FROM pacientes p
    LEFT JOIN avaliacoes a ON p.id = a.paciente_id
    WHERE p.nutricionista_id = ? AND p.ativo = 1
    ORDER BY p.nome, a.data_avaliacao DESC
    """, (user['id'],))
    
    pacientes_data = cursor.fetchall()
    conn.close()
    
    if not pacientes_data:
        st.warning("⚠️ Nenhum paciente com dados suficientes encontrado.")
        return
    
    # Agrupar por paciente (pegar dados mais recentes)
    pacientes_únicos = {}
    for row in pacientes_data:
        if row[0] not in pacientes_únicos:
            pacientes_únicos[row[0]] = row
    
    pacientes = list(pacientes_únicos.values())
    
    with st.form("ai_meal_planner_form"):
        st.markdown("##### 🎯 Configuração do Plano IA")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Seleção do paciente
            paciente_selecionado = st.selectbox(
                "👤 Selecione o Paciente",
                options=pacientes,
                format_func=lambda x: f"{x[1]} ({calculate_age(x[3]) if x[3] else 'N/I'} anos, {x[2] or 'N/I'})"
            )
            
            if paciente_selecionado:
                st.markdown("**📊 Dados do Paciente:**")
                idade = calculate_age(paciente_selecionado[3]) if paciente_selecionado[3] else None
                st.markdown(f"• **Idade:** {idade or 'N/I'} anos")
                st.markdown(f"• **Sexo:** {paciente_selecionado[2] or 'N/I'}")
                st.markdown(f"• **Objetivo:** {paciente_selecionado[4] or 'N/I'}")
                if paciente_selecionado[6] and paciente_selecionado[7]:
                    st.markdown(f"• **Peso/Altura:** {paciente_selecionado[6]:.1f}kg / {paciente_selecionado[7]*100:.0f}cm")
                    st.markdown(f"• **IMC:** {paciente_selecionado[8]:.1f}" if paciente_selecionado[8] else "")
        
        with col2:
            # Configurações avançadas da IA
            st.markdown("**🤖 Configurações da IA:**")
            
            nivel_atividade_ia = st.selectbox("🏃 Nível de Atividade", [
                "Sedentário", "Levemente ativo", "Moderadamente ativo", "Muito ativo", "Atleta"
            ])
            
            abordagem_nutricional = st.selectbox("📊 Abordagem Nutricional", [
                "Equilibrada (Padrão)", "Low Carb Moderado", "Mediterrânea", 
                "DASH (Hipertensão)", "Alta Proteína", "Anti-inflamatória"
            ])
            
            considerar_restricoes = st.checkbox("🚫 Considerar restrições alimentares", True)
            
            incluir_suplementacao = st.checkbox("💊 Incluir sugestões de suplementação")
            
            nivel_detalhamento = st.selectbox("📋 Nível de Detalhamento", [
                "Básico", "Intermediário", "Avançado com substituições"
            ])
        
        # Parâmetros específicos
        st.markdown("##### ⚙️ Parâmetros Específicos")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            objetivo_calorico = st.selectbox("🎯 Objetivo Calórico", [
                "Manutenção", "Déficit Moderado (-300 kcal)", "Déficit Alto (-500 kcal)",
                "Superávit Moderado (+300 kcal)", "Superávit Alto (+500 kcal)"
            ])
        
        with col2:
            numero_refeicoes_ia = st.selectbox("🍽️ Número de Refeições", [3, 4, 5, 6], index=2)
            
        with col3:
            orcamento_estimado = st.selectbox("💰 Orçamento Estimado", [
                "Econômico", "Moderado", "Sem restrição orçamentária"
            ])
        
        # Preferências culinárias
        st.markdown("##### 🍳 Preferências Culinárias")
        
        preferencias_culinarias = st.multiselect("Selecione as preferências:", [
            "Culinária Brasileira", "Mediterrânea", "Asiática", "Vegetariana",
            "Vegana", "Sem Glúten", "Sem Lactose", "Low Carb", "Cetogênica",
            "Comida de Rua Saudável", "Pratos Rápidos", "Meal Prep"
        ])
        
        # Alimentos a evitar
        alimentos_evitar = st.text_area("🚫 Alimentos Específicos a Evitar",
            placeholder="Ex: frango, brócolis, leite de vaca...")
        
        # Alimentos preferidos
        alimentos_preferidos = st.text_area("❤️ Alimentos Preferidos",
            placeholder="Ex: salmão, abacate, batata doce...")
        
        if st.form_submit_button("🤖 Gerar Plano com IA", use_container_width=True):
            if not paciente_selecionado:
                st.error("❌ Selecione um paciente!")
                return
            
            # Simular processamento da IA
            with st.spinner("🤖 IA analisando perfil do paciente e criando plano personalizado..."):
                time.sleep(3)  # Simular processamento
                
                # Calcular parâmetros baseado nos dados do paciente
                idade = calculate_age(paciente_selecionado[3]) if paciente_selecionado[3] else 30
                sexo = paciente_selecionado[2]
                peso = paciente_selecionado[6] or 70
                altura = paciente_selecionado[7] or 1.70
                
                # Calcular TMB usando Mifflin-St Jeor
                if sexo == "Masculino":
                    tmb = (10 * peso) + (6.25 * altura * 100) - (5 * idade) + 5
                else:
                    tmb = (10 * peso) + (6.25 * altura * 100) - (5 * idade) - 161
                
                # Aplicar fator de atividade
                fatores_atividade = {
                    "Sedentário": 1.2,
                    "Levemente ativo": 1.375,
                    "Moderadamente ativo": 1.55,
                    "Muito ativo": 1.725,
                    "Atleta": 1.9
                }
                
                get = tmb * fatores_atividade[nivel_atividade_ia]
                
                # Ajustar por objetivo calórico
                ajustes = {
                    "Manutenção": 0,
                    "Déficit Moderado (-300 kcal)": -300,
                    "Déficit Alto (-500 kcal)": -500,
                    "Superávit Moderado (+300 kcal)": +300,
                    "Superávit Alto (+500 kcal)": +500
                }
                
                calorias_plano = int(get + ajustes[objetivo_calorico])
                
                # Distribuição de macros baseada na abordagem
                distribuicoes = {
                    "Equilibrada (Padrão)": {"carb": 50, "prot": 20, "lip": 30},
                    "Low Carb Moderado": {"carb": 30, "prot": 30, "lip": 40},
                    "Mediterrânea": {"carb": 45, "prot": 18, "lip": 37},
                    "DASH (Hipertensão)": {"carb": 55, "prot": 18, "lip": 27},
                    "Alta Proteína": {"carb": 35, "prot": 35, "lip": 30},
                    "Anti-inflamatória": {"carb": 40, "prot": 25, "lip": 35}
                }
                
                dist = distribuicoes[abordagem_nutricional]
                carb_g = int(calorias_plano * dist["carb"] / 100 / 4)
                prot_g = int(calorias_plano * dist["prot"] / 100 / 4)
                lip_g = int(calorias_plano * dist["lip"] / 100 / 9)
                
            st.success("✅ Plano alimentar gerado pela IA com sucesso!")
            
            # Mostrar resultados
            st.markdown("### 🤖 Plano Gerado pela IA Nutricional")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🔥 Calorias", f"{calorias_plano} kcal")
                st.metric("📊 TMB Calculada", f"{tmb:.0f} kcal")
            
            with col2:
                st.metric("🍞 Carboidratos", f"{carb_g}g", f"{dist['carb']}%")
            
            with col3:
                st.metric("🥩 Proteínas", f"{prot_g}g", f"{dist['prot']}%")
                prot_por_kg = prot_g / peso
                st.caption(f"{prot_por_kg:.2f} g/kg")
            
            with col4:
                st.metric("🥑 Lipídios", f"{lip_g}g", f"{dist['lip']}%")
            
            # Plano alimentar detalhado gerado pela IA
            st.markdown("##### 🍽️ Estrutura Alimentar Sugerida")
            
            # Criar estrutura de refeições baseada no número selecionado
            refeicoes_ia = {
                3: [
                    {"nome": "Café da Manhã", "horario": "07:00", "calorias": int(calorias_plano * 0.30)},
                    {"nome": "Almoço", "horario": "12:00", "calorias": int(calorias_plano * 0.40)},
                    {"nome": "Jantar", "horario": "19:00", "calorias": int(calorias_plano * 0.30)}
                ],
                4: [
                    {"nome": "Café da Manhã", "horario": "07:00", "calorias": int(calorias_plano * 0.25)},
                    {"nome": "Almoço", "horario": "12:00", "calorias": int(calorias_plano * 0.35)},
                    {"nome": "Lanche da Tarde", "horario": "15:30", "calorias": int(calorias_plano * 0.15)},
                    {"nome": "Jantar", "horario": "19:00", "calorias": int(calorias_plano * 0.25)}
                ],
                5: [
                    {"nome": "Café da Manhã", "horario": "07:00", "calorias": int(calorias_plano * 0.20)},
                    {"nome": "Lanche da Manhã", "horario": "10:00", "calorias": int(calorias_plano * 0.10)},
                    {"nome": "Almoço", "horario": "12:30", "calorias": int(calorias_plano * 0.35)},
                    {"nome": "Lanche da Tarde", "horario": "15:30", "calorias": int(calorias_plano * 0.15)},
                    {"nome": "Jantar", "horario": "19:00", "calorias": int(calorias_plano * 0.20)}
                ],
                6: [
                    {"nome": "Café da Manhã", "horario": "07:00", "calorias": int(calorias_plano * 0.20)},
                    {"nome": "Lanche da Manhã", "horario": "10:00", "calorias": int(calorias_plano * 0.10)},
                    {"nome": "Almoço", "horario": "12:30", "calorias": int(calorias_plano * 0.30)},
                    {"nome": "Lanche da Tarde", "horario": "15:30", "calorias": int(calorias_plano * 0.15)},
                    {"nome": "Jantar", "horario": "19:00", "calorias": int(calorias_plano * 0.15)},
                    {"nome": "Ceia", "horario": "21:30", "calorias": int(calorias_plano * 0.10)}
                ]
            }
            
            # Sugestões de alimentos por refeição (simulado)
            sugestoes_alimentos = {
                "Café da Manhã": [
                    "2 fatias de pão integral",
                    "1 ovo mexido",
                    "1 copo de leite desnatado",
                    "1 banana média",
                    "1 col. sopa de aveia"
                ],
                "Lanche da Manhã": [
                    "1 maçã média",
                    "15g de castanha-do-pará"
                ],
                "Almoço": [
                    "150g de peito de frango grelhado",
                    "1 xíc. de arroz integral cozido",
                    "1 xíc. de feijão carioca",
                    "Salada de folhas verdes",
                    "1 col. sopa de azeite extra virgem"
                ],
                "Lanche da Tarde": [
                    "1 iogurte natural desnatado",
                    "1 col. sopa de granola",
                    "1/2 mamão papaia"
                ],
                "Jantar": [
                    "150g de salmão grelhado",
                    "200g de batata doce assada",
                    "Brócolis refogado",
                    "Salada de rúcula com tomate cereja"
                ],
                "Ceia": [
                    "1 copo de leite desnatado morno",
                    "1 col. sopa de aveia"
                ]
            }
            
            for refeicao in refeicoes_ia[numero_refeicoes_ia]:
                with st.expander(f"🍽️ {refeicao['nome']} - {refeicao['horario']} ({refeicao['calorias']} kcal)", expanded=True):
                    
                    alimentos = sugestoes_alimentos.get(refeicao['nome'], ["Alimentos personalizados baseados nas preferências"])
                    
                    for alimento in alimentos:
                        st.markdown(f"• {alimento}")
            
            # Orientações da IA
            st.markdown("##### 💡 Orientações Personalizadas da IA")
            
            orientacoes_ia = [
                f"🎯 **Objetivo:** {paciente_selecionado[4] or 'Melhoria da saúde geral'}",
                f"💧 **Hidratação:** Consuma {int(peso * 35)}ml de água por dia",
                f"🏃 **Atividade:** Mantenha seu nível atual ({nivel_atividade_ia.lower()})",
                f"📊 **Distribuição:** {abordagem_nutricional} - ideal para seu perfil"
            ]
            
            if considerar_restricoes and paciente_selecionado[5]:
                orientacoes_ia.append(f"🚫 **Restrições consideradas:** {paciente_selecionado[5]}")
            
            if incluir_suplementacao:
                orientacoes_ia.append("💊 **Suplementação:** Consulte sobre Vitamina D, Ômega-3 e Complexo B")
            
            for orientacao in orientacoes_ia:
                st.info(orientacao)
            
            # Opção de salvar o plano gerado
            if st.button("💾 Salvar Plano Gerado pela IA", use_container_width=True):
                
                # Preparar dados para salvamento
                refeicoes_data_ia = {}
                for refeicao in refeicoes_ia[numero_refeicoes_ia]:
                    alimentos_lista = sugestoes_alimentos.get(refeicao['nome'], [])
                    refeicoes_data_ia[refeicao['nome']] = {
                        'horario': refeicao['horario'],
                        'percentual': round(refeicao['calorias'] / calorias_plano * 100, 1),
                        'calorias': refeicao['calorias'],
                        'alimentos': '\n'.join([f"• {alimento}" for alimento in alimentos_lista])
                    }
                
                try:
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    plano_uuid = str(uuid.uuid4())
                    nome_plano_ia = f"Plano IA - {paciente_selecionado[1]} - {abordagem_nutricional}"
                    
                    cursor.execute('''
                    INSERT INTO planos_alimentares (
                        uuid, paciente_id, nutricionista_id, nome, objetivo,
                        calorias_totais, carboidratos, proteinas, lipidios, fibras,
                        data_validade, refeicoes, observacoes, orientacoes, ativo, ia_otimizado
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 1)
                    ''', (
                        plano_uuid, paciente_selecionado[0], user['id'], nome_plano_ia,
                        paciente_selecionado[4] or "Gerado por IA",
                        calorias_plano, carb_g, prot_g, lip_g, 25,
                        date.today() + timedelta(days=30),
                        json.dumps(refeicoes_data_ia, ensure_ascii=False),
                        f"Plano criado com IA Nutricional - Abordagem: {abordagem_nutricional}",
                        '\n'.join(orientacoes_ia)
                    ))
                    
                    conn.commit()
                    conn.close()
                    
                    st.success("✅ Plano gerado pela IA salvo com sucesso!")
                    
                except Exception as e:
                    st.error(f"❌ Erro ao salvar plano: {str(e)}")

def show_nutritional_meal_analysis(user):
    st.markdown('<div class="sub-header">📊 Análise Nutricional de Planos</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT pa.id, pa.nome, p.nome as paciente_nome, pa.calorias_totais,
           pa.carboidratos, pa.proteinas, pa.lipidios, pa.fibras
    FROM planos_alimentares pa
    JOIN pacientes p ON pa.paciente_id = p.id
    WHERE pa.nutricionista_id = ? AND pa.ativo = 1
    ORDER BY pa.data_criacao DESC
    """, (user['id'],))
    
    planos = cursor.fetchall()
    conn.close()
    
    if not planos:
        st.warning("⚠️ Nenhum plano ativo encontrado para análise.")
        return
    
    # Seleção do plano
    plano_selecionado = st.selectbox(
        "📋 Selecione o Plano para Análise",
        options=planos,
        format_func=lambda x: f"{x[1]} - {x[2]} ({x[3] or 'N/I'} kcal)"
    )
    
    if plano_selecionado:
        plano_id = plano_selecionado[0]
        
        st.markdown(f"### 📊 Análise Nutricional - {plano_selecionado[1]}")
        st.markdown(f"**👤 Paciente:** {plano_selecionado[2]}")
        
        # Dados nutricionais básicos
        calorias = plano_selecionado[3] or 0
        carb = plano_selecionado[4] or 0
        prot = plano_selecionado[5] or 0
        lip = plano_selecionado[6] or 0
        fibras = plano_selecionado[7] or 0
        
        # Cálculos de percentuais
        if calorias > 0:
            carb_perc = (carb * 4 / calorias) * 100
            prot_perc = (prot * 4 / calorias) * 100
            lip_perc = (lip * 9 / calorias) * 100
        else:
            carb_perc = prot_perc = lip_perc = 0
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🔥 Calorias Totais", f"{calorias} kcal")
        
        with col2:
            st.metric("🍞 Carboidratos", f"{carb}g", f"{carb_perc:.1f}%")
        
        with col3:
            st.metric("🥩 Proteínas", f"{prot}g", f"{prot_perc:.1f}%")
        
        with col4:
            st.metric("🥑 Lipídios", f"{lip}g", f"{lip_perc:.1f}%")
        
        # Análises detalhadas
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Distribuição Macro",
            "🎯 Adequação Nutricional", 
            "📈 Comparações",
            "💡 Recomendações"
        ])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de distribuição de macronutrientes
                fig_macro = px.pie(
                    values=[carb_perc, prot_perc, lip_perc],
                    names=['Carboidratos', 'Proteínas', 'Lipídios'],
                    title="Distribuição de Macronutrientes (%)",
                    color_discrete_sequence=['#4CAF50', '#2196F3', '#FF9800']
                )
                st.plotly_chart(fig_macro, use_container_width=True)
            
            with col2:
                # Gráfico de calorias por macronutriente
                calorias_macro = {
                    'Carboidratos': carb * 4,
                    'Proteínas': prot * 4,
                    'Lipídios': lip * 9
                }
                
                fig_calorias = px.bar(
                    x=list(calorias_macro.keys()),
                    y=list(calorias_macro.values()),
                    title="Distribuição de Calorias por Macronutriente",
                    color=list(calorias_macro.keys()),
                    color_discrete_sequence=['#4CAF50', '#2196F3', '#FF9800']
                )
                fig_calorias.update_layout(showlegend=False)
                st.plotly_chart(fig_calorias, use_container_width=True)
        
        with tab2:
            st.markdown("##### 🎯 Análise de Adequação Nutricional")
            
            # Faixas de referência baseadas em diretrizes
            referencias = {
                "Carboidratos": {"min": 45, "max": 65, "atual": carb_perc},
                "Proteínas": {"min": 10, "max": 35, "atual": prot_perc},
                "Lipídios": {"min": 20, "max": 35, "atual": lip_perc}
            }
            
            for nutriente, valores in referencias.items():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Barra de progresso customizada
                    atual = valores["atual"]
                    minimo = valores["min"]
                    maximo = valores["max"]
                    
                    if atual < minimo:
                        cor = "#F44336"  # Vermelho
                        status = "Abaixo"
                    elif atual > maximo:
                        cor = "#FF9800"  # Laranja
                        status = "Acima"
                    else:
                        cor = "#4CAF50"  # Verde
                        status = "Adequado"
                    
                    # Criar gráfico de barras horizontal para mostrar faixa
                    fig_adequacao = go.Figure()
                    
                    # Barra de fundo (faixa ideal)
                    fig_adequacao.add_trace(go.Bar(
                        y=[nutriente],
                        x=[maximo],
                        orientation='h',
                        marker_color='#E0E0E0',
                        name='Máximo',
                        showlegend=False
                    ))
                    
                    # Barra de valor atual
                    fig_adequacao.add_trace(go.Bar(
                        y=[nutriente],
                        x=[atual],
                        orientation='h',
                        marker_color=cor,
                        name='Atual',
                        showlegend=False
                    ))
                    
                    # Adicionar linhas de referência
                    fig_adequacao.add_vline(x=minimo, line_dash="dash", line_color="green", 
                                          annotation_text=f"Mín: {minimo}%")
                    fig_adequacao.add_vline(x=maximo, line_dash="dash", line_color="red", 
                                          annotation_text=f"Máx: {maximo}%")
                    
                    fig_adequacao.update_layout(
                        title=f"{nutriente}: {atual:.1f}%",
                        xaxis_title="Percentual (%)",
                        height=150,
                        margin=dict(l=0, r=0, t=40, b=0)
                    )
                    
                    st.plotly_chart(fig_adequacao, use_container_width=True)
                
                with col2:
                    st.markdown(f"**Status:**")
                    st.markdown(f"<span style='color: {cor}; font-weight: bold;'>{status}</span>", 
                              unsafe_allow_html=True)
                    st.markdown(f"**Ideal:** {minimo}-{maximo}%")
        
        with tab3:
            st.markdown("##### 📈 Comparações com Diretrizes")
            
            # Comparar com diferentes diretrizes nutricionais
            diretrizes = {
                "OMS/WHO": {"carb": 55, "prot": 15, "lip": 30},
                "Diretriz Brasileira": {"carb": 50, "prot": 20, "lip": 30},
                "DASH": {"carb": 55, "prot": 18, "lip": 27},
                "Mediterrânea": {"carb": 45, "prot": 18, "lip": 37}
            }
            
            # Criar DataFrame para comparação
            dados_comparacao = []
            for nome, valores in diretrizes.items():
                dados_comparacao.append({
                    'Diretriz': nome,
                    'Carboidratos': valores['carb'],
                    'Proteínas': valores['prot'],
                    'Lipídios': valores['lip']
                })
            
            # Adicionar dados do plano atual
            dados_comparacao.append({
                'Diretriz': 'Plano Atual',
                'Carboidratos': carb_perc,
                'Proteínas': prot_perc,
                'Lipídios': lip_perc
            })
            
            df_comparacao = pd.DataFrame(dados_comparacao)
            
            # Gráfico de comparação
            fig_comparacao = px.bar(
                df_comparacao,
                x='Diretriz',
                y=['Carboidratos', 'Proteínas', 'Lipídios'],
                title="Comparação com Diretrizes Nutricionais",
                barmode='group',
                color_discrete_sequence=['#4CAF50', '#2196F3', '#FF9800']
            )
            st.plotly_chart(fig_comparacao, use_container_width=True)
            
            # Análise de aderência
            st.markdown("##### 📊 Análise de Aderência às Diretrizes")
            
            for nome, valores in diretrizes.items():
                diferenca_carb = abs(carb_perc - valores['carb'])
                diferenca_prot = abs(prot_perc - valores['prot'])
                diferenca_lip = abs(lip_perc - valores['lip'])
                
                aderencia = 100 - ((diferenca_carb + diferenca_prot + diferenca_lip) / 3)
                aderencia = max(0, aderencia)
                
                cor_aderencia = "#4CAF50" if aderencia >= 80 else "#FF9800" if aderencia >= 60 else "#F44336"
                
                st.markdown(f"""
                <div style="background: {cor_aderencia}20; border-left: 4px solid {cor_aderencia}; padding: 0.5rem; margin: 0.25rem 0;">
                    <strong>{nome}:</strong> Aderência de <span style="color: {cor_aderencia}; font-weight: bold;">{aderencia:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
        
        with tab4:
            st.markdown("##### 💡 Recomendações para Otimização")
            
            recomendacoes = []
            
            # Análise de carboidratos
            if carb_perc < 45:
                recomendacoes.append({
                    "tipo": "warning",
                    "titulo": "🍞 Carboidratos Baixos",
                    "descricao": f"O percentual atual ({carb_perc:.1f}%) está abaixo do recomendado (45-65%). Considere incluir mais cereais integrais, frutas e vegetais amiláceos."
                })
            elif carb_perc > 65:
                recomendacoes.append({
                    "tipo": "warning",
                    "titulo": "🍞 Carboidratos Elevados",
                    "descricao": f"O percentual atual ({carb_perc:.1f}%) está acima do recomendado (45-65%). Considere reduzir carboidratos simples e aumentar proteínas."
                })
            else:
                recomendacoes.append({
                    "tipo": "success",
                    "titulo": "🍞 Carboidratos Adequados",
                    "descricao": f"O percentual atual ({carb_perc:.1f}%) está dentro da faixa ideal (45-65%)."
                })
            
            # Análise de proteínas
            if prot_perc < 10:
                recomendacoes.append({
                    "tipo": "error",
                    "titulo": "🥩 Proteínas Insuficientes",
                    "descricao": f"O percentual atual ({prot_perc:.1f}%) está muito baixo. Inclua mais carnes magras, peixes, ovos, leguminosas e laticínios."
                })
            elif prot_perc > 35:
                recomendacoes.append({
                    "tipo": "warning",
                    "titulo": "🥩 Proteínas Muito Elevadas",
                    "descricao": f"O percentual atual ({prot_perc:.1f}%) está muito alto. Verifique se há necessidade específica ou reduza gradualmente."
                })
            elif prot_perc < 15:
                recomendacoes.append({
                    "tipo": "info",
                    "titulo": "🥩 Proteínas Podem Ser Aumentadas",
                    "descricao": f"Atual: {prot_perc:.1f}%. Para melhor saciedade e preservação muscular, considere aumentar para 18-25%."
                })
            else:
                recomendacoes.append({
                    "tipo": "success",
                    "titulo": "🥩 Proteínas Adequadas",
                    "descricao": f"O percentual atual ({prot_perc:.1f}%) está em uma faixa adequada."
                })
            
            # Análise de lipídios
            if lip_perc < 20:
                recomendacoes.append({
                    "tipo": "warning",
                    "titulo": "🥑 Lipídios Insuficientes",
                    "descricao": f"O percentual atual ({lip_perc:.1f}%) pode ser insuficiente para absorção de vitaminas lipossolúveis. Inclua azeite, abacate e oleaginosas."
                })
            elif lip_perc > 35:
                recomendacoes.append({
                    "tipo": "warning",
                    "titulo": "🥑 Lipídios Elevados",
                    "descricao": f"O percentual atual ({lip_perc:.1f}%) está alto. Revise as fontes e priorize gorduras insaturadas."
                })
            else:
                recomendacoes.append({
                    "tipo": "success",
                    "titulo": "🥑 Lipídios Adequados",
                    "descricao": f"O percentual atual ({lip_perc:.1f}%) está dentro da faixa recomendada."
                })
            
            # Análise de fibras
            if fibras > 0:
                if fibras < 25:
                    recomendacoes.append({
                        "tipo": "info",
                        "titulo": "🌾 Fibras - Considerar Aumento",
                        "descricao": f"Atual: {fibras}g. Recomenda-se 25-35g/dia. Inclua mais cereais integrais, frutas e vegetais."
                    })
                elif fibras > 35:
                    recomendacoes.append({
                        "tipo": "info",
                        "titulo": "🌾 Fibras - Atenção ao Excesso",
                        "descricao": f"Atual: {fibras}g. Acima de 35g pode causar desconforto intestinal. Aumente gradualmente."
                    })
                else:
                    recomendacoes.append({
                        "tipo": "success",
                        "titulo": "🌾 Fibras Adequadas",
                        "descricao": f"Atual: {fibras}g está na faixa ideal (25-35g)."
                    })
            
            # Mostrar recomendações
            for rec in recomendacoes:
                if rec["tipo"] == "success":
                    st.success(f"**{rec['titulo']}**\n{rec['descricao']}")
                elif rec["tipo"] == "warning":
                    st.warning(f"**{rec['titulo']}**\n{rec['descricao']}")
                elif rec["tipo"] == "error":
                    st.error(f"**{rec['titulo']}**\n{rec['descricao']}")
                else:
                    st.info(f"**{rec['titulo']}**\n{rec['descricao']}")

def show_print_meal_plans(user):
    st.markdown('<div class="sub-header">🖨️ Imprimir e Exportar Planos</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT pa.id, pa.nome, p.nome as paciente_nome, pa.data_criacao
    FROM planos_alimentares pa
    JOIN pacientes p ON pa.paciente_id = p.id
    WHERE pa.nutricionista_id = ? AND pa.ativo = 1
    ORDER BY pa.data_criacao DESC
    """, (user['id'],))
    
    planos = cursor.fetchall()
    conn.close()
    
    if not planos:
        st.warning("⚠️ Nenhum plano ativo encontrado.")
        return
    
    # Seleção múltipla de planos
    planos_selecionados = st.multiselect(
        "📋 Selecione os Planos para Exportar",
        options=planos,
        format_func=lambda x: f"{x[1]} - {x[2]} ({x[3]})"
    )
    
    if not planos_selecionados:
        st.info("📋 Selecione pelo menos um plano para continuar.")
        return
    
    # Opções de formatação
    st.markdown("##### 🎨 Opções de Formatação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        formato_exportacao = st.selectbox("📄 Formato", [
            "PDF Profissional",
            "PDF Simples",
            "Word (.docx)",
            "HTML para Web",
            "Texto Simples"
        ])
        
        incluir_logo = st.checkbox("🏢 Incluir logo da clínica", True)
        incluir_cabecalho = st.checkbox("📋 Incluir cabeçalho personalizado", True)
        incluir_rodape = st.checkbox("📄 Incluir informações de contato no rodapé", True)
    
    with col2:
        orientacao = st.radio("📐 Orientação", ["Retrato", "Paisagem"])
        tamanho_fonte = st.selectbox("🔤 Tamanho da Fonte", ["8pt", "10pt", "12pt", "14pt"], index=2)
        incluir_valores_nutricionais = st.checkbox("📊 Incluir valores nutricionais detalhados", True)
        incluir_observacoes = st.checkbox("📝 Incluir observações e orientações", True)
    
    # Personalização do cabeçalho
    if incluir_cabecalho:
        st.markdown("##### ✏️ Personalizar Cabeçalho")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome_clinica = st.text_input("🏢 Nome da Clínica", 
                value=user.get('clinica', 'Clínica de Nutrição'))
            nome_nutricionista = st.text_input("👨‍⚕️ Nome do Nutricionista", 
                value=user['nome'])
        
        with col2:
            coren_numero = st.text_input("🏥 COREN/CRN", 
                value=user.get('coren', ''))
            telefone_contato = st.text_input("📞 Telefone", 
                value=user.get('telefone', ''))
    
    # Preview dos planos selecionados
    st.markdown("##### 👁️ Preview dos Planos Selecionados")
    
    for plano_dados in planos_selecionados:
        with st.expander(f"📋 {plano_dados[1]} - {plano_dados[2]}", expanded=False):
            
            # Buscar detalhes completos do plano
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM planos_alimentares WHERE id = ?", (plano_dados[0],))
            plano_completo = cursor.fetchone()
            
            cursor.execute("SELECT * FROM pacientes WHERE id = ?", (plano_completo[2],))
            paciente_dados = cursor.fetchone()
            
            conn.close()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Informações Nutricionais:**")
                st.markdown(f"• Calorias: {plano_completo[6] or 'N/E'} kcal")
                st.markdown(f"• Carboidratos: {plano_completo[7] or 'N/E'}g")
                st.markdown(f"• Proteínas: {plano_completo[8] or 'N/E'}g")
                st.markdown(f"• Lipídios: {plano_completo[9] or 'N/E'}g")
            
            with col2:
                st.markdown("**👤 Dados do Paciente:**")
                if paciente_dados[6]:  # data_nascimento
                    idade = calculate_age(paciente_dados[6])
                    st.markdown(f"• Idade: {idade} anos")
                st.markdown(f"• Sexo: {paciente_dados[7] or 'N/I'}")
                st.markdown(f"• Objetivo: {plano_completo[5] or 'N/E'}")
    
    # Botões de ação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Gerar PDF", use_container_width=True):
            with st.spinner("📄 Gerando PDF..."):
                time.sleep(2)
                st.success("✅ PDF gerado com sucesso!")
                
                # Simular download
                pdf_content = "Conteúdo do PDF simulado"
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_content,
                    file_name=f"planos_alimentares_{date.today().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
    
    with col2:
        if st.button("📧 Enviar por Email", use_container_width=True):
            
            emails_pacientes = []
            for plano_dados in planos_selecionados:
                conn = db_manager.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT email, nome FROM pacientes WHERE id = (SELECT paciente_id FROM planos_alimentares WHERE id = ?)", (plano_dados[0],))
                paciente_email = cursor.fetchone()
                conn.close()
                
                if paciente_email and paciente_email[0]:
                    emails_pacientes.append(f"{paciente_email[1]} ({paciente_email[0]})")
            
            if emails_pacientes:
                st.info(f"📧 Enviando para: {', '.join(emails_pacientes)}")
                with st.spinner("📧 Enviando emails..."):
                    time.sleep(2)
                st.success("✅ Emails enviados com sucesso!")
            else:
                st.warning("⚠️ Nenhum paciente possui email cadastrado.")
    
    with col3:
        if st.button("🖨️ Imprimir", use_container_width=True):
            st.info("🖨️ Abrindo diálogo de impressão... (funcionalidade simulada)")
    
    # Histórico de exportações
    st.markdown("##### 📊 Histórico de Exportações Recentes")
    
    # Simular histórico
    historico_exportacoes = [
        {
            "data": "2024-01-15 14:30",
            "planos": 3,
            "formato": "PDF Profissional",
            "status": "Concluído"
        },
        {
            "data": "2024-01-14 09:15",
            "planos": 1,
            "formato": "Word (.docx)",
            "status": "Concluído"
        },
        {
            "data": "2024-01-13 16:45",
            "planos": 5,
            "formato": "PDF Simples",
            "status": "Enviado por Email"
        }
    ]
    
    for hist in historico_exportacoes:
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 0.5rem; margin: 0.25rem 0; border-radius: 5px; border-left: 3px solid #4CAF50;">
            <strong>📅 {hist['data']}</strong> - {hist['planos']} plano(s) | {hist['formato']} | Status: {hist['status']}
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# 🍳 SISTEMA COMPLETO DE RECEITAS
# =============================================================================

def show_receitas(user):
    load_css()
    
    st.markdown('<h1 class="ultra-header">🍳 Sistema de Receitas Nutricionais</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📚 Banco de Receitas",
        "➕ Nova Receita",
        "🔍 Busca Avançada",
        "📊 Análise Nutricional",
        "⭐ Favoritas"
    ])
    
    with tab1:
        show_recipes_database(user)
    
    with tab2:
        show_new_recipe_form(user)
    
    with tab3:
        show_advanced_recipe_search(user)
    
    with tab4:
        show_recipe_nutritional_analysis(user)
    
    with tab5:
        show_favorite_recipes(user)

def show_recipes_database(user):
    st.markdown('<div class="sub-header">📚 Banco de Receitas Nutricionais</div>', unsafe_allow_html=True)
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    # Buscar estatísticas
    cursor.execute("SELECT COUNT(*) FROM receitas WHERE criada_por = ?", (user['id'],))
    minhas_receitas = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM receitas WHERE publica = 1")
    receitas_publicas = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT categoria) FROM receitas WHERE criada_por = ? OR publica = 1", (user['id'],))
    total_categorias = cursor.fetchone()[0]
    
    # Estatísticas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👨‍🍳 Minhas Receitas", minhas_receitas)
    
    with col2:
        st.metric("🌍 Receitas Públicas", receitas_publicas)
    
    with col3:
        st.metric("📂 Categorias", total_categorias)
    
    with col4:
        total_receitas = minhas_receitas + receitas_publicas
        st.metric("📚 Total Disponível", total_receitas)
    
    # Filtros
    st.markdown("##### 🔍 Filtros")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Buscar categorias disponíveis
        cursor.execute("""
        SELECT DISTINCT categoria FROM receitas 
        WHERE (criada_por = ? OR publica = 1) AND categoria IS NOT NULL
        ORDER BY categoria
        """, (user['id'],))
        categorias = [cat[0] for cat in cursor.fetchall()]
        
        categoria_filtro = st.selectbox("📂 Categoria", ["Todas"] + categorias)
    
    with col2:
        dificuldade_filtro = st.selectbox("⭐ Dificuldade", [
            "Todas", "Fácil", "Médio", "Difícil"
        ])
    
    with col3:
        tempo_filtro = st.selectbox("⏱️ Tempo de Preparo", [
            "Todos", "Até 15 min", "15-30 min", "30-60 min", "Mais de 1h"
        ])
    
    with col4:
        origem_filtro = st.selectbox("👨‍🍳 Origem", [
            "Todas", "Minhas Receitas", "Receitas Públicas"
        ])
    
    # Busca por texto
    busca_texto = st.text_input("🔍 Buscar receitas por nome ou ingredientes", 
                               placeholder="Ex: frango, banana, low carb...")
    
    # Query principal com filtros
    query = """
    SELECT r.*, u.nome as criador_nome
    FROM receitas r
    LEFT JOIN usuarios u ON r.criada_por = u.id
    WHERE (r.criada_por = ? OR r.publica = 1)
    """
    params = [user['id']]
    
    # Aplicar filtros
    if categoria_filtro != "Todas":
        query += " AND r.categoria = ?"
        params.append(categoria_filtro)
    
    if dificuldade_filtro != "Todas":
        query += " AND r.dificuldade = ?"
        params.append(dificuldade_filtro)
    
    if tempo_filtro != "Todos":
        if tempo_filtro == "Até 15 min":
            query += " AND r.tempo_preparo <= 15"
        elif tempo_filtro == "15-30 min":
            query += " AND r.tempo_preparo BETWEEN 16 AND 30"
        elif tempo_filtro == "30-60 min":
            query += " AND r.tempo_preparo BETWEEN 31 AND 60"
        else:  # Mais de 1h
            query += " AND r.tempo_preparo > 60"
    
    if origem_filtro == "Minhas Receitas":
        query += " AND r.criada_por = ?"
        params.append(user['id'])
    elif origem_filtro == "Receitas Públicas":
        query += " AND r.publica = 1 AND r.criada_por != ?"
        params.append(user['id'])
    
    if busca_texto:
        query += " AND (r.nome LIKE ? OR r.ingredientes LIKE ? OR r.tags LIKE ?)"
        busca_term = f"%{busca_texto}%"
        params.extend([busca_term, busca_term, busca_term])
    
    query += " ORDER BY r.data_criacao DESC"
    
    cursor.execute(query, params)
    receitas = cursor.fetchall()
    conn.close()
    
    if not receitas:
        st.info("📝 Nenhuma receita encontrada com os filtros aplicados.")
        if st.button("➕ Criar Primeira Receita", use_container_width=True):
            st.session_state.active_recipe_tab = 1
            st.rerun()
        return
    
    st.markdown(f"##### 📚 {len(receitas)} Receitas Encontradas")
    
    # Exibir receitas em grid
    num_cols = 2
    for i in range(0, len(receitas), num_cols):
        cols = st.columns(num_cols)
        
        for j, col in enumerate(cols):
            if i + j < len(receitas):
                receita = receitas[i + j]
                
                with col:
                    with st.container():
                        # Informações básicas
                        tempo_total = (receita[7] or 0) + (receita[8] or 0)  # preparo + cozimento
                        
                        st.markdown(f'''
                        <div class="recipe-card">
                            <h4>🍳 {receita[2]}</h4>
                            <p><strong>📂 Categoria:</strong> {receita[3] or 'Não categorizada'}</p>
                            <p><strong>⭐ Dificuldade:</strong> {receita[10] or 'N/I'} | 
                               <strong>⏱️ Tempo:</strong> {tempo_total}min | 
                               <strong>🍽️ Porções:</strong> {receita[9] or 'N/I'}</p>
                            <p><strong>🔥 Calorias/porção:</strong> {receita[11] or 'N/I'} kcal</p>
                            <p><strong>👨‍🍳 Criado por:</strong> {receita[-1] or 'Sistema'}</p>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                        # Botões de ação
                        col_btn1, col_btn2, col_btn3 = st.columns(3)
                        
                        with col_btn1:
                            if st.button("👁️ Ver", key=f"view_recipe_{receita[0]}"):
                                st.session_state.viewing_recipe_id = receita[0]
                                st.session_state.show_recipe_details = True
                                st.rerun()
                        
                        with col_btn2:
                            if receita[24] == user['id']:  # criada_por
                                if st.button("✏️ Editar", key=f"edit_recipe_{receita[0]}"):
                                    st.session_state.editing_recipe_id = receita[0]
                                    st.session_state.active_recipe_tab = 1
                                    st.rerun()
                            else:
                                if st.button("📋 Copiar", key=f"copy_recipe_{receita[0]}"):
                                    st.session_state.copying_recipe_id = receita[0]
                                    st.session_state.active_recipe_tab = 1
                                    st.rerun()
                        
                        with col_btn3:
                            # Rating atual
                            rating = receita[27] or 0
                            if st.button(f"⭐ {rating:.1f}", key=f"rate_recipe_{receita[0]}"):
                                st.session_state.rating_recipe_id = receita[0]
                                st.rerun()
    
    # Modal para detalhes da receita
    if st.session_state.get('show_recipe_details', False):
        show_recipe_details_modal(user)

def show_recipe_details_modal(user):
    """Modal com detalhes completos da receita"""
    
    recipe_id = st.session_state.get('viewing_recipe_id')
    if not recipe_id:
        return
    
    conn = db_manager.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM receitas WHERE id = ?", (recipe_id,))
    receita = cursor.fetchone()
    conn.close()
    
    if not receita:
        st.error("Receita não encontrada")
        return
    
    # Modal usando expander
    with st.expander(f"🍳 {receita[2]} - Detalhes Completos", expanded=True):
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### 📋 {receita[2]}")
            st.markdown(f"**📂 Categoria:** {receita[3] or 'Não informada'}")
            st.markdown(f"**⭐ Dificuldade:** {receita[10] or 'N/I'}")
            st.markdown(f"**⏱️ Tempo de Preparo:** {receita[7] or 0} min")
            st.markdown(f"**🔥 Tempo de Cozimento:** {receita[8] or 0} min")
            st.markdown(f"**🍽️ Porções:** {receita[9] or 'N/I'}")
            
            # Tags
            if receita[22]:  # tags
                tags = receita[22].split(',')
                tags_html = ' '.join([f'<span style="background: #E8F5E8; padding: 2px 8px; border-radius: 12px; margin: 2px; font-size: 0.8em;">#{tag.strip()}</span>' for tag in tags])
                st.markdown(f"**🏷️ Tags:** {tags_html}", unsafe_allow_html=True)
        
        with col2:
            st.markdown("### 📊 Informação Nutricional (por porção)")
            
            col_nut1, col_nut2 = st.columns(2)
            
            with col_nut1:
                st.metric("🔥 Calorias", f"{receita[11] or 0} kcal")
                st.metric("🍞 Carboidratos", f"{receita[12] or 0}g")
                st.metric("🥩 Proteínas", f"{receita[13] or 0}g")
            
            with col_nut2:
                st.metric("🥑 Lipídios", f"{receita[14] or 0}g")
                st.metric("🌾 Fibras", f"{receita[15] or 0}g")
                st.metric("🧂 Sódio", f"{receita[16] or 0}mg")
        
        # Ingredientes
        st.markdown("### 🥗 Ingredientes")
        if receita[4]:  # ingredientes
            try:
                ingredientes = json.loads(receita[4])
                for ingrediente in ingredientes:
                    st.markdown(f"• {ingrediente}")
            except:
                st.text(receita[4])
        else:
            st.info("Nenhum ingrediente listado.")
        
        # Modo de preparo
        st.markdown("### 👨‍🍳 Modo de Preparo")
        if receita[5]:  # modo_preparo
            # Separar por linhas ou números
            preparo_steps = receita[5].split('\n')
            for i, step in enumerate(preparo_steps, 1):
                if step.strip():
                    st.markdown(f"**{i}.** {step.strip()}")
        else:
            st.info("Modo de preparo não informado.")
        
        # Ações
        col_action1, col_action2, col_action3, col_action4 = st.columns(4)
        
        with col_action1:
            if st.button("📋 Adicionar ao Plano", key="add_to_plan"):
                st.info("Funcionalidade em desenvolvimento")
        
        with col_action2:
            if st.button("📱 Compartilhar", key="share_recipe"):
                st.success("Link copiado: https://nutriapp.com/receitas/{}".format(receita[0]))
        
        with col_action3:
            if st.button("🖨️ Imprimir", key="print_recipe"):
                st.info("Abrindo versão para impressão...")
        
        with col_action4:
            if st.button("❌ Fechar", key="close_recipe"):
                st.session_state.show_recipe_details = False
                st.rerun()

def show_new_recipe_form(user):
    st.markdown('<div class="sub-header">➕ Criar/Editar Receita</div>', unsafe_allow_html=True)
    
    # Verificar se está editando ou copiando
    editing_id = st.session_state.get('editing_recipe_id', None)
    copying_id = st.session_state.get('copying_recipe_id', None)
    
    recipe_data = None
    
    if editing_id:
        st.info(f"✏️ Editando receita (ID: {editing_id})")
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM receitas WHERE id = ?", (editing_id,))
        recipe_data = cursor.fetchone()
        conn.close()
    elif copying_id:
        st.info(f"📋 Copiando receita (ID: {copying_id})")
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM receitas WHERE id = ?", (copying_id,))
        recipe_data = cursor.fetchone()
        conn.close()
    
    with st.form("recipe_form"):
        
        # Informações básicas
        st.markdown("##### 📋 Informações Básicas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome_receita = st.text_input("🍳 Nome da Receita *", 
                value=f"Cópia de {recipe_data[2]}" if copying_id and recipe_data else recipe_data[2] if recipe_data else "")
            
            categoria_receita = st.selectbox("📂 Categoria", [
                "", "Café da Manhã", "Lanches", "Almoço", "Jantar", "Sobremesas",
                "Bebidas", "Saladas", "Sopas", "Carnes", "Peixes", "Vegetarianos",
                "Veganos", "Sem Glúten", "Low Carb", "Proteicos", "Light", "Outras"
            ], index=0)
            
            dificuldade_receita = st.selectbox("⭐ Dificuldade", [
                "", "Fácil", "Médio", "Difícil"
            ], index=0)
        
        with col2:
            tempo_preparo = st.number_input("⏱️ Tempo de Preparo (min)", 
                0, 480, recipe_data[7] if recipe_data and recipe_data[7] else 0)
            
            tempo_cozimento = st.number_input("🔥 Tempo de Cozimento (min)", 
                0, 480, recipe_data[8] if recipe_data and recipe_data[8] else 0)
            
            num_porcoes = st.number_input("🍽️ Número de Porções", 
                1, 20, recipe_data[9] if recipe_data and recipe_data[9] else 1)
        
        # Ingredientes
        st.markdown("##### 🥗 Ingredientes")
        
        # Interface para adicionar ingredientes dinamicamente
        if 'recipe_ingredients' not in st.session_state:
            if recipe_data and recipe_data[4]:
                try:
                    st.session_state.recipe_ingredients = json.loads(recipe_data[4])
                except:
                    st.session_state.recipe_ingredients = [""]
            else:
                st.session_state.recipe_ingredients = [""]
        
        # Mostrar ingredientes atuais
        ingredientes_atuais = []
        for i, ingrediente in enumerate(st.session_state.recipe_ingredients):
            col_ing, col_del = st.columns([4, 1])
            
            with col_ing:
                ing_value = st.text_input(f"Ingrediente {i+1}", value=ingrediente, key=f"ing_{i}")
                if ing_value:
                    ingredientes_atuais.append(ing_value)
            
            with col_del:
                if st.form_submit_button("🗑️", key=f"del_ing_{i}") and len(st.session_state.recipe_ingredients) > 1:
                    st.session_state.recipe_ingredients.pop(i)
                    st.rerun()
        
        # Botão para adicionar mais ingredientes
        if st.form_submit_button("➕ Adicionar Ingrediente"):
            st.session_state.recipe_ingredients.append("")
            st.rerun()
        
        # Modo de preparo
        st.markdown("##### 👨‍🍳 Modo de Preparo")
        
        modo_preparo = st.text_area("Descreva passo a passo como preparar a receita", 
            value=recipe_data[5] if recipe_data and recipe_data[5] else "",
            height=200,
            placeholder="""1. Pré-aqueça o forno a 180°C
2. Em uma tigela, misture os ingredientes secos...
3. Adicione os ingredientes líquidos...
...""")
        
        # Informações nutricionais
        st.markdown("##### 📊 Informações Nutricionais (por porção)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            calorias_porcao = st.number_input("🔥 Calorias", 
                0.0, 2000.0, recipe_data[11] if recipe_data and recipe_data[11] else 0.0, step=1.0)
            
            carboidratos = st.number_input("🍞 Carboidratos (g)", 
                0.0, 200.0, recipe_data[12] if recipe_data and recipe_data[12] else 0.0, step=0.1)
            
            fibras = st.number_input("🌾 Fibras (g)", 
                0.0, 50.0, recipe_data[15] if recipe_data and recipe_data[15] else 0.0, step=0.1)
        
        with col2:
            proteinas = st.number_input("🥩 Proteínas (g)", 
                0.0, 100.0, recipe_data[13] if recipe_data and recipe_data[13] else 0.0, step=0.1)
            
            lipidios = st.number_input("🥑 Lipídios (g)", 
                0.0, 100.0, recipe_data[14] if recipe_data and recipe_data[14] else 0.0, step=0.1)
            
            acucar = st.number_input("🍯 Açúcar (g)", 
                0.0, 100.0, recipe_data[17] if recipe_data and recipe_data[17] else 0.0, step=0.1)
        
        with col3:
            sodio = st.number_input("🧂 Sódio (mg)", 
                0.0, 5000.0, recipe_data[16] if recipe_data and recipe_data[16] else 0.0, step=1.0)
            
            colesterol = st.number_input("💔 Colesterol (mg)", 
                0.0, 1000.0, recipe_data[18] if recipe_data and recipe_data[18] else 0.0, step=1.0)
            
            calcular_automatico = st.checkbox("🧮 Calcular automaticamente", 
                help="Calcula baseado nos ingredientes (funcionalidade futura)")
        
        # Tags e categorização
        st.markdown("##### 🏷️ Tags e Categorização")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tags_receita = st.text_input("🏷️ Tags (separadas por vírgula)", 
                value=recipe_data[22] if recipe_data and recipe_data[22] else "",
                placeholder="Ex: saudável, rápido, econômico, vegetariano")
            
            receita_publica = st.checkbox("🌍 Tornar receita pública", 
                value=recipe_data[26] if recipe_data else False,
                help="Outras pessoas poderão ver e usar esta receita")
        
        with col2:
            observacoes_receita = st.text_area("📝 Observações e Dicas", 
                value="",
                height=100,
                placeholder="Dicas especiais, substituições possíveis, informações adicionais...")
        
        # Botões de submissão
        col1, col2, col3 = st.columns(3)
        
        with col1:
