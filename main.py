"""
MAIN.PY - Ponto de entrada principal do sistema
Demonstra uso de POO (Programação Orientada a Objetos)

Conceitos de POO demonstrados:
1. ENCAPSULAMENTO - Dados e métodos juntos em classes
2. HERANÇA - Classes que estendem outras classes
3. POLIMORFISMO - Mesma interface, comportamentos diferentes
4. ABSTRAÇÃO - Classes abstratas definem contratos
5. COMPOSIÇÃO - Objetos contém outros objetos
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from vaccine.services import (
    VaccineAnalyzer,
    CountryComparator,
    CSVImporter,
    CSVExporter,
    AnalyzerFactory
)
from vaccine.models import VaccineData


def print_separator(title: str = ""):
    """Imprime separador visual"""
    print("\n" + "="*80)
    if title:
        print(f"  {title}")
        print("="*80)


def demo_encapsulamento():
    """
    Demonstração de ENCAPSULAMENTO
    Classe VaccineAnalyzer encapsula dados e operações
    """
    print_separator("1. DEMONSTRAÇÃO DE ENCAPSULAMENTO")
    
    print("\nCriando analisador para o Brasil...")
    analyzer = VaccineAnalyzer("brasil")
    analyzer.load_data()
    
    print(f"\nTotal de vacinados: {analyzer.get_total_vaccinated():,}")
    print(f"Total de óbitos: {analyzer.get_total_deaths():,}")
    print(f"Taxa de mortalidade: {analyzer.get_mortality_rate()}%")
    
    print("\n✓ Encapsulamento: Dados privados (_country, _data) acessados via métodos públicos")


def demo_heranca_polimorfismo():
    """
    Demonstração de HERANÇA e POLIMORFISMO
    CSVExporter herda de DataExporter (abstrata)
    """
    print_separator("2. DEMONSTRAÇÃO DE HERANÇA E POLIMORFISMO")
    
    print("\nCriando exportador CSV (herda de DataExporter)...")
    exporter = CSVExporter()
    
    data = VaccineData.objects.filter(country="brasil")[:5]
    csv_output = exporter.export(data)
    
    print(f"\nTipo de conteúdo: {exporter.get_content_type()}")
    print("Primeiras linhas do CSV:")
    print(csv_output.read()[:200] + "...")
    
    print("\n✓ Herança: CSVExporter estende DataExporter")
    print("✓ Polimorfismo: export() implementado de forma específica")


def demo_composicao():
    """
    Demonstração de COMPOSIÇÃO
    CountryComparator contém múltiplos VaccineAnalyzer
    """
    print_separator("3. DEMONSTRAÇÃO DE COMPOSIÇÃO")
    
    print("\nCriando comparador de países...")
    countries = ["brasil", "portugal", "italia", "usa"]
    comparator = CountryComparator(countries)
    
    print(f"\nComparação de vacinados:")
    vaccinated = comparator.compare_vaccinated()
    for country, total in vaccinated.items():
        print(f"  {country.upper()}: {total:,}")
    
    print(f"\nTaxas de mortalidade:")
    rates = comparator.compare_mortality_rates()
    for country, rate in rates.items():
        print(f"  {country.upper()}: {rate}%")
    
    best = comparator.get_best_performance()
    print(f"\n🏆 Melhor desempenho: {best.upper()}")
    
    print("\n✓ Composição: CountryComparator contém múltiplos VaccineAnalyzer")


def demo_factory_pattern():
    """
    Demonstração de FACTORY PATTERN
    AnalyzerFactory cria objetos baseado em tipo
    """
    print_separator("4. DEMONSTRAÇÃO DE FACTORY PATTERN")
    
    print("\nUsando Factory para criar analisador single...")
    analyzer = AnalyzerFactory.create_analyzer("single", country="brasil")
    summary = analyzer.get_summary()
    
    print(f"\nResumo do Brasil:")
    print(f"  Vacinados: {summary['total_vaccinated']:,}")
    print(f"  Óbitos: {summary['total_deaths']:,}")
    
    print("\nUsando Factory para criar comparador...")
    comparator = AnalyzerFactory.create_analyzer(
        "comparator",
        countries=["brasil", "portugal"]
    )
    report = comparator.generate_report()
    
    print(f"\nRelatório comparativo:")
    print(f"  Países: {', '.join(report['countries'])}")
    print(f"  Melhor desempenho: {report['best_performer'].upper()}")
    
    print("\n✓ Factory Pattern: Criação de objetos centralizada e flexível")


def demo_single_responsibility():
    """
    Demonstração de SINGLE RESPONSIBILITY PRINCIPLE
    Cada classe tem uma responsabilidade única
    """
    print_separator("5. DEMONSTRAÇÃO DE RESPONSABILIDADE ÚNICA")
    
    print("\nCSVImporter - responsável apenas por importação")
    print("VaccineAnalyzer - responsável apenas por análise")
    print("CSVExporter - responsável apenas por exportação")
    print("CountryComparator - responsável apenas por comparação")
    
    print("\n✓ Cada classe tem uma única razão para mudar")
    print("✓ Código mais fácil de manter e testar")


def generate_full_report():
    """Gera relatório completo usando todas as classes POO"""
    print_separator("RELATÓRIO COMPLETO - INTEGRANDO TODOS OS CONCEITOS POO")
    
    # Usar Factory para criar comparador
    countries = ["brasil", "portugal", "italia", "usa"]
    comparator = AnalyzerFactory.create_analyzer("comparator", countries=countries)
    
    # Gerar relatório
    report = comparator.generate_report()
    
    print(f"\n📊 ANÁLISE COMPARATIVA DE VACINAÇÃO")
    print(f"\nPaíses analisados: {', '.join([c.upper() for c in report['countries']])}")
    
    print(f"\n📈 TOTAL DE VACINADOS:")
    for country, total in report['vaccinated_comparison'].items():
        print(f"  {country.upper()}: {total:,}")
    
    print(f"\n💀 TOTAL DE ÓBITOS:")
    for country, total in report['deaths_comparison'].items():
        print(f"  {country.upper()}: {total:,}")
    
    print(f"\n📉 TAXA DE MORTALIDADE:")
    for country, rate in report['mortality_rates'].items():
        print(f"  {country.upper()}: {rate}%")
    
    print(f"\n🏆 MELHOR DESEMPENHO: {report['best_performer'].upper()}")
    
    print("\n📋 RESUMOS DETALHADOS POR PAÍS:")
    for summary in report['detailed_summaries']:
        print(f"\n  {summary['country'].upper()}:")
        print(f"    Vacinados: {summary['total_vaccinated']:,}")
        print(f"    Óbitos: {summary['total_deaths']:,}")
        print(f"    Taxa mortalidade: {summary['mortality_rate']}%")
        print(f"    Top 3 estados:")
        for i, state in enumerate(summary['top_states'][:3], 1):
            print(f"      {i}. {state['state']}: {state['vaccinated']:,} vacinados")


def main():
    """Função principal - ponto de entrada do programa"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "ANÁLISE DE VACINAÇÃO - POO" + " "*32 + "║")
    print("║" + " "*15 + "Demonstração de Programação Orientada a Objetos" + " "*15 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        # Demonstrar cada conceito de POO
        demo_encapsulamento()
        input("\nPressione ENTER para continuar...")
        
        demo_heranca_polimorfismo()
        input("\nPressione ENTER para continuar...")
        
        demo_composicao()
        input("\nPressione ENTER para continuar...")
        
        demo_factory_pattern()
        input("\nPressione ENTER para continuar...")
        
        demo_single_responsibility()
        input("\nPressione ENTER para continuar...")
        
        # Relatório final integrando tudo
        generate_full_report()
        
        print_separator("DEMONSTRAÇÃO CONCLUÍDA")
        print("\n✅ Todos os conceitos de POO foram demonstrados com sucesso!")
        print("\nConceitos cobertos:")
        print("  1. Encapsulamento (VaccineAnalyzer)")
        print("  2. Herança (CSVExporter extends DataExporter)")
        print("  3. Polimorfismo (export() method)")
        print("  4. Abstração (DataExporter abstract class)")
        print("  5. Composição (CountryComparator has VaccineAnalyzers)")
        print("  6. Factory Pattern (AnalyzerFactory)")
        print("  7. Single Responsibility (cada classe uma responsabilidade)")
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
