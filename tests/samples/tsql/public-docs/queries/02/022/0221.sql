-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/string-concatenation-transact-sql?view=sql-server-ver16

-- Uses AdventureWorks  
  
SELECT (LastName + ', ' + SUBSTRING(FirstName, 1, 1) + '.') AS Name, Title  
FROM DimEmployee  
WHERE Title LIKE '%Vice Pres%'  
ORDER BY LastName ASC;