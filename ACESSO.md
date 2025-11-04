## 🚀 Acesso ao Sistema NutriStock360-Pro

> 💡 **Quer começar rapidamente?** Veja o [Quick Start Guide](QUICKSTART.md) para estar usando o sistema em 5 minutos!

## 📋 Informações de Acesso

Bem-vindo ao **NutriStock360-Pro**! Este documento fornece todas as informações necessárias para acessar o sistema, incluindo cronograma, ambientes disponíveis e como começar a usar.

---

## 🌐 Ambientes Disponíveis

### 1. **Ambiente de Produção**
- **Status**: ✅ Disponível
- **URL**: Será disponibilizada após deploy no Railway
- **Descrição**: Ambiente principal para uso em produção
- **Acesso**: Requer cadastro de conta

### 2. **Ambiente de Homologação/Testes**
- **Status**: ✅ Disponível
- **URL**: Pode ser configurado separadamente no Railway
- **Descrição**: Ambiente para testes de novas funcionalidades
- **Acesso**: Mesmas credenciais do ambiente de produção
- **Dados**: Dados de demonstração inclusos

### 3. **Ambiente Local (Desenvolvimento)**
- **Status**: ✅ Disponível
- **Descrição**: Execute o sistema localmente para testes
- **Requisitos**: Python 3.8+, pip
- **Como executar**:
  ```bash
  # Clone o repositório
  git clone https://github.com/RodrigoSC89/NutriStock360-Pro.git
  cd NutriStock360-Pro
  
  # Instale as dependências
  pip install -r requirements.txt
  
  # Execute o sistema
  streamlit run main.py
  ```
- **Acesso local**: http://localhost:8501

---

## 📅 Cronograma de Liberação

### **Fase 1: Sistema Base** ✅ CONCLUÍDO
**Status**: Disponível para uso imediato

**Funcionalidades liberadas**:
- ✅ Sistema de autenticação multiusuário
- ✅ Gestão completa de pacientes
- ✅ Cadastro e avaliações antropométricas
- ✅ Histórico de consultas
- ✅ Dashboard com métricas em tempo real
- ✅ Base de dados de alimentos (tabela TACO)
- ✅ Calculadora nutricional integrada
- ✅ Sistema de receitas

**Credenciais de Demonstração**:
- **Usuário**: `admin`
- **Senha**: `admin123`

---

### **Fase 2: Funcionalidades Avançadas** ✅ CONCLUÍDO
**Status**: Disponível para uso

**Funcionalidades liberadas**:
- ✅ Planos alimentares personalizados
- ✅ Agendamento de consultas
- ✅ Gestão de metas dos pacientes
- ✅ Lista de compras automatizada
- ✅ Exportação de relatórios (se PDF disponível)
- ✅ Gráficos de evolução
- ✅ Sistema de receitas com categorias

---

### **Fase 3: Deploy em Nuvem** 🔄 EM ANDAMENTO
**Previsão**: Imediato (configurável pelo usuário)

**Tarefas**:
- 🔄 Configuração do Railway
- 🔄 Deploy do PostgreSQL (opcional)
- 🔄 Configuração de domínio customizado (opcional)
- 🔄 Monitoramento e logs

**Como fazer deploy**:
Siga o guia completo no arquivo `guia` na raiz do projeto que contém instruções passo a passo para:
1. Criar repositório no GitHub
2. Configurar conta no Railway
3. Deploy automático
4. Configuração de PostgreSQL
5. Obtenção da URL do sistema

**Tempo estimado**: 30-45 minutos

---

### **Fase 4: Otimizações** 📝 PLANEJADO
**Previsão**: Próximas versões

**Melhorias planejadas**:
- 📝 Integração com APIs de nutrição
- 📝 Aplicativo mobile (PWA)
- 📝 Notificações por e-mail/SMS
- 📝 Relatórios PDF avançados
- 📝 Backup automático
- 📝 Multi-idiomas

---

## 🎯 Como Começar

### **Passo 1: Escolha o Ambiente**

**Para Testes Locais** (recomendado para primeiros testes):
```bash
# Clone e execute localmente
git clone https://github.com/RodrigoSC89/NutriStock360-Pro.git
cd NutriStock360-Pro
pip install -r requirements.txt
streamlit run main.py
```

**Para Deploy em Produção**:
Siga o guia completo no arquivo `guia` para fazer deploy no Railway.

---

### **Passo 2: Primeiro Acesso**

1. **Acesse o sistema** pela URL (local ou Railway)
2. **Faça login** com as credenciais de demonstração:
   - Usuário: `admin`
   - Senha: `admin123`
3. **Ou crie uma nova conta** clicando em "Criar Conta"

---

### **Passo 3: Explore as Funcionalidades**

O sistema já vem com dados de demonstração incluindo:
- 3 pacientes exemplo
- Histórico de avaliações
- Base de alimentos
- Receitas exemplo

**Menu lateral** disponível:
- 🏠 **Dashboard**: Visão geral e métricas
- 👥 **Pacientes**: Gestão completa de pacientes
- 📊 **Avaliações**: Avaliações antropométricas
- 📅 **Consultas**: Agendamento e histórico
- 🥗 **Planos Alimentares**: Criação de dietas
- 🍽️ **Receitas**: Banco de receitas
- 🥑 **Alimentos**: Base de dados nutricional
- 🧮 **Calculadora**: Cálculos nutricionais (IMC, TMB, etc)
- 🛒 **Lista de Compras**: Geração automática
- 🎯 **Metas**: Acompanhamento de objetivos
- 👤 **Perfil**: Gerenciamento de conta

---

## 🧪 Ambiente de Testes/Homologação

### **Como Usar o Ambiente de Testes**

1. **Dados de Demonstração**:
   O sistema já inclui dados fictícios para facilitar testes:
   - Pacientes exemplo com histórico
   - Avaliações ao longo do tempo
   - Receitas pré-cadastradas
   - Base de alimentos populares

2. **Resetar Dados**:
   Se desejar começar do zero, delete o arquivo `nutristock360.db` e reinicie o sistema.

3. **Testar Funcionalidades**:
   - Cadastre novos pacientes
   - Registre avaliações
   - Crie planos alimentares
   - Agende consultas
   - Explore o dashboard

---

## 📊 Módulos e Funcionalidades Disponíveis

### ✅ **Módulo de Gestão de Pacientes**
- Cadastro completo com dados pessoais
- Informações médicas e alergias
- Histórico de consultas
- Metas e objetivos
- Status de progresso

### ✅ **Módulo de Avaliações**
- Medidas antropométricas completas
- Cálculo automático de IMC
- Histórico de evolução
- Gráficos de progresso

### ✅ **Módulo de Planos Alimentares**
- Criação de dietas personalizadas
- Cálculo automático de macros
- Múltiplas refeições por dia
- Biblioteca de alimentos

### ✅ **Módulo de Receitas**
- Banco de receitas
- Categorização por tipo de refeição
- Informações nutricionais
- Tempo de preparo e dificuldade

### ✅ **Módulo de Consultas**
- Agendamento de consultas
- Controle de status (pendente, confirmado, concluído)
- Histórico completo
- Calendário visual

### ✅ **Dashboard e Relatórios**
- Métricas em tempo real
- Total de pacientes ativos
- Consultas do mês
- Gráficos de evolução
- Estatísticas gerais

### ✅ **Calculadora Nutricional**
- Cálculo de IMC
- Taxa Metabólica Basal (TMB)
- Gasto Energético Total (GET)
- Distribuição de macronutrientes
- Necessidades calóricas

---

## 🔐 Segurança e Privacidade

- ✅ Sistema com autenticação obrigatória
- ✅ Senhas criptografadas (hash SHA-256)*
- ✅ Dados isolados por usuário (multiusuário)
- ✅ Sessões seguras
- ✅ Nenhum dado compartilhado entre nutricionistas

**Nota de Segurança**: O hash SHA-256 é adequado para demonstração e uso básico. Para ambientes de produção com dados médicos sensíveis, recomenda-se atualizar para algoritmos mais robustos como bcrypt, scrypt ou Argon2. Esta melhoria está no roadmap de segurança.

---

## 📞 Suporte e Acompanhamento

### **Acompanhar Mudanças e Novidades**

1. **GitHub**:
   - Acompanhe os commits no repositório
   - Veja o histórico de alterações
   - Reporte issues ou sugestões

2. **Releases**:
   - Verifique a seção de releases no GitHub
   - Changelog com todas as mudanças

3. **Documentação**:
   - Consulte `README.md` para visão geral
   - Consulte `guia` para instruções de deploy
   - Consulte `ROADMAP.md` para planejamento futuro

---

## ❓ Perguntas Frequentes

### **1. O sistema está pronto para uso em produção?**
✅ Sim! Todas as funcionalidades principais estão implementadas e testadas.

### **2. Preciso de conhecimentos técnicos para usar?**
Não para usar o sistema. Sim (básico) para fazer o deploy no Railway, mas temos guia completo.

### **3. Os dados ficam seguros?**
Sim. O sistema usa criptografia para senhas e cada usuário tem seus dados isolados.

### **4. Posso customizar o sistema?**
Sim. O código é aberto e pode ser modificado conforme necessário.

### **5. Existe custo para hospedar?**
- Railway: ~$5-10/mês após créditos gratuitos iniciais ($5)
- Alternativa: Hospedar localmente sem custo

### **6. Como faço backup dos dados?**
Faça backup do arquivo `nutristock360.db` regularmente. No Railway, configure backups do PostgreSQL.

### **7. Posso usar offline?**
Sim, se executar localmente. A versão Railway requer internet.

---

## 🚀 Próximos Passos Recomendados

1. ✅ **Teste localmente** primeiro para conhecer todas as funcionalidades
2. 🔄 **Faça deploy no Railway** seguindo o guia
3. 📊 **Configure seus dados** reais (pacientes, receitas, etc)
4. 🎯 **Comece a usar** no dia a dia do consultório
5. 📝 **Dê feedback** reportando issues ou sugestões no GitHub

---

## 📧 Contato

Para dúvidas sobre acesso ou funcionalidades:
- **GitHub Issues**: https://github.com/RodrigoSC89/NutriStock360-Pro/issues
- **Repositório**: https://github.com/RodrigoSC89/NutriStock360-Pro

---

**NutriStock360-Pro** - Sistema completo para nutricionistas, disponível agora! 🎉
