-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/select-local-variable-transact-sql?view=sql-server-ver16

DECLARE @List AS nvarchar(max);
SELECT @List = CONCAT(COALESCE(@List + ', ',''), p.LastName)
  FROM Person.Person AS p
  WHERE p.FirstName = 'William'
  ORDER BY p.BusinessEntityID;
SELECT @List;