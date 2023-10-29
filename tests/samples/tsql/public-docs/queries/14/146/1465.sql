-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/string-comparison-assignment?view=sql-server-ver16

DECLARE @LNameBin BINARY (100) = 0x5A68656E67;

SELECT LastName,
    FirstName
FROM Person.Person
WHERE LastName = CONVERT(VARCHAR, @LNameBin);