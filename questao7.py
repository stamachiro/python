import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

data_dir = r'C:\Users\stama\Downloads\1-lh_nautical_csv'
if not os.path.exists(data_dir):
    data_dir = r'C:\Users\stama\OneDrive\Documentos\Trabalho\1-lh_nautical_csv'
if not os.path.exists(data_dir):
    data_dir = '.'

products = pd.read_csv(os.path.join(data_dir, 'products.csv'), encoding='latin1')
product_variants = pd.read_csv(os.path.join(data_dir, 'product_variants.csv'))
orders = pd.read_csv(os.path.join(data_dir, 'orders.csv'))
order_items = pd.read_csv(os.path.join(data_dir, 'order_items.csv'))

products['clean_name'] = products['name'].apply(
    lambda x: x.encode('latin1').decode('utf-8', errors='ignore') if isinstance(x, str) else x
)

ref_product_id = products[products['clean_name'] == 'Motor de Popa 1949'].iloc[0]['id']

items_with_prod = order_items.merge(product_variants[['id', 'product_id']], left_on='product_variant_id', right_on='id')
user_prod_df = items_with_prod.merge(orders[['id', 'customer_id']], left_on='order_id', right_on='id')

interaction_matrix = (user_prod_df.groupby(['customer_id', 'product_id']).size().unstack(fill_value=0) > 0).astype(int)

sim_matrix = cosine_similarity(interaction_matrix.T)
sim_df = pd.DataFrame(sim_matrix, index=interaction_matrix.columns, columns=interaction_matrix.columns)

ref_sim = sim_df[ref_product_id].drop(ref_product_id).sort_values(ascending=False).head(5)

top5_ranking = pd.DataFrame({
    'product_id': ref_sim.index,
    'similaridade_cosseno': ref_sim.values
}).merge(products[['id', 'clean_name']], left_on='product_id', right_on='id')

print(top5_ranking[['product_id', 'clean_name', 'similaridade_cosseno']])
