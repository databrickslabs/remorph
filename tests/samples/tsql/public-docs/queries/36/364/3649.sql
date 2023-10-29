-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-database-transact-sql-compatibility-level?view=sql-server-ver16

WITH cte AS
    (SELECT * FROM (VALUES (1),(2),(3)) v (a)),
r AS
    (SELECT a FROM cte
    UNION ALL
    (SELECT a FROM cte EXCEPT SELECT a FROM r)
)
SELECT a
FROM r;
GO