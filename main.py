from pathlib import Path

from pipeline.encrypt import encrypt_sensitive_fields, get_or_create_key
from pipeline.extract import read_customer_data
from pipeline.load import save_csv, save_to_sqlite
from pipeline.transform import clean_customer_data, create_summary_report


BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw_customers.csv"
CLEANED_DATA_PATH = BASE_DIR / "data" / "cleaned_data.csv"
SUMMARY_REPORT_PATH = BASE_DIR / "data" / "summary_report.csv"
DATABASE_PATH = BASE_DIR / "database" / "customers.db"
KEY_PATH = BASE_DIR / "encryption.key"


def run_pipeline() -> None:
    """Run the full ETL pipeline from CSV input to secure analytics outputs."""
    raw_customers = read_customer_data(RAW_DATA_PATH)
    cleaned_customers = clean_customer_data(raw_customers)

    encryption_key = get_or_create_key(KEY_PATH)
    secure_customers = encrypt_sensitive_fields(cleaned_customers, encryption_key)

    summary_report = create_summary_report(cleaned_customers)

    save_to_sqlite(secure_customers, DATABASE_PATH)
    save_csv(secure_customers, CLEANED_DATA_PATH)
    save_csv(summary_report, SUMMARY_REPORT_PATH)

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
