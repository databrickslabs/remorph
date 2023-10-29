-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/asymkeyproperty-transact-sql?view=sql-server-ver16

SELECT   
ASYMKEYPROPERTY(256, 'algorithm_desc') AS Algorithm,  
ASYMKEYPROPERTY(256, 'string_sid') AS String_SID,  
ASYMKEYPROPERTY(256, 'sid') AS SID ;  
GO