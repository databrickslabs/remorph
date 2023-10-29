-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/has-perms-by-name-transact-sql?view=sql-server-ver16

SELECT HAS_PERMS_BY_NAME('AdventureWorks2022.Sales.SalesPerson',   
    'OBJECT', 'INSERT');