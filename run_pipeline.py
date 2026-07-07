from src.ingestion.bronze_ingestion import ingest_raw_to_bronze
from src.processing.silver_processing import process_bronze_to_silver
from src.quality.data_quality import validate_data
from src.transformations.gold_kpis import build_gold_kpis
from src.transformations.warehouse_builder import build_dimensional_warehouse
from src.transformations.duckdb_loader import load_csv_to_duckdb


def run_pipeline():
    print("Iniciando pipeline hospitalar...")
    ingest_raw_to_bronze()
    process_bronze_to_silver()
    validate_data()
    build_gold_kpis()
    build_dimensional_warehouse()
    load_csv_to_duckdb()
    print("Pipeline finalizado com sucesso.")


if __name__ == "__main__":
    run_pipeline()