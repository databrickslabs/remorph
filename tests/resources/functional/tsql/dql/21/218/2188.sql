-- tsql sql:
WITH tmp AS (
    SELECT TOP 1 *
    FROM (
        SELECT o_orderkey AS x
        FROM (
            VALUES (1), (2), (3)
        ) AS orders(o_orderkey)
        EXCEPT
        SELECT o_orderkey
        FROM (
            VALUES (1), (2)
        ) AS order_items(o_orderkey)
    ) AS tmp
)
SELECT CASE WHEN EXISTS (SELECT * FROM tmp) THEN 'needs repair' ELSE 'no need for repair' END AS result;
