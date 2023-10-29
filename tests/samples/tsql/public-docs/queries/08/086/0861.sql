-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-asymmetric-key-transact-sql?view=sql-server-ver16

CREATE ASYMMETRIC KEY EKM_askey1   
    FROM PROVIDER EKM_Provider1  
    WITH   
        ALGORITHM = RSA_2048,   
        CREATION_DISPOSITION = CREATE_NEW  
        , PROVIDER_KEY_NAME  = 'key10_user1' ;  
GO