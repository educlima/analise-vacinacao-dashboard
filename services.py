"""
Camada de Serviços - Demonstra POO com classes de negócio
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from django.db.models import Sum, QuerySet
from .models import VaccineData
import csv
import io
from datetime import datetime


class DataExporter(ABC):
    """Classe abstrata base para exportadores de dados"""
    
    @abstractmethod
    def export(self, data: QuerySet) -> Any:
        """Método abstrato que deve ser implementado pelas subclasses"""
        pass
    
    @abstractmethod
    def get_content_type(self) -> str:
        """Retorna o tipo de conteúdo do arquivo"""
        pass


class CSVExporter(DataExporter):
    """Exportador de dados em formato CSV"""
    
    def export(self, data: QuerySet) -> io.StringIO:
        """Exporta dados para CSV"""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['país', 'estado_região', 'data', 'vacinados', 'óbitos', 'população'])
        
        for record in data:
            writer.writerow([
                record.country,
                record.state_or_region or 'N/A',
                record.date,
                record.vaccinated,
                record.deaths,
                record.population
            ])
        
        output.seek(0)
        return output
    
    def get_content_type(self) -> str:
        return 'text/csv'


class VaccineAnalyzer:
    """
    Classe responsável por análises estatísticas de dados de vacinação
    Demonstra ENCAPSULAMENTO: dados e métodos relacionados juntos
    """
    
    def __init__(self, country: str = None):
        """Construtor da classe"""
        self._country = country  # Atributo privado (encapsulamento)
        self._data = None
    
    @property
    def country(self) -> str:
        """Getter para país (encapsulamento)"""
        return self._country
    
    @country.setter
    def country(self, value: str):
        """Setter para país com validação (encapsulamento)"""
        if not value or not isinstance(value, str):
            raise ValueError("País deve ser uma string não vazia")
        self._country = value.lower()
    
    def load_data(self):
        """Carrega dados do banco de dados"""
        if self._country:
            self._data = VaccineData.objects.filter(country=self._country)
        else:
            self._data = VaccineData.objects.all()
        return self
    
    def get_total_vaccinated(self) -> int:
        """Retorna total de vacinados"""
        if not self._data:
            self.load_data()
        result = self._data.aggregate(total=Sum('vaccinated'))
        return result['total'] or 0
    
    def get_total_deaths(self) -> int:
        """Retorna total de óbitos"""
        if not self._data:
            self.load_data()
        result = self._data.aggregate(total=Sum('deaths'))
        return result['total'] or 0
    
    def get_mortality_rate(self) -> float:
        """Calcula taxa de mortalidade"""
        vaccinated = self.get_total_vaccinated()
        deaths = self.get_total_deaths()
        
        if vaccinated == 0:
            return 0.0
        
        return round((deaths / vaccinated) * 100, 2)
    
    def get_states_ranking(self, top_n: int = 10) -> List[Dict]:
        """Retorna ranking de estados por vacinação"""
        if not self._data:
            self.load_data()
        
        states = self._data.values('state_or_region').distinct()
        results = []
        
        for state_obj in states:
            state = state_obj['state_or_region']
            if not state:
                continue
            
            data = self._data.filter(state_or_region=state).aggregate(
                vaccinated=Sum('vaccinated'),
                deaths=Sum('deaths')
            )
            
            results.append({
                'state': state,
                'vaccinated': data['vaccinated'] or 0,
                'deaths': data['deaths'] or 0
            })
        
        results.sort(key=lambda x: x['vaccinated'], reverse=True)
        return results[:top_n]
    
    def get_summary(self) -> Dict:
        """Retorna resumo completo das análises"""
        return {
            'country': self._country,
            'total_vaccinated': self.get_total_vaccinated(),
            'total_deaths': self.get_total_deaths(),
            'mortality_rate': self.get_mortality_rate(),
            'top_states': self.get_states_ranking(5)
        }


class CountryComparator:
    """
    Compara dados de vacinação entre múltiplos países
    Demonstra COMPOSIÇÃO: usa múltiplos objetos VaccineAnalyzer
    """
    
    def __init__(self, countries: List[str]):
        """Inicializa com lista de países"""
        self.countries = countries
        self.analyzers = []  # Lista de analisadores (composição)
        
        # Criar um analisador para cada país
        for country in countries:
            analyzer = VaccineAnalyzer(country)
            analyzer.load_data()
            self.analyzers.append(analyzer)
    
    def compare_vaccinated(self) -> Dict[str, int]:
        """Compara total de vacinados entre países"""
        return {
            analyzer.country: analyzer.get_total_vaccinated()
            for analyzer in self.analyzers
        }
    
    def compare_deaths(self) -> Dict[str, int]:
        """Compara total de óbitos entre países"""
        return {
            analyzer.country: analyzer.get_total_deaths()
            for analyzer in self.analyzers
        }
    
    def compare_mortality_rates(self) -> Dict[str, float]:
        """Compara taxas de mortalidade entre países"""
        return {
            analyzer.country: analyzer.get_mortality_rate()
            for analyzer in self.analyzers
        }
    
    def get_best_performance(self) -> str:
        """Retorna país com melhor desempenho (maior vacinação, menor mortalidade)"""
        rates = self.compare_mortality_rates()
        vaccinated = self.compare_vaccinated()
        
        # País com maior vacinação e menor mortalidade
        best_country = min(
            rates.items(),
            key=lambda x: (x[1], -vaccinated.get(x[0], 0))
        )
        
        return best_country[0]
    
    def generate_report(self) -> Dict:
        """Gera relatório comparativo completo"""
        return {
            'countries': self.countries,
            'vaccinated_comparison': self.compare_vaccinated(),
            'deaths_comparison': self.compare_deaths(),
            'mortality_rates': self.compare_mortality_rates(),
            'best_performer': self.get_best_performance(),
            'detailed_summaries': [
                analyzer.get_summary() for analyzer in self.analyzers
            ]
        }


class CSVImporter:
    """
    Importa dados de arquivos CSV
    Demonstra princípio de RESPONSABILIDADE ÚNICA
    """
    
    def __init__(self, country: str):
        """Inicializa importador para um país específico"""
        self.country = country.lower()
        self.imported_count = 0
        self.errors = []
    
    def validate_row(self, row: Dict) -> bool:
        """Valida uma linha do CSV"""
        required_fields = ['date', 'vaccinated', 'deaths', 'population']
        
        for field in required_fields:
            if field not in row:
                self.errors.append(f"Campo obrigatório ausente: {field}")
                return False
        
        return True
    
    def import_from_file(self, file_content: str) -> int:
        """Importa dados do arquivo CSV"""
        reader = csv.DictReader(io.StringIO(file_content))
        
        for row in reader:
            if not self.validate_row(row):
                continue
            
            try:
                vaccine_data = VaccineData(
                    country=self.country,
                    state_or_region=row.get('state_or_region', 'Nacional'),
                    date=row['date'],
                    vaccinated=int(row.get('vaccinated', 0)),
                    deaths=int(row.get('deaths', 0)),
                    population=int(row.get('population', 0))
                )
                vaccine_data.save()
                self.imported_count += 1
            except Exception as e:
                self.errors.append(f"Erro ao importar linha: {str(e)}")
                continue
        
        return self.imported_count
    
    def get_import_summary(self) -> Dict:
        """Retorna resumo da importação"""
        return {
            'country': self.country,
            'imported_count': self.imported_count,
            'errors_count': len(self.errors),
            'errors': self.errors[:10]  # Primeiros 10 erros
        }


class AnalyzerFactory:
    """
    Factory para criar diferentes tipos de analisadores
    Demonstra DESIGN PATTERN FACTORY
    """
    
    @staticmethod
    def create_analyzer(analyzer_type: str, **kwargs) -> Any:
        """Cria um analisador baseado no tipo especificado"""
        if analyzer_type == "single":
            country = kwargs.get('country')
            if not country:
                raise ValueError("País é obrigatório para análise single")
            return VaccineAnalyzer(country)
        
        elif analyzer_type == "comparator":
            countries = kwargs.get('countries', [])
            if not countries:
                raise ValueError("Lista de países é obrigatória para comparador")
            return CountryComparator(countries)
        
        else:
            raise ValueError(f"Tipo de analisador desconhecido: {analyzer_type}")
