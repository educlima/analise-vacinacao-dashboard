"""
Script para coletar dados de vacinação e óbitos de APIs públicas
Utiliza dados do OWID (Our World in Data) e APIs de saúde públicas
"""
import os
import sys
import django
import pandas as pd
import requests
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from vaccine.models import VaccineData

def fetch_owid_data():
    """Coleta dados do Our World in Data"""
    print("Coletando dados do Our World in Data...")
    
    url = "https://covid.ourworldindata.org/data/owid-covid-data.json"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Erro ao coletar dados OWID: {e}")
        return {}

def process_owid_data(data):
    """Processa dados do OWID e salva no banco"""
    country_mapping = {
        "Brazil": "brasil",
        "Portugal": "portugal",
        "Italy": "italia",
        "United States": "usa"
    }
    
    for country_name, country_code in country_mapping.items():
        print(f"Processando {country_name}...")
        
        if country_name not in data:
            print(f"  {country_name} não encontrado")
            continue
        
        country_data = data[country_name]
        
        if "data" not in country_data:
            continue
        
        for entry in country_data["data"]:
            try:
                date_str = entry.get("date")
                if not date_str:
                    continue
                
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                
                vaccinated = entry.get("people_fully_vaccinated", 0) or 0
                deaths = entry.get("total_deaths", 0) or 0
                population = entry.get("population", 0) or 0
                
                if vaccinated == 0 and deaths == 0:
                    continue
                
                VaccineData.objects.update_or_create(
                    country=country_code,
                    state_or_region="Nacional",
                    date=date,
                    defaults={
                        "vaccinated": int(vaccinated),
                        "deaths": int(deaths),
                        "population": int(population),
                    }
                )
            except Exception as e:
                print(f"  Erro ao processar entrada: {e}")
                continue

def generate_sample_data():
    """Gera dados de exemplo se não houver dados reais"""
    print("Gerando dados de exemplo...")
    
    countries = ["brasil", "portugal", "italia", "usa"]
    states = {
        "brasil": ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Bahia"],
        "portugal": ["Lisboa", "Porto", "Covilhã"],
        "italia": ["Roma", "Milão", "Nápoles"],
        "usa": ["California", "Nova York", "Texas"],
    }
    
    base_date = datetime.now().date() - timedelta(days=90)
    
    for country in countries:
        country_states = states.get(country, ["Nacional"])
        
        for state in country_states:
            for i in range(90):
                date = base_date + timedelta(days=i)
                
                base_vaccinated = {
                    "brasil": 80000000,
                    "portugal": 5000000,
                    "italia": 35000000,
                    "usa": 200000000,
                }[country]
                
                vaccinated = int(base_vaccinated * (0.5 + (i / 180)) + (i * 50000))
                deaths = int(vaccinated * 0.02 + (i * 100))
                
                VaccineData.objects.update_or_create(
                    country=country,
                    state_or_region=state,
                    date=date,
                    defaults={
                        "vaccinated": vaccinated,
                        "deaths": deaths,
                        "population": base_vaccinated * 2,
                    }
                )
    
    print("Dados de exemplo gerados com sucesso!")

if __name__ == "__main__":
    # Tentar coletar dados reais
    owid_data = fetch_owid_data()
    
    if owid_data:
        process_owid_data(owid_data)
    else:
        print("Usando dados de exemplo...")
        generate_sample_data()
