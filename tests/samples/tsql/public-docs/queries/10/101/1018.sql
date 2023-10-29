-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/odbc-scalar-functions-transact-sql?view=sql-server-ver16

CREATE FUNCTION dbo.ODBCudf  
(  
    @string_exp NVARCHAR(4000)  
)  
RETURNS INT  
AS  
BEGIN  
DECLARE @len INT  
SET @len = (SELECT {fn OCTET_LENGTH( @string_exp )})  
RETURN(@len)  
END ;  
GO
SELECT dbo.ODBCudf('Returns the length.');  
--Returns 38