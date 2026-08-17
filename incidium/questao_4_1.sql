WITH cliente_metricas AS (
    SELECT 
        o.customer_id,
        SUM(o.total) AS faturamento_total,
        COUNT(DISTINCT o.id) AS frequencia_pedidos,
        ROUND(SUM(o.total) / COUNT(DISTINCT o.id), 2) AS ticket_medio,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    JOIN order_items oi ON o.id = oi.order_id
    JOIN product_variants pv ON oi.product_variant_id = pv.id
    JOIN products p ON pv.product_id = p.id
    GROUP BY o.customer_id
    HAVING COUNT(DISTINCT p.category_id) >= 13
)
SELECT 
    customer_id,
    ticket_medio,
    faturamento_total,
    frequencia_pedidos,
    diversidade_categorias
FROM cliente_metricas
ORDER BY 
    ticket_medio DESC,
    customer_id ASC
LIMIT 10;
