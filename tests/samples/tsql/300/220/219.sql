-- Uses AdventureWorks  
  
SELECT FirstName, LastName, MiddleName  
FROM DIMEmployee  
WHERE MiddleName IS NOT NULL  
ORDER BY LastName DESC;