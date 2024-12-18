-- tsql sql:
WITH daily_storage AS (
    SELECT r_name AS region, n_name AS nation, SUM(o_totalprice) AS total_price, SUM(ps_supplycost * ps_availqty) AS total_storage
    FROM (
        VALUES ('USA', 'USA', '1995-01-01', 100.0, 1000.0, 1.0),
               ('Canada', 'Canada', '1996-01-01', 200.0, 2000.0, 1.0),
               ('Mexico', 'Mexico', '1997-01-01', 300.0, 3000.0, 1.0)
    ) AS ps (r_name, n_name, o_orderdate, o_totalprice, ps_supplycost, ps_availqty)
    WHERE o_orderdate BETWEEN '1995-01-01' AND '1998-12-31'
    GROUP BY r_name, n_name
)
SELECT region, nation, total_price, total_storage
FROM daily_storage
ORDER BY total_storage DESC;
