import sqlite3
import pandas as pd
import os
data_dir = r'C:\Users\stama\Downloads\1-lh_nautical_csv'
orders_path = os.path.join(data_dir, 'orders.csv')
print("Carregando orders.csv no banco de dados local temporário...")
conn = sqlite3.connect(':memory:')
df_orders = pd.read_csv(orders_path, low_memory=False)
df_orders.to_sql('orders', conn, index=False, if_exists='replace')
sql_query = """
SELECT
    COUNT(*) AS total_linhas,
    MIN(created_at) AS data_minima,
    MAX(created_at) AS data_maxima,
    MIN(total) AS valor_minimo,
    MAX(total) AS valor_maximo,
    ROUND(AVG(total), 2) AS valor_medio
FROM orders;
