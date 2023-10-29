-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

SELECT '2006-04-25T15:50:59.997' AS UnconvertedText,
    CAST('2006-04-25T15:50:59.997' AS DATETIME) AS UsingCast,
    CONVERT(DATETIME, '2006-04-25T15:50:59.997', 126) AS UsingConvertFrom_ISO8601;
GO