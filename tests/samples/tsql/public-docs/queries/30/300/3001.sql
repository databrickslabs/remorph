-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/try-cast-transact-sql?view=sql-server-ver16

SET DATEFORMAT dmy;

SELECT TRY_CAST('12/31/2022' AS DATETIME2) AS Result;
GO