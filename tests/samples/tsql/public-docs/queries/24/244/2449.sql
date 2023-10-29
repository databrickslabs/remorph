-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/precision-scale-and-length-transact-sql?view=sql-server-ver16

SELECT CAST(0.0000009000 AS DECIMAL(30, 10)) * CAST(1.0000000000 AS DECIMAL(30, 10)) [decimal(38, 6)];