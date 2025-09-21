# Guia Completo: Deploy NutriStock360 no Railway

## Pré-requisitos

1. **Conta no GitHub** (gratuita)
2. **Conta no Railway** (gratuita)
3. **Arquivos do sistema** organizados

## Passo 1: Preparar os Arquivos

### 1.1 Criar uma pasta no seu computador
```
NutriStock360/
├── main.py (versão Railway)
├── requirements.txt (versão Railway)
├── railway.json
├── index.html (calculadora nutricional)
└── README.md
```

### 1.2 Baixar os arquivos
- Copie o conteúdo de cada arquivo dos artefatos acima
- Cole em arquivos novos com os nomes corretos
- Salve todos na mesma pasta

### 1.3 Verificar estrutura
Sua pasta deve ter exatamente estes arquivos:
- `main.py` (arquivo principal da API)
- `requirements.txt` (dependências Python)
- `railway.json` (configurações Railway)
- `index.html` (opcional - calculadora)

## Passo 2: Criar Repositório no GitHub

### 2.1 Acessar GitHub
1. Vá para https://github.com
2. Faça login ou crie conta gratuita
3. Clique no botão verde "New" (ou "Novo")

### 2.2 Configurar repositório
1. **Repository name**: `nutristock360`
2. **Description**: `Sistema completo para nutricionistas`
3. **Public** (deixe marcado)
4. **Add README**: deixe desmarcado
5. Clique "Create repository"

### 2.3 Upload dos arquivos
1. Na página do repositório criado
2. Clique "uploading an existing file"
3. Arraste todos os arquivos da pasta para o navegador
4. Escreva: "Adicionar sistema NutriStock360"
5. Clique "Commit changes"

## Passo 3: Deploy no Railway

### 3.1 Criar conta Railway
1. Vá para https://railway.app
2. Clique "Login"
3. Escolha "Login with GitHub"
4. Autorize a conexão

### 3.2 Criar novo projeto
1. No dashboard Railway, clique "New Project"
2. Selecione "Deploy from GitHub repo"
3. Encontre e selecione `nutristock360`
4. Clique no repositório

### 3.3 Configuração automática
Railway vai automaticamente:
- Detectar que é um projeto Python/FastAPI
- Instalar dependências do requirements.txt
- Configurar o build

### 3.4 Adicionar PostgreSQL
1. No projeto Railway, clique "New"
2. Selecione "Database"
3. Escolha "Add PostgreSQL"
4. Aguarde a configuração (1-2 minutos)

### 3.5 Configurar variáveis de ambiente
1. Clique no serviço principal (nutristock360)
2. Vá para aba "Variables"
3. Adicione:
   ```
   SECRET_KEY = nutristock360_production_secret_change_this
   ENVIRONMENT = production
   ```
4. Clique "Add" para cada variável

### 3.6 Deploy final
1. Railway vai fazer deploy automaticamente
2. Aguarde 5-10 minutos
3. Você verá logs na aba "Deployments"

## Passo 4: Verificar Sistema

### 4.1 Obter URL
1. No Railway, clique no seu serviço
2. Vá para aba "Settings"
3. Procure "Domains"
4. Clique "Generate Domain"
5. Copie a URL gerada (ex: https://nutristock360-production.up.railway.app)

### 4.2 Testar funcionamento
1. Acesse a URL gerada
2. Adicione `/docs` no final (ex: https://sua-url.railway.app/docs)
3. Você deve ver a documentação da API
4. Teste criar uma conta em `/register`

## Passo 5: Configurar Frontend

### 5.1 Atualizar URL da API
No arquivo `index.html`, encontre:
```javascript
const API_BASE = 'http://localhost:8000';
```

Altere para:
```javascript
const API_BASE = 'https://sua-url.railway.app';
```

### 5.2 Fazer upload do frontend
Você pode:
- **Opção A**: Hospedar no GitHub Pages (só frontend)
- **Opção B**: Adicionar à pasta static do Railway

## Solução de Problemas

### Build falhou
1. Verifique se todos os arquivos estão na raiz do repositório
2. Confira se `requirements.txt` está correto
3. Veja os logs na aba "Deployments"

### Erro de conexão
1. Verifique se PostgreSQL foi adicionado
2. Aguarde alguns minutos após o deploy
3. Veja logs para erros específicos

### Variáveis de ambiente
Railway automaticamente conecta PostgreSQL através da variável `DATABASE_URL`

## URLs Importantes

Após deploy bem-sucedido:
- **API Docs**: https://sua-url.railway.app/docs
- **Health Check**: https://sua-url.railway.app/health
- **Sistema**: https://sua-url.railway.app/

## Próximos Passos

1. **Testar sistema** completamente
2. **Configurar domínio customizado** (opcional)
3. **Monitorar logs** regularmente
4. **Fazer backups** dos dados importantes

## Custos

- **Primeiros 5$**: Gratuitos
- **Após trial**: ~$5-10/mês para uso básico
- **PostgreSQL**: Incluído no plano

## Suporte

Se der erro:
1. Verifique logs no Railway
2. Consulte documentação: https://docs.railway.app
3. Procure ajuda na comunidade Railway

---

**Tempo estimado total**: 30-45 minutos
**Dificuldade**: Iniciante
**Resultado**: Sistema completo funcionando online