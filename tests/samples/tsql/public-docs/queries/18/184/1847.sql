-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/unicode-transact-sql?view=sql-server-ver16

DECLARE @nstring NCHAR(12);  
SET @nstring = N'Åkergatan 24';  
SELECT UNICODE(@nstring), NCHAR(UNICODE(@nstring));