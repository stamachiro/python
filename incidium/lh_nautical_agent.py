import os
import glob
import pandas as pd
import numpy as np
from pathlib import Path
class LHNauticalDataEngine:
    def __init__(self, data_dir: str = "./lh_nautical_csv"):
        self.data_dir = Path(data_dir)
        self.tables = {}
    def load_all_csvs(self):
        if not self.data_dir.exists():
            os.makedirs(self.data_dir, exist_ok=True)
            print(f"[!] Directory {self.data_dir} created. Place the 24 CSV files here.")
            return False
        csv_files = glob.glob(str(self.data_dir / "*.csv"))
        if not csv_files:
            print(f"[!] No CSV files found in {self.data_dir}.")
            return False
        for file in csv_files:
            table_name = Path(file).stem
            try:
                self.tables[table_name] = pd.read_csv(file, low_memory=False)
                print(f"[✓] Loaded {table_name}: {self.tables[table_name].shape}")
            except Exception as e:
                print(f"[X] Error loading {file}: {e}")
        return True
    def run_data_quality_audit(self):
        audit_report = {}
        for name, df in self.tables.items():
            audit_report[name] = {
                "rows": len(df),
                "columns": len(df.columns),
                "null_counts": df.isnull().sum().to_dict(),
                "duplicate_rows": df.duplicated().sum(),
                "dtypes": df.dtypes.astype(str).to_dict()
            }
        return audit_report
    def calculate_sales_and_losses(self, sales_df, products_df):
        if sales_df is not None and products_df is not None:
            merged = pd.merge(sales_df, products_df, on="product_id", how="left")
            merged['revenue'] = merged['quantity'] * merged['unit_price']
            merged['cost'] = merged['quantity'] * merged['unit_cost']
            merged['profit'] = merged['revenue'] - merged['cost']
            loss_products = merged[merged['profit'] < 0].groupby(['product_id', 'product_name'])['profit'].sum().reset_index()
            return loss_products.sort_values(by='profit')
        return None
    def calculate_customer_lifetime_value(self, sales_df, customers_df):
        if sales_df is not None and customers_df is not None:
            merged = pd.merge(sales_df, customers_df, on="customer_id", how="left")
            merged['profit'] = (merged['quantity'] * merged['unit_price']) - (merged['quantity'] * merged['unit_cost'])
            customer_profit = merged.groupby(['customer_id', 'customer_name'])['profit'].sum().reset_index()
            return customer_profit.sort_values(by='profit', ascending=False)
        return None
    def calculate_weekday_sales_with_zeroes(self, sales_df):
        if sales_df is not None:
            sales_df['date'] = pd.to_datetime(sales_df['sale_date'])
            sales_df['weekday'] = sales_df['date'].dt.day_name()
            sales_df['day_date'] = sales_df['date'].dt.date
            daily = sales_df.groupby(['day_date', 'weekday'])['quantity'].sum().reset_index()
            all_dates = pd.date_range(start=daily['day_date'].min(), end=daily['day_date'].max())
            full_df = pd.DataFrame({'day_date': all_dates.date})
            full_df['weekday'] = pd.to_datetime(full_df['day_date']).dt.day_name()
            complete_daily = pd.merge(full_df, daily[['day_date', 'quantity']], on='day_date', how='left').fillna(0)
            weekday_avg = complete_daily.groupby('weekday')['quantity'].mean().reset_index()
            return weekday_avg
        return None
if __name__ == "__main__":
    engine = LHNauticalDataEngine()
    print("LH Nautical iniciada")
