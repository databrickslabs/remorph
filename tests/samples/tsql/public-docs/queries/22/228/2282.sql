-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/try-cast-transact-sql?view=sql-server-ver16

SELECT
CASE WHEN TRY_CAST('test' AS FLOAT) IS NULL
     THEN 'Cast failed'
     ELSE 'Cast succeeded'
END AS Result;
GO