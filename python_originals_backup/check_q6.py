"""
LH Nautical - Question 6 Multi-Product Check
Author: Senior AI Analyst
"""

import sys
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

products = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\products.csv', encoding='latin1')
product_variants = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\product_variants.csv')
orders = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\orders.csv')
order_items = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\order_items.csv')

products['clean_name'] = products['name'].apply(lambda x: x.encode('latin1').decode('utf-8', errors='ignore') if isinstance(x, str) else x)

for target in [[74], [240], [74, 240]]:
    v_ids = product_variants[product_variants['product_id'].isin(target)]['id'].tolist()
    items = order_items[order_items['product_variant_id'].isin(v_ids)].copy()
    m = items.merge(orders[['id', 'created_at']], left_on='order_id', right_on='id')
    m['dt'] = pd.to_datetime(m['created_at'])
    m['ym'] = m['dt'].dt.to_period('M')
    monthly = m.groupby('ym')['quantity'].sum().reset_index()
    all_m = pd.DataFrame({'ym': pd.period_range('2020-01', '2026-12', freq='M')}).merge(monthly, on='ym', how='left').fillna(0)
    all_m['quantity'] = all_m['quantity'].astype(int)
    all_m['ma3'] = all_m['quantity'].shift(1).rolling(3).mean()
    test = all_m[(all_m['ym'] >= '2026-01') & (all_m['ym'] <= '2026-03')].copy()
    test['abs_err'] = np.abs(test['quantity'] - test['ma3'])
    
    print(f"=== TARGET PRODUCT IDs: {target} (Variants: {v_ids}) ===")
    for _, r in test.iterrows():
        print(f"  Mês: {r['ym']} | Real: {r['quantity']:2d} un | Previsão: {r['ma3']:5.2f} un | Erro: {r['abs_err']:5.2f}")
    print(f"  MAE Q1 2026: {test['abs_err'].mean():.2f} unidades\n")
