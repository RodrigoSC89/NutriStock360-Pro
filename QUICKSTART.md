# 🚀 Quick Start - NutriStock360-Pro

Guia rápido para começar a usar o sistema em 5 minutos!

---

## ⚡ Início Rápido (Local)

### 1. Clone o Repositório
```bash
git clone https://github.com/RodrigoSC89/NutriStock360-Pro.git
cd NutriStock360-Pro
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 3. Execute o Sistema
```bash
streamlit run main.py
```

### 4. Acesse no Navegador
```
http://localhost:8501
```

### 5. Faça Login
**Credenciais de demonstração:**
- **Usuário**: `admin`
- **Senha**: `admin123`

---

## 🎯 O que Fazer Primeiro?

### 1️⃣ Explore o Dashboard
- Veja as métricas gerais do sistema
- Analise os gráficos de evolução
- Conheça os indicadores disponíveis

### 2️⃣ Navegue pelos Pacientes de Demonstração
- Acesse o menu "👥 Pacientes"
- Veja 3 pacientes exemplo já cadastrados
- Explore os detalhes de cada um
- Analise o histórico de avaliações

### 3️⃣ Teste a Calculadora Nutricional
- Acesse "🧮 Calculadora"
- Calcule IMC, TMB, GET
- Experimente diferentes valores
- Veja as necessidades nutricionais

### 4️⃣ Explore a Base de Alimentos
- Acesse "🥑 Alimentos"
- Navegue pelos alimentos brasileiros (TACO)
- Veja informações nutricionais completas
- Adicione novos alimentos se desejar

### 5️⃣ Crie Seu Primeiro Plano Alimentar
- Acesse "🥗 Planos Alimentares"
- Selecione um paciente
- Crie um plano personalizado
- Adicione refeições e alimentos

---

## 📚 Próximos Passos

### Personalize o Sistema

1. **Crie Sua Conta**
   - Clique em "Criar Conta" na tela de login
   - Preencha seus dados (CRN, nome, email)
   - Faça login com sua nova conta

2. **Cadastre Seus Pacientes**
   - Menu "👥 Pacientes" → "➕ Novo Paciente"
   - Preencha os dados completos
   - Adicione histórico médico e alergias

3. **Registre Avaliações**
   - Selecione um paciente
   - Menu "📊 Avaliações" → "➕ Nova Avaliação"
   - Registre medidas e acompanhe evolução

4. **Agende Consultas**
   - Menu "📅 Consultas"
   - Crie agendamentos
   - Controle status (pendente, confirmado, concluído)

5. **Adicione Receitas**
   - Menu "🍽️ Receitas"
   - Cadastre suas receitas favoritas
   - Categorize por tipo de refeição

---

## 🌐 Deploy para Produção

Quando estiver pronto para usar em produção:

1. **Leia o Guia de Deploy**
   - Arquivo: [guia](guia)
   - Tempo: 30-45 minutos
   - Plataforma: Railway

2. **Siga os Passos**
   - Criar conta no GitHub (se não tiver)
   - Criar conta no Railway
   - Conectar repositório
   - Deploy automático

3. **Configure o Ambiente**
   - Adicione PostgreSQL (opcional)
   - Configure variáveis de ambiente
   - Obtenha URL pública

---

## 💡 Dicas Úteis

### Navegação
- Use o **menu lateral** para acessar todos os módulos
- Cada módulo tem suas próprias sub-funções
- Dados são salvos automaticamente

### Dados de Demonstração
- O sistema vem com pacientes, receitas e alimentos exemplo
- Use para explorar funcionalidades
- Delete quando quiser usar dados reais

### Resetar Sistema
Para começar do zero com dados limpos:
```bash
rm nutristock360.db
streamlit run main.py
```

### Performance
- O sistema é leve e rápido localmente
- Para muitos pacientes, considere PostgreSQL
- Backup regular do arquivo `.db`

---

## ❓ Precisa de Ajuda?

### Documentação Completa
- 📋 [ACESSO.md](ACESSO.md) - Informações de acesso e cronograma
- 🗺️ [ROADMAP.md](ROADMAP.md) - Funcionalidades e planejamento
- 📖 [README.md](README.md) - Visão geral do sistema
- 📘 [guia](guia) - Deploy no Railway

### Suporte
- **Issues**: https://github.com/RodrigoSC89/NutriStock360-Pro/issues
- **Repositório**: https://github.com/RodrigoSC89/NutriStock360-Pro

---

## ✅ Checklist de Primeiros Passos

- [ ] Clone o repositório
- [ ] Instale dependências
- [ ] Execute o sistema
- [ ] Faça login com credenciais demo
- [ ] Explore o dashboard
- [ ] Navegue pelos pacientes exemplo
- [ ] Teste a calculadora
- [ ] Veja a base de alimentos
- [ ] Crie uma conta própria
- [ ] Cadastre um paciente real
- [ ] Registre uma avaliação
- [ ] Crie um plano alimentar
- [ ] Agende uma consulta
- [ ] Adicione uma receita

---

**Tempo estimado para completar**: 15-20 minutos

**Pronto para começar?** Execute `streamlit run main.py` e acesse http://localhost:8501! 🚀
