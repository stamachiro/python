"""
LH Nautical - Power BI CSV & Data Package Generator
Author: Senior AI Analyst
Description: Exports consolidated datasets for direct import into Power BI dashboards.
"""

import sys
import os
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

data_dir = r'C:\Users\stama\Downloads\1-lh_nautical_csv'
out_dir = r'c:\Users\stama\OneDrive\Documentos\Trabalho\power_bi_exports'
os.makedirs(out_dir, exist_ok=True)

# Load base tables
orders = pd.read_csv(os.path.join(data_dir, 'orders.csv'))
order_items = pd.read_csv(os.path.join(data_dir, 'order_items.csv'))
products = pd.read_csv(os.path.join(data_dir, 'products.csv'), encoding='latin1')
product_variants = pd.read_csv(os.path.join(data_dir, 'product_variants.csv'))
categories = pd.read_csv(os.path.join(data_dir, 'categories.csv'), encoding='latin1')

products['clean_name'] = products['name'].apply(lambda x: x.encode('latin1').decode('utf-8', errors='ignore') if isinstance(x, str) else x)
categories['clean_name'] = categories['name'].apply(lambda x: x.encode('latin1').decode('utf-8', errors='ignore') if isinstance(x, str) else x)

# 1. Export Question 4 Data (Top 10 Elite Customers)
items_ren = order_items.rename(columns={'id': 'order_item_id'})
variants_ren = product_variants.rename(columns={'id': 'variant_id'})
products_ren = products.rename(columns={'id': 'product_id_pk'})
orders_ren = orders.rename(columns={'id': 'order_id_pk'})

items_full = items_ren.merge(variants_ren[['variant_id', 'product_id']], left_on='product_variant_id', right_on='variant_id')
items_full = items_full.merge(products_ren[['product_id_pk', 'category_id']], left_on='product_id', right_on='product_id_pk')
items_full = items_full.merge(orders_ren[['order_id_pk', 'customer_id', 'total']], left_on='order_id', right_on='order_id_pk')

cust_orders = orders.groupby('customer_id').agg(faturamento_total=('total', 'sum'), frequencia=('id', 'nunique')).reset_index()
cust_orders['ticket_medio'] = cust_orders['faturamento_total'] / cust_orders['frequencia']

cust_cat = items_full.groupby('customer_id')['category_id'].nunique().reset_index().rename(columns={'category_id': 'diversidade_categorias'})
cust_stats = cust_orders.merge(cust_cat, on='customer_id', how='left').fillna({'diversidade_categorias': 0})
cust_stats['diversidade_categorias'] = cust_stats['diversidade_categorias'].astype(int)

top10_elite = cust_stats[cust_stats['diversidade_categorias'] >= 13].sort_values(by=['ticket_medio', 'customer_id'], ascending=[False, True]).head(10)
top10_elite.to_csv(os.path.join(out_dir, 'bi_q4_top10_elite_customers.csv'), index=False, encoding='utf-8-sig')

# 2. Export Question 5 Data (Calendar POS Sales)
pos = orders[orders['channel'].str.lower() == 'pos'].copy()
pos['order_date'] = pd.to_datetime(pos['created_at']).dt.date
min_d, max_d = pos['order_date'].min(), pos['order_date'].max()

full_dates = pd.date_range(min_d, max_d)
calendar = pd.DataFrame({'date_dt': full_dates})
calendar['date'] = calendar['date_dt'].dt.date
weekday_pt = {0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira', 3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado', 6: 'Domingo'}
calendar['dia_semana'] = calendar['date_dt'].dt.dayofweek.map(weekday_pt)

daily_sales = pos.groupby('order_date')['total'].sum().reset_index().rename(columns={'order_date': 'date', 'total': 'faturamento_diario'})
bi_calendar_sales = calendar.merge(daily_sales, on='date', how='left').fillna({'faturamento_diario': 0.0})
bi_calendar_sales.to_csv(os.path.join(out_dir, 'bi_q5_calendar_pos_sales.csv'), index=False, encoding='utf-8-sig')

# 3. Export Question 6 Data (Demand Forecast Q1 2026)
prod_ids = products[products['clean_name'] == 'Bússola de Bordo 702']['id'].tolist()
v_ids = product_variants[product_variants['product_id'].isin(prod_ids)]['id'].tolist()
items_bussola = order_items[order_items['product_variant_id'].isin(v_ids)].merge(orders_ren[['order_id_pk', 'created_at']], left_on='order_id', right_on='order_id_pk')
items_bussola['ym'] = pd.to_datetime(items_bussola['created_at']).dt.to_period('M')

monthly_bussola = items_bussola.groupby('ym')['quantity'].sum().reset_index()
all_months = pd.period_range('2020-01', '2026-12', freq='M')
df_forecast = pd.DataFrame({'ym': all_months}).merge(monthly_bussola, on='ym', how='left').fillna({'quantity': 0})
df_forecast['quantity'] = df_forecast['quantity'].astype(int)
df_forecast['ma3_pred'] = df_forecast['quantity'].shift(1).rolling(3).mean()
df_forecast['ym_str'] = df_forecast['ym'].astype(str)
df_forecast.to_csv(os.path.join(out_dir, 'bi_q6_demand_forecast_bussola.csv'), index=False, encoding='utf-8-sig')

# 4. Export Question 7 Data (Cosine Recommendations for Motor 1949)
target_product = products[products['clean_name'] == 'Motor de Popa 1949'].iloc[0]
ref_id = target_product['id']

items_prod = order_items.merge(product_variants[['id', 'product_id']], left_on='product_variant_id', right_on='id')
u_p = items_prod.merge(orders_ren[['order_id_pk', 'customer_id']], left_on='order_id', right_on='order_id_pk')
mat = (u_p.groupby(['customer_id', 'product_id']).size().unstack(fill_value=0) > 0).astype(int)

vecs = mat.values.T
dots = np.dot(vecs, vecs.T)
norms = np.linalg.norm(vecs, axis=1)
n_mat = np.outer(norms, norms)
n_mat[n_mat == 0] = 1e-9
cos_mat = dots / n_mat

p_ids = mat.columns.tolist()
sim_df = pd.DataFrame(cos_mat, index=p_ids, columns=p_ids)
ref_sim = sim_df[ref_id].drop(ref_id).sort_values(ascending=False).head(5)

df_recs = pd.DataFrame({'product_id': ref_sim.index, 'cosine_similarity': ref_sim.values})
df_recs = df_recs.merge(products[['id', 'clean_name', 'category_id']], left_on='product_id', right_on='id')
df_recs.to_csv(os.path.join(out_dir, 'bi_q7_recommendations_motor_1949.csv'), index=False, encoding='utf-8-sig')

print(f"[SUCCESS] Exported 4 Power BI datasets to: {out_dir}")
