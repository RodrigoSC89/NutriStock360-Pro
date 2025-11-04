# NutriStock360-Pro - Sistema Completo para Nutricionistas

Sistema profissional para gestão de consultório nutricional com autenticação multiusuário, gestão de pacientes, planos alimentares e calculadora nutricional.

## 🚀 Acesso Rápido

- 📋 **[Informações de Acesso e Cronograma](ACESSO.md)** - Como acessar o sistema e timeline
- 🗺️ **[Roadmap e Planejamento](ROADMAP.md)** - Funcionalidades e próximas etapas
- 📖 **[Guia de Deploy](guia)** - Instruções completas para deploy no Railway

## Funcionalidades

- **Sistema Multiusuário** - Cada nutricionista tem seus dados isolados
- **Gestão de Pacientes** - Cadastro completo com histórico médico
- **Base de Alimentos** - Alimentos brasileiros (tabela TACO)
- **Planos Alimentares** - Criação de planos personalizados
- **Agenda de Consultas** - Sistema completo de agendamento
- **Dashboard** - Métricas e indicadores em tempo real
- **Calculadora Nutricional** - IMC, TMB, necessidades nutricionais

## Tecnologias

- **Frontend**: Streamlit (Python)
- **Backend**: Python com SQLite
- **Banco de Dados**: SQLite (local) ou PostgreSQL (Railway)
- **Deploy**: Railway / Streamlit Cloud
- **Visualização**: Plotly, Pandas

## Status do Projeto

✅ **Sistema Completo e Funcional**

Todas as funcionalidades principais estão implementadas e disponíveis para uso:
- Sistema de autenticação multiusuário
- Gestão completa de pacientes
- Avaliações antropométricas
- Planos alimentares personalizados
- Agendamento de consultas
- Dashboard com métricas
- Calculadora nutricional
- Base de alimentos (TACO)
- Sistema de receitas

Para mais detalhes sobre status e cronograma, veja [ACESSO.md](ACESSO.md).

## URLs do Sistema

**Ambiente Local** (para testes):
- **Sistema**: http://localhost:8501 (após executar `streamlit run main.py`)

**Após Deploy no Railway**:
- **Sistema**: https://sua-url.railway.app/
- **Health Check**: Disponível via interface Streamlit

Consulte o [guia de deploy](guia) para instruções completas de como fazer o deploy.

## Como Usar

### Opção 1: Executar Localmente (Recomendado para Testes)

```bash
# Clone o repositório
git clone https://github.com/RodrigoSC89/NutriStock360-Pro.git
cd NutriStock360-Pro

# Instale as dependências
pip install -r requirements.txt

# Execute o sistema
streamlit run main.py
```

Acesse em: http://localhost:8501

**Credenciais de demonstração**:
- Usuário: `admin`
- Senha: `admin123`

### Opção 2: Deploy no Railway (Para Produção)

Siga o guia completo no arquivo [guia](guia) que contém instruções passo a passo.

**Tempo estimado**: 30-45 minutos  
**Custo**: ~$5-10/mês após créditos gratuitos

### Primeiros Passos

1. Acesse o sistema pela URL (local ou Railway)
2. Faça login com as credenciais de demonstração ou crie uma conta
3. Explore o menu lateral com todas as funcionalidades
4. O sistema já vem com dados de demonstração (pacientes, receitas, alimentos)

Para informações detalhadas sobre acesso e funcionalidades, consulte [ACESSO.md](ACESSO.md).

## Estrutura do Sistema

### Módulos Disponíveis

- 🏠 **Dashboard**: Métricas e indicadores em tempo real
- 👥 **Pacientes**: Cadastro completo com histórico médico e progresso
- 📊 **Avaliações**: Avaliações antropométricas e evolução
- 📅 **Consultas**: Sistema completo de agendamento
- 🥗 **Planos Alimentares**: Criação de planos personalizados
- 🍽️ **Receitas**: Banco de receitas com informações nutricionais
- 🥑 **Alimentos**: Base de dados (tabela TACO) com alimentos brasileiros
- 🧮 **Calculadora**: IMC, TMB, GET, necessidades nutricionais
- 🛒 **Lista de Compras**: Geração automatizada
- 🎯 **Metas**: Acompanhamento de objetivos dos pacientes
- 👤 **Perfil**: Gerenciamento de conta e dados do nutricionista

## Deploy

O sistema pode ser hospedado de duas formas:

1. **Localmente**: Execute em seu próprio computador/servidor
2. **Railway**: Plataforma em nuvem com deploy automático

Consulte o [guia completo de deploy](guia) para instruções passo a passo.

## Segurança e Privacidade

- ✅ Sistema com autenticação obrigatória
- ✅ Senhas criptografadas (SHA-256)
- ✅ Dados isolados por usuário (multiusuário)
- ✅ Sessões seguras
- ✅ Nenhum dado compartilhado entre nutricionistas

## Documentação

- 📋 **[ACESSO.md](ACESSO.md)**: Informações completas sobre como acessar o sistema, ambientes disponíveis, cronograma e módulos
- 🗺️ **[ROADMAP.md](ROADMAP.md)**: Planejamento de desenvolvimento, funcionalidades implementadas e futuras
- 📖 **[guia](guia)**: Instruções detalhadas para deploy no Railway

## Suporte e Contribuições

### Reportar Problemas
Encontrou um bug? Abra uma [issue](https://github.com/RodrigoSC89/NutriStock360-Pro/issues)

### Sugerir Funcionalidades
Tem uma ideia? Abra uma [issue](https://github.com/RodrigoSC89/NutriStock360-Pro/issues) com a tag "enhancement"

### Contribuir com Código
1. Fork o repositório
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Envie um pull request

## Desenvolvido para

Nutricionistas brasileiros que precisam de um sistema completo e profissional para gestão do consultório.

---

**NutriStock360** - Transformando a prática nutricional através da tecnologia.
