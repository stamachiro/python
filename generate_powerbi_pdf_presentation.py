"""
LH Nautical - Power BI PDF Presentation Generator (Removed 'Sr. Almir' references)
Author: Senior AI Analyst
Description: Re-architects presentation slides with 100% neutral executive wording
             (removed all occurrences of 'Sr. Almir').
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

# Global Font Settings
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

out_dir = r"c:\Users\stama\OneDrive\Documentos\Trabalho"
inc_dir = r"c:\Users\stama\OneDrive\Documentos\Trabalho\incidium"

pdf_filename = os.path.join(out_dir, "LH_Nautical_PowerBI_Executive_Presentation.pdf")
inc_pdf_filename = os.path.join(inc_dir, "LH_Nautical_PowerBI_Executive_Presentation.pdf")

# Data definitions
weekday_data = {
    'Dia': ['Quinta-feira', 'Domingo', 'Segunda-feira', 'Sábado', 'Terça-feira', 'Sexta-feira', 'Quarta-feira'],
    'Media_Correta': [157154.32, 157616.13, 158241.15, 164858.27, 166118.83, 170193.68, 173605.44],
    'Media_Estagiario': [166238.38, 162974.19, 161335.26, 169980.98, 169841.38, 174987.87, 178481.99]
}
df_q5 = pd.DataFrame(weekday_data)

top10_customers = {
    'Customer_ID': ['Cliente #22', 'Cliente #1477', 'Cliente #929', 'Cliente #1116', 'Cliente #1691', 'Cliente #774', 'Cliente #1470', 'Cliente #1599', 'Cliente #965', 'Cliente #1722'],
    'Ticket_Medio': [41839.94, 41648.30, 41645.23, 40983.58, 40773.57, 40340.44, 40021.27, 39904.66, 39841.05, 39532.94]
}
df_q4_cust = pd.DataFrame(top10_customers)

top_categories = {
    'Categoria': ['Hélices', 'Coletes Salva-Vidas', 'Eletrônica Náutica', 'Âncoras', 'Iluminação'],
    'Quantidade': [492, 393, 392, 387, 333]
}
df_q4_cat = pd.DataFrame(top_categories)

q6_data = {
    'Mes': ['Out/25', 'Nov/25', 'Dez/25', 'Jan/26', 'Fev/26', 'Mar/26'],
    'Vendas_Reais': [34, 60, 22, 79, 68, 60],
    'Previsao_MA3': [None, None, None, 38.67, 53.67, 56.33]
}
df_q6 = pd.DataFrame(q6_data)

q7_recs = {
    'Rank': ['1º', '2º', '3º', '4º', '5º'],
    'Produto_Recomendado': ['Motor de Popa 5331', 'Cabo Náutico 2105', 'Vela Mestra 1913', 'Cabo Náutico 9048', 'GPS Plotter 6249'],
    'Similaridade': ['0.2566', '0.2562', '0.2558', '0.2393', '0.2377'],
    'Co_Compras': ['106 clientes', '103 clientes', '100 clientes', '99 clientes', '98 clientes']
}
df_q7 = pd.DataFrame(q7_recs)

# Colors
navy_header = '#0A1128'
bg_white = '#FFFFFF'
card_bg = '#FFFFFF'
frame_blue_bg = '#F0F6FF'
frame_blue_border = '#2563EB'
text_dark = '#0F172A'

# Color Palettes
accent_blue = '#1D4ED8'
accent_orange = '#F97316'
warning_red = '#EF4444'        # Quinta-feira is RED
success_green = '#10B981'

# Slide 3 Palette: Distinct shades of blue for each category
slide3_blue_shades = ['#1E3A8A', '#2563EB', '#0284C7', '#06B6D4', '#38BDF8']

# Slide 4 Palette: Rainbow colors for weekdays (Quinta-feira strictly RED)
rainbow_weekdays_map = {
    'Quinta-feira': '#EF4444',   # Red (Maintained!)
    'Domingo': '#F97316',        # Orange
    'Segunda-feira': '#F59E0B',   # Yellow/Amber
    'Sábado': '#10B981',         # Green
    'Terça-feira': '#06B6D4',     # Cyan
    'Sexta-feira': '#2563EB',     # Blue
    'Quarta-feira': '#8B5CF6'     # Violet/Purple
}

def apply_header_gradient_layout(fig, slide_title, page_str):
    bg_ax = fig.add_axes([0, 0, 1, 1], facecolor=bg_white)
    bg_ax.axis('off')
    
    # Outer Blue Frame (Leaves ~1cm page border)
    frame_ax = fig.add_axes([0.03, 0.03, 0.94, 0.86], facecolor=frame_blue_bg)
    frame_ax.axis('off')
    frame_patch = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.01", ec=frame_blue_border, fc=frame_blue_bg, lw=1.5)
    frame_ax.add_patch(frame_patch)
    
    # Header bar with blue gradient (Top 9% height)
    header_ax = fig.add_axes([0, 0.91, 1, 0.09])
    header_ax.axis('off')
    
    gradient = np.linspace(0, 1, 256).reshape(1, 256)
    cmap = plt.cm.colors.LinearSegmentedColormap.from_list("header_grad", ["#0B192C", "#1E3A8A", "#2563EB"])
    header_ax.imshow(gradient, aspect='auto', cmap=cmap, extent=[0, 1, 0, 1])
    
    header_ax.text(0.04, 0.55, "Desafio Lighthouse - Dados & AI", color='white', fontsize=12, fontweight='bold', va='center')
    header_ax.text(0.38, 0.55, f"|   {slide_title}", color='#93C5FD', fontsize=11, fontweight='bold', va='center')
    header_ax.text(0.96, 0.55, page_str, color='#CBD5E1', fontsize=9.5, fontweight='bold', ha='right', va='center')

def create_kpi_card(fig, rect, title, value, subtitle="", color=text_dark, border_color='#CBD5E1'):
    ax = fig.add_axes(rect, facecolor=card_bg)
    ax.axis('off')
    rect_patch = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02", ec=border_color, fc=card_bg, lw=1.2)
    ax.add_patch(rect_patch)
    ax.text(0.08, 0.70, title.upper(), fontsize=7.2, color='#64748B', fontweight='bold')
    ax.text(0.08, 0.38, value, fontsize=12, color=color, fontweight='bold')
    if subtitle:
        ax.text(0.08, 0.16, subtitle, fontsize=6.8, color='#94A3B8')

image_files = []

# ===================================================================================
# SLIDE 1: VISÃO GERAL EXECUTIVA & KPIS GLOBAIS
# ===================================================================================
fig1 = plt.figure(figsize=(12, 6.75), dpi=200)
apply_header_gradient_layout(fig1, "Visão Geral Executiva & KPIs", "Página 1 de 6")

ax_overview = fig1.add_axes([0.05, 0.63, 0.90, 0.22], facecolor=card_bg)
ax_overview.axis('off')
rect_patch = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02", ec='#2563EB', fc=card_bg, lw=1.2)
ax_overview.add_patch(rect_patch)

ax_overview.text(0.03, 0.80, "RESUMO EXECUTIVO DO PROJETO - LH NAUTICAL", fontsize=9.5, fontweight='bold', color=accent_blue)

overview_text = (
    "• Análise do ciclo completo de varejo náutico cobrindo o período de 2020 a 2026.\n"
    "• Estruturação de pipeline relacional em PostgreSQL para 24 tabelas com carga bruta.\n"
    "• Identificação da carteira de Clientes de Elite (Ticket Médio de R$ 40.000+ em 13+ categorias).\n"
    "• Correção do cálculo de faturamento com Dimensão de Calendário contínua (2.557 dias).\n"
    "• Diagnóstico de Previsão de Demanda e Motor de Recomendação por Similaridade de Cosseno."
)
ax_overview.text(0.03, 0.10, overview_text, fontsize=8.0, color='#334155', va='bottom', multialignment='left')

create_kpi_card(fig1, [0.05, 0.36, 0.43, 0.22], "Faturamento Bruto (2020-2026)", "R$ 1.406.487.210,00", "Total acumulado de 48.998 pedidos", color=navy_header)
create_kpi_card(fig1, [0.52, 0.36, 0.43, 0.22], "Ticket Médio Geral", "R$ 28.704,99", "Média por transação registrada", color=navy_header)

create_kpi_card(fig1, [0.05, 0.08, 0.43, 0.22], "Pior Dia nas Lojas Físicas", "QUINTA-FEIRA", "R$ 157.154,32 / dia real", color=warning_red, border_color=warning_red)
create_kpi_card(fig1, [0.52, 0.08, 0.43, 0.22], "Impacto dos Dias Ignorados", "+ R$ 9.084,06 / dia", "Média inflada (ignorou 20 dias R$ 0)", color=warning_red, border_color=warning_red)

p1_path = os.path.join(out_dir, "p1.png")
fig1.savefig(p1_path, dpi=200)
plt.close(fig1)
image_files.append(p1_path)

# ===================================================================================
# SLIDE 2: QUESTÃO 4 - RANKING DOS CLIENTES DE ELITE
# ===================================================================================
fig2 = plt.figure(figsize=(12, 6.75), dpi=200)
apply_header_gradient_layout(fig2, "Questão 4 - Ranking dos Clientes de Elite", "Página 2 de 6")

create_kpi_card(fig2, [0.05, 0.76, 0.43, 0.11], "Clientes Diversificados (≥ 13 setores)", "1.971 Clientes", "98,5% da base de clientes ativos", color=navy_header)
create_kpi_card(fig2, [0.52, 0.76, 0.43, 0.11], "Top 1 Ticket Médio Elite", "R$ 41.839,94", "Cliente ID #22 (Faturamento R$ 1,08 MI)", color=accent_orange)

ax_card2 = fig2.add_axes([0.05, 0.06, 0.90, 0.66], facecolor=card_bg)
ax_card2.axis('off')
rect_patch = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02", ec='#CBD5E1', fc=card_bg, lw=1)
ax_card2.add_patch(rect_patch)

ax2 = fig2.add_axes([0.17, 0.12, 0.73, 0.52], facecolor=card_bg)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#CBD5E1')
ax2.spines['bottom'].set_color('#CBD5E1')

bars2 = ax2.barh(df_q4_cust['Customer_ID'], df_q4_cust['Ticket_Medio'], color=accent_blue, height=0.48)
ax2.invert_yaxis()
ax2.set_xlabel("Ticket Médio (R$)", fontsize=8.2, fontweight='bold', color='#475569')
ax2.set_title("Ranking dos Top 10 Clientes de Elite por Ticket Médio (Diversidade ≥ 13 Categorias)", fontsize=9.5, fontweight='bold', color=navy_header, pad=8)
ax2.set_xlim(0, 54000)
ax2.xaxis.set_major_formatter('R$ {x:,.0f}')

for bar in bars2:
    w = bar.get_width()
    ax2.text(w + 500, bar.get_y() + bar.get_height()/2, f"R$ {w:,.2f}", va='center', fontsize=7.5, fontweight='bold', color='#1E293B')

p2_path = os.path.join(out_dir, "p2.png")
fig2.savefig(p2_path, dpi=200)
plt.close(fig2)
image_files.append(p2_path)

# ===================================================================================
# SLIDE 3: QUESTÃO 4 - CONCENTRAÇÃO DE CATEGORIAS
# ===================================================================================
fig3 = plt.figure(figsize=(12, 6.75), dpi=200)
apply_header_gradient_layout(fig3, "Questão 4 - Produtos Mais Comprados pela Elite", "Página 3 de 6")

create_kpi_card(fig3, [0.05, 0.76, 0.43, 0.11], "Categoria Campeã de Vendas na Elite", "HÉLICES (492 unidades)", "Setor líder absoluto de consumo", color=slide3_blue_shades[0], border_color=slide3_blue_shades[0])
create_kpi_card(fig3, [0.52, 0.76, 0.43, 0.11], "2º Lugar de Vendas na Elite", "COLETES SALVA-VIDAS (393 un)", "Equipamentos de segurança essenciais", color=slide3_blue_shades[1])

ax_card3 = fig3.add_axes([0.05, 0.06, 0.90, 0.66], facecolor=card_bg)
ax_card3.axis('off')
rect_patch = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02", ec='#CBD5E1', fc=card_bg, lw=1)
ax_card3.add_patch(rect_patch)

ax3 = fig3.add_axes([0.14, 0.14, 0.76, 0.50], facecolor=card_bg)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['left'].set_color('#CBD5E1')
ax3.spines['bottom'].set_color('#CBD5E1')

bars3 = ax3.bar(df_q4_cat['Categoria'], df_q4_cat['Quantidade'], color=slide3_blue_shades, width=0.45)
ax3.set_ylabel("Quantidade Total Comprada (Unidades)", fontsize=8.5, fontweight='bold', color='#475569')
ax3.set_title("Volume de Itens Comprados pelos 10 Clientes de Elite por Categoria", fontsize=10, fontweight='bold', color=navy_header, pad=8)
ax3.set_ylim(0, 560)
plt.setp(ax3.get_xticklabels(), fontsize=8.5, fontweight='bold')

for bar in bars3:
    h = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, h + 10, f"{int(h)} un", ha='center', fontsize=8.5, fontweight='bold', color='#1E293B')

p3_path = os.path.join(out_dir, "p3.png")
fig3.savefig(p3_path, dpi=200)
plt.close(fig3)
image_files.append(p3_path)

# ===================================================================================
# SLIDE 4: QUESTÃO 5 - LOJAS FÍSICAS (NO 'SR. ALMIR' REFERENCE)
# ===================================================================================
fig4 = plt.figure(figsize=(12, 6.75), dpi=200)
apply_header_gradient_layout(fig4, "Questão 5 - Vendas POS & Impacto dos Dias Ignorados", "Página 4 de 6")

# 1. Top Diagnostic Box (Height: 0.18)
ax_text4 = fig4.add_axes([0.05, 0.69, 0.90, 0.18], facecolor=card_bg)
ax_text4.axis('off')
rect_patch = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02", ec='#2563EB', fc=card_bg, lw=1.2)
ax_text4.add_patch(rect_patch)

ax_text4.text(0.03, 0.84, "DIAGNÓSTICO DE CALENDÁRIO - IMPACTO DOS DIAS IGNORADOS (POS)", fontsize=9.0, fontweight='bold', color=accent_blue)

# Neutral executive wording without 'Sr. Almir'
p4_spacious_text = (
    "• PERÍODO ANALISADO: 01/01/2020 a 31/12/2026 (2.557 dias no calendário contínuo).\n"
    "• IMPACTO DOS DIAS IGNORADOS: Ignorou 20 quintas-feiras com venda R$ 0,00.\n"
    "  Média Real de Vendas: R$ 157.154,32 / dia   |   Média sem os Zeros: R$ 166.238,38 / dia (+R$ 9.084,06/dia)."
)
ax_text4.text(0.03, 0.65, p4_spacious_text, fontsize=7.6, color='#334155', va='top', multialignment='left')

# 2. Middle Chart Card Box (Height: 0.44)
ax_card4 = fig4.add_axes([0.05, 0.22, 0.90, 0.44], facecolor=card_bg)
ax_card4.axis('off')
rect_patch = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02", ec='#CBD5E1', fc=card_bg, lw=1)
ax_card4.add_patch(rect_patch)

# Reduced Chart Height inside Chart Card
ax1 = fig4.add_axes([0.18, 0.26, 0.72, 0.36], facecolor=card_bg)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('#CBD5E1')
ax1.spines['bottom'].set_color('#CBD5E1')

y_pos = np.arange(len(df_q5['Dia']))
rainbow_bar_colors = [rainbow_weekdays_map[d] for d in df_q5['Dia']]

bars1 = ax1.barh(y_pos, df_q5['Media_Correta'], color=rainbow_bar_colors, height=0.46)

ax1.set_yticks(y_pos)
ax1.set_yticklabels(df_q5['Dia'], fontsize=7.2, fontweight='bold', color='#334155')
ax1.invert_yaxis()
ax1.set_xlabel("Venda Média Diária Real (R$)", fontsize=7.8, fontweight='bold', color='#475569')
ax1.set_title("Média Diária de Vendas por Dia da Semana (POS - Com Dias Sem Venda)", fontsize=8.8, fontweight='bold', color=navy_header, pad=6)
ax1.set_xlim(0, 240000)

for bar in bars1:
    w = bar.get_width()
    ax1.text(w + 2500, bar.get_y() + bar.get_height()/2, f"R$ {w:,.2f}", va='center', fontsize=7.0, fontweight='bold', color='#1E293B')

# 3. Dedicated White Frame Card at Bottom for Recommendation (Neutral Title)
ax_rec_box4 = fig4.add_axes([0.05, 0.05, 0.90, 0.14], facecolor=card_bg)
ax_rec_box4.axis('off')
rect_patch = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02", ec=success_green, fc=card_bg, lw=1.5)
ax_rec_box4.add_patch(rect_patch)

ax_rec_box4.text(0.03, 0.72, "RECOMENDAÇÃO OPERACIONAL E DE GESTÃO DA DIRETORIA", fontsize=8.8, fontweight='bold', color=success_green)
rec_card_text = (
    "• A Quinta-feira apresenta a pior média real de vendas das lojas físicas (R$ 157.154,32 / dia).\n"
    "• Recomendação: É o dia ideal para realizar manutenção preventiva, balanço de estoque e folga programada da equipe."
)
ax_rec_box4.text(0.03, 0.40, rec_card_text, fontsize=7.6, color='#1E293B', va='top', multialignment='left')

p4_path = os.path.join(out_dir, "p4.png")
fig4.savefig(p4_path, dpi=200)
plt.close(fig4)
image_files.append(p4_path)

# ===================================================================================
# SLIDE 5: QUESTÃO 6 - PREVISÃO DE DEMANDA (BÚSSOLA DE BORDO 702)
# ===================================================================================
fig5 = plt.figure(figsize=(12, 6.75), dpi=200)
apply_header_gradient_layout(fig5, "Questão 6 - Previsão de Demanda (Bússola 702)", "Página 5 de 6")

create_kpi_card(fig5, [0.05, 0.76, 0.28, 0.11], "Modelo Baseline Treinado", "MÉDIA MÓVEL 3M", "Método sequencial deslizante", color=navy_header)
create_kpi_card(fig5, [0.36, 0.76, 0.28, 0.11], "Erro Preditivo MAE (Q1 2026)", "19,44 Unidades/Mês", "Erro médio absoluto acumulado", color=warning_red, border_color=warning_red)
create_kpi_card(fig5, [0.66, 0.76, 0.28, 0.11], "Soma Previsão Q1 2026", "149 Unidades", "Previsão total de 3 meses", color=accent_orange)

ax_card5 = fig5.add_axes([0.05, 0.06, 0.90, 0.66], facecolor=card_bg)
ax_card5.axis('off')
rect_patch = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02", ec='#CBD5E1', fc=card_bg, lw=1)
ax_card5.add_patch(rect_patch)

ax4 = fig5.add_axes([0.14, 0.14, 0.76, 0.50], facecolor=card_bg)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

ax4.plot(df_q6['Mes'], df_q6['Vendas_Reais'], marker='o', color=navy_header, linewidth=2.2, label='Vendas Reais (y)')
ax4.plot(df_q6['Mes'], df_q6['Previsao_MA3'], marker='s', linestyle='--', color=warning_red, linewidth=2.2, label='Previsão Média Móvel (ŷ)')

ax4.set_title("Série Temporal de Vendas Reais vs Previsão Média Móvel (Bússola de Bordo 702)", fontsize=10, fontweight='bold', color=navy_header, pad=8)
ax4.set_ylabel("Quantidade de Unidades Vendidas", fontsize=8.5, fontweight='bold', color='#475569')
ax4.legend(loc='upper left', fontsize=8)
ax4.grid(axis='y', linestyle=':', alpha=0.6)
ax4.set_ylim(0, 95)

ax4.annotate('Gap do Verão:\nReal = 79 un vs Previsão = 38,67 un\n(Erro Absoluto = 40,33 un)', xy=(3, 79), xytext=(2.2, 83),
             arrowprops=dict(facecolor=warning_red, shrink=0.05, width=1.2, headwidth=6),
             fontsize=7.8, fontweight='bold', color=warning_red)

p5_path = os.path.join(out_dir, "p5.png")
fig5.savefig(p5_path, dpi=200)
plt.close(fig5)
image_files.append(p5_path)

# ===================================================================================
# SLIDE 6: QUESTÃO 7 - MOTOR DE RECOMENDAÇÃO (REMOVED ID PRODUTO COLUMN)
# ===================================================================================
fig6 = plt.figure(figsize=(12, 6.75), dpi=200)
apply_header_gradient_layout(fig6, "Questão 7 - Motor de Recomendação Cosseno", "Página 6 de 6")

create_kpi_card(fig6, [0.05, 0.76, 0.43, 0.11], "Matriz Usuário x Produto", "2.000 x 500 Matriz Binária", "Interação de presença/ausência", color=navy_header)
create_kpi_card(fig6, [0.52, 0.76, 0.43, 0.11], "Produto Recomendado nº 1", "Motor de Popa 5331 (ID #389)", "Similaridade de Cosseno: 0.2566", color=accent_orange)

ax_rec = fig6.add_axes([0.05, 0.06, 0.90, 0.66], facecolor=card_bg)
ax_rec.axis('off')
rect_patch = patches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02", ec='#CBD5E1', fc=card_bg, lw=1)
ax_rec.add_patch(rect_patch)

ax_rec.text(0.04, 0.91, "RANKING DE SIMILARIDADE DE COSSENO PARA 'MOTOR DE POPA 1949' (ID #180)", fontsize=10, fontweight='bold', color=navy_header)

headers_rec = ["Rank", "Produto Recomendado", "Similaridade Cosseno", "Volume de Co-compras"]
col_x = [0.05, 0.18, 0.58, 0.80]
y_start = 0.78

for idx, h in enumerate(headers_rec):
    ax_rec.text(col_x[idx], y_start, h, fontsize=8.8, fontweight='bold', color='#334155')

ax_rec.plot([0.04, 0.96], [y_start - 0.03, y_start - 0.03], color='#CBD5E1', lw=1)

y_row = y_start - 0.11
for _, row in df_q7.iterrows():
    ax_rec.text(col_x[0], y_row, row['Rank'], fontsize=9.0, fontweight='bold', color=accent_orange)
    ax_rec.text(col_x[1], y_row, row['Produto_Recomendado'], fontsize=9.0, color='#1E293B', fontweight='bold')
    ax_rec.text(col_x[2], y_row, row['Similaridade'], fontsize=9.0, fontweight='bold', color=navy_header)
    ax_rec.text(col_x[3], y_row, row['Co_Compras'], fontsize=8.5, color='#475569')
    y_row -= 0.11

ax_rec.text(0.04, 0.08, "• Recomendação E-commerce: Exibir cabos náuticos e GPS como itens complementares de compra.", fontsize=8.0, color=success_green, fontweight='bold')

p6_path = os.path.join(out_dir, "p6.png")
fig6.savefig(p6_path, dpi=200)
plt.close(fig6)
image_files.append(p6_path)

# ===================================================================================
# COMPILE IMAGES INTO MULTI-PAGE PDF
# ===================================================================================
images = [Image.open(f).convert("RGB") for f in image_files]
images[0].save(pdf_filename, save_all=True, append_images=images[1:])
images[0].save(inc_pdf_filename, save_all=True, append_images=images[1:])

print(f"[SUCCESS] PDF with zero references to 'Sr. Almir' generated perfectly!")
print(f"  └─ File 1: {pdf_filename}")
print(f"  └─ File 2: {inc_pdf_filename}")
