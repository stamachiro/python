import sys
import pandas as pd
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
orders = pd.read_csv(r'C:\Users\stama\Downloads\1-lh_nautical_csv\orders.csv')
pos = orders[orders['channel'] == 'pos'].copy()
pos['order_date'] = pd.to_datetime(pos['created_at']).dt.date
min_date = pos['order_date'].min()
max_date = pos['order_date'].max()
print(f"Min Date: {min_date} | Max Date: {max_date}")
full_dates = pd.date_range(start=min_date, end=max_date, freq='D')
calendar = pd.DataFrame({'date_dt': full_dates})
calendar['date'] = calendar['date_dt'].dt.date
calendar['weekday_name_en'] = calendar['date_dt'].dt.day_name()
calendar['day_num'] = calendar['date_dt'].dt.dayofweek
weekday_pt = {
    0: 'Segunda-feira',
    1: 'Terça-feira',
    2: 'Quarta-feira',
    3: 'Quinta-feira',
    4: 'Sexta-feira',
    5: 'Sábado',
    6: 'Domingo'
}
calendar['dia_semana'] = calendar['day_num'].map(weekday_pt)
daily_sales = pos.groupby('order_date')['total'].sum().reset_index()
daily_sales.columns = ['date', 'faturamento_diario']
merged = calendar.merge(daily_sales, on='date', how='left').fillna({'faturamento_diario': 0.0})
naive = daily_sales.merge(calendar[['date', 'dia_semana', 'day_num']], on='date') \
    .groupby(['day_num', 'dia_semana']) \
    .agg(
        dias_com_venda=('faturamento_diario', 'count'),
        faturamento_total=('faturamento_diario', 'sum'),
        media_estagiario=('faturamento_diario', 'mean')
    ).reset_index()
correct = merged.groupby(['day_num', 'dia_semana']) \
    .agg(
        dias_totais_calendario=('date', 'count'),
        dias_com_venda=('faturamento_diario', lambda x: (x > 0).sum()),
        dias_sem_venda=('faturamento_diario', lambda x: (x == 0).sum()),
        faturamento_total=('faturamento_diario', 'sum'),
        media_correta=('faturamento_diario', 'mean')
    ).reset_index()
summary = correct.merge(naive[['day_num', 'media_estagiario']], on='day_num')
summary = summary.sort_values(by='media_correta', ascending=True)
print("\n")
print("RESULTADO COMPLETO DA QUESTÃO 5 — ANÁLISE DE CALENDÁRIO (LOJAS FÍSICAS - POS)")
print(")
print(f"{'Dia da Semana':15s} | {'Total Dias':10s} | {'Dias c/ Venda':13s} | {'Dias s/ Venda':13s} | {'Média Errada (Estagiário)':26s} | {'Média Correta (Sr. Almir)':25s}")
print("-" * 115)
for idx, row in summary.iterrows():
    print(f"{row['dia_semana']:15s} | {row['dias_totais_calendario']:10d} | {row['dias_com_venda']:13d} | {row['dias_sem_venda']:13d} | R$ {row['media_estagiario']:22.2f} | R$ {row['media_correta']:21.2f}")
worst = summary.iloc[0]
print("\n")
print(f"PIOR DIA DA SEMANA NAS LOJAS FÍSICAS (POS): {worst['dia_semana'].upper()}")
print(f"Média Real Diária (considerando dias sem venda): R$ {worst['media_correta']:.2f}")
print(f"Média Errada do Estagiário: R$ {worst['media_estagiario']:.2f}")
print(f"Diferença / Inflação no cálculo do Estagiário: R$ {worst['media_estagiario'] - worst['media_correta']:.2f}")
print("")
