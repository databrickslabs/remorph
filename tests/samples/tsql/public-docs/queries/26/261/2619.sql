-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/cast-and-convert-transact-sql?view=sql-server-ver16

SELECT GETDATE() AS UnconvertedDateTime,
    CAST(GETDATE() AS NVARCHAR(30)) AS UsingCast,
    CONVERT(NVARCHAR(30), GETDATE(), 126) AS UsingConvertTo_ISO8601;
GO