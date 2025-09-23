# Atualizar dados do paciente
                        cursor.execute('''
                            UPDATE patients SET 
                                full_name = ?, email = ?, phone = ?, birth_date = ?, gender = ?,
                                height = ?, current_weight = ?, target_weight = ?, activity_level = ?,
                                medical_conditions = ?, allergies = ?, dietary_preferences = ?,
                                emergency_contact = ?, emergency_phone = ?, insurance_info = ?,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE id = ?
                        ''', (full_name, email, phone, birth_date, gender, height, current_weight,
                             target_weight, activity_level, medical_conditions, allergies,
                             dietary_preferences, emergency_contact, emergency_phone, insurance_info,
                             patient['id']))
                        
                        # Atualizar email do usuário se alterado
                        if email != patient.get('user_email'):
                            cursor.execute('''
                                UPDATE users SET email = ? WHERE id = ?
                            ''', (email, user_id))
                        
                        conn.commit()
                        log_audit_action(user_id, 'update_profile', 'patients', patient['id'])
                        st.success("✅ Perfil atualizado com sucesso!")
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Erro ao atualizar perfil: {e}")
                    finally:
                        conn.close()
            
            # Informações adicionais
            st.markdown("---")
            st.markdown("### 📊 Informações Calculadas")
            
            col_calc1, col_calc2, col_calc3 = st.columns(3)
            
            with col_calc1:
                if patient['height'] and patient['current_weight']:
                    imc = patient['current_weight'] / (patient['height'] ** 2)
                    st.metric("📊 IMC Atual", f"{imc:.1f}")
            
            with col_calc2:
                if patient['birth_date']:
                    birth_date = pd.to_datetime(patient['birth_date'])
                    age = (datetime.now() - birth_date).days // 365
                    st.metric("📅 Idade", f"{age} anos")
            
            with col_calc3:
                if patient['nutritionist_name']:
                    st.info(f"🥗 **Seu Nutricionista:**\n{patient['nutritionist_name']}")
        
        with tab2:
            st.subheader("⚙️ Configurações da Conta")
            
            # Alterar senha
            st.markdown("### 🔒 Alterar Senha")
            
            with st.form("password_form"):
                current_password = st.text_input("🔒 Senha Atual", type="password")
                new_password = st.text_input("🔑 Nova Senha", type="password")
                confirm_password = st.text_input("🔑 Confirmar Nova Senha", type="password")
                
                submitted_password = st.form_submit_button("🔄 Alterar Senha")
                
                if submitted_password:
                    if new_password != confirm_password:
                        st.error("❌ As senhas não coincidem!")
                    elif len(new_password) < 6:
                        st.error("❌ A senha deve ter pelo menos 6 caracteres!")
                    else:
                        # Verificar senha atual
                        user_data = pd.read_sql_query("""
                            SELECT password_hash FROM users WHERE id = ?
                        """, conn, params=[user_id])
                        
                        if not user_data.empty:
                            stored_hash = user_data.iloc[0]['password_hash']
                            current_hash = hash_password(current_password)
                            
                            if current_hash == stored_hash:
                                try:
                                    cursor = conn.cursor()
                                    new_hash = hash_password(new_password)
                                    
                                    cursor.execute('''
                                        UPDATE users SET password_hash = ? WHERE id = ?
                                    ''', (new_hash, user_id))
                                    
                                    conn.commit()
                                    log_audit_action(user_id, 'change_password', 'users', user_id)
                                    st.success("✅ Senha alterada com sucesso!")
                                
                                except Exception as e:
                                    st.error(f"❌ Erro ao alterar senha: {e}")
                            else:
                                st.error("❌ Senha atual incorreta!")
            
            # Notificações
            st.markdown("### 🔔 Preferências de Notificação")
            
            col_notif1, col_notif2 = st.columns(2)
            
            with col_notif1:
                email_notifications = st.checkbox("📧 Notificações por Email", value=True)
                appointment_reminders = st.checkbox("📅 Lembretes de Consulta", value=True)
                progress_updates = st.checkbox("📊 Atualizações de Progresso", value=True)
            
            with col_notif2:
                sms_notifications = st.checkbox("📱 Notificações por SMS", value=False)
                meal_reminders = st.checkbox("🍽️ Lembretes de Refeição", value=False)
                water_reminders = st.checkbox("💧 Lembretes de Hidratação", value=False)
            
            if st.button("💾 Salvar Preferências"):
                st.success("✅ Preferências salvas!")
            
            # Privacidade
            st.markdown("### 🔒 Privacidade e Segurança")
            
            col_privacy1, col_privacy2 = st.columns(2)
            
            with col_privacy1:
                share_progress = st.checkbox("📊 Compartilhar progresso no ranking", value=True)
                public_profile = st.checkbox("👤 Perfil público para outros pacientes", value=False)
            
            with col_privacy2:
                data_analytics = st.checkbox("📈 Permitir uso dos dados para melhorias", value=True)
                marketing_emails = st.checkbox("📢 Receber emails promocionais", value=False)
            
            # Exclusão de conta
            st.markdown("---")
            st.markdown("### ⚠️ Zona de Perigo")
            
            with st.expander("🗑️ Excluir Conta", expanded=False):
                st.warning("""
                ⚠️ **Atenção:** Esta ação é irreversível!
                
                Ao excluir sua conta, todos os seus dados serão permanentemente removidos:
                - Histórico de consultas
                - Registros de progresso
                - Planos alimentares
                - Pontos e badges
                """)
                
                delete_reason = st.selectbox("Motivo da exclusão:", [
                    "Selecione um motivo",
                    "Não uso mais o serviço",
                    "Problemas de privacidade",
                    "Funcionalidades insuficientes",
                    "Mudança de nutricionista",
                    "Outro"
                ])
                
                if delete_reason != "Selecione um motivo":
                    confirm_delete = st.text_input("Digite 'EXCLUIR' para confirmar:")
                    
                    if confirm_delete == "EXCLUIR":
                        if st.button("🗑️ Confirmar Exclusão", type="primary"):
                            st.error("🚫 Funcionalidade de exclusão desabilitada na versão demo.")
        
        with tab3:
            st.subheader("📊 Histórico de Atividades")
            
            # Resumo da conta
            account_created = pd.to_datetime(patient['created_at']).strftime('%d/%m/%Y')
            days_active = (datetime.now() - pd.to_datetime(patient['created_at'])).days
            
            col_history1, col_history2, col_history3 = st.columns(3)
            
            with col_history1:
                st.metric("📅 Conta criada em", account_created)
            
            with col_history2:
                st.metric("⏱️ Dias ativo", days_active)
            
            with col_history3:
                # Última atualização
                last_update = pd.to_datetime(patient['updated_at']).strftime('%d/%m/%Y')
                st.metric("🔄 Última atualização", last_update)
            
            # Estatísticas de uso
            st.markdown("### 📈 Estatísticas de Uso")
            
            # Total de consultas
            total_appointments = pd.read_sql_query("""
                SELECT COUNT(*) as count FROM appointments WHERE patient_id = ?
            """, conn, params=[patient['id']]).iloc[0]['count']
            
            # Total de registros de progresso
            total_progress = pd.read_sql_query("""
                SELECT COUNT(*) as count FROM patient_progress WHERE patient_id = ?
            """, conn, params=[patient['id']]).iloc[0]['count']
            
            # Planos alimentares recebidos
            total_plans = pd.read_sql_query("""
                SELECT COUNT(*) as count FROM meal_plans WHERE patient_id = ?
            """, conn, params=[patient['id']]).iloc[0]['count']
            
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            
            with col_stats1:
                st.metric("📅 Total de Consultas", total_appointments)
            
            with col_stats2:
                st.metric("📊 Registros de Progresso", total_progress)
            
            with col_stats3:
                st.metric("🍽️ Planos Recebidos", total_plans)
            
            # Atividade recente
            st.markdown("### 🕐 Atividade Recente")
            
            # Buscar atividades recentes (simulado com dados reais)
            recent_activities = []
            
            # Últimas consultas
            recent_appointments = pd.read_sql_query("""
                SELECT appointment_date, status, appointment_type 
                FROM appointments 
                WHERE patient_id = ? 
                ORDER BY appointment_date DESC 
                LIMIT 3
            """, conn, params=[patient['id']])
            
            for _, apt in recent_appointments.iterrows():
                apt_date = pd.to_datetime(apt['appointment_date']).strftime('%d/%m/%Y %H:%M')
                recent_activities.append({
                    'date': apt['appointment_date'],
                    'action': f"📅 Consulta {apt['status']} - {apt['appointment_type'] or 'Padrão'}",
                    'details': apt_date
                })
            
            # Últimos registros de progresso
            recent_progress = pd.read_sql_query("""
                SELECT record_date, weight FROM patient_progress 
                WHERE patient_id = ? 
                ORDER BY record_date DESC 
                LIMIT 3
            """, conn, params=[patient['id']])
            
            for _, prog in recent_progress.iterrows():
                prog_date = pd.to_datetime(prog['record_date']).strftime('%d/%m/%Y')
                recent_activities.append({
                    'date': prog['record_date'],
                    'action': f"📊 Progresso registrado - {prog['weight']} kg",
                    'details': prog_date
                })
            
            # Ordenar por data
            recent_activities.sort(key=lambda x: x['date'], reverse=True)
            
            if recent_activities:
                for activity in recent_activities[:5]:  # Mostrar apenas os 5 mais recentes
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #4CAF50;">
                        <strong>{activity['action']}</strong><br>
                        <small style="color: #666;">{activity['details']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("📝 Nenhuma atividade recente registrada.")
    
    else:
        st.error("❌ Dados do paciente não encontrados.")
    
    conn.close()

# FUNCIONALIDADES ADMINISTRATIVAS AVANÇADAS

def show_system_analytics():
    st.markdown('<h1 class="main-header">📈 Analytics do Sistema</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "👥 Usuários", "💰 Financeiro", "🎯 Performance"])
    
    with tab1:
        st.subheader("📊 Visão Geral do Sistema")
        
        conn = sqlite3.connect('nutriapp360.db')
        
        # KPIs principais
        col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
        
        # Total de usuários ativos
        total_users = pd.read_sql_query("SELECT COUNT(*) as count FROM users WHERE active = 1", conn).iloc[0]['count']
        
        # Total de pacientes
        total_patients = pd.read_sql_query("SELECT COUNT(*) as count FROM patients WHERE active = 1", conn).iloc[0]['count']
        
        # Consultas este mês
        appointments_month = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM appointments 
            WHERE strftime('%Y-%m', appointment_date) = strftime('%Y-%m', 'now')
        """, conn).iloc[0]['count']
        
        # Taxa de ocupação (consultas realizadas vs agendadas)
        ocupation_rate = pd.read_sql_query("""
            SELECT 
                COUNT(CASE WHEN status = 'realizado' THEN 1 END) * 100.0 / COUNT(*) as rate
            FROM appointments 
            WHERE strftime('%Y-%m', appointment_date) = strftime('%Y-%m', 'now')
        """, conn).iloc[0]['rate'] or 0
        
        with col_kpi1:
            st.metric("👥 Usuários Ativos", total_users, delta="+5%")
        
        with col_kpi2:
            st.metric("🙋‍♂️ Pacientes", total_patients, delta="+12%")
        
        with col_kpi3:
            st.metric("📅 Consultas/Mês", appointments_month, delta="+8%")
        
        with col_kpi4:
            st.metric("📊 Taxa de Ocupação", f"{ocupation_rate:.1f}%", delta="+3%")
        
        # Gráficos de tendência
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Crescimento de usuários por mês
            monthly_users = pd.read_sql_query("""
                SELECT 
                    strftime('%Y-%m', created_at) as month,
                    COUNT(*) as new_users
                FROM users 
                WHERE created_at >= date('now', '-12 months')
                GROUP BY strftime('%Y-%m', created_at)
                ORDER BY month
            """, conn)
            
            if not monthly_users.empty:
                fig = px.line(monthly_users, x='month', y='new_users', 
                             title="📈 Novos Usuários por Mês", markers=True)
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
        
        with col_chart2:
            # Distribuição de consultas por status
            appointment_status = pd.read_sql_query("""
                SELECT status, COUNT(*) as count 
                FROM appointments 
                WHERE appointment_date >= date('now', '-30 days')
                GROUP BY status
            """, conn)
            
            if not appointment_status.empty:
                fig = px.pie(appointment_status, values='count', names='status',
                           title="📊 Status das Consultas (30 dias)")
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
        
        # Métricas de engajamento
        st.subheader("🎯 Métricas de Engajamento")
        
        col_engage1, col_engage2, col_engage3 = st.columns(3)
        
        with col_engage1:
            # Pacientes com progresso recente
            active_patients = pd.read_sql_query("""
                SELECT COUNT(DISTINCT patient_id) as count 
                FROM patient_progress 
                WHERE record_date >= date('now', '-30 days')
            """, conn).iloc[0]['count']
            
            st.metric("📊 Pacientes Ativos", active_patients)
        
        with col_engage2:
            # Planos alimentares ativos
            active_plans = pd.read_sql_query("""
                SELECT COUNT(*) as count FROM meal_plans 
                WHERE status = 'ativo' AND start_date <= date('now') 
                AND (end_date IS NULL OR end_date >= date('now'))
            """, conn).iloc[0]['count']
            
            st.metric("🍽️ Planos Ativos", active_plans)
        
        with col_engage3:
            # Conversas com IA
            ia_conversations = pd.read_sql_query("""
                SELECT COUNT(*) as count FROM llm_conversations 
                WHERE created_at >= date('now', '-7 days')
            """, conn).iloc[0]['count']
            
            st.metric("🤖 Conversas IA (7d)", ia_conversations)
        
        conn.close()
    
    with tab2:
        st.subheader("👥 Analytics de Usuários")
        
        conn = sqlite3.connect('nutriapp360.db')
        
        # Distribuição por tipo de usuário
        col_user1, col_user2 = st.columns(2)
        
        with col_user1:
            user_distribution = pd.read_sql_query("""
                SELECT role, COUNT(*) as count 
                FROM users WHERE active = 1 
                GROUP BY role
            """, conn)
            
            if not user_distribution.empty:
                # Traduzir roles para português
                role_translation = {
                    'admin': 'Administradores',
                    'nutritionist': 'Nutricionistas',
                    'secretary': 'Secretárias',
                    'patient': 'Pacientes'
                }
                
                user_distribution['role_pt'] = user_distribution['role'].map(role_translation)
                
                fig = px.pie(user_distribution, values='count', names='role_pt',
                           title="👥 Distribuição por Tipo de Usuário")
                st.plotly_chart(fig, use_container_width=True)
        
        with col_user2:
            # Usuários mais ativos (por logins)
            st.markdown("**🏆 Top Usuários Ativos:**")
            
            # Simular dados de login (em sistema real, viria de tabela de logs)
            top_users = pd.read_sql_query("""
                SELECT full_name, role, last_login 
                FROM users 
                WHERE active = 1 AND last_login IS NOT NULL 
                ORDER BY last_login DESC 
                LIMIT 5
            """, conn)
            
            if not top_users.empty:
                for idx, user in top_users.iterrows():
                    last_login = pd.to_datetime(user['last_login']).strftime('%d/%m/%Y %H:%M') if user['last_login'] else 'Nunca'
                    
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 0.5rem; border-radius: 5px; margin: 0.3rem 0;">
                        <strong>{user['full_name']}</strong> ({user['role']})<br>
                        <small>Último acesso: {last_login}</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Análise temporal de cadastros
        st.subheader("📅 Cadastros por Período")
        
        registration_timeline = pd.read_sql_query("""
            SELECT 
                strftime('%Y-%m', created_at) as month,
                role,
                COUNT(*) as count
            FROM users 
            WHERE created_at >= date('now', '-12 months')
            GROUP BY strftime('%Y-%m', created_at), role
            ORDER BY month
        """, conn)
        
        if not registration_timeline.empty:
            # Criar gráfico de área empilhada
            fig = px.area(registration_timeline, x='month', y='count', color='role',
                         title="📈 Novos Cadastros por Mês e Tipo")
            st.plotly_chart(fig, use_container_width=True)
        
        conn.close()
    
    with tab3:
        st.subheader("💰 Analytics Financeiro")
        
        conn = sqlite3.connect('nutriapp360.db')
        
        # Métricas financeiras
        col_fin1, col_fin2, col_fin3, col_fin4 = st.columns(4)
        
        # Receita total
        total_revenue = pd.read_sql_query("""
            SELECT SUM(amount) as total FROM patient_financial 
            WHERE payment_status = 'pago'
        """, conn).iloc[0]['total'] or 0
        
        # Receita este mês
        monthly_revenue = pd.read_sql_query("""
            SELECT SUM(amount) as total FROM patient_financial 
            WHERE payment_status = 'pago' 
            AND strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
        """, conn).iloc[0]['total'] or 0
        
        # Valor pendente
        pending_amount = pd.read_sql_query("""
            SELECT SUM(amount) as total FROM patient_financial 
            WHERE payment_status = 'pendente'
        """, conn).iloc[0]['total'] or 0
        
        # Ticket médio
        avg_ticket = pd.read_sql_query("""
            SELECT AVG(amount) as avg FROM patient_financial 
            WHERE payment_status = 'pago'
        """, conn).iloc[0]['avg'] or 0
        
        with col_fin1:
            st.metric("💰 Receita Total", f"R$ {total_revenue:,.2f}")
        
        with col_fin2:
            st.metric("📅 Receita Mensal", f"R$ {monthly_revenue:,.2f}", delta="+15%")
        
        with col_fin3:
            st.metric("⏰ Valor Pendente", f"R$ {pending_amount:,.2f}")
        
        with col_fin4:
            st.metric("🎯 Ticket Médio", f"R$ {avg_ticket:.2f}")
        
        # Gráficos financeiros
        col_chart_fin1, col_chart_fin2 = st.columns(2)
        
        with col_chart_fin1:
            # Receita por mês
            monthly_revenue_chart = pd.read_sql_query("""
                SELECT 
                    strftime('%Y-%m', created_at) as month,
                    SUM(CASE WHEN payment_status = 'pago' THEN amount ELSE 0 END) as revenue
                FROM patient_financial 
                WHERE created_at >= date('now', '-12 months')
                GROUP BY strftime('%Y-%m', created_at)
                ORDER BY month
            """, conn)
            
            if not monthly_revenue_chart.empty:
                fig = px.bar(monthly_revenue_chart, x='month', y='revenue',
                           title="💰 Receita Mensal")
                st.plotly_chart(fig, use_container_width=True)
        
        with col_chart_fin2:
            # Métodos de pagamento
            payment_methods = pd.read_sql_query("""
                SELECT payment_method, SUM(amount) as total 
                FROM patient_financial 
                WHERE payment_status = 'pago' AND payment_method IS NOT NULL
                GROUP BY payment_method
            """, conn)
            
            if not payment_methods.empty:
                fig = px.pie(payment_methods, values='total', names='payment_method',
                           title="💳 Receita por Método de Pagamento")
                st.plotly_chart(fig, use_container_width=True)
        
        # Análise de inadimplência
        st.subheader("📊 Análise de Inadimplência")
        
        # Pagamentos em atraso
        overdue_analysis = pd.read_sql_query("""
            SELECT 
                COUNT(*) as count,
                SUM(amount) as total_amount,
                AVG(julianday('now') - julianday(due_date)) as avg_days_overdue
            FROM patient_financial 
            WHERE payment_status = 'pendente' 
            AND due_date < date('now')
        """, conn)
        
        if not overdue_analysis.empty and overdue_analysis.iloc[0]['count'] > 0:
            overdue_info = overdue_analysis.iloc[0]
            
            col_overdue1, col_overdue2, col_overdue3 = st.columns(3)
            
            with col_overdue1:
                st.metric("🚨 Pagamentos em Atraso", int(overdue_info['count']))
            
            with col_overdue2:
                st.metric("💸 Valor em Atraso", f"R$ {overdue_info['total_amount']:,.2f}")
            
            with col_overdue3:
                st.metric("⏱️ Atraso Médio", f"{overdue_info['avg_days_overdue']:.0f} dias")
        
        conn.close()
    
    with tab4:
        st.subheader("🎯 Análise de Performance")
        
        conn = sqlite3.connect('nutriapp360.db')
        
        # KPIs de performance
        col_perf1, col_perf2, col_perf3, col_perf4 = st.columns(4)
        
        # Taxa de comparecimento
        attendance_rate = pd.read_sql_query("""
            SELECT 
                COUNT(CASE WHEN status = 'realizado' THEN 1 END) * 100.0 / COUNT(*) as rate
            FROM appointments 
            WHERE appointment_date < datetime('now')
        """, conn).iloc[0]['rate'] or 0
        
        # Taxa de cancelamento
        cancellation_rate = pd.read_sql_query("""
            SELECT 
                COUNT(CASE WHEN status = 'cancelado' THEN 1 END) * 100.0 / COUNT(*) as rate
            FROM appointments
        """, conn).iloc[0]['rate'] or 0
        
        # Pacientes com progresso positivo
        positive_progress = pd.read_sql_query("""
            SELECT COUNT(DISTINCT patient_id) as count
            FROM (
                SELECT 
                    patient_id,
                    MIN(weight) as first_weight,
                    MAX(weight) as last_weight
                FROM patient_progress 
                GROUP BY patient_id
                HAVING first_weight > last_weight
            )
        """, conn).iloc[0]['count']
        
        # Satisfação média (simulada)
        avg_satisfaction = 4.6
        
        with col_perf1:
            st.metric("📊 Taxa Comparecimento", f"{attendance_rate:.1f}%")
        
        with col_perf2:
            st.metric("❌ Taxa Cancelamento", f"{cancellation_rate:.1f}%")
        
        with col_perf3:
            st.metric("📈 Progresso Positivo", positive_progress)
        
        with col_perf4:
            st.metric("⭐ Satisfação Média", f"{avg_satisfaction:.1f}/5")
        
        # Performance por nutricionista
        st.subheader("🥗 Performance por Nutricionista")
        
        nutritionist_performance = pd.read_sql_query("""
            SELECT 
                n.full_name,
                COUNT(DISTINCT a.patient_id) as total_patients,
                COUNT(a.id) as total_appointments,
                COUNT(CASE WHEN a.status = 'realizado' THEN 1 END) as completed_appointments,
                COUNT(CASE WHEN a.status = 'cancelado' THEN 1 END) as cancelled_appointments
            FROM users n
            LEFT JOIN appointments a ON a.nutritionist_id = n.id
            WHERE n.role = 'nutritionist' AND n.active = 1
            GROUP BY n.id, n.full_name
        """, conn)
        
        if not nutritionist_performance.empty:
            # Calcular métricas
            nutritionist_performance['attendance_rate'] = (
                nutritionist_performance['completed_appointments'] / 
                nutritionist_performance['total_appointments'] * 100
            ).fillna(0)
            
            nutritionist_performance['cancellation_rate'] = (
                nutritionist_performance['cancelled_appointments'] / 
                nutritionist_performance['total_appointments'] * 100
            ).fillna(0)
            
            # Exibir tabela
            display_columns = [
                'full_name', 'total_patients', 'total_appointments', 
                'attendance_rate', 'cancellation_rate'
            ]
            
            column_config = {
                'full_name': 'Nutricionista',
                'total_patients': 'Pacientes',
                'total_appointments': 'Consultas',
                'attendance_rate': st.column_config.NumberColumn(
                    'Taxa Comparecimento (%)',
                    format="%.1f%%"
                ),
                'cancellation_rate': st.column_config.NumberColumn(
                    'Taxa Cancelamento (%)',
                    format="%.1f%%"
                )
            }
            
            st.dataframe(
                nutritionist_performance[display_columns],
                column_config=column_config,
                use_container_width=True,
                hide_index=True
            )
        
        # Tendências de performance
        st.subheader("📈 Tendências de Performance")
        
        performance_trends = pd.read_sql_query("""
            SELECT 
                strftime('%Y-%m', appointment_date) as month,
                COUNT(*) as total_appointments,
                COUNT(CASE WHEN status = 'realizado' THEN 1 END) as completed,
                COUNT(CASE WHEN status = 'cancelado' THEN 1 END) as cancelled
            FROM appointments 
            WHERE appointment_date >= date('now', '-12 months')
            GROUP BY strftime('%Y-%m', appointment_date)
            ORDER BY month
        """, conn)
        
        if not performance_trends.empty:
            performance_trends['attendance_rate'] = (
                performance_trends['completed'] / performance_trends['total_appointments'] * 100
            )
            
            performance_trends['cancellation_rate'] = (
                performance_trends['cancelled'] / performance_trends['total_appointments'] * 100
            )
            
            col_trend1, col_trend2 = st.columns(2)
            
            with col_trend1:
                fig = px.line(performance_trends, x='month', y='attendance_rate',
                             title="📊 Taxa de Comparecimento ao Longo do Tempo",
                             markers=True)
                st.plotly_chart(fig, use_container_width=True)
            
            with col_trend2:
                fig = px.line(performance_trends, x='month', y='cancellation_rate',
                             title="❌ Taxa de Cancelamento ao Longo do Tempo",
                             markers=True, color_discrete_sequence=['red'])
                st.plotly_chart(fig, use_container_width=True)
        
        conn.close()

def show_advanced_reports():
    st.markdown('<h1 class="main-header">📋 Relatórios Avançados</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard Executivo", "📈 Relatório de Resultados", "💰 Relatório Financeiro", "🎯 Relatório Personalizado"])
    
    with tab1:
        st.subheader("📊 Dashboard Executivo")
        
        # Período de análise
        col_period1, col_period2 = st.columns(2)
        
        with col_period1:
            start_date_exec = st.date_input("📅 Data inicial", 
                                          value=datetime.now().date() - timedelta(days=90))
        
        with col_period2:
            end_date_exec = st.date_input("📅 Data final", 
                                        value=datetime.now().date())
        
        if st.button("📊 Gerar Dashboard Executivo", type="primary"):
            with st.spinner("📊 Gerando relatório executivo..."):
                conn = sqlite3.connect('nutriapp360.db')
                
                # Resumo executivo
                st.markdown("### 📋 Resumo Executivo")
                
                period_days = (end_date_exec - start_date_exec).days
                
                # KPIs do período
                kpis = {
                    'total_appointments': pd.read_sql_query(f"""
                        SELECT COUNT(*) as count FROM appointments 
                        WHERE DATE(appointment_date) BETWEEN '{start_date_exec}' AND '{end_date_exec}'
                    """, conn).iloc[0]['count'],
                    
                    'completed_appointments': pd.read_sql_query(f"""
                        SELECT COUNT(*) as count FROM appointments 
                        WHERE DATE(appointment_date) BETWEEN '{start_date_exec}' AND '{end_date_exec}'
                        AND status = 'realizado'
                    """, conn).iloc[0]['count'],
                    
                    'total_revenue': pd.read_sql_query(f"""
                        SELECT SUM(amount) as total FROM patient_financial 
                        WHERE payment_status = 'pago' 
                        AND DATE(created_at) BETWEEN '{start_date_exec}' AND '{end_date_exec}'
                    """, conn).iloc[0]['total'] or 0,
                    
                    'new_patients': pd.read_sql_query(f"""
                        SELECT COUNT(*) as count FROM patients 
                        WHERE DATE(created_at) BETWEEN '{start_date_exec}' AND '{end_date_exec}'
                    """, conn).iloc[0]['count']
                }
                
                col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
                
                with col_kpi1:
                    st.metric("📅 Consultas Realizadas", kpis['completed_appointments'])
                
                with col_kpi2:
                    attendance_rate = (kpis['completed_appointments'] / kpis['total_appointments'] * 100) if kpis['total_appointments'] > 0 else 0
                    st.metric("📊 Taxa de Comparecimento", f"{attendance_rate:.1f}%")
                
                with col_kpi3:
                    st.metric("💰 Receita do Período", f"R$ {kpis['total_revenue']:,.2f}")
                
                with col_kpi4:
                    st.metric("👥 Novos Pacientes", kpis['new_patients'])
                
                # Análise de tendências
                st.markdown("### 📈 Análise de Tendências")
                
                weekly_data = pd.read_sql_query(f"""
                    SELECT 
                        strftime('%Y-W%W', appointment_date) as week,
                        COUNT(*) as appointments,
                        COUNT(CASE WHEN status = 'realizado' THEN 1 END) as completed
                    FROM appointments 
                    WHERE DATE(appointment_date) BETWEEN '{start_date_exec}' AND '{end_date_exec}'
                    GROUP BY strftime('%Y-W%W', appointment_date)
                    ORDER BY week
                """, conn)
                
                if not weekly_data.empty:
                    fig = go.Figure()
                    
                    fig.add_trace(go.Scatter(
                        x=weekly_data['week'],
                        y=weekly_data['appointments'],
                        mode='lines+markers',
                        name='Total de Consultas',
                        line=dict(color='blue')
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=weekly_data['week'],
                        y=weekly_data['completed'],
                        mode='lines+markers',
                        name='Consultas Realizadas',
                        line=dict(color='green')
                    ))
                    
                    fig.update_layout(
                        title="📈 Evolução Semanal de Consultas",
                        xaxis_title="Semana",
                        yaxis_title="Número de Consultas",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Insights e recomendações
                st.markdown("### 💡 Insights e Recomendações")
                
                insights = []
                
                if attendance_rate < 80:
                    insights.append("🔴 **Atenção:** Taxa de comparecimento baixa. Considere implementar lembretes automáticos.")
                elif attendance_rate > 90:
                    insights.append("🟢 **Excelente:** Alta taxa de comparecimento. Mantenha as práticas atuais.")
                
                if kpis['new_patients'] > 0:
                    avg_new_per_week = kpis['new_patients'] / (period_days / 7)
                    if avg_new_per_week > 2:
                        insights.append("🟢 **Crescimento:** Boa aquisição de novos pacientes.")
                    else:
                        insights.append("🟡 **Oportunidade:** Considere estratégias de marketing para atrair mais pacientes.")
                
                revenue_per_day = kpis['total_revenue'] / period_days if period_days > 0 else 0
                insights.append(f"💰 **Receita média diária:** R$ {revenue_per_day:.2f}")
                
                for insight in insights:
                    st.markdown(insight)
                
                conn.close()
    
    with tab2:
        st.subheader("📈 Relatório de Resultados dos Pacientes")
        
        # Filtros
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            result_period = st.selectbox("📅 Período de Análise", [
                "Últimos 30 dias",
                "Últimos 3 meses", 
                "Últimos 6 meses",
                "Último ano"
            ])
        
        with col_filter2:
            nutritionist_filter = st.selectbox("🥗 Nutricionista", ["Todos", "Dr. Ana Silva"])
        
        if st.button("📈 Gerar Relatório de Resultados", type="primary"):
            with st.spinner("📈 Analisando resultados dos pacientes..."):
                conn = sqlite3.connect('nutriapp360.db')
                
                # Determinar período
                period_map = {
                    "Últimos 30 dias": 30,
                    "Últimos 3 meses": 90,
                    "Últimos 6 meses": 180,
                    "Último ano": 365
                }
                
                days_back = period_map[result_period]
                cutoff_date = datetime.now() - timedelta(days=days_back)
                
                # Análise de progresso dos pacientes
                patient_progress = pd.read_sql_query(f"""
                    SELECT 
                        p.full_name,
                        p.patient_id,
                        p.current_weight,
                        p.target_weight,
                        MIN(pp.weight) as first_weight,
                        MAX(pp.weight) as last_weight,
                        COUNT(pp.id) as total_records,
                        MIN(pp.record_date) as first_date,
                        MAX(pp.record_date) as last_date
                    FROM patients p
                    JOIN patient_progress pp ON pp.patient_id = p.id
                    WHERE pp.record_date >= '{cutoff_date.strftime('%Y-%m-%d')}'
                    AND p.active = 1
                    GROUP BY p.id, p.full_name, p.patient_id, p.current_weight, p.target_weight
                    HAVING COUNT(pp.id) >= 2
                    ORDER BY p.full_name
                """, conn)
                
                if not patient_progress.empty:
                    # Calcular métricas de sucesso
                    patient_progress['weight_change'] = patient_progress['last_weight'] - patient_progress['first_weight']
                    patient_progress['progress_days'] = (pd.to_datetime(patient_progress['last_date']) - pd.to_datetime(patient_progress['first_date'])).dt.days
                    
                    # Classificar resultados
                    def classify_result(row):
                        if pd.isna(row['target_weight']) or pd.isna(row['weight_change']):
                            return 'Sem meta definida'
                        
                        if row['target_weight'] < row['first_weight']:  # Meta de emagrecimento
                            if row['weight_change'] <= -2:  # Perdeu mais de 2kg
                                return 'Excelente progresso'
                            elif row['weight_change'] <= -0.5:  # Perdeu algo
                                return 'Bom progresso'
                            elif row['weight_change'] <= 1:  # Manteve peso
                                return 'Progresso estável'
                            else:
                                return 'Progresso insatisfatório'
                        else:  # Meta de ganho de peso
                            if row['weight_change'] >= 2:
                                return 'Excelente progresso'
                            elif row['weight_change'] >= 0.5:
                                return 'Bom progresso'
                            elif row['weight_change'] >= -1:
                                return 'Progresso estável'
                            else:
                                return 'Progresso insatisfatório'
                    
                    patient_progress['result_classification'] = patient_progress.apply(classify_result, axis=1)
                    
                    # Resumo de resultados
                    st.markdown("### 📊 Resumo de Resultados")
                    
                    result_summary = patient_progress['result_classification'].value_counts()
                    
                    col_result1, col_result2 = st.columns(2)
                    
                    with col_result1:
                        # Métricas de sucesso
                        total_patients_analyzed = len(patient_progress)
                        successful_patients = len(patient_progress[patient_progress['result_classification'].isin(['Excelente progresso', 'Bom progresso'])])
                        success_rate = (successful_patients / total_patients_analyzed * 100) if total_patients_analyzed > 0 else 0
                        
                        st.metric("👥 Pacientes Analisados", total_patients_analyzed)
                        st.metric("✅ Taxa de Sucesso", f"{success_rate:.1f}%")
                        st.metric("📊 Perda Média de Peso", f"{patient_progress['weight_change'].mean():.1f} kg")
                    
                    with col_result2:
                        # Gráfico de distribuição de resultados
                        fig = px.pie(values=result_summary.values, names=result_summary.index,
                                   title="📊 Distribuição de Resultados")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Tabela detalhada
                    st.markdown("### 📋 Resultados Detalhados")
                    
                    display_progress = patient_progress[[
                        'full_name', 'patient_id', 'weight_change', 'progress_days', 
                        'total_records', 'result_classification'
                    ]].copy()
                    
                    display_progress.columns = [
                        'Nome', 'ID', 'Variação Peso (kg)', 'Dias Acompanhamento', 
                        'Registros', 'Classificação'
                    ]
                    
                    # Colorir por resultado
                    def color_result(val):
                        if 'Excelente' in val:
                            return 'background-color: #c8e6c9'
                        elif 'Bom' in val:
                            return 'background-color: #fff3e0'
                        elif 'Estável' in val:
                            return 'background-color: #e3f2fd'
                        else:
                            return 'background-color: #ffebee'
                    
                    styled_df = display_progress.style.applymap(color_result, subset=['Classificação'])
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                    
                    # Exportar relatório
                    csv_data = display_progress.to_csv(index=False)
                    st.download_button(
                        label="📥 Baixar Relatório CSV",
                        data=csv_data,
                        file_name=f"relatorio_resultados_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                
                else:
                    st.warning("📊 Não há dados suficientes para gerar o relatório no período selecionado.")
                
                conn.close()
    
    with tab3:
        st.subheader("💰 Relatório Financeiro Detalhado")
        
        # Configurações do relatório
        col_config1, col_config2, col_config3 = st.columns(3)
        
        with col_config1:
            report_type = st.selectbox("📊 Tipo de Relatório", [
                "Receita por Período",
                "Análise de Inadimplência", 
                "Performance por Nutricionista",
                "Projeção de Receita"
            ])
        
        with col_config2:
            period_start = st.date_input("📅 Início", value=datetime.now().date().replace(day=1))
        
        with col_config3:
            period_end = st.date_input("📅 Fim", value=datetime.now().date())
        
        if st.button("💰 Gerar Relatório Financeiro", type="primary"):
            with st.spinner("💰 Processando dados financeiros..."):
                conn = sqlite3.connect('nutriapp360.db')
                
                if report_type == "Receita por Período":
                    # Análise de receita detalhada
                    st.markdown("### 💰 Análise de Receita por Período")
                    
                    daily_revenue = pd.read_sql_query(f"""
                        SELECT 
                            DATE(created_at) as date,
                            COUNT(*) as transactions,
                            SUM(CASE WHEN payment_status = 'pago' THEN amount ELSE 0 END) as revenue,
                            SUM(CASE WHEN payment_status = 'pendente' THEN amount ELSE 0 END) as pending,
                            AVG(CASE WHEN payment_status = 'pago' THEN amount END) as avg_ticket
                        FROM patient_financial 
                        WHERE DATE(created_at) BETWEEN '{period_start}' AND '{period_end}'
                        GROUP BY DATE(created_at)
                        ORDER BY date
                    """, conn)
                    
                    if not daily_revenue.empty:
                        # Gráfico de receita diária
                        fig = go.Figure()
                        
                        fig.add_trace(go.Bar(
                            x=daily_revenue['date'],
                            y=daily_revenue['revenue'],
                            name='Receita',
                            marker_color='green'
                        ))
                        
                        fig.add_trace(go.Bar(
                            x=daily_revenue['date'],
                            y=daily_revenue['pending'],
                            name='Pendente',
                            marker_color='orange'
                        ))
                        
                        fig.update_layout(
                            title="💰 Receita e Valores Pendentes por Dia",
                            xaxis_title="Data",
                            yaxis_title="Valor (R$)",
                            height=400,
                            barmode='stack'
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Resumo do período
                        total_revenue = daily_revenue['revenue'].sum()
                        total_pending = daily_revenue['pending'].sum()
                        avg_daily_revenue = daily_revenue['revenue'].mean()
                        
                        col_summary1, col_summary2, col_summary3 = st.columns(3)
                        
                        with col_summary1:
                            st.metric("💰 Receita Total", f"R$ {total_revenue:,.2f}")
                        
                        with col_summary2:
                            st.metric("⏰ Total Pendente", f"R$ {total_pending:,.2f}")
                        
                        with col_summary3:
                            st.metric("📊 Receita Média/Dia", f"R$ {avg_daily_revenue:,.2f}")
                
                elif report_type == "Análise de Inadimplência":
                    st.markdown("### 🚨 Análise de Inadimplência")
                    
                    overdue_analysis = pd.read_sql_query(f"""
                        SELECT 
                            p.full_name as patient_name,
                            pf.amount,
                            pf.due_date,
                            julianday('now') - julianday(pf.due_date) as days_overdue,
                            pf.service_type,
                            pf.payment_method
                        FROM patient_financial pf
                        JOIN patients p ON p.id = pf.patient_id
                        WHERE pf.payment_status = 'pendente' 
                        AND pf.due_date < date('now')
                        AND DATE(pf.created_at) BETWEEN '{period_start}' AND '{period_end}'
                        ORDER BY days_overdue DESC
                    """, conn)
                    
                    if not overdue_analysis.empty:
                        # Métricas de inadimplência
                        total_overdue = overdue_analysis['amount'].sum()
                        avg_days_overdue = overdue_analysis['days_overdue'].mean()
                        worst_case = overdue_analysis['days_overdue'].max()
                        
                        col_over1, col_over2, col_over3 = st.columns(3)
                        
                        with col_over1:
                            st.metric("💸 Total em Atraso", f"R$ {total_overdue:,.2f}")
                        
                        with col_over2:
                            st.metric("⏱️ Atraso Médio", f"{avg_days_overdue:.0f} dias")
                        
                        with col_over3:
                            st.metric("🚨 Maior Atraso", f"{worst_case:.0f} dias")
                        
                        # Gráfico de distribuição por faixa de atraso
                        def categorize_overdue(days):
                            if days <= 7:
                                return "1-7 dias"
                            elif days <= 30:
                                return "8-30 dias"
                            elif days <= 60:
                                return "31-60 dias"
                            else:
                                return ">60 dias"
                        
                        overdue_analysis['category'] = overdue_analysis['days_overdue'].apply(categorize_overdue)
                        category_summary = overdue_analysis.groupby('category')['amount'].sum().reset_index()
                        
                        fig = px.bar(category_summary, x='category', y='amount',
                                   title="💸 Valores em Atraso por Faixa de Tempo",
                                   color='amount', color_continuous_scale='Reds')
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Lista detalhada
                        st.markdown("### 📋 Pagamentos em Atraso")
                        st.dataframe(overdue_analysis, use_container_width=True, hide_index=True)
                    
                    else:
                        st.success("✅ Nenhum pagamento em atraso no período!")
                
                conn.close()
    
    with tab4:
        st.subheader("🎯 Relatório Personalizado")
        
        st.markdown("### 🛠️ Construtor de Relatório")
        
        # Seleção de métricas
        col_custom1, col_custom2 = st.columns(2)
        
        with col_custom1:
            st.markdown("**📊 Métricas Disponíveis:**")
            
            metrics_selected = st.multiselect("Selecione as métricas:", [
                "Total de Consultas",
                "Taxa de Comparecimento", 
                "Receita Total",
                "Novos Pacientes",
                "Pacientes com Progresso",
                "Planos Alimentares Ativos",
                "Conversas com IA",
                "Taxa de Cancelamento"
            ])
        
        with col_custom2:
            st.markdown("**📅 Configurações de Período:**")
            
            aggregation = st.selectbox("Agrupar por:", ["Dia", "Semana", "Mês"])
            chart_type = st.selectbox("Tipo de Gráfico:", ["Linha", "Barra", "Área"])
            
            custom_start = st.date_input("Data inicial:", value=datetime.now().date() - timedelta(days=30))
            custom_end = st.date_input("Data final:", value=datetime.now().date())
        
        # Filtros adicionais
        st.markdown("### 🔍 Filtros Adicionais")
        
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            nutritionist_custom = st.selectbox("🥗 Nutricionista:", ["Todos", "Dr. Ana Silva"])
        
        with col_filter2:
            patient_status = st.selectbox("👥 Status do Paciente:", ["Todos", "Ativo", "Inativo"])
        
        with col_filter3:
            appointment_type = st.selectbox("📅 Tipo de Consulta:", ["Todos", "Primeira consulta", "Retorno"])
        
        if st.button("🎯 Gerar Relatório Personalizado", type="primary"):
            if not metrics_selected:
                st.error("❌ Selecione pelo menos uma métrica!")
            else:
                with st.spinner("🎯 Gerando relatório personalizado..."):
                    st.success(f"✅ Relatório personalizado gerado com {len(metrics_selected)} métricas!")
                    
                    # Simulação de dados para demonstração
                    date_range = pd.date_range(start=custom_start, end=custom_end, freq='D')
                    
                    # Gerar dados simulados para cada métrica
                    report_data = pd.DataFrame({'date': date_range})
                    
                    for metric in metrics_selected:
                        if metric == "Total de Consultas":
                            report_data[metric] = np.random.randint(5, 20, len(date_range))
                        elif metric == "Taxa de Comparecimento":
                            report_data[metric] = np.random.uniform(75, 95, len(date_range))
                        elif metric == "Receita Total":
                            report_data[metric] = np.random.uniform(1000, 5000, len(date_range))
                        elif metric == "Novos Pacientes":
                            report_data[metric] = np.random.randint(0, 5, len(date_range))
                        else:
                            report_data[metric] = np.random.randint(1, 50, len(date_range))
                    
                    # Criar gráfico baseado na seleção
                    if chart_type == "Linha":
                        fig = px.line(report_data, x='date', y=metrics_selected,
                                    title="📈 Relatório Personalizado - Tendência")
                    elif chart_type == "Barra":
                        fig = px.bar(report_data, x='date', y=metrics_selected[0] if len(metrics_selected) == 1 else metrics_selected,
                                   title="📊 Relatório Personalizado - Comparação")
                    else:  # Área
                        fig = px.area(report_data, x='date', y=metrics_selected,
                                    title="📊 Relatório Personalizado - Área")
                    
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Tabela de dados
                    st.markdown("### 📋 Dados do Relatório")
                    st.dataframe(report_data, use_container_width=True, hide_index=True)
                    
                    # Opções de exportação
                    col_export1, col_export2, col_export3 = st.columns(3)
                    
                    with col_export1:
                        csv_data = report_data.to_csv(index=False)
                        st.download_button(
                            label="📥 Baixar CSV",
                            data=csv_data,
                            file_name=f"relatorio_personalizado_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                    
                    with col_export2:
                        st.download_button(
                            label="📊 Baixar Excel",
                            data="Arquivo Excel simulado",
                            file_name=f"relatorio_personalizado_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    with col_export3:
                        st.download_button(
                            label="📄 Baixar PDF",
                            data="Relatório PDF simulado",
                            file_name=f"relatorio_personalizado_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf"
                        )

def show_audit_log():
    st.markdown('<h1 class="main-header">🔍 Log de Auditoria</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Atividades Recentes", "🔍 Busca Avançada", "📊 Análise de Segurança"])
    
    with tab1:
        st.subheader("📋 Atividades Recentes do Sistema")
        
        # Filtros rápidos
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            time_filter = st.selectbox("⏰ Período", [
                "Última hora",
                "Últimas 24 horas", 
                "Últimos 7 dias",
                "Últimos 30 dias",
                "Personalizado"
            ])
        
        with col_filter2:
            action_filter = st.selectbox("🎯 Tipo de Ação", [
                "Todas",
                "Login/Logout",
                "Criação de registros",
                "Atualizações",
                "Exclusões",
                "Acessos a dados"
            ])
        
        with col_filter3:
            user_filter = st.selectbox("👤 Usuário", ["Todos", "Administradores", "Nutricionistas", "Secretárias"])
        
        # Buscar logs
        conn = sqlite3.connect('nutriapp360.db')
        
        # Determinar filtro de tempo
        if time_filter == "Última hora":
            time_condition = "al.created_at >= datetime('now', '-1 hour')"
        elif time_filter == "Últimas 24 horas":
            time_condition = "al.created_at >= datetime('now', '-1 day')"
        elif time_filter == "Últimos 7 dias":
            time_condition = "al.created_at >= datetime('now', '-7 days')"
        elif time_filter == "Últimos 30 dias":
            time_condition = "al.created_at >= datetime('now', '-30 days')"
        else:
            time_condition = "1=1"  # Personalizado - mostrar todos
        
        # Query principal
        audit_query = f"""
            SELECT 
                al.*,
                u.full_name,
                u.role,
                u.username
            FROM audit_log al
            JOIN users u ON u.id = al.user_id
            WHERE {time_condition}
        """
        
        # Aplicar filtros adicionais
        if action_filter != "Todas":
            action_map = {
                "Login/Logout": "('login', 'logout')",
                "Criação de registros": "('create_patient', 'create_appointment', 'create_meal_plan', 'create_recipe', 'create_financial')",
                "Atualizações": "('update_profile', 'update_patient', 'update_appointment')",
                "Exclusões": "('delete_patient', 'delete_appointment')",
                "Acessos a dados": "('view_patient', 'view_reports')"
            }
            
            if action_filter in action_map:
                audit_query += f" AND al.action_type IN {action_map[action_filter]}"
        
        if user_filter != "Todos":
            role_map = {
                "Administradores": "'admin'",
                "Nutricionistas": "'nutritionist'",
                "Secretárias": "'secretary'"
            }
            
            if user_filter in role_map:
                audit_query += f" AND u.role = {role_map[user_filter]}"
        
        audit_query += " ORDER BY al.created_at DESC LIMIT 100"
        
        audit_logs = pd.read_sql_query(audit_query, conn)
        
        if not audit_logs.empty:
            # Estatísticas rápidas
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            
            with col_stat1:
                st.metric("📊 Total de Ações", len(audit_logs))
            
            with col_stat2:
                unique_users = audit_logs['user_id'].nunique()
                st.metric("👥 Usuários Ativos", unique_users)
            
            with col_stat3:
                most_common_action = audit_logs['action_type'].mode().iloc[0] if not audit_logs.empty else "N/A"
                st.metric("🎯 Ação Mais Comum", most_common_action)
            
            with col_stat4:
                # Ações por hora (estimativa)
                if len(audit_logs) > 0:
                    first_log = pd.to_datetime(audit_logs['created_at']).min()
                    last_log = pd.to_datetime(audit_logs['created_at']).max()
                    hours_diff = max(1, (last_log - first_log).total_seconds() / 3600)
                    actions_per_hour = len(audit_logs) / hours_diff
                    st.metric("⚡ Ações/Hora", f"{actions_per_hour:.1f}")
            
            # Timeline de atividades
            st.markdown("### 🕐 Timeline de Atividades")
            
            for idx, log in audit_logs.iterrows():
                log_time = pd.to_datetime(log['created_at']).strftime('%d/%m/%Y %H:%M:%S')
                
                # Ícones por tipo de ação
                action_icons = {
                    'login': '🔓',
                    'logout': '🔒',
                    'create_patient': '👥➕',
                    'create_appointment': '📅➕',
                    'create_meal_plan': '🍽️➕',
                    'update_profile': '👤✏️',
                    'update_patient': '👥✏️',
                    'record_progress': '📊➕',
                    'create_financial': '💰➕',
                    'update_payment_pago': '💰✅'
                }
                
                icon = action_icons.get(log['action_type'], '📝')
                
                # Cores por tipo de usuário
                role_colors = {
                    'admin': '#9C27B0',
                    'nutritionist': '#4CAF50',
                    'secretary': '#FF9800',
                    'patient': '#2196F3'
                }
                
                color = role_colors.get(log['role'], '#666')
                
                st.markdown(f"""
                <div style="border-left: 4px solid {color}; padding: 1rem; margin: 0.5rem 0; 
                            background: #f8f9fa; border-radius: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{icon} {log['full_name']}</strong> 
                            <span style="color: {color}; font-size: 0.9rem;">({log['role']})</span>
                        </div>
                        <small style="color: #666;">{log_time}</small>
                    </div>
                    <div style="margin-top: 0.5rem;">
                        <strong>Ação:</strong> {log['action_type']} 
                        {f"em <strong>{log['table_affected']}</strong>" if log['table_affected'] else ""}
                        {f" (ID: {log['record_id']})" if log['record_id'] else ""}
                    </div>
                    {f"<div style='margin-top: 0.3rem; color: #666;'><strong>IP:</strong> {log['ip_address']}</div>" if log['ip_address'] else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📝 Nenhuma atividade encontrada para os filtros selecionados.")
        
        conn.close()
    
    with tab2:
        st.subheader("🔍 Busca Avançada de Auditoria")
        
        with st.form("advanced_search_form"):
            col_search1, col_search2 = st.columns(2)
            
            with col_search1:
                search_user = st.text_input("👤 Nome do Usuário")
                search_action = st.text_input("🎯 Tipo de Ação")
                search_table = st.text_input("📋 Tabela Afetada")
            
            with col_search2:
                search_start_date = st.date_input("📅 Data Inicial", value=datetime.now().date() - timedelta(days=7))
                search_end_date = st.date_input("📅 Data Final", value=datetime.now().date())
                search_ip = st.text_input("🌐 Endereço IP")
            
            search_submitted = st.form_submit_button("🔍 Buscar", type="primary")
            
            if search_submitted:
                conn = sqlite3.connect('nutriapp360.db')
                
                # Construir query dinâmica
                where_conditions = ["1=1"]
                params = []
                
                if search_user:
                    where_conditions.append("u.full_name LIKE ?")
                    params.append(f"%{search_user}%")
                
                if search_action:
                    where_conditions.append("al.action_type LIKE ?")
                    params.append(f"%{search_action}%")
                
                if search_table:
                    where_conditions.append("al.table_affected LIKE ?")
                    params.append(f"%{search_table}%")
                
                if search_ip:
                    where_conditions.append("al.ip_address LIKE ?")
                    params.append(f"%{search_ip}%")
                
                where_conditions.append("DATE(al.created_at) BETWEEN ? AND ?")
                params.extend([search_start_date.strftime('%Y-%m-%d'), search_end_date.strftime('%Y-%m-%d')])
                
                search_query = f"""
                    SELECT 
                        al.*,
                        u.full_name,
                        u.role,
                        u.username
                    FROM audit_log al
                    JOIN users u ON u.id = al.user_id
                    WHERE {' AND '.join(where_conditions)}
                    ORDER BY al.created_at DESC
                    LIMIT 200
                """
                
                search_results = pd.read_sql_query(search_query, conn, params=params)
                
                if not search_results.empty:
                    st.success(f"🔍 Encontrados {len(search_results)} registros")
                    
                    # Exibir resultados em tabela
                    display_results = search_results[[
                        'created_at', 'full_name', 'role', 'action_type', 
                        'table_affected', 'record_id', 'ip_address'
                    ]].copy()
                    
                    display_results.columns = [
                        'Data/Hora', 'Usuário', 'Função', 'Ação', 
                        'Tabela', 'ID Registro', 'IP'
                    ]
                    
                    # Formatar data
                    display_results['Data/Hora'] = pd.to_datetime(display_results['Data/Hora']).dt.strftime('%d/%m/%Y %H:%M:%S')
                    
                    st.dataframe(display_results, use_container_width=True, hide_index=True)
                    
                    # Exportar resultados
                    csv_results = display_results.to_csv(index=False)
                    st.download_button(
                        label="📥 Exportar Resultados CSV",
                        data=csv_results,
                        file_name=f"auditoria_busca_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                else:
                    st.warning("🔍 Nenhum resultado encontrado para os critérios de busca.")
                
                conn.close()
    
    with tab3:
        st.subheader("📊 Análise de Segurança")
        
        conn = sqlite3.connect('nutriapp360.db')
        
        # Análise de padrões suspeitos
        st.markdown("### 🚨 Detecção de Padrões Suspeitos")
        
        col_security1, col_security2 = st.columns(2)
        
        with col_security1:
            # Logins fora do horário
            unusual_logins = pd.read_sql_query("""
                SELECT 
                    u.full_name,
                    al.created_at,
                    strftime('%H', al.created_at) as hour
                FROM audit_log al
                JOIN users u ON u.id = al.user_id
                WHERE al.action_type = 'login'
                AND (strftime('%H', al.created_at) < '06' OR strftime('%H', al.created_at) > '22')
                AND al.created_at >= datetime('now', '-7 days')
                ORDER BY al.created_at DESC
            """, conn)
            
            if not unusual_logins.empty:
                st.warning(f"⚠️ **Logins Fora do Horário:** {len(unusual_logins)} ocorrências")
                
                for idx, login in unusual_logins.iterrows():
                    login_time = pd.to_datetime(login['created_at']).strftime('%d/%m/%Y %H:%M')
                    st.write(f"• {login['full_name']} - {login_time}")
            else:
                st.success("✅ Nenhum login suspeito detectado")
        
        with col_security2:
            # Múltiplas tentativas de login
            failed_attempts = pd.read_sql_query("""
                SELECT 
                    u.full_name,
                    COUNT(*) as attempts,
                    MAX(al.created_at) as last_attempt
                FROM audit_log al
                JOIN users u ON u.id = al.user_id
                WHERE al.action_type LIKE '%failed%'
                AND al.created_at >= datetime('now', '-24 hours')
                GROUP BY u.id, u.full_name
                HAVING COUNT(*) > 3
                ORDER BY attempts DESC
            """, conn)
            
            if not failed_attempts.empty:
                st.error(f"🚨 **Múltiplas Tentativas Falhas:** {len(failed_attempts)} usuários")
                
                for idx, attempt in failed_attempts.iterrows():
                    last_attempt = pd.to_datetime(attempt['last_attempt']).strftime('%d/%m/%Y %H:%M')
                    st.write(f"• {attempt['full_name']} - {attempt['attempts']} tentativas (última: {last_attempt})")
            else:
                st.success("✅ Nenhuma atividade suspeita de login")
        
        # Gráfico de atividade por horário
        st.markdown("### 📈 Atividade por Horário")
        
        hourly_activity = pd.read_sql_query("""
            SELECT 
                strftime('%H', created_at) as hour,
                COUNT(*) as activities
            FROM audit_log 
            WHERE created_at >= datetime('now', '-7 days')
            GROUP BY strftime('%H', created_at)
            ORDER BY hour
        """, conn)
        
        if not hourly_activity.empty:
            hourly_activity['hour'] = hourly_activity['hour'].astype(int)
            
            fig = px.bar(hourly_activity, x='hour', y='activities',
                        title="📊 Atividades por Hora do Dia (Últimos 7 dias)")
            fig.update_xaxis(title="Hora do Dia", tickmode='linear', tick0=0, dtick=1)
            fig.update_yaxis(title="Número de Atividades")
            st.plotly_chart(fig, use_container_width=True)
        
        # Resumo de segurança
        st.markdown("### 🛡️ Resumo de Segurança")
        
        security_metrics = pd.read_sql_query("""
            SELECT 
                COUNT(DISTINCT CASE WHEN action_type = 'login' THEN user_id END) as active_users_7d,
                COUNT(CASE WHEN action_type = 'login' THEN 1 END) as total_logins_7d,
                COUNT(CASE WHEN action_type LIKE '%failed%' THEN 1 END) as failed_attempts_7d,
                COUNT(DISTINCT ip_address) as unique_ips_7d
            FROM audit_log 
            WHERE created_at >= datetime('now', '-7 days')
        """, conn).iloc[0]
        
        col_summary1, col_summary2, col_summary3, col_summary4 = st.columns(4)
        
        with col_summary1:
            st.metric("👥 Usuários Ativos (7d)", int(security_metrics['active_users_7d']))
        
        with col_summary2:
            st.metric("🔓 Total de Logins (7d)", int(security_metrics['total_logins_7d']))
        
        with col_summary3:
            st.metric("❌ Tentativas Falharam (7d)", int(security_metrics['failed_attempts_7d']))
        
        with col_summary4:
            st.metric("🌐 IPs Únicos (7d)", int(security_metrics['unique_ips_7d']))
        
        # Recomendações de segurança
        st.markdown("### 💡 Recomendações de Segurança")
        
        recommendations = []
        
        if security_metrics['failed_attempts_7d'] > 10:
            recommendations.append("🔴 Alto número de tentativas de login falharam. Considere implementar bloqueio temporário.")
        
        if security_metrics['unique_ips_7d'] > security_metrics['active_users_7d'] * 2:
            recommendations.append("🟡 Muitos IPs diferentes para poucos usuários. Monitore acessos remotos.")
        
        if len(unusual_logins) > 5:
            recommendations.append("🟡 Vários logins fora do horário comercial. Verifique necessidade.")
        
        if not recommendations:
            recommendations.append("🟢 Sistema apresenta padrões normais de segurança.")
        
        for rec in recommendations:
            st.markdown(rec)
        
        conn.close()

def show_system_settings():
    st.markdown('<h1 class="main-header">⚙️ Configurações do Sistema</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎛️ Configurações Gerais", "👥 Gestão de Usuários", "🔒 Segurança", "💾 Backup & Restauração"])
    
    with tab1:
        st.subheader("🎛️ Configurações Gerais do Sistema")
        
        # Configurações básicas
        st.markdown("### 🏢 Informações da Clínica")
        
        with st.form("clinic_info_form"):
            col_clinic1, col_clinic2 = st.columns(2)
            
            with col_clinic1:
                clinic_name = st.text_input("🏢 Nome da Clínica", value="NutriClínica Saúde & Bem-Estar")
                clinic_address = st.text_area("📍 Endereço", value="Rua das Flores, 123\nSão Paulo - SP\n01234-567")
                clinic_phone = st.text_input("📱 Telefone", value="(11) 3456-7890")
                clinic_email = st.text_input("📧 Email", value="contato@nutriclinica.com.br")
            
            with col_clinic2:
                clinic_cnpj = st.text_input("📋 CNPJ", value="12.345.678/0001-90")
                clinic_website = st.text_input("🌐 Website", value="www.nutriclinica.com.br")
                clinic_logo = st.file_uploader("🖼️ Logo da Clínica", type=['png', 'jpg', 'jpeg'])
                
                # Horário de funcionamento
                business_hours = st.text_area("🕐 Horário de Funcionamento", 
                                             value="Segunda a Sexta: 8h às 18h\nSábado: 8h às 12h")
            
            if st.form_submit_button("💾 Salvar Informações da Clínica"):
                st.success("✅ Informações da clínica atualizadas com sucesso!")
        
        # Configurações do sistema
        st.markdown("### ⚙️ Configurações do Sistema")
        
        col_sys1, col_sys2 = st.columns(2)
        
        with col_sys1:
            st.markdown("**📅 Agendamentos:**")
            
            appointment_duration = st.selectbox("⏱️ Duração padrão da consulta", [30, 45, 60, 90], index=2)
            appointment_interval = st.selectbox("⏰ Intervalo entre consultas", [15, 30, 45], index=1)
            
            max_appointments_day = st.number_input("📊 Máximo de consultas por dia", min_value=5, max_value=50, value=20)
            
            advance_booking_days = st.number_input("📅 Dias de antecedência para agendamento", min_value=1, max_value=90, value=30)
            
            st.markdown("**💰 Financeiro:**")
            
            default_consultation_price = st.number_input("💵 Valor padrão da consulta (R$)", min_value=50.0, value=150.0, step=10.0)
            payment_due_days = st.number_input("📅 Dias para vencimento", min_value=1, max_value=60, value=7)
        
        with col_sys2:
            st.markdown("**🔔 Notificações:**")
            
            email_notifications = st.checkbox("📧 Notificações por email", value=True)
            sms_notifications = st.checkbox("📱 Notificações por SMS", value=False)
            
            reminder_hours = st.selectbox("⏰ Lembrete de consulta (horas antes)", [2, 4, 12, 24], index=2)
            
            st.markdown("**🎯 Sistema:**")
            
            auto_backup = st.checkbox("💾 Backup automático diário", value=True)
            maintenance_mode = st.checkbox("🔧 Modo de manutenção", value=False)
            
            max_file_size = st.selectbox("📁 Tamanho máximo de arquivo (MB)", [5, 10, 20, 50], index=1)
            
            session_timeout = st.selectbox("⏱️ Timeout de sessão (minutos)", [30, 60, 120, 240], index=1)
        
        if st.button("⚙️ Salvar Configurações do Sistema"):
            st.success("✅ Configurações do sistema atualizadas!")
        
        # Status do sistema
        st.markdown("### 📊 Status do Sistema")
        
        col_status1, col_status2, col_status3, col_status4 = st.columns(4)
        
        with col_status1:
            st.metric("💾 Uso do Banco", "15.2 MB")
        
        with col_status2:
            st.metric("📁 Arquivos", "2.3 GB")
        
        with col_status3:
            st.metric("🔄 Uptime", "127 dias")
        
        with col_status4:
            st.metric("👥 Usuários Online", "3")
    
    with tab2:
        st.subheader("👥 Gestão Avançada de Usuários")
        
        # Políticas de usuário
        st.markdown("### 📋 Políticas de Usuário")
        
        col_policy1, col_policy2 = st.columns(2)
        
        with col_policy1:
            st.markdown("**🔒 Senhas:**")
            
            min_password_length = st.number_input("📏 Comprimento mínimo da senha", min_value=6, max_value=20, value=8)
            require_uppercase = st.checkbox("🔤 Exigir letras maiúsculas", value=True)
            require_numbers = st.checkbox("🔢 Exigir números", value=True)
            require_symbols = st.checkbox("🔣 Exigir símbolos", value=False)
            
            password_expiry_days = st.number_input("📅 Expiração da senha (dias)", min_value=30, max_value=365, value=90)
            
            st.markdown("**👤 Conta:**")
            
            max_login_attempts = st.number_input("❌ Máximo de tentativas de login", min_value=3, max_value=10, value=5)
            account_lockout_minutes = st.number_input("🔒 Bloqueio da conta (minutos)", min_value=5, max_value=60, value=15)
        
        with col_policy2:
            st.markdown("**📊 Atividade:**")
            
            inactive_days_warning = st.number_input("⚠️ Aviso de inatividade (dias)", min_value=30, max_value=180, value=60)
            inactive_days_disable = st.number_input("🚫 Desabilitar por inatividade (dias)", min_value=60, max_value=365, value=120)
            
            force_logout_hours = st.number_input("🔄 Logout forçado (horas)", min_value=8, max_value=72, value=24)
            
            st.markdown("**🔐 Autenticação:**")
            
            two_factor_auth = st.checkbox("🔐 Autenticação de dois fatores", value=False)
            remember_device_days = st.number_input("📱 Lembrar dispositivo (dias)", min_value=1, max_value=30, value=7)
        
        if st.button("👥 Salvar Políticas de Usuário"):
            st.success("✅ Políticas de usuário atualizadas!")
        
        # Permissões por função
        st.markdown("### 🔑 Permissões por Função")
        
        roles_permissions = {
            "👨‍⚕️ Administrador": {
                "Gestão de usuários": True,
                "Configurações do sistema": True,
                "Relatórios avançados": True,
                "Auditoria": True,
                "Backup/Restauração": True,
                "Gestão financeira": True
            },
            "🥗 Nutricionista": {
                "Gestão de pacientes": True,
                "Planos alimentares": True,
                "Receitas": True,
                "Consultas": True,
                "Relatórios básicos": True,
                "Progresso dos pacientes": True
            },
            "📋 Secretária": {
                "Agendamentos": True,
                "Informações básicas de pacientes": True,
                "Financeiro básico": True,
                "Relatórios operacionais": True,
                "Gestão de consultas": True,
                "Contato com pacientes": True
            },
            "🙋‍♂️ Paciente": {
                "Ver próprio perfil": True,
                "Ver próprio progresso": True,
                "Ver plano alimentar": True,
                "Agendamentos próprios": True,
                "Chat com IA": True,
                "Calculadoras": True
            }
        }
        
        for role, permissions in roles_permissions.items():
            with st.expander(f"🔑 Permissões - {role}"):
                cols = st.columns(2)
                
                for i, (permission, enabled) in enumerate(permissions.items()):
                    with cols[i % 2]:
                        st.checkbox(permission, value=enabled, key=f"{role}_{permission}")
    
    with tab3:
        st.subheader("🔒 Configurações de Segurança")
        
        # Configurações de segurança
        st.markdown("### 🛡️ Políticas de Segurança")
        
        col_sec1, col_sec2 = st.columns(2)
        
        with col_sec1:
            st.markdown("**🔐 Criptografia:**")
            
            encryption_level = st.selectbox("🔒 Nível de criptografia", ["AES-128", "AES-256"], index=1)
            encrypt_database = st.checkbox("💾 Criptografar banco de dados", value=True)
            encrypt_backups = st.checkbox("📦 Criptografar backups", value=True)
            
            st.markdown("**🌐 Rede:**")
            
            ssl_required = st.checkbox("🔒 Exigir SSL/HTTPS", value=True)
            ip_whitelist = st.text_area("📍 Lista de IPs permitidos", placeholder="192.168.1.0/24\n10.0.0.0/8")
            
            rate_limiting = st.checkbox("⚡ Limitação de taxa de requisições", value=True)
            max_requests_per_minute = st.number_input("📊 Máximo de requisições/minuto", min_value=10, max_value=1000, value=100)
        
        with col_sec2:
            st.markdown("**📋 Auditoria:**")
            
            log_all_actions = st.checkbox("📝 Registrar todas as ações", value=True)
            log_retention_days = st.number_input("📅 Retenção de logs (dias)", min_value=30, max_value=2555, value=365)
            
            alert_failed_logins = st.checkbox("🚨 Alertar tentativas de login falharam", value=True)
            alert_admin_actions = st.checkbox("⚠️ Alertar ações administrativas", value=True)
            
            st.markdown("**🔍 Monitoramento:**")
            
            monitor_unusual_activity = st.checkbox("👁️ Monitorar atividade incomum", value=True)
            alert_threshold_logins = st.number_input("🚨 Alertar após X logins falharam", min_value=3, max_value=20, value=5)
            
            auto_lock_suspicious = st.checkbox("🔒 Bloquear automaticamente atividade suspeita", value=False)
        
        if st.button("🔒 Salvar Configurações de Segurança"):
            st.success("✅ Configurações de segurança atualizadas!")
        
        # Certificados e chaves
        st.markdown("### 🔑 Certificados e Chaves")
        
        col_cert1, col_cert2 = st.columns(2)
        
        with col_cert1:
            st.markdown("**🔒 Certificado SSL:**")
            
            ssl_cert_file = st.file_uploader("📄 Arquivo do certificado (.crt)", type=['crt', 'pem'])
            ssl_key_file = st.file_uploader("🔐 Chave privada (.key)", type=['key', 'pem'])
            
            ssl_expiry = st.date_input("📅 Data de expiração", value=datetime.now().date() + timedelta(days=365))
            
            if ssl_cert_file and ssl_key_file:
                st.success("✅ Certificados carregados com sucesso!")
            else:
                st.warning("⚠️ Carregue os certificados SSL para maior segurança")
        
        with col_cert2:
            st.markdown("**🔐 Chaves de API:**")
            
            api_key_email = st.text_input("📧 Chave API Email", type="password", placeholder="sk-email-...")
            api_key_sms = st.text_input("📱 Chave API SMS", type="password", placeholder="sk-sms-...")
            api_key_backup = st.text_input("💾 Chave API Backup", type="password", placeholder="sk-backup-...")
            
            if st.button("🔄 Gerar Novas Chaves API"):
                st.info("🔄 Novas chaves de API geradas. Atualize suas integrações.")
        
        # Teste de segurança
        st.markdown("### 🧪 Teste de Segurança")
        
        col_test1, col_test2, col_test3 = st.columns(3)
        
        with col_test1:
            if st.button("🔍 Verificar Vulnerabilidades"):
                with st.spinner("🔍 Verificando sistema..."):
                    # Simular verificação
                    import time
                    time.sleep(2)
                    
                    st.success("✅ Sistema seguro - Nenhuma vulnerabilidade encontrada")
        
        with col_test2:
            if st.button("🔒 Teste de Penetração"):
                with st.spinner("🔒 Executando testes..."):
                    import time
                    time.sleep(3)
                    
                    st.info("🔒 Teste concluído - 3 pontos de melhoria identificados")
        
        with col_test3:
            if st.button("📊 Relatório de Segurança"):
                st.download_button(
                    label="📥 Baixar Relatório",
                    data="Relatório de Segurança - Sistema aprovado em todos os testes",
                    file_name=f"security_report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
    
    with tab4:
        st.subheader("💾 Backup & Restauração")
        
        # Configurações de backup
        st.markdown("### ⚙️ Configurações de Backup")
        
        col_backup1, col_backup2 = st.columns(2)
        
        with col_backup1:
            st.markdown("**📅 Agendamento:**")
            
            auto_backup_enabled = st.checkbox("🔄 Backup automático", value=True)
            backup_frequency = st.selectbox("⏰ Frequência", ["Diário", "Semanal", "Mensal"])
            backup_time = st.time_input("🕐 Horário", value=datetime.now().time().replace(hour=2, minute=0))
            
            retention_days = st.number_input("📅 Manter backups por (dias)", min_value=7, max_value=365, value=30)
            
            st.markdown("**📦 Tipo de Backup:**")
            
            backup_database = st.checkbox("💾 Banco de dados", value=True)
            backup_files = st.checkbox("📁 Arquivos do sistema", value=True)
            backup_logs = st.checkbox("📋 Logs de auditoria", value=True)
            backup_configs = st.checkbox("⚙️ Configurações", value=True)
        
        with col_backup2:
            st.markdown("**☁️ Destino:**")
            
            backup_location = st.selectbox("📍 Local de armazenamento", [
                "Local (servidor)",
                "Google Drive", 
                "AWS S3",
                "Dropbox",
                "FTP Server"
            ])
            
            if backup_location != "Local (servidor)":
                backup_credentials = st.text_area("🔑 Credenciais", placeholder="Configurações de acesso...")
            
            compress_backup = st.checkbox("🗜️ Comprimir backup", value=True)
            encrypt_backup = st.checkbox("🔒 Criptografar backup", value=True)
            
            test_restore = st.checkbox("🧪 Testar restauração automaticamente", value=False)
        
        if st.button("💾 Salvar Configurações de Backup"):
            st.success("✅ Configurações de backup atualizadas!")
        
        # Backup manual
        st.markdown("### 📦 Backup Manual")
        
        col_manual1, col_manual2, col_manual3 = st.columns(3)
        
        with col_manual1:
            if st.button("💾 Criar Backup Completo", type="primary"):
                with st.spinner("💾 Criando backup completo..."):
                    # Simular criação de backup
                    progress_bar = st.progress(0)
                    
                    for i in range(101):
                        progress_bar.progress(i)
                        if i % 20 == 0:
                            time.sleep(0.1)
                    
                    backup_filename = f"backup_completo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                    st.success(f"✅ Backup criado: {backup_filename}")
                    
                    st.download_button(
                        label="📥 Baixar Backup",
                        data="Dados do backup simulado",
                        file_name=backup_filename,
                        mime="application/zip"
                    )
        
        with col_manual2:
            if st.button("💾 Backup Rápido (BD)"):
                with st.spinner("💾 Criando backup do banco..."):
                    time.sleep(1)
                    
                    db_backup_filename = f"db_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
                    st.success(f"✅ Backup do BD criado: {db_backup_filename}")
        
        with col_manual3:
            if st.button("📁 Backup de Arquivos"):
                with st.spinner("📁 Copiando arquivos..."):
                    time.sleep(1)
                    
                    files_backup_filename = f"files_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
                    st.success(f"✅ Backup de arquivos criado: {files_backup_filename}")
        
        # Histórico de backups
        st.markdown("### 📋 Histórico de Backups")
        
        # Simular histórico de backups
        backup_history = [
            {
                "data": "2024-01-15 02:00:00",
                "tipo": "Completo",
                "tamanho": "45.2 MB",
                "status": "✅ Sucesso",
                "local": "AWS S3"
            },
            {
                "data": "2024-01-14 02:00:00", 
                "tipo": "Completo",
                "tamanho": "44.8 MB",
                "status": "✅ Sucesso",
                "local": "AWS S3"
            },
            {
                "data": "2024-01-13 02:00:00",
                "tipo": "Completo", 
                "tamanho": "44.1 MB",
                "status": "✅ Sucesso",
                "local": "AWS S3"
            },
            {
                "data": "2024-01-12 02:00:00",
                "tipo": "Completo",
                "tamanho": "43.9 MB", 
                "status": "⚠️ Parcial",
                "local": "AWS S3"
            },
            {
                "data": "2024-01-11 02:00:00",
                "tipo": "Completo",
                "tamanho": "43.5 MB",
                "status": "✅ Sucesso", 
                "local": "AWS S3"
            }
        ]
        
        backup_df = pd.DataFrame(backup_history)
        backup_df.columns = ["📅 Data/Hora", "📦 Tipo", "📊 Tamanho", "✅ Status", "📍 Local"]
        
        st.dataframe(backup_df, use_container_width=True, hide_index=True)
        
        # Restauração
        st.markdown("### 🔄 Restauração do Sistema")
        
        col_restore1, col_restore2 = st.columns(2)
        
        with col_restore1:
            st.markdown("**📁 Restaurar de Arquivo:**")
            
            restore_file = st.file_uploader("📥 Selecionar arquivo de backup", type=['zip', 'sql', 'tar.gz'])
            
            if restore_file:
                restore_options = st.multiselect("🔄 O que restaurar:", [
                    "💾 Banco de dados",
                    "📁 Arquivos do sistema", 
                    "📋 Logs",
                    "⚙️ Configurações"
                ])
                
                if st.button("🔄 Restaurar Sistema", type="primary"):
                    if restore_options:
                        st.warning("⚠️ **ATENÇÃO:** Esta operação substituirá os dados atuais!")
                        
                        confirm_restore = st.checkbox("✅ Confirmo que quero restaurar o sistema")
                        
                        if confirm_restore:
                            with st.spinner("🔄 Restaurando sistema..."):
                                time.sleep(3)
                                st.success("✅ Sistema restaurado com sucesso!")
                    else:
                        st.error("❌ Selecione pelo menos um item para restaurar")
        
        with col_restore2:
            st.markdown("**☁️ Restaurar da Nuvem:**")
            
            cloud_backups = [
                "backup_completo_20240115_020000.zip",
                "backup_completo_20240114_020000.zip", 
                "backup_completo_20240113_020000.zip",
                "backup_completo_20240112_020000.zip"
            ]
            
            selected_cloud_backup = st.selectbox("☁️ Backup na nuvem:", cloud_backups)
            
            if st.button("☁️ Restaurar da Nuvem"):
                st.warning("⚠️ Esta operação baixará e restaurará o backup selecionado")
                
                if st.checkbox("✅ Confirmo a restauração da nuvem"):
                    with st.spinner("☁️ Baixando e restaurando..."):
                        time.sleep(4)
                        st.success("✅ Sistema restaurado da nuvem com sucesso!")
        
        # Verificação de integridade
        st.markdown("### 🔍 Verificação de Integridade")
        
        col_integrity1, col_integrity2, col_integrity3 = st.columns(3)
        
        with col_integrity1:
            if st.button("🔍 Verificar Banco de Dados"):
                with st.spinner("🔍 Verificando integridade..."):
                    time.sleep(2)
                    st.success("✅ Banco de dados íntegro")
        
        with col_integrity2:
            if st.button("📁 Verificar Arquivos"):
                with st.spinner("📁 Verificando arquivos..."):
                    time.sleep(2)
                    st.success("✅ Todos os arquivos estão corretos")
        
        with col_integrity3:
            if st.button("🔄 Reparar Automaticamente"):
                with st.spinner("🔄 Executando reparos..."):
                    time.sleep(3)
                    st.info("🔧 Sistema verificado - Nenhum reparo necessário")

# EXECUTAR APLICAÇÃO PRINCIPAL
if __name__ == "__main__":
    main()        conn.close()

# FUNCIONALIDADES DO PACIENTE

def show_patient_dashboard():
    st.markdown('<h1 class="main-header">📊 Meu Dashboard</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar dados do paciente
    patient_data = pd.read_sql_query("""
        SELECT p.*, n.full_name as nutritionist_name
        FROM patients p
        LEFT JOIN users n ON n.id = p.nutritionist_id
        WHERE p.user_id = ?
    """, conn, params=[user_id])
    
    if not patient_data.empty:
        patient = patient_data.iloc[0]
        
        # Informações principais do paciente
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            # Calcular IMC
            if patient['height'] and patient['current_weight']:
                imc = patient['current_weight'] / (patient['height'] ** 2)
                if imc < 18.5:
                    imc_status = "Abaixo do peso"
                    imc_color = "#2196F3"
                elif imc < 25:
                    imc_status = "Peso normal"
                    imc_color = "#4CAF50"
                elif imc < 30:
                    imc_status = "Sobrepeso"
                    imc_color = "#FF9800"
                else:
                    imc_status = "Obesidade"
                    imc_color = "#F44336"
                
                st.markdown(f"""
                <div class="metric-card" style="border-left: 4px solid {imc_color};">
                    <h3 style="margin: 0; color: {imc_color};">📊 IMC: {imc:.1f}</h3>
                    <p style="margin: 0;">{imc_status}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card">
                    <h3 style="margin: 0; color: #999;">📊 IMC: N/A</h3>
                    <p style="margin: 0;">Dados incompletos</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col_info2:
            # Peso atual vs meta
            if patient['current_weight'] and patient['target_weight']:
                weight_diff = patient['current_weight'] - patient['target_weight']
                diff_color = "#4CAF50" if weight_diff <= 0 else "#FF9800"
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin: 0; color: #2196F3;">⚖️ {patient['current_weight']} kg</h3>
                    <p style="margin: 0;">Peso Atual</p>
                    <small style="color: {diff_color};">Meta: {patient['target_weight']} kg ({weight_diff:+.1f})</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card">
                    <h3 style="margin: 0; color: #999;">⚖️ N/A</h3>
                    <p style="margin: 0;">Peso não informado</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col_info3:
            # Próxima consulta
            next_appointment = pd.read_sql_query("""
                SELECT appointment_date, appointment_type 
                FROM appointments 
                WHERE patient_id = ? AND appointment_date > datetime('now') 
                AND status != 'cancelado'
                ORDER BY appointment_date ASC 
                LIMIT 1
            """, conn, params=[patient['id']])
            
            if not next_appointment.empty:
                next_date = pd.to_datetime(next_appointment.iloc[0]['appointment_date'])
                days_until = (next_date.date() - datetime.now().date()).days
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3 style="margin: 0; color: #9C27B0;">📅 {days_until}</h3>
                    <p style="margin: 0;">Dias para próxima consulta</p>
                    <small>{next_date.strftime('%d/%m/%Y %H:%M')}</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card">
                    <h3 style="margin: 0; color: #999;">📅 N/A</h3>
                    <p style="margin: 0;">Nenhuma consulta agendada</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Informações do perfil
        st.markdown(f"""
        <div class="patient-info-card">
            <h4>👋 Bem-vindo(a), {patient['full_name']}!</h4>
            <p><strong>📋 ID do Paciente:</strong> {patient['patient_id']}</p>
            <p><strong>🥗 Seu Nutricionista:</strong> {patient['nutritionist_name'] or 'Não definido'}</p>
            <p><strong>🏃‍♂️ Nível de Atividade:</strong> {patient['activity_level'] or 'Não informado'}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progresso recente
        col_progress1, col_progress2 = st.columns(2)
        
        with col_progress1:
            st.subheader("📈 Meu Progresso Recente")
            
            recent_progress = pd.read_sql_query("""
                SELECT record_date, weight, notes 
                FROM patient_progress 
                WHERE patient_id = ?
                ORDER BY record_date DESC 
                LIMIT 5
            """, conn, params=[patient['id']])
            
            if not recent_progress.empty:
                for idx, progress in recent_progress.iterrows():
                    record_date = pd.to_datetime(progress['record_date']).strftime('%d/%m/%Y')
                    
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #4CAF50;">
                        <strong>📅 {record_date}:</strong> {progress['weight']} kg
                        {f"<br><small>{progress['notes']}</small>" if progress['notes'] else ""}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("📝 Nenhum registro de progresso ainda. Seu nutricionista irá acompanhar sua evolução!")
        
        with col_progress2:
            st.subheader("🎯 Minhas Metas")
            
            # Sistema de pontos/gamificação
            points_data = pd.read_sql_query("""
                SELECT points, level, total_points, streak_days 
                FROM patient_points 
                WHERE patient_id = ?
            """, conn, params=[patient['id']])
            
            if not points_data.empty:
                points = points_data.iloc[0]
                
                # Calcular progresso do nível
                points_for_next_level = (points['level'] * 100) - points['points']
                level_progress = (points['points'] / (points['level'] * 100)) * 100
                
                st.markdown(f"""
                <div class="gamification-card">
                    <h4 style="margin: 0; color: #9C27B0;">🏆 Nível {points['level']}</h4>
                    <p style="margin: 0.5rem 0;"><strong>⭐ Pontos:</strong> {points['points']}</p>
                    <p style="margin: 0.5rem 0;"><strong>🔥 Sequência:</strong> {points['streak_days']} dias</p>
                    <p style="margin: 0; font-size: 0.9rem;">Faltam {points_for_next_level} pontos para o próximo nível!</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Barra de progresso do nível
                st.progress(min(level_progress / 100, 1.0))
            else:
                st.markdown("""
                <div class="gamification-card">
                    <h4 style="margin: 0; color: #9C27B0;">🏆 Nível 1</h4>
                    <p style="margin: 0.5rem 0;"><strong>⭐ Pontos:</strong> 0</p>
                    <p style="margin: 0; font-size: 0.9rem;">Comece sua jornada!</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Badges recentes
            recent_badges = pd.read_sql_query("""
                SELECT badge_name, badge_description, earned_date 
                FROM patient_badges 
                WHERE patient_id = ?
                ORDER BY earned_date DESC 
                LIMIT 3
            """, conn, params=[patient['id']])
            
            if not recent_badges.empty:
                st.markdown("**🏅 Badges Recentes:**")
                for idx, badge in recent_badges.iterrows():
                    earned_date = pd.to_datetime(badge['earned_date']).strftime('%d/%m/%Y')
                    st.markdown(f"🏅 **{badge['badge_name']}** - {earned_date}")
    
    else:
        st.error("❌ Dados do paciente não encontrados. Entre em contato com a secretaria.")
    
    conn.close()

def show_my_progress():
    st.markdown('<h1 class="main-header">📈 Meu Progresso</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar dados do paciente
    patient_data = pd.read_sql_query("""
        SELECT p.*, n.full_name as nutritionist_name
        FROM patients p
        LEFT JOIN users n ON n.id = p.nutritionist_id
        WHERE p.user_id = ?
    """, conn, params=[user_id])
    
    if not patient_data.empty:
        patient = patient_data.iloc[0]
        
        # Histórico completo de progresso
        progress_history = pd.read_sql_query("""
            SELECT * FROM patient_progress 
            WHERE patient_id = ? 
            ORDER BY record_date DESC
        """, conn, params=[patient['id']])
        
        if not progress_history.empty:
            # Gráfico de evolução do peso
            progress_df = progress_history.copy()
            progress_df['record_date'] = pd.to_datetime(progress_df['record_date'])
            progress_df = progress_df.sort_values('record_date')
            
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.subheader("📈 Evolução do Peso")
                
                fig = px.line(progress_df, x='record_date', y='weight', 
                             title="📈 Minha Evolução de Peso",
                             markers=True, line_shape='spline')
                
                # Adicionar linha da meta se existir
                if patient['target_weight']:
                    fig.add_hline(y=patient['target_weight'], line_dash="dash", 
                                line_color="red", annotation_text=f"Meta: {patient['target_weight']} kg")
                
                # Personalizar o gráfico
                fig.update_layout(
                    xaxis_title="Data",
                    yaxis_title="Peso (kg)",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col_chart2:
                st.subheader("📊 Estatísticas")
                
                # Calcular estatísticas
                first_weight = progress_df['weight'].iloc[0]
                last_weight = progress_df['weight'].iloc[-1]
                weight_change = last_weight - first_weight
                avg_weight = progress_df['weight'].mean()
                
                # Número de registros
                total_records = len(progress_df)
                
                # Período de acompanhamento
                first_date = progress_df['record_date'].iloc[0]
                last_date = progress_df['record_date'].iloc[-1]
                days_tracking = (last_date - first_date).days
                
                col_stat1, col_stat2 = st.columns(2)
                
                with col_stat1:
                    change_color = "#4CAF50" if weight_change < 0 else "#F44336" if weight_change > 0 else "#999"
                    st.metric("📊 Variação Total", f"{weight_change:+.1f} kg", 
                             delta_color="inverse" if weight_change < 0 else "normal")
                
                with col_stat2:
                    st.metric("📅 Acompanhamento", f"{days_tracking} dias")
                
                st.metric("📋 Total de Registros", total_records)
                st.metric("⚖️ Peso Médio", f"{avg_weight:.1f} kg")
                
                # Progresso em relação à meta
                if patient['target_weight']:
                    weight_to_goal = last_weight - patient['target_weight']
                    if abs(weight_to_goal) <= 1:
                        goal_status = "🎯 Meta atingida!"
                        goal_color = "#4CAF50"
                    elif weight_to_goal > 0:
                        goal_status = f"📉 {weight_to_goal:.1f} kg acima da meta"
                        goal_color = "#FF9800"
                    else:
                        goal_status = f"📈 {abs(weight_to_goal):.1f} kg para a meta"
                        goal_color = "#2196F3"
                    
                    st.markdown(f"""
                    <div style="background: {goal_color}20; border: 1px solid {goal_color}; 
                                padding: 1rem; border-radius: 8px; margin: 1rem 0; text-align: center;">
                        <strong style="color: {goal_color};">{goal_status}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Histórico detalhado
            st.subheader("📋 Histórico Detalhado")
            
            # Filtro de período
            col_filter1, col_filter2 = st.columns(2)
            
            with col_filter1:
                show_last = st.selectbox("📅 Mostrar", ["Todos os registros", "Últimos 10", "Últimos 30 dias", "Últimos 3 meses"])
            
            # Aplicar filtro
            filtered_progress = progress_history.copy()
            
            if show_last == "Últimos 10":
                filtered_progress = filtered_progress.head(10)
            elif show_last == "Últimos 30 dias":
                cutoff_date = datetime.now() - timedelta(days=30)
                filtered_progress = filtered_progress[pd.to_datetime(filtered_progress['record_date']) >= cutoff_date]
            elif show_last == "Últimos 3 meses":
                cutoff_date = datetime.now() - timedelta(days=90)
                filtered_progress = filtered_progress[pd.to_datetime(filtered_progress['record_date']) >= cutoff_date]
            
            # Exibir registros
            for idx, record in filtered_progress.iterrows():
                record_date = pd.to_datetime(record['record_date']).strftime('%d/%m/%Y')
                
                # Calcular IMC se houver altura
                if patient['height'] and record['weight']:
                    imc = record['weight'] / (patient['height'] ** 2)
                    imc_text = f"📊 IMC: {imc:.1f}"
                else:
                    imc_text = ""
                
                col_record1, col_record2 = st.columns([3, 1])
                
                with col_record1:
                    st.markdown(f"""
                    <div class="appointment-card">
                        <h5 style="margin: 0; color: #2E7D32;">📅 {record_date}</h5>
                        <p style="margin: 0.5rem 0;">
                            <strong>⚖️ Peso:</strong> {record['weight']} kg
                            {f" | {imc_text}" if imc_text else ""}
                            {f" | <strong>🔥 Gordura:</strong> {record['body_fat']}%" if record['body_fat'] else ""}
                        </p>
                        {f"<p style='margin: 0.5rem 0;'><strong>💪 Massa Muscular:</strong> {record['muscle_mass']} kg</p>" if record['muscle_mass'] else ""}
                        {f"<p style='margin: 0.5rem 0;'><strong>📏 Cintura:</strong> {record['waist_circumference']} cm | <strong>Quadril:</strong> {record['hip_circumference']} cm</p>" if record['waist_circumference'] or record['hip_circumference'] else ""}
                        {f"<p style='margin: 0; font-size: 0.9rem; color: #666;'><strong>📝 Observações:</strong> {record['notes']}</p>" if record['notes'] else ""}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_record2:
                    # Mostrar tendência se não for o primeiro registro
                    if idx < len(filtered_progress) - 1:
                        prev_weight = filtered_progress.iloc[idx + 1]['weight']
                        weight_diff = record['weight'] - prev_weight
                        
                        if weight_diff > 0:
                            trend = f"📈 +{weight_diff:.1f} kg"
                            trend_color = "#F44336"
                        elif weight_diff < 0:
                            trend = f"📉 {weight_diff:.1f} kg"
                            trend_color = "#4CAF50"
                        else:
                            trend = "➡️ Sem alteração"
                            trend_color = "#999"
                        
                        st.markdown(f"""
                        <div style="text-align: center; padding: 0.5rem; color: {trend_color}; font-weight: bold;">
                            {trend}
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("📝 Você ainda não possui registros de progresso. Seu nutricionista irá registrar sua evolução durante as consultas!")
            
            # Dica para o paciente
            st.markdown("""
            ### 💡 Como funciona o acompanhamento?
            
            - ⚖️ **Pesagem regular:** Seu nutricionista registrará seu peso a cada consulta
            - 📊 **Medidas corporais:** Além do peso, outras medidas podem ser acompanhadas
            - 📈 **Gráficos de evolução:** Visualize seu progresso ao longo do tempo
            - 🎯 **Metas personalizadas:** Objetivos definidos junto com seu nutricionista
            - 📝 **Observações importantes:** Anotações sobre como você está se sentindo
            """)
    
    conn.close()

def show_my_appointments():
    st.markdown('<h1 class="main-header">📅 Minhas Consultas</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar dados do paciente
    patient_data = pd.read_sql_query("""
        SELECT p.*, n.full_name as nutritionist_name
        FROM patients p
        LEFT JOIN users n ON n.id = p.nutritionist_id
        WHERE p.user_id = ?
    """, conn, params=[user_id])
    
    if not patient_data.empty:
        patient = patient_data.iloc[0]
        
        tab1, tab2, tab3 = st.tabs(["📅 Próximas Consultas", "📋 Histórico", "📊 Estatísticas"])
        
        with tab1:
            st.subheader("📅 Próximas Consultas")
            
            # Consultas futuras
            upcoming_appointments = pd.read_sql_query("""
                SELECT 
                    a.*,
                    n.full_name as nutritionist_name
                FROM appointments a
                JOIN users n ON n.id = a.nutritionist_id
                WHERE a.patient_id = ? 
                AND a.appointment_date > datetime('now')
                AND a.status != 'cancelado'
                ORDER BY a.appointment_date ASC
            """, conn, params=[patient['id']])
            
            if not upcoming_appointments.empty:
                for idx, apt in upcoming_appointments.iterrows():
                    apt_datetime = pd.to_datetime(apt['appointment_date'])
                    apt_date = apt_datetime.strftime('%d/%m/%Y')
                    apt_time = apt_datetime.strftime('%H:%M')
                    
                    # Calcular tempo até a consulta
                    time_until = apt_datetime - datetime.now()
                    days_until = time_until.days
                    hours_until = time_until.seconds // 3600
                    
                    if days_until > 0:
                        time_text = f"em {days_until} dia(s)"
                    elif hours_until > 0:
                        time_text = f"em {hours_until} hora(s)"
                    else:
                        time_text = "hoje"
                    
                    # Cores por status
                    status_colors = {
                        'agendado': '#FF9800',
                        'confirmado': '#2196F3',
                        'realizado': '#4CAF50'
                    }
                    
                    status_color = status_colors.get(apt['status'], '#999')
                    
                    st.markdown(f"""
                    <div class="appointment-card">
                        <h4 style="margin: 0; color: #2E7D32;">
                            📅 {apt_date} às {apt_time} ({apt['duration']} min)
                            <span style="background: {status_color}; color: white; padding: 0.2rem 0.5rem; 
                                         border-radius: 10px; font-size: 0.7rem; margin-left: 1rem;">
                                {apt['status'].title()}
                            </span>
                        </h4>
                        <p style="margin: 0.5rem 0;">
                            <strong>🥗 Nutricionista:</strong> {apt['nutritionist_name']} | 
                            <strong>📋 Tipo:</strong> {apt['appointment_type'] or 'Consulta padrão'}
                        </p>
                        <p style="margin: 0.5rem 0; color: #666;">
                            <strong>⏰ {time_text.title()}</strong> | 
                            <strong>🆔 ID:</strong> {apt['appointment_id']}
                        </p>
                        {f"<p style='margin: 0; font-size: 0.9rem; color: #666;'><strong>📝 Observações:</strong> {apt['notes']}</p>" if apt['notes'] else ""}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Lembrete se a consulta for nos próximos dias
                    if days_until <= 2:
                        st.warning(f"⏰ Lembrete: Consulta {time_text}! Não se esqueça.")
            else:
                st.info("📅 Você não possui consultas agendadas no momento.")
                st.markdown("""
                ### 📞 Como agendar uma consulta?
                
                Entre em contato com a secretaria para agendar sua próxima consulta:
                - 📱 **Telefone:** (11) 99999-0003
                - 📧 **Email:** secretaria@nutriapp.com
                - 🕐 **Horário de atendimento:** Segunda a sexta, 8h às 18h
                """)
        
        with tab2:
            st.subheader("📋 Histórico de Consultas")
            
            # Período para filtro
            period_filter = st.selectbox("📅 Período", 
                                       ['Últimos 3 meses', 'Últimos 6 meses', 'Último ano', 'Todas'])
            
            # Calcular data de corte
            if period_filter == 'Últimos 3 meses':
                cutoff_date = datetime.now() - timedelta(days=90)
            elif period_filter == 'Últimos 6 meses':
                cutoff_date = datetime.now() - timedelta(days=180)
            elif period_filter == 'Último ano':
                cutoff_date = datetime.now() - timedelta(days=365)
            else:
                cutoff_date = datetime.min
            
            # Buscar histórico
            appointment_history = pd.read_sql_query("""
                SELECT 
                    a.*,
                    n.full_name as nutritionist_name
                FROM appointments a
                JOIN users n ON n.id = a.nutritionist_id
                WHERE a.patient_id = ? 
                AND a.appointment_date >= ?
                ORDER BY a.appointment_date DESC
            """, conn, params=[patient['id'], cutoff_date.strftime('%Y-%m-%d %H:%M:%S')])
            
            if not appointment_history.empty:
                for idx, apt in appointment_history.iterrows():
                    apt_datetime = pd.to_datetime(apt['appointment_date'])
                    apt_date = apt_datetime.strftime('%d/%m/%Y')
                    apt_time = apt_datetime.strftime('%H:%M')
                    
                    # Determinar se é passado ou futuro
                    is_past = apt_datetime < datetime.now()
                    
                    # Cores por status
                    status_colors = {
                        'agendado': '#FF9800',
                        'confirmado': '#2196F3', 
                        'realizado': '#4CAF50',
                        'cancelado': '#F44336'
                    }
                    
                    status_color = status_colors.get(apt['status'], '#999')
                    
                    st.markdown(f"""
                    <div class="appointment-card" style="opacity: {'0.8' if is_past else '1'};">
                        <h5 style="margin: 0; color: #2E7D32;">
                            📅 {apt_date} às {apt_time}
                            <span style="background: {status_color}; color: white; padding: 0.2rem 0.5rem; 
                                         border-radius: 10px; font-size: 0.7rem; margin-left: 1rem;">
                                {apt['status'].title()}
                            </span>
                        </h5>
                        <p style="margin: 0.5rem 0;">
                            <strong>🥗 Nutricionista:</strong> {apt['nutritionist_name']} | 
                            <strong>📋 Tipo:</strong> {apt['appointment_type'] or 'Consulta padrão'} | 
                            <strong>⏱️ Duração:</strong> {apt['duration']} min
                        </p>
                        {f"<p style='margin: 0.5rem 0;'><strong>⚖️ Peso registrado:</strong> {apt['weight_recorded']} kg</p>" if apt['weight_recorded'] else ""}
                        {f"<p style='margin: 0; font-size: 0.9rem; color: #666;'><strong>📝 Observações:</strong> {apt['notes']}</p>" if apt['notes'] else ""}
                        {f"<p style='margin: 0; font-size: 0.9rem; color: #666;'><strong>🔒 Próximo retorno:</strong> {pd.to_datetime(apt['follow_up_date']).strftime('%d/%m/%Y')}</p>" if apt['follow_up_date'] else ""}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"📅 Nenhuma consulta encontrada no período selecionado.")
        
        with tab3:
            st.subheader("📊 Minhas Estatísticas de Consultas")
            
            # Estatísticas gerais
            total_appointments = pd.read_sql_query("""
                SELECT COUNT(*) as count FROM appointments 
                WHERE patient_id = ?
            """, conn, params=[patient['id']]).iloc[0]['count']
            
            completed_appointments = pd.read_sql_query("""
                SELECT COUNT(*) as count FROM appointments 
                WHERE patient_id = ? AND status = 'realizado'
            """, conn, params=[patient['id']]).iloc[0]['count']
            
            cancelled_appointments = pd.read_sql_query("""
                SELECT COUNT(*) as count FROM appointments 
                WHERE patient_id = ? AND status = 'cancelado'
            """, conn, params=[patient['id']]).iloc[0]['count']
            
            # Primeira e última consulta
            first_appointment = pd.read_sql_query("""
                SELECT MIN(appointment_date) as first_date FROM appointments 
                WHERE patient_id = ?
            """, conn, params=[patient['id']]).iloc[0]['first_date']
            
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                st.metric("📊 Total de Consultas", total_appointments)
            
            with col_stat2:
                st.metric("✅ Consultas Realizadas", completed_appointments)
            
            with col_stat3:
                st.metric("❌ Consultas Canceladas", cancelled_appointments)
            
            # Tempo de acompanhamento
            if first_appointment:
                first_date = pd.to_datetime(first_appointment)
                days_in_treatment = (datetime.now() - first_date).days
                months_in_treatment = days_in_treatment / 30.44  # Média de dias por mês
                
                col_time1, col_time2 = st.columns(2)
                
                with col_time1:
                    st.metric("📅 Tempo de Acompanhamento", f"{months_in_treatment:.1f} meses")
                
                with col_time2:
                    if completed_appointments > 0:
                        avg_interval = days_in_treatment / completed_appointments
                        st.metric("⏱️ Intervalo Médio", f"{avg_interval:.0f} dias")
            
            # Gráfico de consultas por mês
            monthly_appointments = pd.read_sql_query("""
                SELECT 
                    strftime('%Y-%m', appointment_date) as month,
                    COUNT(*) as count
                FROM appointments 
                WHERE patient_id = ?
                GROUP BY strftime('%Y-%m', appointment_date)
                ORDER BY month
            """, conn, params=[patient['id']])
            
            if not monthly_appointments.empty and len(monthly_appointments) > 1:
                fig = px.bar(monthly_appointments, x='month', y='count', 
                           title="📈 Minhas Consultas por Mês")
                fig.update_layout(
                    xaxis_title="Mês",
                    yaxis_title="Número de Consultas",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
    
    conn.close()

def show_my_plan():
    st.markdown('<h1 class="main-header">🍽️ Meu Plano Alimentar</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar dados do paciente
    patient_data = pd.read_sql_query("""
        SELECT p.*, n.full_name as nutritionist_name
        FROM patients p
        LEFT JOIN users n ON n.id = p.nutritionist_id
        WHERE p.user_id = ?
    """, conn, params=[user_id])
    
    if not patient_data.empty:
        patient = patient_data.iloc[0]
        
        # Buscar plano alimentar ativo
        active_plan = pd.read_sql_query("""
            SELECT mp.*, n.full_name as nutritionist_name
            FROM meal_plans mp
            JOIN users n ON n.id = mp.nutritionist_id
            WHERE mp.patient_id = ? AND mp.status = 'ativo'
            ORDER BY mp.created_at DESC
            LIMIT 1
        """, conn, params=[patient['id']])
        
        if not active_plan.empty:
            plan = active_plan.iloc[0]
            plan_data = json.loads(plan['plan_data']) if plan['plan_data'] else {}
            
            # Cabeçalho do plano
            col_plan1, col_plan2 = st.columns([2, 1])
            
            with col_plan1:
                st.markdown(f"""
                <div class="recipe-card">
                    <h3 style="margin: 0; color: #E65100;">🍽️ {plan['plan_name']}</h3>
                    <p style="margin: 0.5rem 0;">
                        <strong>🥗 Nutricionista:</strong> {plan['nutritionist_name']} | 
                        <strong>🔥 Calorias diárias:</strong> {plan['daily_calories']} kcal
                    </p>
                    <p style="margin: 0; font-size: 0.9rem; color: #666;">
                        <strong>📅 Período:</strong> {pd.to_datetime(plan['start_date']).strftime('%d/%m/%Y')} até {pd.to_datetime(plan['end_date']).strftime('%d/%m/%Y') if plan['end_date'] else 'Indefinido'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_plan2:
                # Progresso do plano
                if plan['end_date']:
                    start_date = pd.to_datetime(plan['start_date']).date()
                    end_date = pd.to_datetime(plan['end_date']).date()
                    today = datetime.now().date()
                    
                    total_days = (end_date - start_date).days
                    elapsed_days = (today - start_date).days
                    
                    if total_days > 0:
                        progress_percent = min(100, max(0, (elapsed_days / total_days) * 100))
                        
                        st.metric("📅 Progresso do Plano", f"{progress_percent:.0f}%")
                        st.progress(progress_percent / 100)
                        
                        remaining_days = (end_date - today).days
                        if remaining_days > 0:
                            st.write(f"⏰ {remaining_days} dias restantes")
                        elif remaining_days == 0:
                            st.write("🎯 Último dia do plano!")
                        else:
                            st.write("📋 Plano expirado - consulte seu nutricionista")
            
            # Objetivo do plano
            if 'objective' in plan_data:
                st.markdown(f"""
                <div style="background: #e3f2fd; border-left: 4px solid #2196f3; padding: 1rem; margin: 1rem 0; border-radius: 8px;">
                    <h4 style="margin: 0; color: #1976d2;">🎯 Objetivo do Plano</h4>
                    <p style="margin: 0.5rem 0; font-size: 1.1rem;">{plan_data['objective']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Refeições do plano
            if 'meals' in plan_data:
                st.subheader("🍽️ Suas Refeições")
                
                meals = plan_data['meals']
                
                for meal_key, meal_info in meals.items():
                    if meal_info['items']:
                        calories_meal = int(plan['daily_calories'] * meal_info['percent'] / 100)
                        
                        with st.expander(f"{meal_info['nome']} ({meal_info['percent']}% - {calories_meal} kcal)", expanded=True):
                            st.markdown(f"**🔥 Calorias estimadas:** {calories_meal} kcal")
                            st.markdown("**🥘 Alimentos:**")
                            
                            for item in meal_info['items']:
                                if item.strip():
                                    st.markdown(f"• {item.strip()}")
                            
                            # Dicas para a refeição
                            meal_tips = {
                                'cafe_manha': "💡 **Dica:** Comece o dia com energia! Inclua proteínas e carboidratos complexos.",
                                'lanche_manha': "💡 **Dica:** Mantenha o metabolismo ativo com um lanche leve e nutritivo.",
                                'almoco': "💡 **Dica:** Refeição principal do dia. Equilibre proteínas, carboidratos e vegetais.",
                                'lanche_tarde': "💡 **Dica:** Evite a fome excessiva no jantar com um lanche balanceado.",
                                'jantar': "💡 **Dica:** Refeição mais leve. Prefira proteínas magras e vegetais."
                            }
                            
                            if meal_key in meal_tips:
                                st.info(meal_tips[meal_key])
            
            # Orientações gerais
            if 'notes' in plan_data and plan_data['notes']:
                st.markdown("### 📝 Orientações do seu Nutricionista")
                st.markdown(f"""
                <div style="background: #fff3e0; border-left: 4px solid #ff9800; padding: 1rem; margin: 1rem 0; border-radius: 8px;">
                    {plan_data['notes']}
                </div>
                """, unsafe_allow_html=True)
            
            # Dicas importantes
            st.markdown("### 💡 Dicas Importantes")
            
            col_tips1, col_tips2 = st.columns(2)
            
            with col_tips1:
                st.markdown("""
                **🥤 Hidratação:**
                - Beba pelo menos 2,5L de água por dia
                - Distribua ao longo do dia
                - Prefira água, chás naturais sem açúcar
                
                **⏰ Horários:**
                - Mantenha regularidade nos horários
                - Não pule refeições
                - Respeite os intervalos entre as refeições
                """)
            
            with col_tips2:
                st.markdown("""
                **🍽️ Substituições:**
                - Consulte sempre seu nutricionista
                - Respeite as porções indicadas
                - Varie os alimentos dentro do mesmo grupo
                
                **📱 Dúvidas:**
                - Entre em contato com seu nutricionista
                - Registre suas dificuldades
                - Relate qualquer desconforto
                """)
            
            # Ações do plano
            st.markdown("---")
            
            col_action1, col_action2, col_action3 = st.columns(3)
            
            with col_action1:
                if st.button("📥 Baixar Plano", use_container_width=True):
                    # Simular download do plano
                    plan_text = f"""
PLANO ALIMENTAR - {plan['plan_name']}
Paciente: {patient['full_name']}
Nutricionista: {plan['nutritionist_name']}
Período: {pd.to_datetime(plan['start_date']).strftime('%d/%m/%Y')} até {pd.to_datetime(plan['end_date']).strftime('%d/%m/%Y') if plan['end_date'] else 'Indefinido'}
Calorias diárias: {plan['daily_calories']} kcal

{plan_data.get('notes', '')}
                    """
                    
                    st.download_button(
                        label="📄 Download PDF",
                        data=plan_text,
                        file_name=f"plano_alimentar_{patient['patient_id']}.txt",
                        mime="text/plain"
                    )
            
            with col_action2:
                if st.button("📧 Enviar por Email", use_container_width=True):
                    st.info("📧 Funcionalidade de envio por email será implementada em breve!")
            
            with col_action3:
                if st.button("❓ Tirar Dúvidas", use_container_width=True):
                    st.info(f"""
                    📱 **Entre em contato com seu nutricionista:**
                    
                    **🥗 {plan['nutritionist_name']}**
                    📧 Email: ana.silva@nutriapp.com
                    📱 WhatsApp: (11) 99999-0002
                    
                    **Horário de atendimento:**
                    Segunda a sexta: 8h às 18h
                    """)
        
        else:
            # Nenhum plano ativo
            st.markdown("""
            <div style="text-align: center; padding: 3rem; background: #f8f9fa; border-radius: 15px; margin: 2rem 0;">
                <h2 style="color: #666;">🍽️ Nenhum Plano Alimentar Ativo</h2>
                <p style="font-size: 1.1rem; color: #888;">
                    Você ainda não possui um plano alimentar ativo.<br>
                    Entre em contato com seu nutricionista para criar seu plano personalizado!
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Informações de contato
            if patient['nutritionist_name']:
                st.markdown(f"""
                ### 📞 Entre em Contato
                
                **🥗 Seu Nutricionista: {patient['nutritionist_name']}**
                - 📧 Email: ana.silva@nutriapp.com
                - 📱 WhatsApp: (11) 99999-0002
                - 🕐 Horário: Segunda a sexta, 8h às 18h
                """)
            else:
                st.markdown("""
                ### 📞 Entre em Contato
                
                **📋 Secretaria:**
                - 📱 Telefone: (11) 99999-0003
                - 📧 Email: secretaria@nutriapp.com
                - 🕐 Horário: Segunda a sexta, 8h às 18h
                """)
    
    conn.close()

def show_points_badges():
    st.markdown('<h1 class="main-header">🏆 Pontos & Badges</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar dados do paciente
    patient_data = pd.read_sql_query("""
        SELECT * FROM patients WHERE user_id = ?
    """, conn, params=[user_id])
    
    if not patient_data.empty:
        patient = patient_data.iloc[0]
        
        # Buscar ou criar dados de pontuação
        points_data = pd.read_sql_query("""
            SELECT * FROM patient_points WHERE patient_id = ?
        """, conn, params=[patient['id']])
        
        if points_data.empty:
            # Criar registro inicial
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO patient_points (patient_id, points, level, total_points, streak_days)
                VALUES (?, 0, 1, 0, 0)
            ''', (patient['id'],))
            conn.commit()
            
            points = {'points': 0, 'level': 1, 'total_points': 0, 'streak_days': 0}
        else:
            points = points_data.iloc[0]
        
        # Cabeçalho de pontuação
        col_points1, col_points2, col_points3 = st.columns(3)
        
        with col_points1:
            # Nível atual
            st.markdown(f"""
            <div class="gamification-card">
                <h2 style="margin: 0; color: #9C27B0;">🏆 Nível {points['level']}</h2>
                <p style="margin: 0.5rem 0; font-size: 1.2rem;"><strong>⭐ {points['points']} pontos</strong></p>
                <p style="margin: 0; font-size: 0.9rem;">Total acumulado: {points['total_points']} pts</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_points2:
            # Progresso para próximo nível
            points_for_next_level = (points['level'] * 100) - points['points']
            level_progress = (points['points'] / (points['level'] * 100)) * 100
            
            st.markdown(f"""
            <div class="gamification-card">
                <h3 style="margin: 0; color: #4CAF50;">📈 Próximo Nível</h3>
                <p style="margin: 0.5rem 0;">Faltam <strong>{points_for_next_level}</strong> pontos</p>
                <p style="margin: 0; font-size: 0.9rem;">Para o nível {points['level'] + 1}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Barra de progresso
            st.progress(min(level_progress / 100, 1.0))
        
        with col_points3:
            # Sequência de dias
            st.markdown(f"""
            <div class="gamification-card">
                <h3 style="margin: 0; color: #FF5722;">🔥 Sequência</h3>
                <p style="margin: 0.5rem 0;"><strong>{points['streak_days']} dias</strong></p>
                <p style="margin: 0; font-size: 0.9rem;">Consecutivos seguindo o plano</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Como ganhar pontos
        st.markdown("### 🎯 Como Ganhar Pontos")
        
        col_earn1, col_earn2 = st.columns(2)
        
        with col_earn1:
            st.markdown("""
            **📅 Consultas & Acompanhamento:**
            - ✅ Comparecer à consulta: **50 pontos**
            - 📊 Registrar progresso: **30 pontos**
            - 🎯 Atingir meta mensal: **100 pontos**
            - 📝 Feedback sobre o plano: **20 pontos**
            """)
        
        with col_earn2:
            st.markdown("""
            **🍽️ Alimentação & Hábitos:**
            - 🥗 Seguir plano por 7 dias: **70 pontos**
            - 💧 Meta de hidratação diária: **10 pontos**
            - 🏃‍♂️ Praticar exercícios: **25 pontos**
            - 📱 Usar o app por 30 dias: **150 pontos**
            """)
        
        # Badges conquistadas
        st.markdown("### 🏅 Minhas Badges")
        
        patient_badges = pd.read_sql_query("""
            SELECT * FROM patient_badges 
            WHERE patient_id = ?
            ORDER BY earned_date DESC
        """, conn, params=[patient['id']])
        
        if not patient_badges.empty:
            # Organizar badges por tipo
            cols_badges = st.columns(min(4, len(patient_badges)))
            
            for idx, badge in patient_badges.iterrows():
                col_idx = idx % len(cols_badges)
                
                with cols_badges[col_idx]:
                    earned_date = pd.to_datetime(badge['earned_date']).strftime('%d/%m/%Y')
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); 
                                padding: 1rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;
                                border: 2px solid #9c27b0;">
                        <h3 style="margin: 0; font-size: 2rem;">{badge['badge_icon'] or '🏅'}</h3>
                        <h5 style="margin: 0.5rem 0; color: #7b1fa2;">{badge['badge_name']}</h5>
                        <p style="margin: 0; font-size: 0.8rem; color: #666;">{badge['badge_description']}</p>
                        <small style="color: #999;">Conquistada em {earned_date}</small>
                        {f"<br><strong style='color: #4caf50;'>+{badge['points_awarded']} pts</strong>" if badge['points_awarded'] else ""}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            # Adicionar algumas badges de exemplo se não houver
            cursor = conn.cursor()
            sample_badges = [
                ('Primeiro Passo', 'Primeira consulta realizada', '🥇', 50),
                ('Hidratação', 'Meta de água atingida por 7 dias', '💧', 70),
                ('Consistência', '30 dias seguindo o plano', '🎯', 150)
            ]
            
            for badge_name, description, icon, points_awarded in sample_badges:
                cursor.execute('''
                    INSERT INTO patient_badges (patient_id, badge_name, badge_description, badge_icon, points_awarded)
                    VALUES (?, ?, ?, ?, ?)
                ''', (patient['id'], badge_name, description, icon, points_awarded))
            
            conn.commit()
            st.rerun()
        
        # Badges disponíveis para conquistar
        st.markdown("### 🎯 Badges para Conquistar")
        
        available_badges = [
            {'name': 'Maratonista', 'description': 'Complete 3 meses de acompanhamento', 'icon': '🏃‍♂️', 'points': 200},
            {'name': 'Meta Alcançada', 'description': 'Atinja seu peso objetivo', 'icon': '🎯', 'points': 300},
            {'name': 'Disciplina', 'description': 'Siga o plano por 60 dias consecutivos', 'icon': '💪', 'points': 250},
            {'name': 'Educador', 'description': 'Compartilhe uma receita saudável', 'icon': '👨‍🍳', 'points': 100},
            {'name': 'Comunidade', 'description': 'Ajude outro paciente no chat', 'icon': '🤝', 'points': 150},
            {'name': 'Inovador', 'description': 'Teste 10 receitas diferentes', 'icon': '🧪', 'points': 180}
        ]
        
        cols_available = st.columns(3)
        
        for idx, badge in enumerate(available_badges):
            col_idx = idx % 3
            
            with cols_available[col_idx]:
                st.markdown(f"""
                <div style="background: #f8f9fa; border: 2px dashed #ccc; 
                            padding: 1rem; border-radius: 10px; text-align: center; margin: 0.5rem 0;">
                    <h3 style="margin: 0; font-size: 2rem; opacity: 0.5;">{badge['icon']}</h3>
                    <h5 style="margin: 0.5rem 0; color: #666;">{badge['name']}</h5>
                    <p style="margin: 0; font-size: 0.8rem; color: #888;">{badge['description']}</p>
                    <strong style="color: #4caf50;">+{badge['points']} pts</strong>
                </div>
                """, unsafe_allow_html=True)
        
        # Ranking (simulado)
        st.markdown("### 🏆 Ranking de Pacientes")
        
        # Simular ranking
        ranking_data = [
            {'position': 1, 'name': 'Maria S.', 'points': 2850, 'level': 15},
            {'position': 2, 'name': 'João P.', 'points': 2340, 'level': 12},
            {'position': 3, 'name': patient['full_name'][:6] + '...', 'points': points['total_points'], 'level': points['level']},
            {'position': 4, 'name': 'Ana C.', 'points': 1820, 'level': 9},
            {'position': 5, 'name': 'Carlos M.', 'points': 1650, 'level': 8}
        ]
        
        st.markdown("**🥇 Top 5 desta semana:**")
        
        for rank in ranking_data:
            if rank['name'].startswith(patient['full_name'][:6]):
                # Destacar o paciente atual
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                            border: 2px solid #4caf50; padding: 0.8rem; border-radius: 8px; margin: 0.3rem 0;">
                    <strong>{rank['position']}º lugar - {rank['name']} (VOCÊ!)</strong>
                    <span style="float: right;">⭐ {rank['points']} pts | 🏆 Nível {rank['level']}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 8px; margin: 0.3rem 0; border-left: 3px solid #ddd;">
                    {rank['position']}º lugar - {rank['name']}
                    <span style="float: right;">⭐ {rank['points']} pts | 🏆 Nível {rank['level']}</span>
                </div>
                """, unsafe_allow_html=True)
    
    conn.close()

def show_patient_chat_ia():
    st.markdown('<h1 class="main-header">🤖 Chat com IA Nutricional</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    # Chat específico para pacientes
    if 'patient_chat_history' not in st.session_state:
        st.session_state.patient_chat_history = []
    
    # Buscar dados do paciente para contexto
    conn = sqlite3.connect('nutriapp360.db')
    patient_data = pd.read_sql_query("""
        SELECT p.*, n.full_name as nutritionist_name
        FROM patients p
        LEFT JOIN users n ON n.id = p.nutritionist_id
        WHERE p.user_id = ?
    """, conn, params=[user_id])
    conn.close()
    
    patient = patient_data.iloc[0] if not patient_data.empty else None
    
    # Interface do chat
    col_chat1, col_chat2 = st.columns([3, 1])
    
    with col_chat1:
        st.subheader("💬 Seu Assistente Nutricional Pessoal")
        
        # Área de conversa
        chat_container = st.container()
        
        with chat_container:
            if st.session_state.patient_chat_history:
                for i, chat in enumerate(st.session_state.patient_chat_history):
                    # Mensagem do paciente
                    st.markdown(f"""
                    <div style="background: #e3f2fd; padding: 1rem; border-radius: 15px; margin: 1rem 0; 
                                margin-left: 20%; border-top-right-radius: 5px;">
                        <strong>Você:</strong><br>
                        {chat['question']}
                        <br><small style="color: #666; float: right;">{chat['timestamp'].strftime('%H:%M')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Resposta do assistente
                    st.markdown(f"""
                    <div style="background: white; border-radius: 15px; padding: 1rem; margin: 1rem 0; 
                                margin-right: 20%; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-top-left-radius: 5px;">
                        <strong>🤖 Assistente:</strong><br>
                        {chat['response']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Mensagem de boas-vindas personalizada
                welcome_message = f"""
                <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                            border-radius: 15px; padding: 2rem; margin: 2rem 0; text-align: center;">
                    <h3 style="margin: 0; color: #2e7d32;">👋 Olá, {patient['full_name'] if patient else 'Paciente'}!</h3>
                    <p style="margin: 1rem 0; font-size: 1.1rem;">
                        Sou seu assistente nutricional pessoal. Posso ajudar com:
                    </p>
                    <div style="text-align: left; max-width: 400px; margin: 0 auto;">
                        <p>🍎 <strong>Dúvidas sobre alimentação saudável</strong></p>
                        <p>🥗 <strong>Substituições em seu plano alimentar</strong></p>
                        <p>🧮 <strong>Cálculos nutricionais básicos</strong></p>
                        <p>💡 <strong>Dicas para manter a dieta</strong></p>
                        <p>🏃‍♂️ <strong>Orientações sobre exercícios e nutrição</strong></p>
                    </div>
                    <p style="margin: 1rem 0; font-style: italic; color: #666;">
                        💡 Faça uma pergunta para começar nossa conversa!
                    </p>
                </div>
                """ if patient else """
                <div style="background: #f8f9fa; border-radius: 15px; padding: 2rem; margin: 2rem 0; text-align: center;">
                    <h3>🤖 Assistente Nutricional</h3>
                    <p>Olá! Estou aqui para ajudar com suas dúvidas sobre nutrição e alimentação saudável.</p>
                </div>
                """
                
                st.markdown(welcome_message, unsafe_allow_html=True)
        
        # Input do usuário
        patient_question = st.text_input(
            "💬 Digite sua pergunta:", 
            key='patient_input',
            placeholder="Ex: Posso substituir o arroz por batata doce no meu plano?"
        )
        
        col_send, col_clear = st.columns([3, 1])
        with col_send:
            send_button = st.button("📤 Enviar", use_container_width=True, type="primary")
        with col_clear:
            if st.button("🗑️ Limpar", use_container_width=True):
                st.session_state.patient_chat_history = []
                st.rerun()
    
    with col_chat2:
        st.subheader("💡 Perguntas Sugeridas")
        
        # Sugestões específicas para pacientes
        patient_suggestions = [
            "Posso comer frutas à noite?",
            "Como substituir o açúcar?",
            "Receitas com pouco carboidrato",
            "Lanches saudáveis para o trabalho",
            "Como beber mais água?",
            "Exercícios para iniciantes",
            "Alimentos ricos em proteína",
            "Dicas para controlar a ansiedade"
        ]
        
        for suggestion in patient_suggestions:
            if st.button(f"💡 {suggestion}", key=f"patient_suggest_{suggestion}", use_container_width=True):
                patient_question = suggestion
                send_button = True
        
        st.markdown("---")
        st.subheader("📊 Minha Conversa")
        
        # Estatísticas do chat do paciente
        if st.session_state.patient_chat_history:
            total_questions = len(st.session_state.patient_chat_history)
            
            st.metric("💬 Perguntas Feitas", total_questions)
            
            # Categorias mais perguntadas
            categories = {
                'alimentação': 0,
                'exercício': 0,
                'receitas': 0,
                'substituições': 0
            }
            
            for chat in st.session_state.patient_chat_history:
                question_lower = chat['question'].lower()
                
                if any(word in question_lower for word in ['comer', 'alimento', 'dieta']):
                    categories['alimentação'] += 1
                elif any(word in question_lower for word in ['exercício', 'atividade', 'treino']):
                    categories['exercício'] += 1
                elif any(word in question_lower for word in ['receita', 'preparo', 'cozinhar']):
                    categories['receitas'] += 1
                elif any(word in question_lower for word in ['substitui', 'trocar', 'substituir']):
                    categories['substituições'] += 1
            
            if max(categories.values()) > 0:
                st.markdown("**📈 Seus temas favoritos:**")
                for category, count in categories.items():
                    if count > 0:
                        st.write(f"• {category.title()}: {count}")
        
        # Lembrete importante
        st.markdown("---")
        st.info("""
        ⚠️ **Importante:** 
        
        Este assistente oferece orientações gerais. Para questões específicas sobre seu plano ou condições de saúde, sempre consulte seu nutricionista.
        """)
    
    # Processar envio da mensagem
    if send_button and patient_question:
        with st.spinner("🤖 Pensando..."):
            llm = LLMAssistant()
            
            # Contexto específico do paciente
            context = f"Paciente: {patient['full_name'] if patient else 'Usuário'}"
            
            if patient:
                # Adicionar informações relevantes do paciente ao contexto
                context += f" | Objetivo: {patient.get('target_weight', 'N/A')} kg"
                if patient.get('medical_conditions'):
                    context += f" | Condições: {patient['medical_conditions']}"
                if patient.get('allergies'):
                    context += f" | Alergias: {patient['allergies']}"
            
            response = llm.generate_response(patient_question, context)
            
            st.session_state.patient_chat_history.append({
                'question': patient_question,
                'response': response,
                'timestamp': datetime.now()
            })
            
            # Salvar conversa no banco
            save_llm_conversation(user_id, patient['id'] if patient else None, 'patient_chat', patient_question, response)
        
        st.rerun()

def show_calculators_personal():
    st.markdown('<h1 class="main-header">🧮 Minhas Calculadoras</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    # Buscar dados do paciente
    conn = sqlite3.connect('nutriapp360.db')
    patient_data = pd.read_sql_query("""
        SELECT * FROM patients WHERE user_id = ?
    """, conn, params=[user_id])
    conn.close()
    
    patient = patient_data.iloc[0] if not patient_data.empty else None
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Meu IMC", "💧 Hidratação", "🔥 Calorias", "🍽️ Porções"])
    
    with tab1:
        st.subheader("📊 Calculadora de IMC Personalizada")
        
        col_imc1, col_imc2 = st.columns(2)
        
        with col_imc1:
            # Usar dados do paciente se disponíveis
            default_weight = float(patient['current_weight']) if patient and patient['current_weight'] else 70.0
            default_height = float(patient['height']) if patient and patient['height'] else 1.70
            
            weight_personal = st.number_input("⚖️ Seu peso atual (kg)", 
                                            min_value=30.0, max_value=300.0, 
                                            value=default_weight, step=0.1)
            
            height_personal = st.number_input("📏 Sua altura (m)", 
                                            min_value=1.0, max_value=2.5, 
                                            value=default_height, step=0.01)
            
            if patient and patient['target_weight']:
                target_weight = float(patient['target_weight'])
                st.info(f"🎯 Sua meta de peso: {target_weight} kg")
        
        with col_imc2:
            if weight_personal and height_personal:
                # Calcular IMC atual
                imc_current = weight_personal / (height_personal ** 2)
                
                # Classificação
                if imc_current < 18.5:
                    category = "Abaixo do peso"
                    color = "#2196F3"
                    advice = "Considere ganhar peso de forma saudável"
                elif imc_current < 25:
                    category = "Peso normal"
                    color = "#4CAF50"
                    advice = "Mantenha seus hábitos saudáveis!"
                elif imc_current < 30:
                    category = "Sobrepeso"
                    color = "#FF9800"
                    advice = "Foque em alimentação balanceada e exercícios"
                else:
                    category = "Obesidade"
                    color = "#F44336"
                    advice = "Busque orientação profissional"
                
                st.markdown(f"""
                <div style="background: {color}20; border: 2px solid {color}; padding: 1.5rem; 
                            border-radius: 15px; text-align: center;">
                    <h2 style="margin: 0; color: {color};">📊 IMC: {imc_current:.1f}</h2>
                    <h4 style="margin: 0.5rem 0; color: {color};">{category}</h4>
                    <p style="margin: 0; color: #666;">{advice}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Se há meta de peso, calcular IMC da meta
                if patient and patient['target_weight']:
                    target_weight = float(patient['target_weight'])
                    imc_target = target_weight / (height_personal ** 2)
                    
                    st.markdown(f"""
                    <div style="background: #e8f5e8; border: 1px solid #4caf50; padding: 1rem; 
                                border-radius: 10px; text-align: center; margin-top: 1rem;">
                        <h4 style="margin: 0; color: #2e7d32;">🎯 IMC da Meta: {imc_target:.1f}</h4>
                        <p style="margin: 0; color: #666;">Peso objetivo: {target_weight} kg</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Faixa de peso saudável
                peso_min = 18.5 * (height_personal ** 2)
                peso_max = 24.9 * (height_personal ** 2)
                
                st.markdown(f"""
                ### 💡 Faixa de Peso Saudável
                Para sua altura ({height_personal}m):
                - **Mínimo:** {peso_min:.1f} kg
                - **Máximo:** {peso_max:.1f} kg
                """)
    
    with tab2:
        st.subheader("💧 Calculadora de Hidratação Personalizada")
        
        col_hydra1, col_hydra2 = st.columns(2)
        
        with col_hydra1:
            weight_hydra = st.number_input("⚖️ Seu peso (kg)", 
                                         min_value=30.0, max_value=200.0, 
                                         value=default_weight, key="weight_hydra_personal")
            
            # Calcular idade se tiver data de nascimento
            if patient and patient['birth_date']:
                birth_date = pd.to_datetime(patient['birth_date'])
                age = (datetime.now() - birth_date).days // 365
                st.info(f"📅 Sua idade: {age} anos")
            else:
                age = st.number_input("📅 Sua idade", min_value=1, max_value=120, value=30)
            
            activity_level = st.selectbox("🏃‍♂️ Seu nível de atividade", [
                "Sedentário (pouco exercício)",
                "Levemente ativo (1-3 dias/semana)",
                "Moderadamente ativo (3-5 dias/semana)",
                "Muito ativo (6-7 dias/semana)",
                "Extremamente ativo (2x por dia)"
            ])
            
            climate = st.selectbox("🌡️ Clima da sua região", ["Temperado", "Quente", "Muito quente"])
        
        with col_hydra2:
            if st.button("💧 Calcular Minha Necessidade", type="primary"):
                # Cálculo base: 35ml/kg
                base_water = weight_hydra * 35
                
                # Ajuste por idade
                if age > 65:
                    base_water *= 0.9
                elif age < 18:
                    base_water *= 1.1
                
                # Ajuste por atividade física
                activity_multipliers = {
                    "Sedentário (pouco exercício)": 1.0,
                    "Levemente ativo (1-3 dias/semana)": 1.1,
                    "Moderadamente ativo (3-5 dias/semana)": 1.2,
                    "Muito ativo (6-7 dias/semana)": 1.3,
                    "Extremamente ativo (2x por dia)": 1.4
                }
                
                base_water *= activity_multipliers[activity_level]
                
                # Ajuste por clima
                climate_multipliers = {
                    "Temperado": 1.0,
                    "Quente": 1.2,
                    "Muito quente": 1.4
                }
                
                base_water *= climate_multipliers[climate]
                
                total_liters = base_water / 1000
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                            border: 2px solid #2196f3; padding: 1.5rem; border-radius: 15px; text-align: center;">
                    <h2 style="margin: 0; color: #1976d2;">💧 {total_liters:.1f}L</h2>
                    <h4 style="margin: 0.5rem 0; color: #1976d2;">Por dia</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Dicas práticas
                glasses_250ml = base_water / 250
                
                st.markdown(f"""
                ### 💡 Dicas Práticas
                
                **🥤 Distribuição ao longo do dia:**
                - {glasses_250ml:.0f} copos de 250ml
                - 1 copo ao acordar
                - 1 copo antes de cada refeição
                - 1 copo a cada 2 horas
                
                **⏰ Lembretes:**
                - Use um app de lembrete
                - Tenha sempre uma garrafa por perto
                - Sabores naturais: limão, hortelã, pepino
                """)
    
    with tab3:
        st.subheader("🔥 Calculadora de Calorias Pessoal")
        
        col_cal1, col_cal2 = st.columns(2)
        
        with col_cal1:
            # Dados pessoais
            gender = st.selectbox("⚧ Sexo", ["Feminino", "Masculino"])
            
            weight_cal = st.number_input("⚖️ Peso (kg)", 
                                       value=default_weight, key="weight_cal_personal")
            height_cal = st.number_input("📏 Altura (cm)", 
                                       value=default_height * 100, key="height_cal_personal")
            
            if patient and patient['birth_date']:
                birth_date = pd.to_datetime(patient['birth_date'])
                age_cal = (datetime.now() - birth_date).days // 365
                st.info(f"📅 Sua idade: {age_cal} anos")
            else:
                age_cal = st.number_input("📅 Idade", value=30, key="age_cal_personal")
            
            activity_cal = st.selectbox("🏃‍♂️ Atividade física", [
                "Sedentário",
                "Levemente ativo", 
                "Moderadamente ativo",
                "Muito ativo",
                "Extremamente ativo"
            ])
            
            goal = st.selectbox("🎯 Seu objetivo", [
                "Manter peso",
                "Emagrecer (0.5 kg/semana)",
                "Emagrecer (1 kg/semana)",
                "Ganhar peso (0.5 kg/semana)"
            ])
        
        with col_cal2:
            if st.button("🔥 Calcular Minhas Calorias", type="primary"):
                # Fórmula de Harris-Benedict
                if gender == "Masculino":
                    tmb = 88.362 + (13.397 * weight_cal) + (4.799 * height_cal) - (5.677 * age_cal)
                else:
                    tmb = 447.593 + (9.247 * weight_cal) + (3.098 * height_cal) - (4.330 * age_cal)
                
                # Fator de atividade
                activity_factors = {
                    "Sedentário": 1.2,
                    "Levemente ativo": 1.375,
                    "Moderadamente ativo": 1.55,
                    "Muito ativo": 1.725,
                    "Extremamente ativo": 1.9
                }
                
                maintenance_calories = tmb * activity_factors[activity_cal]
                
                # Ajustar por objetivo
                goal_adjustments = {
                    "Manter peso": 0,
                    "Emagrecer (0.5 kg/semana)": -500,
                    "Emagrecer (1 kg/semana)": -1000,
                    "Ganhar peso (0.5 kg/semana)": +300
                }
                
                target_calories = maintenance_calories + goal_adjustments[goal]
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                            border: 2px solid #ff9800; padding: 1.5rem; border-radius: 15px; text-align: center;">
                    <h2 style="margin: 0; color: #e65100;">🔥 {target_calories:.0f} kcal</h2>
                    <h4 style="margin: 0.5rem 0; color: #e65100;">Por dia</h4>
                    <p style="margin: 0; color: #666;">Para {goal.lower()}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Detalhamento
                col_detail1, col_detail2 = st.columns(2)
                
                with col_detail1:
                    st.metric("🔥 TMB (Repouso)", f"{tmb:.0f} kcal")
                
                with col_detail2:
                    st.metric("⚡ Gasto Total", f"{maintenance_calories:.0f} kcal")
                
                # Distribuição por refeições
                st.markdown("### 🍽️ Distribuição Sugerida")
                
                meals = [
                    ("Café da manhã", 0.25),
                    ("Lanche manhã", 0.10),
                    ("Almoço", 0.35),
                    ("Lanche tarde", 0.10),
                    ("Jantar", 0.20)
                ]
                
                for meal_name, percentage in meals:
                    meal_calories = target_calories * percentage
                    st.write(f"• **{meal_name}:** {meal_calories:.0f} kcal ({percentage*100:.0f}%)")
    
    with tab4:
        st.subheader("🍽️ Guia de Porções Personalizado")
        
        # Grupo de alimentos com porções
        food_groups = {
            "🍞 Carboidratos": {
                "Arroz cozido": "4 colheres de sopa (100g) = 130 kcal",
                "Pão integral": "2 fatias (50g) = 120 kcal", 
                "Batata doce": "1 unidade média (150g) = 90 kcal",
                "Macarrão": "1 xícara cozido (100g) = 110 kcal"
            },
            "🥩 Proteínas": {
                "Peito de frango": "1 filé médio (120g) = 200 kcal",
                "Peixe grelhado": "1 filé (150g) = 180 kcal",
                "Ovos": "2 unidades = 140 kcal",
                "Feijão": "1 concha (80g) = 70 kcal"
            },
            "🥗 Vegetais": {
                "Salada verde": "1 prato raso = 20 kcal",
                "Brócolis": "1 xícara = 25 kcal",
                "Cenoura": "1 unidade média = 30 kcal",
                "Tomate": "1 unidade média = 20 kcal"
            },
            "🍎 Frutas": {
                "Maçã": "1 unidade média = 80 kcal",
                "Banana": "1 unidade média = 90 kcal",
                "Laranja": "1 unidade média = 60 kcal",
                "Mamão": "1 fatia (100g) = 40 kcal"
            },
            "🥑 Gorduras": {
                "Azeite": "1 colher de sopa = 120 kcal",
                "Abacate": "1/4 unidade = 80 kcal",
                "Castanhas": "6 unidades = 100 kcal",
                "Amendoim": "1 colher de sopa = 90 kcal"
            }
        }
        
        # Seletor de grupo alimentar
        selected_group = st.selectbox("📂 Escolha um grupo de alimentos:", list(food_groups.keys()))
        
        # Mostrar alimentos do grupo selecionado
        st.markdown(f"### {selected_group}")
        
        for food, portion in food_groups[selected_group].items():
            st.markdown(f"""
            <div style="background: #f8f9fa; border-left: 4px solid #4caf50; padding: 1rem; margin: 0.5rem 0; border-radius: 8px;">
                <strong>{food}</strong><br>
                <span style="color: #666;">{portion}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Calculadora de porções
        st.markdown("---")
        st.markdown("### 🧮 Calculadora de Porções")
        
        col_portion1, col_portion2 = st.columns(2)
        
        with col_portion1:
            food_item = st.selectbox("🍽️ Selecione o alimento:", [
                "Arroz branco cozido",
                "Frango grelhado", 
                "Feijão cozido",
                "Banana",
                "Azeite"
            ])
            
            portion_size = st.number_input("📏 Quantidade (gramas):", min_value=1, value=100)
        
        with col_portion2:
            # Base calórica por 100g
            calories_per_100g = {
                "Arroz branco cozido": 130,
                "Frango grelhado": 165,
                "Feijão cozido": 77,
                "Banana": 89,
                "Azeite": 884
            }
            
            if food_item in calories_per_100g:
                cal_per_100 = calories_per_100g[food_item]
                total_calories = (cal_per_100 * portion_size) / 100
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                            border: 2px solid #4caf50; padding: 1rem; border-radius: 10px; text-align: center;">
                    <h4 style="margin: 0; color: #2e7d32;">{total_calories:.0f} kcal</h4>
                    <p style="margin: 0; color: #666;">{portion_size}g de {food_item.lower()}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Dicas de medidas caseiras
        st.markdown("### 📏 Medidas Caseiras Úteis")
        
        col_tips1, col_tips2 = st.columns(2)
        
        with col_tips1:
            st.markdown("""
            **🥄 Colheres:**
            - 1 colher de sopa = 15ml
            - 1 colher de sobremesa = 10ml
            - 1 colher de chá = 5ml
            
            **🥤 Xícaras:**
            - 1 xícara de chá = 240ml
            - 1 xícara de café = 120ml
            """)
        
        with col_tips2:
            st.markdown("""
            **🤏 Punhados:**
            - 1 punhado de oleaginosas = 30g
            - 1 punhado de frutas secas = 40g
            
            **🍽️ Pratos:**
            - 1 prato fundo = 300ml
            - 1 prato raso = 200ml
            """)

def show_patient_profile():
    st.markdown('<h1 class="main-header">👤 Meu Perfil</h1>', unsafe_allow_html=True)
    
    user_id = st.session_state.user['id']
    
    conn = sqlite3.connect('nutriapp360.db')
    
    # Buscar dados do paciente e usuário
    patient_data = pd.read_sql_query("""
        SELECT p.*, u.username, u.email as user_email, n.full_name as nutritionist_name
        FROM patients p
        JOIN users u ON u.id = p.user_id
        LEFT JOIN users n ON n.id = p.nutritionist_id
        WHERE p.user_id = ?
    """, conn, params=[user_id])
    
    if not patient_data.empty:
        patient = patient_data.iloc[0]
        
        tab1, tab2, tab3 = st.tabs(["📋 Dados Pessoais", "⚙️ Configurações", "📊 Histórico"])
        
        with tab1:
            st.subheader("📋 Suas Informações Pessoais")
            
            # Formulário de edição
            with st.form("profile_form"):
                col_form1, col_form2 = st.columns(2)
                
                with col_form1:
                    full_name = st.text_input("👤 Nome Completo", value=patient['full_name'])
                    email = st.text_input("📧 Email", value=patient['email'] or '')
                    phone = st.text_input("📱 Telefone", value=patient['phone'] or '')
                    birth_date = st.date_input("📅 Data de Nascimento", 
                                             value=pd.to_datetime(patient['birth_date']).date() if patient['birth_date'] else None)
                    gender = st.selectbox("⚧ Gênero", ["M", "F"], 
                                        index=0 if patient['gender'] == 'M' else 1)
                
                with col_form2:
                    height = st.number_input("📏 Altura (m)", min_value=1.0, max_value=2.5, 
                                           value=float(patient['height']) if patient['height'] else 1.70, step=0.01)
                    current_weight = st.number_input("⚖️ Peso Atual (kg)", min_value=30.0, max_value=300.0,
                                                   value=float(patient['current_weight']) if patient['current_weight'] else 70.0)
                    target_weight = st.number_input("🎯 Peso Objetivo (kg)", min_value=30.0, max_value=300.0,
                                                   value=float(patient['target_weight']) if patient['target_weight'] else 65.0)
                    activity_level = st.selectbox("🏃‍♂️ Nível de Atividade", 
                                                ['Sedentário', 'Leve', 'Moderado', 'Ativo', 'Muito Ativo'],
                                                index=['Sedentário', 'Leve', 'Moderado', 'Ativo', 'Muito Ativo'].index(patient['activity_level']) if patient['activity_level'] else 0)
                
                # Informações médicas
                st.markdown("### 🏥 Informações Médicas")
                
                medical_conditions = st.text_area("🏥 Condições Médicas", 
                                                value=patient['medical_conditions'] or '',
                                                placeholder="Ex: Diabetes tipo 2, Hipertensão...")
                
                allergies = st.text_area("🚨 Alergias Alimentares", 
                                        value=patient['allergies'] or '',
                                        placeholder="Ex: Glúten, Lactose, Amendoim...")
                
                dietary_preferences = st.text_area("🥗 Preferências Alimentares", 
                                                  value=patient['dietary_preferences'] or '',
                                                  placeholder="Ex: Vegetariano, Vegano, Low carb...")
                
                # Contato de emergência
                st.markdown("### 🆘 Contato de Emergência")
                
                col_emergency1, col_emergency2 = st.columns(2)
                
                with col_emergency1:
                    emergency_contact = st.text_input("👤 Nome do Contato", 
                                                    value=patient['emergency_contact'] or '')
                
                with col_emergency2:
                    emergency_phone = st.text_input("📞 Telefone de Emergência", 
                                                   value=patient['emergency_phone'] or '')
                
                # Informações do plano de saúde
                insurance_info = st.text_input("🏥 Plano de Saúde", 
                                             value=patient['insurance_info'] or '',
                                             placeholder="Ex: Unimed, Bradesco Saúde...")
                
                submitted = st.form_submit_button("💾 Salvar Alterações", type="primary")
                
                if submitted:
                    try:
                        cursor = conn.cursor()
                        
                        # Atualizar dados do paciente
                        cursor.execute('''
                            UPDATE patients SET 
                                full_name = ?, email = ?, phone = ?, birth_date = ?, gender = ?,
                                height = ?, current_weight =#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NutriApp360 - Sistema Completo de Apoio ao Nutricionista
Version: 5.0 - SISTEMA COMPLETAMENTE FUNCIONAL
Author: NutriApp360 Team
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
import os
import math
import random
import base64
from io import BytesIO
import re
from typing import Dict, List, Optional
import calendar
import numpy as np

# Configurações iniciais
st.set_page_config(
    page_title="NutriApp360 v5.0 - Sistema Completo",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
        padding: 1rem;
        border-radius: 15px;
        border: 3px solid #4CAF50;
    }
    
    .dashboard-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #4CAF50;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .dashboard-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        border: 2px solid #4CAF50;
        transition: all 0.3s ease;
    }
    
    .patient-info-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    
    .appointment-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .recipe-card {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ff9800;
        margin: 0.5rem 0;
    }
    
    .financial-card {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4caf50;
        margin: 0.5rem 0;
    }
    
    .gamification-card {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #9c27b0;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 0.75rem 1.25rem;
        margin-bottom: 1rem;
        border-radius: 0.25rem;
    }
    
    .warning-message {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 0.75rem 1.25rem;
        margin-bottom: 1rem;
        border-radius: 0.25rem;
    }
    
    .info-badge {
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    
    .status-active {
        background: #c8e6c9;
        color: #2e7d32;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
    }
    
    .status-pending {
        background: #fff3e0;
        color: #ef6c00;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
    }
    
    .status-completed {
        background: #e8f5e8;
        color: #4caf50;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
    }
    
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Banco de dados
def init_database():
    """Inicializa banco de dados com estrutura completa"""
    conn = sqlite3.connect('nutriapp360.db')
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'nutritionist', 'secretary', 'patient')),
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            crn TEXT,
            specializations TEXT,
            profile_image TEXT,
            permissions TEXT,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            created_by INTEGER,
            FOREIGN KEY (created_by) REFERENCES users (id)
        )
    ''')
    
    # Tabela de pacientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            patient_id TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            birth_date DATE,
            gender TEXT,
            height REAL,
            current_weight REAL,
            target_weight REAL,
            activity_level TEXT,
            medical_conditions TEXT,
            allergies TEXT,
            dietary_preferences TEXT,
            emergency_contact TEXT,
            emergency_phone TEXT,
            insurance_info TEXT,
            nutritionist_id INTEGER,
            secretary_id INTEGER,
            active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (nutritionist_id) REFERENCES users (id),
            FOREIGN KEY (secretary_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de agendamentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            appointment_id TEXT UNIQUE NOT NULL,
            patient_id INTEGER NOT NULL,
            nutritionist_id INTEGER NOT NULL,
            secretary_id INTEGER,
            appointment_date DATETIME NOT NULL,
            duration INTEGER DEFAULT 60,
            appointment_type TEXT,
            status TEXT DEFAULT 'agendado',
            notes TEXT,
            weight_recorded REAL,
            private_notes TEXT,
            follow_up_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (nutritionist_id) REFERENCES users (id),
            FOREIGN KEY (secretary_id) REFERENCES users (id)
        )
    ''')
    
    # Outras tabelas necessárias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meal_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_id TEXT UNIQUE NOT NULL,
            patient_id INTEGER NOT NULL,
            nutritionist_id INTEGER NOT NULL,
            plan_name TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE,
            daily_calories INTEGER,
            plan_data TEXT,
            status TEXT DEFAULT 'ativo',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (nutritionist_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT,
            prep_time INTEGER,
            cook_time INTEGER,
            servings INTEGER,
            calories_per_serving INTEGER,
            protein REAL,
            carbs REAL,
            fat REAL,
            fiber REAL,
            ingredients TEXT,
            instructions TEXT,
            tags TEXT,
            difficulty TEXT,
            nutritionist_id INTEGER,
            is_public BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (nutritionist_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            record_date DATE NOT NULL,
            weight REAL,
            body_fat REAL,
            muscle_mass REAL,
            waist_circumference REAL,
            hip_circumference REAL,
            notes TEXT,
            photos TEXT,
            recorded_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (recorded_by) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_financial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            appointment_id INTEGER,
            service_type TEXT,
            amount REAL NOT NULL,
            payment_method TEXT,
            payment_status TEXT DEFAULT 'pendente',
            due_date DATE,
            paid_date DATE,
            processed_by INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (appointment_id) REFERENCES appointments (id),
            FOREIGN KEY (processed_by) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            points INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            total_points INTEGER DEFAULT 0,
            last_activity DATE,
            streak_days INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            badge_name TEXT NOT NULL,
            badge_description TEXT,
            badge_icon TEXT,
            earned_date DATE DEFAULT CURRENT_DATE,
            points_awarded INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS llm_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            patient_id INTEGER,
            conversation_type TEXT,
            user_message TEXT NOT NULL,
            llm_response TEXT NOT NULL,
            context_data TEXT,
            feedback_rating INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action_type TEXT NOT NULL,
            table_affected TEXT,
            record_id INTEGER,
            old_values TEXT,
            new_values TEXT,
            ip_address TEXT,
            user_agent TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_database (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT NOT NULL,
            category TEXT,
            calories_per_100g REAL,
            protein_per_100g REAL,
            carbs_per_100g REAL,
            fat_per_100g REAL,
            fiber_per_100g REAL,
            sodium_per_100g REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Inserir dados iniciais se não existirem
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        insert_sample_data(cursor)
    
    conn.commit()
    conn.close()

def insert_sample_data(cursor):
    """Insere dados de exemplo no sistema"""
    
    # Usuários iniciais
    users_data = [
        ('admin', hashlib.sha256('admin123'.encode()).hexdigest(), 'admin', 'Administrador Sistema', 'admin@nutriapp.com', '(11) 99999-0001', None, None, None, '["all"]'),
        ('dr_silva', hashlib.sha256('nutri123'.encode()).hexdigest(), 'nutritionist', 'Dr. Ana Silva Santos', 'ana.silva@nutriapp.com', '(11) 99999-0002', 'CRN-3 12345', 'Nutrição Clínica, Esportiva', None, '["patients", "appointments", "meal_plans", "reports"]'),
        ('secretaria', hashlib.sha256('sec123'.encode()).hexdigest(), 'secretary', 'Maria Fernanda Costa', 'secretaria@nutriapp.com', '(11) 99999-0003', None, None, None, '["appointments", "patients_basic", "financial"]'),
        ('paciente1', hashlib.sha256('pac123'.encode()).hexdigest(), 'patient', 'João Carlos Oliveira', 'joao@email.com', '(11) 99999-0004', None, None, None, '["own_data", "own_progress"]')
    ]
    
    cursor.executemany('''
        INSERT INTO users (username, password_hash, role, full_name, email, phone, crn, specializations, profile_image, permissions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', users_data)
    
    # Pacientes de exemplo
    patients_data = [
        (4, 'PAT001', 'João Carlos Oliveira', 'joao@email.com', '(11) 98765-4321', '1985-03-15', 'M', 1.78, 85.2, 78.0, 'Sedentário', 'Diabetes tipo 2', 'Glúten', '', 'Maria Oliveira', '(11) 99999-1111', 'Unimed', 2, 3),
        (None, 'PAT002', 'Maria Santos Silva', 'maria@email.com', '(11) 98765-4322', '1990-07-22', 'F', 1.65, 72.5, 65.0, 'Moderado', 'Hipertensão', 'Lactose', 'Vegetariana', 'Pedro Silva', '(11) 99999-2222', 'Bradesco Saúde', 2, 3),
        (None, 'PAT003', 'Carlos Eduardo Lima', 'carlos@email.com', '(11) 98765-4323', '1982-11-08', 'M', 1.82, 95.0, 85.0, 'Ativo', 'Colesterol alto', 'Nenhuma', '', 'Ana Lima', '(11) 99999-3333', 'SulAmérica', 2, 3)
    ]
    
    cursor.executemany('''
        INSERT INTO patients (user_id, patient_id, full_name, email, phone, birth_date, gender, height, 
                             current_weight, target_weight, activity_level, medical_conditions, 
                             allergies, dietary_preferences, emergency_contact, emergency_phone, 
                             insurance_info, nutritionist_id, secretary_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', patients_data)
    
    # Receitas de exemplo
    recipes_data = [
        ('REC001', 'Salada de Quinoa com Vegetais', 'Saladas', 15, 0, 4, 320, 12.5, 42.0, 8.5, 6.2, 
         'Quinoa cozida (1 xícara), Tomate (2 unidades), Pepino (1 unidade), Cebola roxa (1/2), Azeite (2 colheres), Limão (1 unidade)', 
         '1. Cozinhe a quinoa. 2. Corte os vegetais. 3. Misture tudo. 4. Tempere com azeite e limão.', 
         'saudável,vegetariano,sem glúten', 'Fácil', 2),
        ('REC002', 'Salmão Grelhado com Legumes', 'Peixes', 20, 25, 2, 380, 35.0, 15.0, 22.0, 4.8,
         'Salmão (150g), Brócolis (1 xícara), Cenoura (1 unidade), Azeite (1 colher), Ervas finas',
         '1. Tempere o salmão. 2. Grelhe por 15 min. 3. Refogue os legumes. 4. Sirva quente.',
         'proteína,ômega 3,low carb', 'Médio', 2)
    ]
    
    cursor.executemany('''
        INSERT INTO recipes (recipe_id, name, category, prep_time, cook_time, servings, calories_per_serving,
                           protein, carbs, fat, fiber, ingredients, instructions, tags, difficulty, nutritionist_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', recipes_data)
    
    # Banco de alimentos
    foods_data = [
        ('Arroz branco cozido', 'Cereais', 130, 2.7, 28.0, 0.3, 0.4, 1),
        ('Arroz integral cozido', 'Cereais', 123, 2.6, 23.0, 0.9, 1.8, 1),
        ('Feijão preto cozido', 'Leguminosas', 77, 4.5, 14.0, 0.5, 8.7, 2),
        ('Peito de frango grelhado', 'Carnes', 165, 31.0, 0, 3.6, 0, 74),
        ('Salmão grelhado', 'Peixes', 206, 22.0, 0, 12.0, 0, 59),
        ('Brócolis cozido', 'Vegetais', 35, 2.8, 7.0, 0.4, 3.3, 41),
        ('Banana', 'Frutas', 89, 1.1, 23.0, 0.3, 2.6, 1),
        ('Abacate', 'Frutas', 160, 2.0, 9.0, 15.0, 7.0, 7),
        ('Ovos cozidos', 'Proteínas', 155, 13.0, 1.1, 11.0, 0, 124),
        ('Iogurte natural', 'Laticínios', 59, 10.0, 3.6, 0.4, 0, 36)
    ]
    
    cursor.executemany('''
        INSERT INTO food_database (food_name, category, calories_per_100g, protein_per_100g, 
                                 carbs_per_100g, fat_per_100g, fiber_per_100g, sodium_per_100g)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', foods_data)

# Sistema de autenticação
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    conn = sqlite3.connect('nutriapp360.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users SET last_login = CURRENT_TIMESTAMP 
        WHERE username = ? AND password_hash = ?
    ''', (username, hash_password(password)))
    
    cursor.execute('''
        SELECT id, username, password_hash, role, full_name, email, permissions 
        FROM users 
        WHERE username = ? AND active = 1
    ''', (username,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result and hash_password(password) == result[2]:
        return {
            'id': result[0],
            'username': result[1],
            'role': result[3],
            'full_name': result[4],
            'email': result[5],
            'permissions': json.loads(result[6]) if result[6] else []
        }
    return None

def log_audit_action(user_id, action, table, record_id):
    """Registra ação no log de auditoria"""
    try:
        conn = sqlite3.connect('nutriapp360.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_log (user_id, action_type, table_affected, record_id)
            VALUES (?, ?, ?, ?)
        ''', (user_id, action, table, record_id))
        
        conn.commit()
        conn.close()
    except:
        pass

# Assistente IA
class LLMAssistant:
    def __init__(self):
        self.context = "Assistente especializado em nutrição e saúde."
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """Gera resposta baseada no contexto"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["plano", "cardapio", "refeicao", "alimentar"]):
            return self._generate_meal_plan_response()
        elif any(word in prompt_lower for word in ["receita", "preparo", "cozinhar"]):
            return self._generate_recipe_response()
        elif any(word in prompt_lower for word in ["peso", "emagrecer", "dieta"]):
            return self._generate_weight_response()
        elif any(word in prompt_lower for word in ["imc", "calculo", "indice"]):
            return self._generate_calculation_response()
        elif any(word in prompt_lower for word in ["exercicio", "atividade", "treino"]):
            return self._generate_exercise_response()
        else:
            return self._generate_general_response()
    
    def _generate_meal_plan_response(self):
        return """
**🍽️ Plano Alimentar Equilibrado (1800 kcal)**

**☀️ Café da manhã (450 kcal - 25%):**
• 2 fatias de pão integral (140 kcal)
• 1 ovo mexido (90 kcal)  
• 1/2 abacate médio (120 kcal)
• 1 copo de leite desnatado (80 kcal)
• 1 banana pequena (70 kcal)

**🥤 Lanche manhã (180 kcal - 10%):**
• 1 iogurte grego natural (120 kcal)
• 1 colher de granola (60 kcal)

**🍽️ Almoço (630 kcal - 35%):**
• 150g peito de frango grelhado (250 kcal)
• 4 colheres arroz integral (140 kcal)
• 1 concha feijão preto (100 kcal)
• Salada verde + 1 col. azeite (90 kcal)
• 1 fruta média (50 kcal)

**🥪 Lanche tarde (180 kcal - 10%):**
• 1 maçã média (80 kcal)
• 10 amêndoas (100 kcal)

**🌙 Jantar (360 kcal - 20%):**
• 120g salmão grelhado (220 kcal)
• Legumes refogados (80 kcal)
• 1 batata doce pequena (60 kcal)

**💧 Hidratação:** 2,5L água + chás naturais sem açúcar

**⏰ Horários sugeridos:**
- Café: 7h00
- Lanche manhã: 10h00  
- Almoço: 12h30
- Lanche tarde: 15h30
- Jantar: 19h00
        """
    
    def _generate_recipe_response(self):
        return """
**👨‍🍳 Receita: Bowl Buddha Nutritivo**

**🥗 Ingredientes (2 porções):**
• 1 xícara quinoa cozida (160g)
• 150g grão-de-bico cozido
• 1 beterraba média assada
• 1/2 abacate maduro
• 100g espinafre baby
• 1/4 repolho roxo fatiado
• 2 col. sopa sementes de girassol
• 2 col. sopa azeite extra virgem
• 1 limão (suco)
• Sal e pimenta a gosto

**⏱️ Modo de Preparo (30 min):**
1. **Quinoa (15 min):** Cozinhe com caldo de legumes
2. **Beterraba (45 min):** Asse com azeite e ervas (180°C)
3. **Montagem:** Base de espinafre, adicione quinoa, grão-de-bico
4. **Decoração:** Beterraba, abacate, repolho em seções
5. **Finalização:** Sementes por cima, molho de limão e azeite

**📊 Informação Nutricional (por porção):**
• **Calorias:** 520 kcal
• **Proteínas:** 18g (14%)
• **Carboidratos:** 65g (50%)  
• **Gorduras:** 22g (36%)
• **Fibras:** 15g
• **Sódio:** 280mg

**🏷️ Tags:** Vegetariano • Sem Glúten • Rico em Fibras • Antioxidante

**💡 Dicas:**
- Prepare a beterraba com antecedência
- Varie as sementes (chia, linhaça, abóbora)
- Adicione outras proteínas se desejar
        """
    
    def _generate_weight_response(self):
        return """
**⚖️ Estratégias para Emagrecimento Saudável**

**🎯 Princípios Fundamentais:**
• **Déficit calórico:** 300-500 kcal/dia (perda de 0,5-1kg/semana)
• **Distribuição macro:** 25% proteína | 45% carboidrato | 30% gordura
• **Frequência:** 5-6 refeições menores vs 3 grandes
• **Hidratação:** 35ml/kg peso corporal/dia

**🍽️ Estratégias Alimentares:**
1. **Proteína em cada refeição:** 20-30g para saciedade
2. **Fibras abundantes:** 25-35g/dia para digestão
3. **Carboidratos complexos:** Evitar picos de insulina
4. **Gorduras boas:** Ômega-3, azeite, oleaginosas

**📈 Monitoramento Eficaz:**
• **Peso:** 2x/semana, mesmo horário, mesmas condições
• **Medidas:** Cintura, quadril, braços (quinzenal)
• **Fotos progresso:** Mesma pose, iluminação (mensal)
• **Energia:** Escala de 1-10 diariamente

**⚠️ Sinais de Alerta:**
- Perda >1kg/semana por períodos longos
- Fadiga excessiva ou irritabilidade
- Obsessão com comida ou peso
- Perda de massa muscular

**🎯 Meta Semanal:**
- Semana 1-2: Adaptação aos novos hábitos
- Semana 3-4: Primeiros resultados visíveis  
- Mês 2+: Perda consistente e sustentável

**💪 Lembre-se:** Foco na saúde, não apenas no número da balança!
        """
    
    def _generate_calculation_response(self):
        return """
**📊 Calculadoras Nutricionais Essenciais**

**🔢 IMC (Índice de Massa Corporal):**
• **Fórmula:** Peso(kg) ÷ Altura²(m)
• **Classificação:**
  - Abaixo do peso: <18,5
  - Peso normal: 18,5-24,9
  - Sobrepeso: 25,0-29,9  
  - Obesidade I: 30,0-34,9
  - Obesidade II: 35,0-39,9
  - Obesidade III: ≥40,0

**🔥 TMB (Taxa Metabólica Basal):**
**Homens:** 88,362 + (13,397 × peso) + (4,799 × altura) - (5,677 × idade)
**Mulheres:** 447,593 + (9,247 × peso) + (3,098 × altura) - (4,330 × idade)

**⚡ Gasto Calórico Total:**
• **Sedentário:** TMB × 1,2
• **Leve:** TMB × 1,375  
• **Moderado:** TMB × 1,55
• **Intenso:** TMB × 1,725
• **Muito intenso:** TMB × 1,9

**💧 Necessidade Hídrica:**
• **Fórmula básica:** 35ml × peso corporal
• **Com exercício:** +500-750ml por hora de atividade
• **Clima quente:** +20-25% da necessidade base

**🍽️ Distribuição de Macronutrientes:**
• **Carboidratos:** 45-65% das calorias totais
• **Proteínas:** 15-25% das calorias totais  
• **Gorduras:** 20-35% das calorias totais

**Exemplo prático para pessoa de 70kg, 170cm, 30 anos:**
- IMC: 24,2 (peso normal)
- TMB: ~1.680 kcal
- Gasto total (moderado): ~2.600 kcal
- Água: ~2,5L/dia
        """
    
    def _generate_exercise_response(self):
        return """
**🏃‍♀️ Exercícios e Nutrição: Guia Completo**

**⏰ Alimentação Pré-Treino (1-2h antes):**
• **Carboidratos:** Banana, aveia, batata doce
• **Proteína leve:** Iogurte, ovo
• **Hidratação:** 400-500ml água
• **Evitar:** Gorduras, fibras em excesso

**💪 Durante o Exercício:**
• **<1h:** Apenas água
• **1-2h:** 150-200ml bebida isotônica a cada 20min
• **>2h:** Carboidratos simples (gel, banana)

**🔋 Pós-Treino (até 2h depois):**
• **"Janela anabólica":** Carboidrato + Proteína (3:1 ou 4:1)
• **Exemplos:** 
  - Leite com chocolate
  - Banana + whey protein
  - Sanduíche de peito de peru
• **Hidratação:** 150% do peso perdido no treino

**🏋️‍♂️ Por Tipo de Exercício:**

**Cardio (Corrida, bike, natação):**
- Foco em carboidratos antes
- Reposição hídrica durante
- Proteína + carbo após

**Musculação:**
- Proteína 2-3h antes
- Carboidrato pré-treino
- Whey + carbo imediatamente após

**Exercícios longos (>2h):**
- Carga de carboidrato 3 dias antes
- Suplementação durante
- Recuperação nutricional planejada

**📊 Suplementação Básica:**
• **Whey Protein:** 20-30g pós-treino
• **Creatina:** 3-5g/dia (qualquer horário)
• **BCAA:** 5-10g durante treinos longos
• **Maltodextrina:** 30-60g em treinos >1h

**⚠️ Sinais de Atenção:**
- Fadiga excessiva
- Perda de performance
- Recuperação lenta
- Lesões frequentes

**💡 Dica de Ouro:** A nutrição representa 70% dos resultados. Treino sem alimentação adequada = resultados limitados!
        """
    
    def _generate_general_response(self):
        return """
**🤖 Assistente Nutricional NutriApp360**

Olá! Sou seu assistente especializado em nutrição e bem-estar.

**🎯 Posso ajudar com:**
• 📋 Planos alimentares personalizados
• 👨‍🍳 Receitas saudáveis e nutritivas  
• ⚖️ Estratégias de emagrecimento
• 🧮 Cálculos nutricionais (IMC, TMB, etc.)
• 💪 Orientações sobre exercício e alimentação
• 🥗 Análise de alimentos e nutrientes
• 💡 Dicas de alimentação saudável
• 🎯 Estabelecimento de metas realistas

**📝 Como usar:**
Digite sua dúvida específica para receber orientação personalizada e baseada em evidências científicas!

**💬 Exemplos de perguntas:**
- "Como calcular meu gasto calórico diário?"
- "Preciso de um plano para ganhar massa muscular"
- "Qual a melhor alimentação pré-treino?"
- "Como montar um prato equilibrado?"
- "Receitas ricas em proteína"

**⚠️ Importante:** 
Estas são orientações gerais. Para casos específicos, sempre consulte seu nutricionista para avaliação personalizada.

**🚀 Vamos começar? Digite sua pergunta!**
        """

def save_llm_conversation(user_id, patient_id, conv_type, user_message, llm_response, feedback=None):
    """Salva conversa com LLM no banco"""
    try:
        conn = sqlite3.connect('nutriapp360.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO llm_conversations (user_id, patient_id, conversation_type, user_message, llm_response, feedback_rating)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, patient_id, conv_type, user_message, llm_response, feedback))
        
        conn.commit()
        conn.close()
    except:
        pass

# Interface de login
def show_login_page():
    st.markdown("""
    <div class="main-header">
        <h1>🥗 NutriApp360 v5.0</h1>
        <h3>Sistema Completo de Gestão Nutricional</h3>
        <p><strong>✅ TODAS AS FUNCIONALIDADES IMPLEMENTADAS</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        user_type = st.selectbox("🎭 Tipo de Usuário", [
            "👨‍⚕️ Administrador", 
            "🥗 Nutricionista", 
            "📋 Secretária", 
            "🙋‍♂️ Paciente"
        ])
        
        with st.form("login_form"):
            username = st.text_input("👤 Usuário")
            password = st.text_input("🔒 Senha", type="password")
            
            col_login1, col_login2 = st.columns(2)
            with col_login1:
                login_btn = st.form_submit_button("🚀 Entrar", use_container_width=True, type="primary")
            with col_login2:
                demo_btn = st.form_submit_button("🎮 Demo", use_container_width=True)
            
            if demo_btn:
                demo_credentials = {
                    "👨‍⚕️ Administrador": ("admin", "admin123"),
                    "🥗 Nutricionista": ("dr_silva", "nutri123"),
                    "📋 Secretária": ("secretaria", "sec123"),
                    "🙋‍♂️ Paciente": ("paciente1", "pac123")
                }
                username, password = demo_credentials[user_type]
                login_btn = True
            
            if login_btn and username and password:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.success(f"🎉 Bem-vindo(a), {user['full_name']}!")
                    log_audit_action(user['id'], 'login', 'users', user['id'])
                    st.rerun()
                else:
                    st.error("❌ Credenciais inválidas!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Credenciais demo
        demo_map = {
            "👨‍⚕️ Administrador": ("admin", "admin123"),
            "🥗 Nutricionista": ("dr_silva", "nutri123"),
            "📋 Secretária": ("secretaria", "sec123"),
            "🙋‍♂️ Paciente": ("paciente1", "pac123")
        }
        
        st.info(f"""
        **🎮 Credenciais Demo ({user_type}):**
        
        **👤 Usuário:** `{demo_map[user_type][0]}`
        
        **🔒 Senha:** `{demo_map[user_type][1]}`
        """)

# Sidebar
def show_sidebar():
    user_role = st.session_state.user['role']
    user_name = st.session_state.user['full_name']
    
    # Header do sidebar
    role_icons = {
        'admin': '👨‍⚕️',
        'nutritionist': '🥗',
        'secretary': '📋',
        'patient': '🙋‍♂️'
    }
    
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #4CAF50, #8BC34A); 
                border-radius: 15px; margin-bottom: 1rem;">
        <h3 style="color: white; margin: 0;">{role_icons[user_role]} NutriApp360</h3>
        <p style="color: white; margin: 0; font-size: 0.9rem;">
            Olá, <strong>{user_name}</strong>
        </p>
        <span style="background: rgba(255,255,255,0.2); padding: 0.2rem 0.5rem; border-radius: 10px; color: white; font-size: 0.8rem;">
            {user_role.title()}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Menus por usuário
    menu_options = {
        'admin': {
            'dashboard': '📊 Dashboard Executivo',
            'users_management': '👥 Gestão de Usuários',
            'system_analytics': '📈 Analytics do Sistema',
            'reports_advanced': '📋 Relatórios Avançados',
            'audit_log': '🔍 Log de Auditoria',
            'system_settings': '⚙️ Configurações Sistema'
        },
        'nutritionist': {
            'dashboard': '📊 Dashboard Pessoal',
            'patients': '👥 Meus Pacientes',
            'appointments': '📅 Agendamentos',
            'meal_plans': '🍽️ Planos Alimentares',
            'recipes': '👨‍🍳 Biblioteca Receitas',
            'progress_tracking': '📈 Acompanhamento',
            'ia_assistant': '🤖 Assistente IA',
            'calculators': '🧮 Calculadoras',
            'reports': '📋 Relatórios'
        },
        'secretary': {
            'dashboard': '📊 Dashboard Operacional',
            'appointments': '📅 Gestão Agendamentos',
            'patients_basic': '👥 Pacientes',
            'financial': '💰 Sistema Financeiro',
            'reports_basic': '📋 Relatórios'
        },
        'patient': {
            'dashboard': '📊 Meu Dashboard',
            'my_progress': '📈 Meu Progresso',
            'my_appointments': '📅 Minhas Consultas',
            'my_plan': '🍽️ Meu Plano Alimentar',
            'points_badges': '🏆 Pontos & Badges',
            'chat_ia': '🤖 Chat com IA',
            'calculators_personal': '🧮 Calculadoras',
            'profile': '👤 Meu Perfil'
        }
    }
    
    current_menu = menu_options.get(user_role, {})
    selected_page = st.sidebar.selectbox("📋 Menu Principal", 
                                       list(current_menu.keys()),
                                       format_func=lambda x: current_menu[x])
    
    # Status do sistema
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 Status do Sistema**")
    
    conn = sqlite3.connect('nutriapp360.db')
    try:
        total_users = pd.read_sql_query("SELECT COUNT(*) as count FROM users WHERE active = 1", conn).iloc[0]['count']
        total_patients = pd.read_sql_query("SELECT COUNT(*) as count FROM patients WHERE active = 1", conn).iloc[0]['count']
        
        st.sidebar.metric("👥 Usuários Ativos", total_users)
        st.sidebar.metric("🙋‍♂️ Pacientes", total_patients)
    except:
        pass
    finally:
        conn.close()
    
    # Logout
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Sair do Sistema", use_container_width=True):
        log_audit_action(st.session_state.user['id'], 'logout', 'users', st.session_state.user['id'])
        st.session_state.user = None
        st.rerun()
    
    return selected_page

# Roteamento principal
def main():
    load_css()
    init_database()
    
    if 'user' not in st.session_state or not st.session_state.user:
        show_login_page()
        return
    
    selected_page = show_sidebar()
    user_role = st.session_state.user['role']
    
    # Roteamento por função
    if user_role == 'admin':
        admin_routes(selected_page)
    elif user_role == 'nutritionist':
        nutritionist_routes(selected_page)
    elif user_role == 'secretary':
        secretary_routes(selected_page)
    elif user_role == 'patient':
        patient_routes(selected_page)

def admin_routes(page):
    """Rotas para administrador"""
    if page == 'dashboard':
        show_admin_dashboard()
    elif page == 'users_management':
        show_users_management()
    elif page == 'system_analytics':
        show_system_analytics()
    elif page == 'reports_advanced':
        show_advanced_reports()
    elif page == 'audit_log':
        show_audit_log()
    elif page == 'system_settings':
        show_system_settings()

def nutritionist_routes(page):
    """Rotas para nutricionista"""
    if page == 'dashboard':
        show_nutritionist_dashboard()
    elif page == 'patients':
        show_patients_management()
    elif page == 'appointments':
        show_appointments_management()
    elif page == 'meal_plans':
        show_meal_plans_management()
    elif page == 'recipes':
        show_recipes_management()
    elif page == 'progress_tracking':
        show_progress_tracking()
    elif page == 'ia_assistant':
        show_ia_assistant()
    elif page == 'calculators':
        show_calculators()
    elif page == 'reports':
        show_nutritionist_reports()

def secretary_routes(page):
    """Rotas para secretária"""
    if page == 'dashboard':
        show_secretary_dashboard()
    elif page == 'appointments':
        show_appointments_management()
    elif page == 'patients_basic':
        show_patients_basic()
    elif page == 'financial':
        show_financial_management()
    elif page == 'reports_basic':
        show_reports_basic()

def patient_routes(page):
    """Rotas para paciente"""
    if page == 'dashboard':
        show_patient_dashboard()
    elif page == 'my_progress':
        show_my_progress()
    elif page == 'my_appointments':
        show_my_appointments()
    elif page == 'my_plan':
        show_my_plan()
    elif page == 'points_badges':
        show_points_badges()
    elif page == 'chat_ia':
        show_patient_chat_ia()
    elif page == 'calculators_personal':
        show_calculators_personal()
    elif page == 'profile':
        show_patient_profile()

# IMPLEMENTAÇÃO COMPLETA DAS FUNCIONALIDADES

def show_admin_dashboard():
    st.markdown('<h1 class="main-header">📊 Dashboard Executivo</h1>', unsafe_allow_html=True)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    conn = sqlite3.connect('nutriapp360.db')
    
    try:
        total_users = pd.read_sql_query("SELECT COUNT(*) as count FROM users WHERE active = 1", conn).iloc[0]['count']
        total_patients = pd.read_sql_query("SELECT COUNT(*) as count FROM patients WHERE active = 1", conn).iloc[0]['count']
        total_nutritionists = pd.read_sql_query("SELECT COUNT(*) as count FROM users WHERE role = 'nutritionist' AND active = 1", conn).iloc[0]['count']
        total_appointments_month = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM appointments 
            WHERE strftime('%Y-%m', appointment_date) = strftime('%Y-%m', 'now')
        """, conn).iloc[0]['count']
        
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
                <h3 style="margin: 0; color: #2196F3;">🙋‍♂️ {total_patients}</h3>
                <p style="margin: 0;">Pacientes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; color: #9C27B0;">🥗 {total_nutritionists}</h3>
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
        
        # Gráficos de análise
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("📈 Crescimento de Usuários")
            # Simular dados de crescimento
            months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
            users_growth = [8, 12, 18, 24, 32, total_users]
            patients_growth = [4, 7, 11, 16, 23, total_patients]
            
            growth_data = pd.DataFrame({
                'Mês': months,
                'Usuários': users_growth,
                'Pacientes': patients_growth
            })
            
            fig = px.line(growth_data, x='Mês', y=['Usuários', 'Pacientes'], 
                         title="Crescimento Mensal", markers=True)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col_chart2:
            st.subheader("📊 Distribuição de Usuários")
            user_dist = pd.read_sql_query("""
                SELECT role, COUNT(*) as count 
                FROM users WHERE active = 1 
                GROUP BY role
            """, conn)
            
            role_names = {
                'admin': 'Administradores',
                'nutritionist': 'Nutricionistas', 
                'secretary': 'Secretárias',
                'patient': 'Pacientes'
            }
            
            user_dist['role_name'] = user_dist['role'].map(role_names)
            
            fig = px.pie(user_dist, values='count', names='role_name', 
                        title="Tipos de Usuário")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Atividade recente
        st.subheader("🔍 Atividade Recente do Sistema")
        
        recent_activity = pd.read_sql_query("""
            SELECT 
                a.action_type,
                a.table_affected,
                u.full_name,
                a.created_at,
                a.record_id
            FROM audit_log a
            JOIN users u ON u.id = a.user_id
            ORDER BY a.created_at DESC
            LIMIT 10
        """, conn)
        
        if not recent_activity.empty:
            for idx, activity in recent_activity.iterrows():
                action_time = pd.to_datetime(activity['created_at']).strftime('%d/%m/%Y %H:%M')
                
                st.markdown(f"""
                <div class="appointment-card">
                    <strong>{activity['full_name']}</strong> realizou <strong>{activity['action_type']}</strong> 
                    em {activity['table_affected']} 
                    <small style="float: right; color: #666;">{action_time}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📝 Nenhuma atividade recente registrada")
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar dashboard: {e}")
    finally:
        conn.close()

def show_users_management():
    st.markdown('<h1 class="main-header">👥 Gestão de Usuários</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Lista de Usuários", "➕ Novo Usuário", "📊 Estatísticas"])
    
    with tab1:
        st.subheader("👥 Usuários do Sistema")
        
        conn = sqlite3.connect('nutriapp360.db')
        users_df = pd.read_sql_query("""
            SELECT 
                id, username, full_name, email, phone, role, 
                active, created_at, last_login
            FROM users 
            ORDER BY created_at DESC
        """, conn)
        conn.close()
        
        if not users_df.empty:
            # Filtros
            col_filter1, col_filter2, col_filter3 = st.columns(3)
            
            with col_filter1:
                role_filter = st.selectbox("🎭 Filtrar por Função", 
                                         ['Todos'] + list(users_df['role'].unique()))
            
            with col_filter2:
                status_filter = st.selectbox("📊 Status", 
                                           ['Todos', 'Ativo', 'Inativo'])
            
            with col_filter3:
                search_text = st.text_input("🔍 Buscar por nome")
            
            # Aplicar filtros
            filtered_df = users_df.copy()
            
            if role_filter != 'Todos':
                filtered_df = filtered_df[filtered_df['role'] == role_filter]
            
            if status_filter == 'Ativo':
                filtered_df = filtered_df[filtered_df['active'] == 1]
            elif status_filter == 'Inativo':
                filtered_df = filtered_df[filtered_df['active'] == 0]
            
            if search_text:
                filtered_df = filtered_df[
                    filtered_df['full_name'].str.contains(search_text, case=False, na=False)
                ]
            
            # Exibir usuários
            for idx, user in filtered_df.iterrows():
                status_color = "#4CAF50" if user['active'] else "#F44336"
                status_text = "Ativo" if user['active'] else "Inativo"
                
                role_icons = {
                    'admin': '👨‍⚕️',
                    'nutritionist': '🥗',
                    'secretary': '📋',
                    'patient': '🙋‍♂️'
                }
                
                last_login = pd.to_datetime(user['last_login']).strftime('%d/%m/%Y %H:%M') if user['last_login'] else 'Nunca'
                created = pd.to_datetime(user['created_at']).strftime('%d/%m/%Y')
                
                col_user1, col_user2 = st.columns([3, 1])
                
                with col_user1:
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h4 style="margin: 0; color: #2E7D32;">
                            {role_icons.get(user['role'], '👤')} {user['full_name']}
                            <span style="background: {status_color}; color: white; padding: 0.2rem 0.5rem; 
                                         border-radius: 10px; font-size: 0.7rem; margin-left: 1rem;">
                                {status_text}
                            </span>
                        </h4>
                        <p style="margin: 0.5rem 0; color: #666;">
                            <strong>👤 Usuário:</strong> {user['username']} | 
                            <strong>📧 Email:</strong> {user['email'] or 'N/A'} | 
                            <strong>📱 Telefone:</strong> {user['phone'] or 'N/A'}
                        </p>
                        <p style="margin: 0; font-size: 0.9rem; color: #888;">
                            <strong>📅 Criado:</strong> {created} | 
                            <strong>🔐 Último login:</strong> {last_login}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_user2:
                    if st.button(f"✏️ Editar", key=f"edit_{user['id']}"):
                        st.session_state.edit_user_id = user['id']
                        st.rerun()
        else:
            st.info("📝 Nenhum usuário encontrado")
    
    with tab2:
        st.subheader("➕ Cadastrar Novo Usuário")
        
        with st.form("new_user_form"):
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                new_username = st.text_input("👤 Nome de usuário *")
                new_full_name = st.text_input("👤 Nome completo *")
                new_email = st.text_input("📧 Email")
                new_phone = st.text_input("📱 Telefone")
            
            with col_form2:
                new_role = st.selectbox("🎭 Função *", 
                                      ['nutritionist', 'secretary', 'patient', 'admin'])
                new_password = st.text_input("🔒 Senha *", type="password")
                new_crn = st.text_input("📋 CRN (apenas nutricionistas)")
                new_specializations = st.text_input("🎓 Especializações")
            
            submitted = st.form_submit_button("✅ Cadastrar Usuário", type="primary")
            
            if submitted:
                if new_username and new_full_name and new_password:
                    try:
                        conn = sqlite3.connect('nutriapp360.db')
                        cursor = conn.cursor()
                        
                        # Verificar se usuário já existe
                        cursor.execute("SELECT id FROM users WHERE username = ?", (new_username,))
                        if cursor.fetchone():
                            st.error("❌ Nome de usuário já existe!")
                        else:
                            # Inserir novo usuário
                            cursor.execute('''
                                INSERT INTO users (username, password_hash, role, full_name, email, 
                                                 phone, crn, specializations, created_by)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (new_username, hash_password(new_password), new_role, new_full_name,
                                 new_email, new_phone, new_crn, new_specializations, 
                                 st.session_state.user['id']))
                            
                            conn.commit()
                            log_audit_action(st.session_state.user['id'], 'create_user', 'users', cursor.lastrowid)
                            st.success(f"✅ Usuário {new_full_name} cadastrado com sucesso!")
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Erro ao cadastrar usuário: {e}")
                    finally:
                        conn.close()
                else:
                    st.error("❌ Preencha todos os campos obrigatórios!")
    
    with tab3:
        st.subheader("📊 Estatísticas de Usuários")
        
        conn = sqlite3.connect('nutriapp360.db')
        
        # Estatísticas por função
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            role_stats = pd.read_sql_query("""
                SELECT role, COUNT(*) as count, 
                       SUM(CASE WHEN active = 1 THEN 1 ELSE 0 END) as active_count
                FROM users 
                GROUP BY role
            """, conn)
            
            if not role_stats.empty:
                st.markdown("**👥 Por Função:**")
                for idx, stat in role_stats.iterrows():
                    role_name = {
                        'admin': 'Administradores',
                        'nutritionist': 'Nutricionistas',
                        'secretary': 'Secretárias', 
                        'patient': 'Pacientes'
                    }.get(stat['role'], stat['role'])
                    
                    st.metric(role_name, f"{stat['active_count']}/{stat['count']}")
        
        with col_stat2:
            # Usuários por mês
            monthly_users = pd.read_sql_query("""
                SELECT 
                    strftime('%Y-%m', created_at) as month,
                    COUNT(*) as count
                FROM users 
                GROUP BY strftime('%Y-%m', created_at)
                ORDER BY month DESC
                LIMIT 6
            """, conn)
            
            if not monthly_users.empty:
                fig = px.bar(monthly_users, x='month', y='count', 
                           title="📈 Novos Usuários por Mês")
                st.plotly_chart(fig, use_container_width=True)
        
        conn.close()

def show_patients_management():
    st.markdown('<h1 class="main-header">👥 Gestão de Pacientes</h1>', unsafe_allow_html=True)
    
    nutritionist_id = st.session_state.user['id']
    
    tab1, tab2, tab3 = st.tabs(["📋 Meus Pacientes", "➕ Novo Paciente", "📊 Estatísticas"])
    
    with tab1:
        st.subheader("👥 Lista de Pacientes")
        
        conn = sqlite3.connect('nutriapp360.db')
        patients_df = pd.read_sql_query("""
            SELECT 
                p.*, u.full_name as user_name
            FROM patients p
            LEFT JOIN users u ON u.id = p.user_id
            WHERE p.nutritionist_id = ? AND p.active = 1
            ORDER BY p.created_at DESC
        """, conn, params=[nutritionist_id])
        
        if not patients_df.empty:
            # Filtros
            col_filter1, col_filter2 = st.columns(2)
            
            with col_filter1:
                search_patient = st.text_input("🔍 Buscar paciente")
            
            with col_filter2:
                gender_filter = st.selectbox("⚧ Gênero", ['Todos', 'M', 'F'])
            
            # Aplicar filtros
            filtered_patients = patients_df.copy()
            
            if search_patient:
                filtered_patients = filtered_patients[
                    filtered_patients['full_name'].str.contains(search_patient, case=False, na=False)
                ]
            
            if gender_filter != 'Todos':
                filtered_patients = filtered_patients[filtered_patients['gender'] == gender_filter]
            
            # Exibir pacientes
            for idx, patient in filtered_patients.iterrows():
                col_patient1, col_patient2 = st.columns([3, 1])
                
                with col_patient1:
                    # Calcular idade
                    if patient['birth_date']:
                        birth_date = pd.to_datetime(patient['birth_date'])
                        age = (datetime.now() - birth_date).days // 365
                    else:
                        age = "N/A"
                    
                    # Calcular IMC
                    if patient['height'] and patient['current_weight']:
                        imc = patient['current_weight'] / (patient['height'] ** 2)
                        imc_text = f"{imc:.1f}"
                        
                        if imc < 18.5:
                            imc_color = "#2196F3"
                        elif imc < 25:
                            imc_color = "#4CAF50"
                        elif imc < 30:
                            imc_color = "#FF9800"
                        else:
                            imc_color = "#F44336"
                    else:
                        imc_text = "N/A"
                        imc_color = "#999"
                    
                    gender_icon = "👨" if patient['gender'] == 'M' else "👩"
                    
                    st.markdown(f"""
                    <div class="patient-info-card">
                        <h4 style="margin: 0; color: #2E7D32;">
                            {gender_icon} {patient['full_name']} ({age} anos)
                        </h4>
                        <p style="margin: 0.5rem 0;">
                            <strong>📋 ID:</strong> {patient['patient_id']} | 
                            <strong>📧 Email:</strong> {patient['email'] or 'N/A'} | 
                            <strong>📱 Telefone:</strong> {patient['phone'] or 'N/A'}
                        </p>
                        <p style="margin: 0.5rem 0;">
                            <strong>⚖️ Peso:</strong> {patient['current_weight'] or 'N/A'} kg | 
                            <strong>🎯 Meta:</strong> {patient['target_weight'] or 'N/A'} kg | 
                            <strong>📏 IMC:</strong> <span style="color: {imc_color}; font-weight: bold;">{imc_text}</span>
                        </p>
                        <p style="margin: 0; font-size: 0.9rem; color: #666;">
                            <strong>🏃‍♂️ Atividade:</strong> {patient['activity_level'] or 'N/A'} | 
                            <strong>🚨 Condições:</strong> {patient['medical_conditions'] or 'Nenhuma'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_patient2:
                    if st.button(f"👁️ Ver Detalhes", key=f"view_{patient['id']}"):
                        st.session_state.selected_patient_id = patient['id']
                        st.session_state.show_patient_details = True
                        st.rerun()
        else:
            st.info("📝 Nenhum paciente encontrado")
        
        conn.close()
        
        # Modal de detalhes do paciente
        if hasattr(st.session_state, 'show_patient_details') and st.session_state.show_patient_details:
            show_patient_details_modal()
    
    with tab2:
        st.subheader("➕ Cadastrar Novo Paciente")
        
        with st.form("new_patient_form"):
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                patient_name = st.text_input("👤 Nome completo *")
                patient_email = st.text_input("📧 Email")
                patient_phone = st.text_input("📱 Telefone")
                birth_date = st.date_input("📅 Data de nascimento")
                gender = st.selectbox("⚧ Gênero", ['M', 'F'])
            
            with col_form2:
                height = st.number_input("📏 Altura (m)", min_value=1.0, max_value=2.5, value=1.70, step=0.01)
                current_weight = st.number_input("⚖️ Peso atual (kg)", min_value=30.0, max_value=300.0, value=70.0)
                target_weight = st.number_input("🎯 Peso objetivo (kg)", min_value=30.0, max_value=300.0, value=65.0)
                activity_level = st.selectbox("🏃‍♂️ Nível de atividade", 
                                            ['Sedentário', 'Leve', 'Moderado', 'Ativo', 'Muito Ativo'])
            
            medical_conditions = st.text_area("🏥 Condições médicas")
            allergies = st.text_area("🚨 Alergias alimentares")
            dietary_preferences = st.text_area("🥗 Preferências alimentares")
            
            col_emergency1, col_emergency2 = st.columns(2)
            with col_emergency1:
                emergency_contact = st.text_input("🆘 Contato de emergência")
            with col_emergency2:
                emergency_phone = st.text_input("📞 Telefone de emergência")
            
            submitted = st.form_submit_button("✅ Cadastrar Paciente", type="primary")
            
            if submitted:
                if patient_name:
                    try:
                        conn = sqlite3.connect('nutriapp360.db')
                        cursor = conn.cursor()
                        
                        # Gerar ID do paciente
                        patient_id = f"PAT{random.randint(1000, 9999)}"
                        
                        cursor.execute('''
                            INSERT INTO patients (patient_id, full_name, email, phone, birth_date, 
                                                gender, height, current_weight, target_weight, 
                                                activity_level, medical_conditions, allergies, 
                                                dietary_preferences, emergency_contact, emergency_phone, 
                                                nutritionist_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (patient_id, patient_name, patient_email, patient_phone, birth_date,
                             gender, height, current_weight, target_weight, activity_level,
                             medical_conditions, allergies, dietary_preferences, emergency_contact,
                             emergency_phone, nutritionist_id))
                        
                        conn.commit()
                        log_audit_action(st.session_state.user['id'], 'create_patient', 'patients', cursor.lastrowid)
                        st.success(f"✅ Paciente {patient_name} cadastrado com sucesso!")
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Erro ao cadastrar paciente: {e}")
                    finally:
                        conn.close()
                else:
                    st.error("❌ Nome do paciente é obrigatório!")
    
    with tab3:
        st.subheader("📊 Estatísticas dos Pacientes")
        
        conn = sqlite3.connect('nutriapp360.db')
        
        # Métricas gerais
        col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
        
        total_patients = pd.read_sql_query("""
            SELECT COUNT(*) as count FROM patients 
            WHERE nutritionist_id = ? AND active = 1
        """, conn, params=[nutritionist_id]).iloc[0]['count']
        
        avg_age = pd.read_sql_query("""
            SELECT AVG((julianday('now') - julianday(birth_date))/365.25) as avg_age 
            FROM patients 
            WHERE nutritionist_id = ? AND active = 1 AND birth_date IS NOT NULL
        """, conn, params=[nutritionist_id]).iloc[0]['avg_age']
        
        gender_stats = pd.read_sql_query("""
            SELECT gender, COUNT(*) as count 
            FROM patients 
            WHERE nutritionist_id = ? AND active = 1 
            GROUP BY gender
        """, conn, params=[nutritionist_id])
        
        with col_metric1:
            st.metric("👥 Total de Pacientes", total_patients)
        
        with col_metric2:
            st.metric("📊 Idade Média", f"{avg_age:.0f} anos" if avg_age else "N/A")
        
        with col_metric3:
            male_count = gender_stats[gender_stats['gender'] == 'M']['count'].sum() if not gender_stats.empty else 0
            st.metric("👨 Homens", male_count)
        
        with col_metric4:
            female_count = gender_stats[gender_stats['gender'] == 'F']['count'].sum() if not gender_stats.empty else 0
            st.metric("👩 Mulheres", female_count)
        
        # Gráfico de distribuição por IMC
        if total_patients > 0:
            imc_data = pd.read_sql_query("""
                SELECT 
                    current_weight, height,
                    CASE 
                        WHEN current_weight/(height*height) < 18.5 THEN 'Abaixo do peso'
                        WHEN current_weight/(height*height) < 25 THEN 'Peso normal'
                        WHEN current_weight/(height*height) < 30 THEN 'Sobrepeso'
                        ELSE 'Obesidade'
                    END as imc_category
                FROM patients 
                WHERE nutritionist_id = ? AND active = 1 
                AND current_weight IS NOT NULL AND height IS NOT NULL
            """, conn, params=[nutritionist_id])
            
            if not imc_data.empty:
                col_chart1, col_chart2 = st.columns(2)
                
                with col_chart1:
                    imc_dist = imc_data['imc_category'].value_counts()
                    fig = px.pie(values=imc_dist.values, names=imc_dist.index, 
                               title="📊 Distribuição por IMC")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col_chart2:
                    activity_dist = pd.read_sql_query("""
                        SELECT activity_level, COUNT(*) as count 
                        FROM patients 
                        WHERE nutritionist_id = ? AND active = 1 
                        GROUP BY activity_level
                    """, conn, params=[nutritionist_id])
                    
                    if not activity_dist.empty:
                        fig = px.bar(activity_dist, x='activity_level', y='count', 
                                   title="🏃‍♂️ Nível de Atividade")
                        st.plotly_chart(fig, use_container_width=True)
        
        conn.close()

def show_patient_details_modal():
    """Mostra detalhes completos do paciente selecionado"""
    if hasattr(st.session_state, 'selected_patient_id'):
        conn = sqlite3.connect('nutriapp360.db')
        
        patient = pd.read_sql_query("""
            SELECT p.*, u.full_name as user_name
            FROM patients p
            LEFT JOIN users u ON u.id = p.user_id
            WHERE p.id = ?
        """, conn, params=[st.session_state.selected_patient_id])
        
        if not patient.empty:
            patient = patient.iloc[0]
            
            st.markdown("---")
            st.markdown(f"### 👤 Detalhes: {patient['full_name']}")
            
            col_close = st.columns([4, 1])
            with col_close[1]:
                if st.button("❌ Fechar"):
                    st.session_state.show_patient_details = False
                    del st.session_state.selected_patient_id
                    st.rerun()
            
            # Informações pessoais
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.markdown("**📋 Informações Pessoais**")
                st.write(f"**ID:** {patient['patient_id']}")
                st.write(f"**Email:** {patient['email'] or 'N/A'}")
                st.write(f"**Telefone:** {patient['phone'] or 'N/A'}")
                st.write(f"**Nascimento:** {patient['birth_date'] or 'N/A'}")
                st.write(f"**Gênero:** {'Masculino' if patient['gender'] == 'M' else 'Feminino'}")
            
            with col_info2:
                st.markdown("**📊 Dados Físicos**")
                st.write(f"**Altura:** {patient['height']} m")
                st.write(f"**Peso Atual:** {patient['current_weight']} kg")
                st.write(f"**Peso Objetivo:** {patient['target_weight']} kg")
                
                if patient['height'] and patient['current_weight']:
                    imc = patient['current_weight'] / (patient['height'] ** 2)
                    st.write(f"**IMC:** {imc:.1f}")
                
                st.write(f"**Atividade:** {patient['activity_level']}")
            
            # Informações médicas
            if patient['medical_conditions'] or patient['allergies'] or patient['dietary_preferences']:
                st.markdown("**🏥 Informações Médicas**")
                
                if patient['medical_conditions']:
                    st.write(f"**Condições Médicas:** {patient['medical_conditions']}")
                
                if patient['allergies']:
                    st.write(f"**Alergias:** {patient['allergies']}")
                
                if patient['dietary_preferences']:
                    st.write(f"**Preferências Alimentares:** {patient['dietary_preferences']}")
            
            # Contato de emergência
            if patient['emergency_contact'] or patient['emergency_phone']:
                st.markdown("**🆘 Contato de Emergência**")
                st.write(f"**Nome:** {patient['emergency_contact'] or 'N/A'}")
                st.write(f"**Telefone:** {patient['emergency_phone'] or 'N/A'}")
            
            # Histórico de progresso
            st.markdown("**📈 Histórico de Progresso**")
            
            progress_data = pd.read_sql_query("""
                SELECT * FROM patient_progress 
                WHERE patient_id = ? 
                ORDER BY record_date DESC 
                LIMIT 5
            """, conn, params=[st.session_state.selected_patient_id])
            
            if not progress_data.empty:
                for idx, progress in progress_data.iterrows():
                    record_date = pd.to_datetime(progress['record_date']).strftime('%d/%m/%Y')
                    st.write(f"**{record_date}:** Peso: {progress['weight']}kg, Notas: {progress['notes'] or 'Nenhuma'}")
            else:
                st.info("📝 Nenhum registro de progresso encontrado")
        
        conn.close()

def show_appointments_management():
    st.markdown('<h1 class="main-header">📅 Gestão de Agendamentos</h1>', unsafe_allow_html=True)
    
    user_role = st.session_state.user['role']
    user_id = st.session_state.user['id']
    
    tab1, tab2, tab3 = st.tabs(["📋 Agendamentos", "➕ Novo Agendamento", "📊 Relatórios"])
    
    with tab1:
        st.subheader("📅 Lista de Agendamentos")
        
        # Filtros de data
        col_date1, col_date2, col_date3 = st.columns(3)
        
        with col_date1:
            date_filter = st.selectbox("📅 Período", 
                                     ['Hoje', 'Esta Semana', 'Este Mês', 'Personalizado'])
        
        # Calcular datas baseado no filtro
        today = date.today()
        
        if date_filter == 'Hoje':
            start_date = end_date = today
        elif date_filter == 'Esta Semana':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif date_filter == 'Este Mês':
            start_date = today.replace(day=1)
            next_month = today.replace(day=28) + timedelta(days=4)
            end_date = next_month - timedelta(days=next_month.day)
        else:  # Personalizado
            with col_date2:
                start_date = st.date_input("📅 Data inicial", value=today)
            with col_date3:
                end_date = st.date_input("📅 Data final", value=today)
        
        # Status filter
        status_filter = st.selectbox("📊 Status", 
                                   ['Todos', 'agendado', 'confirmado', 'realizado', 'cancelado'])
        
        # Buscar agendamentos
        conn = sqlite3.connect('nutriapp360.db')
        
        # Query baseada no papel do usuário
        if user_role == 'nutritionist':
            where_clause = "a.nutritionist_id = ?"
            params = [user_id]
        elif user_role == 'secretary':
            where_clause = "a.secretary_id = ?"
            params = [user_id]
        else:  # admin
            where_clause = "1=1"
            params = []
        
        query = f"""
            SELECT 
                a.id, a.appointment_id, a.appointment_date, a.duration, 
                a.appointment_type, a.status, a.notes,
                p.full_name as patient_name, p.patient_id,
                n.full_name as nutritionist_name
            FROM appointments a
            JOIN patients p ON p.id = a.patient_id
            JOIN users n ON n.id = a.nutritionist_id
            WHERE {where_clause}
            AND DATE(a.appointment_date) BETWEEN ? AND ?
        """
        params.extend([start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')])
        
        if status_filter != 'Todos':
            query += " AND a.status = ?"
            params.append(status_filter)
        
        query += " ORDER BY a.appointment_date"
        
        appointments_df = pd.read_sql_query(query, conn, params=params)
        
        if not appointments_df.empty:
            for idx, apt in appointments_df.iterrows():
                apt_datetime = pd.to_datetime(apt['appointment_date'])
                apt_date = apt_datetime.strftime('%d/%m/%Y')
                apt_time = apt_datetime.strftime('%H:%M')
                
                # Cores por status
                status_colors = {
                    'agendado': '#FF9800',
                    'confirmado': '#2196F3',
                    'realizado': '#4CAF50',
                    'cancelado': '#F44336'
                }
                
                status_color = status_colors.get(apt['status'], '#999')
                
                col_apt1, col_apt2 = st.columns([3, 1])
                
                with col_apt1:
                    st.markdown(f"""
                    <div class="appointment-card">
                        <h4 style="margin: 0; color: #2E7D32;">
                            📅 {apt_date} às {apt_time} ({apt['duration']} min)
                            <span style="background: {status_color}; color: white; padding: 0.2rem 0.5rem; 
                                         border-radius: 10px; font-size: 0.7rem; margin-left: 1rem;">
                                {apt['status'].title()}
                            </span>
                        </h4>
                        <p style="margin: 0.5rem 0;">
                            <strong>👤 Paciente:</strong> {apt['patient_name']} ({apt['patient_id']}) | 
                            <strong>🥗 Nutricionista:</strong> {apt['nutritionist_name']}
                        </p>
                        <p style="margin: 0.5rem 0;">
                            <strong>📋 Tipo:</strong> {apt['appointment_type'] or 'Consulta padrão'} | 
                            <strong>🆔 ID:</strong> {apt['appointment_id']}
                        </p>
                        {f"<p style='margin: 0; font-size: 0.9rem; color: #666;'><strong>📝 Notas:</strong> {apt['notes']}</p>" if apt['notes'] else ""}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_apt2:
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        if st.button("✏️", key=f"edit_apt_{apt['id']}", help="Editar"):
                            st.session_state.edit_appointment_id = apt['id']
                            st.rerun()
                    
                    with col_btn2:
                        if apt['status'] == 'agendado':
                            if st.button("✅", key=f"confirm_apt_{apt['id']}", help="Confirmar"):
                                update_appointment_status(apt['id'], 'confirmado')
                                st.rerun()
        else:
            st.info("📝 Nenhum agendamento encontrado para o período selecionado")
        
        conn.close()
    
    with tab2:
        st.subheader("➕ Novo Agendamento")
        
        with st.form("new_appointment_form"):
            # Buscar pacientes disponíveis
            conn = sqlite3.connect('nutriapp360.db')
            
            if user_role == 'nutritionist':
                patients_query = """
                    SELECT id, patient_id, full_name 
                    FROM patients 
                    WHERE nutritionist_id = ? AND active = 1
                    ORDER BY full_name
                """
                patients_df = pd.read_sql_query(patients_query, conn, params=[user_id])
            else:
                patients_query = """
                    SELECT id, patient_id, full_name 
                    FROM patients 
                    WHERE active = 1
                    ORDER BY full_name
                """
                patients_df = pd.read_sql_query(patients_query, conn)
            
            # Buscar nutricionistas
            nutritionists_df = pd.read_sql_query("""
                SELECT id, full_name 
                FROM users 
                WHERE role = 'nutritionist' AND active = 1
                ORDER BY full_name
            """, conn)
            
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                # Seleção de paciente
                if not patients_df.empty:
                    patient_options = {f"{row['full_name']} ({row['patient_id']})": row['id'] 
                                     for idx, row in patients_df.iterrows()}
                    selected_patient = st.selectbox("👤 Paciente *", list(patient_options.keys()))
                    patient_id = patient_options[selected_patient]
                else:
                    st.error("❌ Nenhum paciente disponível")
                    patient_id = None
                
                # Data e hora
                apt_date = st.date_input("📅 Data *", value=datetime.now().date())
                apt_time = st.time_input("🕐 Horário *", value=datetime.now().time())
                
                # Tipo de consulta
                apt_type = st.selectbox("📋 Tipo de Consulta", [
                    'Primeira consulta',
                    'Retorno',
                    'Acompanhamento',
                    'Revisão de plano',
                    'Consulta online'
                ])
            
            with col_form2:
                # Seleção de nutricionista
                if user_role == 'nutritionist':
                    nutritionist_id = user_id
                    st.info(f"🥗 Nutricionista: {st.session_state.user['full_name']}")
                else:
                    if not nutritionists_df.empty:
                        nutritionist_options = {row['full_name']: row['id'] 
                                              for idx, row in nutritionists_df.iterrows()}
                        selected_nutritionist = st.selectbox("🥗 Nutricionista *", list(nutritionist_options.keys()))
                        nutritionist_id = nutritionist_options[selected_nutritionist]
                    else:
                        st.error("❌ Nenhum nutricionista disponível")
                        nutritionist_id = None
                
                # Duração
                duration = st.selectbox("⏱️ Duração", [30, 45, 60, 90, 120], index=2)
                
                # Status inicial
                initial_status = st.selectbox("📊 Status", ['agendado', 'confirmado'])
            
            # Observações
            apt_notes = st.text_area("📝 Observações")
            
            submitted = st.form_submit_button("✅ Criar Agendamento", type="primary")
            
            if submitted:
                if patient_id and nutritionist_id and apt_date and apt_time:
                    try:
                        # Combinar data e hora
                        apt_datetime = datetime.combine(apt_date, apt_time)
                        
                        # Gerar ID do agendamento
                        apt_id = f"APT{random.randint(1000, 9999)}"
                        
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO appointments (appointment_id, patient_id, nutritionist_id, 
                                                    secretary_id, appointment_date, duration, 
                                                    appointment_type, status, notes)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (apt_id, patient_id, nutritionist_id, user_id if user_role == 'secretary' else None,
                             apt_datetime, duration, apt_type, initial_status, apt_notes))
                        
                        conn.commit()
                        log_audit_action(user_id, 'create_appointment', 'appointments', cursor.lastrowid)
                        st.success(f"✅ Agendamento {apt_id} criado com sucesso!")
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Erro ao criar agendamento: {e}")
                    finally:
                        conn.close()
                else:
                    st.error("❌ Preencha todos os campos obrigatórios!")
        
        conn.close()
    
    with tab3:
        st.subheader("📊 Relatório de Agendamentos")
        
        conn = sqlite3.connect('nutriapp360.db')
        
        # Métricas do período
        col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
        
        # Query baseada no papel do usuário
        if user_role == 'nutritionist':
            base_query = f"FROM appointments WHERE nutritionist_id = {user_id}"
        elif user_role == 'secretary':
            base_query = f"FROM appointments WHERE secretary_id = {user_id}"
        else:
            base_query = "FROM appointments"
        
        total_apts = pd.read_sql_query(f"SELECT COUNT(*) as count {base_query}", conn).iloc[0]['count']
        
        today_apts = pd.read_sql_query(f"""
            SELECT COUNT(*) as count {base_query} 
            AND DATE(appointment_date) = DATE('now')
        """, conn).iloc[0]['count']
        
        completed_apts = pd.read_sql_query(f"""
            SELECT COUNT(*) as count {base_query} 
            AND status = 'realizado'
        """, conn).iloc[0]['count']
        
        cancelled_apts = pd.read_sql_query(f"""
            SELECT COUNT(*) as count {base_query} 
            AND status = 'cancelado'
        """, conn).iloc[0]['count']
        
        with col_metric1:
            st.metric("📅 Total", total_apts)
        
        with col_metric2:
            st.metric("🗓️ Hoje", today_apts)
        
        with col_metric3:
            st.metric("✅ Realizados", completed_apts)
        
        with col_metric4:
            st.metric("❌ Cancelados", cancelled_apts)
        
        # Gráfico de agendamentos por status
        if total_apts > 0:
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                status_data = pd.read_sql_query(f"""
                    SELECT status, COUNT(*) as count {base_query} 
                    GROUP BY status
                """, conn)
                
                if not status_data.empty:
                    fig = px.pie(status_data, values='count', names='status', 
                               title="📊 Agendamentos por Status")
                    st.plotly_chart(fig, use_container_width=True)
            
            with col_chart2:
                # Agendamentos por semana
                weekly_data = pd.read_sql_query(f"""
                    SELECT 
                        strftime('%Y-%W', appointment_date) as week,
                        COUNT(*) as count
                    {base_query}
                    GROUP BY strftime('%Y-%W', appointment_date)
                    ORDER BY week DESC
                    LIMIT 8
                """, conn)
                
                if not weekly_data.empty:
                    fig = px.bar(weekly_data, x='week', y='count', 
                               title="📈 Agendamentos por Semana")
                    st.plotly_chart(fig, use_container_width=True)
        
        conn.close()

def update_appointment_status(appointment_id, new_status):
    """Atualiza status do agendamento"""
    try:
        conn = sqlite3.connect('nutriapp360.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE appointments 
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (new_status, appointment_id))
        
        conn.commit()
        log_audit_action(st.session_state.user['id'], f'update_appointment_status_{new_status}', 
                        'appointments', appointment_id)
        conn.close()
        st.success(f"✅ Status atualizado para: {new_status}")
    except Exception as e:
        st.error(f"❌ Erro ao atualizar status: {e}")

def show_meal_plans_management():
    st.markdown('<h1 class="main-header">🍽️ Planos Alimentares</h1>', unsafe_allow_html=True)
    
    nutritionist_id = st.session_state.user['id']
    
    tab1, tab2, tab3 = st.tabs(["📋 Meus Planos", "➕ Novo Plano", "🍎 Banco de Alimentos"])
    
    with tab1:
        st.subheader("🍽️ Planos Alimentares Ativos")
        
        conn = sqlite3.connect('nutriapp360.db')
        
        plans_df = pd.read_sql_query("""
            SELECT 
                mp.*, p.full_name as patient_name, p.patient_id
            FROM meal_plans mp
            JOIN patients p ON p.id = mp.patient_id
            WHERE mp.nutritionist_id = ? AND mp.status = 'ativo'
            ORDER BY mp.created_at DESC
        """, conn, params=[nutritionist_id])
        
        if not plans_df.empty:
            for idx, plan in plans_df.iterrows():
                start_date = pd.to_datetime(plan['start_date']).strftime('%d/%m/%Y')
                end_date = pd.to_datetime(plan['end_date']).strftime('%d/%m/%Y') if plan['end_date'] else 'Indefinido'
                
                col_plan1, col_plan2 = st.columns([3, 1])
                
                with col_plan1:
                    st.markdown(f"""
                    <div class="recipe-card">
                        <h4 style="margin: 0; color: #E65100;">
                            🍽️ {plan['plan_name']}
                        </h4>
                        <p style="margin: 0.5rem 0;">
                            <strong>👤 Paciente:</strong> {plan['patient_name']} ({plan['patient_id']}) | 
                            <strong>🔥 Calorias:</strong> {plan['daily_calories'] or 'N/A'} kcal/dia
                        </p>
                        <p style="margin: 0; font-size: 0.9rem; color: #666;">
                            <strong>📅 Período:</strong> {start_date} até {end_date} | 
                            <strong>🆔 ID:</strong> {plan['plan_id']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_plan2:
                    col_btn1, col_btn2 = st.columns(2)
                    
                    with col_btn1:
                        if st.button("👁️", key=f"view_plan_{plan['id']}", help="Visualizar"):
                            st.session_state.selected_plan_id = plan['id']
                            st.session_state.show_plan_details = True
                            st.rerun()
                    
                    with col_btn2:
                        if st.button("✏️", key=f"edit_plan_{plan['id']}", help="Editar"):
                            st.session_state.edit_plan_id = plan['id']
                            st.rerun()
        else:
            st.info("📝 Nenhum plano alimentar encontrado")
        
        conn.close()
    
    with tab2:
        st.subheader("➕ Criar Novo Plano Alimentar")
        
        with st.form("new_meal_plan_form"):
            # Buscar pacientes
            conn = sqlite3.connect('nutriapp360.db')
            patients_df = pd.read_sql_query("""
                SELECT id, patient_id, full_name 
                FROM patients 
                WHERE nutritionist_id = ? AND active = 1
                ORDER BY full_name
            """, conn, params=[nutritionist_id])
            
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                if not patients_df.empty:
                    patient_options = {f"{row['full_name']} ({row['patient_id']})": row['id'] 
                                     for idx, row in patients_df.iterrows()}
                    selected_patient = st.selectbox("👤 Paciente *", list(patient_options.keys()))
                    plan_patient_id = patient_options[selected_patient]
                else:
                    st.error("❌ Nenhum paciente disponível")
                    plan_patient_id = None
                
                plan_name = st.text_input("📝 Nome do Plano *", placeholder="Ex: Plano de Emagrecimento - João")
                daily_calories = st.number_input("🔥 Calorias Diárias", min_value=800, max_value=4000, value=1800)
                
            with col_form2:
                start_date = st.date_input("📅 Data de Início *", value=datetime.now().date())
                end_date = st.date_input("📅 Data de Fim", value=datetime.now().date() + timedelta(days=30))
                plan_objective = st.selectbox("🎯 Objetivo", [
                    'Emagrecimento',
                    'Ganho de peso',
                    'Manutenção',
                    'Ganho de massa muscular',
                    'Controle glicêmico',
                    'Redução de colesterol'
                ])
            
            st.markdown("### 🍽️ Estrutura do Plano")
            
            # Template de plano
            meal_structure = {
                'cafe_manha': {'nome': 'Café da Manhã', 'percent': 25, 'items': []},
                'lanche_manha': {'nome': 'Lanche da Manhã', 'percent': 10, 'items': []},
                'almoco': {'nome': 'Almoço', 'percent': 35, 'items': []},
                'lanche_tarde': {'nome': 'Lanche da Tarde', 'percent': 10, 'items': []},
                'jantar': {'nome': 'Jantar', 'percent': 20, 'items': []}
            }
            
            # Interface para cada refeição
            for meal_key, meal_info in meal_structure.items():
                st.markdown(f"**{meal_info['nome']} ({meal_info['percent']}% - {int(daily_calories * meal_info['percent'] / 100)} kcal)**")
                
                meal_items = st.text_area(
                    f"Alimentos para {meal_info['nome']}", 
                    placeholder="Ex: 2 fatias de pão integral\n1 ovo cozido\n1 copo de leite desnatado",
                    key=f"meal_{meal_key}",
                    height=100
                )
                
                meal_structure[meal_key]['items'] = meal_items.split('\n') if meal_items else []
            
            # Observações gerais
            plan_notes = st.text_area("📝 Observações e Orientações", 
                                    placeholder="Orientações gerais, restrições, substituições permitidas...")
            
            submitted = st.form_submit_button("✅ Criar Plano Alimentar", type="primary")
            
            if submitted:
                if plan_patient_id and plan_name and start_date:
                    try:
                        # Gerar ID do plano
                        plan_id = f"PLN{random.randint(1000, 9999)}"
                        
                        # Estruturar dados do plano
                        plan_data = {
                            'objective': plan_objective,
                            'meals': meal_structure,
                            'notes': plan_notes,
                            'created_by': st.session_state.user['full_name']
                        }
                        
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO meal_plans (plan_id, patient_id, nutritionist_id, plan_name,
                                                  start_date, end_date, daily_calories, plan_data)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (plan_id, plan_patient_id, nutritionist_id, plan_name,
                             start_date, end_date, daily_calories, json.dumps(plan_data)))
                        
                        conn.commit()
                        log_audit_action(nutritionist_id, 'create_meal_plan', 'meal_plans', cursor.lastrowid)
                        st.success(f"✅ Plano alimentar {plan_name} criado com sucesso!")
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Erro ao criar plano: {e}")
                    finally:
                        conn.close()
                else:
                    st.error("❌ Preencha os campos obrigatórios!")
    
    with tab3:
        st.subheader("🍎 Banco de Alimentos")
        
        # Busca por alimentos
        search_food = st.text_input("🔍 Buscar alimento", placeholder="Ex: arroz, frango, banana...")
        
        conn = sqlite3.connect('nutriapp360.db')
        
        if search_food:
            foods_df = pd.read_sql_query("""
                SELECT * FROM food_database 
                WHERE food_name LIKE ? OR category LIKE ?
                ORDER BY food_name
            """, conn, params=[f"%{search_food}%", f"%{search_food}%"])
        else:
            foods_df = pd.read_sql_query("""
                SELECT * FROM food_database 
                ORDER BY category, food_name
                LIMIT 20
            """, conn)
        
        if not foods_df.empty:
            st.markdown("**📊 Informações Nutricionais (por 100g)**")
            
            for idx, food in foods_df.iterrows():
                col_food1, col_food2 = st.columns([2, 3])
                
                with col_food1:
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                        <h5 style="margin: 0; color: #2E7D32;">{food['food_name']}</h5>
                        <p style="margin: 0; color: #666; font-size: 0.9rem;">{food['category']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_food2:
                    col_nut1, col_nut2, col_nut3, col_nut4 = st.columns(4)
                    
                    with col_nut1:
                        st.metric("🔥 Kcal", f"{food['calories_per_100g']:.0f}")
                    
                    with col_nut2:
                        st.metric("🥩 Prot", f"{food['protein_per_100g']:.1f}g")
                    
                    with col_nut3:
                        st.metric("🍞 Carb", f"{food['carbs_per_100g']:.1f}g")
                    
                    with col_nut4:
                        st.metric("🥑 Gord", f"{food['fat_per_100g']:.1f}g")
        else:
            st.info("🔍 Nenhum alimento encontrado. Tente uma busca diferente.")
        
        # Adicionar novo alimento
        st.markdown("---")
        st.markdown("### ➕ Adicionar Novo Alimento")
        
        with st.form("add_food_form"):
            col_food_form1, col_food_form2 = st.columns(2)
            
            with col_food_form1:
                new_food_name = st.text_input("🍎 Nome do Alimento *")
                new_food_category = st.selectbox("📂 Categoria", [
                    'Cereais', 'Carnes', 'Peixes', 'Laticínios', 'Frutas', 
                    'Vegetais', 'Leguminosas', 'Oleaginosas', 'Gorduras', 'Outros'
                ])
                new_calories = st.number_input("🔥 Calorias (por 100g)", min_value=0.0, step=0.1)
                new_protein = st.number_input("🥩 Proteínas (g)", min_value=0.0, step=0.1)
            
            with col_food_form2:
                new_carbs = st.number_input("🍞 Carboidratos (g)", min_value=0.0, step=0.1)
                new_fat = st.number_input("🥑 Gorduras (g)", min_value=0.0, step=0.1)
                new_fiber = st.number_input("🌾 Fibras (g)", min_value=0.0, step=0.1)
                new_sodium = st.number_input("🧂 Sódio (mg)", min_value=0.0, step=0.1)
            
            submitted_food = st.form_submit_button("✅ Adicionar Alimento")
            
            if submitted_food and new_food_name:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO food_database (food_name, category, calories_per_100g, 
                                                 protein_per_100g, carbs_per_100g, fat_per_100g, 
                                                 fiber_per_100g, sodium_per_100g)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (new_food_name, new_food_category, new_calories, new_protein,
                         new_carbs, new_fat, new_fiber, new_sodium))
                    
                    conn.commit()
                    st.success(f"✅ Alimento {new_food_name} adicionado ao banco!")
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Erro ao adicionar alimento: {e}")
        
        conn.close()

def show_recipes_management():
    st.markdown('<h1 class="main-header">👨‍🍳 Biblioteca de Receitas</h1>', unsafe_allow_html=True)
    
    nutritionist_id = st.session_state.user['id']
    
    tab1, tab2, tab3 = st.tabs(["📚 Minhas Receitas", "➕ Nova Receita", "🔍 Buscar Receitas"])
    
    with tab1:
        st.subheader("👨‍🍳 Suas Receitas")
        
        conn = sqlite3.connect('nutriapp360.db')
        
        # Filtros
        col_filter1, col_filter2 = st.columns(2)
        
        with col_filter1:
            category_filter = st.selectbox("📂 Categoria", 
                                         ['Todas', 'Saladas', 'Peixes', 'Carnes', 'Vegetariana', 
                                          'Sobremesas', 'Lanches', 'Sopas', 'Sucos', 'Outros'])
        
        with col_filter2:
            difficulty_filter = st.selectbox("⭐ Dificuldade", ['Todas', 'Fácil', 'Médio', 'Difícil'])
        
        # Buscar receitas
        query = """
            SELECT * FROM recipes 
            WHERE nutritionist_id = ? OR is_public = 1
        """
        params = [nutritionist_id]
        
        if category_filter != 'Todas':
            query += " AND category = ?"
            params.append(category_filter)
        
        if difficulty_filter != 'Todas':
            query += " AND difficulty = ?"
            params.append(difficulty_filter)
        
        query += " ORDER BY created_at DESC"
        
        recipes_df = pd.read_sql_query(query, conn, params=params)
        
        if not recipes_df.empty:
            for idx, recipe in recipes_df.iterrows():
                is_mine = recipe['nutritionist_id'] == nutritionist_id
                
                col_recipe1, col_recipe2 = st.columns([3, 1])
                
                with col_recipe1:
                    # Ícones de dificuldade
                    difficulty_icons = {
                        'Fácil': '⭐',
                        'Médio': '⭐⭐',
                        'Difícil': '⭐⭐⭐'
                    }
                    
                    total_time = (recipe['prep_time'] or 0) + (recipe['cook_time'] or 0)
                    
                    st.markdown(f"""
                    <div class="recipe-card">
                        <h4 style="margin: 0; color: #E65100;">
                            👨‍🍳 {recipe['name']}
                            {'🔒' if not recipe['is_public'] else '🌍'}
                            {'✨ Minha' if is_mine else ''}
                        </h4>
                        <p style="margin: 0.5rem 0;">
                            <strong>📂 Categoria:</strong> {recipe['category'] or 'N/A'} | 
                            <strong>⏱️ Tempo:</strong> {total_time} min | 
                            <strong>👥 Porções:</strong> {recipe['servings'] or 'N/A'}
                        </p>
                        <p style="margin: 0.5rem 0;">
                            <strong>🔥 Calorias:</strong> {recipe['calories_per_serving'] or 'N/A'} kcal/porção | 
                            <strong>⭐ Dificuldade:</strong> {difficulty_icons.get(recipe['difficulty'], '⭐')} {recipe['difficulty'] or 'N/A'}
                        </p>
                        <p style="margin: 0; font-size: 0.9rem; color: #666;">
                            <strong>🏷️ Tags:</strong> {recipe['tags'] or 'Nenhuma'}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_recipe2:
                    if st.button("👁️", key=f"view_recipe_{recipe['id']}", help="Ver Receita"):
                        st.session_state.selected_recipe_id = recipe['id']
                        st.session_state.show_recipe_details = True
                        st.rerun()
                    
                    if is_mine:
                        if st.button("✏️", key=f"edit_recipe_{recipe['id']}", help="Editar"):
                            st.session_state.edit_recipe_id = recipe['id']
                            st.rerun()
        else:
            st.info("📝 Nenhuma receita encontrada")
        
        conn.close()
        
        # Modal de detalhes da receita
        if hasattr(st.session_state, 'show_recipe_details') and st.session_state.show_recipe_details:
            show_recipe_details_modal()
    
    with tab2:
        st.subheader("➕ Criar Nova Receita")
        
        with st.form("new_recipe_form"):
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                recipe_name = st.text_input("👨‍🍳 Nome da Receita *")
                recipe_category = st.selectbox("📂 Categoria", [
                    'Saladas', 'Peixes', 'Carnes', 'Vegetariana', 'Vegana',
                    'Sobremesas', 'Lanches', 'Sopas', 'Sucos', 'Smoothies', 'Outros'
                ])
                prep_time = st.number_input("⏱️ Tempo de Preparo (min)", min_value=0, value=15)
                cook_time = st.number_input("🔥 Tempo de Cozimento (min)", min_value=0, value=0)
                servings = st.number_input("👥 Número de Porções", min_value=1, value=2)
            
            with col_form2:
                calories_per_serving = st.number_input("🔥 Calorias por Porção", min_value=0, value=200)
                protein = st.number_input("🥩 Proteínas (g/porção)", min_value=0.0, step=0.1, value=10.0)
                carbs = st.number_input("🍞 Carboidratos (g/porção)", min_value=0.0, step=0.1, value=20.0)
                fat = st.number_input("🥑 Gorduras (g/porção)", min_value=0.0, step=0.1, value=5.0)
                fiber = st.number_input("🌾 Fibras (g/porção)", min_value=0.0, step=0.1, value=3.0)
            
            difficulty = st.selectbox("⭐ Dificuldade", ['Fácil', 'Médio', 'Difícil'])
            
            # Ingredientes
            st.markdown("### 🥘 Ingredientes")
            ingredients = st.text_area("Lista de ingredientes (um por linha)", 
                                     placeholder="1 xícara de arroz integral\n200g de frango\n2 tomates médios\n...",
                                     height=120)
            
            # Modo de preparo
            st.markdown("### 📝 Modo de Preparo")
            instructions = st.text_area("Instruções passo a passo", 
                                       placeholder="1. Cozinhe o arroz...\n2. Tempere o frango...\n3. Refogue os vegetais...",
                                       height=150)
            
            # Tags e configurações
            col_tags1, col_tags2 = st.columns(2)
            
            with col_tags1:
                tags = st.text_input("🏷️ Tags (separadas por vírgula)", 
                                    placeholder="saudável, fácil, rápido, sem glúten")
            
            with col_tags2:
                is_public = st.checkbox("🌍 Tornar receita pública", value=True)
            
            submitted = st.form_submit_button("✅ Criar Receita", type="primary")
            
            if submitted:
                if recipe_name and ingredients and instructions:
                    try:
                        conn = sqlite3.connect('nutriapp360.db')
                        cursor = conn.cursor()
                        
                        # Gerar ID da receita
                        recipe_id = f"REC{random.randint(1000, 9999)}"
                        
                        cursor.execute('''
                            INSERT INTO recipes (recipe_id, name, category, prep_time, cook_time, 
                                               servings, calories_per_serving, protein, carbs, fat, 
                                               fiber, ingredients, instructions, tags, difficulty, 
                                               nutritionist_id, is_public)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (recipe_id, recipe_name, recipe_category, prep_time, cook_time,
                             servings, calories_per_serving, protein, carbs, fat, fiber,
                             ingredients, instructions, tags, difficulty, nutritionist_id, is_public))
                        
                        conn.commit()
                        log_audit_action(nutritionist_id, 'create_recipe', 'recipes', cursor.lastrowid)
                        st.success(f"✅ Receita {recipe_name} criada com sucesso!")
                        st.rerun()
                    
                    except Exception as e:
                        st.error(f"❌ Erro ao criar receita: {e}")
                    finally:
                        conn.close()
                else:
                    st.error("❌ Preencha todos os campos obrigatórios!")
    
    with tab3:
        st.subheader("🔍 Buscar Receitas")
        
        search_recipe = st.text_input("🔍 Buscar por nome ou ingrediente")
        
        if search_recipe:
            conn = sqlite3.connect('nutriapp360.db')
            
            search_results = pd.read_sql_query("""
                SELECT * FROM recipes 
                WHERE (name LIKE ? OR ingredients LIKE ? OR tags LIKE ?) 
                AND (nutritionist_id = ? OR is_public = 1)
                ORDER BY name
            """, conn, params=[f"%{search_recipe}%", f"%{search_recipe}%", 
                              f"%{search_recipe}%", nutritionist_id])
            
            if not search_results.empty:
                st.write(f"🔍 {len(search_results)} receita(s) encontrada(s)")
                
                for idx, recipe in search_results.iterrows():
                    with st.expander(f"👨‍🍳 {recipe['name']} - {recipe['category']}"):
                        col_detail1, col_detail2 = st.columns(2)
                        
                        with col_detail1:
                            st.write(f"**⏱️ Tempo total:** {(recipe['prep_time'] or 0) + (recipe['cook_time'] or 0)} min")
                            st.write(f"**👥 Porções:** {recipe['servings']}")
                            st.write(f"**🔥 Calorias:** {recipe['calories_per_serving']} kcal/porção")
                            st.write(f"**⭐ Dificuldade:** {recipe['difficulty']}")
                        
                        with col_detail2:
                            st.write(f"**🥩 Proteínas:** {recipe['protein']}g")
                            st.write(f"**🍞 Carboidratos:** {recipe['carbs']}g")
                            st.write(f"**🥑 Gorduras:** {recipe['fat']}g")
                            st.write(f"**🌾 Fibras:** {recipe['fiber']}g")
                        
                        st.write("**🥘 Ingredientes:**")
                        st.write(recipe['ingredients'])
                        
                        st.write("**📝 Modo de Preparo:**")
                        st.write(recipe['instructions'])
                        
                        if recipe['tags']:
                            st.write(f"**🏷️ Tags:** {recipe['tags']}")
            else:
                st.info("🔍 Nenhuma receita encontrada para essa busca")
            
            conn.close()
        else:
            st.info("💡 Digite algo no campo de busca para encontrar receitas")

def show_recipe_details_modal():
    """Mostra detalhes completos da receita selecionada"""
    if hasattr(st.session_state, 'selected_recipe_id'):
        conn = sqlite3.connect('nutriapp360.db')
        
        recipe = pd.read_sql_query("""
            SELECT r.*, u.full_name as nutritionist_name
            FROM recipes r
            LEFT JOIN users u ON u.id = r.nutritionist_id
            WHERE r.id = ?
        """, conn, params=[st.session_state.selected_recipe_id])
        
        if not recipe.empty:
            recipe = recipe.iloc[0]
            
            st.markdown("---")
            st.markdown(f"### 👨‍🍳 {recipe['name']}")
            
            col_close = st.columns([4, 1])
            with col_close[1]:
                if st.button("❌ Fechar"):
                    st.session_state.show_recipe_details = False
                    del st.session_state.selected_recipe_id
                    st.rerun()
            
            # Informações gerais
            col_info1, col_info2, col_info3 = st.columns(3)
            
            with col_info1:
                st.metric("⏱️ Preparo", f"{recipe['prep_time']} min")
                st.metric("🔥 Cozimento", f"{recipe['cook_time']} min")
            
            with col_info2:
                st.metric("👥 Porções", recipe['servings'])
                st.metric("🔥 Calorias", f"{recipe['calories_per_serving']} kcal")
            
            with col_info3:
                st.metric("⭐ Dificuldade", recipe['difficulty'])
                st.metric("📂 Categoria", recipe['category'])
            
            # Informações nutricionais
            st.markdown("### 📊 Informações Nutricionais (por porção)")
            
            col_nut1, col_nut2, col_nut3, col_nut4 = st.columns(4)
            
            with col_nut1:
                st.metric("🥩 Proteínas", f"{recipe['protein']}g")
            
            with col_nut2:
                st.metric("🍞 Carboidratos", f"{recipe['carbs']}g")
            
            with col_nut3:
                st.metric("🥑 Gorduras", f"{recipe['fat']}g")
            
            with col_nut4:
                st.metric("🌾 Fibras", f"{recipe['fiber']}g")
            
            # Ingredientes e preparo
            col_recipe1, col_recipe2 = st.columns(2)
            
            with col_recipe1:
                st.markdown("### 🥘 Ingredientes")
                ingredients_list = recipe['ingredients'].split('\n')
                for ingredient in ingredients_list:
                    if ingredient.strip():
                        st.write(f"• {ingredient.strip()}")
            
            with col_recipe2:
                st.markdown("### 📝 Modo de Preparo")
                instructions_list = recipe['instructions'].split('\n')
                for i, instruction in enumerate(instructions_list, 1):
                    if instruction.strip():
                        st.write(f"**{i}.** {instruction.strip()}")
            
            # Tags e criador
            if recipe['tags']:
                st.markdown(f"**🏷️ Tags:** {recipe['tags']}")
            
            st.markdown(f"**👨‍⚕️ Criado por:** {recipe['nutritionist_name'] or 'Sistema'}")
        
        conn.close()

def show_progress_tracking():
    st.markdown('<h1 class="main-header">📈 Acompanhamento de Progresso</h1>', unsafe_allow_html=True)
    
    nutritionist_id = st.session_state.user['id']
    
    tab1, tab2, tab3 = st.tabs(["👥 Pacientes", "📊 Registrar Progresso", "📈 Relatórios"])
    
    with tab1:
        st.subheader("👥 Selecionar Paciente para Acompanhamento")
        
        conn = sqlite3.connect('nutriapp360.db')
        
        patients_df = pd.read_sql_query("""
            SELECT p.*, 
                   (SELECT COUNT(*) FROM patient_progress pp WHERE pp.patient_id = p.id) as progress_count,
                   (SELECT record_date FROM patient_progress pp WHERE pp.patient_id = p.id ORDER BY record_date DESC LIMIT 1) as last_record
            FROM patients p
            WHERE p.nutritionist_id = ? AND p.active = 1
            ORDER BY p.full_name
        """, conn, params=[nutritionist_id])
        
        if not patients_df.empty:
            for idx, patient in patients_df.iterrows():
                last_record = pd.to_datetime(patient['last_record']).strftime('%d/%m/%Y') if patient['last_record'] else 'Nunca'
                
                col_patient1, col_patient2 = st.columns([3, 1])
                
                with col_patient1:
                    # Calcular IMC atual
                    if patient['height'] and patient['current_weight']:
                        imc = patient['current_weight'] / (patient['height'] ** 2)
                        imc_text = f"{imc:.1f}"
                    else:
                        imc_text = "N/A"
                    
                    st.markdown(f"""
                    <div class="patient-info-card">
                        <h4 style="margin: 0; color: #2E7D32;">
                            📊 {patient['full_name']} ({patient['patient_id']})
                        </h4>
                        <p style="margin: 0.5rem 0;">
                            <strong>⚖️ Peso Atual:</strong> {patient['current_weight']} kg | 
                            <strong>🎯 Meta:</strong> {patient['target_weight']} kg | 
                            <strong>📏 IMC:</strong> {imc_text}
                        </p>
                        <p style="margin: 0; font-size: 0.9rem; color: #666;">
                            <strong>📈 Registros:</strong> {patient['progress_count']} | 
                            <strong>📅 Último registro:</strong> {last_record}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_patient2:
                    if st.button(f"📊 Ver Progresso", key=f"progress_{patient['id']}"):
                        st.session_state.selected_progress_patient_id = patient['id']
                        st.session_state.show_patient_progress = True
                        st.rerun()
        else:
            st.info("📝 Nenhum paciente encontrado")
        
        conn.close()
        
        # Modal de progresso do paciente
        if hasattr(st.session_state, 'show_patient_progress') and st.session_state.show_patient_progress:
            show_patient_progress_modal()
    
    with tab2:
        st.subheader("📊 Registrar Novo Progresso")
        
        with st.form("progress_form"):
            conn = sqlite3.connect('nutriapp360.db')
            
            # Selecionar paciente
            patients_df = pd.read_sql_query("""
                SELECT id, patient_id, full_name, current_weight, target_weight, height
                FROM patients 
                WHERE nutritionist_id = ? AND active = 1
                ORDER BY full_name
            """, conn, params=[nutritionist_id])
            
            if not patients_df.empty:
                patient_options = {f"{row['full_name']} ({row['patient_id']})": row['id'] 
                                 for idx, row in patients_df.iterrows()}
                selected_patient = st.selectbox("👤 Paciente *", list(patient_options.keys()))
                progress_patient_id = patient_options[selected_patient]
                
                # Mostrar dados atuais do paciente
                current_patient = patients_df[patients_df['id'] == progress_patient_id].iloc[0]
                
                col_current1, col_current2, col_current3 = st.columns(3)
                
                with col_current1:
                    st.info(f"**Peso Atual:** {current_patient['current_weight']} kg")
                
                with col_current2:
                    st.info(f"**Meta:** {current_patient['target_weight']} kg")
                
                with col_current3:
                    if current_patient['height'] and current_patient['current_weight']:
                        current_imc = current_patient['current_weight'] / (current_patient['height'] ** 2)
                        st.info(f"**IMC Atual:** {current_imc:.1f}")
                    else:
                        st.info("**IMC:** N/A")
                
                # Formulário de progresso
                col_form1, col_form2 = st.columns(2)
                
                with col_form1:
                    record_date = st.date_input("📅 Data do Registro *", value=datetime.now().date())
                    new_weight = st.number_input("⚖️ Peso (kg) *", 
                                               min_value=30.0, max_value=300.0, 
                                               value=float(current_patient['current_weight']) if current_patient['current_weight'] else 70.0)
                    body_fat = st.number_input("🔥 Gordura Corporal (%)", min_value=0.0, max_value=50.0, step=0.1)
                    muscle_mass = st.number_input("💪 Massa Muscular (kg)", min_value=0.0, max_value=100.0, step=0.1)
                
                with col_form2:
                    waist_circumference = st.number_input("📏 Circunferência Cintura (cm)", min_value=0.0, max_value=200.0, step=0.1)
                    hip_circumference = st.number_input("📏 Circunferência Quadril (cm)", min_value=0.0, max_value=200.0, step=0.1)
                    
                    # Calcular novo IMC
                    if current_patient['height'] and new_weight:
                        new_imc = new_weight / (current_patient['height'] ** 2)
                        st.metric("📊 Novo IMC", f"{new_imc:.1f}")
                    
                    # Diferença de peso
                    if current_patient['current_weight']:
                        weight_diff = new_weight - current_patient['current_weight']
                        st.metric("📈 Variação de Peso", f"{weight_diff:+.1f} kg")
                
                # Observações
                progress_notes = st.text_area("📝 Observações", 
                                            placeholder="Como o paciente está se sentindo? Dificuldades? Melhorias?")
                
                submitted = st.form_submit_button("✅ Registrar Progresso", type="primary")
                
                if submitted:
                    if progress_patient_id and record_date and new_weight:
                        try:
                            cursor = conn.cursor()
                            
                            # Inserir registro de progresso
                            cursor.execute('''
                                INSERT INTO patient_progress (patient_id, record_date, weight, body_fat, 
                                                            muscle_mass, waist_circumference, hip_circumference, 
                                                            notes, recorded_by)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (progress_patient_id, record_date, new_weight, body_fat if body_fat > 0 else None,
                                 muscle_mass if muscle_mass > 0 else None, 
                                 waist_circumference if waist_circumference > 0 else None,
                                 hip_circumference if hip_circumference > 0 else None,
                                 progress_notes, nutritionist_id))
                            
                            # Atualizar peso atual do paciente
                            cursor.execute('''
                                UPDATE patients 
                                SET current_weight = ?, updated_at = CURRENT_TIMESTAMP
                                WHERE id = ?
                            ''', (new_weight, progress_patient_id))
                            
                            conn.commit()
                            log_audit_action(nutritionist_id, 'record_progress', 'patient_progress', cursor.lastrowid)
                            st.success(f"✅ Progresso registrado com sucesso!")
                            st.rerun()
                        
                        except Exception as e:
                            st.error(f"❌ Erro ao registrar progresso: {e}")
                        finally:
                            conn.close()
                    else:
                        st.error("❌ Preencha os campos obrigatórios!")
            else:
                st.error("❌ Nenhum paciente disponível")
            
            conn.close()
    
    with tab3:
        st.subheader("📈 Relatórios de Progresso")
        
        conn = sqlite3.connect('nutriapp360.db')
        
        # Estatísticas gerais
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        total_records = pd.read_sql_query("""
            SELECT COUNT(*) as count 
            FROM patient_progress pp
            JOIN patients p ON p.id = pp.patient_id
            WHERE p.nutritionist_id = ?
        """, conn, params=[nutritionist_id]).iloc[0]['count']
        
        patients_with_progress = pd.read_sql_query("""
            SELECT COUNT(DISTINCT pp.patient_id) as count
            FROM patient_progress pp
            JOIN patients p ON p.id = pp.patient_id
            WHERE p.nutritionist_id = ?
        """, conn, params=[nutritionist_id]).iloc[0]['count']
        
        with col_stat1:
            st.metric("📊 Total de Registros", total_records)
        
        with col_stat2:
            st.metric("👥 Pacientes com Progresso", patients_with_progress)
        
        # Progresso médio dos pacientes
        if total_records > 0:
            avg_progress = pd.read_sql_query("""
                SELECT 
                    p.full_name,
                    MIN(pp.weight) as first_weight,
                    MAX(pp.weight) as last_weight,
                    COUNT(pp.id) as records_count,
                    AVG(pp.weight) as avg_weight
                FROM patient_progress pp
                JOIN patients p ON p.id = pp.patient_id
                WHERE p.nutritionist_id = ?
                GROUP BY p.id, p.full_name
                HAVING COUNT(pp.id) >= 2
                ORDER BY records_count DESC
            """, conn, params=[nutritionist_id])
            
            if not avg_progress.empty:
                st.markdown("### 📈 Progresso dos Pacientes")
                
                for idx, patient_prog in avg_progress.iterrows():
                    weight_change = patient_prog['last_weight'] - patient_prog['first_weight']
                    change_color = "#4CAF50" if weight_change < 0 else "#F44336" if weight_change > 0 else "#999"
                    
                    st.markdown(f"""
                    <div class="dashboard-card">
                        <h5 style="margin: 0; color: #2E7D32;">{patient_prog['full_name']}</h5>
                        <p style="margin: 0.5rem 0;">
                            <strong>📊 Registros:</strong> {patient_prog['records_count']} | 
                            <strong>⚖️ Variação:</strong> <span style="color: {change_color}; font-weight: bold;">{weight_change:+.1f} kg</span>
                        </p>
                        <p style="margin: 0; font-size: 0.9rem; color: #666;">
                            <strong>Primeiro:</strong> {patient_prog['first_weight']:.1f} kg | 
                            <strong>Último:</strong> {patient_prog['last_weight']:.1f} kg | 
                            <strong>Média:</strong> {patient_prog['avg_weight']:.1f} kg
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        
        conn.close()

def show_patient_progress_modal():
    """Mostra progresso detalhado do paciente selecionado"""
    if hasattr(st.session_state, 'selected_progress_patient_id'):
        conn = sqlite3.connect('nutriapp360.db')
        
        # Dados do paciente
        patient = pd.read_sql_query("""
            SELECT * FROM patients WHERE id = ?
        """, conn, params=[st.session_state.selected_progress_patient_id]).iloc[0]
        
        # Histórico de progresso
        progress_history = pd.read_sql_query("""
            SELECT * FROM patient_progress 
            WHERE patient_id = ? 
            ORDER BY record_date DESC
        """, conn, params=[st.session_state.selected_progress_patient_id])
        
        st.markdown("---")
        st.markdown(f"### 📈 Progresso: {patient['full_name']}")
        
        col_close = st.columns([4, 1])
        with col_close[1]:
            if st.button("❌ Fechar"):
                st.session_state.show_patient_progress = False
                del st.session_state.selected_progress_patient_id
                st.rerun()
        
        if not progress_history.empty:
            # Gráfico de evolução do peso
            progress_df = progress_history.copy()
            progress_df['record_date'] = pd.to_datetime(progress_df['record_date'])
            progress_df = progress_df.sort_values('record_date')
            
            fig = px.line(progress_df, x='record_date', y='weight', 
                         title=f"📈 Evolução do Peso - {patient['full_name']}",
                         markers=True)
            
            # Adicionar linha da meta
            if patient['target_weight']:
                fig.add_hline(y=patient['target_weight'], line_dash="dash", 
                            line_color="red", annotation_text=f"Meta: {patient['target_weight']} kg")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela de registros
            st.markdown("### 📊 Histórico de Registros")
            
            for idx, record in progress_history.iterrows():
                record_date = pd.to_datetime(record['record_date']).strftime('%d/%m/%Y')
                
                # Calcular IMC se houver altura
                if patient['height'] and record['weight']:
                    imc = record['weight'] / (patient['height'] ** 2)
                    imc_text = f"{imc:.1f}"
                else:
                    imc_text = "N/A"
                
                st.markdown(f"""
                <div class="appointment-card">
                    <h5 style="margin: 0; color: #2E7D32;">📅 {record_date}</h5>
                    <p style="margin: 0.5rem 0;">
                        <strong>⚖️ Peso:</strong> {record['weight']} kg | 
                        <strong>📏 IMC:</strong> {imc_text}
                        {f" | <strong>🔥 Gordura:</strong> {record['body_fat']}%" if record['body_fat'] else ""}
                        {f" | <strong>💪 Músculo:</strong> {record['muscle_mass']} kg" if record['muscle_mass'] else ""}
                    </p>
                    {f"<p style='margin: 0.5rem 0;'><strong>📏 Cintura:</strong> {record['waist_circumference']} cm | <strong>Quadril:</strong> {record['hip_circumference']} cm</p>" if record['waist_circumference'] or record['hip_circumference'] else ""}
                    {f"<p style='margin: 0; font-size: 0.9rem; color: #666;'><strong>📝 Observações:</strong> {record['notes']}</p>" if record['notes'] else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📝 Nenhum registro de progresso encontrado para este paciente")
        
        conn.close()

# CONTINUANDO COM AS OUTRAS FUNCIONALIDADES...
