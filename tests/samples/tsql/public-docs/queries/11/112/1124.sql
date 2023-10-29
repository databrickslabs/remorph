-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-route-transact-sql?view=sql-server-ver16

CREATE ROUTE LogRequests  
    WITH  
    SERVICE_NAME = '//Adventure-Works.com/LogRequests',  
    ADDRESS = 'LOCAL' ;