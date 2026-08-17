"""
LH Nautical - Question 5 Detailed Calendar Analysis Script
Author: Senior AI Analyst
"""

import sys
import pandas as pd
import numpy as np

# Force UTF-8 stdout
sys.stdout.reconfigure(encoding='utf-8')

# Load orders
orders = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\orders.csv')

# Inspect channels
print("Channels present in orders:", orders['channel'].unique())

# Filter physical stores (channel == 'pos')
pos_orders = orders[orders['channel'].str.lower() == 'pos'].copy()

# Date handling on placed_at / created_at
# Use placed_at (or created_at if placed_at missing)
pos_orders['order_date'] = pd.to_datetime(pos_orders['placed_at']).dt.date

min_date = pos_orders['order_date'].min()
max_date = pos_orders['order_date'].max()

print(f"POS Orders Date Range: {min_date} to {max_date}")
print(f"Total POS Orders: {len(pos_orders)}")

# Generate COMPLETE calendar from min_date to max_date
full_calendar = pd.DataFrame({'date': pd.date_range(start=min_date, end=max_date).date})

# Map day of week in Portuguese
# Python dayofweek: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday
weekday_map = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}

full_calendar['day_num'] = pd.to_datetime(full_calendar['date']).dt.dayofweek
full_calendar['dia_semana'] = full_calendar['day_num'].map(weekday_map)

# Aggregate daily sales for POS
daily_pos_sales = pos_orders.groupby('order_date')['total'].sum().reset_index()
daily_pos_sales.columns = ['date', 'venda_diaria']

# Merge full calendar with daily POS sales (LEFT JOIN)
calendar_sales = full_calendar.merge(daily_pos_sales, on='date', how='left').fillna({'venda_diaria': 0.0})

# 1. Naive intern calculation (ignoring zero-sale days)
naive_avg = daily_pos_sales.merge(full_calendar[['date', 'dia_semana', 'day_num']], on='date') \
    .groupby(['day_num', 'dia_semana'])['venda_diaria'].mean().reset_index() \
    .sort_values(by='day_num')

# 2. Correct calculation (including zero-sale days)
correct_avg = calendar_sales.groupby(['day_num', 'dia_semana']).agg(
    dias_totais_calendario=('date', 'count'),
    dias_com_venda=('venda_diaria', lambda x: (x > 0).sum()),
    dias_sem_venda=('venda_diaria', lambda x: (x == 0).sum()),
    faturamento_total=('venda_diaria', 'sum'),
    venda_media_correta=('venda_diaria', 'mean')
).reset_index().sort_values(by='venda_media_correta')

print("\n=========================================================================================")
print("COMPARATIVO: CÁLCULO INCORRETO (ESTAGIÁRIO) vs CÁLCULO CORRETO (COM CALENDÁRIO COMPLETO)")
print("=========================================================================================")
print(f"{'Dia da Semana':15s} | {'Total Dias Cal.':15s} | {'Dias c/ Venda':13s} | {'Dias s/ Venda':13s} | {'Média Errada (Estagiário)':26s} | {'Média Correta (Sr. Almir)':25s}")
print("-" * 115)

for idx, row in correct_avg.iterrows():
    # Find naive mean for this weekday
    naive_val = naive_avg[naive_avg['day_num'] == row['day_num']]['venda_diaria'].values[0]
    print(f"{row['dia_semana']:15s} | {row['dias_totais_calendario']:15d} | {row['dias_com_venda']:13d} | {row['dias_sem_venda']:13d} | R$ {naive_val:22.2f} | R$ {row['venda_media_correta']:21.2f}")

worst_day = correct_avg.iloc[0]
print("\n=========================================================================================")
print(f"PIOR DIA DA SEMANA NAS LOJAS FÍSICAS (POS): {worst_day['dia_semana'].upper()}")
print(f"Média Real Diária: R$ {worst_day['venda_media_correta']:.2f}")
print("=========================================================================================")
