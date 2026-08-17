# ⚓ RELATÓRIO EXECUTIVO & PACOTE DE ENTREGAS: DESAFIO LH NAUTICAL

**Empresa**: LH Nautical Retail (Dados 2020 – 2026)  
**Autor**: Analista de IA Sênior  
**Destinatários**: Gabriel Santos (Tech Lead), Marina Costa (Gerente de Negócios), Sr. Almir (Fundador)  

---

## 📁 1. Índice do Pacote de Arquivos Gerados no Diretório

Todos os arquivos abaixo foram gerados, validados e estão disponíveis para submissão direta na pasta do projeto:

| Nome do Arquivo | Tipo / Formato | Descrição & Função no Projeto |
| :--- | :---: | :--- |
| [`LH_Nautical_Master_Solutions.py`](file:///c:/Users/stama/OneDrive/Documentos/Trabalho/LH_Nautical_Master_Solutions.py) | **Python 3 Script / Notebook** | Código mestre completo e comentado que resolve end-to-end as 7 questões do desafio com 100% de reproducibilidade. |
| [`schema.sql`](file:///c:/Users/stama/OneDrive/Documentos/Trabalho/schema.sql) | **SQL DDL** | Script DDL PostgreSQL para criação automática das 24 tabelas com inferência dinâmica de tipos (Python Standard Library puro). |
| [`schema_generator.py`](file:///c:/Users/stama/OneDrive/Documentos/Trabalho/schema_generator.py) | **Python 3 Script** | Gerador automático de schema DDL PostgreSQL sem dependências externas (conforme exigido na Questão 2). |
| [`data_loader.py`](file:///c:/Users/stama/OneDrive/Documentos/Trabalho/data_loader.py) | **Python 3 Script** | Ingestor em batch via PostgreSQL `COPY` nativo que carrega todos os 24 CSVs mantendo 100% dos dados brutos (Questão 3). |
| [`export_powerbi_files.py`](file:///c:/Users/stama/OneDrive/Documentos/Trabalho/export_powerbi_files.py) | **Python 3 Script** | Exportador de dados consolidados e otimizados para rápida importação e modelagem no Power BI. |
| [`power_bi_exports/`](file:///c:/Users/stama/OneDrive/Documentos/Trabalho/power_bi_exports) | **Pasta de CSVs** | Contém os CSVs sumarizados: `bi_q4_top10_elite_customers.csv`, `bi_q5_calendar_pos_sales.csv`, `bi_q6_demand_forecast_bussola.csv`, `bi_q7_recommendations_motor_1949.csv`. |

---

## 📊 2. Resumo Executivo das Respostas Oficializadas

### 📌 Questão 1 — EDA (`orders`)
* **Linhas**: 48.998 | **Colunas**: 13
* **Intervalo de Datas**: `01/01/2020 01:19:28` a `31/12/2026 23:43:09`
* **Valores em `total`**: Mínimo R\$ 32,62 | Máximo R\$ 127.262,02 | Média R\$ 28.704,99
* **Diagnóstico**: Tabela confiável quanto aos totais (0 nulos em `total`), mas exige tratamento prévio para filtrar pedidos cancelados/estornados e imputar vendedor nulo (E-commerce).

### 📌 Questão 2 & 3 — Schema & Carregamento PostgreSQL
* **Schema DDL**: Arquivo `schema.sql` gerado 100% em Python 3 Standard Library com inferência de `INTEGER`, `BIGINT`, `NUMERIC(15,2)`, `TIMESTAMP`, `DATE` e `VARCHAR`.
* **Carga Bruta**: Script `data_loader.py` utilizando o comando nativo `COPY` do PostgreSQL para carga ultra-rápida sem remover nulos ou alterar caracteres acentuados.

### 📌 Questão 4 — Análise de Clientes de Elite
* **Top 1 Cliente de Elite**: `customer_id = 22` (Ticket Médio: R\$ 41.839,94 | Faturamento Total: R\$ 1.087.838,44 | 14 categorias distintas).
* **Categoria Líder de Vendas na Elite**: **Hélices** (`category_id = 8`) com **492 unidades compradas**.

### 📌 Questão 5 — Dimensão de Calendário & Pior Dia nas Lojas Físicas
* **Pior Dia da Semana**: **Quinta-feira** (Média Real: **R\$ 157.154,32 / dia**, considerando 20 quintas-feiras com R\$ 0 em vendas).
* **Correção do Erro do Estagiário**: O estagiário ignorou os dias sem venda e inflou a média de quinta-feira para R\$ 166.238,38 (+ R\$ 9.084,06 / dia de erro).

### 📌 Questão 6 — Previsão de Demanda (Bússola de Bordo 702)
* **Previsões Q1 2026 (Média Móvel 3 Meses)**: Jan/2026 = 38,67 un (Real: 79 un) | Fev/2026 = 53,67 un (Real: 68 un) | Mar/2026 = 56,33 un (Real: 60 un).
* **Erro MAE**: **19,44 unidades/mês** (ou 16,44 un para o ID 74 isolado).
* **Adequação do Baseline**: **NÃO é adequado**. Por ser um modelo linear simples, ele é cego à sazonalidade de pico de Verão náutico, subestimando as vendas de janeiro e gerando risco grave de ruptura de estoque (*stockout*).

### 📌 Questão 7 — Sistema de Recomendação (Motor de Popa 1949)
* **Matriz de Interação**: $2.000$ Clientes $\times$ $500$ Produtos (Binária).
* **Top 5 Recomendações (Similaridade de Cosseno)**:
  1. 🥇 **Motor de Popa 5331** (Similaridade: 0,2566 | 106 co-compras)
  2. 🥈 **Cabo Náutico 2105** (Similaridade: 0,2562 | 103 co-compras)
  3. 🥉 **Vela Mestra 1913** (Similaridade: 0,2558 | 100 co-compras)
  4. 🏅 **Cabo Náutico 9048** (Similaridade: 0,2393 | 99 co-compras)
  5. 🏅 **GPS Plotter 6249** (Similaridade: 0,2377 | 98 co-compras)

---

## 🎨 3. Arquitetura do Dashboard Obrigatório para o Power BI

Para garantir aprovação com nota máxima e encantar o **Sr. Almir** e a **Marina Costa**, o dashboard deve ser montado em 3 páginas dinâmicas:

### Page 1: Executive Overview & Loss Mitigation (Visão Sr. Almir)
* **KPI Cards**: Faturamento Total (R\$ 1,4 BI), Ticket Médio Geral (R\$ 28,7k), Total de Pedidos (48.998).
* **Visual 1 (Questão 5)**: Gráfico de Colunas Comparativo da Venda Média Diária por Dia da Semana (POS) evidenciando **Quinta-feira** com marcador de alerta.
* **Filtros Slicers**: Canal (POS / E-commerce), Ano (2020 - 2026), Categoria.

### Page 2: Client Intelligence & Category Deep Dive (Visão Marina Costa)
* **Visual 2 (Questão 4)**: Gráfico de Barras com o Ranking dos Top 10 Clientes de Elite (Filtro $\ge 13$ categorias).
* **Visual 3**: Matriz/Treemap das categorias de produtos mais consumidas pelos clientes VIP (Destaque para **Hélices** com 492 unidades).
* **Tabela Detalhada**: Matriz RFM de Clientes com LTV e contagem de categorias.

### Page 3: Predictive Engine & Smart Recommendations (Visão Gabriel Santos)
* **Visual 4 (Questão 6)**: Gráfico de Linha Duplo (Vendas Reais vs. Previsão Média Móvel) com área sombreada do MAE de 19,44 un no Q1/2026.
* **Visual 5 (Questão 7)**: Card Interativo de Cross-Sell mostrando os 5 Produtos recomendados para o **Motor de Popa 1949** com barra de índice de similaridade de cosseno.

---

### 🚀 Instrução de Envio
Você pode zipar ou anexar diretamente os arquivos da pasta `power_bi_exports/`, o arquivo `schema.sql`, o script `data_loader.py` e o notebook `LH_Nautical_Master_Solutions.py` no espaço de envio da plataforma!
