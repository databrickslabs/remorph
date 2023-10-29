-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/json-value-transact-sql?view=sql-server-ver16

SELECT FirstName, LastName,
 JSON_VALUE(jsonInfo,'$.info.address.town') AS Town
FROM Person.Person
WHERE JSON_VALUE(jsonInfo,'$.info.address.state') LIKE 'US%'
ORDER BY JSON_VALUE(jsonInfo,'$.info.address.town')