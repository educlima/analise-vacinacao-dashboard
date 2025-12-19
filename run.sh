#!/bin/bash

echo "🚀 Iniciando Django Vaccine Analysis..."

# Criar migrations
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Coletar dados
echo "📊 Coletando dados de vacinação..."
python scripts/collect_data.py

# Criar superuser (opcional)
# python manage.py createsuperuser

# Iniciar servidor
echo "🎯 Iniciando servidor..."
python manage.py runserver 0.0.0.0:8000
