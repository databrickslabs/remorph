-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-remote-service-binding-transact-sql?view=sql-server-ver16

CREATE REMOTE SERVICE BINDING APBinding  
    TO SERVICE '//Adventure-Works.com/services/AccountsPayable'  
    WITH USER = APUser ;