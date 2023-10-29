-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/like-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks
  
SELECT FirstName,
    LastName,
    Phone
FROM DimEmployee
WHERE phone NOT LIKE '612%'
ORDER BY LastName;