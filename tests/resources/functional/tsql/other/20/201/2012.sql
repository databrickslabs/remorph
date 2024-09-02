--Query type: DDL
WITH SalesCTE AS (
    SELECT s_suppkey, s_name, SUM(l_extendedprice * (1 - l_discount)) AS total_revenue
    FROM (
        VALUES (1, 'Supplier#000000001', 100.0, 0.1),
               (2, 'Supplier#000000002', 200.0, 0.2),
               (3, 'Supplier#000000003', 300.0, 0.3)
    ) AS t(s_suppkey, s_name, l_extendedprice, l_discount)
    GROUP BY s_suppkey, s_name
),
RankedSales AS (
    SELECT s_suppkey, s_name, total_revenue, RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
    FROM SalesCTE
)
SELECT rs.s_suppkey, rs.s_name, rs.total_revenue, rs.revenue_rank, subquery.report_title
FROM RankedSales rs
CROSS JOIN (
    SELECT 'Top Suppliers' AS report_title
) AS subquery
WHERE rs.revenue_rank <= 2
GROUP BY rs.s_suppkey, rs.s_name, rs.total_revenue, rs.revenue_rank, subquery.report_title
HAVING rs.total_revenue > (SELECT AVG(total_revenue) FROM SalesCTE)