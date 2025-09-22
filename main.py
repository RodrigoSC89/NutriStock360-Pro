<div style="color: {status_color}; font-weight: bold; font-size: 1.1rem;">
                            {status_icon} {status_text}
                        </div>
                        <div style="font-size: 1.2rem; margin: 0.5rem 0;">
                            {progress_percent:.0f}%
                        </div>
                        <div style="font-size: 0.9rem;">
                            {challenge['current_progress']:.1f}/{challenge['target_value']:.0f}
                        </div>
                    </div>
                </div>
                
                <div style="background: #ddd; border-radius: 10px; height: 15px; margin: 1rem 0;">
                    <div style="background: linear-gradient(45deg, {status_color}, {status_color}88); height: 100%; width: {progress_percent}%; border-radius: 10px; transition: width 0.3s ease;"></div>
                </div>
                
                {f'<p style="margin: 0; color: {status_color}; font-weight: bold;">🎉 Parabéns! Você ganhou {challenge["points_earned"]} pontos!</p>' if challenge['completed'] else ''}
            </div>
            """, unsafe_allow_html=True)
            
            # Ações para desafios em andamento
            if not challenge['completed'] and pd.to_datetime(challenge['end_date']).date() >= datetime.now().date():
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button(f"📈 Atualizar Progresso", key=f"update_{challenge['id']}"):
                        update_progress = st.number_input(
                            f"Novo progresso para {challenge['title']}", 
                            min_value=0.0, 
                            max_value=float(challenge['target_value']),
                            value=float(challenge['current_progress']),
                            step=0.1,
                            key=f"progress_input_{challenge['id']}"
                        )
                        
                        if st.button("✅ Confirmar", key=f"confirm_update_{challenge['id']}"):
                            cursor = conn.cursor()
                            
                            # Verificar se atingiu a meta
                            completed = update_progress >= challenge['target_value']
                            
                            if completed and not challenge['completed']:
                                # Conceder pontos
                                award_points(patient_id, challenge['points_reward'], 
                                           f"Desafio concluído: {challenge['title']}")
                                
                                cursor.execute("""
                                    UPDATE patient_challenges 
                                    SET current_progress = ?, completed = 1, completed_date = DATE('now'), points_earned = ?
                                    WHERE patient_id = ? AND challenge_id = ?
                                """, (update_progress, challenge['points_reward'], patient_id, challenge['id']))
                            else:
                                cursor.execute("""
                                    UPDATE patient_challenges 
                                    SET current_progress = ?
                                    WHERE patient_id = ? AND challenge_id = ?
                                """, (update_progress, patient_id, challenge['id']))
                            
                            conn.commit()
                            st.success("✅ Progresso atualizado!")
                            st.rerun()
                
                with col2:
                    if st.button(f"❓ Dicas", key=f"tips_{challenge['id']}"):
                        # Dicas baseadas no tipo de desafio
                        tips = get_challenge_tips(challenge['challenge_type'])
                        st.info(f"💡 **Dicas para {challenge['title']}:**\n\n{tips}")
    
    else:
        st.info("🎯 Você não possui desafios ativos no momento.")
    
    # Desafios concluídos
    completed_challenges = pd.read_sql_query("""
        SELECT c.title, c.description, pc.completed_date, pc.points_earned, c.challenge_type
        FROM patient_challenges pc
        JOIN challenges c ON pc.challenge_id = c.id
        WHERE pc.patient_id = ? AND pc.completed = 1
        ORDER BY pc.completed_date DESC
        LIMIT 10
    """, conn, params=[patient_id])
    
    if not completed_challenges.empty:
        st.markdown("### 🏆 Desafios Concluídos")
        
        total_points_earned = completed_challenges['points_earned'].sum()
        st.success(f"🎯 Total de pontos ganhos em desafios: {total_points_earned}")
        
        for _, challenge in completed_challenges.iterrows():
            type_icons = {
                'streak': '🔥',
                'weight_loss': '⚖️',
                'hydration': '💧',
                'exercise': '🏃',
                'nutrition': '🥗'
            }
            type_icon = type_icons.get(challenge['challenge_type'], '🎯')
            
            st.markdown(f"""
            <div style="background: #E8F5E8; padding: 1rem; border-radius: 10px; border-left: 4px solid #4CAF50; margin: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h5 style="margin: 0; color: #2E7D32;">{type_icon} {challenge['title']}</h5>
                        <p style="margin: 0.5rem 0; font-size: 0.9rem;">{challenge['description']}</p>
                        <small>📅 Concluído em: {challenge['completed_date']}</small>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #4CAF50; font-weight: bold; font-size: 1.1rem;">
                            ✅ Concluído
                        </div>
                        <div style="color: #4CAF50; font-weight: bold;">
                            +{challenge['points_earned']} pts
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Estatísticas pessoais
    st.markdown("### 📊 Minhas Estatísticas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_challenges = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM patient_challenges WHERE patient_id = ?
        """, conn, params=[patient_id]).iloc[0]['count']
        st.metric("🎯 Total Participações", total_challenges)
    
    with col2:
        completed_count = completed_challenges.shape[0] if not completed_challenges.empty else 0
        completion_rate = (completed_count / total_challenges * 100) if total_challenges > 0 else 0
        st.metric("✅ Taxa de Sucesso", f"{completion_rate:.1f}%")
    
    with col3:
        current_streak = pd.read_sql_query("""
            SELECT streak_days FROM patient_points WHERE patient_id = ?
        """, conn, params=[patient_id])
        streak = current_streak.iloc[0]['streak_days'] if not current_streak.empty else 0
        st.metric("🔥 Sequência Atual", f"{streak} dias")
    
    with col4:
        if not completed_challenges.empty:
            st.metric("🏆 Pontos Ganhos", total_points_earned)
        else:
            st.metric("🏆 Pontos Ganhos", "0")
    
    conn.close()

def get_challenge_tips(challenge_type):
    """Retorna dicas baseadas no tipo de desafio"""
    tips = {
        'streak': """
        • Crie uma rotina diária consistente
        • Use lembretes no celular
        • Celebrate pequenas vitórias
        • Tenha um plano B para dias difíceis
        • Encontre um parceiro de accountability
        """,
        'weight_loss': """
        • Pese-se sempre no mesmo horário
        • Foque na consistência, não na perfeição
        • Combine alimentação saudável com exercícios
        • Beba muita água
        • Tenha paciência - resultados levam tempo
        """,
        'hydration': """
        • Tenha sempre uma garrafa de água por perto
        • Use apps para lembrar de beber água
        • Adicione limão ou hortelã para variar o sabor
        • Beba um copo ao acordar
        • Monitore a cor da urina como indicador
        """,
        'exercise': """
        • Comece devagar e aumente gradualmente
        • Encontre atividades que você goste
        • Programe exercícios na sua agenda
        • Tenha roupas e equipamentos prontos
        • Celebre cada sessão concluída
        """,
        'nutrition': """
        • Planeje refeições com antecedência
        • Mantenha lanches saudáveis disponíveis
        • Leia rótulos dos alimentos
        • Cozinhe mais em casa
        • Pratique mindful eating
        """
    }
    return tips.get(challenge_type, "Continue se esforçando! Você consegue!")

def show_recipes_patient():
    """Receitas para pacientes"""
    st.markdown('<h1 class="main-header">🍳 Receitas Saudáveis</h1>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox("🏷️ Categoria", [
            "Todas", "Café da manhã", "Almoço", "Jantar", "Lanche", 
            "Saladas", "Pratos principais", "Bebidas", "Sobremesas"
        ])
    
    with col2:
        difficulty_filter = st.selectbox("📊 Dificuldade", ["Todas", "Fácil", "Médio", "Difícil"])
    
    with col3:
        prep_time_filter = st.selectbox("⏰ Tempo de Preparo", [
            "Qualquer", "Até 15 min", "15-30 min", "30-60 min", "Mais de 1h"
        ])
    
    # Busca
    search_term = st.text_input("🔍 Buscar receitas", placeholder="Digite ingredientes ou nome da receita...")
    
    # Query das receitas
    query = "SELECT * FROM recipes WHERE is_public = 1"
    params = []
    
    if category_filter != "Todas":
        query += " AND category = ?"
        params.append(category_filter)
    
    if difficulty_filter != "Todas":
        query += " AND difficulty = ?"
        params.append(difficulty_filter)
    
    if prep_time_filter != "Qualquer":
        if prep_time_filter == "Até 15 min":
            query += " AND prep_time <= 15"
        elif prep_time_filter == "15-30 min":
            query += " AND prep_time BETWEEN 16 AND 30"
        elif prep_time_filter == "30-60 min":
            query += " AND prep_time BETWEEN 31 AND 60"
        else:
            query += " AND prep_time > 60"
    
    if search_term:
        query += " AND (name LIKE ? OR ingredients LIKE ? OR tags LIKE ?)"
        search_param = f"%{search_term}%"
        params.extend([search_param, search_param, search_param])
    
    query += " ORDER BY name"
    
    recipes = pd.read_sql_query(query, conn, params=params)
    
    if not recipes.empty:
        st.write(f"📊 Encontradas {len(recipes)} receitas")
        
        # Grid de receitas
        cols = st.columns(2)
        
        for i, (_, recipe) in enumerate(recipes.iterrows()):
            with cols[i % 2]:
                # Card da receita
                difficulty_colors = {"Fácil": "#4CAF50", "Médio": "#FF9800", "Difícil": "#F44336"}
                difficulty_color = difficulty_colors.get(recipe['difficulty'], "#9E9E9E")
                
                st.markdown(f"""
                <div class="recipe-card">
                    <h4 style="margin: 0; color: #E65100;">{recipe['name']}</h4>
                    <p style="margin: 0.5rem 0; font-size: 0.9rem; color: #666;">
                        🏷️ {recipe['category']} | 
                        ⏰ {recipe['prep_time'] + recipe['cook_time']} min total |
                        👥 {recipe['servings']} porções
                    </p>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 0.5rem 0;">
                        <span style="background: {difficulty_color}; color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">
                            {recipe['difficulty']}
                        </span>
                        <span style="font-weight: bold; color: #2E7D32;">
                            🔥 {recipe['calories_per_serving']} kcal/porção
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Expandir para ver detalhes
                with st.expander("Ver receita completa"):
                    # Informações nutricionais
                    col_a, col_b, col_c, col_d = st.columns(4)
                    with col_a:
                        st.metric("🥩 Proteína", f"{recipe['protein']}g")
                    with col_b:
                        st.metric("🍞 Carboidrato", f"{recipe['carbs']}g")
                    with col_c:
                        st.metric("🥑 Gordura", f"{recipe['fat']}g")
                    with col_d:
                        st.metric("🌾 Fibra", f"{recipe['fiber']}g")
                    
                    # Ingredientes
                    st.markdown("**🛒 Ingredientes:**")
                    ingredients_list = recipe['ingredients'].split('\n') if recipe['ingredients'] else []
                    for ingredient in ingredients_list:
                        if ingredient.strip():
                            st.write(f"• {ingredient.strip()}")
                    
                    # Modo de preparo
                    st.markdown("**👨‍🍳 Modo de Preparo:**")
                    instructions = recipe['instructions'].split('\n') if recipe['instructions'] else []
                    for i, instruction in enumerate(instructions, 1):
                        if instruction.strip():
                            st.write(f"{i}. {instruction.strip()}")
                    
                    # Tags
                    if recipe['tags']:
                        st.markdown("**🏷️ Tags:**")
                        tags = recipe['tags'].split(',')
                        tag_html = " ".join([f'<span class="badge">{tag.strip()}</span>' for tag in tags])
                        st.markdown(tag_html, unsafe_allow_html=True)
                    
                    # Botões de ação
                    col_x, col_y, col_z = st.columns(3)
                    with col_x:
                        if st.button("❤️ Favoritar", key=f"fav_{recipe['id']}"):
                            st.success("Receita adicionada aos favoritos!")
                    with col_y:
                        if st.button("📱 Compartilhar", key=f"share_{recipe['id']}"):
                            st.success("Link copiado para compartilhamento!")
                    with col_z:
                        if st.button("📋 Adicionar ao Plano", key=f"plan_{recipe['id']}"):
                            st.success("Receita sugerida ao seu nutricionista!")
    else:
        st.warning("🔍 Nenhuma receita encontrada com os filtros aplicados.")
    
    # Receitas favoritas (simuladas)
    st.markdown("### ❤️ Suas Receitas Favoritas")
    
    favorite_recipes = ["Salada de Quinoa com Legumes", "Smoothie Verde Detox", "Salmão Grelhado com Aspargos"]
    
    if favorite_recipes:
        cols = st.columns(len(favorite_recipes))
        for i, recipe_name in enumerate(favorite_recipes):
            with cols[i]:
                st.markdown(f"""
                <div style="background: #FFF3E0; padding: 1rem; border-radius: 8px; text-align: center; border: 2px solid #FF9800;">
                    <h5 style="margin: 0; color: #E65100;">❤️ {recipe_name}</h5>
                    <p style="margin: 0.5rem 0; font-size: 0.8rem;">Clique para ver detalhes</p>
                </div>
                """, unsafe_allow_html=True)
    
    conn.close()

def show_notifications():
    """Notificações do paciente"""
    st.markdown('<h1 class="main-header">🔔 Minhas Notificações</h1>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar notificações do paciente
    user_id = st.session_state.user['id']
    
    notifications = pd.read_sql_query("""
        SELECT * FROM notifications 
        WHERE recipient_id = ? AND recipient_type = 'patient'
        ORDER BY sent_date DESC
    """, conn, params=[user_id])
    
    if not notifications.empty:
        # Estatísticas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_notifications = len(notifications)
            st.metric("📧 Total", total_notifications)
        
        with col2:
            unread_count = len(notifications[notifications['read_status'] == 0])
            st.metric("🆕 Não Lidas", unread_count)
        
        with col3:
            today_notifications = len(notifications[notifications['sent_date'].str.startswith(datetime.now().strftime('%Y-%m-%d'))])
            st.metric("📅 Hoje", today_notifications)
        
        # Filtro de tipo
        notification_types = ["Todas"] + notifications['notification_type'].unique().tolist()
        selected_type = st.selectbox("🏷️ Filtrar por tipo", notification_types)
        
        # Filtrar notificações
        filtered_notifications = notifications.copy()
        if selected_type != "Todas":
            filtered_notifications = notifications[notifications['notification_type'] == selected_type]
        
        # Botão para marcar todas como lidas
        if unread_count > 0:
            if st.button("✅ Marcar todas como lidas"):
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE notifications 
                    SET read_status = 1, read_date = CURRENT_TIMESTAMP
                    WHERE recipient_id = ? AND recipient_type = 'patient' AND read_status = 0
                """, (user_id,))
                conn.commit()
                st.success("✅ Todas as notificações foram marcadas como lidas!")
                st.rerun()
        
        # Lista de notificações
        st.markdown("### 📋 Lista de Notificações")
        
        for _, notification in filtered_notifications.iterrows():
            # Ícones por tipo
            type_icons = {
                'achievement': '🏆',
                'reminder': '⏰',
                'badge': '🏅',
                'points': '🎯',
                'appointment': '📅',
                'plan': '📋',
                'general': '📢'
            }
            
            icon = type_icons.get(notification['notification_type'], '📢')
            
            # Cor baseada na prioridade e status de leitura
            if notification['read_status'] == 0:
                if notification['priority'] == 'high':
                    bg_color = "#FFEBEE"
                    border_color = "#F44336"
                elif notification['priority'] == 'normal':
                    bg_color = "#E3F2FD"
                    border_color = "#2196F3"
                else:
                    bg_color = "#F3E5F5"
                    border_color = "#9C27B0"
                opacity = "1"
                font_weight = "bold"
            else:
                bg_color = "#F5F5F5"
                border_color = "#BDBDBD"
                opacity = "0.7"
                font_weight = "normal"
            
            st.markdown(f"""
            <div style="background: {bg_color}; padding: 1rem; border-radius: 10px; 
                        border-left: 4px solid {border_color}; margin: 0.5rem 0; opacity: {opacity};">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <h5 style="margin: 0; font-weight: {font_weight}; color: #333;">
                            {icon} {notification['title']}
                        </h5>
                        <p style="margin: 0.5rem 0; color: #666;">{notification['message']}</p>
                        <small style="color: #999;">
                            📅 {notification['sent_date']} | 
                            🏷️ {notification['notification_type'].title()} |
                            📊 {notification['priority'].title()}
                        </small>
                    </div>
                    <div style="margin-left: 1rem;">
                        {f'<span style="background: #4CAF50; color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">✅ Lida</span>' if notification['read_status'] == 1 else f'<span style="background: #FF9800; color: white; padding: 0.2rem 0.5rem; border-radius: 12px; font-size: 0.8rem;">🆕 Nova</span>'}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Ações para notificações não lidas
            if notification['read_status'] == 0:
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button("👁️ Marcar como lida", key=f"read_{notification['id']}"):
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE notifications 
                            SET read_status = 1, read_date = CURRENT_TIMESTAMP
                            WHERE id = ?
                        """, (notification['id'],))
                        conn.commit()
                        st.success("✅ Notificação marcada como lida!")
                        st.rerun()
    
    else:
        st.info("📭 Nenhuma notificação encontrada.")
        
        # Configurações de notificação
        st.markdown("### ⚙️ Configurações de Notificação")
        
        st.markdown("""
        <div class="info-card">
            <h4>🔔 Tipos de Notificação Disponíveis</h4>
            <ul>
                <li>🏆 <strong>Conquistas:</strong> Badges e metas atingidas</li>
                <li>⏰ <strong>Lembretes:</strong> Consultas e atividades</li>
                <li>🎯 <strong>Pontos:</strong> Pontuações e níveis</li>
                <li>📅 <strong>Agendamentos:</strong> Consultas marcadas/canceladas</li>
                <li>📋 <strong>Planos:</strong> Atualizações no plano alimentar</li>
                <li>📢 <strong>Gerais:</strong> Informações importantes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Preferências (simuladas)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📧 Notificações por Email:**")
            st.checkbox("Conquistas e badges", value=True)
            st.checkbox("Lembretes de consulta", value=True)
            st.checkbox("Atualizações do plano", value=False)
        
        with col2:
            st.markdown("**📱 Notificações Push:**")
            st.checkbox("Lembretes diários", value=True)
            st.checkbox("Marcos de progresso", value=True)
            st.checkbox("Mensagens do nutricionista", value=True)
    
    conn.close()

def show_profile():
    """Perfil do paciente"""
    st.markdown('<h1 class="main-header">👤 Meu Perfil</h1>', unsafe_allow_html=True)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Encontrar dados do paciente
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM patients WHERE email = ?", (st.session_state.user['email'],))
    patient_data = cursor.fetchone()
    
    if not patient_data:
        st.error("❌ Dados do paciente não encontrados.")
        return
    
    patient_id = patient_data[0]
    
    # Buscar informações completas
    patient_info = pd.read_sql_query("""
        SELECT * FROM patients WHERE id = ?
    """, conn, params=[patient_id]).iloc[0]
    
    # Tabs do perfil
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Dados Pessoais", "📊 Estatísticas", "🎯 Objetivos", "⚙️ Configurações"])
    
    with tab1:
        show_personal_data(patient_info, patient_id, conn)
    
    with tab2:
        show_patient_statistics(patient_id, conn)
    
    with tab3:
        show_patient_goals(patient_info, patient_id, conn)
    
    with tab4:
        show_patient_settings(patient_id, conn)
    
    conn.close()

def show_personal_data(patient_info, patient_id, conn):
    """Dados pessoais do paciente"""
    st.markdown("### 📝 Informações Pessoais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="info-card">
            <h4 style="margin: 0;">👤 Dados Básicos</h4>
            <p style="margin: 0.5rem 0;"><strong>Nome:</strong> {patient_info['full_name']}</p>
            <p style="margin: 0.5rem 0;"><strong>Email:</strong> {patient_info['email']}</p>
            <p style="margin: 0.5rem 0;"><strong>Telefone:</strong> {patient_info['phone'] or 'Não informado'}</p>
            <p style="margin: 0.5rem 0;"><strong>Data de Nascimento:</strong> {patient_info['birth_date'] or 'Não informado'}</p>
            <p style="margin: 0;"><strong>Sexo:</strong> {'Feminino' if patient_info['gender'] == 'F' else 'Masculino' if patient_info['gender'] == 'M' else 'Não informado'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-card">
            <h4 style="margin: 0;">📏 Dados Físicos</h4>
            <p style="margin: 0.5rem 0;"><strong>Altura:</strong> {patient_info['height']}m</p>
            <p style="margin: 0.5rem 0;"><strong>Peso Atual:</strong> {patient_info['current_weight']}kg</p>
            <p style="margin: 0.5rem 0;"><strong>Peso Meta:</strong> {patient_info['target_weight']}kg</p>
            <p style="margin: 0;"><strong>Nível de Atividade:</strong> {patient_info['activity_level'] or 'Não informado'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Informações médicas
    st.markdown("### 🏥 Informações Médicas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="warning-card">
            <h5 style="margin: 0;">⚠️ Condições Médicas</h5>
            <p style="margin: 0.5rem 0;">{patient_info['medical_conditions'] or 'Nenhuma condição relatada'}</p>
        </div>
        """)
        
        st.markdown(f"""
        <div class="warning-card">
            <h5 style="margin: 0;">🚫 Alergias</h5>
            <p style="margin: 0.5rem 0;">{patient_info['allergies'] or 'Nenhuma alergia conhecida'}</p>
        </div>
        """)
    
    with col2:
        st.markdown(f"""
        <div class="success-card">
            <h5 style="margin: 0;">🥗 Preferências Alimentares</h5>
            <p style="margin: 0.5rem 0;">{patient_info['dietary_preferences'] or 'Nenhuma restrição específica'}</p>
        </div>
        """)
        
        # Data de cadastro
        st.markdown(f"""
        <div class="info-card">
            <h5 style="margin: 0;">📅 Histórico</h5>
            <p style="margin: 0.5rem 0;"><strong>Cadastro:</strong> {patient_info['created_at'][:10]}</p>
            <p style="margin: 0;"><strong>Última atualização:</strong> {patient_info['updated_at'][:10]}</p>
        </div>
        """)
    
    # Botão para editar dados
    if st.button("✏️ Solicitar Atualização de Dados"):
        st.info("📧 Solicitação enviada ao seu nutricionista. Suas informações serão atualizadas na próxima consulta.")

def show_patient_statistics(patient_id, conn):
    """Estatísticas do paciente"""
    st.markdown("### 📊 Suas Estatísticas")
    
    # Estatísticas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    # Total de consultas
    total_appointments = pd.read_sql_query("""
        SELECT COUNT(*) as count FROM appointments WHERE patient_id = ?
    """, conn, params=[patient_id]).iloc[0]['count']
    
    with col1:
        st.metric("📅 Total de Consultas", total_appointments)
    
    # Pontos e nível
    points_data = pd.read_sql_query("""
        SELECT points, level, total_points, streak_days FROM patient_points WHERE patient_id = ?
    """, conn, params=[patient_id])
    
    if not points_data.empty:
        points_info = points_data.iloc[0]
        
        with col2:
            st.metric("🎯 Pontos Totais", points_info['total_points'])
        with col3:
            st.metric("⭐ Nível Atual", points_info['level'])
        with col4:
            st.metric("🔥 Sequência", f"{points_info['streak_days']} dias")
    
    # Gráfico de evolução de pontos
    st.markdown("#### 📈 Evolução de Pontos")
    
    # Simular histórico de pontos (normalmente viria de uma tabela de histórico)
    dates = pd.date_range(start='2024-09-01', end='2024-09-30', freq='D')
    points_evolution = pd.DataFrame({
        'date': dates,
        'cumulative_points': [50 + i*15 + random.randint(-10, 20) for i in range(len(dates))]
    })
    
    fig = px.line(points_evolution, x='date', y='cumulative_points',
                 title='Evolução dos Pontos Acumulados',
                 labels={'cumulative_points': 'Pontos Totais', 'date': 'Data'})
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Badges conquistados
    badges = pd.read_sql_query("""
        SELECT badge_name, badge_icon, earned_date, points_awarded
        FROM patient_badges 
        WHERE patient_id = ?
        ORDER BY earned_date DESC
    """, conn, params=[patient_id])
    
    if not badges.empty:
        st.markdown("#### 🏅 Histórico de Conquistas")
        
        for _, badge in badges.iterrows():
            st.markdown(f"""
            <div style="display: flex; align-items: center; background: #F3E5F5; padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0;">
                <span style="font-size: 1.5rem; margin-right: 1rem;">{badge['badge_icon']}</span>
                <div style="flex: 1;">
                    <strong>{badge['badge_name']}</strong><br>
                    <small>📅 {badge['earned_date']} • +{badge['points_awarded']} pontos</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Progresso de peso
    progress_data = pd.read_sql_query("""
        SELECT record_date, weight FROM patient_progress 
        WHERE patient_id = ? 
        ORDER BY record_date
    """, conn, params=[patient_id])
    
    if not progress_data.empty:
        st.markdown("#### ⚖️ Evolução do Peso")
        
        fig = px.line(progress_data, x='record_date', y='weight',
                     title='Histórico de Peso',
                     markers=True)
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Estatísticas de peso
        first_weight = progress_data.iloc[0]['weight']
        current_weight = progress_data.iloc[-1]['weight']
        weight_change = current_weight - first_weight
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏁 Peso Inicial", f"{first_weight:.1f}kg")
        with col2:
            st.metric("⚖️ Peso Atual", f"{current_weight:.1f}kg")
        with col3:
            st.metric("📉 Variação", f"{weight_change:+.1f}kg", 
                     delta=f"{weight_change:.1f}kg")

def show_patient_goals(patient_info, patient_id, conn):
    """Objetivos do paciente"""
    st.markdown("### 🎯 Meus Objetivos")
    
    # Objetivo principal de peso
    current_weight = patient_info['current_weight']
    target_weight = patient_info['target_weight']
    weight_diff = current_weight - target_weight
    
    progress_percent = max(0, min(100, (1 - abs(weight_diff) / max(abs(current_weight - target_weight), 1)) * 100))
    
    st.markdown(f"""
    <div class="success-card">
        <h4 style="margin: 0;">⚖️ Objetivo de Peso</h4>
        <p style="margin: 0.5rem 0;"><strong>Meta:</strong> {target_weight}kg</p>
        <p style="margin: 0.5rem 0;"><strong>Peso atual:</strong> {current_weight}kg</p>
        <p style="margin: 0.5rem 0;"><strong>Faltam:</strong> {abs(weight_diff):.1f}kg</p>
        <div style="background: #ddd; border-radius: 10px; height: 15px; margin: 0.5rem 0;">
            <div style="background: #4CAF50; height: 100%; width: {progress_percent}%; border-radius: 10px;"></div>
        </div>
        <p style="margin: 0; text-align: right;">{progress_percent:.0f}% do objetivo</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Objetivos de curto prazo
    st.markdown("#### 📅 Objetivos de Curto Prazo")
    
    short_term_goals = [
        {"goal": "Perder 1kg este mês", "progress": 60, "deadline": "31/10/2024"},
        {"goal": "Beber 2L de água por dia", "progress": 85, "deadline": "Diário"},
        {"goal": "Exercitar-se 3x por semana", "progress": 75, "deadline": "Semanal"},
        {"goal": "Seguir o plano alimentar", "progress": 90, "deadline": "Diário"}
    ]
    
    for goal in short_term_goals:
        color = "#4CAF50" if goal['progress'] >= 80 else "#FF9800" if goal['progress'] >= 60 else "#F44336"
        
        st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid {color}; margin: 0.5rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{goal['goal']}</strong><br>
                    <small>📅 {goal['deadline']}</small>
                </div>
                <div style="text-align: right;">
                    <span style="color: {color}; font-weight: bold; font-size: 1.1rem;">{goal['progress']}%</span>
                </div>
            </div>
            <div style="background: #ddd; border-radius: 10px; height: 8px; margin: 0.5rem 0;">
                <div style="background: {color}; height: 100%; width: {goal['progress']}%; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Objetivos de longo prazo
    st.markdown("#### 🎯 Objetivos de Longo Prazo")
    
    long_term_goals = [
        "Manter peso ideal por 6 meses",
        "Melhorar exames de sangue",
        "Aumentar massa muscular",
        "Adotar estilo de vida saudável permanente"
    ]
    
    for goal in long_term_goals:
        st.markdown(f"""
        <div style="background: #E3F2FD; padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0;">
            🎯 {goal}
        </div>
        """, unsafe_allow_html=True)
    
    # Sugestão de novos objetivos
    st.markdown("#### ➕ Definir Novo Objetivo")
    
    with st.form("new_goal_form"):
        new_goal = st.text_input("🎯 Descreva seu objetivo", placeholder="Ex: Correr 5km sem parar")
        goal_deadline = st.date_input("📅 Prazo desejado", value=date.today() + timedelta(days=30))
        goal_category = st.selectbox("🏷️ Categoria", ["Peso", "Exercício", "Alimentação", "Hábitos", "Outros"])
        
        if st.form_submit_button("💾 Definir Objetivo"):
            if new_goal:
                st.success("🎯 Objetivo definido! Seu nutricionista será notificado e poderá incluí-lo no seu plano.")
            else:
                st.warning("⚠️ Por favor, descreva seu objetivo.")

def show_patient_settings(patient_id, conn):
    """Configurações do paciente"""
    st.markdown("### ⚙️ Configurações da Conta")
    
    # Configurações de notificação
    st.markdown("#### 🔔 Notificações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📧 Email:**")
        email_achievements = st.checkbox("Conquistas e badges", value=True)
        email_reminders = st.checkbox("Lembretes de consulta", value=True)
        email_progress = st.checkbox("Relatórios de progresso", value=False)
        email_tips = st.checkbox("Dicas nutricionais", value=True)
    
    with col2:
        st.markdown("**📱 Push/SMS:**")
        push_daily = st.checkbox("Lembretes diários", value=True)
        push_appointments = st.checkbox("Consultas próximas", value=True)
        push_goals = st.checkbox("Metas atingidas", value=True)
        push_challenges = st.checkbox("Novos desafios", value=False)
    
    # Configurações de privacidade
    st.markdown("#### 🔒 Privacidade")
    
    privacy_ranking = st.checkbox("Aparecer no ranking público", value=True, 
                                help="Permite que outros pacientes vejam seu progresso no ranking")
    privacy_share = st.checkbox("Permitir compartilhamento de progresso", value=False,
                              help="Permite que o nutricionista compartilhe seu sucesso (anonimamente)")
    
    # Configurações de interface
    st.markdown("#### 🎨 Interface")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.selectbox("🎨 Tema", ["Claro", "Escuro", "Automático"])
        language = st.selectbox("🌍 Idioma", ["Português", "English", "Español"])
    
    with col2:
        units = st.selectbox("📏 Sistema de Medidas", ["Métrico (kg, cm)", "Imperial (lb, in)"])
        date_format = st.selectbox("📅 Formato de Data", ["DD/MM/AAAA", "MM/DD/AAAA", "AAAA-MM-DD"])
    
    # Exportar dados
    st.markdown("#### 📊 Exportar Dados")
    
    st.info("📋 Você pode solicitar uma cópia dos seus dados pessoais e progresso a qualquer momento.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Relatório Completo"):
            st.success("📧 Relatório completo será enviado por email em até 24h")
    
    with col2:
        if st.button("📊 Dados de Progresso"):
            st.success("📊 Planilha com dados de progresso baixada!")
    
    with col3:
        if st.button("🏆 Histórico de Conquistas"):
            st.success("🏆 PDF com histórico de conquistas baixado!")
    
    # Suporte
    st.markdown("#### 🆘 Suporte")
    
    st.markdown(f"""
    <div class="info-card">
        <h5 style="margin: 0;">📞 Contatos de Suporte</h5>
        <p style="margin: 0.5rem 0;"><strong>Nutricionista:</strong> Dr(a). Nome do Nutricionista</p>
        <p style="margin: 0.5rem 0;"><strong>Telefone:</strong> (11) 99999-9999</p>
        <p style="margin: 0.5rem 0;"><strong>Email:</strong> nutricionista@clinica.com</p>
        <p style="margin: 0;"><strong>Horário:</strong> Segunda a Sexta, 8h às 18h</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Salvar configurações
    if st.button("💾 Salvar Configurações", type="primary"):
        st.success("✅ Configurações salvas com sucesso!")

# =============================================================================
# CALCULADORAS NUTRICIONAIS EXPANDIDAS
# =============================================================================

def show_calculators():
    """Calculadoras nutricionais expandidas"""
    st.markdown('<h1 class="main-header">🧮 Calculadoras Nutricionais</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 TMB & GET", "🥗 Macros", "💧 Hidratação", "🏃 Exercício", "📏 Antropometria"])
    
    with tab1:
        show_metabolism_calculators()
    
    with tab2:
        show_macro_calculator()
    
    with tab3:
        show_hydration_calculator()
    
    with tab4:
        show_exercise_calculator()
    
    with tab5:
        show_anthropometry_calculator()

def show_metabolism_calculators():
    """Calculadoras de metabolismo"""
    st.markdown("### 📊 Taxa Metabólica Basal (TMB) e Gasto Energético Total (GET)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Dados do Paciente")
        age = st.number_input("👤 Idade (anos)", min_value=10, max_value=100, value=30)
        weight = st.number_input("⚖️ Peso (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
        height = st.number_input("📏 Altura (cm)", min_value=100, max_value=250, value=170)
        gender = st.selectbox("👤 Sexo", ["Feminino", "Masculino"])
        
        # Fórmulas disponíveis
        formula = st.selectbox("🧮 Fórmula", [
            "Harris-Benedict Revisada",
            "Mifflin-St Jeor", 
            "Katch-McArdle",
            "Cunningham"
        ])
        
        if formula in ["Katch-McArdle", "Cunningham"]:
            body_fat = st.number_input("📊 Percentual de Gordura (%)", min_value=5.0, max_value=50.0, value=20.0)
        
        # Nível de atividade
        activity_level = st.selectbox("🏃 Nível de Atividade", [
            "Sedentário (pouco ou nenhum exercício)",
            "Levemente ativo (exercício leve 1-3 dias/semana)",
            "Moderadamente ativo (exercício moderado 3-5 dias/semana)",
            "Muito ativo (exercício pesado 6-7 dias/semana)",
            "Extremamente ativo (exercício muito pesado, trabalho físico)"
        ])
    
    with col2:
        if st.button("🧮 Calcular", type="primary"):
            # Fatores de atividade
            activity_factors = {
                "Sedentário (pouco ou nenhum exercício)": 1.2,
                "Levemente ativo (exercício leve 1-3 dias/semana)": 1.375,
                "Moderadamente ativo (exercício moderado 3-5 dias/semana)": 1.55,
                "Muito ativo (exercício pesado 6-7 dias/semana)": 1.725,
                "Extremamente ativo (exercício muito pesado, trabalho físico)": 1.9
            }
            
            factor = activity_factors[activity_level]
            
            # Cálculo da TMB
            if formula == "Harris-Benedict Revisada":
                if gender == "Masculino":
                    tmb = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
                else:
                    tmb = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            
            elif formula == "Mifflin-St Jeor":
                if gender == "Masculino":
                    tmb = (10 * weight) + (6.25 * height) - (5 * age) + 5
                else:
                    tmb = (10 * weight) + (6.25 * height) - (5 * age) - 161
            
            elif formula == "Katch-McArdle":
                lean_mass = weight * (1 - body_fat/100)
                tmb = 370 + (21.6 * lean_mass)
            
            else:  # Cunningham
                lean_mass = weight * (1 - body_fat/100)
                tmb = 500 + (22 * lean_mass)
            
            get = tmb * factor
            
            # Resultados
            st.markdown(f"""
            <div class="success-card">
                <h4 style="margin: 0;">📊 Resultados</h4>
                <p style="margin: 0.5rem 0;"><strong>TMB:</strong> {tmb:.0f} kcal/dia</p>
                <p style="margin: 0.5rem 0;"><strong>GET:</strong> {get:.0f} kcal/dia</p>
                <p style="margin: 0;"><strong>Fórmula utilizada:</strong> {formula}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Objetivos calóricos
            st.markdown("#### 🎯 Objetivos Calóricos")
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.metric("📉 Perda de Peso", f"{get - 500:.0f} kcal/dia", 
                         delta="-500 kcal (-0,5kg/semana)")
            
            with col_b:
                st.metric("⚖️ Manutenção", f"{get:.0f} kcal/dia", 
                         delta="Peso estável")
            
            with col_c:
                st.metric("📈 Ganho de Peso", f"{get + 300:.0f} kcal/dia", 
                         delta="+300 kcal (+0,3kg/semana)")
            
            # Interpretação
            bmi = weight / ((height/100) ** 2)
            
            st.markdown("#### 📋 Interpretação e Recomendações")
            
            st.markdown(f"""
            <div class="info-card">
                <p><strong>📊 IMC:</strong> {bmi:.1f} kg/m² - {get_bmi_classification(bmi)}</p>
                <p><strong>💡 Recomendações:</strong></p>
                <ul>
                    <li>Para perda de peso saudável: {get - 300:.0f} a {get - 500:.0f} kcal/dia</li>
                    <li>Déficit máximo recomendado: {get * 0.8:.0f} kcal/dia</li>
                    <li>Consumo mínimo seguro: {1200 if gender == 'Feminino' else 1500} kcal/dia</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

def get_bmi_classification(bmi):
    """Classificação do IMC"""
    if bmi < 18.5:
        return "Abaixo do peso"
    elif bmi < 25:
        return "Peso normal"
    elif bmi < 30:
        return "Sobrepeso"
    elif bmi < 35:
        return "Obesidade grau I"
    elif bmi < 40:
        return "Obesidade grau II"
    else:
        return "Obesidade grau III"

def show_macro_calculator():
    """Calculadora de macronutrientes"""
    st.markdown("### 🥗 Calculadora de Macronutrientes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Configuração")
        total_calories = st.number_input("🔥 Calorias Totais", min_value=800, max_value=5000, value=2000)
        
        approach = st.selectbox("📋 Abordagem", [
            "Padrão Balanceado",
            "Low Carb",
            "High Protein",
            "Atleta Endurance",
            "Personalizado"
        ])
        
        if approach == "Personalizado":
            carb_percent = st.slider("🍞 Carboidratos (%)", 10, 70, 50)
            protein_percent = st.slider("🥩 Proteínas (%)", 10, 40, 25)
            fat_percent = 100 - carb_percent - protein_percent
            st.write(f"🥑 Gorduras: {fat_percent}%")
        else:
            # Distribuições pré-definidas
            distributions = {
                "Padrão Balanceado": (50, 25, 25),
                "Low Carb": (20, 30, 50),
                "High Protein": (40, 35, 25),
                "Atleta Endurance": (60, 20, 20)
            }
            carb_percent, protein_percent, fat_percent = distributions[approach]
        
        # Mostrar distribuição
        st.markdown(f"""
        <div class="info-card">
            <h5>📊 Distribuição Selecionada:</h5>
            <p>🍞 Carboidratos: {carb_percent}%</p>
            <p>🥩 Proteínas: {protein_percent}%</p>
            <p>🥑 Gorduras: {fat_percent}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Cálculos
        carb_calories = total_calories * carb_percent / 100
        protein_calories = total_calories * protein_percent / 100
        fat_calories = total_calories * fat_percent / 100
        
        carb_grams = carb_calories / 4
        protein_grams = protein_calories / 4
        fat_grams = fat_calories / 9
        
        st.markdown("#### 📋 Resultados")
        
        # Métricas
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("🍞 Carboidratos", f"{carb_grams:.0f}g", 
                     delta=f"{carb_calories:.0f} kcal")
        
        with col_b:
            st.metric("🥩 Proteínas", f"{protein_grams:.0f}g", 
                     delta=f"{protein_calories:.0f} kcal")
        
        with col_c:
            st.metric("🥑 Gorduras", f"{fat_grams:.0f}g", 
                     delta=f"{fat_calories:.0f} kcal")
        
        # Gráfico de pizza
        fig = px.pie(
            values=[carb_calories, protein_calories, fat_calories],
            names=['Carboidratos', 'Proteínas', 'Gorduras'],
            title='Distribuição Calórica',
            color_discrete_sequence=['#FF9800', '#4CAF50', '#2196F3']
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Equivalências
        st.markdown("#### 🍽️ Equivalências Alimentares")
        
        st.markdown(f"""
        <div class="success-card">
            <h5>📝 Exemplos de Fontes:</h5>
            <p><strong>🍞 Carboidratos ({carb_grams:.0f}g):</strong></p>
            <ul>
                <li>{carb_grams/50:.1f} xícaras de arroz cozido</li>
                <li>{carb_grams/25:.1f} fatias de pão integral</li>
                <li>{carb_grams/15:.1f} bananas médias</li>
            </ul>
            
            <p><strong>🥩 Proteínas ({protein_grams:.0f}g):</strong></p>
            <ul>
                <li>{protein_grams/25:.1f} filés de frango (100g)</li>
                <li>{protein_grams/20:.1f} ovos grandes</li>
                <li>{protein_grams/8:.1f} copos de leite</li>
            </ul>
            
            <p><strong>🥑 Gorduras ({fat_grams:.0f}g):</strong></p>
            <ul>
                <li>{fat_grams/14:.1f} colheres de azeite</li>
                <li>{fat_grams/15:.1f} abacates pequenos</li>
                <li>{fat_grams/6:.1f} colheres de amendoim</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_hydration_calculator():
    """Calculadora de hidratação"""
    st.markdown("### 💧 Calculadora de Hidratação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Dados para Cálculo")
        weight = st.number_input("⚖️ Peso (kg)", min_value=30.0, max_value=200.0, value=70.0)
        age = st.number_input("👤 Idade (anos)", min_value=10, max_value=100, value=30)
        activity_level = st.selectbox("🏃 Nível de Atividade", [
            "Sedentário",
            "Levemente ativo",
            "Moderadamente ativo", 
            "Muito ativo",
            "Atleta"
        ])
        
        climate = st.selectbox("🌡️ Clima", [
            "Temperado (20-25°C)",
            "Quente (25-30°C)",
            "Muito quente (>30°C)",
            "Frio (<20°C)"
        ])
        
        # Condições especiais
        st.markdown("#### ⚕️ Condições Especiais")
        fever = st.checkbox("🤒 Febre")
        diarrhea = st.checkbox("💩 Diarreia")
        pregnancy = st.checkbox("🤱 Gravidez")
        breastfeeding = st.checkbox("🍼 Amamentação")
    
    with col2:
        # Cálculo base
        base_hydration = weight * 35  # 35ml por kg
        
        # Ajustes por atividade
        activity_multipliers = {
            "Sedentário": 1.0,
            "Levemente ativo": 1.1,
            "Moderadamente ativo": 1.2,
            "Muito ativo": 1.4,
            "Atleta": 1.6
        }
        
        # Ajustes por clima
        climate_multipliers = {
            "Frio (<20°C)": 0.9,
            "Temperado (20-25°C)": 1.0,
            "Quente (25-30°C)": 1.2,
            "Muito quente (>30°C)": 1.5
        }
        
        total_hydration = base_hydration * activity_multipliers[activity_level] * climate_multipliers[climate]
        
        # Ajustes especiais
        if fever:
            total_hydration *= 1.13  # +13% para cada grau de febre
        if diarrhea:
            total_hydration += 500  # +500ml
        if pregnancy:
            total_hydration += 300  # +300ml
        if breastfeeding:
            total_hydration += 700  # +700ml
        
        # Resultados
        st.markdown("#### 💧 Recomendação de Hidratação")
        
        st.metric("💧 Total Diário", f"{total_hydration:.0f} ml", 
                 delta=f"{total_hydration/250:.1f} copos (250ml)")
        
        # Distribuição ao longo do dia
        st.markdown("#### ⏰ Distribuição Recomendada")
        
        distribution = {
            "Ao acordar": total_hydration * 0.15,
            "Manhã": total_hydration * 0.25,
            "Almoço": total_hydration * 0.20,
            "Tarde": total_hydration * 0.25,
            "Noite": total_hydration * 0.15
        }
        
        for period, amount in distribution.items():
            st.write(f"🕐 **{period}:** {amount:.0f}ml ({amount/250:.1f} copos)")
        
        # Dicas
        st.markdown("#### 💡 Dicas de Hidratação")
        
        tips = [
            "🌅 Beba um copo de água ao acordar",
            "⏰ Use lembretes no celular a cada 2 horas",
            "🍋 Adicione limão ou hortelã para variar o sabor",
            "🚰 Tenha sempre uma garrafa por perto",
            "🥗 Consuma alimentos ricos em água (frutas, sopas)",
            "☕ Limite cafeína que pode desidratar",
            "🏃 Aumente a ingestão antes, durante e após exercícios",
            "🌡️ Monitore a cor da urina como indicador"
        ]
        
        for tip in tips:
            st.write(f"• {tip}")

def show_exercise_calculator():
    """Calculadora de exercícios"""
    st.markdown("### 🏃 Calculadora de Gasto Energético em Exercícios")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Dados Pessoais")
        weight = st.number_input("⚖️ Peso (kg)", min_value=30.0, max_value=200.0, value=70.0)
        duration = st.number_input("⏰ Duração (minutos)", min_value=1, max_value=480, value=30)
        
        exercise_type = st.selectbox("🏃 Tipo de Exercício", [
            "Caminhada leve (4 km/h)",
            "Caminhada rápida (6 km/h)",
            "Corrida leve (8 km/h)",
            "Corrida moderada (10 km/h)",
            "Corrida intensa (12 km/h)",
            "Ciclismo leve (16 km/h)",
            "Ciclismo moderado (20 km/h)",
            "Ciclismo intenso (25 km/h)",
            "Natação moderada",
            "Natação intensa",
            "Musculação moderada",
            "Musculação intensa",
            "Futebol",
            "Basquete",
            "Tênis",
            "Yoga",
            "Pilates",
            "Dança",
            "Boxe",
            "Crossfit"
        ])
    
    with col2:
        # METs (Metabolic Equivalent of Task) para cada atividade
        mets = {
            "Caminhada leve (4 km/h)": 3.5,
            "Caminhada rápida (6 km/h)": 4.5,
            "Corrida leve (8 km/h)": 8.0,
            "Corrida moderada (10 km/h)": 10.0,
            "Corrida intensa (12 km/h)": 12.5,
            "Ciclismo leve (16 km/h)": 6.0,
            "Ciclismo moderado (20 km/h)": 8.0,
            "Ciclismo intenso (25 km/h)": 12.0,
            "Natação moderada": 8.0,
            "Natação intensa": 11.0,
            "Musculação moderada": 3.5,
            "Musculação intensa": 6.0,
            "Futebol": 7.0,
            "Basquete": 6.5,
            "Tênis": 7.3,
            "Yoga": 2.5,
            "Pilates": 3.0,
            "Dança": 4.8,
            "Boxe": 12.0,
            "Crossfit": 8.0
        }
        
        met_value = mets[exercise_type]
        
        # Cálculo: Calorias = METs × peso(kg) × tempo(h)
        calories_burned = met_value * weight * (duration / 60)
        
        st.markdown("#### 🔥 Gasto Energético")
        
        st.metric("🔥 Calorias Queimadas", f"{calories_burned:.0f} kcal",
                 delta=f"{calories_burned/duration:.1f} kcal/min")
        
        # Equivalências alimentares
        st.markdown("#### 🍎 Equivalências Alimentares")
        
        food_equivalents = {
            "🍎 Maçã média": 80,
            "🍌 Banana média": 105,
            "🍫 Chocolate (30g)": 150,
            "🍕 Fatia de pizza": 285,
            "🍔 Hambúrguer": 540,
            "☕ Café com leite": 100,
            "🥤 Refrigerante (350ml)": 140,
            "🍰 Fatia de bolo": 350
        }
        
        st.markdown("**Você queimou o equivalente a:**")
        for food, kcal in food_equivalents.items():
            equivalent = calories_burned / kcal
            if equivalent >= 0.5:
                st.write(f"• {equivalent:.1f}x {food}")
        
        # Recomendações
        st.markdown("#### 💡 Recomendações")
        
        intensity_level = "Baixa" if met_value < 6 else "Moderada" if met_value < 9 else "Alta"
        
        recommendations = {
            "Baixa": [
                "Ideal para iniciantes ou recuperação",
                "Pode ser feito diariamente",
                "Bom para saúde cardiovascular básica"
            ],
            "Moderada": [
                "Excelente para perda de peso",
                "Recomendado 3-5x por semana",
                "Melhora condicionamento cardiovascular"
            ],
            "Alta": [
                "Ótimo para atletas ou condicionados",
                "2-3x por semana com descanso",
                "Máximo benefício em menor tempo"
            ]
        }
        
        st.write(f"**Intensidade: {intensity_level}**")
        for rec in recommendations[intensity_level]:
            st.write(f"• {rec}")

def show_anthropometry_calculator():
    """Calculadoras antropométricas"""
    st.markdown("### 📏 Calculadoras Antropométricas")
    
    tab1, tab2, tab3 = st.tabs(["📊 IMC e Composição", "📐 Circunferências", "🔬 Dobras Cutâneas"])
    
    with tab1:
        show_bmi_composition()
    
    with tab2:
        show_circumferences()
    
    with tab3:
        show_skinfolds()

def show_bmi_composition():
    """IMC e composição corporal"""
    st.markdown("#### 📊 IMC e Análise Corporal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("⚖️ Peso (kg)", min_value=30.0, max_value=200.0, value=70.0)
        height = st.number_input("📏 Altura (cm)", min_value=100, max_value=250, value=170)
        age = st.number_input("👤 Idade (anos)", min_value=18, max_value=100, value=30)
        gender = st.selectbox("👤 Sexo", ["Feminino", "Masculino"])
    
    with col2:
        # Cálculos
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        ideal_weight_min = 18.5 * (height_m ** 2)
        ideal_weight_max = 24.9 * (height_m ** 2)
        
        st.metric("📊 IMC", f"{bmi:.1f} kg/m²", 
                 delta=get_bmi_classification(bmi))
        
        st.markdown(f"""
        <div class="info-card">
            <h5>⚖️ Peso Ideal:</h5>
            <p>{ideal_weight_min:.1f} - {ideal_weight_max:.1f} kg</p>
            <p><strong>Para atingir:</strong> {abs(weight - ideal_weight_max):+.1f} kg</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Classificação visual
        bmi_ranges = [
            ("Abaixo do peso", 18.5, "#2196F3"),
            ("Peso normal", 24.9, "#4CAF50"),
            ("Sobrepeso", 29.9, "#FF9800"),
            ("Obesidade I", 34.9, "#FF5722"),
            ("Obesidade II", 39.9, "#D32F2F"),
            ("Obesidade III", 50, "#B71C1C")
        ]
        
        for category, max_bmi, color in bmi_ranges:
            is_current = bmi <= max_bmi
            style = f"background: {color}; color: white;" if is_current else "background: #f0f0f0; color: #666;"
            
            if is_current:
                st.markdown(f"""
                <div style="{style} padding: 0.5rem; border-radius: 5px; margin: 0.2rem 0; font-weight: bold;">
                    👉 {category}: até {max_bmi} kg/m²
                </div>
                """, unsafe_allow_html=True)
                break
            else:
                st.markdown(f"""
                <div style="{style} padding: 0.5rem; border-radius: 5px; margin: 0.2rem 0;">
                    {category}: até {max_bmi} kg/m²
                </div>
                """, unsafe_allow_html=True)

def show_circumferences():
    """Análise de circunferências"""
    st.markdown("#### 📐 Análise de Circunferências")
    
    col1, col2 = st.columns(2)
    
    with col1:
        waist = st.number_input("📏 Cintura (cm)", min_value=50, max_value=150, value=80)
        hip = st.number_input("📏 Quadril (cm)", min_value=60, max_value=180, value=100)
        neck = st.number_input("📏 Pescoço (cm)", min_value=25, max_value=60, value=35)
        gender = st.selectbox("👤 Sexo", ["Feminino", "Masculino"], key="circ_gender")
    
    with col2:
        # Relação cintura-quadril (RCQ)
        rcq = waist / hip
        
        # Classificação de risco por RCQ
        if gender == "Feminino":
            risk_rcq = "Baixo" if rcq < 0.8 else "Moderado" if rcq < 0.85 else "Alto"
        else:
            risk_rcq = "Baixo" if rcq < 0.95 else "Moderado" if rcq < 1.0 else "Alto"
        
        # Risco por circunferência da cintura
        if gender == "Feminino":
            risk_waist = "Baixo" if waist < 80 else "Aumentado" if waist < 88 else "Muito Alto"
        else:
            risk_waist = "Baixo" if waist < 94 else "Aumentado" if waist < 102 else "Muito Alto"
        
        st.metric("📐 Relação Cintura/Quadril", f"{rcq:.2f}", 
                 delta=f"Risco {risk_rcq}")
        
        st.markdown(f"""
        <div class="{'success-card' if risk_waist == 'Baixo' else 'warning-card' if risk_waist == 'Aumentado' else 'warning-card'}">
            <h5>⚠️ Risco Cardiovascular:</h5>
            <p><strong>Por RCQ:</strong> {risk_rcq}</p>
            <p><strong>Por Cintura:</strong> {risk_waist}</p>
            <p><strong>Cintura ideal:</strong> {'< 80cm' if gender == 'Feminino' else '< 94cm'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Estimativa de gordura corporal (fórmula simplificada)
        if gender == "Feminino":
            body_fat_est = (waist * 0.67) + (hip * 0.14) + (neck * -0.43) - 9.4
        else:
            body_fat_est = (waist * 0.74) + (neck * -0.87) - 8.2
        
        st.markdown(f"""
        <div class="info-card">
            <h5>📊 Estimativa de Gordura Corporal:</h5>
            <p><strong>{body_fat_est:.1f}%</strong></p>
            <small>*Estimativa baseada em circunferências</small>
        </div>
        """, unsafe_allow_html=True)

def show_skinfolds():
    """Análise de dobras cutâneas"""
    st.markdown("#### 🔬 Análise de Dobras Cutâneas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📏 Medidas (mm):**")
        triceps = st.number_input("Tríceps", min_value=1, max_value=50, value=10)
        biceps = st.number_input("Bíceps", min_value=1, max_value=50, value=8)
        subscapular = st.number_input("Subescapular", min_value=1, max_value=50, value=12)
        suprailiac = st.number_input("Supra-ilíaca", min_value=1, max_value=50, value=15)
        
        age = st.number_input("👤 Idade", min_value=18, max_value=100, value=30, key="skin_age")
        gender = st.selectbox("👤 Sexo", ["Feminino", "Masculino"], key="skin_gender")
    
    with col2:
        # Cálculo usando equação de Durnin & Womersley
        sum_skinfolds = triceps + biceps + subscapular + suprailiac
        log_sum = math.log10(sum_skinfolds)
        
        if gender == "Feminino":
            if age <= 29:
                density = 1.1549 - (0.0678 * log_sum)
            elif age <= 49:
                density = 1.1423 - (0.0632 * log_sum)
            else:
                density = 1.1333 - (0.0612 * log_sum)
        else:
            if age <= 29:
                density = 1.1631 - (0.0632 * log_sum)
            elif age <= 49:
                density = 1.1422 - (0.0544 * log_sum)
            else:
                density = 1.1620 - (0.0700 * log_sum)
        
        # Fórmula de Siri para % de gordura
        body_fat_percent = ((4.95 / density) - 4.5) * 100
        
        st.metric("📊 Gordura Corporal", f"{body_fat_percent:.1f}%")
        
        # Classificação
        if gender == "Feminino":
            if body_fat_percent < 10:
                classification = "Essencial"
            elif body_fat_percent < 14:
                classification = "Atlética"
            elif body_fat_percent < 21:
                classification = "Boa forma"
            elif body_fat_percent < 25:
                classification = "Aceitável"
            else:
                classification = "Obesidade"
        else:
            if body_fat_percent < 5:
                classification = "Essencial"
            elif body_fat_percent < 10:
                classification = "Atlético"
            elif body_fat_percent < 15:
                classification = "Boa forma"
            elif body_fat_percent < 20:
                classification = "Aceitável"
            else:
                classification = "Obesidade"
        
        st.markdown(f"""
        <div class="success-card">
            <h5>📋 Classificação:</h5>
            <p><strong>{classification}</strong></p>
            <p><strong>Soma das dobras:</strong> {sum_skinfolds}mm</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Recomendações
        recommendations = {
            "Essencial": "Percentual muito baixo. Consulte um profissional.",
            "Atlética/Atlético": "Excelente composição corporal!",
            "Boa forma": "Muito boa composição corporal.",
            "Aceitável": "Dentro da normalidade, mas pode melhorar.",
            "Obesidade": "Recomenda-se programa de emagrecimento."
        }
        
        st.info(f"💡 {recommendations.get(classification, 'Continue o bom trabalho!')}")

# =============================================================================
# FUNÇÃO PRINCIPAL EXPANDIDA
# =============================================================================

def main():
    """Função principal da aplicação"""
    load_css()
    init_database()
    
    if not check_auth():
        login_page()
        return
    
    # Navegação baseada no tipo de usuário
    user_role = st.session_state.user['role']
    
    if user_role in ['admin', 'nutritionist']:
        # Interface para nutricionistas
        selected_page = show_sidebar()
        
        if selected_page == "dashboard":
            show_dashboard()
        elif selected_page == "patients":
            show_patients_management()
        elif selected_page == "appointments":
            show_appointments_management()
        elif selected_page == "calculators":
            show_calculators()
        elif selected_page == "meal_plans":
            show_meal_plans_management()
        elif selected_page == "recipes":
            show_recipes_management()
        elif selected_page == "gamification":
            show_gamification()
        elif selected_page == "financial":
            show_financial()
        elif selected_page == "ai_assistant":
            show_ai_assistant()
        elif selected_page == "analytics":
            show_analytics_dashboard()
        elif selected_page == "settings":
            show_settings_management()
    
    else:
        # Interface para pacientes
        selected_page = show_sidebar()
        
        if selected_page == "patient_dashboard":
            show_patient_dashboard()
        elif selected_page == "my_progress":
            show_my_progress()
        elif selected_page == "my_plan":
            show_my_plan()
        elif selected_page == "challenges":
            show_challenges()
        elif selected_page == "recipes_patient":
            show_recipes_patient()
        elif selected_page == "notifications":
            show_notifications()
        elif selected_page == "profile":
            show_profile()

# Funções que ainda precisam ser implementadas (placeholders)
def show_patients_management():
    st.title("👥 Gestão de Pacientes")
    st.info("Módulo de gestão de pacientes em desenvolvimento...")

def show_appointments_management():
    st.title("📅 Gestão de Agendamentos")
    st.info("Módulo de agendamentos em desenvolvimento...")

def show_meal_plans_management():
    st.title("📋 Gestão de Planos Alimentares")
    st.info("Módulo de planos alimentares em desenvolvimento...")

def show_recipes_management():
    st.title("🍳 Gestão de Receitas")
    st.info("Módulo de receitas em desenvolvimento...")

def show_analytics_dashboard():
    st.title("📈 Dashboard de Analytics")
    st.info("Dashboard de analytics em desenvolvimento...")

def show_settings_management():
    st.title("⚙️ Configurações do Sistema")
    st.info("Configurações do sistema em desenvolvimento...")

if __name__ == "__main__":
    main()
