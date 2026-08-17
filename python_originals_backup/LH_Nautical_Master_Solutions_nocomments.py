import os
import sys
import csv
import re
from datetime import datetime
from pathlib import Path
import pandas as pd
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
data_dir = r'C:\Users\stama\Downloads\1-lh_nautical_csv'
print(">>> EXECUÇÃO DA QUESTÃO 1 - EDA <<<")
df_orders = pd.read_csv(os.path.join(data_dir, 'orders.csv'), low_memory=False)
rows, cols = df_orders.shape
created_at_dt = pd.to_datetime(df_orders['created_at'])
min_date, max_date = created_at_dt.min(), created_at_dt.max()
total_min = df_orders['total'].min()
total_max = df_orders['total'].max()
total_mean = df_orders['total'].mean()
print(f"Linhas: {rows:,} | Colunas: {cols}")
print(f"Intervalo de Datas: {min_date} a {max_date}")
print(f"Mínimo: R$ {total_min:,.2f} | Máximo: R$ {total_max:,.2f} | Média: R$ {total_mean:,.2f}\n")
print(">>> EXECUÇÃO DA QUESTÃO 2 & 3 - SCHEMA E CARREGAMENTO <<<")
print("Schema gerado em 'schema.sql' usando apenas biblioteca padrão do Python (csv, os, re, datetime).")
print("Loader em batch 'data_loader.py' pronto para ingestão no PostgreSQL via COPY.\n")
print(">>> EXECUÇÃO DA QUESTÃO 4 - CLIENTES DE ELITE <<<")
order_items = pd.read_csv(os.path.join(data_dir, 'order_items.csv'))
products = pd.read_csv(os.path.join(data_dir, 'products.csv'), encoding='latin1')
product_variants = pd.read_csv(os.path.join(data_dir, 'product_variants.csv'))
categories = pd.read_csv(os.path.join(data_dir, 'categories.csv'), encoding='latin1')
products['clean_name'] = products['name'].apply(lambda x: x.encode('latin1').decode('utf-8', errors='ignore') if isinstance(x, str) else x)
categories['clean_name'] = categories['name'].apply(lambda x: x.encode('latin1').decode('utf-8', errors='ignore') if isinstance(x, str) else x)
items_ren = order_items.rename(columns={'id': 'order_item_id'})
variants_ren = product_variants.rename(columns={'id': 'variant_id'})
products_ren = products.rename(columns={'id': 'product_id_pk'})
orders_ren = df_orders.rename(columns={'id': 'order_id_pk'})
categories_ren = categories.rename(columns={'id': 'category_id_pk'})
items_full = items_ren.merge(variants_ren[['variant_id', 'product_id']], left_on='product_variant_id', right_on='variant_id')
items_full = items_full.merge(products_ren[['product_id_pk', 'category_id']], left_on='product_id', right_on='product_id_pk')
items_full = items_full.merge(orders_ren[['order_id_pk', 'customer_id', 'total']], left_on='order_id', right_on='order_id_pk')
cust_orders = df_orders.groupby('customer_id').agg(faturamento_total=('total', 'sum'), frequencia=('id', 'nunique')).reset_index()
cust_orders['ticket_medio'] = cust_orders['faturamento_total'] / cust_orders['frequencia']
cust_categories = items_full.groupby('customer_id')['category_id'].nunique().reset_index().rename(columns={'category_id': 'diversidade_categorias'})
cust_stats = cust_orders.merge(cust_categories, on='customer_id', how='left').fillna({'diversidade_categorias': 0})
cust_stats['diversidade_categorias'] = cust_stats['diversidade_categorias'].astype(int)
top10_elite = cust_stats[cust_stats['diversidade_categorias'] >= 13].sort_values(by=['ticket_medio', 'customer_id'], ascending=[False, True]).head(10)
print(top10_elite[['customer_id', 'ticket_medio', 'faturamento_total', 'frequencia', 'diversidade_categorias']].to_string(index=False))
top10_items = items_full[items_full['customer_id'].isin(top10_elite['customer_id'])]
cat_breakdown = top10_items.groupby('category_id')['quantity'].sum().reset_index().merge(categories_ren[['category_id_pk', 'clean_name']], left_on='category_id', right_on='category_id_pk').sort_values(by='quantity', ascending=False)
print(f"Categoria mais comprada pela Elite: {cat_breakdown.iloc[0]['clean_name']} ({cat_breakdown.iloc[0]['quantity']} unidades)\n")
print(">>> EXECUÇÃO DA QUESTÃO 5 - PIOR DIA DA SEMANA (POS) <<<")
pos = df_orders[df_orders['channel'].str.lower() == 'pos'].copy()
pos['order_date'] = pd.to_datetime(pos['created_at']).dt.date
min_d, max_d = pos['order_date'].min(), pos['order_date'].max()
full_dates = pd.date_range(min_d, max_d)
calendar = pd.DataFrame({'date_dt': full_dates})
calendar['date'] = calendar['date_dt'].dt.date
weekday_pt = {0: 'Segunda-feira', 1: 'Terça-feira', 2: 'Quarta-feira', 3: 'Quinta-feira', 4: 'Sexta-feira', 5: 'Sábado', 6: 'Domingo'}
calendar['dia_semana'] = calendar['date_dt'].dt.dayofweek.map(weekday_pt)
daily_sales = pos.groupby('order_date')['total'].sum().reset_index().rename(columns={'order_date': 'date', 'total': 'faturamento_diario'})
merged_cal = calendar.merge(daily_sales, on='date', how='left').fillna({'faturamento_diario': 0.0})
correct_summary = merged_cal.groupby('dia_semana')['faturamento_diario'].mean().reset_index().sort_values(by='faturamento_diario')
print(f"Pior dia da semana real (Lojas Físicas): {correct_summary.iloc[0]['dia_semana'].upper()} (Média: R$ {correct_summary.iloc[0]['faturamento_diario']:,.2f}/dia)\n")
print(">>> EXECUÇÃO DA QUESTÃO 6 - PREVISÃO DE DEMANDA <<<")
prod_ids = products[products['clean_name'] == 'Bússola de Bordo 702']['id'].tolist()
v_ids = product_variants[product_variants['product_id'].isin(prod_ids)]['id'].tolist()
items_bussola = order_items[order_items['product_variant_id'].isin(v_ids)].merge(orders_ren[['order_id_pk', 'created_at']], left_on='order_id', right_on='order_id_pk')
items_bussola['ym'] = pd.to_datetime(items_bussola['created_at']).dt.to_period('M')
monthly_bussola = items_bussola.groupby('ym')['quantity'].sum().reset_index()
all_months = pd.period_range('2020-01', '2026-12', freq='M')
df_forecast = pd.DataFrame({'ym': all_months}).merge(monthly_bussola, on='ym', how='left').fillna({'quantity': 0})
df_forecast['quantity'] = df_forecast['quantity'].astype(int)
df_forecast['ma3_pred'] = df_forecast['quantity'].shift(1).rolling(3).mean()
q1_2026 = df_forecast[(df_forecast['ym'] >= '2026-01') & (df_forecast['ym'] <= '2026-03')].copy()
q1_2026['abs_err'] = np.abs(q1_2026['quantity'] - q1_2026['ma3_pred'])
mae = q1_2026['abs_err'].mean()
print(f"MAE do Modelo Baseline no Q1 2026: {mae:.2f} unidades")
print("Baseline Inadequado: Não capta a forte sazonalidade de pico no verão náutico.\n")
print(">>> EXECUÇÃO DA QUESTÃO 7 - SISTEMA DE RECOMENDAÇÃO <<<")
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
df_recs = pd.DataFrame({'product_id': ref_sim.index, 'cosine_similarity': ref_sim.values}).merge(products[['id', 'clean_name']], left_on='product_id', right_on='id')
print("Top 5 Recomendações para Motor de Popa 1949:")
for idx, row in df_recs.iterrows():
    print(f"  {idx+1}º | Product ID: {row['product_id']:3d} | Similaridade Cosseno: {row['cosine_similarity']:.4f} | Produto: {row['clean_name']}")
print("\n===================================================================================")
print("[CONCLUÍDO] Todas as 7 questões calculadas com sucesso!")
print("===================================================================================")
