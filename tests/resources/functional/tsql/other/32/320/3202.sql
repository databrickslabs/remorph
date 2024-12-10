-- tsql sql:
CREATE PROCEDURE #uspUpdateEmployeeLogin
AS
BEGIN
    WITH orders AS (
        SELECT *
        FROM (
            VALUES (1, 1, 'O'),
                   (2, 2, 'O'),
                   (3, 3, 'O')
        ) AS orders(o_orderkey, o_custkey, o_orderstatus)
    ),
    lineitem AS (
        SELECT *
        FROM (
            VALUES (1, 10),
                   (2, 20),
                   (3, 30)
        ) AS lineitem(l_orderkey, l_quantity)
    )
    SELECT orders.o_orderkey,
           orders.o_custkey,
           orders.o_orderstatus,
           SUM(lineitem.l_quantity) AS TotalQuantity
    FROM orders
    JOIN lineitem ON orders.o_orderkey = lineitem.l_orderkey
    WHERE orders.o_orderstatus = 'O'
    GROUP BY orders.o_orderkey,
             orders.o_custkey,
             orders.o_orderstatus
    HAVING SUM(lineitem.l_quantity) > 10
    ORDER BY SUM(lineitem.l_quantity) DESC;
END;
ADD SIGNATURE TO #uspUpdateEmployeeLogin BY CERTIFICATE HumanResourcesDP;
-- REMORPH CLEANUP: DROP PROCEDURE #uspUpdateEmployeeLogin;
-- REMORPH CLEANUP: DROP CERTIFICATE HumanResourcesDP;
