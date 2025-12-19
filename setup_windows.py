"""
Script de instalação para Windows 11
Resolve problemas de compilação com NumPy e Pandas no Windows
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Executa comando e mostra progresso"""
    print(f"\n{'='*60}")
    print(f"[INSTALANDO] {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True)
        print(f"[OK] {description} instalado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] Falha ao instalar {description}")
        print(f"Detalhes: {e}")
        return False

def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  Instalador Django - Análise de Dados de Vacinação        ║
    ║  Windows 11 - Python 3.13                                  ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Atualizar pip
    print("\n[PASSO 1] Atualizando pip...")
    run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "pip upgrade"
    )
    
    # Step 2: Instalar NumPy primeiro (versão otimizada para Windows)
    print("\n[PASSO 2] Instalando NumPy (pode levar alguns minutos)...")
    run_command(
        f"{sys.executable} -m pip install numpy==2.0.0 --no-cache-dir",
        "NumPy 2.0.0"
    )
    
    # Step 3: Instalar Pandas
    print("\n[PASSO 3] Instalando Pandas...")
    run_command(
        f"{sys.executable} -m pip install pandas==2.2.0 --no-cache-dir",
        "Pandas 2.2.0"
    )
    
    # Step 4: Instalar Django
    print("\n[PASSO 4] Instalando Django...")
    run_command(
        f"{sys.executable} -m pip install Django==5.0.1",
        "Django 5.0.1"
    )
    
    # Step 5: Instalar dependências Django
    print("\n[PASSO 5] Instalando dependências Django...")
    run_command(
        f"{sys.executable} -m pip install djangorestframework==3.14.0 django-cors-headers==4.3.1",
        "Django REST Framework e CORS"
    )
    
    # Step 6: Instalar Plotly e outras dependências
    print("\n[PASSO 6] Instalando Plotly e ferramentas de visualização...")
    run_command(
        f"{sys.executable} -m pip install plotly==5.18.0 openpyxl==3.1.2",
        "Plotly e Excel"
    )
    
    # Step 7: Instalar dependências adicionais
    print("\n[PASSO 7] Instalando dependências adicionais...")
    run_command(
        f"{sys.executable} -m pip install requests==2.31.0 gunicorn==21.2.0 psycopg2-binary==2.9.9 python-decouple==3.8",
        "Requests, Gunicorn, PostgreSQL, Decouple"
    )
    
    # Step 8: Fazer migrações
    print("\n[PASSO 8] Configurando banco de dados...")
    run_command(
        f"{sys.executable} manage.py migrate",
        "Migrações Django"
    )
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  INSTALAÇÃO CONCLUÍDA COM SUCESSO! ✓                       ║
    ╚════════════════════════════════════════════════════════════╝
    
    Próximos passos:
    
    1. Coletar dados:
       python scripts/collect_data.py
    
    2. Criar superusuário (opcional):
       python manage.py createsuperuser
    
    3. Iniciar servidor:
       python manage.py runserver
    
    Acesse: http://localhost:8000
    
    """)

if __name__ == "__main__":
    main()
