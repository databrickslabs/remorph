-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-certificate-transact-sql?view=sql-server-ver16

CREATE CERTIFICATE Shipping04
    FROM FILE = 'c:\storedcerts\shipping04cert.pfx'
    WITH 
    FORMAT = 'PFX', 
	PRIVATE KEY (
        DECRYPTION BY PASSWORD = '9n34khUbhk$w4ecJH5gh'
	);