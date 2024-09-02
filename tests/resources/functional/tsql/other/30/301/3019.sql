--Query type: DDL
CREATE PROCEDURE prc_gm30
AS
BEGIN
    WITH t43 AS (
        SELECT * FROM (VALUES (1, '2022-01-01', 'Customer1'), (2, '2022-01-02', 'Customer2')) AS t43 (KeyInt43, OrderDate, CustomerName)
    ),
    t44 AS (
        SELECT * FROM (VALUES (1, 'Product1'), (2, 'Product2')) AS t44 (KeyInt44, ProductName)
    )
    SELECT t43.KeyInt43, t43.OrderDate, t43.CustomerName, t44.ProductName
    FROM t43
    INNER JOIN t44 ON t44.KeyInt44 = t43.KeyInt43;
END;

-- Execute the procedure
EXEC prc_gm30;

-- REMORPH CLEANUP: DROP PROCEDURE prc_gm30;