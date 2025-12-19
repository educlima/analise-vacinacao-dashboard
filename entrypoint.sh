#!/bin/bash

set -e

echo "Executando migrações do Django..."
python manage.py migrate --noinput

echo "Carregando dados de exemplo..."
python /app/scripts/collect_data.py || echo "Aviso: Falha ao coletar dados, usando dados de exemplo"

echo "Iniciando servidor Django..."
exec "$@"
