-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/subqueries-azure-sql-data-warehouse-parallel-data-warehouse?view=aps-pdw-2016-au7

SELECT * FROM RA   
    WHERE RA.a2 IN   
    (SELECT 1 FROM RB INNER JOIN RC ON RA.a1=RB.b1+RC.c1);