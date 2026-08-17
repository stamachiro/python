import sys
import pandas as pd
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
products = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\products.csv')
product_variants = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\product_variants.csv')
orders = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\orders.csv')
order_items = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\order_items.csv')
print("Searching for product 'Bússola de Bordo 702'...")
products['clean_name'] = products['name'].apply(lambda x: x.encode('latin1').decode('utf-8', errors='ignore') if isinstance(x, str) else x)
bussola_prod = products[products['clean_name'].str.contains('Bússola de Bordo 702', case=False, na=False)]
if bussola_prod.empty:
    bussola_prod = products[products['name'].str.contains('702', case=False, na=False)]
print("Found product(s):")
print(bussola_prod[['id', 'name', 'clean_name']])
prod_id = bussola_prod.iloc[0]['id']
variants = product_variants[product_variants['product_id'] == prod_id]
variant_ids = variants['id'].tolist()
items = order_items[order_items['product_variant_id'].isin(variant_ids)].copy()
merged = items.merge(orders[['id', 'created_at', 'status']], left_on='order_id', right_on='id')
merged['dt'] = pd.to_datetime(merged['created_at'])
merged['year_month'] = merged['dt'].dt.to_period('M')
monthly_sales = merged.groupby('year_month')['quantity'].sum().reset_index()
all_months = pd.period_range(start='2020-01', end='2026-12', freq='M')
full_monthly = pd.DataFrame({'year_month': all_months})
full_monthly = full_monthly.merge(monthly_sales, on='year_month', how='left').fillna({'quantity': 0})
full_monthly['quantity'] = full_monthly['quantity'].astype(int)
print("\nMonthly Sales History (Last 12 months up to Q1 2026):")
print(full_monthly[full_monthly['year_month'] >= '2025-01'].to_string(index=False))
full_monthly['ma3_pred'] = full_monthly['quantity'].shift(1).rolling(window=3).mean()
q1_2026 = full_monthly[(full_monthly['year_month'] >= '2026-01') & (full_monthly['year_month'] <= '2026-03')].copy()
print("\n")
print("Previsão do modelo (Media Movel De 3 Meses) Para o primeiro semestre (Q1 2026)")
print("")
q1_2026['abs_error'] = np.abs(q1_2026['quantity'] - q1_2026['ma3_pred'])
mae = q1_2026['abs_error'].mean()
for idx, row in q1_2026.iterrows():
    print(f"Mês: {row['year_month']} | Venda Real (y): {row['quantity']:3d} un | Previsão Média Móvel (ŷ): {row['ma3_pred']:6.2f} un | Erro Absoluto |y - ŷ|: {row['abs_error']:6.2f}")
print("-" * 95)
print(f"Erro ao Processar no Q1 2026: {mae:.2f} unidades")
print("")
