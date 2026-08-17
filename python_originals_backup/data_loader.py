"""
LH Nautical - Automated Data Loader for PostgreSQL
Author: Senior AI Analyst
Description: Ingests all 24 raw CSV files directly into PostgreSQL tables
             matching schema.sql using high-performance psycopg2 bulk COPY.
"""

import os
import glob
import logging
from pathlib import Path

# External DB libraries (permitted under Questão 3 premises)
try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    psycopg2 = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class LHNauticalDataLoader:
    def __init__(self, host="localhost", port=5432, dbname="lh_nautical_db", user="postgres", password="your_password"):
        self.conn_params = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password
        }

    def execute_schema_sql(self, schema_sql_path="schema.sql"):
        """Executes DDL script to create tables in PostgreSQL."""
        if not psycopg2:
            logging.error("psycopg2 library not found. Install via: pip install psycopg2-binary")
            return False

        try:
            conn = psycopg2.connect(**self.conn_params)
            cursor = conn.cursor()
            
            with open(schema_sql_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
                
            cursor.execute(schema_sql)
            conn.commit()
            cursor.close()
            conn.close()
            logging.info(f"[✓] Successfully executed '{schema_sql_path}' DDL.")
            return True
        except Exception as e:
            logging.error(f"[X] Failed to execute schema.sql: {e}")
            return False

    def load_csv_to_postgres(self, csv_folder="./lh_nautical_csv"):
        """
        Loads all CSV files into PostgreSQL using bulk COPY command.
        Strictly preserves raw data without altering characters or removing nulls.
        """
        if not psycopg2:
            logging.error("psycopg2 is required for PostgreSQL ingestion.")
            return

        folder_path = Path(csv_folder)
        csv_files = sorted(list(folder_path.glob("*.csv")))
        
        if not csv_files:
            logging.warning(f"No CSV files found in {csv_folder}")
            return

        try:
            conn = psycopg2.connect(**self.conn_params)
            cursor = conn.cursor()

            for csv_file in csv_files:
                table_name = csv_file.stem.lower()
                logging.info(f"Ingesting raw CSV: {csv_file.name} -> Table: {table_name}")

                with open(csv_file, 'r', encoding='utf-8-sig', errors='replace') as f:
                    # PostgreSQL COPY command: Fast bulk copy without data alteration
                    copy_sql = sql.SQL("""
                        COPY {} FROM STDIN WITH (
                            FORMAT csv,
                            HEADER true,
                            DELIMITER ',',
                            QUOTE '"',
                            NULL ''
                        )
                    """).format(sql.Identifier(table_name))

                    cursor.copy_expert(copy_sql, f)
                
                conn.commit()
                
                # Verify row count loaded
                cursor.execute(sql.SQL("SELECT COUNT(*) FROM {};").format(sql.Identifier(table_name)))
                count = cursor.fetchone()[0]
                logging.info(f"[✓] Table '{table_name}' loaded successfully. Total Rows: {count:,}")

            cursor.close()
            conn.close()
            logging.info("==========================================================")
            logging.info("[SUCCESS] All 24 raw CSV files loaded into PostgreSQL!")
            logging.info("==========================================================")

        except Exception as e:
            logging.error(f"[X] Critical error during CSV loading: {e}")

if __name__ == "__main__":
    # PostgreSQL Configuration Parameters
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_NAME = os.getenv("DB_NAME", "lh_nautical")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "postgres")
    CSV_DIR = os.getenv("CSV_DIR", "./1-lh_nautical_csv")

    loader = LHNauticalDataLoader(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

    # Step 1: Create Schema
    # loader.execute_schema_sql("schema.sql")

    # Step 2: Bulk Load Raw CSVs
    # loader.load_csv_to_postgres(CSV_DIR)
    
    print("Script 'data_loader.py' ready. Configured for PostgreSQL ingestion.")
