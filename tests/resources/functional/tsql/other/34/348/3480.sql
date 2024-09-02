--Query type: DDL
WITH temp_result AS (
    SELECT s.supplierkey, s.name AS supplier_name, n.name AS nation_name
    FROM (
        VALUES (1, 'Supplier1', 'USA'),
               (2, 'Supplier2', 'Canada')
    ) s(supplierkey, name, nationkey)
    INNER JOIN (
        VALUES (1, 'USA'),
               (2, 'Canada')
    ) n(nationkey, name) ON s.nationkey = n.nationkey
),
     total_revenue AS (
    SELECT l.supplierkey, SUM(l.extendedprice * (1 - l.discount)) AS revenue
    FROM (
        VALUES (1, 100, 0.1),
               (2, 200, 0.2)
    ) l(supplierkey, extendedprice, discount)
    GROUP BY l.supplierkey
)
SELECT tr.supplierkey, tr.supplier_name, tr.nation_name, tr.revenue, ROW_NUMBER() OVER (ORDER BY tr.revenue DESC) AS row_num
FROM (
    SELECT tr.supplierkey, tr.supplier_name, tr.nation_name, tr2.revenue
    FROM temp_result tr
    INNER JOIN total_revenue tr2 ON tr.supplierkey = tr2.supplierkey
    WHERE tr.nation_name = 'USA' AND tr2.revenue > (
        SELECT AVG(revenue)
        FROM (
            VALUES (1000000.0),
                   (2000000.0)
        ) AS avg_revenue(revenue)
    )
) tr
ORDER BY tr.revenue DESC;