-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/subqueries-azure-sql-data-warehouse-parallel-data-warehouse?view=aps-pdw-2016-au7

SELECT * FROM RA   
    WHERE 3 = (SELECT COUNT(*)   
        FROM (SELECT b1 FROM RB WHERE RB.b1 = RA.a1) X);