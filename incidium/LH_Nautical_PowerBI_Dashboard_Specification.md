# 🎨 ESPECIFICAÇÃO & GUIA DE CONSTRUÇÃO DO DASHBOARD POWER BI

**Projeto**: LH Nautical Analytics Dashboard  
**Destino**: Material Complementar (Dashboard Obrigatório)  
**Autor**: Sergio Tamachiro

---

## 📐 1. Modelo Estrela (Star Schema) no Power BI

Para garantir performance máxima e tabelas limpas no Power BI, importe os CSVs gerados na pasta [`power_bi_exports/`](file:///c:/Users/stama/OneDrive/Documentos/Trabalho/power_bi_exports) ou os CSVs brutos originais conectados conforme o diagrama:

```
           +--------------------+
           |     dCalendario    |
           +--------------------+
                     | (1)
                     |
                     | (*)
           +--------------------+
           |      fVendas       |
           +--------------------+
           /         |          \
       (*) /     (*) |      (*)  \
          /          |            \
+-----------+  +-----------+  +------------+
| dCliente  |  | dProduto  |  | dCategoria |
+-----------+  +-----------+  +------------+
```

---

## 💻 2. Guia de Medidas DAX para Copiar e Colar

### Medida 1: Faturamento Total Líquido
```dax
Faturamento Total = 
SUM(fVendas[total])
```

### Medida 2: Ticket Médio Geral
```dax
Ticket Medio = 
DIVIDE([Faturamento Total], DISTINCTCOUNT(fVendas[id]), 0)
```

### Medida 3: Venda Média Diária por Dia da Semana (Com Dias Sem Venda — Questão 5)
```dax
Venda Media POS Com Zero = 
VAR _VendaPOS = CALCULATE(SUM(fVendas[total]), fVendas[channel] = "pos")
VAR _TotalDiasNaData = COUNTROWS(dCalendario)
RETURN
DIVIDE(_VendaPOS, _TotalDiasNaData, 0)
```

### Medida 4: Ticket Médio do Cliente de Elite (Questão 4)
```dax
Ticket Medio Cliente Elite = 
CALCULATE(
    [Ticket Medio],
    FILTER(
        dCliente,
        [Diversidade Categorias Cliente] >= 13
    )
)
```

### Medida 5: Diversidade de Categorias por Cliente (Questão 4)
```dax
Diversidade Categorias Cliente = 
CALCULATE(
    DISTINCTCOUNT(dProduto[category_id]),
    CROSSFILTER(fVendas[product_id], dProduto[product_id], Both)
)
```

---

## 🎨 3. Design System & Guia Visual

* **Paleta de Cores Náutica Premium**:
  * **Azul Marinho Principal (Navy)**: `#0B192C` (Fundo de headers e cards principais)
  * **Azul Oceano (Ocean Accent)**: `#1E3E62` (Barras de gráficos e destaques)
  * **Dourado/Bronze Náutico (Gold Accent)**: `#FF6B00` ou `#D4AF37` (KPIs de Elite e Campeões)
  * **Vermelho de Alerta (Warning Red)**: `#E74C3C` (Marcadores de perdas e pior dia da semana - Quinta-feira)
  * **Fundo das Telas**: `#F8F9FA` (Cinza claro limpo)

---

## 🖥️ 4. Estrutura das Páginas do Dashboard

### 📄 Tela 1: Resumo Executivo & Calendário de Vendas (Atendendo ao Sr. Almir)
1. **Header**: Logo LH Nautical + Título "Painel de Inteligência Comercial e Desempenho de Lojas Físicas".
2. **Cards Superiores**: Faturamento Acumulado | Ticket Médio | Total de Pedidos | Pior Dia da Semana (Quinta-feira).
3. **Gráfico Central (Questão 5)**: Gráfico de Colunas mostrando a Média Diária Real de Vendas por Dia da Semana (POS), com destaque vermelho na **Quinta-feira** (R\$ 157.154,32) e anotação explicando o erro do estagiário.

### 📄 Tela 2: Inteligência de Clientes de Elite & Produtos (Atendendo a Marina Costa)
1. **Cards Superiores**: Clientes VIP ($\ge 13$ Categorias) | Ticket Médio da Elite (R\$ 40,5k) | Categoria Campeã (Hélices).
2. **Gráfico 1 (Questão 4)**: Ranking dos Top 10 Clientes de Elite (Barras horizontais ordenadas por Ticket Médio com desempate por ID).
3. **Gráfico 2**: Treemap/Matriz das categorias mais compradas pelos clientes VIP (Destaque para **Hélices** com 492 itens).

### 📄 Tela 3: Motores Preditivos & Cross-Selling (Atendendo ao Gabriel Santos)
1. **Gráfico 1 (Questão 6)**: Gráfico de Linha Dupla comparando Vendas Reais vs. Previsão da Média Móvel de 3 Meses no Q1 2026 para a **Bússola de Bordo 702** (MAE = 19,44 un).
2. **Painel de Recomendação (Questão 7)**: Tabela/Cards interativos do Motor de Recomendação listando os Top 5 produtos recomendados para o **Motor de Popa 1949** baseados na Similaridade de Cosseno.
