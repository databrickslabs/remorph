-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-certificate-transact-sql?view=sql-server-ver16

CREATE CERTIFICATE Shipping19   
    FROM EXECUTABLE FILE = 'c:\Shipping\Certs\Shipping19.dll';  
GO