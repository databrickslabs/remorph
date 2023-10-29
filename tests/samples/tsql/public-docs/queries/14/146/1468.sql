-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/select-local-variable-transact-sql?view=sql-server-ver16

DECLARE @List AS nvarchar(max);
SELECT @List = STRING_AGG(p.LastName,', ') WITHIN GROUP (ORDER BY p.BusinessEntityID)
  FROM Person.Person AS p
  WHERE p.FirstName = 'William';
SELECT @List;