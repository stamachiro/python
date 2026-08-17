"""
LH Nautical - Fetch Real Orders Examples
Author: Senior AI Analyst
"""

import sys
import os
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

data_dir = r'C:\Users\stama\Downloads\1-lh_nautical_csv'
orders = pd.read_csv(os.path.join(data_dir, 'orders.csv'))
order_items = pd.read_csv(os.path.join(data_dir, 'order_items.csv'))
product_variants = pd.read_csv(os.path.join(data_dir, 'product_variants.csv'))
products = pd.read_csv(os.path.join(data_dir, 'products.csv'), encoding='latin1')
customers = pd.read_csv(os.path.join(data_dir, 'customers.csv'), encoding='latin1')

products['clean_name'] = products['name'].apply(lambda x: x.encode('latin1').decode('utf-8', errors='ignore') if isinstance(x, str) else x)
customers['clean_name'] = customers['legal_name'].apply(lambda x: x.encode('latin1').decode('utf-8', errors='ignore') if isinstance(x, str) else x)

print("=========================================================================================")
print("EXEMPLOS REAIS DE PEDIDOS EXTRAÍDOS DIRETAMENTE DO BANCO DE DADOS DA LH NAUTICAL")
print("=========================================================================================\n")

# Pick specific interesting order IDs: Pedido #1 (Small/Medium), Pedido #2 (High Value), Pedido Max (Highest), Pedido Min (Lowest)
max_order_id = orders.loc[orders['total'].idxmax()]['id']
min_order_id = orders.loc[orders['total'].idxmin()]['id']

selected_orders = [1, 2, max_order_id, min_order_id]

for oid in selected_orders:
    ord_row = orders[orders['id'] == oid].iloc[0]
    cust_row = customers[customers['id'] == ord_row['customer_id']].iloc[0]
    
    # Items in this order
    items_in_order = order_items[order_items['order_id'] == oid].merge(
        product_variants[['id', 'product_id']], left_on='product_variant_id', right_on='id'
    ).merge(
        products[['id', 'clean_name']], left_on='product_id', right_on='id'
    )
    
    print(f"📦 PEDIDO Nº: {ord_row['order_number']} (ID no Banco: {ord_row['id']})")
    print(f"   📅 Data do Pedido: {ord_row['created_at']}")
    print(f"   🛒 Canal de Venda: {ord_row['channel'].upper()}")
    print(f"   👤 Cliente: {cust_row['clean_name']} (ID Cliente: {ord_row['customer_id']})")
    print(f"   🚦 Status do Pedido: {ord_row['status'].upper()}")
    print(f"   💰 Subtotal: R$ {ord_row['subtotal']:,.2f}")
    print(f"   🏷️ Desconto: R$ {ord_row['discount_amount']:,.2f}")
    print(f"   💵 VALOR TOTAL FINAL: R$ {ord_row['total']:,.2f}")
    print(f"   🛍️ Itens Incluídos no Pedido:")
    
    for idx, item in items_in_order.iterrows():
        print(f"      • {item['quantity']}x {item['clean_name']} | Preço Unitário: R$ {item['unit_price']:,.2f} | Total do Item: R$ {item['line_total']:,.2f}")
    
    print("-" * 85 + "\n")
