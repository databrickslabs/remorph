-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-route-transact-sql?view=sql-server-ver16

CREATE ROUTE ExpenseRoute  
    WITH  
    ADDRESS = 'TCP://dispatch.Adventure-Works.com' ;