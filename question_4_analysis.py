"""
LH Nautical - Question 4 Detailed Analysis Script
Author: Senior AI Analyst
"""

import sys
import pandas as pd
import numpy as np

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

# Load files
orders = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\orders.csv')
order_items = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\order_items.csv')
product_variants = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\product_variants.csv')
products = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\products.csv')
categories = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\categories.csv', encoding='latin1')

# Fix double encoding in categories
categories['clean_name'] = categories['name'].apply(lambda x: x.encode('latin1').decode('utf-8', errors='ignore') if isinstance(x, str) else x)

# Rename ID columns before joining to avoid suffix confusion
order_items_ren = order_items.rename(columns={'id': 'order_item_id'})
product_variants_ren = product_variants.rename(columns={'id': 'variant_id'})
products_ren = products.rename(columns={'id': 'product_id_pk'})
orders_ren = orders.rename(columns={'id': 'order_id_pk'})
categories_ren = categories.rename(columns={'id': 'category_id_pk'})

# 1. Join relationships
items_full = order_items_ren.merge(product_variants_ren[['variant_id', 'product_id']], left_on='product_variant_id', right_on='variant_id')
items_full = items_full.merge(products_ren[['product_id_pk', 'category_id']], left_on='product_id', right_on='product_id_pk')
items_full = items_full.merge(orders_ren[['order_id_pk', 'customer_id', 'total']], left_on='order_id', right_on='order_id_pk')

# 2. Customer metrics
cust_orders = orders.groupby('customer_id').agg(
    faturamento_total=('total', 'sum'),
    frequencia=('id', 'nunique')
).reset_index()

cust_orders['ticket_medio'] = cust_orders['faturamento_total'] / cust_orders['frequencia']

cust_categories = items_full.groupby('customer_id')['category_id'].nunique().reset_index().rename(columns={'category_id': 'diversidade_categorias'})

cust_stats = cust_orders.merge(cust_categories, on='customer_id', how='left').fillna({'diversidade_categorias': 0})
cust_stats['diversidade_categorias'] = cust_stats['diversidade_categorias'].astype(int)

# 3. Filter Elite Customers (diversidade >= 13)
elite_customers = cust_stats[cust_stats['diversidade_categorias'] >= 13].copy()

# Sort by ticket_medio DESC, customer_id ASC
top10_elite = elite_customers.sort_values(by=['ticket_medio', 'customer_id'], ascending=[False, True]).head(10)

print("=========================================================================================")
print("TOP 10 CLIENTES DE ELITE (Diversidade >= 13 Categorias)")
print("=========================================================================================")
for rank, (idx, row) in enumerate(top10_elite.iterrows(), start=1):
    print(f"Rank {rank:2d} | Customer ID: {int(row['customer_id']):4d} | Ticket Médio: R$ {row['ticket_medio']:10.2f} | Faturamento Total: R$ {row['faturamento_total']:12.2f} | Frequência: {int(row['frequencia']):2d} | Diversidade: {int(row['diversidade_categorias']):2d}")

# 4. Category breakdown for these 10 customers
top10_ids = top10_elite['customer_id'].tolist()
top10_items = items_full[items_full['customer_id'].isin(top10_ids)]

cat_breakdown = top10_items.groupby('category_id')['quantity'].sum().reset_index()
cat_breakdown = cat_breakdown.merge(categories_ren[['category_id_pk', 'clean_name']], left_on='category_id', right_on='category_id_pk')
cat_breakdown = cat_breakdown.sort_values(by='quantity', ascending=False).reset_index(drop=True)

print("\n=========================================================================================")
print("RANKING DE CATEGORIAS MAIS COMPRADAS PELOS TOP 10 CLIENTES DE ELITE")
print("=========================================================================================")
for rank, row in cat_breakdown.iterrows():
    print(f"Posição {rank+1:2d} | Category ID: {row['category_id']:2d} | Categoria: {row['clean_name']:25s} | Qtd Itens Comprados: {row['quantity']:4d}")
