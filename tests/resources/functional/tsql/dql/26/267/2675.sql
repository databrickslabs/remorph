--Query type: DQL
SELECT c_name, o_orderdate, o_totalprice
FROM (
    SELECT TOP(1) c_name, o_orderdate, o_totalprice
    FROM (
        VALUES ('Customer#000000001', '1996-01-02', 149.50),
               ('Customer#000000002', '1996-01-03', 249.50)
    ) AS c (c_name, o_orderdate, o_totalprice)
    WHERE o_orderdate = '1996-01-02'
    ORDER BY o_totalprice ASC
) AS a
UNION ALL
SELECT c_name, o_orderdate, o_totalprice
FROM (
    SELECT TOP(1) c_name, o_orderdate, o_totalprice
    FROM (
        VALUES ('Customer#000000003', '1996-01-04', 349.50),
               ('Customer#000000004', '1996-01-05', 449.50)
    ) AS c (c_name, o_orderdate, o_totalprice)
    WHERE o_orderdate = '1996-01-04'
    ORDER BY o_totalprice ASC
) AS b