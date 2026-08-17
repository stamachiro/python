import sys
import os
import pandas as pd
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
data_dir = r'C:\Users\stama\Downloads\1-lh_nautical_csv'
products = pd.read_csv(os.path.join(data_dir, 'products.csv'), encoding='latin1')
product_variants = pd.read_csv(os.path.join(data_dir, 'product_variants.csv'))
orders = pd.read_csv(os.path.join(data_dir, 'orders.csv'))
order_items = pd.read_csv(os.path.join(data_dir, 'order_items.csv'))
products['clean_name'] = products['name'].apply(lambda x: x.encode('latin1').decode('utf-8', errors='ignore') if isinstance(x, str) else x)
for target, label in [([74, 240], "Catálogo Completo (IDs 74 + 240)"), ([74], "Produto ID 74 Isolado")]:
    v_ids = product_variants[product_variants['product_id'].isin(target)]['id'].tolist()
    items = order_items[order_items['product_variant_id'].isin(v_ids)].merge(orders[['id', 'created_at']], left_on='order_id', right_on='id')
    items['ym'] = pd.to_datetime(items['created_at']).dt.to_period('M')
    monthly = items.groupby('ym')['quantity'].sum().reset_index()
    all_m = pd.DataFrame({'ym': pd.period_range('2020-01', '2026-12', freq='M')}).merge(monthly, on='ym', how='left').fillna(0)
    all_m['quantity'] = all_m['quantity'].astype(int)
    all_m['ma3'] = all_m['quantity'].shift(1).rolling(3).mean()
    q1 = all_m[(all_m['ym'] >= '2026-01') & (all_m['ym'] <= '2026-03')].copy()
    sum_exact = q1['ma3'].sum()
    sum_rounded = round(sum_exact)
    print(f"=== {label} ===")
    for _, r in q1.iterrows():
        print(f"  Mês: {r['ym']} | Previsão Mensal (ŷ): {r['ma3']:.4f} unidades")
    print(f"  --> Soma Total Exata: {sum_exact:.4f}")
    print(f"  --> SOMA TOTAL ARREDONDADA: {sum_rounded} unidades\n")
