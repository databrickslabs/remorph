-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

SELECT TOP(1)
   SYSDATETIME() AS UnconvertedDateTime,
   CAST(SYSDATETIME() AS NVARCHAR(30)) AS UsingCast,
   CONVERT(NVARCHAR(30), SYSDATETIME(), 126) AS UsingConvertTo_ISO8601
FROM dbo.DimCustomer;