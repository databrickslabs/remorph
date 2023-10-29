-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/backup-certificate-transact-sql?view=sql-server-ver16

BACKUP CERTIFICATE Shipping04 TO FILE = 'c:\storedcerts\shipping04cert.pfx'
WITH  
    FORMAT = 'PFX',  
    PRIVATE KEY ( 
ENCRYPTION BY PASSWORD = '9n34khUbhk$w4ecJH5gh',  
ALGORITHM = 'AES_256'
    )