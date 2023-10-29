-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/get-transmission-status-transact-sql?view=sql-server-ver16

SELECT Status =  
    GET_TRANSMISSION_STATUS('58ef1d2d-c405-42eb-a762-23ff320bddf0') ;