--Query type: DDL
CREATE PROCEDURE usp_GetOrderLevel
AS
SELECT o_orderkey, o_custkey, 0 AS [Order Level]
FROM (
    VALUES (1, 10),
           (2, 20),
           (3, 30)
) AS Orders (o_orderkey, o_custkey);

SELECT *
FROM (
    VALUES (1, 10),
           (2, 20),
           (3, 30)
) AS Orders (o_orderkey, o_custkey);
-- REMORPH CLEANUP: DROP PROCEDURE usp_GetOrderLevel;