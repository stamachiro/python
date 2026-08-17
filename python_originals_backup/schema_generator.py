"""
LH Nautical - Schema Generator for PostgreSQL
Author: Senior AI Analyst
Description: Pure Python 3 script (standard library only: csv, os, sys, datetime, re, pathlib)
             that reads all CSV files in a directory, infers PostgreSQL data types,
             and generates a single 'schema.sql' file with CREATE TABLE statements.
"""

import csv
import os
import re
from datetime import datetime
from pathlib import Path

def is_integer(val_str):
    """Checks if string represents an integer."""
    if not val_str:
        return False
    try:
        int(val_str)
        return True
    except ValueError:
        return False

def is_float(val_str):
    """Checks if string represents a floating point / numeric number."""
    if not val_str:
        return False
    try:
        float(val_str)
        return True
    except ValueError:
        return False

def is_boolean(val_str):
    """Checks if string represents a boolean value."""
    if not val_str:
        return False
    return val_str.lower() in ('true', 'false', 't', 'f', '1', '0', 'yes', 'no')

def is_timestamp(val_str):
    """Checks if string represents a ISO/Standard timestamp."""
    if not val_str:
        return False
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S%z"
    ]
    for fmt in formats:
        try:
            datetime.strptime(val_str, fmt)
            return True
        except ValueError:
            pass
    return False

def is_date(val_str):
    """Checks if string represents a date YYYY-MM-DD."""
    if not val_str:
        return False
    try:
        datetime.strptime(val_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def infer_postgres_type(sample_values):
    """
    Infers the best PostgreSQL data type for a list of string values from a CSV column.
    """
    non_empty = [v.strip() for v in sample_values if v is not None and v.strip() != '']
    
    if not non_empty:
        return "TEXT"  # Default fallback if column is completely empty
        
    # Check boolean
    if all(is_boolean(v) for v in non_empty) and set(v.lower() for v in non_empty).issubset({'true', 'false', 't', 'f'}):
        return "BOOLEAN"

    # Check Integer
    if all(is_integer(v) for v in non_empty):
        max_val = max(abs(int(v)) for v in non_empty)
        if max_val < 2147483647:
            return "INTEGER"
        else:
            return "BIGINT"

    # Check Float / Numeric
    if all(is_float(v) for v in non_empty):
        return "NUMERIC(15, 2)"

    # Check Timestamp
    if all(is_timestamp(v) for v in non_empty):
        return "TIMESTAMP"

    # Check Date
    if all(is_date(v) for v in non_empty):
        return "DATE"

    # Check Text / Varchar
    max_len = max(len(v) for v in non_empty)
    if max_len <= 50:
        return "VARCHAR(50)"
    elif max_len <= 255:
        return "VARCHAR(255)"
    else:
        return "TEXT"

def generate_schema_sql(input_dir, output_file="schema.sql", max_sample_rows=5000):
    """
    Reads all CSVs from input_dir and writes SQL DDL to output_file.
    Uses ONLY standard Python 3 libraries.
    """
    input_path = Path(input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"Directory {input_dir} not found.")

    csv_files = sorted(list(input_path.glob("*.csv")))
    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return

    sql_statements = []
    sql_statements.append("-- ==========================================================")
    sql_statements.append("-- LH Nautical - Auto Generated PostgreSQL DDL Schema")
    sql_statements.append("-- Generated using pure Python 3 standard library")
    sql_statements.append(f"-- Total Tables: {len(csv_files)}")
    sql_statements.append("-- ==========================================================\n")

    for csv_file in csv_files:
        table_name = csv_file.stem.lower()
        # Clean table name to be safe in SQL
        table_name = re.sub(r'[^a-z0-9_]', '_', table_name)
        
        with open(csv_file, mode='r', encoding='utf-8-sig', errors='replace') as f:
            reader = csv.reader(f)
            try:
                headers = next(reader)
            except StopIteration:
                continue  # Empty CSV file

            # Clean headers
            clean_headers = [re.sub(r'[^a-zA-Z0-9_]', '_', h.strip().lower()) for h in headers]
            columns_data = {h: [] for h in clean_headers}

            row_count = 0
            for row in reader:
                if row_count >= max_sample_rows:
                    break
                for idx, val in enumerate(row):
                    if idx < len(clean_headers):
                        columns_data[clean_headers[idx]].append(val)
                row_count += 1

            # Infer types
            column_definitions = []
            for col in clean_headers:
                col_type = infer_postgres_type(columns_data[col])
                # Primary key heuristic for 'id' column
                if col == 'id':
                    col_def = f"    {col} INTEGER PRIMARY KEY"
                else:
                    col_def = f"    {col} {col_type}"
                column_definitions.append(col_def)

            table_ddl = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
            table_ddl += ",\n".join(column_definitions)
            table_ddl += "\n);\n"
            
            sql_statements.append(f"-- Table: {table_name}")
            sql_statements.append(table_ddl)

    output_path = Path(output_file)
    with open(output_path, mode='w', encoding='utf-8') as out_f:
        out_f.write("\n".join(sql_statements))

    print(f"[SUCCESS] Successfully generated '{output_file}' with {len(csv_files)} table definitions.")

if __name__ == "__main__":
    import sys
    
    # Target folder: default to '1-lh_nautical_csv' or command line argument
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "./1-lh_nautical_csv"
    output_sql = sys.argv[2] if len(sys.argv) > 2 else "./schema.sql"
    
    generate_schema_sql(target_dir, output_sql)
