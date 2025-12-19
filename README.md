# 💉 Dashboard de Análise de Vacinação

Um sistema completo de análise de dados de vacinação e óbitos usando **Python, Django e análise de dados com Plotly**, comparando Brasil, Portugal, Itália e EUA.

## 📋 Características

✅ **Dashboard Interativo** com gráficos em tempo real
✅ **Múltiplos Tipos de Gráficos**: Barras, Linhas, Pizza e Dispersão
✅ **Comparativo entre 4 Países**: Brasil, Portugal, Itália e EUA
✅ **Filtros por País e Estado/Região**
✅ **Análise de Dados com Python**: Pandas, NumPy
✅ **API REST** para integração com outros sistemas
✅ **Dados em Tempo Real** de APIs públicas (Our World in Data)
✅ **Exportação de Dados** para análise posterior
✅ **Docker** para ambiente isolado sem conflitos de dependências

---

## 🚨 IMPORTANTE: Docker Desktop Deve Estar Rodando

Antes de executar qualquer comando Docker, **você DEVE iniciar o Docker Desktop**:

1. Procure por **"Docker Desktop"** no Windows Search
2. Clique para abrir
3. **Aguarde aparecer "Docker Desktop is running"** (pode levar 30 segundos a 1 minuto)
4. Verifique no PowerShell:

```powershell
docker --version
```

Se mostrar a versão, Docker está pronto. Se der erro, Docker Desktop não foi iniciado corretamente.

---

## 🐳 Instalação com Docker (Recomendado - Windows 11)

### Pré-requisitos
- Docker Desktop instalado e rodando ✓

### Passo 1: Abra o Terminal no VS Code

- Pressione **Ctrl + '** (aspas simples)
- Certifique-se que está na pasta do projeto:

```powershell
cd C:\Users\seu_usuario\Downloads\data-analysis-dashboard
```

### Passo 2: Construir a Imagem

```powershell
docker-compose build
```

**Primeira vez leva 5-10 minutos.** Aguarde até ver `Successfully tagged`.

### Passo 3: Iniciar os Containers

```powershell
docker-compose up -d
```

### Passo 4: Executar Migrações

```powershell
docker-compose exec web python manage.py migrate
```

### Passo 5: Coletar Dados

```powershell
docker-compose exec web python scripts/collect_data.py
```

Este comando pode levar 1-2 minutos coletando dados das APIs.

### Passo 6: Acessar o Dashboard

Abra no navegador: **http://localhost:8000**

---

## 🔧 Comandos Docker Úteis

### Ver status dos containers
```powershell
docker-compose ps
```

Deve mostrar os containers `vaccine_analysis` e `vaccine_db` como **Up**.

### Ver logs em tempo real
```powershell
docker-compose logs -f web
```

Use **Ctrl + C** para sair.

### Parar os containers
```powershell
docker-compose down
```

### Remover tudo (limpar dados)
```powershell
docker-compose down -v
docker system prune -a
```

**Cuidado:** Isto deleta todos os dados!

### Entrar no terminal do container
```powershell
docker-compose exec web bash
```

### Executar comando no container
```powershell
docker-compose exec web python manage.py createsuperuser
```

---

## 🛠️ Instalação Tradicional (Python Local) - SEM DOCKER

Se preferir não usar Docker, siga isto:

### Pré-requisitos
- Python 3.11+ instalado
- pip funcionando

### 1. Crie um Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Instale as Dependências

```bash
pip install -r requirements-simple.txt
```

### 3. Configure o Banco de Dados

```bash
python manage.py migrate
```

### 4. Colete os Dados

```bash
python scripts/collect_data.py
```

### 5. Inicie o Servidor

```bash
python manage.py runserver
```

Acesse: **http://localhost:8000**

---

## 📁 Estrutura do Projeto

```
vaccine-analysis/
├── Dockerfile               # Imagem Docker
├── docker-compose.yml       # Orquestração Docker (SEM versão)
├── entrypoint.sh           # Script de inicialização
├── config/
│   ├── settings.py         # Configurações Django
│   ├── urls.py             # Rotas principais
│   └── wsgi.py
├── vaccine/
│   ├── models.py           # Modelos de dados
│   ├── views.py            # APIs REST
│   ├── serializers.py      # Serialização
│   └── urls.py
├── templates/
│   └── dashboard.html      # Dashboard interativo
├── scripts/
│   └── collect_data.py     # Coleta de dados
├── requirements.txt        # Dependências (Docker)
├── requirements-simple.txt # Dependências (Python local)
├── manage.py               # Gerenciador Django
└── README.md
```

---

## 🔌 Endpoints da API

### Obter Dados Comparativos entre Países

```
GET /api/countries-data/?countries=brasil,portugal,italia,usa
```

### Obter Dados por Estado/Região

```
GET /api/state-data/?country=brasil
```

### Obter Dados para Gráficos

```
GET /api/chart-data/?country=brasil&type=bar
```

### Comparação entre Países

```
GET /api/comparison/?countries=brasil,portugal,italia,usa
```

---

## 📊 Usando o Dashboard

### Seleção de Tipo de Gráfico

- **Barras** - Comparação direta entre valores
- **Linhas** - Evolução temporal dos dados
- **Pizza** - Proporção entre países
- **Dispersão** - Correlações entre variáveis
- **Área** - Evolução com preenchimento

### Seleção de Métrica

- **Vacinados** - Pessoas completamente vacinadas
- **Óbitos** - Número de mortes registradas
- **Ambos** - Visualização dual

### Filtro por País

- **Todos** - Comparativo entre Brasil, Portugal, Itália, EUA
- **Brasil** - Dados brasileiros por estado
- **Portugal** - Dados portugueses por região
- **Itália** - Dados italianos por região
- **EUA** - Dados americanos por estado

---

## 🔍 Análise de Dados com Python

```python
import pandas as pd
from vaccine.models import VaccineData

# Carregar dados
data = VaccineData.objects.all().values()
df = pd.DataFrame(list(data))

# Filtrar por país
brasil = df[df['country'] == 'brasil']

# Estatísticas
print("Total vacinados:", brasil['vaccinated'].sum())
print("Total óbitos:", brasil['deaths'].sum())
```

---

## 🐛 Troubleshooting

### Erro: "The system cannot find the file specified" no Docker

**Solução:** Docker Desktop NÃO está rodando!

1. Abra Docker Desktop
2. Aguarde aparecer "Docker Desktop is running"
3. Execute novamente: `docker-compose build`

### Erro: "warning... attribute version is obsolete"

**Solução:** O docker-compose.yml foi atualizado. Sem ação necessária.

### Docker: Porta 8000 já em uso

Edite `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Use porta 8001 ao invés
```

### Ver logs de erro
```powershell
docker-compose logs web
```

### Limpar tudo e começar novamente
```powershell
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
```

---

## 📈 Interpretação dos Dados

- **Gráfico Comparativo**: Mostra proporção entre países
- **Evolução Temporal**: Mudanças ao longo do tempo
- **Dados por Estado**: Detalhes em nível regional
- **Análise de Correlação**: Relação entre vacinação e óbitos

---

## 📝 Licença

MIT License

## 📞 Suporte

1. Verifique se Docker Desktop está rodando
2. Veja os logs: `docker-compose logs -f web`
3. Tente limpar e refazer: `docker-compose down -v && docker-compose build && docker-compose up -d`

---

**Versão:** 2.0.0 (Docker Simplificado)
**Status:** Pronto para usar
