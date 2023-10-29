-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/select-for-clause-transact-sql?view=sql-server-ver16

SELECT tleft.c1   
FROM tleft   
RIGHT JOIN tright   
ON tleft.c1 = tright.c1   
WHERE tright.c1 <> 2 ;