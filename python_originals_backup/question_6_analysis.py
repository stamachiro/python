"""
LH Nautical - Question 6 Demand Forecasting Script
Author: Senior AI Analyst
"""

import sys
import pandas as pd
import numpy as np

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

# Load files
products = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\products.csv')
product_variants = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\product_variants.csv')
orders = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\orders.csv')
order_items = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\order_items.csv')

# Find product 'Bússola de Bordo 702'
print("Searching for product 'Bússola de Bordo 702'...")
products['clean_name'] = products['name'].apply(lambda x: x.encode('latin1').decode('utf-8', errors='ignore') if isinstance(x, str) else x)

bussola_prod = products[products['clean_name'].str.contains('Bússola de Bordo 702', case=False, na=False)]
if bussola_prod.empty:
    bussola_prod = products[products['name'].str.contains('702', case=False, na=False)]

print("Found product(s):")
print(bussola_prod[['id', 'name', 'clean_name']])

prod_id = bussola_prod.iloc[0]['id']

# Merge datasets
variants = product_variants[product_variants['product_id'] == prod_id]
variant_ids = variants['id'].tolist()

items = order_items[order_items['product_variant_id'].isin(variant_ids)].copy()
merged = items.merge(orders[['id', 'created_at', 'status']], left_on='order_id', right_on='id')

merged['dt'] = pd.to_datetime(merged['created_at'])
merged['year_month'] = merged['dt'].dt.to_period('M')

# Aggregate monthly sales volume (quantity)
monthly_sales = merged.groupby('year_month')['quantity'].sum().reset_index()

# Ensure all months from 2020-01 to 2026-03 exist in index
all_months = pd.period_range(start='2020-01', end='2026-12', freq='M')
full_monthly = pd.DataFrame({'year_month': all_months})
full_monthly = full_monthly.merge(monthly_sales, on='year_month', how='left').fillna({'quantity': 0})
full_monthly['quantity'] = full_monthly['quantity'].astype(int)

print("\nMonthly Sales History (Last 12 months up to Q1 2026):")
print(full_monthly[full_monthly['year_month'] >= '2025-01'].to_string(index=False))

# Build Baseline Model: 3-month moving average (MA3)
# To forecast Jan 2026: avg of Oct 2025, Nov 2025, Dec 2025
# To forecast Feb 2026: avg of Nov 2025, Dec 2025, Jan 2026 (or pure historical Oct, Nov, Dec depending on rolling vs expanding baseline)
# Standard rolling 3-month MA:
full_monthly['ma3_pred'] = full_monthly['quantity'].shift(1).rolling(window=3).mean()

# Filter Q1 2026 (Jan 2026, Feb 2026, Mar 2026)
q1_2026 = full_monthly[(full_monthly['year_month'] >= '2026-01') & (full_monthly['year_month'] <= '2026-03')].copy()

# Forecast for Jan 2026, Feb 2026, Mar 2026
# Let's inspect both rolling prediction (using previous actuals) and static baseline prediction (using Oct, Nov, Dec 2025)
print("\n=========================================================================================")
print("PREVISÕES DO MODELO BASELINE (MÉDIA MÓVEL DE 3 MESES) PARA O PRIMEIRO TRIMESTRE DE 2026 (Q1 2026)")
print("=========================================================================================")

q1_2026['abs_error'] = np.abs(q1_2026['quantity'] - q1_2026['ma3_pred'])
mae = q1_2026['abs_error'].mean()

for idx, row in q1_2026.iterrows():
    print(f"Mês: {row['year_month']} | Venda Real (y): {row['quantity']:3d} un | Previsão Média Móvel (ŷ): {row['ma3_pred']:6.2f} un | Erro Absoluto |y - ŷ|: {row['abs_error']:6.2f}")

print("-" * 95)
print(f"MAE (Mean Absolute Error) no Q1 2026: {mae:.2f} unidades")
print("=========================================================================================")
