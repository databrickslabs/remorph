-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

SELECT TOP(1)
   '2010-07-25T13:50:38.544' AS UnconvertedText,
CAST('2010-07-25T13:50:38.544' AS DATETIME) AS UsingCast,
   CONVERT(DATETIME, '2010-07-25T13:50:38.544', 126) AS UsingConvertFrom_ISO8601
FROM dbo.DimCustomer;