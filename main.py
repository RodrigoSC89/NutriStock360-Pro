def show_admin_dashboard():
    """Dashboard executivo completo para administradores"""
    st.markdown('<h1 class="main-header">📊 Dashboard Executivo</h1>', unsafe_allow_html=True)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    try:
        # KPIs principais
        total_users = pd.read_sql_query("SELECT COUNT(*) as count FROM users WHERE active = 1", conn).iloc[0]['count']
        total_patients = pd.read_sql_query("SELECT COUNT(*) as count FROM patients WHERE active = 1", conn).iloc[0]['count']
        total_nutritionists = pd.read_sql_query("SELECT COUNT(*) as count FROM users WHERE role = 'nutritionist' AND active = 1", conn).iloc[0]['count']
        total_appointments_month = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM appointments 
            WHERE strftime('%Y-%m', appointment_date) = strftime('%Y-%m', 'now')
def show_progress_tracking():
    """Acompanhamento de progresso para nutricionistas"""
    st.markdown('<h1 class="main-header">📈 Acompanhamento de Progresso</h1>', unsafe_allow_html=True)
    
    nutritionist_id = st.session_state.user['id']
    
    tab1, tab2, tab3 = st.tabs(["📊 Visão Geral", "➕ Registrar Progresso", "📈 Análises Avançadas"])
    
    with tab1:
        show_progress_overview(nutritionist_id)
    
    with tab2:
        register_patient_progress(nutritionist_id)
    
    with tab3:
        show_advanced_progress_analysis(nutritionist_id)

def show_progress_overview(nutritionist_id):
    """Visão geral do progresso dos pacientes"""
    conn = sqlite3.connect('nutriapp360.db')
    
    # Pacientes com progresso recente
    recent_progress = pd.read_sql_query("""
        SELECT 
            p.full_name,
            p.patient_id,
            pp.record_date,
            pp.weight,
            pp.body_fat,
            pp.muscle_mass,
            pp.notes,
            LAG(pp.weight) OVER (PARTITION BY p.id ORDER BY pp.record_date) as previous_weight
        FROM patient_progress pp
        JOIN patients p ON p.id = pp.patient_id
        WHERE p.nutritionist_id = ?
        AND pp.record_date >= DATE('now', '-30 days')
        ORDER BY pp.record_date DESC
    """, conn, params=[nutritionist_id])
    
    if not recent_progress.empty:
        st.subheader("📊 Progresso Recente (Últimos 30 dias)")
        
        for idx, progress in recent_progress.iterrows():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                weight_change = ""
                if progress['previous_weight'] and progress['weight']:
                    change = progress['weight'] - progress['previous_weight']
                    if change != 0:
                        color = "#4CAF50" if change < 0 else "#FF9800" if change > 0 else "#757575"
                        weight_change = f"({change:+.1f}kg)"
                
                record_date = pd.to_datetime(progress['record_date']).strftime('%d/%m/%Y')
                
                st.markdown(f"""
                <div class="patient-info-card">
                    <h5>{progress['full_name']} ({progress['patient_id']}) - {record_date}</h5>
                    <p><strong>Peso:</strong> {progress['weight']}kg {weight_change} | 
                       <strong>% Gordura:</strong> {progress['body_fat'] or 'N/A'} | 
                       <strong>% Músculo:</strong> {progress['muscle_mass'] or 'N/A'}</p>
                    {f"<small><strong>Obs:</strong> {progress['notes']}</small>" if progress['notes'] else ""}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("📊 Ver Evolução", key=f"evolution_{idx}"):
                    show_patient_evolution(progress['patient_id'])
    
    # Pacientes sem progresso recente
    patients_no_progress = pd.read_sql_query("""
        SELECT 
            p.full_name,
            p.patient_id,
            MAX(pp.record_date) as last_progress
        FROM patients p
        LEFT JOIN patient_progress pp ON pp.patient_id = p.id
        WHERE p.nutritionist_id = ? AND p.active = 1
        GROUP BY p.id, p.full_name, p.patient_id
        HAVING last_progress IS NULL OR last_progress < DATE('now', '-30 days')
        ORDER BY last_progress DESC NULLS LAST
    """, conn, params=[nutritionist_id])
    
    if not patients_no_progress.empty:
        st.subheader("⚠️ Pacientes sem Progresso Registrado")
        
        for idx, patient in patients_no_progress.iterrows():
            last_date = "Nunca"
            if patient['last_progress']:
                last_date = pd.to_datetime(patient['last_progress']).strftime('%d/%m/%Y')
            
            col_alert1, col_alert2 = st.columns([3, 1])
            
            with col_alert1:
                st.warning(f"📋 {patient['full_name']} ({patient['patient_id']}) - Último registro: {last_date}")
            
            with col_alert2:
                if st.button("➕ Registrar", key=f"register_{patient['patient_id']}"):
                    st.session_state[f"register_progress_{patient['patient_id']}"] = True
                    st.rerun()
    
def show_audit_log():
    """Sistema de auditoria completo"""
    st.markdown('<h1 class="main-header">🔍 Log de Auditoria</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Logs Recentes", "🔍 Busca Avançada", "📊 Análise de Atividade"])
    
    with tab1:
        show_recent_audit_logs()
    
    with tab2:
        show_advanced_audit_search()
    
    with tab3:
        show_audit_analytics()

def show_recent_audit_logs():
    """Exibe logs de auditoria recentes"""
    st.subheader("📋 Atividades Recentes")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Filtros básicos
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        days_back = st.selectbox("Período", [1, 7, 30, 90], index=1, format_func=lambda x: f"Últimos {x} dias")
    
    with col_filter2:
        action_filter = st.selectbox("Tipo de Ação", [
            "Todas", "login", "logout", "create_user", "create_patient", 
            "create_appointment", "register_progress", "create_charge"
        ])
    
    with col_filter3:
        user_roles = ["Todos", "admin", "nutritionist", "secretary", "patient"]
        role_filter = st.selectbox("Papel do Usuário", user_roles)
    
    # Query com filtros
    where_conditions = ["al.created_at >= DATE('now', ?)"]
    params = [f'-{days_back} days']
    
    if action_filter != "Todas":
        where_conditions.append("al.action_type = ?")
        params.append(action_filter)
    
    if role_filter != "Todos":
        where_conditions.append("u.role = ?")
        params.append(role_filter)
    
    where_clause = " AND ".join(where_conditions)
    
    # Buscar logs
    audit_logs = pd.read_sql_query(f"""
        SELECT 
            al.*,
            u.full_name,
            u.role,
            u.username
        FROM audit_log al
        JOIN users u ON u.id = al.user_id
        WHERE {where_clause}
        ORDER BY al.created_at DESC
        LIMIT 100
    """, conn, params=params)
    
    conn.close()
    
    if not audit_logs.empty:
        # Estatísticas rápidas
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        total_actions = len(audit_logs)
        unique_users = audit_logs['user_id'].nunique()
        most_common_action = audit_logs['action_type'].mode().iloc[0] if len(audit_logs) > 0 else "N/A"
        
        with col_stat1:
            st.metric("Total Ações", total_actions)
        with col_stat2:
            st.metric("Usuários Ativos", unique_users)
        with col_stat3:
            st.metric("Ação Mais Comum", most_common_action)
        with col_stat4:
            recent_logins = len(audit_logs[audit_logs['action_type'] == 'login'])
            st.metric("Logins", recent_logins)
        
        # Timeline de atividades
        for idx, log in audit_logs.iterrows():
            timestamp = pd.to_datetime(log['created_at']).strftime('%d/%m/%Y %H:%M:%S')
            
            # Cores por tipo de ação
            action_colors = {
                'login': '#4CAF50',
                'logout': '#757575', 
                'create_user': '#2196F3',
                'create_patient': '#9C27B0',
                'create_appointment': '#FF9800',
                'register_progress': '#00BCD4',
                'create_charge': '#4CAF50',
                'edit_user': '#FFC107',
                'delete': '#F44336'
            }
            
            color = action_colors.get(log['action_type'], '#757575')
            
            # Ícones por ação
            action_icons = {
                'login': '🔓',
                'logout': '🔒',
                'create_user': '👤',
                'create_patient': '🏥',
                'create_appointment': '📅',
                'register_progress': '📈',
                'create_charge': '💰',
                'edit_user': '✏️',
                'delete': '🗑️'
            }
            
            icon = action_icons.get(log['action_type'], '📝')
            
            st.markdown(f"""
            <div style="border-left: 4px solid {color}; padding: 1rem; margin: 0.5rem 0; background: white; border-radius: 5px;">
                <h5 style="margin: 0; color: {color};">{icon} {log['action_type'].replace('_', ' ').title()}</h5>
                <p style="margin: 0.3rem 0;"><strong>Usuário:</strong> {log['full_name']} ({log['role']}) - {log['username']}</p>
                <p style="margin: 0;"><small><strong>Quando:</strong> {timestamp}</small></p>
                {f"<p style='margin: 0;'><small><strong>Tabela:</strong> {log['table_affected']}</small></p>" if log['table_affected'] else ""}
                {f"<p style='margin: 0;'><small><strong>Registro ID:</strong> {log['record_id']}</small></p>" if log['record_id'] else ""}
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.info("Nenhum log de auditoria encontrado nos critérios selecionados.")

def show_advanced_audit_search():
    """Busca avançada nos logs de auditoria"""
    st.subheader("🔍 Busca Avançada")
    
    with st.form("advanced_audit_search"):
        col_search1, col_search2 = st.columns(2)
        
        with col_search1:
            user_search = st.text_input("Nome do usuário")
            action_search = st.text_input("Tipo de ação")
            table_search = st.text_input("Tabela afetada")
        
        with col_search2:
            date_start = st.date_input("Data início", value=date.today() - timedelta(days=30))
            date_end = st.date_input("Data fim", value=date.today())
            record_id_search = st.text_input("ID do registro")
        
        search_button = st.form_submit_button("🔍 Buscar")
        
        if search_button:
            conn = sqlite3.connect('nutriapp360.db')
            
            # Construir query dinamicamente
            where_conditions = ["al.created_at BETWEEN ? AND ?"]
            params = [date_start, date_end]
            
            if user_search:
                where_conditions.append("u.full_name LIKE ?")
                params.append(f"%{user_search}%")
            
            if action_search:
                where_conditions.append("al.action_type LIKE ?")
                params.append(f"%{action_search}%")
            
            if table_search:
                where_conditions.append("al.table_affected LIKE ?")
                params.append(f"%{table_search}%")
            
            if record_id_search:
                where_conditions.append("al.record_id = ?")
                params.append(record_id_search)
            
            where_clause = " AND ".join(where_conditions)
            
            search_results = pd.read_sql_query(f"""
                SELECT 
                    al.*,
                    u.full_name,
                    u.role,
                    u.username
                FROM audit_log al
                JOIN users u ON u.id = al.user_id
                WHERE {where_clause}
                ORDER BY al.created_at DESC
                LIMIT 200
            """, conn, params=params)
            
            conn.close()
            
            if not search_results.empty:
                st.success(f"✅ Encontrados {len(search_results)} registros")
                
                # Exibir resultados em tabela
                display_results = search_results[[
                    'created_at', 'full_name', 'role', 'action_type', 
                    'table_affected', 'record_id'
                ]].copy()
                
                display_results['created_at'] = pd.to_datetime(display_results['created_at']).dt.strftime('%d/%m/%Y %H:%M')
                display_results.columns = ['Data/Hora', 'Usuário', 'Papel', 'Ação', 'Tabela', 'ID Registro']
                
                st.dataframe(display_results, use_container_width=True)
            else:
                st.warning("Nenhum resultado encontrado com os critérios especificados.")

def show_audit_analytics():
    """Análise de atividade do sistema"""
    st.subheader("📊 Análise de Atividade")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Período para análise
    col_analytics1, col_analytics2 = st.columns(2)
    with col_analytics1:
        analytics_start = st.date_input("Período início", value=date.today() - timedelta(days=30), key="analytics_start")
    with col_analytics2:
        analytics_end = st.date_input("Período fim", value=date.today(), key="analytics_end")
    
    # Atividade por usuário
    user_activity = pd.read_sql_query("""
        SELECT 
            u.full_name,
            u.role,
            COUNT(al.id) as total_actions,
            COUNT(DISTINCT DATE(al.created_at)) as active_days
        FROM users u
        LEFT JOIN audit_log al ON al.user_id = u.id
        WHERE al.created_at BETWEEN ? AND ?
        GROUP BY u.id, u.full_name, u.role
        ORDER BY total_actions DESC
    """, conn, params=[analytics_start, analytics_end])
    
    if not user_activity.empty:
        st.write("**👥 Atividade por Usuário:**")
        
        col_user_chart, col_user_table = st.columns(2)
        
        with col_user_chart:
            # Gráfico de atividade por papel
            role_activity = user_activity.groupby('role')['total_actions'].sum().reset_index()
            fig_roles = px.pie(role_activity, values='total_actions', names='role',
                             title="Atividade por Papel do Usuário")
            st.plotly_chart(fig_roles, use_container_width=True)
        
        with col_user_table:
            # Top usuários mais ativos
            top_users = user_activity.head(10)
            top_users_display = top_users[['full_name', 'role', 'total_actions', 'active_days']].copy()
            top_users_display.columns = ['Nome', 'Papel', 'Ações', 'Dias Ativos']
            st.dataframe(top_users_display, use_container_width=True)
    
    # Atividade por tipo de ação
    action_activity = pd.read_sql_query("""
        SELECT 
            action_type,
            COUNT(*) as count,
            COUNT(DISTINCT user_id) as unique_users
        FROM audit_log
        WHERE created_at BETWEEN ? AND ?
        GROUP BY action_type
        ORDER BY count DESC
    """, conn, params=[analytics_start, analytics_end])
    
    if not action_activity.empty:
        st.write("**📊 Atividade por Tipo de Ação:**")
        
        col_action_chart, col_action_table = st.columns(2)
        
        with col_action_chart:
            fig_actions = px.bar(action_activity, x='action_type', y='count',
                               title="Frequência por Tipo de Ação")
            st.plotly_chart(fig_actions, use_container_width=True)
        
        with col_action_table:
            action_display = action_activity.copy()
            action_display.columns = ['Tipo de Ação', 'Quantidade', 'Usuários Únicos']
            st.dataframe(action_display, use_container_width=True)
    
    # Atividade temporal
    temporal_activity = pd.read_sql_query("""
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as total_actions,
            COUNT(DISTINCT user_id) as active_users
        FROM audit_log
        WHERE created_at BETWEEN ? AND ?
        GROUP BY DATE(created_at)
        ORDER BY date
    """, conn, params=[analytics_start, analytics_end])
    
    if not temporal_activity.empty:
        st.write("**📈 Atividade Temporal:**")
        
        temporal_activity['date'] = pd.to_datetime(temporal_activity['date'])
        
        fig_temporal = px.line(temporal_activity, x='date', y=['total_actions', 'active_users'],
                             title="Atividade do Sistema ao Longo do Tempo", markers=True)
        st.plotly_chart(fig_temporal, use_container_width=True)
    
    conn.close()

def show_system_settings():
    """Configurações do sistema"""
    st.markdown('<h1 class="main-header">⚙️ Configurações do Sistema</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Clínica", "💰 Financeiro", "🎮 Gamificação", "🔔 Notificações"])
    
    with tab1:
        show_clinic_settings()
    
    with tab2:
        show_financial_settings()
    
    with tab3:
        show_gamification_settings()
    
    with tab4:
        show_notification_settings()

def show_clinic_settings():
    """Configurações da clínica"""
    st.subheader("🏢 Informações da Clínica")
    
    # Simulação de configurações (em um sistema real, estas seriam armazenadas no banco)
    if 'clinic_settings' not in st.session_state:
        st.session_state.clinic_settings = {
            'name': 'Clínica NutriApp360',
            'address': 'Rua das Palmeiras, 123 - Centro',
            'city': 'São Paulo - SP',
            'phone': '(11) 3333-4444',
            'email': 'contato@nutriapp360.com',
            'cnpj': '12.345.678/0001-90',
            'working_hours': '08:00 - 18:00',
            'working_days': 'Segunda a Sexta'
        }
    
    with st.form("clinic_settings_form"):
        col_clinic1, col_clinic2 = st.columns(2)
        
        with col_clinic1:
            clinic_name = st.text_input("Nome da Clínica", value=st.session_state.clinic_settings['name'])
            clinic_address = st.text_input("Endereço", value=st.session_state.clinic_settings['address'])
            clinic_city = st.text_input("Cidade/Estado", value=st.session_state.clinic_settings['city'])
            clinic_phone = st.text_input("Telefone", value=st.session_state.clinic_settings['phone'])
        
        with col_clinic2:
            clinic_email = st.text_input("Email", value=st.session_state.clinic_settings['email'])
            clinic_cnpj = st.text_input("CNPJ", value=st.session_state.clinic_settings['cnpj'])
            clinic_hours = st.text_input("Horário de Funcionamento", value=st.session_state.clinic_settings['working_hours'])
            clinic_days = st.text_input("Dias de Funcionamento", value=st.session_state.clinic_settings['working_days'])
        
        if st.form_submit_button("💾 Salvar Configurações"):
            st.session_state.clinic_settings.update({
                'name': clinic_name,
                'address': clinic_address,
                'city': clinic_city,
                'phone': clinic_phone,
                'email': clinic_email,
                'cnpj': clinic_cnpj,
                'working_hours': clinic_hours,
                'working_days': clinic_days
            })
            st.success("✅ Configurações da clínica salvas!")

def show_gamification_settings():
    """Configurações de gamificação"""
    st.subheader("🎮 Configurações de Gamificação")
    
    # Configurações de pontuação
    if 'gamification_settings' not in st.session_state:
        st.session_state.gamification_settings = {
            'points_consultation': 20,
            'points_progress': 15,
            'points_week_goal': 25,
            'points_month_goal': 100,
            'points_per_level': 100,
            'enable_notifications': True,
            'enable_rankings': True
        }
    
    st.write("**🎯 Sistema de Pontuação**")
    
    col_points1, col_points2 = st.columns(2)
    
    with col_points1:
        consultation_points = st.number_input("Pontos por consulta realizada", 
                                            value=st.session_state.gamification_settings['points_consultation'])
        progress_points = st.number_input("Pontos por registro de progresso", 
                                        value=st.session_state.gamification_settings['points_progress'])
        week_goal_points = st.number_input("Pontos por meta semanal atingida", 
                                         value=st.session_state.gamification_settings['points_week_goal'])
    
    with col_points2:
        month_goal_points = st.number_input("Pontos por meta mensal atingida", 
                                          value=st.session_state.gamification_settings['points_month_goal'])
        points_per_level = st.number_input("Pontos necessários por nível", 
                                         value=st.session_state.gamification_settings['points_per_level'])
        
        enable_notifications = st.checkbox("Notificações de gamificação", 
                                         value=st.session_state.gamification_settings['enable_notifications'])
        enable_rankings = st.checkbox("Sistema de rankings", 
                                    value=st.session_state.gamification_settings['enable_rankings'])
    
    if st.button("💾 Salvar Configurações de Gamificação"):
        st.session_state.gamification_settings.update({
            'points_consultation': consultation_points,
            'points_progress': progress_points,
            'points_week_goal': week_goal_points,
            'points_month_goal': month_goal_points,
            'points_per_level': points_per_level,
            'enable_notifications': enable_notifications,
            'enable_rankings': enable_rankings
        })
        st.success("✅ Configurações de gamificação salvas!")
    
    # Preview das badges disponíveis
    st.write("**🏆 Badges do Sistema**")
    
    system_badges = [
        {"name": "Primeiro Passo", "description": "Primeira consulta", "icon": "🚀", "points": 20},
        {"name": "Consistência", "description": "7 dias seguidos", "icon": "🔥", "points": 50},
        {"name": "Dedicação", "description": "30 dias seguidos", "icon": "💪", "points": 150},
        {"name": "Meta Alcançada", "description": "Objetivo de peso atingido", "icon": "🎯", "points": 200},
        {"name": "Transformação", "description": "Mudança significativa", "icon": "🦋", "points": 100}
    ]
    
    for badge in system_badges:
        st.markdown(f"""
        <div class="gamification-card">
            <h5>{badge['icon']} {badge['name']} (+{badge['points']} pontos)</h5>
            <p style="font-size: 0.9rem;">{badge['description']}</p>
        </div>
        """, unsafe_allow_html=True)

def show_notification_settings():
    """Configurações de notificações"""
    st.subheader("🔔 Configurações de Notificações")
    
    if 'notification_settings' not in st.session_state:
        st.session_state.notification_settings = {
            'email_reminders': True,
            'sms_reminders': False,
            'appointment_reminder_hours': 24,
            'payment_reminder_days': 3,
            'progress_reminder_days': 7,
            'admin_notifications': True,
            'system_alerts': True
        }
    
    st.write("**📧 Lembretes Automáticos**")
    
    col_notif1, col_notif2 = st.columns(2)
    
    with col_notif1:
        email_reminders = st.checkbox("Lembretes por email", 
                                    value=st.session_state.notification_settings['email_reminders'])
        sms_reminders = st.checkbox("Lembretes por SMS", 
                                  value=st.session_state.notification_settings['sms_reminders'])
        admin_notifications = st.checkbox("Notificações administrativas", 
                                        value=st.session_state.notification_settings['admin_notifications'])
    
    with col_notif2:
        appointment_hours = st.number_input("Lembrete de consulta (horas antes)", 
                                          value=st.session_state.notification_settings['appointment_reminder_hours'])
        payment_days = st.number_input("Lembrete de pagamento (dias antes)", 
                                     value=st.session_state.notification_settings['payment_reminder_days'])
        progress_days = st.number_input("Lembrete de progresso (dias)", 
                                      value=st.session_state.notification_settings['progress_reminder_days'])
    
    st.write("**⚙️ Configurações do Sistema**")
    
    system_alerts = st.checkbox("Alertas do sistema", 
                               value=st.session_state.notification_settings['system_alerts'])
    
    if st.button("💾 Salvar Configurações de Notificações"):
        st.session_state.notification_settings.update({
            'email_reminders': email_reminders,
            'sms_reminders': sms_reminders,
            'appointment_reminder_hours': appointment_hours,
            'payment_reminder_days': payment_days,
            'progress_reminder_days': progress_days,
            'admin_notifications': admin_notifications,
            'system_alerts': system_alerts
        })
        st.success("✅ Configurações de notificações salvas!")

def show_backup_restore():
    """Sistema de backup e restore"""
    st.markdown('<h1 class="main-header">💾 Backup & Restore</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["💾 Backup", "📥 Restore", "📊 Histórico"])
    
    with tab1:
        show_backup_options()
    
    with tab2:
        show_restore_options()
    
    with tab3:
        show_backup_history()

def show_backup_options():
    """Opções de backup"""
    st.subheader("💾 Criar Backup")
    
    # Opções de backup
    st.write("**📋 Selecione os dados para backup:**")
    
    backup_users = st.checkbox("👥 Usuários", value=True)
    backup_patients = st.checkbox("🏥 Pacientes", value=True)
    backup_appointments = st.checkbox("📅 Agendamentos", value=True)
    backup_progress = st.checkbox("📈 Progresso dos pacientes", value=True)
    backup_financial = st.checkbox("💰 Dados financeiros", value=True)
    backup_recipes = st.checkbox("🍳 Receitas", value=True)
    backup_meal_plans = st.checkbox("📋 Planos alimentares", value=True)
    backup_audit = st.checkbox("🔍 Logs de auditoria", value=False)
    
    # Tipo de backup
    backup_type = st.selectbox("Tipo de backup:", [
        "Backup Completo",
        "Backup Incremental", 
        "Backup Somente Dados Críticos"
    ])
    
    # Agendamento
    st.write("**⏰ Agendamento Automático:**")
    
    auto_backup = st.checkbox("Habilitar backup automático")
    
    if auto_backup:
        backup_frequency = st.selectbox("Frequência:", [
            "Diário", "Semanal", "Mensal"
        ])
        backup_time = st.time_input("Horário:", value=datetime.strptime("02:00", "%H:%M").time())
    
    # Botão de backup manual
    if st.button("🚀 Iniciar Backup Agora"):
        with st.spinner("Criando backup..."):
            # Simular processo de backup
            import time
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            tables_to_backup = []
            if backup_users:
                tables_to_backup.append("users")
            if backup_patients:
                tables_to_backup.append("patients")
            if backup_appointments:
                tables_to_backup.append("appointments")
            if backup_progress:
                tables_to_backup.append("patient_progress")
            if backup_financial:
                tables_to_backup.append("patient_financial")
            if backup_recipes:
                tables_to_backup.append("recipes")
            if backup_meal_plans:
                tables_to_backup.append("meal_plans")
            if backup_audit:
                tables_to_backup.append("audit_log")
            
            for i, table in enumerate(tables_to_backup):
                status_text.text(f"Fazendo backup da tabela: {table}")
                progress = (i + 1) / len(tables_to_backup)
                progress_bar.progress(progress)
                time.sleep(0.5)  # Simular tempo de processamento
            
            status_text.text("Backup concluído!")
            
            # Simular informações do backup
            backup_info = {
                'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S'),
                'size': '2.3 MB',
                'tables': len(tables_to_backup),
                'records': 1247  # Simulado
            }
            
            st.success(f"""
            ✅ **Backup criado com sucesso!**
            
            📁 **Arquivo:** backup_{backup_info['timestamp']}.sql  
            📊 **Tamanho:** {backup_info['size']}  
            🗃️ **Tabelas:** {backup_info['tables']}  
            📝 **Registros:** {backup_info['records']}  
            """)

def show_restore_options():
    """Opções de restore"""
    st.subheader("📥 Restaurar Backup")
    
    st.warning("⚠️ **Atenção:** A restauração substituirá todos os dados atuais. Certifique-se de ter um backup recente antes de prosseguir.")
    
    # Lista de backups disponíveis (simulado)
    available_backups = [
        {
            'filename': 'backup_20241025_020000.sql',
            'date': '25/10/2024 02:00:00',
            'size': '2.3 MB',
            'type': 'Completo'
        },
        {
            'filename': 'backup_20241024_020000.sql', 
            'date': '24/10/2024 02:00:00',
            'size': '2.1 MB',
            'type': 'Completo'
        },
        {
            'filename': 'backup_20241023_020000.sql',
            'date': '23/10/2024 02:00:00', 
            'size': '2.0 MB',
            'type': 'Completo'
        }
    ]
    
    st.write("**📋 Backups Disponíveis:**")
    
    selected_backup = st.selectbox(
        "Selecione o backup para restaurar:",
        range(len(available_backups)),
        format_func=lambda x: f"{available_backups[x]['filename']} - {available_backups[x]['date']} ({available_backups[x]['size']})"
    )
    
    # Opções de restore
    st.write("**⚙️ Opções de Restauração:**")
    
    restore_mode = st.selectbox("Modo de restauração:", [
        "Restauração Completa (substitui todos os dados)",
        "Restauração Parcial (selecionar tabelas)",
        "Restauração com Merge (preserva dados mais recentes)"
    ])
    
    if restore_mode == "Restauração Parcial (selecionar tabelas)":
        st.write("**Selecione as tabelas para restaurar:**")
        restore_users = st.checkbox("👥 Usuários", key="restore_users")
        restore_patients = st.checkbox("🏥 Pacientes", key="restore_patients") 
        restore_appointments = st.checkbox("📅 Agendamentos", key="restore_appointments")
        restore_progress = st.checkbox("📈 Progresso", key="restore_progress")
    
    # Confirmação de segurança
    st.write("**🔒 Confirmação de Segurança:**")
    
    safety_check = st.text_input("Digite 'CONFIRMAR RESTORE' para prosseguir:")
    
    if st.button("🔄 Iniciar Restauração", disabled=(safety_check != "CONFIRMAR RESTORE")):
        if safety_check == "CONFIRMAR RESTORE":
            with st.spinner("Restaurando backup..."):
                import time
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                steps = [
                    "Validando arquivo de backup",
                    "Criando backup de segurança atual",
                    "Limpando dados existentes", 
                    "Restaurando dados",
                    "Verificando integridade",
                    "Finalizando processo"
                ]
                
                for i, step in enumerate(steps):
                    status_text.text(f"Etapa {i+1}/{len(steps)}: {step}")
                    progress = (i + 1) / len(steps)
                    progress_bar.progress(progress)
                    time.sleep(1)
                
                st.success("✅ Backup restaurado com sucesso!")
                st.info("🔄 O sistema será reiniciado para aplicar as alterações.")

def show_backup_history():
    """Histórico de backups"""
    st.subheader("📊 Histórico de Backups")
    
    # Histórico simulado
    backup_history = [
        {
            'date': '25/10/2024 02:00',
            'type': 'Automático',
            'status': 'Sucesso',
            'size': '2.3 MB',
            'duration': '45s',
            'tables': 8
        },
        {
            'date': '24/10/2024 02:00',
            'type': 'Automático', 
            'status': 'Sucesso',
            'size': '2.1 MB',
            'duration': '42s',
            'tables': 8
        },
        {
            'date': '23/10/2024 15:30',
            'type': 'Manual',
            'status': 'Sucesso',
            'size': '2.0 MB', 
            'duration': '38s',
            'tables': 7
        },
        {
            'date': '23/10/2024 02:00',
            'type': 'Automático',
            'status': 'Falhou',
            'size': '-',
            'duration': '15s',
            'tables': 0
        },
        {
            'date': '22/10/2024 02:00',
            'type': 'Automático',
            'status': 'Sucesso',
            'size': '1.9 MB',
            'duration': '40s',
            'tables': 8
        }
    ]
    
    # Criar DataFrame para exibição
    history_df = pd.DataFrame(backup_history)
    
    # Estilizar status
    def style_status(val):
        if val == 'Sucesso':
            return 'color: #4CAF50; font-weight: bold;'
        elif val == 'Falhou':
            return 'color: #F44336; font-weight: bold;'
        return ''
    
    # Exibir tabela
    st.dataframe(history_df, use_container_width=True)
    
    # Estatísticas
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    total_backups = len(backup_history)
    successful_backups = len([b for b in backup_history if b['status'] == 'Sucesso'])
    success_rate = (successful_backups / total_backups * 100) if total_backups > 0 else 0
    avg_size = "2.1 MB"  # Simulado
    
    with col_stat1:
        st.metric("Total de Backups", total_backups)
    
    with col_stat2:
        st.metric("Bem-sucedidos", successful_backups)
    
    with col_stat3:
        st.metric("Taxa de Sucesso", f"{success_rate:.1f}%")
    
    with col_stat4:
        st.metric("Tamanho Médio", avg_size)
    
    # Gráfico de tendência
    dates = [datetime.strptime(b['date'], '%d/%m/%Y %H:%M') for b in backup_history if b['status'] == 'Sucesso']
    sizes_mb = [float(b['size'].replace(' MB', '')) for b in backup_history if b['status'] == 'Sucesso']
    
    if len(dates) > 1:
        trend_df = pd.DataFrame({'date': dates, 'size_mb': sizes_mb})
        fig_trend = px.line(trend_df, x='date', y='size_mb', 
                           title='Evolução do Tamanho dos Backups', markers=True)
        fig_trend.update_layout(yaxis_title='Tamanho (MB)')
        st.plotly_chart(fig_trend, use_container_width=True)

def show_patient_profile():
    """Perfil completo do paciente"""
    st.markdown('<h1 class="main-header">👤 Meu Perfil</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar dados do paciente
    patient_data = pd.read_sql_query("""
        SELECT p.*, n.full_name as nutritionist_name, s.full_name as secretary_name
        FROM patients p
        LEFT JOIN users n ON n.id = p.nutritionist_id
        LEFT JOIN users s ON s.id = p.secretary_id
        WHERE p.user_id = ?
    """, conn, params=[user_id])
    
    if patient_data.empty:
        st.error("Dados do paciente não encontrados.")
        conn.close()
        return
    
    patient = patient_data.iloc[0]
    
    tab1, tab2, tab3 = st.tabs(["📋 Dados Pessoais", "🏥 Informações Médicas", "📱 Preferências"])
    
    with tab1:
        show_personal_data(patient, conn)
    
    with tab2:
        show_medical_info(patient, conn)
    
    with tab3:
        show_patient_preferences(patient, conn)
    
    conn.close()

def show_personal_data(patient, conn):
    """Dados pessoais do paciente"""
    st.subheader("📋 Meus Dados Pessoais")
    
    # Informações básicas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="patient-info-card">
            <h4>👤 Informações Básicas</h4>
            <p><strong>Nome:</strong> {patient['full_name']}</p>
            <p><strong>ID do Paciente:</strong> {patient['patient_id']}</p>
            <p><strong>Email:</strong> {patient['email'] or 'Não informado'}</p>
            <p><strong>Telefone:</strong> {patient['phone'] or 'Não informado'}</p>
            <p><strong>Data de Nascimento:</strong> {pd.to_datetime(patient['birth_date']).strftime('%d/%m/%Y') if patient['birth_date'] else 'Não informado'}</p>
            <p><strong>Gênero:</strong> {patient['gender'] or 'Não informado'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="patient-info-card">
            <h4>🏥 Equipe de Cuidados</h4>
            <p><strong>Nutricionista:</strong> {patient['nutritionist_name'] or 'Não definido'}</p>
            <p><strong>Secretária:</strong> {patient['secretary_name'] or 'Não definido'}</p>
            <p><strong>Convênio:</strong> {patient['insurance_info'] or 'Particular'}</p>
            <p><strong>Cadastrado em:</strong> {pd.to_datetime(patient['created_at']).strftime('%d/%m/%Y') if patient['created_at'] else 'N/A'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Dados físicos
    st.subheader("📏 Dados Físicos")
    
    col3, col4 = st.columns(2)
    
    with col3:
        # IMC atual
        imc = "N/A"
        imc_category = ""
        if patient['height'] and patient['current_weight']:
            imc_value = patient['current_weight'] / (patient['height'] ** 2)
            imc = f"{imc_value:.1f}"
            
            if imc_value < 18.5:
                imc_category = "Abaixo do peso"
            elif imc_value < 25:
                imc_category = "Peso normal"
            elif imc_value < 30:
                imc_category = "Sobrepeso"
            else:
                imc_category = "Obesidade"
        
        st.metric("Altura", f"{patient['height']} m" if patient['height'] else "N/A")
        st.metric("Peso Atual", f"{patient['current_weight']} kg" if patient['current_weight'] else "N/A")
    
    with col4:
        st.metric("Peso Objetivo", f"{patient['target_weight']} kg" if patient['target_weight'] else "N/A")
        st.metric("IMC", imc)
        if imc_category:
            if "normal" in imc_category.lower():
                st.success(f"📊 {imc_category}")
            elif "sobrepeso" in imc_category.lower():
                st.warning(f"📊 {imc_category}")
            else:
                st.info(f"📊 {imc_category}")
    
    # Progresso visual
    if patient['current_weight'] and patient['target_weight']:
        weight_diff = patient['current_weight'] - patient['target_weight']
        if abs(weight_diff) > 0.5:
            if weight_diff > 0:
                st.info(f"🎯 Faltam {weight_diff:.1f}kg para atingir seu objetivo!")
            else:
                st.success(f"🎉 Você está {abs(weight_diff):.1f}kg abaixo do seu objetivo!")
        else:
            st.success("🎯 Você está no seu peso objetivo!")

def show_medical_info(patient, conn):
    """Informações médicas do paciente"""
    st.subheader("🏥 Informações Médicas")
    
    col_med1, col_med2 = st.columns(2)
    
    with col_med1:
        st.markdown(f"""
        <div class="patient-info-card">
            <h4>⚕️ Condições de Saúde</h4>
            <p><strong>Condições médicas:</strong></p>
            <p>{patient['medical_conditions'] or 'Nenhuma condição médica relatada'}</p>
            
            <p><strong>Nível de atividade:</strong></p>
            <p>{patient['activity_level'] or 'Não informado'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_med2:
        st.markdown(f"""
        <div class="patient-info-card">
            <h4>🚫 Restrições Alimentares</h4>
            <p><strong>Alergias:</strong></p>
            <p>{patient['allergies'] or 'Nenhuma alergia conhecida'}</p>
            
            <p><strong>Preferências dietéticas:</strong></p>
            <p>{patient['dietary_preferences'] or 'Nenhuma preferência específica'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Contatos de emergência
    st.subheader("🚨 Contatos de Emergência")
    
    st.markdown(f"""
    <div class="patient-info-card">
        <h4>📞 Em Caso de Emergência</h4>
        <p><strong>Nome do contato:</strong> {patient['emergency_contact'] or 'Não informado'}</p>
        <p><strong>Telefone:</strong> {patient['emergency_phone'] or 'Não informado'}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Histórico médico recente
    st.subheader("📊 Meu Histórico Recente")
    
    # Último progresso registrado
    last_progress = pd.read_sql_query("""
        SELECT * FROM patient_progress 
        WHERE patient_id = ?
        ORDER BY record_date DESC
        LIMIT 5
    """, conn, params=[patient['id']])
    
    if not last_progress.empty:
        st.write("**📈 Últimos Registros de Progresso:**")
        
        for idx, progress in last_progress.iterrows():
            record_date = pd.to_datetime(progress['record_date']).strftime('%d/%m/%Y')
            
            progress_text = f"**{record_date}:** "
            if progress['weight']:
                progress_text += f"Peso: {progress['weight']}kg "
            if progress['body_fat']:
                progress_text += f"| % Gordura: {progress['body_fat']} "
            if progress['muscle_mass']:
                progress_text += f"| % Músculo: {progress['muscle_mass']} "
            
            st.write(progress_text)
            
            if progress['notes']:
                st.caption(f"📝 {progress['notes']}")
    else:
        st.info("Nenhum registro de progresso ainda.")

def show_patient_preferences(patient, conn):
    """Preferências do paciente"""
    st.subheader("📱 Minhas Preferências")
    
    # Preferências de notificação (simuladas)
    st.write("**🔔 Notificações**")
    
    col_pref1, col_pref2 = st.columns(2)
    
    with col_pref1:
        email_notifications = st.checkbox("Receber lembretes por email", value=True)
        appointment_reminders = st.checkbox("Lembretes de consulta", value=True)
        progress_reminders = st.checkbox("Lembretes de progresso", value=True)
    
    with col_pref2:
        sms_notifications = st.checkbox("Receber lembretes por SMS", value=False)
        gamification_notifications = st.checkbox("Notificações de pontos e badges", value=True)
        newsletter = st.checkbox("Receber newsletter nutricional", value=False)
    
    # Horário preferido para notificações
    st.write("**⏰ Horários de Notificação**")
    
    col_time1, col_time2 = st.columns(2)
    
    with col_time1:
        morning_reminders = st.checkbox("Lembretes matinais", value=True)
        if morning_reminders:
            morning_time = st.time_input("Horário matinal", value=datetime.strptime("08:00", "%H:%M").time())
    
    with col_time2:
        evening_reminders = st.checkbox("Lembretes noturnos", value=False)
        if evening_reminders:
            evening_time = st.time_input("Horário noturno", value=datetime.strptime("19:00", "%H:%M").time())
    
    # Preferências de privacidade
    st.write("**🔒 Privacidade**")
    
    share_progress = st.checkbox("Permitir compartilhamento do meu progresso em rankings anônimos", value=True)
    data_analysis = st.checkbox("Permitir uso dos meus dados para análises e melhorias do sistema", value=True)
    
    # Preferências alimentares detalhadas
    st.write("**🍽️ Preferências Alimentares Detalhadas**")
    
    food_preferences = st.multiselect(
        "Selecione suas preferências:",
        ["Vegetariano", "Vegano", "Low Carb", "Sem Glúten", "Sem Lactose", 
         "Mediterrânea", "Cetogênica", "Paleolítica", "Flexitariana", "Intermitente"],
        default=[]
    )
    
    foods_dislike = st.text_area("Alimentos que você não gosta:", 
                                 placeholder="Ex: brócolis, fígado, peixe...")
    
    cooking_skill = st.select_slider("Seu nível culinário:", 
                                   options=["Iniciante", "Básico", "Intermediário", "Avançado", "Chef"],
                                   value="Básico")
    
    cooking_time = st.select_slider("Tempo disponível para cozinhar:", 
                                  options=["Menos de 15min", "15-30min", "30-60min", "Mais de 1h"],
                                  value="15-30min")
    
    if st.button("💾 Salvar Preferências"):
        # Em um sistema real, salvaria no banco de dados
        st.success("✅ Suas preferências foram salvas com sucesso!")
        st.info("💡 Suas preferências ajudam seu nutricionista a criar planos mais personalizados para você.")

def show_system_analytics():
    """Analytics avançados do sistema para administradores"""
    st.markdown('<h1 class="main-header">📈 Analytics do Sistema</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "👥 Usuários", "💰 Financeiro", "🔮 Previsões"])
    
    with tab1:
        show_system_overview_analytics()
    
    with tab2:
        show_user_analytics()
    
    with tab3:
        show_financial_analytics()
    
    with tab4:
        show_predictive_analytics()

def show_system_overview_analytics():
    """Visão geral das analytics do sistema"""
    st.subheader("📊 Visão Geral do Sistema")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Período para análise
    col_period1, col_period2 = st.columns(2)
    with col_period1:
        analytics_start = st.date_input("Data início", value=date.today() - timedelta(days=30))
    with col_period2:
        analytics_end = st.date_input("Data fim", value=date.today())
    
    # KPIs principais
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    
    # Total de usuários ativos
    active_users = pd.read_sql_query("""
        SELECT COUNT(*) as count FROM users 
        WHERE active = 1 AND last_login >= ?
    """, conn, params=[analytics_start]).iloc[0]['count']
    
    # Total de consultas no período
    total_appointments = pd.read_sql_query("""
        SELECT COUNT(*) as count FROM appointments 
        WHERE DATE(appointment_date) BETWEEN ? AND ?
    """, conn, params=[analytics_start, analytics_end]).iloc[0]['count']
    
    # Taxa de crescimento de pacientes
    new_patients = pd.read_sql_query("""
        SELECT COUNT(*) as count FROM patients 
        WHERE DATE(created_at) BETWEEN ? AND ?
    """, conn, params=[analytics_start, analytics_end]).iloc[0]['count']
    
    # Receita total no período
    total_revenue = pd.read_sql_query("""
        SELECT COALESCE(SUM(amount), 0) as total FROM patient_financial 
        WHERE payment_status = 'pago' AND DATE(paid_date) BETWEEN ? AND ?
    """, conn, params=[analytics_start, analytics_end]).iloc[0]['total']
    
    with col_kpi1:
        st.metric("Usuários Ativos", active_users)
    
    with col_kpi2:
        st.metric("Consultas no Período", total_appointments)
    
    with col_kpi3:
        st.metric("Novos Pacientes", new_patients)
    
    with col_kpi4:
        st.metric("Receita Total", f"R$ {total_revenue:.2f}")
    
    # Gráficos de tendência
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Crescimento de usuários ao longo do tempo
        user_growth = pd.read_sql_query("""
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as new_users,
                SUM(COUNT(*)) OVER (ORDER BY DATE(created_at)) as cumulative_users
            FROM users
            WHERE DATE(created_at) BETWEEN ? AND ?
            GROUP BY DATE(created_at)
            ORDER BY date
        """, conn, params=[analytics_start, analytics_end])
        
        if not user_growth.empty:
            fig_growth = px.line(user_growth, x='date', y=['new_users', 'cumulative_users'],
                               title="Crescimento de Usuários", markers=True)
            st.plotly_chart(fig_growth, use_container_width=True)
    
    with col_chart2:
        # Taxa de utilização do sistema
        utilization_data = pd.read_sql_query("""
            SELECT 
                action_type,
                COUNT(*) as count
            FROM audit_log
            WHERE DATE(created_at) BETWEEN ? AND ?
            GROUP BY action_type
            ORDER BY count DESC
            LIMIT 10
        """, conn, params=[analytics_start, analytics_end])
        
        if not utilization_data.empty:
            fig_utilization = px.bar(utilization_data, x='action_type', y='count',
                                   title="Ações Mais Utilizadas")
            st.plotly_chart(fig_utilization, use_container_width=True)
    
    # Métricas de engajamento
    st.subheader("📱 Métricas de Engajamento")
    
    # Calcular métricas de engajamento
    engagement_metrics = pd.read_sql_query("""
        SELECT 
            COUNT(DISTINCT u.id) as total_users,
            COUNT(DISTINCT CASE WHEN al.created_at >= ? THEN u.id END) as active_users,
            AVG(CASE WHEN al.created_at >= ? THEN action_count END) as avg_actions_per_user
        FROM users u
        LEFT JOIN (
            SELECT user_id, COUNT(*) as action_count, MAX(created_at) as created_at
            FROM audit_log 
            GROUP BY user_id
        ) al ON al.user_id = u.id
    """, conn, params=[analytics_start, analytics_start])
    
    if not engagement_metrics.empty:
        metrics = engagement_metrics.iloc[0]
        
        col_eng1, col_eng2, col_eng3 = st.columns(3)
        
        with col_eng1:
            engagement_rate = (metrics['active_users'] / metrics['total_users'] * 100) if metrics['total_users'] > 0 else 0
            st.metric("Taxa de Engajamento", f"{engagement_rate:.1f}%")
        
        with col_eng2:
            st.metric("Usuários Ativos", metrics['active_users'])
        
        with col_eng3:
            st.metric("Ações Médias/Usuário", f"{metrics['avg_actions_per_user']:.1f}" if metrics['avg_actions_per_user'] else "0")
    
    conn.close()

def show_user_analytics():
    """Analytics detalhados de usuários"""
    st.subheader("👥 Analytics de Usuários")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Distribuição de usuários por papel
    user_distribution = pd.read_sql_query("""
        SELECT role, COUNT(*) as count, 
               COUNT(CASE WHEN active = 1 THEN 1 END) as active_count
        FROM users
        GROUP BY role
        ORDER BY count DESC
    """, conn)
    
    if not user_distribution.empty:
        col_dist1, col_dist2 = st.columns(2)
        
        with col_dist1:
            fig_dist = px.pie(user_distribution, values='count', names='role',
                            title="Distribuição de Usuários por Papel")
            st.plotly_chart(fig_dist, use_container_width=True)
        
        with col_dist2:
            # Tabela com dados detalhados
            display_dist = user_distribution.copy()
            display_dist['active_rate'] = (display_dist['active_count'] / display_dist['count'] * 100).round(1)
            display_dist.columns = ['Papel', 'Total', 'Ativos', 'Taxa Ativação (%)']
            st.dataframe(display_dist, use_container_width=True)
    
    # Atividade de usuários ao longo do tempo
    st.subheader("📈 Atividade ao Longo do Tempo")
    
    activity_timeline = pd.read_sql_query("""
        SELECT 
            DATE(al.created_at) as date,
            u.role,
            COUNT(*) as actions
        FROM audit_log al
        JOIN users u ON u.id = al.user_id
        WHERE al.created_at >= DATE('now', '-30 days')
        GROUP BY DATE(al.created_at), u.role
        ORDER BY date, u.role
    """, conn)
    
    if not activity_timeline.empty:
        fig_timeline = px.line(activity_timeline, x='date', y='actions', color='role',
                             title="Atividade Diária por Tipo de Usuário", markers=True)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Top usuários mais ativos
    st.subheader("🏆 Usuários Mais Ativos")
    
    top_active_users = pd.read_sql_query("""
        SELECT 
            u.full_name,
            u.role,
            COUNT(al.id) as total_actions,
            MAX(al.created_at) as last_activity
        FROM users u
        LEFT JOIN audit_log al ON al.user_id = u.id
        WHERE al.created_at >= DATE('now', '-30 days')
        GROUP BY u.id, u.full_name, u.role
        ORDER BY total_actions DESC
        LIMIT 10
    """, conn)
    
    if not top_active_users.empty:
        top_active_users['last_activity'] = pd.to_datetime(top_active_users['last_activity']).dt.strftime('%d/%m/%Y %H:%M')
        top_active_users.columns = ['Nome', 'Papel', 'Total Ações', 'Última Atividade']
        st.dataframe(top_active_users, use_container_width=True)
    
    # Análise de retenção
    st.subheader("📊 Análise de Retenção")
    
    retention_data = pd.read_sql_query("""
        SELECT 
            strftime('%Y-%m', created_at) as month,
            COUNT(*) as new_users,
            COUNT(CASE WHEN last_login >= DATE('now', '-7 days') THEN 1 END) as retained_users
        FROM users
        WHERE created_at >= DATE('now', '-6 months')
        GROUP BY strftime('%Y-%m', created_at)
        ORDER BY month
    """, conn)
    
    if not retention_data.empty:
        retention_data['retention_rate'] = (retention_data['retained_users'] / retention_data['new_users'] * 100).round(1)
        
        fig_retention = px.bar(retention_data, x='month', y=['new_users', 'retained_users'],
                             title="Novos Usuários vs Usuários Retidos")
        st.plotly_chart(fig_retention, use_container_width=True)
        
        st.write("**Taxa de Retenção por Mês:**")
        retention_display = retention_data[['month', 'retention_rate']].copy()
        retention_display.columns = ['Mês', 'Taxa Retenção (%)']
        st.dataframe(retention_display, use_container_width=True)
    
    conn.close()

def show_financial_analytics():
    """Analytics financeiros avançados"""
    st.subheader("💰 Analytics Financeiros")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Período para análise
    col_fin_period1, col_fin_period2 = st.columns(2)
    with col_fin_period1:
        fin_start = st.date_input("Período início", value=date.today() - timedelta(days=90), key="fin_analytics_start")
    with col_fin_period2:
        fin_end = st.date_input("Período fim", value=date.today(), key="fin_analytics_end")
    
    # Métricas financeiras principais
    financial_metrics = pd.read_sql_query("""
        SELECT 
            COUNT(*) as total_transactions,
            SUM(amount) as total_revenue,
            SUM(CASE WHEN payment_status = 'pago' THEN amount ELSE 0 END) as paid_revenue,
            SUM(CASE WHEN payment_status = 'pendente' THEN amount ELSE 0 END) as pending_revenue,
            AVG(amount) as avg_transaction_value
        FROM patient_financial
        WHERE DATE(created_at) BETWEEN ? AND ?
    """, conn, params=[fin_start, fin_end])
    
    if not financial_metrics.empty:
        metrics = financial_metrics.iloc[0]
        
        col_fin_metric1, col_fin_metric2, col_fin_metric3, col_fin_metric4 = st.columns(4)
        
        with col_fin_metric1:
            st.metric("Receita Total", f"R$ {metrics['total_revenue']:.2f}")
        
        with col_fin_metric2:
            st.metric("Receita Paga", f"R$ {metrics['paid_revenue']:.2f}")
        
        with col_fin_metric3:
            payment_rate = (metrics['paid_revenue'] / metrics['total_revenue'] * 100) if metrics['total_revenue'] > 0 else 0
            st.metric("Taxa Pagamento", f"{payment_rate:.1f}%")
        
        with col_fin_metric4:
            st.metric("Ticket Médio", f"R$ {metrics['avg_transaction_value']:.2f}")
    
    # Evolução da receita
    revenue_evolution = pd.read_sql_query("""
        SELECT 
            strftime('%Y-%m', created_at) as month,
            SUM(amount) as total_revenue,
            SUM(CASE WHEN payment_status = 'pago' THEN amount ELSE 0 END) as paid_revenue,
            COUNT(*) as transaction_count
        FROM patient_financial
        WHERE DATE(created_at) BETWEEN ? AND ?
        GROUP BY strftime('%Y-%m', created_at)
        ORDER BY month
    """, conn, params=[fin_start, fin_end])
    
    if not revenue_evolution.empty:
        fig_revenue = px.line(revenue_evolution, x='month', y=['total_revenue', 'paid_revenue'],
                            title="Evolução da Receita Mensal", markers=True)
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    # Receita por tipo de serviço
    col_service1, col_service2 = st.columns(2)
    
    with col_service1:
        service_revenue = pd.read_sql_query("""
            SELECT 
                service_type,
                SUM(amount) as revenue,
                COUNT(*) as count,
                AVG(amount) as avg_value
            FROM patient_financial
            WHERE DATE(created_at) BETWEEN ? AND ?
            GROUP BY service_type
            ORDER BY revenue DESC
        """, conn, params=[fin_start, fin_end])
        
        if not service_revenue.empty:
            fig_service = px.pie(service_revenue, values='revenue', names='service_type',
                               title="Receita por Tipo de Serviço")
            st.plotly_chart(fig_service, use_container_width=True)
    
    with col_service2:
        if not service_revenue.empty:
            service_display = service_revenue.copy()
            service_display['revenue'] = service_display['revenue'].apply(lambda x: f"R$ {x:.2f}")
            service_display['avg_value'] = service_display['avg_value'].apply(lambda x: f"R$ {x:.2f}")
            service_display.columns = ['Tipo Serviço', 'Receita Total', 'Quantidade', 'Valor Médio']
            st.dataframe(service_display, use_container_width=True)
    
    # Análise de inadimplência
    st.subheader("⚠️ Análise de Inadimplência")
    
    overdue_analysis = pd.read_sql_query("""
        SELECT 
            CASE 
                WHEN DATE(due_date) < DATE('now', '-30 days') THEN 'Mais de 30 dias'
                WHEN DATE(due_date) < DATE('now', '-7 days') THEN '7-30 dias'
                WHEN DATE(due_date) < DATE('now') THEN 'Até 7 dias'
                ELSE 'Em dia'
            END as overdue_category,
            COUNT(*) as count,
            SUM(amount) as amount
        FROM patient_financial
        WHERE payment_status = 'pendente'
        GROUP BY overdue_category
        ORDER BY amount DESC
    """, conn)
    
    if not overdue_analysis.empty:
        col_overdue1, col_overdue2 = st.columns(2)
        
        with col_overdue1:
            fig_overdue = px.bar(overdue_analysis, x='overdue_category', y='amount',
                               title="Valor em Atraso por Categoria")
            st.plotly_chart(fig_overdue, use_container_width=True)
        
        with col_overdue2:
            overdue_display = overdue_analysis.copy()
            overdue_display['amount'] = overdue_display['amount'].apply(lambda x: f"R$ {x:.2f}")
            overdue_display.columns = ['Categoria', 'Quantidade', 'Valor']
            st.dataframe(overdue_display, use_container_width=True)
    
    conn.close()

def show_predictive_analytics():
    """Analytics preditivos e insights"""
    st.subheader("🔮 Analytics Preditivos")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Previsão de crescimento
    st.write("**📈 Previsão de Crescimento de Pacientes**")
    
    # Dados históricos de crescimento
    growth_data = pd.read_sql_query("""
        SELECT 
            strftime('%Y-%m', created_at) as month,
            COUNT(*) as new_patients
        FROM patients
        WHERE created_at >= DATE('now', '-6 months')
        GROUP BY strftime('%Y-%m', created_at)
        ORDER BY month
    """, conn)
    
    if not growth_data.empty and len(growth_data) >= 3:
        # Calcular tendência simples (média móvel)
        growth_data['month_num'] = range(len(growth_data))
        
        # Regressão linear simples para previsão
        from sklearn.linear_model import LinearRegression
        import numpy as np
        
        X = growth_data['month_num'].values.reshape(-1, 1)
        y = growth_data['new_patients'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Prever próximos 3 meses
        future_months = np.array([[len(growth_data)], [len(growth_data)+1], [len(growth_data)+2]])
        predictions = model.predict(future_months)
        
        # Criar dados para visualização
        last_month = pd.to_datetime(growth_data.iloc[-1]['month'])
        future_dates = [
            (last_month + pd.DateOffset(months=1)).strftime('%Y-%m'),
            (last_month + pd.DateOffset(months=2)).strftime('%Y-%m'),
            (last_month + pd.DateOffset(months=3)).strftime('%Y-%m')
        ]
        
        # Combinar dados históricos e previsões
        all_data = growth_data[['month', 'new_patients']].copy()
        all_data['type'] = 'Histórico'
        
        for i, (date, pred) in enumerate(zip(future_dates, predictions)):
            pred_row = pd.DataFrame({
                'month': [date],
                'new_patients': [max(0, int(pred))],  # Não permitir valores negativos
                'type': ['Previsão']
            })
            all_data = pd.concat([all_data, pred_row], ignore_index=True)
        
        fig_prediction = px.line(all_data, x='month', y='new_patients', color='type',
                               title="Crescimento de Pacientes - Histórico vs Previsão",
                               markers=True)
        st.plotly_chart(fig_prediction, use_container_width=True)
        
        # Insights
        avg_growth = growth_data['new_patients'].mean()
        last_growth = growth_data['new_patients'].iloc[-1]
        trend = "crescente" if last_growth > avg_growth else "decrescente"
        
        st.info(f"""
        **📊 Insights de Crescimento:**
        - Média mensal de novos pacientes: {avg_growth:.1f}
        - Último mês: {last_growth} novos pacientes
        - Tendência: {trend}
        - Previsão próximo mês: {max(0, int(predictions[0]))} novos pacientes
        """)
    
    # Análise de churn (pacientes inativos)
    st.write("**📉 Análise de Churn de Pacientes**")
    
    churn_analysis = pd.read_sql_query("""
        SELECT 
            COUNT(CASE WHEN last_appointment IS NULL THEN 1 END) as never_returned,
            COUNT(CASE WHEN last_appointment < DATE('now', '-90 days') THEN 1 END) as inactive_90_days,
            COUNT(CASE WHEN last_appointment < DATE('now', '-60 days') THEN 1 END) as inactive_60_days,
            COUNT(CASE WHEN last_appointment < DATE('now', '-30 days') THEN 1 END) as inactive_30_days,
            COUNT(*) as total_patients
        FROM (
            SELECT 
                p.id,
                MAX(a.appointment_date) as last_appointment
            FROM patients p
            LEFT JOIN appointments a ON a.patient_id = p.id AND a.status = 'realizada'
            WHERE p.active = 1
            GROUP BY p.id
        )
    """, conn)
    
    if not churn_analysis.empty:
        churn = churn_analysis.iloc[0]
        
        col_churn1, col_churn2, col_churn3, col_churn4 = st.columns(4)
        
        with col_churn1:
            never_rate = (churn['never_returned'] / churn['total_patients'] * 100) if churn['total_patients'] > 0 else 0
            st.metric("Nunca Voltaram", f"{never_rate:.1f}%")
        
        with col_churn2:
            churn_90 = (churn['inactive_90_days'] / churn['total_patients'] * 100) if churn['total_patients'] > 0 else 0
            st.metric("Inativos 90+ dias", f"{churn_90:.1f}%")
        
        with col_churn3:
            churn_60 = (churn['inactive_60_days'] / churn['total_patients'] * 100) if churn['total_patients'] > 0 else 0
            st.metric("Inativos 60+ dias", f"{churn_60:.1f}%")
        
        with col_churn4:
            churn_30 = (churn['inactive_30_days'] / churn['total_patients'] * 100) if churn['total_patients'] > 0 else 0
            st.metric("Inativos 30+ dias", f"{churn_30:.1f}%")
    
    # Recomendações baseadas em dados
    st.write("**💡 Recomendações Inteligentes**")
    
    recommendations = []
    
    # Análise de inadimplência
    overdue_count = pd.read_sql_query("""
        SELECT COUNT(*) as count FROM patient_financial 
        WHERE payment_status = 'pendente' AND due_date < DATE('now')
    """, conn).iloc[0]['count']
    
    if overdue_count > 5:
        recommendations.append({
            'type': 'warning',
            'title': 'Alto Índice de Inadimplência',
            'message': f'{overdue_count} pagamentos em atraso. Considere implementar lembretes automáticos.',
            'action': 'Configurar notificações de cobrança'
        })
    
    # Análise de capacidade
    upcoming_appointments = pd.read_sql_query("""
        SELECT COUNT(*) as count FROM appointments 
        WHERE DATE(appointment_date) BETWEEN DATE('now') AND DATE('now', '+7 days')
        AND status = 'agendado'
    """, conn).iloc[0]['count']
    
    if upcoming_appointments < 10:
        recommendations.append({
            'type': 'info',
            'title': 'Baixa Ocupação na Próxima Semana',
            'message': f'Apenas {upcoming_appointments} consultas agendadas. Oportunidade para campanhas.',
            'action': 'Entrar em contato com pacientes inativos'
        })
    
    # Análise de crescimento
    if 'growth_data' in locals() and not growth_data.empty:
        recent_growth = growth_data['new_patients'].iloc[-2:].mean() if len(growth_data) >= 2 else 0
        if recent_growth > avg_growth * 1.2:
            recommendations.append({
                'type': 'success',
                'title': 'Crescimento Acelerado',
                'message': 'Crescimento acima da média. Considere expandir a equipe.',
                'action': 'Avaliar contratação de novos profissionais'
            })
    
    # Exibir recomendações
    for rec in recommendations:
        if rec['type'] == 'warning':
            st.warning(f"**{rec['title']}:** {rec['message']}\n\n*Ação sugerida: {rec['action']}*")
        elif rec['type'] == 'success':
            st.success(f"**{rec['title']}:** {rec['message']}\n\n*Ação sugerida: {rec['action']}*")
        else:
            st.info(f"**{rec['title']}:** {rec['message']}\n\n*Ação sugerida: {rec['action']}*")
    
    if not recommendations:
        st.success("✅ Sistema funcionando dentro dos parâmetros normais!")
    
    conn.close()

def show_advanced_reports():
    """Relatórios avançados para administradores"""
    st.markdown('<h1 class="main-header">📋 Relatórios Avançados</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Executivo", "📈 Operacional", "💰 Financeiro", "🔍 Auditoria"])
    
    with tab1:
        show_executive_report()
    
    with tab2:
        show_operational_report()
    
    with tab3:
        show_financial_executive_report()
    
    with tab4:
        show_audit_report()

def show_executive_report():
    """Relatório executivo consolidado"""
    st.subheader("📊 Relatório Executivo")
    
    # Período do relatório
    col_exec1, col_exec2 = st.columns(2)
    with col_exec1:
        exec_start = st.date_input("Período início", value=date.today().replace(day=1))
    with col_exec2:
        exec_end = st.date_input("Período fim", value=date.today())
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Resumo executivo
    st.write("## 📋 Resumo Executivo")
    
    # KPIs consolidados
    kpis = pd.read_sql_query("""
        SELECT 
            (SELECT COUNT(*) FROM users WHERE active = 1) as total_users,
            (SELECT COUNT(*) FROM patients WHERE active = 1) as total_patients,
            (SELECT COUNT(*) FROM appointments WHERE DATE(appointment_date) BETWEEN ? AND ?) as period_appointments,
            (SELECT COUNT(*) FROM appointments WHERE DATE(appointment_date) BETWEEN ? AND ? AND status = 'realizada') as completed_appointments,
            (SELECT COALESCE(SUM(amount), 0) FROM patient_financial WHERE payment_status = 'pago' AND DATE(paid_date) BETWEEN ? AND ?) as period_revenue,
            (SELECT COUNT(*) FROM patients WHERE DATE(created_at) BETWEEN ? AND ?) as new_patients
    """, conn, params=[exec_start, exec_end] * 3)
    
    if not kpis.empty:
        kpi_data = kpis.iloc[0]
        
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        
        with col_kpi1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>👥 Base de Usuários</h3>
                <p><strong>Total:</strong> {kpi_data['total_users']} usuários</p>
                <p><strong>Pacientes:</strong> {kpi_data['total_patients']}</p>
                <p><strong>Novos no período:</strong> {kpi_data['new_patients']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_kpi2:
            completion_rate = (kpi_data['completed_appointments'] / kpi_data['period_appointments'] * 100) if kpi_data['period_appointments'] > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <h3>📅 Operacional</h3>
                <p><strong>Consultas:</strong> {kpi_data['period_appointments']}</p>
                <p><strong>Realizadas:</strong> {kpi_data['completed_appointments']}</p>
                <p><strong>Taxa conclusão:</strong> {completion_rate:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_kpi3:
            avg_revenue = kpi_data['period_revenue'] / kpi_data['completed_appointments'] if kpi_data['completed_appointments'] > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <h3>💰 Financeiro</h3>
                <p><strong>Receita:</strong> R$ {kpi_data['period_revenue']:.2f}</p>
                <p><strong>Ticket médio:</strong> R$ {avg_revenue:.2f}</p>
                <p><strong>Consultas pagas:</strong> {kpi_data['completed_appointments']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Gráficos executivos
    st.write("## 📈 Indicadores de Performance")
    
    col_chart_exec1, col_chart_exec2 = st.columns(2)
    
    with col_chart_exec1:
        # Performance por nutricionista
        nutritionist_performance = pd.read_sql_query("""
            SELECT 
                u.full_name,
                COUNT(DISTINCT p.id) as total_patients,
                COUNT(DISTINCT a.id) as total_appointments,
                COALESCE(SUM(pf.amount), 0) as revenue
            FROM users u
            LEFT JOIN patients p ON p.nutritionist_id = u.id
            LEFT JOIN appointments a ON a.nutritionist_id = u.id AND DATE(a.appointment_date) BETWEEN ? AND ?
            LEFT JOIN patient_financial pf ON pf.patient_id = p.id AND pf.payment_status = 'pago'
            WHERE u.role = 'nutritionist' AND u.active = 1
            GROUP BY u.id, u.full_name
            ORDER BY revenue DESC
        """, conn, params=[exec_start, exec_end])
        
        if not nutritionist_performance.empty:
            fig_perf = px.bar(nutritionist_performance, x='full_name', y='revenue',
                            title="Performance por Nutricionista (Receita)")
            st.plotly_chart(fig_perf, use_container_width=True)
    
    with col_chart_exec2:
        # Evolução mensal
        monthly_evolution = pd.read_sql_query("""
            SELECT 
                strftime('%Y-%m', appointment_date) as month,
                COUNT(*) as appointments,
                COUNT(CASE WHEN status = 'realizada' THEN 1 END) as completed
            FROM appointments
            WHERE appointment_date >= DATE('now', '-6 months')
            GROUP BY strftime('%Y-%m', appointment_date)
            ORDER BY month
        """, conn)
        
        if not monthly_evolution.empty:
            fig_evolution = px.line(monthly_evolution, x='month', y=['appointments', 'completed'],
                                  title="Evolução Mensal de Consultas", markers=True)
            st.plotly_chart(fig_evolution, use_container_width=True)
    
    # Recomendações estratégicas
    st.write("## 💡 Recomendações Estratégicas")
    
    # Análise de crescimento
    growth_rate = (kpi_data['new_patients'] / max(kpi_data['total_patients'] - kpi_data['new_patients'], 1)) * 100 if 'kpi_data' in locals() else 0
    
    if growth_rate > 20:
        st.success(f"📈 **Crescimento Acelerado**: {growth_rate:.1f}% de crescimento no período. Considere expandir a equipe e infraestrutura.")
    elif growth_rate > 10:
        st.info(f"📊 **Crescimento Saudável**: {growth_rate:.1f}% de crescimento. Mantenha as estratégias atuais.")
    else:
        st.warning(f"⚠️ **Crescimento Baixo**: {growth_rate:.1f}% de crescimento. Revise estratégias de marketing e retenção.")
    
    # Análise de eficiência operacional
    if 'completion_rate' in locals() and completion_rate < 80:
        st.warning("⚠️ **Eficiência Operacional**: Taxa de conclusão baixa. Revise processos de agendamento e follow-up.")
    elif 'completion_rate' in locals() and completion_rate > 90:
        st.success("✅ **Excelente Eficiência**: Alta taxa de conclusão de consultas. Parabéns à equipe!")
    
    conn.close()

def show_operational_report():
    """Relatório operacional detalhado"""
    st.subheader("📈 Relatório Operacional")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Utilização da agenda
    st.write("## 📅 Utilização da Agenda")
    
    agenda_utilization = pd.read_sql_query("""
        SELECT 
            u.full_name as nutritionist,
            COUNT(a.id) as total_slots,
            COUNT(CASE WHEN a.status = 'realizada' THEN 1 END) as used_slots,
            COUNT(CASE WHEN a.status = 'cancelado' THEN 1 END) as cancelled_slots,
            AVG(a.duration) as avg_duration
        FROM users u
        LEFT JOIN appointments a ON a.nutritionist_id = u.id AND a.appointment_date >= DATE('now', '-30 days')
        WHERE u.role = 'nutritionist' AND u.active = 1
        GROUP BY u.id, u.full_name
        ORDER BY total_slots DESC
    """, conn)
    
    if not agenda_utilization.empty:
        agenda_utilization['utilization_rate'] = (agenda_utilization['used_slots'] / agenda_utilization['total_slots'] * 100).fillna(0)
        
        fig_util = px.bar(agenda_utilization, x='nutritionist', y='utilization_rate',
                         title="Taxa de Utilização da Agenda por Nutricionista (%)")
        st.plotly_chart(fig_util, use_container_width=True)
        
        # Tabela detalhada
        util_display = agenda_utilization[['nutritionist', 'total_slots', 'used_slots', 'cancelled_slots', 'utilization_rate', 'avg_duration']].copy()
        util_display['utilization_rate'] = util_display['utilization_rate'].round(1)
        util_display['avg_duration'] = util_display['avg_duration'].fillna(0).round(0)
        util_display.columns = ['Nutricionista', 'Total Slots', 'Utilizados', 'Cancelados', 'Taxa Utilização (%)', 'Duração Média (min)']
        st.dataframe(util_display, use_container_width=True)
    
    # Análise de no-show
    st.write("## 🚫 Análise de No-Show")
    
    no_show_analysis = pd.read_sql_query("""
        SELECT 
            strftime('%Y-%m', appointment_date) as month,
            COUNT(*) as total_appointments,
            COUNT(CASE WHEN status = 'cancelado' THEN 1 END) as no_shows,
            COUNT(CASE WHEN status = 'realizada' THEN 1 END) as completed
        FROM appointments
        WHERE appointment_date >= DATE('now', '-6 months')
        GROUP BY strftime('%Y-%m', appointment_date)
        ORDER BY month
    """, conn)
    
    if not no_show_analysis.empty:
        no_show_analysis['no_show_rate'] = (no_show_analysis['no_shows'] / no_show_analysis['total_appointments'] * 100).round(1)
        
        fig_noshow = px.line(no_show_analysis, x='month', y='no_show_rate',
                           title="Taxa de No-Show Mensal (%)", markers=True)
        st.plotly_chart(fig_noshow, use_container_width=True)
        
        avg_no_show = no_show_analysis['no_show_rate'].mean()
        if avg_no_show > 20:
            st.warning(f"⚠️ Taxa de no-show alta: {avg_no_show:.1f}%. Considere implementar lembretes automáticos.")
        elif avg_no_show > 10:
            st.info(f"📊 Taxa de no-show moderada: {avg_no_show:.1f}%. Monitore e implemente melhorias.")
        else:
            st.success(f"✅ Taxa de no-show baixa: {avg_no_show:.1f}%. Excelente gestão!")
    
    # Produtividade por período
    st.write("## ⏰ Produtividade por Horário")
    
    hourly_productivity = pd.read_sql_query("""
        SELECT 
            strftime('%H', appointment_date) as hour,
            COUNT(*) as appointments,
            COUNT(CASE WHEN status = 'realizada' THEN 1 END) as completed,
            AVG(duration) as avg_duration
        FROM appointments
        WHERE appointment_date >= DATE('now', '-30 days')
        GROUP BY strftime('%H', appointment_date)
        ORDER BY hour
    """, conn)
    
    if not hourly_productivity.empty:
        hourly_productivity['completion_rate'] = (hourly_productivity['completed'] / hourly_productivity['appointments'] * 100).round(1)
        
        fig_hourly = px.bar(hourly_productivity, x='hour', y='appointments',
                          title="Distribuição de Consultas por Horário")
        st.plotly_chart(fig_hourly, use_container_width=True)
        
        # Identificar horários de pico
        peak_hour = hourly_productivity.loc[hourly_productivity['appointments'].idxmax(), 'hour']
        peak_appointments = hourly_productivity['appointments'].max()
        
        st.info(f"📊 **Horário de pico**: {peak_hour}:00 com {peak_appointments} consultas")
    
    conn.close()

def show_financial_executive_report():
    """Relatório financeiro executivo"""
    st.subheader("💰 Relatório Financeiro Executivo")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Período do relatório
    col_fin_exec1, col_fin_exec2 = st.columns(2)
    with col_fin_exec1:
        fin_exec_start = st.date_input("Data início", value=date.today() - timedelta(days=90), key="fin_exec_start")
    with col_fin_exec2:
        fin_exec_end = st.date_input("Data fim", value=date.today(), key="fin_exec_end")
    
    # Resumo financeiro
    financial_summary = pd.read_sql_query("""
        SELECT 
            SUM(amount) as total_billed,
            SUM(CASE WHEN payment_status = 'pago' THEN amount ELSE 0 END) as total_received,
            SUM(CASE WHEN payment_status = 'pendente' THEN amount ELSE 0 END) as total_pending,
            COUNT(*) as total_transactions,
            COUNT(DISTINCT patient_id) as unique_patients,
            AVG(amount) as avg_transaction_value
        FROM patient_financial
        WHERE DATE(created_at) BETWEEN ? AND ?
    """, conn, params=[fin_exec_start, fin_exec_end])
    
    if not financial_summary.empty:
        summary = financial_summary.iloc[0]
        
        st.write("## 💼 Resumo Financeiro")
        
        col_summary1, col_summary2, col_summary3 = st.columns(3)
        
        with col_summary1:
            collection_rate = (summary['total_received'] / summary['total_billed'] * 100) if summary['total_billed'] > 0 else 0
            st.markdown(f"""
            <div class="financial-card">
                <h4>📊 Performance de Cobrança</h4>
                <p><strong>Faturado:</strong> R$ {summary['total_billed']:.2f}</p>
                <p><strong>Recebido:</strong> R$ {summary['total_received']:.2f}</p>
                <p><strong>Taxa cobrança:</strong> {collection_rate:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_summary2:
            revenue_per_patient = summary['total_received'] / summary['unique_patients'] if summary['unique_patients'] > 0 else 0
            st.markdown(f"""
            <div class="financial-card">
                <h4>👥 Receita por Paciente</h4>
                <p><strong>Pacientes únicos:</strong> {summary['unique_patients']}</p>
                <p><strong>Receita/paciente:</strong> R$ {revenue_per_patient:.2f}</p>
                <p><strong>Ticket médio:</strong> R$ {summary['avg_transaction_value']:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_summary3:
            st.markdown(f"""
            <div class="financial-card">
                <h4>💰 Valores Pendentes</h4>
                <p><strong>Total pendente:</strong> R$ {summary['total_pending']:.2f}</p>
                <p><strong>% do faturado:</strong> {(summary['total_pending']/summary['total_billed']*100):.1f}%</p>
                <p><strong>Transações:</strong> {summary['total_transactions']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Análise de lucratividade por serviço
    st.write("## 📈 Lucratividade por Serviço")
    
    service_profitability = pd.read_sql_query("""
        SELECT 
            service_type,
            COUNT(*) as quantity,
            SUM(amount) as total_revenue,
            AVG(amount) as avg_price,
            SUM(CASE WHEN payment_status = 'pago' THEN amount ELSE 0 END) as received_revenue,
            (SUM(CASE WHEN payment_status = 'pago' THEN amount ELSE 0 END) / SUM(amount) * 100) as collection_rate
        FROM patient_financial
        WHERE DATE(created_at) BETWEEN ? AND ?
        GROUP BY service_type
        ORDER BY total_revenue DESC
    """, conn, params=[fin_exec_start, fin_exec_end])
    
    if not service_profitability.empty:
        # Gráfico de receita por serviço
        fig_service_revenue = px.bar(service_profitability, x='service_type', y='total_revenue',
                                   title="Receita Total por Tipo de Serviço")
        st.plotly_chart(fig_service_revenue, use_container_width=True)
        
        # Tabela detalhada
        service_display = service_profitability.copy()
        service_display['total_revenue'] = service_display['total_revenue'].apply(lambda x: f"R$ {x:.2f}")
        service_display['avg_price'] = service_display['avg_price'].apply(lambda x: f"R$ {x:.2f}")
        service_display['received_revenue'] = service_display['received_revenue'].apply(lambda x: f"R$ {x:.2f}")
        service_display['collection_rate'] = service_display['collection_rate'].apply(lambda x: f"{x:.1f}%")
        service_display.columns = ['Tipo de Serviço', 'Quantidade', 'Receita Total', 'Preço Médio', 'Receita Recebida', 'Taxa Cobrança']
        st.dataframe(service_display, use_container_width=True)
    
    # Fluxo de caixa projetado
    st.write("## 💸 Fluxo de Caixa")
    
    cash_flow = pd.read_sql_query("""
        SELECT 
            DATE(due_date) as due_date,
            SUM(CASE WHEN payment_status = 'pendente' THEN amount ELSE 0 END) as expected_inflow,
            SUM(CASE WHEN payment_status = 'pago' AND DATE(paid_date) = DATE(due_date) THEN amount ELSE 0 END) as actual_inflow
        FROM patient_financial
        WHERE due_date BETWEEN DATE('now') AND DATE('now', '+30 days')
        GROUP BY DATE(due_date)
        ORDER BY due_date
    """, conn)
    
    if not cash_flow.empty:
        fig_cashflow = px.line(cash_flow, x='due_date', y=['expected_inflow', 'actual_inflow'],
                             title="Fluxo de Caixa - Próximos 30 Dias", markers=True)
        st.plotly_chart(fig_cashflow, use_container_width=True)
        
        total_expected = cash_flow['expected_inflow'].sum()
        st.info(f"💰 **Receita esperada nos próximos 30 dias**: R$ {total_expected:.2f}")
    
    conn.close()

def show_audit_report():
    """Relatório de auditoria consolidado"""
    st.subheader("🔍 Relatório de Auditoria")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Período do relatório
    col_audit1, col_audit2 = st.columns(2)
    with col_audit1:
        audit_start = st.date_input("Data início", value=date.today() - timedelta(days=30), key="audit_report_start")
    with col_audit2:
        audit_end = st.date_input("Data fim", value=date.today(), key="audit_report_end")
    
    # Resumo de atividades
    st.write("## 📊 Resumo de Atividades")
    
    activity_summary = pd.read_sql_query("""
        SELECT 
            COUNT(*) as total_actions,
            COUNT(DISTINCT user_id) as active_users,
            COUNT(DISTINCT DATE(created_at)) as active_days
        FROM audit_log
        WHERE DATE(created_at) BETWEEN ? AND ?
    """, conn, params=[audit_start, audit_end])
    
    if not activity_summary.empty:
        summary = activity_summary.iloc[0]
        
        col_audit_summary1, col_audit_summary2, col_audit_summary3 = st.columns(3)
        
        with col_audit_summary1:
            st.metric("Total de Ações", summary['total_actions'])
        
        with col_audit_summary2:
            st.metric("Usuários Ativos", summary['active_users'])
        
        with col_audit_summary3:
            avg_actions_day = summary['total_actions'] / summary['active_days'] if summary['active_days'] > 0 else 0
            st.metric("Ações Médias/Dia", f"{avg_actions_day:.1f}")
    
    # Ações por tipo
    actions_by_type = pd.read_sql_query("""
        SELECT 
            action_type,
            COUNT(*) as count,
            COUNT(DISTINCT user_id) as unique_users
        FROM audit_log
        WHERE DATE(created_at) BETWEEN ? AND ?
        GROUP BY action_type
        ORDER BY count DESC
    """, conn, params=[audit_start, audit_end])
    
    if not actions_by_type.empty:
        col_audit_chart1, col_audit_chart2 = st.columns(2)
        
        with col_audit_chart1:
            fig_actions = px.pie(actions_by_type, values='count', names='action_type',
                                title="Distribuição de Ações por Tipo")
            st.plotly_chart(fig_actions, use_container_width=True)
        
        with col_audit_chart2:
            actions_display = actions_by_type.copy()
            actions_display.columns = ['Tipo de Ação', 'Quantidade', 'Usuários Únicos']
            st.dataframe(actions_display, use_container_width=True)
    
    # Atividade por usuário
    st.write("## 👥 Atividade por Usuário")
    
    user_activity = pd.read_sql_query("""
        SELECT 
            u.full_name,
            u.role,
            COUNT(al.id) as total_actions,
            MAX(al.created_at) as last_activity
        FROM audit_log al
        JOIN users u ON u.id = al.user_id
        WHERE DATE(al.created_at) BETWEEN ? AND ?
        GROUP BY u.id, u.full_name, u.role
        ORDER BY total_actions DESC
        LIMIT 20
    """, conn, params=[audit_start, audit_end])
    
    if not user_activity.empty:
        user_activity['last_activity'] = pd.to_datetime(user_activity['last_activity']).dt.strftime('%d/%m/%Y %H:%M')
        user_activity.columns = ['Nome', 'Papel', 'Total Ações', 'Última Atividade']
        st.dataframe(user_activity, use_container_width=True)
    
    # Timeline de atividades críticas
    st.write("## ⚠️ Atividades Críticas")
    
    critical_actions = pd.read_sql_query("""
        SELECT 
            al.created_at,
            al.action_type,
            u.full_name,
            u.role,
            al.table_affected,
            al.record_id
        FROM audit_log al
        JOIN users u ON u.id = al.user_id
        WHERE DATE(al.created_at) BETWEEN ? AND ?
        AND (al.action_type LIKE '%delete%' OR al.action_type LIKE '%deactivate%' OR al.action_type LIKE '%admin%')
        ORDER BY al.created_at DESC
        LIMIT 50
    """, conn, params=[audit_start, audit_end])
    
    if not critical_actions.empty:
        for idx, action in critical_actions.iterrows():
            timestamp = pd.to_datetime(action['created_at']).strftime('%d/%m/%Y %H:%M:%S')
            
            st.markdown(f"""
            <div style="border-left: 4px solid #F44336; padding: 0.5rem; margin: 0.3rem 0; background: #FFEBEE; border-radius: 5px;">
                <strong>⚠️ {action['action_type'].replace('_', ' ').title()}</strong><br>
                <small><strong>Usuário:</strong> {action['full_name']} ({action['role']}) | 
                <strong>Data:</strong> {timestamp}</small><br>
                {f"<small><strong>Tabela:</strong> {action['table_affected']} | <strong>ID:</strong> {action['record_id']}</small>" if action['table_affected'] else ""}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ Nenhuma atividade crítica detectada no período.")
    
    # Relatório de conformidade
    st.write("## ✅ Conformidade e Segurança")
    
    compliance_check = {
        "Logins sem logout correspondente": pd.read_sql_query("""
            SELECT COUNT(*) as count FROM audit_log al1
            WHERE al1.action_type = 'login' 
            AND DATE(al1.created_at) BETWEEN ? AND ?
            AND NOT EXISTS (
                SELECT 1 FROM audit_log al2 
                WHERE al2.user_id = al1.user_id 
                AND al2.action_type = 'logout' 
                AND al2.created_at > al1.created_at
            )
        """, conn, params=[audit_start, audit_end]).iloc[0]['count'],
        
        "Ações fora do horário comercial": pd.read_sql_query("""
            SELECT COUNT(*) as count FROM audit_log
            WHERE DATE(created_at) BETWEEN ? AND ?
            AND (strftime('%H', created_at) < '08' OR strftime('%H', created_at) > '18')
        """, conn, params=[audit_start, audit_end]).iloc[0]['count'],
        
        "Múltiplos logins mesmo usuário": pd.read_sql_query("""
            SELECT COUNT(DISTINCT user_id) as count FROM (
                SELECT user_id, DATE(created_at) as date, COUNT(*) as logins
                FROM audit_log
                WHERE action_type = 'login' AND DATE(created_at) BETWEEN ? AND ?
                GROUP BY user_id, DATE(created_at)
                HAVING COUNT(*) > 3
            )
        """, conn, params=[audit_start, audit_end]).iloc[0]['count']
    }
    
    for check_name, check_value in compliance_check.items():
        if check_value > 0:
            st.warning(f"⚠️ **{check_name}**: {check_value} ocorrências")
        else:
            st.success(f"✅ **{check_name}**: Nenhuma ocorrência")
    
    conn.close()

# Implementar as últimas funcionalidades que ainda não foram completadas
def show_notifications_admin():
    """Sistema de notificações para administradores"""
    st.markdown('<h1 class="main-header">📧 Centro de Notificações</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📬 Notificações Ativas", "⚙️ Configurar", "📊 Relatório"])
    
    with tab1:
        show_active_notifications()
    
    with tab2:
        configure_notifications()
    
    with tab3:
        show_notifications_report()

def show_active_notifications():
    """Exibe notificações ativas do sistema"""
    st.subheader("📬 Notificações Ativas")
    
    # Simular notificações do sistema
    system_notifications = [
        {
            'type': 'warning',
            'title': 'Backup Pendente',
            'message': 'Último backup realizado há 2 dias. Considere executar backup manual.',
            'timestamp': datetime.now() - timedelta(hours=2),
            'priority': 'Alta',
            'category': 'Sistema'
        },
        {
            'type': 'info',
            'title': 'Novos Usuários',
            'message': '3 novos pacientes cadastrados hoje.',
            'timestamp': datetime.now() - timedelta(minutes=30),
            'priority': 'Baixa',
            'category': 'Operacional'
        },
        {
            'type': 'success',
            'title': 'Receita do Dia',
            'message': 'Meta diária de receita atingida: R$ 1.200,00.',
            'timestamp': datetime.now() - timedelta(minutes=10),
            'priority': 'Média',
            'category': 'Financeiro'
        },
        {
            'type': 'error',
            'title': 'Falha na Sincronização',
            'message': 'Erro ao sincronizar dados com sistema externo.',
            'timestamp': datetime.now() - timedelta(hours=1),
            'priority': 'Crítica',
            'category': 'Técnico'
        }
    ]
    
    # Filtros
    col_notif_filter1, col_notif_filter2 = st.columns(2)
    
    with col_notif_filter1:
        priority_filter = st.selectbox("Filtrar por prioridade:", 
                                     ["Todas", "Crítica", "Alta", "Média", "Baixa"])
    
    with col_notif_filter2:
        category_filter = st.selectbox("Filtrar por categoria:",
                                     ["Todas", "Sistema", "Operacional", "Financeiro", "Técnico"])
    
    # Exibir notificações
    for notification in system_notifications:
        # Aplicar filtros
        if priority_filter != "Todas" and notification['priority'] != priority_filter:
            continue
        if category_filter != "Todas" and notification['category'] != category_filter:
            continue
        
        # Cores por tipo
        colors = {
            'error': '#F44336',
            'warning': '#FF9800', 
            'info': '#2196F3',
            'success': '#4CAF50'
        }
        
        # Ícones por tipo
        icons = {
            'error': '🚨',
            'warning': '⚠️',
            'info': 'ℹ️', 
            'success': '✅'
        }
        
        color = colors[notification['type']]
        icon = icons[notification['type']]
        time_str = notification['timestamp'].strftime('%d/%m/%Y %H:%M')
        
        col_notif1, col_notif2 = st.columns([4, 1])
        
        with col_notif1:
            st.markdown(f"""
            <div style="border-left: 4px solid {color}; padding: 1rem; margin: 0.5rem 0; 
                        background: white; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                <h5 style="margin: 0; color: {color};">{icon} {notification['title']}</h5>
                <p style="margin: 0.3rem 0;">{notification['message']}</p>
                <small><strong>Categoria:</strong> {notification['category']} | 
                       <strong>Prioridade:</strong> {notification['priority']} | 
                       <strong>Data:</strong> {time_str}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col_notif2:
            if st.button("🗑️ Marcar como Lida", key=f"mark_read_{notification['title']}"):
                st.success("Notificação marcada como lida!")

def configure_notifications():
    """Configurar sistema de notificações"""
    st.subheader("⚙️ Configurar Notificações")
    
    # Configurações por categoria
    st.write("**📊 Notificações do Sistema**")
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        system_alerts = st.checkbox("Alertas do sistema", value=True)
        backup_alerts = st.checkbox("Alertas de backup", value=True)
        security_alerts = st.checkbox("Alertas de segurança", value=True)
        performance_alerts = st.checkbox("Alertas de performance", value=False)
    
    with col_config2:
        financial_alerts = st.checkbox("Alertas financeiros", value=True)
        user_alerts = st.checkbox("Alertas de usuários", value=False)
        appointment_alerts = st.checkbox("Alertas de agendamento", value=True)
        data_alerts = st.checkbox("Alertas de dados", value=False)
    
    # Configurações de entrega
    st.write("**📧 Métodos de Entrega**")
    
    col_delivery1, col_delivery2 = st.columns(2)
    
    with col_delivery1:
        email_notifications = st.checkbox("Notificações por email", value=True)
        if email_notifications:
            admin_email = st.text_input("Email do administrador", value="admin@nutriapp360.com")
    
    with col_delivery2:
        dashboard_notifications = st.checkbox("Notificações no dashboard", value=True)
        push_notifications = st.checkbox("Notificações push (futuro)", value=False)
    
    # Configurações de frequência
    st.write("**⏰ Frequência de Notificações**")
    
    notification_frequency = st.selectbox("Frequência de verificação:", [
        "Tempo Real", "A cada 5 minutos", "A cada 15 minutos", 
        "A cada hora", "Diariamente"
    ])
    
    digest_frequency = st.selectbox("Resumo diário:", [
        "Desabilitado", "Diário às 8h", "Diário às 18h", "Semanal"
    ])
    
    # Configurações avançadas
    st.write("**🔧 Configurações Avançadas**")
    
    col_advanced1, col_advanced2 = st.columns(2)
    
    with col_advanced1:
        critical_threshold = st.number_input("Limite para alertas críticos", value=5)
        warning_threshold = st.number_input("Limite para avisos", value=10)
    
    with col_advanced2:
        max_notifications_day = st.number_input("Máximo notificações/dia", value=50)
        auto_resolve = st.checkbox("Auto-resolver notificações antigas", value=True)
    
    if st.button("💾 Salvar Configurações de Notificação"):
        st.success("✅ Configurações de notificação salvas com sucesso!")
        st.info("🔔 As novas configurações entrarão em vigor nos próximos 5 minutos.")

def show_notifications_report():
    """Relatório de notificações"""
    st.subheader("📊 Relatório de Notificações")
    
    # Período do relatório
    col_report1, col_report2 = st.columns(2)
    with col_report1:
        report_start = st.date_input("Data início", value=date.today() - timedelta(days=30), key="notif_report_start")
    with col_report2:
        report_end = st.date_input("Data fim", value=date.today(), key="notif_report_end")
    
    # Simular dados de notificações
    notification_stats = {
        'total_sent': 247,
        'total_read': 198,
        'total_critical': 12,
        'total_warnings': 89,
        'total_info': 146,
        'avg_response_time': 2.3  # horas
    }
    
    # Métricas principais
    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
    
    with col_stats1:
        st.metric("Total Enviadas", notification_stats['total_sent'])
    
    with col_stats2:
        read_rate = (notification_stats['total_read'] / notification_stats['total_sent'] * 100)
        st.metric("Taxa de Leitura", f"{read_rate:.1f}%")
    
    with col_stats3:
        st.metric("Críticas", notification_stats['total_critical'])
    
    with col_stats4:
        st.metric("Tempo Resposta Médio", f"{notification_stats['avg_response_time']:.1f}h")
    
    # Distribuição por tipo
    notification_types = pd.DataFrame({
        'Tipo': ['Crítica', 'Aviso', 'Informação'],
        'Quantidade': [notification_stats['total_critical'], 
                      notification_stats['total_warnings'], 
                      notification_stats['total_info']]
    })
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig_types = px.pie(notification_types, values='Quantidade', names='Tipo',
                          title="Distribuição por Tipo de Notificação")
        st.plotly_chart(fig_types, use_container_width=True)
    
    with col_chart2:
        # Simulação de tendência temporal
        dates = pd.date_range(start=report_start, end=report_end, freq='D')
        daily_notifications = pd.DataFrame({
            'Data': dates,
            'Notificações': np.random.poisson(8, len(dates))  # Média de 8 notificações por dia
        })
        
        fig_trend = px.line(daily_notifications, x='Data', y='Notificações',
                          title="Tendência Diária de Notificações", markers=True)
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Top categorias de notificação
    top_categories = pd.DataFrame({
        'Categoria': ['Sistema', 'Financeiro', 'Agendamento', 'Usuários', 'Backup'],
        'Quantidade': [67, 45, 38, 32, 28],
        'Taxa Resolução': [95.5, 88.9, 92.1, 87.5, 100.0]
    })
    
    st.write("**📊 Top Categorias de Notificação**")
    st.dataframe(top_categories, use_container_width=True)
    
    # Recomendações
    st.write("**💡 Recomendações**")
    
    if read_rate < 80:
        st.warning("📧 Taxa de leitura baixa. Considere revisar a relevância das notificações.")
    else:
        st.success("✅ Boa taxa de leitura de notificações!")
    
    if notification_stats['avg_response_time'] > 4:
        st.warning("⏰ Tempo de resposta alto. Considere aumentar a prioridade de alertas críticos.")
    else:
        st.info("📊 Tempo de resposta dentro do esperado.")

# Função principal executando o sistema completo
if __name__ == "__main__":
    main()

def register_patient_progress(nutritionist_id):
    """Registra progresso de paciente"""
    st.subheader("➕ Registrar Progresso do Paciente")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Selecionar paciente
    patients_df = pd.read_sql_query("""
        SELECT id, full_name, patient_id FROM patients 
        WHERE nutritionist_id = ? AND active = 1
        ORDER BY full_name
    """, conn, params=[nutritionist_id])
    
    if patients_df.empty:
        st.warning("Você não possui pacientes cadastrados.")
        conn.close()
        return
    
    selected_patient = st.selectbox(
        "Selecione o paciente:",
        options=patients_df['id'].tolist(),
        format_func=lambda x: f"{patients_df[patients_df['id'] == x]['full_name'].iloc[0]} ({patients_df[patients_df['id'] == x]['patient_id'].iloc[0]})"
    )
    
    # Buscar último registro do paciente
    last_progress = pd.read_sql_query("""
        SELECT * FROM patient_progress 
        WHERE patient_id = ?
        ORDER BY record_date DESC
        LIMIT 1
    """, conn, params=[selected_patient])
    
    # Exibir último registro
    if not last_progress.empty:
        last_record = last_progress.iloc[0]
        last_date = pd.to_datetime(last_record['record_date']).strftime('%d/%m/%Y')
        
        st.info(f"""
        **📊 Último registro ({last_date}):**
        • Peso: {last_record['weight']}kg
        • % Gordura: {last_record['body_fat'] or 'N/A'}
        • % Músculo: {last_record['muscle_mass'] or 'N/A'}
        """)
    
    # Formulário de registro
    with st.form("progress_form"):
        col_prog1, col_prog2 = st.columns(2)
        
        with col_prog1:
            record_date = st.date_input("Data do registro", value=date.today())
            weight = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)
            body_fat = st.number_input("% Gordura corporal (opcional)", min_value=0.0, max_value=50.0, value=0.0, step=0.1)
        
        with col_prog2:
            muscle_mass = st.number_input("% Massa muscular (opcional)", min_value=0.0, max_value=70.0, value=0.0, step=0.1)
            waist = st.number_input("Circunferência cintura (cm, opcional)", min_value=0.0, value=0.0, step=0.1)
            hip = st.number_input("Circunferência quadril (cm, opcional)", min_value=0.0, value=0.0, step=0.1)
        
        notes = st.text_area("Observações", placeholder="Ex: Paciente relatou mais disposição, melhor qualidade do sono...")
        
        submit_progress = st.form_submit_button("💾 Salvar Progresso")
        
        if submit_progress:
            try:
                cursor = conn.cursor()
                
                # Ajustar valores zero para None
                body_fat_value = body_fat if body_fat > 0 else None
                muscle_mass_value = muscle_mass if muscle_mass > 0 else None
                waist_value = waist if waist > 0 else None
                hip_value = hip if hip > 0 else None
                
                cursor.execute('''
                    INSERT INTO patient_progress (
                        patient_id, record_date, weight, body_fat, muscle_mass,
                        waist_circumference, hip_circumference, notes, recorded_by
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    selected_patient, record_date, weight, body_fat_value, muscle_mass_value,
                    waist_value, hip_value, notes, nutritionist_id
                ))
                
                # Atualizar pontos do paciente
                award_points_for_progress(selected_patient, weight, last_progress)
                
                conn.commit()
                log_audit_action(nutritionist_id, 'register_progress', 'patient_progress', cursor.lastrowid)
                st.success("✅ Progresso registrado com sucesso!")
                st.rerun()
            
            except Exception as e:
                st.error(f"❌ Erro ao registrar progresso: {e}")
    
    conn.close()

def award_points_for_progress(patient_id, current_weight, last_progress_df):
    """Premia paciente com pontos baseado no progresso"""
    try:
        conn = sqlite3.connect('nutriapp360.db')
        cursor = conn.cursor()
        
        points_to_award = 5  # Pontos base por registro
        badge_awarded = None
        
        # Verificar se perdeu peso
        if not last_progress_df.empty:
            last_weight = last_progress_df.iloc[0]['weight']
            if last_weight and current_weight < last_weight:
                weight_loss = last_weight - current_weight
                if weight_loss >= 1.0:  # Perdeu 1kg ou mais
                    points_to_award += 25
                    badge_awarded = {
                        'name': 'Perda de Peso',
                        'description': f'Perdeu {weight_loss:.1f}kg de forma saudável',
                        'icon': '⚖️',
                        'points': 25
                    }
                elif weight_loss >= 0.5:  # Perdeu 0.5kg ou mais
                    points_to_award += 15
        
        # Atualizar pontos
        cursor.execute('''
            UPDATE patient_points 
            SET points = points + ?, total_points = total_points + ?,
                last_activity = DATE('now'), updated_at = CURRENT_TIMESTAMP
            WHERE patient_id = ?
        ''', (points_to_award, points_to_award, patient_id))
        
        # Verificar se deve subir de nível
        cursor.execute("SELECT points, level FROM patient_points WHERE patient_id = ?", (patient_id,))
        points_data = cursor.fetchone()
        
        if points_data:
            current_points, current_level = points_data
            points_needed = calculate_points_for_level(current_level + 1)
            
            if current_points >= points_needed:
                cursor.execute('''
                    UPDATE patient_points 
                    SET level = level + 1, points = points - ?
                    WHERE patient_id = ?
                ''', (points_needed, patient_id))
        
        # Criar badge se aplicável
        if badge_awarded:
            cursor.execute('''
                INSERT INTO patient_badges (
                    patient_id, badge_name, badge_description, badge_icon, points_awarded
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                patient_id, badge_awarded['name'], badge_awarded['description'],
                badge_awarded['icon'], badge_awarded['points']
            ))
        
        conn.commit()
        conn.close()
    
    except Exception as e:
        print(f"Erro ao premiar pontos: {e}")

def show_advanced_progress_analysis(nutritionist_id):
    """Análises avançadas de progresso"""
    st.subheader("📈 Análises Avançadas")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Seletor de período
    col_period1, col_period2 = st.columns(2)
    with col_period1:
        start_date = st.date_input("Período inicial", value=date.today() - timedelta(days=90))
    with col_period2:
        end_date = st.date_input("Período final", value=date.today())
    
    # Análise geral dos pacientes
    progress_summary = pd.read_sql_query("""
        SELECT 
            p.full_name,
            p.patient_id,
            COUNT(pp.id) as total_records,
            MIN(pp.weight) as min_weight,
            MAX(pp.weight) as max_weight,
            AVG(pp.weight) as avg_weight,
            FIRST_VALUE(pp.weight) OVER (PARTITION BY p.id ORDER BY pp.record_date ASC) as initial_weight,
            FIRST_VALUE(pp.weight) OVER (PARTITION BY p.id ORDER BY pp.record_date DESC) as current_weight
        FROM patients p
        LEFT JOIN patient_progress pp ON pp.patient_id = p.id
        WHERE p.nutritionist_id = ?
        AND pp.record_date BETWEEN ? AND ?
        GROUP BY p.id, p.full_name, p.patient_id
        HAVING COUNT(pp.id) > 0
        ORDER BY p.full_name
    """, conn, params=[nutritionist_id, start_date, end_date])
    
    if not progress_summary.empty:
        # Calcular mudanças de peso
        progress_summary['weight_change'] = progress_summary['current_weight'] - progress_summary['initial_weight']
        progress_summary['success_rate'] = progress_summary['weight_change'].apply(
            lambda x: "✅ Progresso" if x < -0.5 else "⚠️ Manutenção" if abs(x) <= 0.5 else "❌ Ganho"
        )
        
        # Métricas gerais
        col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
        
        total_patients = len(progress_summary)
        successful_patients = len(progress_summary[progress_summary['weight_change'] < -0.5])
        avg_weight_loss = progress_summary['weight_change'].mean()
        
        with col_metric1:
            st.metric("Pacientes Analisados", total_patients)
        with col_metric2:
            st.metric("Com Progresso", successful_patients)
        with col_metric3:
            success_rate = (successful_patients / total_patients * 100) if total_patients > 0 else 0
            st.metric("Taxa de Sucesso", f"{success_rate:.1f}%")
        with col_metric4:
            st.metric("Mudança Média", f"{avg_weight_loss:.1f}kg")
        
        # Tabela detalhada
        st.subheader("📊 Resumo por Paciente")
        
        display_summary = progress_summary[['full_name', 'patient_id', 'total_records', 
                                          'initial_weight', 'current_weight', 'weight_change', 'success_rate']].copy()
        display_summary.columns = ['Nome', 'ID', 'Registros', 'Peso Inicial', 'Peso Atual', 'Mudança', 'Status']
        display_summary['Peso Inicial'] = display_summary['Peso Inicial'].round(1)
        display_summary['Peso Atual'] = display_summary['Peso Atual'].round(1)
        display_summary['Mudança'] = display_summary['Mudança'].round(1)
        
        st.dataframe(display_summary, use_container_width=True)
        
        # Gráficos
        col_graph1, col_graph2 = st.columns(2)
        
        with col_graph1:
            # Distribuição de resultados
            status_counts = progress_summary['success_rate'].value_counts()
            fig_status = px.pie(values=status_counts.values, names=status_counts.index,
                              title="Distribuição de Resultados")
            st.plotly_chart(fig_status, use_container_width=True)
        
        with col_graph2:
            # Mudança de peso por paciente
            fig_change = px.bar(progress_summary, x='patient_id', y='weight_change',
                              title="Mudança de Peso por Paciente")
            fig_change.update_layout(xaxis_title="Paciente ID", yaxis_title="Mudança de Peso (kg)")
            st.plotly_chart(fig_change, use_container_width=True)
        
        # Evolução temporal
        st.subheader("📈 Evolução Temporal")
        
        temporal_data = pd.read_sql_query("""
            SELECT 
                pp.record_date,
                AVG(pp.weight) as avg_weight,
                COUNT(pp.id) as num_records
            FROM patient_progress pp
            JOIN patients p ON p.id = pp.patient_id
            WHERE p.nutritionist_id = ?
            AND pp.record_date BETWEEN ? AND ?
            GROUP BY pp.record_date
            ORDER BY pp.record_date
        """, conn, params=[nutritionist_id, start_date, end_date])
        
        if not temporal_data.empty:
            temporal_data['record_date'] = pd.to_datetime(temporal_data['record_date'])
            
            fig_temporal = px.line(temporal_data, x='record_date', y='avg_weight',
                                 title="Peso Médio dos Pacientes ao Longo do Tempo", markers=True)
            st.plotly_chart(fig_temporal, use_container_width=True)
    
    else:
        st.info("Nenhum dado de progresso encontrado no período selecionado.")
    
    conn.close()

def show_reports_nutritionist():
    """Relatórios para nutricionistas"""
    st.markdown('<h1 class="main-header">📊 Meus Relatórios</h1>', unsafe_allow_html=True)
    
    nutritionist_id = st.session_state.user['id']
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Performance", "👥 Pacientes", "💰 Financeiro", "🎯 Objetivos"])
    
    with tab1:
        show_performance_report(nutritionist_id)
    
    with tab2:
        show_patients_report(nutritionist_id)
    
    with tab3:
        show_nutritionist_financial_report(nutritionist_id)
    
    with tab4:
        show_goals_report(nutritionist_id)

def show_performance_report(nutritionist_id):
    """Relatório de performance do nutricionista"""
    st.subheader("📈 Relatório de Performance")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Período para análise
    col_perf1, col_perf2 = st.columns(2)
    with col_perf1:
        period_start = st.date_input("Período início", value=date.today().replace(day=1))
    with col_perf2:
        period_end = st.date_input("Período fim", value=date.today())
    
    # Métricas de consultas
    appointments_data = pd.read_sql_query("""
        SELECT 
            COUNT(*) as total_appointments,
            COUNT(CASE WHEN status = 'realizada' THEN 1 END) as completed,
            COUNT(CASE WHEN status = 'cancelado' THEN 1 END) as cancelled,
            AVG(duration) as avg_duration
        FROM appointments 
        WHERE nutritionist_id = ?
        AND DATE(appointment_date) BETWEEN ? AND ?
    """, conn, params=[nutritionist_id, period_start, period_end])
    
    if not appointments_data.empty:
        data = appointments_data.iloc[0]
        
        col_perf_metric1, col_perf_metric2, col_perf_metric3, col_perf_metric4 = st.columns(4)
        
        with col_perf_metric1:
            st.metric("Total Consultas", data['total_appointments'])
        
        with col_perf_metric2:
            st.metric("Realizadas", data['completed'])
        
        with col_perf_metric3:
            completion_rate = (data['completed'] / data['total_appointments'] * 100) if data['total_appointments'] > 0 else 0
            st.metric("Taxa Realização", f"{completion_rate:.1f}%")
        
        with col_perf_metric4:
            st.metric("Duração Média", f"{data['avg_duration']:.0f} min")
        
        # Evolução diária
        daily_appointments = pd.read_sql_query("""
            SELECT 
                DATE(appointment_date) as date,
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'realizada' THEN 1 END) as completed
            FROM appointments 
            WHERE nutritionist_id = ?
            AND DATE(appointment_date) BETWEEN ? AND ?
            GROUP BY DATE(appointment_date)
            ORDER BY date
        """, conn, params=[nutritionist_id, period_start, period_end])
        
        if not daily_appointments.empty:
            fig_daily = px.line(daily_appointments, x='date', y=['total', 'completed'],
                              title="Consultas por Dia", markers=True)
            st.plotly_chart(fig_daily, use_container_width=True)
    
    # Análise de pacientes
    patients_analysis = pd.read_sql_query("""
        SELECT 
            COUNT(DISTINCT p.id) as total_patients,
            COUNT(DISTINCT CASE WHEN pp.patient_id IS NOT NULL THEN p.id END) as patients_with_progress,
            AVG(CASE WHEN pp.weight IS NOT NULL THEN 
                (SELECT weight FROM patient_progress WHERE patient_id = p.id ORDER BY record_date DESC LIMIT 1) -
                (SELECT weight FROM patient_progress WHERE patient_id = p.id ORDER BY record_date ASC LIMIT 1)
            END) as avg_weight_change
        FROM patients p
        LEFT JOIN patient_progress pp ON pp.patient_id = p.id
        WHERE p.nutritionist_id = ?
        AND p.active = 1
    """, conn, params=[nutritionist_id])
    
    if not patients_analysis.empty:
        analysis = patients_analysis.iloc[0]
        
        st.subheader("👥 Análise de Pacientes")
        
        col_pat1, col_pat2, col_pat3 = st.columns(3)
        
        with col_pat1:
            st.metric("Total Pacientes Ativos", analysis['total_patients'])
        
        with col_pat2:
            st.metric("Com Progresso Registrado", analysis['patients_with_progress'])
        
        with col_pat3:
            avg_change = analysis['avg_weight_change'] or 0
            st.metric("Mudança Média de Peso", f"{avg_change:.1f}kg")
    
    conn.close()

def show_patients_report(nutritionist_id):
    """Relatório detalhado de pacientes"""
    st.subheader("👥 Relatório de Pacientes")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Pacientes por status
    patients_status = pd.read_sql_query("""
        SELECT 
            p.*,
            COUNT(a.id) as total_appointments,
            COUNT(CASE WHEN a.status = 'realizada' THEN 1 END) as completed_appointments,
            MAX(a.appointment_date) as last_appointment,
            COUNT(pp.id) as progress_records,
            (
                SELECT weight FROM patient_progress 
                WHERE patient_id = p.id 
                ORDER BY record_date DESC LIMIT 1
            ) as current_weight,
            (
                SELECT weight FROM patient_progress 
                WHERE patient_id = p.id 
                ORDER BY record_date ASC LIMIT 1
            ) as initial_weight
        FROM patients p
        LEFT JOIN appointments a ON a.patient_id = p.id
        LEFT JOIN patient_progress pp ON pp.patient_id = p.id
        WHERE p.nutritionist_id = ? AND p.active = 1
        GROUP BY p.id
        ORDER BY p.full_name
    """, conn, params=[nutritionist_id])
    
    if not patients_status.empty:
        # Calcular categorias
        today = date.today()
        
        def categorize_patient(row):
            last_apt = pd.to_datetime(row['last_appointment']).date() if row['last_appointment'] else None
            
            if not last_apt:
                return "🆕 Novo"
            elif (today - last_apt).days <= 7:
                return "🟢 Ativo"
            elif (today - last_apt).days <= 30:
                return "🟡 Regular"
            else:
                return "🔴 Inativo"
        
        patients_status['category'] = patients_status.apply(categorize_patient, axis=1)
        patients_status['weight_change'] = patients_status['current_weight'] - patients_status['initial_weight']
        
        # Resumo por categoria
        category_summary = patients_status['category'].value_counts()
        
        st.write("**📊 Distribuição por Status:**")
        
        col_cat1, col_cat2, col_cat3, col_cat4 = st.columns(4)
        
        categories = ["🆕 Novo", "🟢 Ativo", "🟡 Regular", "🔴 Inativo"]
        cols = [col_cat1, col_cat2, col_cat3, col_cat4]
        
        for cat, col in zip(categories, cols):
            count = category_summary.get(cat, 0)
            with col:
                st.metric(cat, count)
        
        # Tabela detalhada
        display_patients = patients_status[[
            'full_name', 'patient_id', 'category', 'total_appointments', 
            'completed_appointments', 'progress_records', 'weight_change'
        ]].copy()
        
        display_patients.columns = [
            'Nome', 'ID', 'Status', 'Total Consultas', 
            'Realizadas', 'Registros Progresso', 'Mudança Peso'
        ]
        
        # Formatar mudança de peso
        display_patients['Mudança Peso'] = display_patients['Mudança Peso'].apply(
            lambda x: f"{x:.1f}kg" if pd.notna(x) else "N/A"
        )
        
        st.dataframe(display_patients, use_container_width=True)
        
        # Gráfico de distribuição
        fig_dist = px.pie(values=category_summary.values, names=category_summary.index,
                         title="Distribuição de Pacientes por Status")
        st.plotly_chart(fig_dist, use_container_width=True)
    
    conn.close()

def show_nutritionist_financial_report(nutritionist_id):
    """Relatório financeiro do nutricionista"""
    st.subheader("💰 Relatório Financeiro")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Período para análise
    col_fin1, col_fin2 = st.columns(2)
    with col_fin1:
        fin_start = st.date_input("Período início", value=date.today().replace(day=1), key="fin_start")
    with col_fin2:
        fin_end = st.date_input("Período fim", value=date.today(), key="fin_end")
    
    # Receitas do nutricionista
    financial_data = pd.read_sql_query("""
        SELECT 
            pf.*,
            p.full_name as patient_name,
            p.patient_id
        FROM patient_financial pf
        JOIN patients p ON p.id = pf.patient_id
        WHERE p.nutritionist_id = ?
        AND DATE(pf.created_at) BETWEEN ? AND ?
    """, conn, params=[nutritionist_id, fin_start, fin_end])
    
    if not financial_data.empty:
        # Métricas financeiras
        total_revenue = financial_data['amount'].sum()
        paid_revenue = financial_data[financial_data['payment_status'] == 'pago']['amount'].sum()
        pending_revenue = financial_data[financial_data['payment_status'] == 'pendente']['amount'].sum()
        
        col_fin_metric1, col_fin_metric2, col_fin_metric3, col_fin_metric4 = st.columns(4)
        
        with col_fin_metric1:
            st.metric("Receita Total", f"R$ {total_revenue:.2f}")
        
        with col_fin_metric2:
            st.metric("Recebido", f"R$ {paid_revenue:.2f}")
        
        with col_fin_metric3:
            st.metric("Pendente", f"R$ {pending_revenue:.2f}")
        
        with col_fin_metric4:
            payment_rate = (paid_revenue / total_revenue * 100) if total_revenue > 0 else 0
            st.metric("Taxa Recebimento", f"{payment_rate:.1f}%")
        
        # Receita por tipo de serviço
        service_revenue = financial_data.groupby('service_type')['amount'].sum().reset_index()
        service_revenue = service_revenue.sort_values('amount', ascending=False)
        
        fig_service = px.bar(service_revenue, x='service_type', y='amount',
                           title="Receita por Tipo de Serviço")
        fig_service.update_layout(xaxis_title="Tipo de Serviço", yaxis_title="Receita (R$)")
        st.plotly_chart(fig_service, use_container_width=True)
        
        # Evolução mensal
        financial_data['month'] = pd.to_datetime(financial_data['created_at']).dt.to_period('M')
        monthly_revenue = financial_data.groupby('month')['amount'].sum().reset_index()
        monthly_revenue['month'] = monthly_revenue['month'].astype(str)
        
        if len(monthly_revenue) > 1:
            fig_monthly = px.line(monthly_revenue, x='month', y='amount',
                                title="Evolução Mensal da Receita", markers=True)
            st.plotly_chart(fig_monthly, use_container_width=True)
    
    else:
        st.info("Nenhum dado financeiro encontrado no período selecionado.")
    
    conn.close()

def show_goals_report(nutritionist_id):
    """Relatório de objetivos e metas"""
    st.subheader("🎯 Relatório de Objetivos")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Definir ou visualizar metas
    col_goals1, col_goals2 = st.columns(2)
    
    with col_goals1:
        st.write("**📋 Definir Metas Mensais**")
        
        if 'monthly_goals' not in st.session_state:
            st.session_state.monthly_goals = {
                'new_patients': 5,
                'appointments': 60,
                'revenue': 5000.00
            }
        
        new_patients_goal = st.number_input("Novos pacientes/mês", value=st.session_state.monthly_goals['new_patients'])
        appointments_goal = st.number_input("Consultas/mês", value=st.session_state.monthly_goals['appointments'])
        revenue_goal = st.number_input("Receita/mês (R$)", value=st.session_state.monthly_goals['revenue'])
        
        if st.button("💾 Salvar Metas"):
            st.session_state.monthly_goals = {
                'new_patients': new_patients_goal,
                'appointments': appointments_goal,
                'revenue': revenue_goal
            }
            st.success("Metas atualizadas!")
    
    with col_goals2:
        st.write("**📊 Performance Atual vs Metas**")
        
        # Performance do mês atual
        current_month_start = date.today().replace(day=1)
        
        # Novos pacientes este mês
        new_patients_current = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM patients 
            WHERE nutritionist_id = ? AND DATE(created_at) >= ?
        """, conn, params=[nutritionist_id, current_month_start]).iloc[0]['count']
        
        # Consultas este mês
        appointments_current = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM appointments 
            WHERE nutritionist_id = ? AND DATE(appointment_date) >= ? AND status = 'realizada'
        """, conn, params=[nutritionist_id, current_month_start]).iloc[0]['count']
        
        # Receita este mês
        revenue_current = pd.read_sql_query("""
            SELECT COALESCE(SUM(pf.amount), 0) as total
            FROM patient_financial pf
            JOIN patients p ON p.id = pf.patient_id
            WHERE p.nutritionist_id = ? AND pf.payment_status = 'pago' 
            AND DATE(pf.paid_date) >= ?
        """, conn, params=[nutritionist_id, current_month_start]).iloc[0]['total']
        
        # Calcular progresso
        goals = st.session_state.monthly_goals
        
        new_patients_progress = (new_patients_current / goals['new_patients']) * 100 if goals['new_patients'] > 0 else 0
        appointments_progress = (appointments_current / goals['appointments']) * 100 if goals['appointments'] > 0 else 0
        revenue_progress = (revenue_current / goals['revenue']) * 100 if goals['revenue'] > 0 else 0
        
        # Exibir progresso
        st.metric("Novos Pacientes", f"{new_patients_current}/{goals['new_patients']}", 
                 delta=f"{new_patients_progress:.1f}%")
        
        st.metric("Consultas Realizadas", f"{appointments_current}/{goals['appointments']}", 
                 delta=f"{appointments_progress:.1f}%")
        
        st.metric("Receita", f"R$ {revenue_current:.2f}/R$ {goals['revenue']:.2f}", 
                 delta=f"{revenue_progress:.1f}%")
        
        # Gráfico de progresso
        progress_data = pd.DataFrame({
            'Meta': ['Novos Pacientes', 'Consultas', 'Receita'],
            'Progresso': [new_patients_progress, appointments_progress, revenue_progress]
        })
        
        fig_progress = px.bar(progress_data, x='Meta', y='Progresso',
                            title="Progresso das Metas (%)", 
                            color='Progresso',
                            color_continuous_scale=['red', 'yellow', 'green'])
        fig_progress.update_layout(yaxis_title="Progresso (%)")
        st.plotly_chart(fig_progress, use_container_width=True)
    
    conn.close()

def show_gamification_nutritionist():
    """Sistema de gamificação para nutricionistas"""
    st.markdown('<h1 class="main-header">🎮 Sistema de Gamificação</h1>', unsafe_allow_html=True)
    
    nutritionist_id = st.session_state.user['id']
    
    tab1, tab2, tab3 = st.tabs(["🏆 Ranking Pacientes", "🎯 Gerenciar Pontos", "📊 Estatísticas"])
    
    with tab1:
        show_patients_ranking(nutritionist_id)
    
    with tab2:
        manage_patient_points(nutritionist_id)
    
    with tab3:
        show_gamification_stats(nutritionist_id)

def show_patients_ranking(nutritionist_id):
    """Ranking de pacientes por pontos"""
    st.subheader("🏆 Ranking dos Pacientes")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Ranking de pacientes
    ranking_data = pd.read_sql_query("""
        SELECT 
            p.full_name,
            p.patient_id,
            COALESCE(pp.points, 0) as points,
            COALESCE(pp.level, 1) as level,
            COALESCE(pp.total_points, 0) as total_points,
            COALESCE(pp.streak_days, 0) as streak_days,
            COUNT(pb.id) as total_badges
        FROM patients p
        LEFT JOIN patient_points pp ON pp.patient_id = p.id
        LEFT JOIN patient_badges pb ON pb.patient_id = p.id
        WHERE p.nutritionist_id = ? AND p.active = 1
        GROUP BY p.id, p.full_name, p.patient_id, pp.points, pp.level, pp.total_points, pp.streak_days
        ORDER BY COALESCE(pp.total_points, 0) DESC
    """, conn, params=[nutritionist_id])
    
    if not ranking_data.empty:
        st.write("**🏅 Top Pacientes por Pontuação Total:**")
        
        # Top 3 com destaque
        for i, (idx, patient) in enumerate(ranking_data.head(3).iterrows()):
            medals = ["🥇", "🥈", "🥉"]
            colors = ["#FFD700", "#C0C0C0", "#CD7F32"]
            
            st.markdown(f"""
            <div class="gamification-card" style="border: 3px solid {colors[i]};">
                <h3>{medals[i]} {patient['full_name']} ({patient['patient_id']})</h3>
                <p><strong>Nível:</strong> {patient['level']} | 
                   <strong>Total Pontos:</strong> {patient['total_points']} | 
                   <strong>Badges:</strong> {patient['total_badges']}</p>
                <p><strong>Sequência:</strong> {patient['streak_days']} dias</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Tabela completa do ranking
        if len(ranking_data) > 3:
            st.write("**📊 Ranking Completo:**")
            
            display_ranking = ranking_data.copy()
            display_ranking.index = range(1, len(display_ranking) + 1)
            display_ranking_show = display_ranking[['full_name', 'patient_id', 'level', 'total_points', 'total_badges', 'streak_days']].copy()
            display_ranking_show.columns = ['Nome', 'ID', 'Nível', 'Total Pontos', 'Badges', 'Sequência (dias)']
            
            st.dataframe(display_ranking_show, use_container_width=True)
        
        # Gráfico de distribuição de níveis
        level_distribution = ranking_data['level'].value_counts().sort_index()
        
        fig_levels = px.bar(x=level_distribution.index, y=level_distribution.values,
                           title="Distribuição de Pacientes por Nível")
        fig_levels.update_layout(xaxis_title="Nível", yaxis_title="Número de Pacientes")
        st.plotly_chart(fig_levels, use_container_width=True)
    
    else:
        st.info("Nenhum paciente encontrado.")
    
    conn.close()

def manage_patient_points(nutritionist_id):
    """Gerenciar pontos dos pacientes"""
    st.subheader("🎯 Gerenciar Pontos e Badges")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Selecionar paciente
    patients_df = pd.read_sql_query("""
        SELECT p.id, p.full_name, p.patient_id,
               COALESCE(pp.points, 0) as current_points,
               COALESCE(pp.level, 1) as current_level
        FROM patients p
        LEFT JOIN patient_points pp ON pp.patient_id = p.id
        WHERE p.nutritionist_id = ? AND p.active = 1
        ORDER BY p.full_name
    """, conn, params=[nutritionist_id])
    
    if patients_df.empty:
        st.warning("Nenhum paciente encontrado.")
        conn.close()
        return
    
    selected_patient = st.selectbox(
        "Selecione o paciente:",
        options=patients_df['id'].tolist(),
        format_func=lambda x: f"{patients_df[patients_df['id'] == x]['full_name'].iloc[0]} ({patients_df[patients_df['id'] == x]['patient_id'].iloc[0]})"
    )
    
    if selected_patient:
        patient_info = patients_df[patients_df['id'] == selected_patient].iloc[0]
        
        # Exibir status atual
        col_status1, col_status2 = st.columns(2)
        
        with col_status1:
            st.info(f"""
            **Status Atual de {patient_info['full_name']}:**
            • Pontos atuais: {patient_info['current_points']}
            • Nível atual: {patient_info['current_level']}
            """)
        
        with col_status2:
            # Badges do paciente
            patient_badges = pd.read_sql_query("""
                SELECT badge_name, badge_icon FROM patient_badges 
                WHERE patient_id = ? ORDER BY earned_date DESC LIMIT 3
            """, conn, params=[selected_patient])
            
            if not patient_badges.empty:
                st.write("**🏆 Badges Recentes:**")
                for _, badge in patient_badges.iterrows():
                    st.write(f"{badge['badge_icon']} {badge['badge_name']}")
            else:
                st.write("**🏆 Badges:** Nenhuma ainda")
        
        # Ações de pontuação
        col_action1, col_action2 = st.columns(2)
        
        with col_action1:
            st.write("**➕ Adicionar Pontos**")
            
            reason_options = {
                "Consulta realizada": 20,
                "Meta semanal atingida": 25,
                "Progresso excepcional": 50,
                "Adesão ao plano": 15,
                "Participação ativa": 10,
                "Outro motivo": 0
            }
            
            selected_reason = st.selectbox("Motivo:", list(reason_options.keys()))
            suggested_points = reason_options[selected_reason]
            
            points_to_add = st.number_input("Pontos a adicionar:", 
                                          min_value=1, max_value=100, 
                                          value=suggested_points if suggested_points > 0 else 10)
            
            custom_reason = ""
            if selected_reason == "Outro motivo":
                custom_reason = st.text_input("Especifique o motivo:")
            
            if st.button("➕ Adicionar Pontos"):
                final_reason = custom_reason if custom_reason else selected_reason
                add_points_to_patient(selected_patient, points_to_add, final_reason, nutritionist_id)
                st.success(f"✅ {points_to_add} pontos adicionados!")
                st.rerun()
        
        with col_action2:
            st.write("**🏆 Conceder Badge**")
            
            available_badges = [
                {"name": "Progresso Consistente", "icon": "📈", "points": 30},
                {"name": "Meta Mensal", "icon": "🎯", "points": 50},
                {"name": "Dedicação Exemplar", "icon": "⭐", "points": 40},
                {"name": "Transformação", "icon": "🦋", "points": 75},
                {"name": "Inspiração", "icon": "💫", "points": 35}
            ]
            
            selected_badge = st.selectbox("Badge a conceder:", 
                                        range(len(available_badges)),
                                        format_func=lambda x: f"{available_badges[x]['icon']} {available_badges[x]['name']} (+{available_badges[x]['points']} pts)")
            
            badge_description = st.text_input("Descrição da conquista:", 
                                            placeholder="Ex: Perdeu 5kg em 2 meses")
            
            if st.button("🏆 Conceder Badge"):
                badge_info = available_badges[selected_badge]
                create_patient_badge(selected_patient, badge_info, badge_description)
                st.success(f"✅ Badge '{badge_info['name']}' concedida!")
                st.rerun()
    
    conn.close()

def add_points_to_patient(patient_id, points, reason, nutritionist_id):
    """Adiciona pontos ao paciente"""
    try:
        conn = sqlite3.connect('nutriapp360.db')
        cursor = conn.cursor()
        
        # Atualizar ou criar registro de pontos
        cursor.execute("""
            INSERT OR REPLACE INTO patient_points 
            (patient_id, points, level, total_points, last_activity, updated_at)
            VALUES (
                ?, 
                COALESCE((SELECT points FROM patient_points WHERE patient_id = ?), 0) + ?,
                COALESCE((SELECT level FROM patient_points WHERE patient_id = ?), 1),
                COALESCE((SELECT total_points FROM patient_points WHERE patient_id = ?), 0) + ?,
                DATE('now'),
                CURRENT_TIMESTAMP
            )
        """, (patient_id, patient_id, points, patient_id, patient_id, points))
        
        # Log da ação
        log_audit_action(nutritionist_id, f'add_points: {reason}', 'patient_points', patient_id)
        
        conn.commit()
        conn.close()
    
    except Exception as e:
        st.error(f"Erro ao adicionar pontos: {e}")

def create_patient_badge(patient_id, badge_info, description):
    """Cria badge para paciente"""
    try:
        conn = sqlite3.connect('nutriapp360.db')
        cursor = conn.cursor()
        
        # Criar badge
        cursor.execute("""
            INSERT INTO patient_badges 
            (patient_id, badge_name, badge_description, badge_icon, points_awarded, earned_date)
            VALUES (?, ?, ?, ?, ?, DATE('now'))
        """, (patient_id, badge_info['name'], description, badge_info['icon'], badge_info['points']))
        
        # Adicionar pontos da badge
        cursor.execute("""
            UPDATE patient_points 
            SET points = points + ?, total_points = total_points + ?, updated_at = CURRENT_TIMESTAMP
            WHERE patient_id = ?
        """, (badge_info['points'], badge_info['points'], patient_id))
        
        conn.commit()
        conn.close()
    
    except Exception as e:
        st.error(f"Erro ao criar badge: {e}")

def show_gamification_stats(nutritionist_id):
    """Estatísticas do sistema de gamificação"""
    st.subheader("📊 Estatísticas de Gamificação")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Estatísticas gerais
    stats_data = pd.read_sql_query("""
        SELECT 
            COUNT(DISTINCT p.id) as total_patients,
            AVG(COALESCE(pp.points, 0)) as avg_points,
            AVG(COALESCE(pp.level, 1)) as avg_level,
            SUM(COALESCE(pp.total_points, 0)) as total_points_awarded,
            COUNT(pb.id) as total_badges_awarded
        FROM patients p
        LEFT JOIN patient_points pp ON pp.patient_id = p.id
        LEFT JOIN patient_badges pb ON pb.patient_id = p.id
        WHERE p.nutritionist_id = ?
    """, conn, params=[nutritionist_id])
    
    if not stats_data.empty:
        stats = stats_data.iloc[0]
        
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            st.metric("Total Pacientes", stats['total_patients'])
        
        with col_stat2:
            st.metric("Pontos Médios", f"{stats['avg_points']:.1f}")
        
        with col_stat3:
            st.metric("Nível Médio", f"{stats['avg_level']:.1f}")
        
        with col_stat4:
            st.metric("Total Badges", stats['total_badges_awarded'])
    
    # Engajamento por período
    engagement_data = pd.read_sql_query("""
        SELECT 
            DATE(pb.earned_date) as date,
            COUNT(*) as badges_earned
        FROM patient_badges pb
        JOIN patients p ON p.id = pb.patient_id
        WHERE p.nutritionist_id = ?
        AND pb.earned_date >= DATE('now', '-30 days')
        GROUP BY DATE(pb.earned_date)
        ORDER BY date
    """, conn, params=[nutritionist_id])
    
    if not engagement_data.empty:
        fig_engagement = px.line(engagement_data, x='date', y='badges_earned',
                               title="Badges Conquistadas nos Últimos 30 Dias", markers=True)
        st.plotly_chart(fig_engagement, use_container_width=True)
    
    # Badges mais populares
    popular_badges = pd.read_sql_query("""
        SELECT 
            pb.badge_name,
            pb.badge_icon,
            COUNT(*) as times_earned
        FROM patient_badges pb
        JOIN patients p ON p.id = pb.patient_id
        WHERE p.nutritionist_id = ?
        GROUP BY pb.badge_name, pb.badge_icon
        ORDER BY times_earned DESC
        LIMIT 5
    """, conn, params=[nutritionist_id])
    
    if not popular_badges.empty:
        st.subheader("🏆 Badges Mais Conquistadas")
        
        for _, badge in popular_badges.iterrows():
            col_badge1, col_badge2 = st.columns([3, 1])
            
            with col_badge1:
                st.write(f"{badge['badge_icon']} **{badge['badge_name']}**")
            
            with col_badge2:
                st.write(f"**{badge['times_earned']}x**")
    
    conn.close(), conn).iloc[0]['count']
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #4CAF50;">👥 {total_users}</h3>
                <p style="margin: 0;">Usuários Ativos</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #2196F3;">🏥 {total_patients}</h3>
                <p style="margin: 0;">Pacientes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #9C27B0;">👨‍⚕️ {total_nutritionists}</h3>
                <p style="margin: 0;">Nutricionistas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #FF9800;">📅 {total_appointments_month}</h3>
                <p style="margin: 0;">Consultas/Mês</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráficos e análises
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.subheader("📈 Crescimento de Usuários")
            
            # Dados de crescimento simulados
            growth_data = pd.DataFrame({
                'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
                'Usuários': [10, 15, 22, 28, 35, total_users],
                'Pacientes': [5, 8, 12, 18, 25, total_patients]
            })
            
            fig = px.line(growth_data, x='Mês', y=['Usuários', 'Pacientes'], 
                         title="Crescimento Mensal", markers=True)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.subheader("💰 Receita Mensal")
            
            revenue_data = pd.read_sql_query("""
                SELECT 
                    strftime('%m', created_at) as mes,
                    SUM(amount) as total
                FROM patient_financial 
                WHERE payment_status = 'pago'
                GROUP BY strftime('%m', created_at)
                ORDER BY mes
            """, conn)
            
            if not revenue_data.empty:
                fig = px.bar(revenue_data, x='mes', y='total', 
                            title="Receita por Mês")
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Dados de receita serão exibidos conforme pagamentos forem processados")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Tabelas de resumo
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("📊 Resumo por Nutricionista")
        
        nutritionist_stats = pd.read_sql_query("""
            SELECT 
                u.full_name as nutricionista,
                COUNT(DISTINCT p.id) as total_pacientes,
                COUNT(DISTINCT a.id) as total_consultas,
                COUNT(DISTINCT CASE WHEN a.status = 'realizada' THEN a.id END) as consultas_realizadas,
                COALESCE(SUM(pf.amount), 0) as receita_total
            FROM users u
            LEFT JOIN patients p ON p.nutritionist_id = u.id
            LEFT JOIN appointments a ON a.nutritionist_id = u.id
            LEFT JOIN patient_financial pf ON pf.processed_by = u.id AND pf.payment_status = 'pago'
            WHERE u.role = 'nutritionist' AND u.active = 1
            GROUP BY u.id, u.full_name
            ORDER BY total_pacientes DESC
        """, conn)
        
        if not nutritionist_stats.empty:
            st.dataframe(nutritionist_stats, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sistema de alertas
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("🔔 Alertas do Sistema")
        
        # Verificar alertas
        pending_payments = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM patient_financial 
            WHERE payment_status = 'pendente' AND due_date < date('now')
        """, conn).iloc[0]['count']
        
        inactive_patients = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM patients p
            WHERE NOT EXISTS (
                SELECT 1 FROM appointments a 
                WHERE a.patient_id = p.id AND a.appointment_date > date('now', '-30 days')
            )
        """, conn).iloc[0]['count']
        
        if pending_payments > 0:
            st.warning(f"⚠️ {pending_payments} pagamentos em atraso")
        
        if inactive_patients > 5:
            st.warning(f"📉 {inactive_patients} pacientes sem consulta há mais de 30 dias")
        
        if pending_payments == 0 and inactive_patients <= 5:
            st.success("✅ Sistema funcionando normalmente")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erro ao carregar dashboard: {e}")
    finally:
    def show_my_progress():
    """Progresso pessoal do paciente"""
    st.markdown('<h1 class="main-header">📈 Meu Progresso</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar ID do paciente
    patient_data = pd.read_sql_query("""
        SELECT id FROM patients WHERE user_id = ?
    """, conn, params=[user_id])
    
    if patient_data.empty:
        st.error("Dados do paciente não encontrados.")
        conn.close()
        return
    
    patient_id = patient_data.iloc[0]['id']
    
    # Dados de progresso
    progress_data = pd.read_sql_query("""
        SELECT * FROM patient_progress 
        WHERE patient_id = ?
        ORDER BY record_date DESC
    """, conn, params=[patient_id])
    
    conn.close()
    
    if not progress_data.empty:
        progress_data['record_date'] = pd.to_datetime(progress_data['record_date'])
        
        # Métricas atuais vs iniciais
        current = progress_data.iloc[0]
        initial = progress_data.iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        
        weight_change = current['weight'] - initial['weight'] if current['weight'] and initial['weight'] else 0
        fat_change = current['body_fat'] - initial['body_fat'] if current['body_fat'] and initial['body_fat'] else 0
        muscle_change = current['muscle_mass'] - initial['muscle_mass'] if current['muscle_mass'] and initial['muscle_mass'] else 0
        
        with col1:
            st.metric("Peso Atual", f"{current['weight']:.1f} kg" if current['weight'] else "N/A", 
                     f"{weight_change:+.1f} kg" if weight_change != 0 else None)
        
        with col2:
            st.metric("% Gordura", f"{current['body_fat']:.1f}%" if current['body_fat'] else "N/A",
                     f"{fat_change:+.1f}%" if fat_change != 0 else None)
        
        with col3:
            st.metric("% Músculo", f"{current['muscle_mass']:.1f}%" if current['muscle_mass'] else "N/A",
                     f"{muscle_change:+.1f}%" if muscle_change != 0 else None)
        
        with col4:
            weeks = len(progress_data) - 1 if len(progress_data) > 1 else 1
            avg_weekly = weight_change / weeks if weeks > 0 else 0
            st.metric("Mudança/Semana", f"{avg_weekly:.2f} kg")
        
        # Gráficos de evolução
        col_graph1, col_graph2 = st.columns(2)
        
        with col_graph1:
            if progress_data['weight'].notna().any():
                fig_weight = px.line(progress_data, x='record_date', y='weight',
                                   title='Evolução do Peso (kg)', markers=True)
                fig_weight.update_layout(height=400)
                st.plotly_chart(fig_weight, use_container_width=True)
        
        with col_graph2:
            # Composição corporal
            body_comp_data = progress_data[['record_date', 'body_fat', 'muscle_mass']].dropna()
            if not body_comp_data.empty:
                fig_comp = px.line(body_comp_data, x='record_date', 
                                 y=['body_fat', 'muscle_mass'],
                                 title='Composição Corporal (%)', markers=True)
                fig_comp.update_layout(height=400)
                st.plotly_chart(fig_comp, use_container_width=True)
        
        # Medidas corporais
        if any(progress_data[col].notna().any() for col in ['waist_circumference', 'hip_circumference']):
            st.subheader("📏 Medidas Corporais")
            
            measurements_data = progress_data[['record_date', 'waist_circumference', 'hip_circumference']].dropna()
            if not measurements_data.empty:
                fig_measurements = px.line(measurements_data, x='record_date',
                                         y=['waist_circumference', 'hip_circumference'],
                                         title='Evolução das Medidas (cm)', markers=True)
                st.plotly_chart(fig_measurements, use_container_width=True)
        
        # Histórico detalhado
        st.subheader("📋 Histórico de Medições")
        
        display_progress = progress_data[['record_date', 'weight', 'body_fat', 'muscle_mass', 
                                        'waist_circumference', 'hip_circumference', 'notes']].copy()
        display_progress['record_date'] = display_progress['record_date'].dt.strftime('%d/%m/%Y')
        display_progress.columns = ['Data', 'Peso (kg)', '% Gordura', '% Músculo', 
                                   'Cintura (cm)', 'Quadril (cm)', 'Observações']
        
        st.dataframe(display_progress, use_container_width=True)
        
        # Análise de tendências
        if len(progress_data) >= 3:
            st.subheader("📊 Análise de Tendências")
            
            col_trend1, col_trend2, col_trend3 = st.columns(3)
            
            # Calcular tendência (últimas 3 medições)
            recent_data = progress_data.head(3)
            if len(recent_data) >= 2:
                recent_weight_change = recent_data.iloc[0]['weight'] - recent_data.iloc[-1]['weight']
                trend = "⬇️ Perdendo peso" if recent_weight_change < -0.3 else "⬆️ Ganhando peso" if recent_weight_change > 0.3 else "➡️ Peso estável"
                
                with col_trend1:
                    st.info(f"**Tendência Atual:**\n{trend}")
                
                with col_trend2:
                    consistency = "Alta" if progress_data['weight'].std() < 2 else "Moderada" if progress_data['weight'].std() < 5 else "Baixa"
                    st.info(f"**Consistência:**\n{consistency}")
                
                with col_trend3:
                    total_change = progress_data.iloc[0]['weight'] - progress_data.iloc[-1]['weight']
                    direction = "positiva" if abs(total_change) > 1 else "estável"
                    st.info(f"**Evolução Geral:**\nMudança {direction}")
    
    else:
        st.info("Seu nutricionista ainda não registrou dados de progresso. Aguarde a primeira consulta!")
        
        # Dicas para pacientes sem dados
        st.subheader("💡 Dicas Enquanto Aguarda")
        
        tips = [
            "🔍 **Automonitoramento:** Anote seus hábitos alimentares em um diário",
            "💧 **Hidratação:** Beba pelo menos 2L de água por dia",
            "🚶‍♀️ **Atividade:** Faça caminhadas regulares de 30 minutos",
            "😴 **Sono:** Durma de 7-8 horas por noite para regular hormônios",
            "📱 **Preparação:** Liste suas dúvidas para a próxima consulta"
        ]
        
        for tip in tips:
            st.write(tip)

def show_my_appointments():
    """Consultas do paciente"""
    st.markdown('<h1 class="main-header">📅 Minhas Consultas</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar ID do paciente
    patient_data = pd.read_sql_query("SELECT id FROM patients WHERE user_id = ?", conn, params=[user_id])
    
    if patient_data.empty:
        st.error("Dados do paciente não encontrados.")
        conn.close()
        return
    
    patient_id = patient_data.iloc[0]['id']
    
    tab1, tab2 = st.tabs(["📋 Próximas Consultas", "📚 Histórico"])
    
    with tab1:
        # Próximas consultas
        upcoming_appointments = pd.read_sql_query("""
            SELECT 
                a.*,
                n.full_name as nutritionist_name,
                n.phone as nutritionist_phone
            FROM appointments a
            JOIN users n ON n.id = a.nutritionist_id
            WHERE a.patient_id = ? 
            AND a.appointment_date > datetime('now')
            AND a.status = 'agendado'
            ORDER BY a.appointment_date
        """, conn, params=[patient_id])
        
        if not upcoming_appointments.empty:
            st.subheader("🔜 Próximas Consultas")
            
            for idx, apt in upcoming_appointments.iterrows():
                apt_datetime = pd.to_datetime(apt['appointment_date'])
                days_until = (apt_datetime.date() - date.today()).days
                
                status_color = "#2196F3"
                if days_until <= 1:
                    status_color = "#FF9800"  # Consulta próxima
                
                st.markdown(f"""
                <div class="appointment-card" style="border-left-color: {status_color};">
                    <h4>📅 {apt_datetime.strftime('%d/%m/%Y às %H:%M')}</h4>
                    <p><strong>Nutricionista:</strong> {apt['nutritionist_name']}</p>
                    <p><strong>Tipo:</strong> {apt['appointment_type']} | <strong>Duração:</strong> {apt['duration']} min</p>
                    <p><strong>Em {days_until} dia(s)</strong></p>
                    {f"<p><strong>Observações:</strong> {apt['notes']}</p>" if apt['notes'] else ""}
                </div>
                """, unsafe_allow_html=True)
                
                # Ações rápidas
                col_apt1, col_apt2, col_apt3 = st.columns(3)
                
                with col_apt1:
                    if st.button(f"📞 Contato", key=f"contact_{apt['id']}"):
                        st.info(f"Telefone: {apt['nutritionist_phone'] or 'Não disponível'}")
                
                with col_apt2:
                    if st.button(f"📝 Preparar", key=f"prepare_{apt['id']}"):
                        show_appointment_preparation()
                
                with col_apt3:
                    if days_until > 1:
                        if st.button(f"⏰ Lembrete", key=f"reminder_{apt['id']}"):
                            st.success("Lembrete configurado! Você será notificado.")
        
        else:
            st.info("Você não possui consultas agendadas.")
            st.write("Entre em contato com sua clínica para agendar sua próxima consulta.")
    
    with tab2:
        # Histórico de consultas
        past_appointments = pd.read_sql_query("""
            SELECT 
                a.*,
                n.full_name as nutritionist_name
            FROM appointments a
            JOIN users n ON n.id = a.nutritionist_id
            WHERE a.patient_id = ?
            ORDER BY a.appointment_date DESC
        """, conn, params=[patient_id])
        
        if not past_appointments.empty:
            st.subheader("📚 Histórico de Consultas")
            
            # Estatísticas
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            total_appointments = len(past_appointments)
            completed_appointments = len(past_appointments[past_appointments['status'] == 'realizada'])
            cancelled_appointments = len(past_appointments[past_appointments['status'] == 'cancelado'])
            
            with col_stat1:
                st.metric("Total de Consultas", total_appointments)
            with col_stat2:
                st.metric("Realizadas", completed_appointments)
            with col_stat3:
                st.metric("Canceladas", cancelled_appointments)
            
            # Lista de consultas passadas
            for idx, apt in past_appointments.iterrows():
                apt_datetime = pd.to_datetime(apt['appointment_date'])
                
                status_colors = {
                    'realizada': '#4CAF50',
                    'cancelado': '#F44336',
                    'agendado': '#2196F3'
                }
                
                status_color = status_colors.get(apt['status'], '#757575')
                
                st.markdown(f"""
                <div class="appointment-card" style="border-left-color: {status_color};">
                    <h5>{apt_datetime.strftime('%d/%m/%Y às %H:%M')} - {apt['nutritionist_name']}</h5>
                    <p><strong>Tipo:</strong> {apt['appointment_type']} | 
                       <strong>Status:</strong> <span style="color: {status_color};">{apt['status'].title()}</span></p>
                    {f"<p><strong>Peso registrado:</strong> {apt['weight_recorded']} kg</p>" if apt['weight_recorded'] else ""}
                    {f"<p><strong>Observações:</strong> {apt['notes']}</p>" if apt['notes'] else ""}
                    {f"<p><strong>Follow-up:</strong> {pd.to_datetime(apt['follow_up_date']).strftime('%d/%m/%Y')}</p>" if apt['follow_up_date'] else ""}
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.info("Você ainda não possui histórico de consultas.")
    
    conn.close()

def show_appointment_preparation():
    """Dicas de preparação para consulta"""
    st.info("""
    **📝 Como se preparar para sua consulta:**
    
    **Antes da consulta:**
    • Liste suas dúvidas e objetivos
    • Anote mudanças no seu peso ou medidas
    • Registre dificuldades ou desafios alimentares
    • Traga seus exames mais recentes
    • Anote medicamentos que está tomando
    
    **Leve com você:**
    • Documento de identidade
    • Carteirinha do convênio (se aplicável)
    • Lista de medicamentos atuais
    • Exames de sangue recentes
    • Diário alimentar (se fizer)
    
    **Durante a consulta:**
    • Seja honesto sobre seus hábitos
    • Tire todas as suas dúvidas
    • Anote as orientações recebidas
    • Pergunte sobre o próximo retorno
    """)

def show_my_plan():
    """Plano alimentar do paciente"""
    st.markdown('<h1 class="main-header">📋 Meu Plano Alimentar</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar ID do paciente
    patient_data = pd.read_sql_query("SELECT id FROM patients WHERE user_id = ?", conn, params=[user_id])
    
    if patient_data.empty:
        st.error("Dados do paciente não encontrados.")
        conn.close()
        return
    
    patient_id = patient_data.iloc[0]['id']
    
    # Buscar plano ativo
    active_plan = pd.read_sql_query("""
        SELECT 
            mp.*,
            n.full_name as nutritionist_name
        FROM meal_plans mp
        JOIN users n ON n.id = mp.nutritionist_id
        WHERE mp.patient_id = ? AND mp.status = 'ativo'
        ORDER BY mp.created_at DESC
        LIMIT 1
    """, conn, params=[patient_id])
    
    conn.close()
    
    if not active_plan.empty:
        plan = active_plan.iloc[0]
        
        # Header do plano
        st.markdown(f"""
        <div class="dashboard-card">
            <h3>📋 {plan['plan_name']}</h3>
            <p><strong>Nutricionista:</strong> {plan['nutritionist_name']}</p>
            <p><strong>Período:</strong> {pd.to_datetime(plan['start_date']).strftime('%d/%m/%Y')} até {pd.to_datetime(plan['end_date']).strftime('%d/%m/%Y') if plan['end_date'] else 'Indeterminado'}</p>
            <p><strong>Calorias diárias:</strong> {plan['daily_calories']} kcal</p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            plan_data = json.loads(plan['plan_data'])
            
            # Distribuição de macronutrientes
            st.subheader("🔢 Distribuição de Macronutrientes")
            
            macros = plan_data.get('macros', {})
            col_macro1, col_macro2, col_macro3 = st.columns(3)
            
            with col_macro1:
                carbs_cals = int(plan['daily_calories'] * macros.get('carbs', 0) / 100)
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #FF9800;">🍞 Carboidratos</h4>
                    <p>{macros.get('carbs', 0)}% ({carbs_cals} kcal)</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_macro2:
                protein_cals = int(plan['daily_calories'] * macros.get('protein', 0) / 100)
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #4CAF50;">🥩 Proteínas</h4>
                    <p>{macros.get('protein', 0)}% ({protein_cals} kcal)</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_macro3:
                fat_cals = int(plan['daily_calories'] * macros.get('fat', 0) / 100)
                st.markdown(f"""
                <div class="metric-card">
                    <h4 style="color: #9C27B0;">🥑 Gorduras</h4>
                    <p>{macros.get('fat', 0)}% ({fat_cals} kcal)</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráfico de pizza dos macros
            macros_df = pd.DataFrame([
                {'Nutriente': 'Carboidratos', 'Porcentagem': macros.get('carbs', 0)},
                {'Nutriente': 'Proteínas', 'Porcentagem': macros.get('protein', 0)},
                {'Nutriente': 'Gorduras', 'Porcentagem': macros.get('fat', 0)}
            ])
            
            fig_macros = px.pie(macros_df, values='Porcentagem', names='Nutriente',
                              title="Distribuição de Macronutrientes")
            st.plotly_chart(fig_macros, use_container_width=True)
            
            # Distribuição das refeições
            st.subheader("🍽️ Plano de Refeições Diário")
            
            meals = plan_data.get('meals', {})
            
            for meal_name, meal_info in meals.items():
                time = meal_info.get('time', 'N/A')
                calories = meal_info.get('calories', 0)
                percent = meal_info.get('percent', 0)
                
                st.markdown(f"""
                <div class="recipe-card">
                    <h4>🕐 {time} - {meal_name}</h4>
                    <p><strong>Calorias:</strong> {calories} kcal ({percent}% do total)</p>
                    <div style="width: 100%; background: #f0f0f0; border-radius: 10px; height: 10px;">
                        <div style="width: {percent}%; background: #4CAF50; height: 100%; border-radius: 10px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Observações do nutricionista
            notes = plan_data.get('notes', '')
            if notes:
                st.subheader("📝 Orientações do Nutricionista")
                st.markdown(f"""
                <div class="dashboard-card" style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);">
                    <p>{notes}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Perfil considerado
            patient_profile = plan_data.get('patient_profile', {})
            if patient_profile:
                st.subheader("👤 Perfil Considerado no Plano")
                
                col_profile1, col_profile2 = st.columns(2)
                
                with col_profile1:
                    st.write(f"**Peso atual:** {patient_profile.get('current_weight', 'N/A')} kg")
                    st.write(f"**Peso objetivo:** {patient_profile.get('target_weight', 'N/A')} kg")
                    st.write(f"**Nível de atividade:** {patient_profile.get('activity_level', 'N/A')}")
                
                with col_profile2:
                    st.write(f"**Condições médicas:** {patient_profile.get('medical_conditions', 'Nenhuma')}")
                    st.write(f"**Alergias:** {patient_profile.get('allergies', 'Nenhuma')}")
                    st.write(f"**Preferências:** {patient_profile.get('dietary_preferences', 'Nenhuma')}")
            
            # Dicas de adesão
            st.subheader("💡 Dicas para Seguir seu Plano")
            
            tips = [
                "📱 **Planejamento:** Prepare suas refeições com antecedência",
                "💧 **Hidratação:** Beba água antes, durante e após as refeições",
                "⏰ **Horários:** Respeite os horários sugeridos para cada refeição",
                "🍽️ **Porções:** Use pratos menores para controlar as porções",
                "📝 **Registro:** Anote como se sente após cada refeição",
                "🤝 **Apoio:** Compartilhe seu plano com família e amigos",
                "📞 **Dúvidas:** Entre em contato com seu nutricionista sempre que necessário"
            ]
            
            for tip in tips:
                st.write(tip)
        
        except json.JSONDecodeError:
            st.error("Erro ao carregar dados do plano. Entre em contato com seu nutricionista.")
    
    else:
        st.info("Você ainda não possui um plano alimentar ativo.")
        st.write("Aguarde sua próxima consulta ou entre em contato com seu nutricionista.")
        
        # Orientações gerais enquanto não tem plano
        st.subheader("🌟 Orientações Gerais")
        
        general_tips = [
            "🥗 **Vegetais:** Inclua vegetais em pelo menos 2 refeições por dia",
            "🍎 **Frutas:** Consuma 2-3 porções de frutas variadas diariamente", 
            "💧 **Água:** Beba pelo menos 2 litros de água por dia",
            "🍚 **Carboidratos:** Prefira versões integrais (arroz, pão, massas)",
            "🥩 **Proteínas:** Inclua uma fonte de proteína em cada refeição principal",
            "🕐 **Regularidade:** Mantenha horários regulares para as refeições",
            "🚫 **Evite:** Alimentos ultraprocessados e bebidas açucaradas"
        ]
        
        for tip in general_tips:
            st.write(tip)

def show_points_badges():
    """Sistema de pontos e badges do paciente"""
    st.markdown('<h1 class="main-header">🎯 Pontos & Conquistas</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar ID do paciente
    patient_data = pd.read_sql_query("SELECT id FROM patients WHERE user_id = ?", conn, params=[user_id])
    
    if patient_data.empty:
        st.error("Dados do paciente não encontrados.")
        conn.close()
        return
    
    patient_id = patient_data.iloc[0]['id']
    
    # Dados de pontuação
    points_data = pd.read_sql_query("""
        SELECT * FROM patient_points WHERE patient_id = ?
    """, conn, params=[patient_id])
    
    if points_data.empty:
        # Inicializar sistema de pontos
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO patient_points (patient_id, points, level, total_points)
            VALUES (?, 0, 1, 0)
        """, (patient_id,))
        conn.commit()
        points_data = pd.read_sql_query("SELECT * FROM patient_points WHERE patient_id = ?", conn, params=[patient_id])
    
    points_info = points_data.iloc[0]
    
    # Dashboard de pontuação
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="gamification-card">
            <h2 style="margin: 0; color: #9C27B0;">🎯 {points_info['points']}</h2>
            <p style="margin: 0;">Pontos Atuais</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="gamification-card">
            <h2 style="margin: 0; color: #FF9800;">⭐ {points_info['level']}</h2>
            <p style="margin: 0;">Nível Atual</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="gamification-card">
            <h2 style="margin: 0; color: #4CAF50;">🏆 {points_info['total_points']}</h2>
            <p style="margin: 0;">Total de Pontos</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="gamification-card">
            <h2 style="margin: 0; color: #F44336;">🔥 {points_info['streak_days']}</h2>
            <p style="margin: 0;">Dias Seguidos</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Barra de progresso para próximo nível
    current_level = points_info['level']
    points_for_next_level = calculate_points_for_level(current_level + 1)
    points_needed = points_for_next_level - points_info['total_points']
    
    if points_needed > 0:
        progress_percentage = (points_info['total_points'] % points_for_next_level) / points_for_next_level * 100
        
        st.subheader(f"📊 Progresso para Nível {current_level + 1}")
        st.progress(progress_percentage / 100)
        st.write(f"Faltam {points_needed} pontos para o próximo nível!")
    else:
        st.success("🎉 Você pode subir de nível! Consulte seu nutricionista.")
    
    # Minhas badges
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("🏆 Minhas Conquistas")
        
        badges_data = pd.read_sql_query("""
            SELECT * FROM patient_badges 
            WHERE patient_id = ?
            ORDER BY earned_date DESC
        """, conn, params=[patient_id])
        
        if not badges_data.empty:
            for idx, badge in badges_data.iterrows():
                earned_date = pd.to_datetime(badge['earned_date']).strftime('%d/%m/%Y')
                
                st.markdown(f"""
                <div class="gamification-card">
                    <h4>{badge['badge_icon']} {badge['badge_name']}</h4>
                    <p style="font-size: 0.9rem; margin: 0.5rem 0;">{badge['badge_description']}</p>
                    <small>Conquistada em {earned_date} | +{badge['points_awarded']} pontos</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Você ainda não conquistou nenhuma badge. Continue seu acompanhamento!")
    
    with col_right:
        st.subheader("🎯 Badges Disponíveis")
        
        available_badges = get_available_badges()
        
        for badge in available_badges:
            st.markdown(f"""
            <div class="gamification-card" style="opacity: 0.7;">
                <h4>{badge['icon']} {badge['name']}</h4>
                <p style="font-size: 0.9rem; margin: 0.5rem 0;">{badge['description']}</p>
                <small>Recompensa: +{badge['points']} pontos</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Sistema de recompensas
    st.subheader("🎁 Como Ganhar Pontos")
    
    point_activities = [
        {"atividade": "Comparecer à consulta", "pontos": 20},
        {"atividade": "Primeira semana de acompanhamento", "pontos": 10},
        {"atividade": "Atingir peso objetivo semanal", "pontos": 15},
        {"atividade": "Manter streak de 7 dias", "pontos": 25},
        {"atividade": "Manter streak de 30 dias", "pontos": 100},
        {"atividade": "Perder 1kg de forma saudável", "pontos": 30},
        {"atividade": "Melhorar composição corporal", "pontos": 25},
        {"atividade": "Seguir plano alimentar", "pontos": 5},
    ]
    
    activities_df = pd.DataFrame(point_activities)
    st.dataframe(activities_df, use_container_width=True)
    
    # Histórico de pontos
    st.subheader("📈 Histórico de Pontos")
    
    # Como não temos tabela de histórico, simular baseado nas badges
    if not badges_data.empty:
        badges_timeline = badges_data[['earned_date', 'badge_name', 'points_awarded']].copy()
        badges_timeline['earned_date'] = pd.to_datetime(badges_timeline['earned_date'])
        badges_timeline = badges_timeline.sort_values('earned_date')
        badges_timeline['pontos_acumulados'] = badges_timeline['points_awarded'].cumsum()
        
        fig_points = px.line(badges_timeline, x='earned_date', y='pontos_acumulados',
                           title='Acúmulo de Pontos ao Longo do Tempo', markers=True)
        st.plotly_chart(fig_points, use_container_width=True)
    
    conn.close()

def calculate_points_for_level(level):
    """Calcula pontos necessários para um nível"""
    return level * 100  # 100 pontos por nível (pode ser ajustado)

def get_available_badges():
    """Retorna badges disponíveis no sistema"""
    return [
        {"name": "Primeiro Passo", "description": "Complete sua primeira consulta", "icon": "🚀", "points": 20},
        {"name": "Persistência", "description": "Mantenha 7 dias consecutivos", "icon": "💪", "points": 25},
        {"name": "Dedicação", "description": "Mantenha 30 dias consecutivos", "icon": "🔥", "points": 100},
        {"name": "Meta Alcançada", "description": "Atinja seu peso objetivo", "icon": "🎯", "points": 150},
        {"name": "Transformação", "description": "Melhore sua composição corporal", "icon": "⚡", "points": 75},
        {"name": "Disciplina", "description": "Complete 10 consultas", "icon": "📚", "points": 50},
        {"name": "Inspiração", "description": "Ajude outros pacientes", "icon": "🌟", "points": 40},
        {"name": "Saúde de Ferro", "description": "Melhore seus exames", "icon": "💎", "points": 80}
    ]

def show_calculators():
    """Calculadoras nutricionais para nutricionistas"""
    st.markdown('<h1 class="main-header">🧮 Calculadoras Nutricionais</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["⚖️ IMC & Composição", "🔥 Gasto Energético", "📊 Macronutrientes", "💧 Hidratação"])
    
    with tab1:
        show_bmi_composition_calculator()
    
    with tab2:
        show_energy_expenditure_calculator()
    
    with tab3:
        show_macronutrient_calculator()
    
    with tab4:
        show_hydration_calculator()

def show_bmi_composition_calculator():
    """Calculadora de IMC e composição corporal"""
    st.subheader("⚖️ Calculadora de IMC e Composição Corporal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📏 Dados Antropométricos**")
        
        weight = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)
        height = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01)
        age = st.number_input("Idade (anos)", min_value=1, max_value=120, value=30)
        gender = st.selectbox("Sexo", ["Masculino", "Feminino"])
        
        # Medidas opcionais
        st.write("**📐 Medidas Adicionais (opcional)**")
        waist = st.number_input("Circunferência da cintura (cm)", min_value=0.0, value=0.0, step=0.1)
        hip = st.number_input("Circunferência do quadril (cm)", min_value=0.0, value=0.0, step=0.1)
        neck = st.number_input("Circunferência do pescoço (cm)", min_value=0.0, value=0.0, step=0.1)
    
    with col2:
        if st.button("🧮 Calcular", use_container_width=True):
            # Cálculo do IMC
            bmi = weight / (height ** 2)
            
            # Classificação do IMC
            if bmi < 18.5:
                bmi_category = "Abaixo do peso"
                bmi_color = "#2196F3"
            elif bmi < 25:
                bmi_category = "Peso normal"
                bmi_color = "#4CAF50"
            elif bmi < 30:
                bmi_category = "Sobrepeso"
                bmi_color = "#FF9800"
            else:
                bmi_category = "Obesidade"
                bmi_color = "#F44336"
            
            # Resultados
            st.markdown(f"""
            <div class="metric-card" style="border: 2px solid {bmi_color};">
                <h3 style="margin: 0; color: {bmi_color};">IMC: {bmi:.1f}</h3>
                <p style="margin: 0;">{bmi_category}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Peso ideal (fórmula de Robinson)
            if gender == "Masculino":
                ideal_weight = 52 + 1.9 * ((height * 100) - 152.4) / 2.54
            else:
                ideal_weight = 49 + 1.7 * ((height * 100) - 152.4) / 2.54
            
            st.metric("Peso Ideal (Robinson)", f"{ideal_weight:.1f} kg")
            
            # Faixa de peso saudável
            healthy_min = 18.5 * (height ** 2)
            healthy_max = 24.9 * (height ** 2)
            st.write(f"**Faixa de peso saudável:** {healthy_min:.1f} - {healthy_max:.1f} kg")
            
            # Relação Cintura-Quadril (se disponível)
            if waist > 0 and hip > 0:
                whr = waist / hip
                whr_risk = "Baixo" if (gender == "Masculino" and whr < 0.9) or (gender == "Feminino" and whr < 0.85) else "Alto"
                st.metric("Relação Cintura-Quadril", f"{whr:.2f}")
                st.write(f"**Risco cardiovascular:** {whr_risk}")
            
            # Estimativa de gordura corporal (fórmula Navy)
            if waist > 0 and neck > 0:
                if gender == "Masculino":
                    body_fat = 495 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height * 100)) - 450
                else:
                    if hip > 0:
                        body_fat = 495 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.22100 * math.log10(height * 100)) - 450
                    else:
                        body_fat = None
                
                if body_fat:
                    st.metric("Estimativa % Gordura Corporal", f"{body_fat:.1f}%")

def show_energy_expenditure_calculator():
    """Calculadora de gasto energético"""
    st.subheader("🔥 Calculadora de Gasto Energético")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**👤 Dados Pessoais**")
        
        weight_tee = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1, key="weight_tee")
        height_tee = st.number_input("Altura (cm)", min_value=100, max_value=250, value=170, key="height_tee")
        age_tee = st.number_input("Idade (anos)", min_value=1, max_value=120, value=30, key="age_tee")
        gender_tee = st.selectbox("Sexo", ["Masculino", "Feminino"], key="gender_tee")
        
        st.write("**🏃‍♀️ Nível de Atividade**")
        activity_level = st.selectbox("Selecione o nível", [
            "Sedentário (pouco ou nenhum exercício)",
            "Levemente ativo (exercício leve 1-3 dias/semana)",
            "Moderadamente ativo (exercício moderado 3-5 dias/semana)",
            "Muito ativo (exercício intenso 6-7 dias/semana)",
            "Extremamente ativo (exercício muito intenso, trabalho físico)"
        ])
        
        # Fatores de atividade física
        activity_factors = {
            "Sedentário (pouco ou nenhum exercício)": 1.2,
            "Levemente ativo (exercício leve 1-3 dias/semana)": 1.375,
            "Moderadamente ativo (exercício moderado 3-5 dias/semana)": 1.55,
            "Muito ativo (exercício intenso 6-7 dias/semana)": 1.725,
            "Extremamente ativo (exercício muito intenso, trabalho físico)": 1.9
        }
    
    with col2:
        if st.button("🧮 Calcular Gasto", use_container_width=True):
            # TMB - Taxa Metabólica Basal (Fórmula de Harris-Benedict revisada)
            if gender_tee == "Masculino":
                bmr = 88.362 + (13.397 * weight_tee) + (4.799 * height_tee) - (5.677 * age_tee)
            else:
                bmr = 447.593 + (9.247 * weight_tee) + (3.098 * height_tee) - (4.330 * age_tee)
            
            # GET - Gasto Energético Total
            activity_factor = activity_factors[activity_level]
            tee = bmr * activity_factor
            
            # Resultados
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #4CAF50;">TMB: {bmr:.0f} kcal/dia</h3>
                <p style="margin: 0;">Taxa Metabólica Basal</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #FF9800;">GET: {tee:.0f} kcal/dia</h3>
                <p style="margin: 0;">Gasto Energético Total</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Objetivos calóricos
            st.write("**🎯 Objetivos Calóricos:**")
            
            col_goal1, col_goal2, col_goal3 = st.columns(3)
            
            with col_goal1:
                maintenance = tee
                st.metric("Manutenção", f"{maintenance:.0f} kcal")
            
            with col_goal2:
                weight_loss = tee - 500  # Déficit de 500 kcal
                st.metric("Emagrecimento", f"{weight_loss:.0f} kcal")
                st.caption("-0.5kg/semana")
            
            with col_goal3:
                weight_gain = tee + 500  # Superávit de 500 kcal
                st.metric("Ganho de peso", f"{weight_gain:.0f} kcal")
                st.caption("+0.5kg/semana")
            
            # Distribuição por refeição
            st.write("**🍽️ Distribuição Sugerida (Emagrecimento):**")
            
            breakfast = weight_loss * 0.25
            lunch = weight_loss * 0.35
            snack1 = weight_loss * 0.10
            snack2 = weight_loss * 0.10
            dinner = weight_loss * 0.20
            
            meal_distribution = {
                "Café da manhã": f"{breakfast:.0f} kcal (25%)",
                "Lanche manhã": f"{snack1:.0f} kcal (10%)",
                "Almoço": f"{lunch:.0f} kcal (35%)",
                "Lanche tarde": f"{snack2:.0f} kcal (10%)",
                "Jantar": f"{dinner:.0f} kcal (20%)"
            }
            
            for meal, calories in meal_distribution.items():
                st.write(f"• **{meal}:** {calories}")

def show_macronutrient_calculator():
    """Calculadora de distribuição de macronutrientes"""
    st.subheader("📊 Calculadora de Macronutrientes")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🎯 Configuração do Plano**")
        
        total_calories = st.number_input("Calorias totais diárias", min_value=800, max_value=5000, value=2000, step=50)
        
        st.write("**📊 Distribuição de Macronutrientes (%)**")
        
        # Presets comuns
        preset = st.selectbox("Preset sugerido:", [
            "Personalizado",
            "Equilibrado (45C/25P/30G)",
            "Low Carb (25C/30P/45G)",
            "High Carb (60C/15P/25G)",
            "Cetogênica (5C/25P/70G)",
            "Atlético (50C/25P/25G)"
        ])
        
        if preset == "Equilibrado (45C/25P/30G)":
            carbs_percent = 45
            protein_percent = 25
            fat_percent = 30
        elif preset == "Low Carb (25C/30P/45G)":
            carbs_percent = 25
            protein_percent = 30
            fat_percent = 45
        elif preset == "High Carb (60C/15P/25G)":
            carbs_percent = 60
            protein_percent = 15
            fat_percent = 25
        elif preset == "Cetogênica (5C/25P/70G)":
            carbs_percent = 5
            protein_percent = 25
            fat_percent = 70
        elif preset == "Atlético (50C/25P/25G)":
            carbs_percent = 50
            protein_percent = 25
            fat_percent = 25
        else:
            carbs_percent = st.slider("Carboidratos (%)", 0, 80, 45)
            protein_percent = st.slider("Proteínas (%)", 10, 50, 25)
            fat_percent = st.slider("Gorduras (%)", 10, 80, 30)
        
        # Verificar se soma 100%
        total_percent = carbs_percent + protein_percent + fat_percent
        if total_percent != 100:
            st.warning(f"Total atual: {total_percent}%. Ajuste para 100%")
    
    with col2:
        if total_percent == 100:
            st.write("**📊 Resultados dos Cálculos**")
            
            # Cálculos
            carbs_calories = total_calories * carbs_percent / 100
            protein_calories = total_calories * protein_percent / 100
            fat_calories = total_calories * fat_percent / 100
            
            carbs_grams = carbs_calories / 4  # 4 kcal por grama
            protein_grams = protein_calories / 4  # 4 kcal por grama
            fat_grams = fat_calories / 9  # 9 kcal por grama
            
            # Resultados em formato tabular
            results_data = {
                "Macronutriente": ["Carboidratos", "Proteínas", "Gorduras"],
                "Porcentagem": [f"{carbs_percent}%", f"{protein_percent}%", f"{fat_percent}%"],
                "Calorias": [f"{carbs_calories:.0f} kcal", f"{protein_calories:.0f} kcal", f"{fat_calories:.0f} kcal"],
                "Gramas": [f"{carbs_grams:.0f}g", f"{protein_grams:.0f}g", f"{fat_grams:.0f}g"]
            }
            
            results_df = pd.DataFrame(results_data)
            st.dataframe(results_df, use_container_width=True)
            
            # Gráfico visual
            macro_data = pd.DataFrame({
                'Macronutriente': ['Carboidratos', 'Proteínas', 'Gorduras'],
                'Porcentagem': [carbs_percent, protein_percent, fat_percent],
                'Calorias': [carbs_calories, protein_calories, fat_calories]
            })
            
            fig = px.pie(macro_data, values='Porcentagem', names='Macronutriente',
                        title=f"Distribuição de Macronutrientes - {total_calories} kcal")
            st.plotly_chart(fig, use_container_width=True)
            
            # Equivalências práticas
            st.write("**🥗 Equivalências Práticas**")
            
            equivalences = {
                f"Carboidratos ({carbs_grams:.0f}g)": [
                    f"• {carbs_grams/20:.1f} fatias de pão integral",
                    f"• {carbs_grams/25:.1f} xícaras de arroz cozido",
                    f"• {carbs_grams/15:.1f} frutas médias",
                ],
                f"Proteínas ({protein_grams:.0f}g)": [
                    f"• {protein_grams/25:.1f} peitos de frango (100g cada)",
                    f"• {protein_grams/12:.1f} ovos",
                    f"• {protein_grams/20:.1f} porções de peixe (100g cada)",
                ],
                f"Gorduras ({fat_grams:.0f}g)": [
                    f"• {fat_grams/14:.1f} colheres de sopa de azeite",
                    f"• {fat_grams/30:.1f} abacates médios",
                    f"• {fat_grams/5:.1f} colheres de sopa de oleaginosas",
                ]
            }
            
            for macro, foods in equivalences.items():
                st.write(f"**{macro}:**")
                for food in foods:
                    st.write(food)

def show_hydration_calculator():
    """Calculadora de necessidades hídricas"""
    st.subheader("💧 Calculadora de Hidratação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**👤 Dados Pessoais**")
        
        weight_hydration = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1, key="weight_hydration")
        age_hydration = st.number_input("Idade (anos)", min_value=1, max_value=120, value=30, key="age_hydration")
        
        st.write("**🏃‍♀️ Fatores Adicionais**")
        
        activity_duration = st.number_input("Duração do exercício (minutos/dia)", min_value=0, max_value=480, value=0)
        climate = st.selectbox("Clima", ["Temperado", "Quente/Úmido", "Seco"])
        pregnancy = st.checkbox("Gravidez")
        breastfeeding = st.checkbox("Amamentação")
        fever = st.checkbox("Febre")
    
    with col2:
        if st.button("💧 Calcular Necessidades", use_container_width=True):
            # Necessidade base: 35ml por kg de peso corporal
            base_hydration = weight_hydration * 35
            
            # Ajustes por idade
            if age_hydration > 65:
                age_factor = 1.1  # Idosos precisam de mais água
            elif age_hydration < 18:
                age_factor = 1.15  # Jovens precisam de mais água
            else:
                age_factor = 1.0
            
            # Ajustes por exercício (550ml por hora de exercício)
            exercise_water = (activity_duration / 60) * 550
            
            # Ajustes por clima
            climate_factors = {
                "Temperado": 1.0,
                "Quente/Úmido": 1.2,
                "Seco": 1.15
            }
            climate_factor = climate_factors[climate]
            
            # Ajustes por condições especiais
            special_factor = 1.0
            if pregnancy:
                special_factor += 0.1
            if breastfeeding:
                special_factor += 0.2
            if fever:
                special_factor += 0.15
            
            # Cálculo final
            total_hydration = (base_hydration * age_factor * climate_factor * special_factor) + exercise_water
            
            # Conversões
            liters = total_hydration / 1000
            glasses = total_hydration / 200  # Copo de 200ml
            
            # Resultados
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #2196F3;">{total_hydration:.0f} ml/dia</h3>
                <p style="margin: 0;">Necessidade Total</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.metric("Em Litros", f"{liters:.1f}L")
            st.metric("Em Copos (200ml)", f"{glasses:.0f} copos")
            
            # Distribuição ao longo do dia
            st.write("**⏰ Distribuição Sugerida:**")
            
            schedule = {
                "Ao acordar": f"{total_hydration * 0.15:.0f}ml",
                "Manhã (até 10h)": f"{total_hydration * 0.25:.0f}ml",
                "Tarde (10h-16h)": f"{total_hydration * 0.35:.0f}ml",
                "Noite (16h-20h)": f"{total_hydration * 0.20:.0f}ml",
                "Antes de dormir": f"{total_hydration * 0.05:.0f}ml"
            }
            
            for time, amount in schedule.items():
                st.write(f"• **{time}:** {amount}")
            
            # Dicas especiais
            st.write("**💡 Dicas Importantes:**")
            
            tips = [
                "💧 **Qualidade:** Prefira água filtrada ou mineral",
                "🌡️ **Temperatura:** Água em temperatura ambiente é melhor absorvida",
                "🏃‍♀️ **Exercício:** Beba 200ml antes, durante e após o exercício",
                "🍎 **Alimentos:** Frutas e vegetais também contribuem para hidratação",
                "⚠️ **Sinais:** Urina escura indica desidratação",
                "📱 **Lembretes:** Use apps para lembrar de beber água"
            ]
            
            for tip in tips:
                st.write(tip)
            
            # Alertas especiais
            if exercise_water > 1000:
                st.warning("⚡ Com mais de 2h de exercício, considere repositores hidroeletrolíticos")
            
            if total_hydration > 4000:
                st.info("💊 Necessidades altas podem requerer acompanhamento médico")

def show_calculators_personal():
    """Calculadoras simplificadas para pacientes"""
    st.markdown('<h1 class="main-header">🧮 Minhas Calculadoras</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["⚖️ Meu IMC", "💧 Minha Hidratação", "🏃‍♀️ Minhas Calorias"])
    
    with tab1:
        show_simple_bmi_calculator()
    
    with tab2:
        show_simple_hydration_calculator()
    
    with tab3:
        show_simple_calorie_calculator()

def show_simple_bmi_calculator():
    """Calculadora de IMC simplificada para pacientes"""
    st.subheader("⚖️ Calculadora de IMC")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("Seu peso (kg)", min_value=30.0, max_value=300.0, value=70.0, step=0.1)
        height = st.number_input("Sua altura (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01)
        
        if st.button("🧮 Calcular meu IMC", use_container_width=True):
            bmi = weight / (height ** 2)
            
            if bmi < 18.5:
                category = "Abaixo do peso"
                color = "#2196F3"
                advice = "Considere consultar um nutricionista para ganho de peso saudável."
            elif bmi < 25:
                category = "Peso normal"
                color = "#4CAF50"
                advice = "Parabéns! Mantenha hábitos saudáveis."
            elif bmi < 30:
                category = "Sobrepeso"
                color = "#FF9800"
                advice = "Pequenas mudanças na dieta e exercícios podem ajudar."
            else:
                category = "Obesidade"
                color = "#F44336"
                advice = "Busque acompanhamento profissional para emagrecimento saudável."
            
            st.session_state['calculated_bmi'] = {
                'value': bmi,
                'category': category,
                'color': color,
                'advice': advice
            }
    
    with col2:
        if 'calculated_bmi' in st.session_state:
            result = st.session_state['calculated_bmi']
            
            st.markdown(f"""
            <div class="metric-card" style="border: 3px solid {result['color']};">
                <h2 style="margin: 0; color: {result['color']};">IMC: {result['value']:.1f}</h2>
                <h4 style="margin: 0;">{result['category']}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            st.info(f"💡 {result['advice']}")
            
            # Faixa de peso saudável
            healthy_min = 18.5 * (height ** 2)
            healthy_max = 24.9 * (height ** 2)
            
            st.write(f"**Faixa de peso saudável para sua altura:**")
            st.write(f"{healthy_min:.1f}kg - {healthy_max:.1f}kg")

def show_simple_hydration_calculator():
    """Calculadora de hidratação simplificada"""
    st.subheader("💧 Calculadora de Hidratação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight_h = st.number_input("Seu peso (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1, key="weight_simple_h")
        exercise_time = st.number_input("Tempo de exercício hoje (minutos)", min_value=0, max_value=240, value=0)
        
        if st.button("💧 Calcular minha necessidade", use_container_width=True):
            base_water = weight_h * 35  # 35ml por kg
            exercise_water = (exercise_time / 60) * 500  # 500ml por hora de exercício
            total_water = base_water + exercise_water
            
            st.session_state['calculated_hydration'] = {
                'total': total_water,
                'liters': total_water / 1000,
                'glasses': total_water / 200
            }
    
    with col2:
        if 'calculated_hydration' in st.session_state:
            result = st.session_state['calculated_hydration']
            
            st.markdown(f"""
            <div class="metric-card">
                <h2 style="margin: 0; color: #2196F3;">{result['liters']:.1f}L</h2>
                <p style="margin: 0;">Por dia</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.write(f"**Isso equivale a:**")
            st.write(f"• {result['glasses']:.0f} copos de 200ml")
            st.write(f"• {result['total']:.0f}ml total")
            
            st.success("💡 Distribua ao longo do dia e beba pequenos goles frequentemente!")

def show_simple_calorie_calculator():
    """Calculadora de calorias simplificada"""
    st.subheader("🏃‍♀️ Calculadora de Calorias")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight_c = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.1, key="weight_simple_c")
        height_c = st.number_input("Altura (cm)", min_value=100, max_value=220, value=170, key="height_simple_c")
        age_c = st.number_input("Idade (anos)", min_value=15, max_value=80, value=30, key="age_simple_c")
        gender_c = st.selectbox("Sexo", ["Feminino", "Masculino"], key="gender_simple_c")
        activity_c = st.selectbox("Seu nível de atividade:", [
            "Sedentário (pouco exercício)",
            "Levemente ativo (exercício 1-3x/semana)",
            "Moderadamente ativo (exercício 3-5x/semana)",
            "Muito ativo (exercício 6-7x/semana)"
        ])
        
        if st.button("🔥 Calcular minhas calorias", use_container_width=True):
            # TMB
            if gender_c == "Masculino":
                bmr = 88.362 + (13.397 * weight_c) + (4.799 * height_c) - (5.677 * age_c)
            else:
                bmr = 447.593 + (9.247 * weight_c) + (3.098 * height_c) - (4.330 * age_c)
            
            # Fator de atividade
            activity_factors = {
                "Sedentário (pouco exercício)": 1.2,
                "Levemente ativo (exercício 1-3x/semana)": 1.375,
                "Moderadamente ativo (exercício 3-5x/semana)": 1.55,
                "Muito ativo (exercício 6-7x/semana)": 1.725
            }
            
            total_calories = bmr * activity_factors[activity_c]
            
            st.session_state['calculated_calories'] = {
                'maintenance': total_calories,
                'weight_loss': total_calories - 300,
                'weight_gain': total_calories + 300
            }
    
    with col2:
        if 'calculated_calories' in st.session_state:
            result = st.session_state['calculated_calories']
            
            st.write("**🎯 Suas necessidades calóricas:**")
            
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #4CAF50;">Manter peso</h3>
                <h4 style="margin: 0;">{result['maintenance']:.0f} kcal/dia</h4>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #FF9800;">Emagrecer</h3>
                <h4 style="margin: 0;">{result['weight_loss']:.0f} kcal/dia</h4>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #2196F3;">Ganhar peso</h3>
                <h4 style="margin: 0;">{result['weight_gain']:.0f} kcal/dia</h4>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("⚠️ Estes são valores estimados. Consulte seu nutricionista para um plano personalizado!")

def show_patient_chat_ia():
    """Chat IA para pacientes"""
    st.markdown('<h1 class="main-header">💬 Chat com Assistente</h1>', unsafe_allow_html=True)
    
    st.info("🤖 Olá! Sou seu assistente nutricional. Posso ajudar com dúvidas sobre alimentação saudável, mas lembre-se: sempre siga as orientações do seu nutricionista!")
    
    # Inicializar histórico se não existir
    if 'patient_chat_history' not in st.session_state:
        st.session_state.patient_chat_history = []
    
    # Sugestões de perguntas para pacientes
    with st.expander("💡 Perguntas Frequentes", expanded=False):
        col_q1, col_q2 = st.columns(2)
        
        with col_q1:
            if st.button("🥗 Como montar um prato saudável?"):
                st.session_state.patient_suggested = "Como devo montar um prato saudável?"
            if st.button("💧 Preciso beber muita água?"):
                st.session_state.patient_suggested = "Quanta água devo beber por dia?"
            if st.button("🍎 Posso comer frutas à noite?"):
                st.session_state.patient_suggested = "É verdade que não posso comer frutas à noite?"
        
        with col_q2:
            if st.button("🏃‍♀️ O que comer antes do exercício?"):
                st.session_state.patient_suggested = "O que devo comer antes de fazer exercício?"
            if st.button("😫 Estou com muita fome, o que faço?"):
                st.session_state.patient_suggested = "Estou sentindo muita fome entre as refeições, o que posso fazer?"
            if st.button("🎂 Posso comer doce na dieta?"):
                st.session_state.patient_suggested = "Posso comer doce seguindo minha dieta?"
    
    # Input do usuário
    patient_question = st.text_input(
        "💭 Digite sua pergunta:",
        value=st.session_state.get('patient_suggested', ''),
        placeholder="Ex: Posso substituir o arroz por batata doce?",
        key='patient_input'
    )
    
    # Limpar sugestão
    if 'patient_suggested' in st.session_state:
        del st.session_state.patient_suggested
    
    col_send, col_clear = st.columns([3, 1])
    with col_send:
        send_button = st.button("🚀 Enviar", use_container_width=True)
    with col_clear:
        if st.button("🗑️ Limpar", use_container_width=True):
            st.session_state.patient_chat_history = []
            st.rerun()
    
    # Processar pergunta
    if send_button and patient_question:
        with st.spinner("🤔 Pensando..."):
            # Gerar resposta focada em orientações gerais para pacientes
            llm = LLMAssistant()
            context = "Paciente buscando orientações gerais de nutrição"
            
            # Personalizar resposta para pacientes
            response = generate_patient_friendly_response(patient_question, context)
            
            # Adicionar ao histórico
            st.session_state.patient_chat_history.append({
                'question': patient_question,
                'response': response,
                'timestamp': datetime.now()
            })
            
            # Salvar no banco
            user_id = st.session_state.user['id']
            save_llm_conversation(user_id, None, 'patient_chat', patient_question, response)
        
        st.rerun()
    
    # Exibir histórico
    if st.session_state.patient_chat_history:
        st.markdown("---")
        
        for i, chat in enumerate(reversed(st.session_state.patient_chat_history)):
            # Pergunta do paciente
            st.markdown(f"""
            <div style="background: #f3e5f5; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #9c27b0;">
                <strong>🙋‍♀️ Você perguntou:</strong><br>
                {chat['question']}
                <br><small>🕐 {chat['timestamp'].strftime('%d/%m/%Y %H:%M')}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Resposta do assistente
            st.markdown(f"""
            <div class="llm-response">
                <strong>🤖 Assistente respondeu:</strong><br>
                {chat['response']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
    else:
        st.info("💡 Faça uma pergunta para começar nossa conversa!")

def generate_patient_friendly_response(question, context):
    """Gera resposta amigável para pacientes"""
    question_lower = question.lower()
    
    # Respostas específicas para pacientes
    if any(word in question_lower for word in ["prato", "montar", "refeicao"]):
        return """
**🥗 Como Montar um Prato Saudável**

**📏 Regra do Prato Ideal:**
• **1/2 do prato:** Vegetais e saladas (quanto mais colorido, melhor!)
• **1/4 do prato:** Proteína (frango, peixe, ovos, leguminosas)
• **1/4 do prato:** Carboidratos (arroz integral, batata, quinoa)
• **1 colher de sopa:** Gordura boa (azeite, abacate)

**🌈 Dica das Cores:**
Quanto mais colorido seu prato, mais nutrientes você está consumindo!
Verde (brócolis), laranja (cenoura), roxo (repolho roxo), vermelho (tomate).

**⚠️ Lembre-se:** Estas são orientações gerais. Sempre siga as recomendações específicas do seu nutricionista!
        """
    
    elif any(word in question_lower for word in ["agua", "hidrat", "beber"]):
        return """
**💧 Hidratação Adequada**

**🎯 Meta Diária:**
• **Fórmula simples:** 35ml × seu peso em kg
• **Exemplo:** Se você pesa 70kg = 70 × 35 = 2,45L por dia

**⏰ Como Distribuir:**
• **Ao acordar:** 1-2 copos
• **Manhã:** 2-3 copos
• **Tarde:** 3-4 copos  
• **Noite:** 1-2 copos

**💡 Dicas Práticas:**
• Use uma garrafa para controlar a quantidade
• Beba pequenos goles ao longo do dia
• Água em temperatura ambiente é melhor absorvida
• Apps de lembrete podem ajudar!

**🚨 Sinais de desidratação:** urina escura, boca seca, dor de cabeça.
        """
    
    elif any(word in question_lower for word in ["fruta", "noite", "tarde"]):
        return """
**🍎 Frutas à Noite: Mito ou Verdade?**

**✅ PODE SIM comer frutas à noite!**

**🧬 A Ciência Explica:**
• Frutas têm fibras que ajudam na digestão
• Açúcar das frutas (frutose) é natural e vem com vitaminas
• O que importa é o total de calorias do dia, não o horário

**🎯 Dicas Inteligentes:**
• **Prefira:** Maçã, pera, morango, kiwi (menos açúcar)
• **Evite exageros:** 1 fruta média é suficiente
• **Combine:** Com iogurte natural ou nuts para mais saciedade

**⚠️ Atenção:** Se você tem diabetes, converse com seu nutricionista sobre os melhores horários.

**Resumo:** Não é o horário que engorda, mas sim comer além do que o corpo precisa!
        """
    
    elif any(word in question_lower for word in ["exercicio", "treino", "academia"]):
        return """
**🏃‍♀️ Alimentação e Exercício**

**⏰ ANTES do Exercício (30-60min antes):**
• **Carboidrato de fácil digestão:** 1 banana, 2 tâmaras
• **Evite:** Fibras em excesso, gorduras, grandes quantidades
• **Hidratação:** 300-500ml de água

**💪 DURANTE o Exercício:**
• **Menos de 1h:** Só água
• **Mais de 1h:** Isotônico ou água de coco

**🔋 APÓS o Exercício (até 30min depois):**
• **Proteína:** Whey, ovos, iogurte grego
• **Carboidrato:** Banana, pão integral, aveia
• **Hidratação:** Reponha o que perdeu no suor

**💡 Exemplo Pós-Treino:**
• Vitamina: 1 banana + 200ml leite + 1 colher aveia
• Ou: 2 ovos mexidos + 1 fatia pão integral

**⚠️ Lembre-se:** Esses são exemplos gerais. Seu nutricionista pode ter orientações específicas para você!
        """
    
    elif any(word in question_lower for word in ["fome", "ansiedade", "beliscar"]):
        return """
**😫 Controlando a Fome Entre Refeições**

**🔍 Primeiro, Identifique:**
• **Fome real:** Estômago roncando, fraqueza
• **Fome emocional:** Tédio, ansiedade, stress

**🎯 Estratégias Anti-Fome:**
• **Beba água primeiro** - às vezes é sede!
• **Mastigue devagar** nas refeições
• **Inclua proteína e fibra** em cada refeição
• **Durma bem** - sono ruim aumenta a fome

**🥗 Lanches Inteligentes (100-150 kcal):**
• 1 maçã + 6 castanhas
• 1 iogurte natural + 1 colher granola
• 2 torradas integrais + ricota
• Cenoura + 2 colheres de hummus

**🧘‍♀️ Para Fome Emocional:**
• Respire fundo 5 vezes
• Beba um chá calmante
• Faça uma atividade prazerosa
• Procure ajuda profissional se necessário

**📞 Quando persistir:** Converse com seu nutricionista para ajustar seu plano!
        """
    
    elif any(word in question_lower for word in ["doce", "sobremesa", "chocolate", "acucar"]):
        return """
**🍰 Doces na Dieta: É Possível!**

**✅ SIM, você pode comer doces!**

**🗓️ Estratégia do 80/20:**
• **80% do tempo:** Siga seu plano alimentar
• **20% do tempo:** Permita-se flexibilidade

**🎯 Dicas Para Doces Inteligentes:**
• **Planeje:** Inclua no seu dia, não "fure" a dieta
• **Quantidade:** 1-2 quadradinhos de chocolate, não a barra toda
• **Qualidade:** Prefira chocolate 70% cacau ou doces caseiros
• **Timing:** Depois de refeições principais (menor impacto na glicemia)

**🏠 Opções Mais Saudáveis:**
• Brigadeiro de tâmara e cacau
• Sorvete de banana (banana congelada batida)
• Mousse de abacate com cacau
• Pudim de chia com frutas

**🚫 Evite a Mentalidade "Tudo ou Nada":**
Comer um doce não arruína toda sua dieta. O importante é a consistência a longo prazo!

**💡 Dica de ouro:** Se está com muita vontade, coma! Mas saboreie cada pedacinho. Às vezes a vontade passa com menos do que imaginamos.
        """
    
    else:
        # Resposta genérica para pacientes
        return """
**🤖 Assistente Nutricional para Pacientes**

Olá! Estou aqui para ajudar com orientações gerais sobre alimentação saudável.

**💡 Posso ajudar você com:**
• Dúvidas sobre alimentos e refeições
• Dicas de lanches saudáveis
• Orientações sobre hidratação
• Informações sobre nutrição básica
• Esclarecimentos sobre mitos alimentares

**⚠️ IMPORTANTE:**
• Sempre siga as orientações específicas do seu nutricionista
• Este chat oferece informações gerais, não substituindo consulta profissional
• Em caso de dúvidas sobre seu plano, entre em contato com sua clínica

**❓ Experimente perguntar:**
• "Como montar um prato saudável?"
• "Posso comer frutas à noite?"
• "O que comer antes do exercício?"
• "Como controlar a fome entre as refeições?"

Digite sua dúvida específica e eu te ajudo! 😊
        """

def show_users_management():
    """Gestão completa de usuários com CRUD e permissões"""
    st.markdown('<h1 class="main-header">👥 Gestão Completa de Usuários</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Lista de Usuários", "➕ Adicionar Usuário", "📊 Relatório de Acesso"])
    
    with tab1:
        st.subheader("👥 Usuários do Sistema")
        
        conn = sqlite3.connect('nutriapp360.db')
        users_df = pd.read_sql_query("""
            SELECT 
                id, username, full_name, email, phone, role, 
                active, created_at, last_login,
                CASE 
                    WHEN role = 'admin' THEN '🔧'
                    WHEN role = 'nutritionist' THEN '👨‍⚕️'
                    WHEN role = 'secretary' THEN '📋'
                    WHEN role = 'patient' THEN '🧑‍💼'
                END as icon
            FROM users 
            ORDER BY created_at DESC
        """, conn)
        conn.close()
        
        if not users_df.empty:
            # Filtros
            col_filter1, col_filter2 = st.columns(2)
            with col_filter1:
                role_filter = st.selectbox("Filtrar por Papel", 
                                         ["Todos", "admin", "nutritionist", "secretary", "patient"])
            with col_filter2:
                status_filter = st.selectbox("Filtrar por Status", ["Todos", "Ativo", "Inativo"])
            
            # Aplicar filtros
            filtered_df = users_df.copy()
            if role_filter != "Todos":
                filtered_df = filtered_df[filtered_df['role'] == role_filter]
            if status_filter != "Todos":
                active_value = 1 if status_filter == "Ativo" else 0
                filtered_df = filtered_df[filtered_df['active'] == active_value]
            
            # Exibir usuários com ações
            for idx, user in filtered_df.iterrows():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    status_class = "status-active" if user['active'] else "status-inactive"
                    status_text = "Ativo" if user['active'] else "Inativo"
                    
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4>{user['icon']} {user['full_name']}</h4>
                        <p><strong>Usuário:</strong> {user['username']} | 
                           <strong>Papel:</strong> {user['role']} | 
                           <strong>Status:</strong> <span class="{status_class}">{status_text}</span></p>
                        <p><strong>Email:</strong> {user['email'] or 'Não informado'} | 
                           <strong>Telefone:</strong> {user['phone'] or 'Não informado'}</p>
                        <small>Criado: {pd.to_datetime(user['created_at']).strftime('%d/%m/%Y %H:%M')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("✏️ Editar", key=f"edit_{user['id']}"):
                        st.session_state[f"editing_user_{user['id']}"] = True
                
                with col3:
                    action = "Desativar" if user['active'] else "Ativar"
                    if st.button(f"{'🔒' if user['active'] else '🔓'} {action}", key=f"toggle_{user['id']}"):
                        toggle_user_status(user['id'], not user['active'])
                        st.rerun()
                
                # Modal de edição
                if st.session_state.get(f"editing_user_{user['id']}", False):
                    with st.expander(f"Editando usuário: {user['full_name']}", expanded=True):
                        edit_user_form(user)
        else:
            st.info("Nenhum usuário encontrado")
    
    with tab2:
        st.subheader("➕ Adicionar Novo Usuário")
        add_user_form()
    
    with tab3:
        st.subheader("📊 Relatório de Acesso")
        show_access_report()

def add_user_form():
    """Formulário para adicionar novo usuário"""
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("👤 Nome de usuário *")
            full_name = st.text_input("👨‍💼 Nome completo *")
            email = st.text_input("📧 Email")
            phone = st.text_input("📞 Telefone")
        
        with col2:
            role = st.selectbox("🎭 Papel *", ["nutritionist", "secretary", "patient", "admin"])
            password = st.text_input("🔒 Senha *", type="password")
            confirm_password = st.text_input("🔒 Confirmar senha *", type="password")
            
            # Campos específicos para nutricionista
            crn = ""
            specializations = ""
            if role == "nutritionist":
                crn = st.text_input("📋 CRN")
                specializations = st.text_area("🎓 Especializações")
        
        submit = st.form_submit_button("✅ Criar Usuário")
        
        if submit:
            if not all([username, full_name, password, confirm_password]):
                st.error("❌ Preencha todos os campos obrigatórios")
            elif password != confirm_password:
                st.error("❌ As senhas não coincidem")
            elif len(password) < 6:
                st.error("❌ A senha deve ter pelo menos 6 caracteres")
            else:
                try:
                    conn = sqlite3.connect('nutriapp360.db')
                    cursor = conn.cursor()
                    
                    # Verificar se usuário já existe
                    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                    if cursor.fetchone():
                        st.error("❌ Nome de usuário já existe")
                        return
                    
                    # Inserir novo usuário
                    permissions = get_default_permissions(role)
                    cursor.execute('''
                        INSERT INTO users (username, password_hash, role, full_name, email, phone, 
                                         crn, specializations, permissions, created_by)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (username, hash_password(password), role, full_name, email, phone,
                          crn, specializations, json.dumps(permissions), st.session_state.user['id']))
                    
                    conn.commit()
                    conn.close()
                    
                    log_audit_action(st.session_state.user['id'], 'create_user', 'users', cursor.lastrowid)
                    st.success(f"✅ Usuário {username} criado com sucesso!")
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Erro ao criar usuário: {e}")

def get_default_permissions(role):
    """Retorna permissões padrão por papel"""
    permissions = {
        'admin': ['all'],
        'nutritionist': ['patients', 'appointments', 'meal_plans', 'reports', 'recipes'],
        'secretary': ['appointments', 'patients_basic', 'financial'],
        'patient': ['own_data', 'own_progress']
    }
    return permissions.get(role, [])

def toggle_user_status(user_id, new_status):
    """Ativa/desativa usuário"""
    try:
        conn = sqlite3.connect('nutriapp360.db')
        cursor = conn.cursor()
        
        cursor.execute("UPDATE users SET active = ? WHERE id = ?", (new_status, user_id))
        conn.commit()
        conn.close()
        
        log_audit_action(st.session_state.user['id'], 'toggle_user_status', 'users', user_id)
        st.success("✅ Status do usuário alterado com sucesso!")
    
    except Exception as e:
        st.error(f"❌ Erro ao alterar status: {e}")

def edit_user_form(user):
    """Formulário para editar usuário existente"""
    with st.form(f"edit_user_form_{user['id']}"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_full_name = st.text_input("Nome completo", value=user['full_name'])
            new_email = st.text_input("Email", value=user['email'] or "")
            new_phone = st.text_input("Telefone", value=user['phone'] or "")
        
        with col2:
            new_password = st.text_input("Nova senha (deixe vazio para manter)")
            confirm_new_password = st.text_input("Confirmar nova senha")
        
        col_save, col_cancel = st.columns(2)
        with col_save:
            save = st.form_submit_button("💾 Salvar")
        with col_cancel:
            cancel = st.form_submit_button("❌ Cancelar")
        
        if cancel:
            st.session_state[f"editing_user_{user['id']}"] = False
            st.rerun()
        
        if save:
            if new_password and new_password != confirm_new_password:
                st.error("❌ As senhas não coincidem")
            else:
                try:
                    conn = sqlite3.connect('nutriapp360.db')
                    cursor = conn.cursor()
                    
                    if new_password:
                        cursor.execute("""
                            UPDATE users 
                            SET full_name = ?, email = ?, phone = ?, password_hash = ?
                            WHERE id = ?
                        """, (new_full_name, new_email, new_phone, hash_password(new_password), user['id']))
                    else:
                        cursor.execute("""
                            UPDATE users 
                            SET full_name = ?, email = ?, phone = ?
                            WHERE id = ?
                        """, (new_full_name, new_email, new_phone, user['id']))
                    
                    conn.commit()
                    conn.close()
                    
                    log_audit_action(st.session_state.user['id'], 'edit_user', 'users', user['id'])
                    st.session_state[f"editing_user_{user['id']}"] = False
                    st.success("✅ Usuário atualizado com sucesso!")
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Erro ao atualizar usuário: {e}")

def show_access_report():
    """Relatório de acessos dos usuários"""
    conn = sqlite3.connect('nutriapp360.db')
    
    access_data = pd.read_sql_query("""
        SELECT 
            u.full_name,
            u.role,
            u.last_login,
            u.created_at,
            COUNT(al.id) as total_actions
        FROM users u
        LEFT JOIN audit_log al ON al.user_id = u.id
        WHERE u.active = 1
        GROUP BY u.id, u.full_name, u.role, u.last_login, u.created_at
        ORDER BY u.last_login DESC NULLS LAST
    """, conn)
    
    conn.close()
    
    if not access_data.empty:
        # Processar dados para exibição
        access_data['last_login_formatted'] = access_data['last_login'].apply(
            lambda x: pd.to_datetime(x).strftime('%d/%m/%Y %H:%M') if x else 'Nunca logou'
        )
        access_data['created_formatted'] = pd.to_datetime(access_data['created_at']).dt.strftime('%d/%m/%Y')
        
        # Exibir tabela formatada
        display_df = access_data[['full_name', 'role', 'last_login_formatted', 'created_formatted', 'total_actions']].copy()
        display_df.columns = ['Nome', 'Papel', 'Último Login', 'Criado em', 'Total Ações']
        
        st.dataframe(display_df, use_container_width=True)
        
        # Gráfico de atividade por papel
        role_activity = access_data.groupby('role')['total_actions'].sum().reset_index()
        fig = px.bar(role_activity, x='role', y='total_actions', 
                    title="Atividade por Tipo de Usuário")
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("Nenhum dado de acesso encontrado")

def show_meal_plans_management():
    """Gestão completa de planos alimentares"""
    st.markdown('<h1 class="main-header">📋 Planos Alimentares</h1>', unsafe_allow_html=True)
    
    nutritionist_id = st.session_state.user['id']
    
    tab1, tab2, tab3 = st.tabs(["📋 Meus Planos", "➕ Criar Plano", "📊 Análise Nutricional"])
    
    with tab1:
        show_existing_meal_plans(nutritionist_id)
    
    with tab2:
        create_new_meal_plan(nutritionist_id)
    
    with tab3:
        show_nutritional_analysis()

def show_existing_meal_plans(nutritionist_id):
    """Exibe planos alimentares existentes"""
    conn = sqlite3.connect('nutriapp360.db')
    
    plans_df = pd.read_sql_query("""
        SELECT 
            mp.*,
            p.full_name as patient_name,
            p.patient_id
        FROM meal_plans mp
        JOIN patients p ON p.id = mp.patient_id
        WHERE mp.nutritionist_id = ?
        ORDER BY mp.created_at DESC
    """, conn, params=[nutritionist_id])
    
    conn.close()
    
    if not plans_df.empty:
        for idx, plan in plans_df.iterrows():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                status_color = "#4CAF50" if plan['status'] == 'ativo' else "#757575"
                start_date = pd.to_datetime(plan['start_date']).strftime('%d/%m/%Y')
                end_date = "Indefinido"
                if plan['end_date']:
                    end_date = pd.to_datetime(plan['end_date']).strftime('%d/%m/%Y')
                
                st.markdown(f"""
                <div class="dashboard-card" style="border-left-color: {status_color};">
                    <h4>📋 {plan['plan_name']}</h4>
                    <p><strong>Paciente:</strong> {plan['patient_name']} ({plan['patient_id']})</p>
                    <p><strong>Período:</strong> {start_date} até {end_date}</p>
                    <p><strong>Calorias diárias:</strong> {plan['daily_calories']} kcal | 
                       <strong>Status:</strong> <span style="color: {status_color};">{plan['status'].title()}</span></p>
                    <small>Criado em: {pd.to_datetime(plan['created_at']).strftime('%d/%m/%Y %H:%M')}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("👁️ Visualizar", key=f"view_plan_{plan['id']}"):
                    show_meal_plan_details(plan)
            
            with col3:
                if st.button("✏️ Editar", key=f"edit_plan_{plan['id']}"):
                    st.session_state[f"editing_plan_{plan['id']}"] = True
                    st.rerun()
    else:
        st.info("Você ainda não criou nenhum plano alimentar. Use a aba 'Criar Plano' para começar.")

def show_meal_plan_details(plan):
    """Exibe detalhes do plano alimentar"""
    with st.expander(f"Detalhes do Plano: {plan['plan_name']}", expanded=True):
        try:
            plan_data = json.loads(plan['plan_data'])
            
            # Macronutrientes
            st.subheader("🔢 Distribuição de Macronutrientes")
            col_macro1, col_macro2, col_macro3 = st.columns(3)
            
            macros = plan_data.get('macros', {})
            with col_macro1:
                st.metric("Carboidratos", f"{macros.get('carbs', 0)}%")
            with col_macro2:
                st.metric("Proteínas", f"{macros.get('protein', 0)}%")
            with col_macro3:
                st.metric("Gorduras", f"{macros.get('fat', 0)}%")
            
            # Refeições
            st.subheader("🍽️ Distribuição das Refeições")
            meals = plan_data.get('meals', {})
            
            for meal_name, meal_info in meals.items():
                col_meal1, col_meal2, col_meal3 = st.columns([2, 1, 1])
                
                with col_meal1:
                    st.write(f"**{meal_name}**")
                with col_meal2:
                    st.write(f"{meal_info.get('calories', 0)} kcal")
                with col_meal3:
                    st.write(f"{meal_info.get('time', 'N/A')}")
            
            # Observações
            notes = plan_data.get('notes', '')
            if notes:
                st.subheader("📝 Observações")
                st.write(notes)
            
            # Perfil do paciente
            patient_profile = plan_data.get('patient_profile', {})
            if patient_profile:
                st.subheader("👤 Perfil do Paciente")
                col_prof1, col_prof2 = st.columns(2)
                
                with col_prof1:
                    st.write(f"**Peso atual:** {patient_profile.get('current_weight', 'N/A')} kg")
                    st.write(f"**Peso objetivo:** {patient_profile.get('target_weight', 'N/A')} kg")
                
                with col_prof2:
                    st.write(f"**Condições médicas:** {patient_profile.get('medical_conditions', 'Nenhuma')}")
                    st.write(f"**Alergias:** {patient_profile.get('allergies', 'Nenhuma')}")
        
        except json.JSONDecodeError:
            st.error("Erro ao carregar dados do plano")

def create_new_meal_plan(nutritionist_id):
    """Formulário para criar novo plano alimentar"""
    st.subheader("➕ Criar Novo Plano Alimentar")
    
    # Selecionar paciente
    conn = sqlite3.connect('nutriapp360.db')
    patients_df = pd.read_sql_query("""
        SELECT id, full_name, patient_id, current_weight, target_weight, 
               medical_conditions, allergies, activity_level, dietary_preferences
        FROM patients 
        WHERE nutritionist_id = ? AND active = 1
        ORDER BY full_name
    """, conn, params=[nutritionist_id])
    conn.close()
    
    if patients_df.empty:
        st.warning("Você não possui pacientes cadastrados.")
        return
    
    selected_patient_id = st.selectbox(
        "Selecione o paciente *",
        options=patients_df['id'].tolist(),
        format_func=lambda x: f"{patients_df[patients_df['id'] == x]['full_name'].iloc[0]} ({patients_df[patients_df['id'] == x]['patient_id'].iloc[0]})"
    )
    
    if selected_patient_id:
        patient_info = patients_df[patients_df['id'] == selected_patient_id].iloc[0]
        
        # Mostrar info do paciente
        with st.expander("👤 Informações do Paciente", expanded=False):
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.write(f"**Peso atual:** {patient_info['current_weight']} kg")
                st.write(f"**Peso objetivo:** {patient_info['target_weight']} kg")
                st.write(f"**Nível de atividade:** {patient_info['activity_level']}")
            with col_info2:
                st.write(f"**Condições médicas:** {patient_info['medical_conditions'] or 'Nenhuma'}")
                st.write(f"**Alergias:** {patient_info['allergies'] or 'Nenhuma'}")
                st.write(f"**Preferências:** {patient_info['dietary_preferences'] or 'Nenhuma'}")
        
        # Formulário do plano
        with st.form("meal_plan_form"):
            col_plan1, col_plan2 = st.columns(2)
            
            with col_plan1:
                plan_name = st.text_input("Nome do plano *", 
                    value=f"Plano Nutricional - {patient_info['full_name']}")
                daily_calories = st.number_input("Calorias diárias *", 
                    min_value=1000, max_value=5000, value=2000, step=100)
                start_date = st.date_input("Data de início *", value=date.today())
                end_date = st.date_input("Data de fim", value=None)
            
            with col_plan2:
                # Distribuição de macronutrientes
                st.write("**Distribuição de Macronutrientes (%)**")
                carbs_percent = st.slider("Carboidratos", 20, 70, 45)
                protein_percent = st.slider("Proteínas", 10, 40, 25)
                fat_percent = st.slider("Gorduras", 15, 50, 30)
                
                # Verificar se soma 100%
                total_percent = carbs_percent + protein_percent + fat_percent
                if total_percent != 100:
                    st.warning(f"Total atual: {total_percent}%. Ajuste para somar 100%.")
            
            # Distribuição das refeições
            st.write("**Distribuição das Refeições**")
            
            col_meal1, col_meal2, col_meal3 = st.columns(3)
            
            meal_distribution = {}
            
            with col_meal1:
                breakfast_percent = st.number_input("Café da manhã (%)", 15, 35, 25)
                lunch_percent = st.number_input("Almoço (%)", 25, 45, 35)
                
                meal_distribution['Café da manhã'] = {
                    'percent': breakfast_percent,
                    'calories': int(daily_calories * breakfast_percent / 100),
                    'time': '08:00'
                }
                meal_distribution['Almoço'] = {
                    'percent': lunch_percent,
                    'calories': int(daily_calories * lunch_percent / 100),
                    'time': '12:00'
                }
            
            with col_meal2:
                snack1_percent = st.number_input("Lanche manhã (%)", 5, 15, 10)
                dinner_percent = st.number_input("Jantar (%)", 15, 35, 20)
                
                meal_distribution['Lanche manhã'] = {
                    'percent': snack1_percent,
                    'calories': int(daily_calories * snack1_percent / 100),
                    'time': '10:00'
                }
                meal_distribution['Jantar'] = {
                    'percent': dinner_percent,
                    'calories': int(daily_calories * dinner_percent / 100),
                    'time': '19:00'
                }
            
            with col_meal3:
                snack2_percent = st.number_input("Lanche tarde (%)", 5, 15, 10)
                
                meal_distribution['Lanche tarde'] = {
                    'percent': snack2_percent,
                    'calories': int(daily_calories * snack2_percent / 100),
                    'time': '15:00'
                }
            
            # Verificar se soma 100%
            meal_total = sum(meal['percent'] for meal in meal_distribution.values())
            if meal_total != 100:
                st.warning(f"Total das refeições: {meal_total}%. Ajuste para somar 100%.")
            
            # Observações
            notes = st.text_area("Observações e instruções especiais")
            
            submit_plan = st.form_submit_button("✅ Criar Plano Alimentar")
            
            if submit_plan:
                if total_percent != 100:
                    st.error("❌ A soma dos macronutrientes deve ser 100%")
                elif meal_total != 100:
                    st.error("❌ A soma das refeições deve ser 100%")
                elif not plan_name:
                    st.error("❌ Nome do plano é obrigatório")
                else:
                    # Criar estrutura do plano
                    plan_data = {
                        'macros': {
                            'carbs': carbs_percent,
                            'protein': protein_percent,
                            'fat': fat_percent
                        },
                        'meals': meal_distribution,
                        'notes': notes,
                        'patient_profile': {
                            'current_weight': patient_info['current_weight'],
                            'target_weight': patient_info['target_weight'],
                            'medical_conditions': patient_info['medical_conditions'],
                            'allergies': patient_info['allergies'],
                            'activity_level': patient_info['activity_level'],
                            'dietary_preferences': patient_info['dietary_preferences']
                        }
                    }
                    
                    try:
                        conn = sqlite3.connect('nutriapp360.db')
                        cursor = conn.cursor()
                        
                        plan_id = f"PLN{str(int(pd.Timestamp.now().timestamp()))[7:]}"
                        
                        cursor.execute('''
                            INSERT INTO meal_plans (
                                plan_id, patient_id, nutritionist_id, plan_name,
                                start_date, end_date, daily_calories, plan_data, status
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            plan_id, selected_patient_id, nutritionist_id, plan_name,
                            start_date, end_date, daily_calories, json.dumps(plan_data), 'ativo'
                        ))
                        
                        conn.commit()
                        conn.close()
                        
                        log_audit_action(st.session_state.user['id'], 'create_meal_plan', 'meal_plans', cursor.lastrowid)
                        st.success(f"✅ Plano alimentar criado com sucesso! ID: {plan_id}")
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Erro ao criar plano: {e}")

def show_nutritional_analysis():
    """Análise nutricional de alimentos e receitas"""
    st.subheader("📊 Análise Nutricional")
    
    tab_analysis1, tab_analysis2 = st.tabs(["🥗 Alimentos", "🍳 Receitas"])
    
    with tab_analysis1:
        st.write("**Análise Nutricional de Alimentos**")
        
        food_input = st.text_input("Digite o alimento (ex: 100g de arroz integral)")
        
        if food_input:
            # Simulação de análise nutricional (em um sistema real, conectaria com uma API de alimentos)
            food_analysis = analyze_food_nutrition(food_input)
            
            if food_analysis:
                col_nut1, col_nut2, col_nut3, col_nut4 = st.columns(4)
                
                with col_nut1:
                    st.metric("Calorias", f"{food_analysis['calories']} kcal")
                with col_nut2:
                    st.metric("Proteínas", f"{food_analysis['protein']} g")
                with col_nut3:
                    st.metric("Carboidratos", f"{food_analysis['carbs']} g")
                with col_nut4:
                    st.metric("Gorduras", f"{food_analysis['fat']} g")
                
                # Gráfico de distribuição
                nutrients_data = pd.DataFrame({
                    'Nutriente': ['Proteínas', 'Carboidratos', 'Gorduras'],
                    'Gramas': [food_analysis['protein'], food_analysis['carbs'], food_analysis['fat']]
                })
                
                fig = px.pie(nutrients_data, values='Gramas', names='Nutriente',
                           title=f"Composição Nutricional - {food_input}")
                st.plotly_chart(fig, use_container_width=True)
    
    with tab_analysis2:
        st.write("**Calculadora de Receitas**")
        
        with st.form("recipe_calculator"):
            recipe_name = st.text_input("Nome da receita")
            servings = st.number_input("Número de porções", min_value=1, value=2)
            
            st.write("**Ingredientes:**")
            ingredients_text = st.text_area(
                "Liste os ingredientes (um por linha)",
                placeholder="100g peito de frango\n200g arroz integral\n1 colher azeite"
            )
            
            calculate = st.form_submit_button("🧮 Calcular")
            
            if calculate and ingredients_text and recipe_name:
                recipe_nutrition = calculate_recipe_nutrition(ingredients_text, servings)
                
                st.success(f"✅ Análise da receita: {recipe_name}")
                
                col_rec1, col_rec2, col_rec3, col_rec4 = st.columns(4)
                
                with col_rec1:
                    st.metric("Calorias/porção", f"{recipe_nutrition['calories_per_serving']:.0f}")
                with col_rec2:
                    st.metric("Proteínas/porção", f"{recipe_nutrition['protein_per_serving']:.1f}g")
                with col_rec3:
                    st.metric("Carboidratos/porção", f"{recipe_nutrition['carbs_per_serving']:.1f}g")
                with col_rec4:
                    st.metric("Gorduras/porção", f"{recipe_nutrition['fat_per_serving']:.1f}g")

def analyze_food_nutrition(food_input):
    """Simula análise nutricional de alimentos"""
    # Database simples de alimentos (em um sistema real usaria uma API como USDA Food Data Central)
    food_db = {
        'arroz integral': {'calories': 112, 'protein': 2.6, 'carbs': 22.0, 'fat': 0.9},
        'frango': {'calories': 165, 'protein': 31.0, 'carbs': 0.0, 'fat': 3.6},
        'ovo': {'calories': 155, 'protein': 13.0, 'carbs': 1.1, 'fat': 11.0},
        'banana': {'calories': 89, 'protein': 1.1, 'carbs': 23.0, 'fat': 0.3},
        'aveia': {'calories': 389, 'protein': 16.9, 'carbs': 66.3, 'fat': 6.9},
        'azeite': {'calories': 884, 'protein': 0.0, 'carbs': 0.0, 'fat': 100.0}
    }
    
    # Busca simples por palavras-chave
    for food_name, nutrition in food_db.items():
        if food_name in food_input.lower():
            # Tenta extrair quantidade (simplificado)
            quantity = 100  # default
            if 'g' in food_input:
                import re
                match = re.search(r'(\d+)g', food_input)
                if match:
                    quantity = int(match.group(1))
            
            # Ajusta valores pela quantidade
            factor = quantity / 100
            return {
                'calories': int(nutrition['calories'] * factor),
                'protein': round(nutrition['protein'] * factor, 1),
                'carbs': round(nutrition['carbs'] * factor, 1),
                'fat': round(nutrition['fat'] * factor, 1)
            }
    
    # Se não encontrar, retorna valores padrão
    return {
        'calories': 100,
        'protein': 5.0,
        'carbs': 15.0,
        'fat': 3.0
    }

def calculate_recipe_nutrition(ingredients_text, servings):
    """Calcula informação nutricional da receita"""
    lines = ingredients_text.strip().split('\n')
    
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    
    for line in lines:
        if line.strip():
            nutrition = analyze_food_nutrition(line)
            total_calories += nutrition['calories']
            total_protein += nutrition['protein']
            total_carbs += nutrition['carbs']
            total_fat += nutrition['fat']
    
    return {
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fat': total_fat,
        'calories_per_serving': total_calories / servings,
        'protein_per_serving': total_protein / servings,
        'carbs_per_serving': total_carbs / servings,
        'fat_per_serving': total_fat / servings
    }

def show_recipes_management():
    """Gestão de receitas"""
    st.markdown('<h1 class="main-header">🍳 Biblioteca de Receitas</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📚 Minhas Receitas", "➕ Nova Receita", "🔍 Buscar Receitas"])
    
    with tab1:
        show_my_recipes()
    
    with tab2:
        add_new_recipe()
    
    with tab3:
        search_recipes()

def show_my_recipes():
    """Exibe receitas do nutricionista"""
    nutritionist_id = st.session_state.user['id']
    conn = sqlite3.connect('nutriapp360.db')
    
    recipes_df = pd.read_sql_query("""
        SELECT * FROM recipes 
        WHERE nutritionist_id = ? OR is_public = 1
        ORDER BY created_at DESC
    """, conn, params=[nutritionist_id])
    
    conn.close()
    
    if not recipes_df.empty:
        # Filtros
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            category_filter = st.selectbox("Categoria", 
                ["Todas"] + recipes_df['category'].dropna().unique().tolist())
        with col_filter2:
            difficulty_filter = st.selectbox("Dificuldade", 
                ["Todas", "Fácil", "Médio", "Difícil"])
        
        # Aplicar filtros
        filtered_df = recipes_df.copy()
        if category_filter != "Todas":
            filtered_df = filtered_df[filtered_df['category'] == category_filter]
        if difficulty_filter != "Todas":
            filtered_df = filtered_df[filtered_df['difficulty'] == difficulty_filter]
        
        # Exibir receitas
        for idx, recipe in filtered_df.iterrows():
            with st.expander(f"🍳 {recipe['name']} ({recipe['category']})"):
                col_recipe1, col_recipe2 = st.columns([2, 1])
                
                with col_recipe1:
                    st.write(f"**Categoria:** {recipe['category']}")
                    st.write(f"**Tempo de preparo:** {recipe['prep_time']} min | **Cozimento:** {recipe['cook_time']} min")
                    st.write(f"**Porções:** {recipe['servings']} | **Dificuldade:** {recipe['difficulty']}")
                    st.write(f"**Tags:** {recipe['tags']}")
                    
                    st.write("**Ingredientes:**")
                    st.text(recipe['ingredients'])
                    
                    st.write("**Modo de preparo:**")
                    st.text(recipe['instructions'])
                
                with col_recipe2:
                    st.write("**Informação Nutricional (por porção):**")
                    st.metric("Calorias", f"{recipe['calories_per_serving']} kcal")
                    st.metric("Proteínas", f"{recipe['protein']}g")
                    st.metric("Carboidratos", f"{recipe['carbs']}g")
                    st.metric("Gorduras", f"{recipe['fat']}g")
                    st.metric("Fibras", f"{recipe['fiber']}g")
                    
                    if recipe['nutritionist_id'] == nutritionist_id:
                        if st.button("✏️ Editar", key=f"edit_recipe_{recipe['id']}"):
                            st.session_state[f"editing_recipe_{recipe['id']}"] = True
    else:
        st.info("Nenhuma receita encontrada. Comece criando sua primeira receita!")

def add_new_recipe():
    """Formulário para nova receita"""
    st.subheader("➕ Adicionar Nova Receita")
    
    with st.form("new_recipe_form"):
        col_recipe1, col_recipe2 = st.columns(2)
        
        with col_recipe1:
            name = st.text_input("Nome da receita *")
            category = st.selectbox("Categoria", [
                "Café da manhã", "Almoço", "Jantar", "Lanches", "Sobremesas",
                "Saladas", "Sopas", "Pratos principais", "Acompanhamentos", "Bebidas"
            ])
            prep_time = st.number_input("Tempo de preparo (min)", min_value=0, value=15)
            cook_time = st.number_input("Tempo de cozimento (min)", min_value=0, value=0)
            servings = st.number_input("Número de porções", min_value=1, value=2)
            difficulty = st.selectbox("Dificuldade", ["Fácil", "Médio", "Difícil"])
        
        with col_recipe2:
            st.write("**Informação Nutricional (por porção):**")
            calories_per_serving = st.number_input("Calorias", min_value=0, value=300)
            protein = st.number_input("Proteínas (g)", min_value=0.0, value=15.0, step=0.1)
            carbs = st.number_input("Carboidratos (g)", min_value=0.0, value=30.0, step=0.1)
            fat = st.number_input("Gorduras (g)", min_value=0.0, value=10.0, step=0.1)
            fiber = st.number_input("Fibras (g)", min_value=0.0, value=3.0, step=0.1)
        
        ingredients = st.text_area("Ingredientes *", 
            placeholder="Liste os ingredientes, um por linha\nEx:\n• 200g peito de frango\n• 1 xícara arroz integral")
        
        instructions = st.text_area("Modo de preparo *",
            placeholder="Descreva o passo a passo do preparo")
        
        tags = st.text_input("Tags (separadas por vírgula)",
            placeholder="saudável, proteico, sem glúten")
        
        is_public = st.checkbox("Tornar receita pública (visível para outros nutricionistas)", value=True)
        
        submit_recipe = st.form_submit_button("✅ Salvar Receita")
        
        if submit_recipe:
            if not all([name, ingredients, instructions]):
                st.error("❌ Preencha todos os campos obrigatórios")
            else:
                try:
                    conn = sqlite3.connect('nutriapp360.db')
                    cursor = conn.cursor()
                    
                    recipe_id = f"REC{str(int(pd.Timestamp.now().timestamp()))[7:]}"
                    
                    cursor.execute('''
                        INSERT INTO recipes (
                            recipe_id, name, category, prep_time, cook_time, servings,
                            calories_per_serving, protein, carbs, fat, fiber,
                            ingredients, instructions, tags, difficulty,
                            nutritionist_id, is_public
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        recipe_id, name, category, prep_time, cook_time, servings,
                        calories_per_serving, protein, carbs, fat, fiber,
                        ingredients, instructions, tags, difficulty,
                        st.session_state.user['id'], is_public
                    ))
                    
                    conn.commit()
                    conn.close()
                    
                    log_audit_action(st.session_state.user['id'], 'create_recipe', 'recipes', cursor.lastrowid)
                    st.success(f"✅ Receita '{name}' criada com sucesso! ID: {recipe_id}")
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Erro ao criar receita: {e}")

def search_recipes():
    """Busca de receitas públicas"""
    st.subheader("🔍 Buscar Receitas Públicas")
    
    search_term = st.text_input("🔍 Buscar por nome, ingrediente ou tag")
    
    conn = sqlite3.connect('nutriapp360.db')
    
    if search_term:
        recipes_df = pd.read_sql_query("""
            SELECT r.*, u.full_name as author_name
            FROM recipes r
            LEFT JOIN users u ON u.id = r.nutritionist_id
            WHERE r.is_public = 1 
            AND (r.name LIKE ? OR r.ingredients LIKE ? OR r.tags LIKE ?)
            ORDER BY r.created_at DESC
        """, conn, params=[f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'])
    else:
        recipes_df = pd.read_sql_query("""
            SELECT r.*, u.full_name as author_name
            FROM recipes r
            LEFT JOIN users u ON u.id = r.nutritionist_id
            WHERE r.is_public = 1
            ORDER BY r.created_at DESC
            LIMIT 10
        """, conn)
    
    conn.close()
    
    if not recipes_df.empty:
        st.write(f"**{len(recipes_df)} receita(s) encontrada(s)**")
        
        for idx, recipe in recipes_df.iterrows():
            with st.expander(f"🍳 {recipe['name']} - por {recipe['author_name'] or 'Sistema'}"):
                col_search1, col_search2 = st.columns([2, 1])
                
                with col_search1:
                    st.write(recipe['ingredients'][:200] + "..." if len(recipe['ingredients']) > 200 else recipe['ingredients'])
                    
                    if st.button("👁️ Ver receita completa", key=f"view_recipe_{recipe['id']}"):
                        st.session_state[f"viewing_recipe_{recipe['id']}"] = True
                
                with col_search2:
                    st.metric("Calorias", f"{recipe['calories_per_serving']} kcal")
                    st.write(f"⏱️ {recipe['prep_time'] + recipe['cook_time']} min total")
                    st.write(f"👥 {recipe['servings']} porções")
                    st.write(f"📊 {recipe['difficulty']}")
                
                # Modal de visualização completa
                if st.session_state.get(f"viewing_recipe_{recipe['id']}", False):
                    show_full_recipe(recipe)
    else:
        if search_term:
            st.info(f"Nenhuma receita encontrada para '{search_term}'")
        else:
            st.info("Digite um termo para buscar receitas")

def show_secretary_dashboard():
    """Dashboard operacional para secretárias"""
    st.markdown('<h1 class="main-header">📋 Dashboard Operacional</h1>', unsafe_allow_html=True)
    
    # Métricas principais para secretária
    col1, col2, col3, col4 = st.columns(4)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    try:
        # KPIs da secretária
        today_appointments = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM appointments 
            WHERE DATE(appointment_date) = DATE('now') AND status = 'agendado'
        """, conn).iloc[0]['count']
        
        pending_payments = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM patient_financial 
            WHERE payment_status = 'pendente'
        """, conn).iloc[0]['count']
        
        week_appointments = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM appointments 
            WHERE appointment_date BETWEEN DATE('now') AND DATE('now', '+7 days')
            AND status = 'agendado'
        """, conn).iloc[0]['count']
        
        total_patients = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM patients WHERE active = 1
        """, conn).iloc[0]['count']
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #FF9800;">📅 {today_appointments}</h3>
                <p style="margin: 0;">Consultas Hoje</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #F44336;">💰 {pending_payments}</h3>
                <p style="margin: 0;">Pagamentos Pendentes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #2196F3;">📊 {week_appointments}</h3>
                <p style="margin: 0;">Próximos 7 Dias</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #4CAF50;">👥 {total_patients}</h3>
                <p style="margin: 0;">Total Pacientes</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Agenda do dia e tarefas
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.subheader("📅 Agenda de Hoje")
            
            today_schedule = pd.read_sql_query("""
                SELECT 
                    a.appointment_date,
                    a.appointment_type,
                    a.status,
                    p.full_name as patient_name,
                    p.patient_id,
                    p.phone,
                    n.full_name as nutritionist_name
                FROM appointments a
                JOIN patients p ON p.id = a.patient_id
                JOIN users n ON n.id = a.nutritionist_id
                WHERE DATE(a.appointment_date) = DATE('now')
                ORDER BY a.appointment_date
            """, conn)
            
            if not today_schedule.empty:
                for idx, apt in today_schedule.iterrows():
                    status_color = {
                        'agendado': '#2196F3',
                        'realizada': '#4CAF50',
                        'cancelado': '#F44336'
                    }.get(apt['status'], '#757575')
                    
                    time_str = pd.to_datetime(apt['appointment_date']).strftime('%H:%M')
                    
                    st.markdown(f"""
                    <div class="appointment-card" style="border-left-color: {status_color};">
                        <h5 style="margin: 0;">{time_str} - {apt['patient_name']}</h5>
                        <p style="margin: 0; font-size: 0.9rem;">
                            <strong>Nutricionista:</strong> {apt['nutritionist_name']}<br>
                            <strong>Telefone:</strong> {apt['phone']} | 
                            <strong>Status:</strong> <span style="color: {status_color};">{apt['status'].title()}</span>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Botões de ação rápida
                col_action1, col_action2 = st.columns(2)
                with col_action1:
                    if st.button("📞 Ligar para Confirmações"):
                        st.info("Funcionalidade de ligação será implementada com integração telefônica")
                with col_action2:
                    if st.button("📱 Enviar SMS Lembretes"):
                        st.info("Funcionalidade de SMS será implementada com integração")
            else:
                st.info("📝 Nenhuma consulta agendada para hoje")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.subheader("💰 Pagamentos Pendentes")
            
            pending_payments_detail = pd.read_sql_query("""
                SELECT 
                    pf.amount,
                    pf.due_date,
                    pf.service_type,
                    p.full_name as patient_name,
                    p.phone
                FROM patient_financial pf
                JOIN patients p ON p.id = pf.patient_id
                WHERE pf.payment_status = 'pendente'
                ORDER BY pf.due_date
                LIMIT 5
            """, conn)
            
            if not pending_payments_detail.empty:
                total_pending = pending_payments_detail['amount'].sum()
                st.metric("Total em Atraso", f"R$ {total_pending:.2f}")
                
                for idx, payment in pending_payments_detail.iterrows():
                    due_date = pd.to_datetime(payment['due_date']).strftime('%d/%m')
                    days_overdue = (date.today() - pd.to_datetime(payment['due_date']).date()).days
                    
                    color = "#F44336" if days_overdue > 0 else "#FF9800"
                    
                    st.markdown(f"""
                    <div class="financial-card" style="border-left-color: {color};">
                        <p style="margin: 0;"><strong>{payment['patient_name']}</strong></p>
                        <p style="margin: 0; font-size: 0.9rem;">
                            R$ {payment['amount']:.2f} - Vence: {due_date}
                            {f" ({days_overdue} dias atraso)" if days_overdue > 0 else ""}
                        </p>
                        <small>{payment['service_type']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ Nenhum pagamento pendente!")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Gráfico de agendamentos da semana
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("📊 Agendamentos da Semana")
        
        week_data = pd.read_sql_query("""
            SELECT 
                DATE(appointment_date) as data,
                COUNT(*) as total
            FROM appointments 
            WHERE appointment_date BETWEEN DATE('now') AND DATE('now', '+7 days')
            GROUP BY DATE(appointment_date)
            ORDER BY data
        """, conn)
        
        if not week_data.empty:
            # Adicionar nomes dos dias da semana
            week_data['data'] = pd.to_datetime(week_data['data'])
            week_data['dia_semana'] = week_data['data'].dt.strftime('%d/%m (%a)')
            
            fig = px.bar(week_data, x='dia_semana', y='total',
                        title="Consultas nos Próximos 7 Dias")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhum agendamento nos próximos 7 dias")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erro ao carregar dashboard: {e}")
    finally:
        conn.close()

def show_financial_management():
    """Gestão financeira completa"""
    st.markdown('<h1 class="main-header">💰 Sistema Financeiro</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["💳 Movimentações", "➕ Nova Cobrança", "📊 Relatórios", "⚙️ Configurações"])
    
    with tab1:
        show_financial_transactions()
    
    with tab2:
        add_new_charge()
    
    with tab3:
        show_financial_reports()
    
    with tab4:
        show_financial_settings()

def show_financial_transactions():
    """Exibe movimentações financeiras"""
    conn = sqlite3.connect('nutriapp360.db')
    
    # Filtros
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        status_filter = st.selectbox("Status", ["Todos", "pendente", "pago", "vencido"])
    with col_filter2:
        start_date = st.date_input("Data início", value=date.today() - timedelta(days=30))
    with col_filter3:
        end_date = st.date_input("Data fim", value=date.today())
    
    # Query com filtros
    where_conditions = ["pf.created_at BETWEEN ? AND ?"]
    params = [start_date, end_date]
    
    if status_filter != "Todos":
        if status_filter == "vencido":
            where_conditions.append("pf.payment_status = 'pendente' AND pf.due_date < DATE('now')")
        else:
            where_conditions.append("pf.payment_status = ?")
            params.append(status_filter)
    
    where_clause = " AND ".join(where_conditions)
    
    financial_df = pd.read_sql_query(f"""
        SELECT 
            pf.*,
            p.full_name as patient_name,
            p.patient_id,
            p.phone,
            u.full_name as processed_by_name
        FROM patient_financial pf
        JOIN patients p ON p.id = pf.patient_id
        LEFT JOIN users u ON u.id = pf.processed_by
        WHERE {where_clause}
        ORDER BY pf.created_at DESC
    """, conn, params=params)
    
    conn.close()
    
    if not financial_df.empty:
        # Resumo financeiro
        col_summary1, col_summary2, col_summary3, col_summary4 = st.columns(4)
        
        total_amount = financial_df['amount'].sum()
        paid_amount = financial_df[financial_df['payment_status'] == 'pago']['amount'].sum()
        pending_amount = financial_df[financial_df['payment_status'] == 'pendente']['amount'].sum()
        overdue_amount = financial_df[
            (financial_df['payment_status'] == 'pendente') & 
            (pd.to_datetime(financial_df['due_date']).dt.date < date.today())
        ]['amount'].sum()
        
        with col_summary1:
            st.metric("Total Geral", f"R$ {total_amount:.2f}")
        with col_summary2:
            st.metric("Recebido", f"R$ {paid_amount:.2f}")
        with col_summary3:
            st.metric("Pendente", f"R$ {pending_amount:.2f}")
        with col_summary4:
            st.metric("Em Atraso", f"R$ {overdue_amount:.2f}")
        
        # Lista de transações
        for idx, transaction in financial_df.iterrows():
            col_trans1, col_trans2, col_trans3 = st.columns([3, 1, 1])
            
            with col_trans1:
                # Determinar cor baseada no status
                if transaction['payment_status'] == 'pago':
                    status_color = "#4CAF50"
                elif transaction['payment_status'] == 'pendente':
                    if pd.to_datetime(transaction['due_date']).date() < date.today():
                        status_color = "#F44336"  # Vencido
                    else:
                        status_color = "#FF9800"  # Pendente
                else:
                    status_color = "#757575"
                
                due_date_str = pd.to_datetime(transaction['due_date']).strftime('%d/%m/%Y') if transaction['due_date'] else 'N/A'
                paid_date_str = pd.to_datetime(transaction['paid_date']).strftime('%d/%m/%Y') if transaction['paid_date'] else '-'
                
                st.markdown(f"""
                <div class="financial-card" style="border-left-color: {status_color};">
                    <h5 style="margin: 0;">{transaction['patient_name']} ({transaction['patient_id']})</h5>
                    <p style="margin: 0.3rem 0;">
                        <strong>Serviço:</strong> {transaction['service_type']} | 
                        <strong>Valor:</strong> R$ {transaction['amount']:.2f}
                    </p>
                    <p style="margin: 0; font-size: 0.9rem;">
                        <strong>Vencimento:</strong> {due_date_str} | 
                        <strong>Pagamento:</strong> {paid_date_str} | 
                        <strong>Método:</strong> {transaction['payment_method'] or 'N/A'}
                    </p>
                    <p style="margin: 0.3rem 0 0 0; font-size: 0.8rem; color: {status_color};">
                        <strong>Status:</strong> {transaction['payment_status'].title()}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_trans2:
                if transaction['payment_status'] == 'pendente':
                    if st.button("💰 Receber", key=f"pay_{transaction['id']}"):
                        mark_as_paid(transaction['id'])
                        st.rerun()
            
            with col_trans3:
                if st.button("✏️ Editar", key=f"edit_{transaction['id']}"):
                    st.session_state[f"editing_transaction_{transaction['id']}"] = True
                    st.rerun()
            
            # Modal de edição
            if st.session_state.get(f"editing_transaction_{transaction['id']}", False):
                edit_transaction_modal(transaction)
    
    else:
        st.info("Nenhuma movimentação encontrada no período selecionado.")

def mark_as_paid(transaction_id):
    """Marca transação como paga"""
    try:
        conn = sqlite3.connect('nutriapp360.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE patient_financial 
            SET payment_status = 'pago', paid_date = DATE('now'), 
                processed_by = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (st.session_state.user['id'], transaction_id))
        
        conn.commit()
        conn.close()
        
        log_audit_action(st.session_state.user['id'], 'mark_payment', 'patient_financial', transaction_id)
        st.success("✅ Pagamento registrado com sucesso!")
    
    except Exception as e:
        st.error(f"❌ Erro ao registrar pagamento: {e}")

def edit_transaction_modal(transaction):
    """Modal para editar transação"""
    with st.expander(f"Editando: {transaction['patient_name']} - R$ {transaction['amount']:.2f}", expanded=True):
        with st.form(f"edit_transaction_{transaction['id']}"):
            col_edit1, col_edit2 = st.columns(2)
            
            with col_edit1:
                new_amount = st.number_input("Valor", value=float(transaction['amount']), step=0.01)
                new_payment_method = st.selectbox("Método de pagamento", 
                    ["Dinheiro", "PIX", "Cartão", "Transferência", "Boleto"],
                    index=["Dinheiro", "PIX", "Cartão", "Transferência", "Boleto"].index(transaction['payment_method']) if transaction['payment_method'] in ["Dinheiro", "PIX", "Cartão", "Transferência", "Boleto"] else 0
                )
            
            with col_edit2:
                new_due_date = st.date_input("Data vencimento", 
                    value=pd.to_datetime(transaction['due_date']).date() if transaction['due_date'] else date.today())
                new_status = st.selectbox("Status", 
                    ["pendente", "pago"],
                    index=["pendente", "pago"].index(transaction['payment_status'])
                )
            
            new_notes = st.text_area("Observações", value=transaction['notes'] or "")
            
            col_save_trans, col_cancel_trans = st.columns(2)
            with col_save_trans:
                save_transaction = st.form_submit_button("💾 Salvar")
            with col_cancel_trans:
                cancel_transaction = st.form_submit_button("❌ Cancelar")
            
            if cancel_transaction:
                st.session_state[f"editing_transaction_{transaction['id']}"] = False
                st.rerun()
            
            if save_transaction:
                try:
                    conn = sqlite3.connect('nutriapp360.db')
                    cursor = conn.cursor()
                    
                    paid_date = date.today() if new_status == 'pago' else None
                    
                    cursor.execute("""
                        UPDATE patient_financial 
                        SET amount = ?, payment_method = ?, due_date = ?, 
                            payment_status = ?, paid_date = ?, notes = ?,
                            processed_by = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (new_amount, new_payment_method, new_due_date, 
                          new_status, paid_date, new_notes,
                          st.session_state.user['id'], transaction['id']))
                    
                    conn.commit()
                    conn.close()
                    
                    log_audit_action(st.session_state.user['id'], 'edit_transaction', 'patient_financial', transaction['id'])
                    st.session_state[f"editing_transaction_{transaction['id']}"] = False
                    st.success("✅ Transação atualizada com sucesso!")
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Erro ao atualizar transação: {e}")

def add_new_charge():
    """Adiciona nova cobrança"""
    st.subheader("➕ Nova Cobrança")
    
    conn = sqlite3.connect('nutriapp360.db')
    patients_df = pd.read_sql_query("""
        SELECT id, full_name, patient_id FROM patients 
        WHERE active = 1
        ORDER BY full_name
    """, conn)
    conn.close()
    
    if patients_df.empty:
        st.warning("Nenhum paciente ativo encontrado.")
        return
    
    with st.form("new_charge_form"):
        col_charge1, col_charge2 = st.columns(2)
        
        with col_charge1:
            selected_patient = st.selectbox(
                "Paciente *",
                options=patients_df['id'].tolist(),
                format_func=lambda x: f"{patients_df[patients_df['id'] == x]['full_name'].iloc[0]} ({patients_df[patients_df['id'] == x]['patient_id'].iloc[0]})"
            )
            
            service_type = st.selectbox("Tipo de serviço", [
                "Consulta Nutricional", "Consulta Retorno", "Plano Alimentar",
                "Acompanhamento Mensal", "Avaliação Corporal", "Consultoria Online"
            ])
            
            amount = st.number_input("Valor (R$) *", min_value=0.01, value=150.00, step=0.01)
        
        with col_charge2:
            payment_method = st.selectbox("Método de pagamento", [
                "PIX", "Dinheiro", "Cartão", "Transferência", "Boleto"
            ])
            
            due_date = st.date_input("Data de vencimento *", value=date.today())
            
            payment_status = st.selectbox("Status inicial", ["pendente", "pago"])
        
        notes = st.text_area("Observações")
        
        submit_charge = st.form_submit_button("✅ Criar Cobrança")
        
        if submit_charge:
            if not selected_patient or amount <= 0:
                st.error("❌ Preencha todos os campos obrigatórios")
            else:
                try:
                    conn = sqlite3.connect('nutriapp360.db')
                    cursor = conn.cursor()
                    
                    paid_date = date.today() if payment_status == 'pago' else None
                    
                    cursor.execute('''
                        INSERT INTO patient_financial (
                            patient_id, service_type, amount, payment_method,
                            payment_status, due_date, paid_date, processed_by, notes
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        selected_patient, service_type, amount, payment_method,
                        payment_status, due_date, paid_date, 
                        st.session_state.user['id'], notes
                    ))
                    
                    conn.commit()
                    conn.close()
                    
                    log_audit_action(st.session_state.user['id'], 'create_charge', 'patient_financial', cursor.lastrowid)
                    st.success(f"✅ Cobrança criada com sucesso!")
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Erro ao criar cobrança: {e}")

def show_financial_reports():
    """Relatórios financeiros"""
    st.subheader("📊 Relatórios Financeiros")
    
    # Período para relatório
    col_report_date1, col_report_date2 = st.columns(2)
    with col_report_date1:
        report_start = st.date_input("Período início", value=date.today().replace(day=1))
    with col_report_date2:
        report_end = st.date_input("Período fim", value=date.today())
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Dados do período
    financial_data = pd.read_sql_query("""
        SELECT 
            pf.*,
            p.full_name as patient_name,
            n.full_name as nutritionist_name
        FROM patient_financial pf
        JOIN patients p ON p.id = pf.patient_id
        LEFT JOIN users n ON n.id = p.nutritionist_id
        WHERE pf.created_at BETWEEN ? AND ?
    """, conn, params=[report_start, report_end])
    
    if not financial_data.empty:
        # Métricas do período
        col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
        
        total_faturamento = financial_data['amount'].sum()
        total_recebido = financial_data[financial_data['payment_status'] == 'pago']['amount'].sum()
        total_pendente = financial_data[financial_data['payment_status'] == 'pendente']['amount'].sum()
        taxa_recebimento = (total_recebido / total_faturamento * 100) if total_faturamento > 0 else 0
        
        with col_metric1:
            st.metric("Faturamento Total", f"R$ {total_faturamento:.2f}")
        with col_metric2:
            st.metric("Total Recebido", f"R$ {total_recebido:.2f}")
        with col_metric3:
            st.metric("Total Pendente", f"R$ {total_pendente:.2f}")
        with col_metric4:
            st.metric("Taxa Recebimento", f"{taxa_recebimento:.1f}%")
        
        # Gráficos
        col_graph1, col_graph2 = st.columns(2)
        
        with col_graph1:
            # Faturamento por serviço
            service_revenue = financial_data.groupby('service_type')['amount'].sum().reset_index()
            fig_service = px.pie(service_revenue, values='amount', names='service_type',
                               title="Faturamento por Tipo de Serviço")
            st.plotly_chart(fig_service, use_container_width=True)
        
        with col_graph2:
            # Status dos pagamentos
            status_data = financial_data['payment_status'].value_counts().reset_index()
            status_data.columns = ['Status', 'Quantidade']
            fig_status = px.bar(status_data, x='Status', y='Quantidade',
                              title="Status dos Pagamentos")
            st.plotly_chart(fig_status, use_container_width=True)
        
        # Faturamento por nutricionista
        if 'nutritionist_name' in financial_data.columns:
            nutritionist_revenue = financial_data.groupby('nutritionist_name')['amount'].agg(['sum', 'count']).reset_index()
            nutritionist_revenue.columns = ['Nutricionista', 'Faturamento', 'Qtd Serviços']
            
            st.subheader("💰 Faturamento por Nutricionista")
            st.dataframe(nutritionist_revenue, use_container_width=True)
        
        # Evolução mensal
        financial_data['month'] = pd.to_datetime(financial_data['created_at']).dt.strftime('%Y-%m')
        monthly_data = financial_data.groupby('month')['amount'].sum().reset_index()
        
        if len(monthly_data) > 1:
            fig_monthly = px.line(monthly_data, x='month', y='amount',
                                title="Evolução Mensal do Faturamento", markers=True)
            st.plotly_chart(fig_monthly, use_container_width=True)
    
    else:
        st.info("Nenhum dado financeiro encontrado no período selecionado.")
    
    conn.close()

def show_financial_settings():
    """Configurações financeiras"""
    st.subheader("⚙️ Configurações Financeiras")
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        st.write("**💰 Valores Padrão de Serviços**")
        
        default_prices = {
            "Consulta Inicial": 150.00,
            "Consulta Retorno": 100.00,
            "Plano Alimentar": 80.00,
            "Acompanhamento Mensal": 200.00,
            "Avaliação Corporal": 120.00
        }
        
        for service, price in default_prices.items():
            new_price = st.number_input(f"{service}", value=price, step=0.01, key=f"price_{service}")
        
        if st.button("💾 Salvar Preços Padrão"):
            st.success("✅ Preços padrão atualizados!")
    
    with col_config2:
        st.write("**📧 Configurações de Cobrança**")
        
        auto_reminder = st.checkbox("Lembrete automático de vencimento", value=True)
        reminder_days = st.number_input("Dias antes do vencimento", min_value=1, value=3)
        
        st.write("**💳 Métodos de Pagamento Aceitos**")
        pix_enabled = st.checkbox("PIX", value=True)
        card_enabled = st.checkbox("Cartão", value=True)
        cash_enabled = st.checkbox("Dinheiro", value=True)
        transfer_enabled = st.checkbox("Transferência", value=True)
        
        if st.button("💾 Salvar Configurações"):
            st.success("✅ Configurações atualizadas!")

def show_patient_dashboard():
    """Dashboard pessoal do paciente"""
    st.markdown('<h1 class="main-header">🏠 Meu Dashboard</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    # Buscar dados do paciente
    conn = sqlite3.connect('nutriapp360.db')
    
    patient_data = pd.read_sql_query("""
        SELECT p.*, n.full_name as nutritionist_name
        FROM patients p
        LEFT JOIN users n ON n.id = p.nutritionist_id
        WHERE p.user_id = ?
    """, conn, params=[user_id])
    
    if patient_data.empty:
        st.warning("Perfil de paciente não encontrado. Entre em contato com a clínica.")
        conn.close()
        return
    
    patient = patient_data.iloc[0]
    patient_id = patient['id']
    
    try:
        # Métricas do paciente
        col1, col2, col3, col4 = st.columns(4)
        
        # Pontos e nível
        points_data = pd.read_sql_query("""
            SELECT points, level, total_points, streak_days
            FROM patient_points WHERE patient_id = ?
        """, conn, params=[patient_id])
        
        points = points_data.iloc[0]['points'] if not points_data.empty else 0
        level = points_data.iloc[0]['level'] if not points_data.empty else 1
        total_points = points_data.iloc[0]['total_points'] if not points_data.empty else 0
        streak = points_data.iloc[0]['streak_days'] if not points_data.empty else 0
        
        # Próxima consulta
        next_appointment = pd.read_sql_query("""
            SELECT appointment_date, appointment_type
            FROM appointments 
            WHERE patient_id = ? AND status = 'agendado' 
            AND appointment_date > datetime('now')
            ORDER BY appointment_date ASC LIMIT 1
        """, conn, params=[patient_id])
        
        next_apt_str = "Não agendada"
        if not next_appointment.empty:
            next_apt_date = pd.to_datetime(next_appointment.iloc[0]['appointment_date'])
            next_apt_str = next_apt_date.strftime('%d/%m %H:%M')
        
        # Total de consultas
        total_appointments = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM appointments WHERE patient_id = ?
        """, conn, params=[patient_id]).iloc[0]['count']
        
        # Badges conquistadas
        total_badges = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM patient_badges WHERE patient_id = ?
        """, conn, params=[patient_id]).iloc[0]['count']
        
        with col1:
            st.markdown(f"""
            <div class="gamification-card">
                <h3 style="margin: 0; color: #9C27B0;">🎯 {points}</h3>
                <p style="margin: 0;">Pontos Atuais</p>
                <small>Nível {level}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="gamification-card">
                <h3 style="margin: 0; color: #FF9800;">🔥 {streak}</h3>
                <p style="margin: 0;">Dias Seguidos</p>
                <small>Sequência ativa</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #2196F3;">📅</h3>
                <p style="margin: 0;">Próxima Consulta</p>
                <small>{next_apt_str}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="gamification-card">
                <h3 style="margin: 0; color: #4CAF50;">🏆 {total_badges}</h3>
                <p style="margin: 0;">Badges Conquistadas</p>
                <small>{total_appointments} consultas</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Informações principais
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.subheader("👤 Meu Perfil")
            
            # Calcular IMC se tiver dados
            imc = "N/A"
            imc_status = ""
            if patient['height'] and patient['current_weight']:
                imc_value = patient['current_weight'] / (patient['height'] ** 2)
                imc = f"{imc_value:.1f}"
                
                if imc_value < 18.5:
                    imc_status = "Abaixo do peso"
                elif imc_value < 25:
                    imc_status = "Peso normal"
                elif imc_value < 30:
                    imc_status = "Sobrepeso"
                else:
                    imc_status = "Obesidade"
            
            age = calculate_age(patient['birth_date']) if patient['birth_date'] else "N/A"
            
            st.markdown(f"""
            <div class="patient-info-card">
                <p><strong>Nome:</strong> {patient['full_name']}</p>
                <p><strong>ID:</strong> {patient['patient_id']}</p>
                <p><strong>Idade:</strong> {age} anos</p>
                <p><strong>Altura:</strong> {patient['height'] or 'N/A'} m</p>
                <p><strong>Peso atual:</strong> {patient['current_weight'] or 'N/A'} kg</p>
                <p><strong>Peso objetivo:</strong> {patient['target_weight'] or 'N/A'} kg</p>
                <p><strong>IMC:</strong> {imc} {f"({imc_status})" if imc_status else ""}</p>
                <p><strong>Nutricionista:</strong> {patient['nutritionist_name'] or 'Não definido'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.subheader("🏆 Minhas Conquistas Recentes")
            
            # Badges recentes
            recent_badges = pd.read_sql_query("""
                SELECT badge_name, badge_description, badge_icon, earned_date, points_awarded
                FROM patient_badges 
                WHERE patient_id = ?
                ORDER BY earned_date DESC
                LIMIT 3
            """, conn, params=[patient_id])
            
            if not recent_badges.empty:
                for idx, badge in recent_badges.iterrows():
                    earned_date = pd.to_datetime(badge['earned_date']).strftime('%d/%m/%Y')
                    
                    st.markdown(f"""
                    <div class="gamification-card">
                        <h4>{badge['badge_icon']} {badge['badge_name']}</h4>
                        <p style="font-size: 0.9rem;">{badge['badge_description']}</p>
                        <small>Conquistada em {earned_date} | +{badge['points_awarded']} pontos</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Você ainda não possui conquistas. Continue seu acompanhamento para ganhar badges!")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Progresso de peso
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("📈 Meu Progresso")
        
        progress_data = pd.read_sql_query("""
            SELECT record_date, weight, body_fat, muscle_mass, notes
            FROM patient_progress 
            WHERE patient_id = ?
            ORDER BY record_date DESC
            LIMIT 10
        """, conn, params=[patient_id])
        
        if not progress_data.empty:
            progress_data['record_date'] = pd.to_datetime(progress_data['record_date'])
            
            # Gráfico de peso
            fig_weight = px.line(progress_data, x='record_date', y='weight',
                               title='Evolução do Peso', markers=True)
            fig_weight.update_layout(height=300)
            st.plotly_chart(fig_weight, use_container_width=True)
            
            # Estatísticas de progresso
            if len(progress_data) > 1:
                weight_change = progress_data.iloc[0]['weight'] - progress_data.iloc[-1]['weight']
                col_prog1, col_prog2, col_prog3 = st.columns(3)
                
                with col_prog1:
                    st.metric("Mudança de Peso", f"{weight_change:.1f} kg")
                with col_prog2:
                    if patient['target_weight']:
                        remaining = progress_data.iloc[0]['weight'] - patient['target_weight']
                        st.metric("Para o Objetivo", f"{remaining:.1f} kg")
                with col_prog3:
                    weeks = len(progress_data) - 1
                    avg_change = weight_change / weeks if weeks > 0 else 0
                    st.metric("Mudança/Semana", f"{avg_change:.2f} kg")
        else:
            st.info("Seu nutricionista ainda não registrou dados de progresso.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erro ao carregar dashboard: {e}")
    finally:
        conn.close()
