-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-route-transact-sql?view=sql-server-ver16

CREATE ROUTE ExpenseRoute  
    WITH  
    SERVICE_NAME = '//Adventure-Works.com/Expenses',  
    LIFETIME = 259200,  
    ADDRESS = 'TCP://services.Adventure-Works.com:1234' ;