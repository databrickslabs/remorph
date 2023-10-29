-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/grouping-id-transact-sql?view=sql-server-ver16

SELECT GROUPING_ID(A,B)  
FROM T   
GROUP BY CUBE(A,B)