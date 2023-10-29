-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/declare-local-variable-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks

DECLARE @find VARCHAR(30);
/* Also allowed:
DECLARE @find VARCHAR(30) = 'Man%';
*/
SET @find = 'Walt%';

SELECT LastName, FirstName, Phone
FROM DimEmployee
WHERE LastName LIKE @find;