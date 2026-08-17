import sys
import pandas as pd
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
products = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\products.csv', encoding='latin1')
product_variants = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\product_variants.csv')
orders = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\orders.csv')
order_items = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\order_items.csv')
products['clean_name'] = products['name'].apply(lambda x: x.encode('latin1').decode('utf-8', errors='ignore') if isinstance(x, str) else x)
target_prod = products[products['clean_name'].str.contains('Motor de Popa 1949', case=False, na=False)]
print("Target product search result:")
print(target_prod[['id', 'name', 'clean_name']])
if target_prod.empty:
    target_prod = products[products['name'].str.contains('1949', case=False, na=False)]
ref_product_id = target_prod.iloc[0]['id']
ref_product_name = target_prod.iloc[0]['clean_name']
print(f"\nReference Product ID: {ref_product_id} | Name: {ref_product_name}")
items_with_prod = order_items.merge(product_variants[['id', 'product_id']], left_on='product_variant_id', right_on='id')
user_prod_df = items_with_prod.merge(orders[['id', 'customer_id']], left_on='order_id', right_on='id')
interaction_matrix = user_prod_df.groupby(['customer_id', 'product_id']).size().unstack(fill_value=0)
binary_matrix = (interaction_matrix > 0).astype(int)
print(f"\nUser x Product Matrix Shape: {binary_matrix.shape} (Customers: {binary_matrix.shape[0]}, Products: {binary_matrix.shape[1]})")
product_vectors = binary_matrix.values
dot_product = np.dot(product_vectors.T, product_vectors)
norms = np.linalg.norm(product_vectors, axis=0)
norms_outer = np.outer(norms, norms)
norms_outer[norms_outer == 0] = 1e-9
cosine_sim_matrix = dot_product / norms_outer
product_ids = binary_matrix.columns.tolist()
sim_df = pd.DataFrame(cosine_sim_matrix, index=product_ids, columns=product_ids)
if ref_product_id not in sim_df.index:
    print(f"Error: {ref_product_id} not found in interaction matrix.")
    sys.exit(1)
ref_sim = sim_df[ref_product_id].copy()
ref_sim = ref_sim.drop(ref_product_id)
top5_prod_ids = ref_sim.sort_values(ascending=False).head(5)
top5_results = pd.DataFrame({
    'product_id': top5_prod_ids.index,
    'cosine_similarity': top5_prod_ids.values
}).merge(products[['id', 'clean_name', 'category_id']], left_on='product_id', right_on='id')
print("\n=========================================================================================")
print(f"RANKING DOS 5 PRODUTOS MAIS SIMILARES A: '{ref_product_name}' (ID: {ref_product_id})")
print("=========================================================================================")
for rank, (idx, row) in enumerate(top5_results.iterrows(), start=1):
    co_occurrences = dot_product[product_ids.index(ref_product_id), product_ids.index(row['product_id'])]
    print(f"Rank {rank:1d} | Product ID: {row['product_id']:3d} | Similaridade Cosseno: {row['cosine_similarity']:.4f} | Co-compras: {int(co_occurrences):3d} clientes | Produto: {row['clean_name']}")
print("=========================================================================================")
