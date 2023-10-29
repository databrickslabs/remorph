-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/logical-functions-choose-transact-sql?view=sql-server-ver16

SELECT Name, ModifiedDate, 
CHOOSE(MONTH(ModifiedDate),'Winter','Winter', 'Spring','Spring','Spring','Summer','Summer',   
                          'Summer','Autumn','Autumn','Autumn','Winter') AS Quarter_Modified
FROM SalesLT.ProductModel AS PM
WHERE Name LIKE '%Frame%'
ORDER BY ModifiedDate;