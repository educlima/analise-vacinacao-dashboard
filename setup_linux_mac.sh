#!/bin/bash

# Script de configuração para Linux e macOS
# Resolve problemas de compilação

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Instalador Django - Análise de Dados de Vacinação        ║"
echo "║  Linux / macOS                                             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar Python
echo "[1] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERRO] Python 3 não encontrado${NC}"
    echo "Instale com: brew install python3 (macOS) ou apt install python3 (Linux)"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}[OK] Python $PYTHON_VERSION detectado${NC}"
echo ""

# Criar ambiente virtual
echo "[2] Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate
echo -e "${GREEN}[OK] Ambiente virtual ativado${NC}"
echo ""

# Atualizar pip
echo "[3] Atualizando pip..."
python3 -m pip install --upgrade pip --quiet
echo -e "${GREEN}[OK] pip atualizado${NC}"
echo ""

# Instalar dependências principais
echo "[4] Instalando NumPy..."
python3 -m pip install numpy==2.0.0 --no-cache-dir --quiet
echo -e "${GREEN}[OK] NumPy instalado${NC}"

echo "[5] Instalando Pandas..."
python3 -m pip install pandas==2.2.0 --no-cache-dir --quiet
echo -e "${GREEN}[OK] Pandas instalado${NC}"

echo "[6] Instalando Django e extensões..."
python3 -m pip install Django==5.0.1 djangorestframework==3.14.0 django-cors-headers==4.3.1 --quiet
echo -e "${GREEN}[OK] Django instalado${NC}"

echo "[7] Instalando Plotly e ferramentas..."
python3 -m pip install plotly==5.18.0 openpyxl==3.1.2 requests==2.31.0 --quiet
echo -e "${GREEN}[OK] Ferramentas instaladas${NC}"

echo "[8] Instalando dependências finais..."
python3 -m pip install gunicorn==21.2.0 psycopg2-binary==2.9.9 python-decouple==3.8 --quiet
echo -e "${GREEN}[OK] Todas as dependências instaladas${NC}"
echo ""

# Fazer migrações
echo "[9] Configurando banco de dados..."
python3 manage.py migrate --quiet
echo -e "${GREEN}[OK] Banco de dados configurado${NC}"
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo -e "║ ${GREEN}INSTALAÇÃO CONCLUÍDA COM SUCESSO!${NC}                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Próximos passos:"
echo ""
echo "1. Coletar dados:"
echo "   python manage.py shell < scripts/collect_data.py"
echo ""
echo "2. Iniciar servidor:"
echo "   python manage.py runserver"
echo ""
echo "Acesse: http://localhost:8000"
echo ""
