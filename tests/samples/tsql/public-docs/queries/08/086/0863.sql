-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-asymmetric-key-transact-sql?view=sql-server-ver16

CREATE ASYMMETRIC KEY PacificSales19  
    AUTHORIZATION Christina  
    FROM FILE = 'c:\PacSales\Managers\ChristinaCerts.tmp';  
GO