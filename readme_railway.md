# NutriStock360 - Sistema para Nutricionistas

Sistema completo para gestão de consultório nutricional com autenticação multiusuário, gestão de pacientes, planos alimentares e calculadora nutricional.

## Funcionalidades

- **Sistema Multiusuário** - Cada nutricionista tem seus dados isolados
- **Gestão de Pacientes** - Cadastro completo com histórico médico
- **Base de Alimentos** - Alimentos brasileiros (tabela TACO)
- **Planos Alimentares** - Criação de planos personalizados
- **Agenda de Consultas** - Sistema completo de agendamento
- **Dashboard** - Métricas e indicadores em tempo real
- **Calculadora Nutricional** - IMC, TMB, necessidades nutricionais

## Tecnologias

- **Backend**: Python FastAPI
- **Banco**: PostgreSQL
- **Frontend**: HTML/CSS/JavaScript
- **Deploy**: Railway

## URLs do Sistema

- **API Docs**: https://sua-url.railway.app/docs
- **Sistema**: https://sua-url.railway.app/
- **Health Check**: https://sua-url.railway.app/health

## Como Usar

1. Acesse o sistema pela URL do Railway
2. Crie sua conta de nutricionista
3. Comece cadastrando pacientes
4. Crie planos alimentares personalizados
5. Use a calculadora nutricional integrada

## Estrutura da API

```
POST /register - Cadastro de usuário
POST /login - Login
GET /me - Dados do usuário

GET/POST /pacientes - Gestão de pacientes
GET/POST /alimentos - Base de alimentos
GET/POST /planos - Planos alimentares
GET/POST /consultas - Agenda de consultas

GET /dashboard - Métricas do sistema
```

## Deploy

Sistema hospedado no Railway com PostgreSQL.

## Desenvolvido para

Nutricionistas brasileiros que precisam de um sistema completo e profissional para gestão do consultório.

---

**NutriStock360** - Transformando a prática nutricional através da tecnologia.