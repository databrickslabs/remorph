-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/string-comparison-assignment?view=sql-server-ver16

SELECT LastName,
    FirstName
FROM Person.Person
WHERE LastName = 'Johnson';