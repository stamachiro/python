import os
import sys
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
data_dir = r'C:\Users\stama\Downloads\1-lh_nautical_csv'
tables = ['customers', 'orders', 'order_items', 'payments']
results = {}
total_sum = 0
for t in tables:
    csv_path = os.path.join(data_dir, f'{t}.csv')
    df = pd.read_csv(csv_path, low_memory=False)
    count = len(df)
    results[t] = count
    total_sum += count
print("")
print("CONTAGEM DE LINHAS INDIVIDUAL E SOMA TOTAL")
print("")
for t, cnt in results.items():
    print(f"Tabela '{t}': {cnt:,} linhas")
print("-" * 58)
print(f"TOTAL SOMADO DAS 4 TABELAS: {total_sum:,} linhas")
print("")
