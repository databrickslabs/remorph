-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/odbc-scalar-functions-transact-sql?view=sql-server-ver16

CREATE PROCEDURE dbo.ODBCprocedure  
(  
    @string_exp NVARCHAR(4000)  
)  
AS  
SELECT {fn OCTET_LENGTH( @string_exp )};