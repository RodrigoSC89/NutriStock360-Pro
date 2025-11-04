# ❓ FAQ - Perguntas Frequentes

Respostas para as perguntas mais comuns sobre o NutriStock360-Pro.

---

## 📅 Acesso e Disponibilidade

### Quando posso acessar o sistema?
**✅ AGORA!** O sistema está 100% funcional e disponível para uso imediato. Você pode:
- Executar localmente em seu computador (5 minutos)
- Fazer deploy no Railway para uso em produção (30-45 minutos)

Consulte o [Quick Start Guide](QUICKSTART.md) ou [ACESSO.md](ACESSO.md) para instruções.

### O sistema está pronto para uso em produção?
**Sim**, todas as funcionalidades principais estão implementadas e testadas:
- ✅ Sistema multiusuário
- ✅ Gestão de pacientes
- ✅ Planos alimentares
- ✅ Avaliações antropométricas
- ✅ Agendamento de consultas
- ✅ Dashboard com métricas
- ✅ Base de alimentos brasileiros
- ✅ Calculadora nutricional

### Existe ambiente de testes/homologação?
**Sim**, você pode testar de várias formas:
1. **Local**: Execute em seu computador com `streamlit run main.py`
2. **Railway Staging**: Configure um ambiente separado no Railway
3. **Dados de demonstração**: O sistema já vem com pacientes e dados exemplo

### Como acompanhar as novidades e atualizações?
- **GitHub**: Acompanhe commits no repositório
- **ROADMAP.md**: Veja funcionalidades planejadas
- **Releases**: Novas versões serão publicadas como releases
- **Issues**: Participe das discussões

---

## 🔧 Instalação e Configuração

### Quais são os requisitos do sistema?
**Para uso local**:
- Python 3.8 ou superior
- 2GB de RAM (recomendado 4GB)
- 500MB de espaço em disco
- Navegador web moderno

**Para deploy no Railway**:
- Conta GitHub (gratuita)
- Conta Railway (gratuita)

### Como instalo o sistema localmente?
```bash
# 1. Clone o repositório
git clone https://github.com/RodrigoSC89/NutriStock360-Pro.git
cd NutriStock360-Pro

# 2. Instale dependências
pip install -r requirements.txt

# 3. Execute
streamlit run main.py
```

Acesse: http://localhost:8501

### Quanto custa usar o sistema?
**Uso local**: Gratuito (apenas custos do seu hardware)

**Deploy no Railway**:
- $5 de créditos gratuitos iniciais
- Após créditos: ~$5-10/mês para uso básico
- PostgreSQL incluído no plano

**Alternativas gratuitas**:
- Streamlit Cloud (limitações de recursos)
- Heroku free tier (descontinuado)
- Hospedar localmente sem custos

### Preciso de conhecimentos técnicos?
**Para usar o sistema**: Não, interface intuitiva e amigável

**Para fazer deploy**: Conhecimentos básicos ajudam, mas temos guia passo a passo completo no arquivo [guia](guia)

### Qual banco de dados o sistema usa?
- **Local**: SQLite (arquivo `.db`, sem configuração necessária)
- **Railway**: PostgreSQL (configuração automática) ou SQLite

---

## 🔐 Segurança e Privacidade

### Os dados ficam seguros?
**Sim**, o sistema implementa várias camadas de segurança:
- ✅ Senhas criptografadas com SHA-256
- ✅ Autenticação obrigatória
- ✅ Isolamento de dados por usuário
- ✅ Sessões seguras
- ✅ Sem compartilhamento entre nutricionistas

### Onde os dados são armazenados?
- **Local**: No arquivo `nutristock360.db` no seu computador
- **Railway**: No banco PostgreSQL hospedado no Railway

### Como faço backup dos dados?
**Local**: 
```bash
# Copie o arquivo do banco de dados
cp nutristock360.db nutristock360_backup_$(date +%Y%m%d).db
```

**Railway**: Configure backups automáticos do PostgreSQL através do painel do Railway

### O sistema é LGPD compliant?
O sistema fornece as ferramentas técnicas necessárias, mas a conformidade total depende de:
- Políticas de privacidade do consultório
- Termo de consentimento dos pacientes
- Procedimentos de backup e segurança
- Treinamento da equipe

**Recomendamos consultar um advogado especializado em LGPD.**

---

## 🎯 Funcionalidades

### Quais funcionalidades estão disponíveis agora?
Veja a lista completa no [ROADMAP.md](ROADMAP.md). Principais:
- ✅ Gestão de pacientes
- ✅ Avaliações antropométricas
- ✅ Planos alimentares
- ✅ Agendamento de consultas
- ✅ Base de alimentos (TACO)
- ✅ Calculadora nutricional
- ✅ Dashboard e relatórios
- ✅ Sistema de receitas
- ✅ Lista de compras

### O sistema gera PDF?
Parcialmente. A geração de PDF depende da biblioteca `reportlab`. Se instalada, alguns relatórios podem ser exportados. Estamos trabalhando em relatórios PDF mais robustos para versões futuras.

### Posso personalizar/customizar o sistema?
**Sim!** O código é aberto e pode ser modificado:
1. Fork o repositório
2. Faça suas alterações
3. Use sua versão customizada

Contribuições são bem-vindas via Pull Requests!

### Posso usar offline?
**Sim**, se executar localmente. Não precisa de internet para funcionar, apenas para:
- Deploy inicial
- Atualizações
- Integrações externas (quando implementadas)

### Quantos pacientes posso cadastrar?
**Ilimitado**. O limite é apenas o espaço em disco e performance:
- SQLite: Dezenas de milhares de registros
- PostgreSQL: Centenas de milhares+

---

## 👥 Multiusuário

### Posso ter vários nutricionistas no mesmo sistema?
**Sim!** O sistema é multiusuário:
- Cada nutricionista cria sua conta
- Dados completamente isolados
- Nenhum compartilhamento entre usuários
- Cada um vê apenas seus pacientes

### Como criar novas contas?
Na tela de login:
1. Clique em "Criar Conta"
2. Preencha os dados (CRN, nome, email, senha)
3. Faça login com a nova conta

### Posso ter diferentes tipos de usuário (admin, nutricionista, estagiário)?
Atualmente, todos os usuários têm os mesmos privilégios. Níveis de acesso diferentes estão no roadmap para versões futuras.

---

## 🔄 Atualizações e Suporte

### Como atualizo o sistema?
**Local**:
```bash
cd NutriStock360-Pro
git pull origin main
pip install -r requirements.txt --upgrade
```

**Railway**: 
- Push para o repositório GitHub
- Railway faz deploy automático

### Como reporto bugs ou problemas?
Abra uma [issue no GitHub](https://github.com/RodrigoSC89/NutriStock360-Pro/issues) com:
- Descrição do problema
- Passos para reproduzir
- Screenshots (se aplicável)
- Mensagens de erro

### Como sugiro novas funcionalidades?
1. Abra uma [issue](https://github.com/RodrigoSC89/NutriStock360-Pro/issues)
2. Use o label "enhancement"
3. Descreva a funcionalidade desejada
4. Explique o caso de uso

### Posso contribuir com código?
**Sim!** Contribuições são bem-vindas:
1. Fork o repositório
2. Crie uma branch para sua feature
3. Desenvolva e teste
4. Envie um Pull Request
5. Aguarde review

---

## 🌐 Deploy e Hospedagem

### Qual é o melhor lugar para hospedar?
Depende das suas necessidades:

**Railway** (recomendado):
- ✅ Fácil configuração
- ✅ PostgreSQL incluído
- ✅ Deploy automático
- ✅ SSL gratuito
- 💰 ~$5-10/mês

**Streamlit Cloud**:
- ✅ Gratuito
- ✅ Integração direta com GitHub
- ⚠️ Limitações de recursos
- ⚠️ Pode ser lento

**Local/VPS próprio**:
- ✅ Controle total
- ✅ Sem custos de plataforma
- ⚠️ Requer manutenção
- ⚠️ Configuração manual

### Como configuro domínio próprio?
No Railway:
1. Acesse configurações do serviço
2. Vá para "Settings" → "Domains"
3. Adicione seu domínio customizado
4. Configure DNS conforme instruções

### O sistema suporta HTTPS?
**Sim**, automaticamente:
- Railway: SSL/HTTPS automático
- Streamlit Cloud: HTTPS incluído
- Local: Requer configuração manual (nginx/certbot)

---

## 📊 Dados e Integrações

### Posso importar dados de outro sistema?
Atualmente não há importação automática, mas você pode:
- Inserir dados manualmente via interface
- Criar script Python para importação direta no banco
- Consultar suporte para casos específicos

### O sistema integra com outras ferramentas?
Atualmente não há integrações diretas. No roadmap:
- 📝 WhatsApp Business
- 📝 Google Calendar
- 📝 APIs de nutrição (USDA, Open Food Facts)
- 📝 Wearables (Fitbit, Apple Health)

### Posso exportar dados?
Sim, você pode:
- Fazer backup do banco de dados completo
- Exportar relatórios (quando PDF disponível)
- Acessar o banco SQLite diretamente para queries

---

## ❓ Outras Dúvidas

### O sistema tem aplicativo mobile?
Não nativamente, mas:
- A interface web é responsiva (funciona em celular)
- PWA (app instalável) está no roadmap
- Acesse via navegador mobile normalmente

### Posso usar em consultório com múltiplos computadores?
**Sim**, se hospedar no Railway ou servidor próprio:
- Acesse a URL de qualquer dispositivo
- Login funciona em qualquer lugar
- Dados sincronizados automaticamente

**Não** se usar localmente (cada PC tem seu próprio banco)

### Tem vídeo tutorial?
Atualmente não temos vídeos, mas temos:
- [Quick Start Guide](QUICKSTART.md)
- [Documentação completa](ACESSO.md)
- [Guia de deploy](guia)
- Interface intuitiva com dados de demonstração

### Posso revender ou oferecer como serviço?
Depende da licença do projeto. Verifique o arquivo LICENSE no repositório. Geralmente:
- ✅ Usar para seu consultório
- ✅ Modificar para suas necessidades
- ⚠️ Revender requer autorização específica

---

## 📞 Ainda tem dúvidas?

**Documentação**:
- [Quick Start](QUICKSTART.md)
- [Acesso e Cronograma](ACESSO.md)
- [Roadmap](ROADMAP.md)
- [README](README.md)

**Suporte**:
- Issues: https://github.com/RodrigoSC89/NutriStock360-Pro/issues
- Repositório: https://github.com/RodrigoSC89/NutriStock360-Pro

---

**Não encontrou sua pergunta?** Abra uma issue no GitHub! 💬
