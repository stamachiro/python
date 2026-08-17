"""
LH Nautical - Teste Básico do Pandas
"""

import pandas as pd

# Lendo o arquivo de pedidos da LH Nautical
df_orders = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\orders.csv')

print("=== PRIMEIRAS 5 LINHAS DA TABELA DE PEDIDOS ===")
print(df_orders.head())

print("\n=== FORMATO DA TABELA (LINHAS, COLUNAS) ===")
print("Formato (Linhas, Colunas):", df_orders.shape)
