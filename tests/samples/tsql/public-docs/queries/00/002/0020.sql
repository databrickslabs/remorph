-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-index-transact-sql?view=sql-server-ver16

-- Create a database
CREATE DATABASE [ columnstore ];
GO

-- Create a rowstore staging table
CREATE TABLE [ staging ] (
     AccountKey              int NOT NULL,
     AccountDescription      nvarchar (50),
     AccountType             nvarchar(50),
     AccountCodeAlternateKey     int
     )

-- Insert 10 million rows into the staging table.
DECLARE @loop int
DECLARE @AccountDescription varchar(50)
DECLARE @AccountKey int
DECLARE @AccountType varchar(50)
DECLARE @AccountCode int

SELECT @loop = 0
BEGIN TRAN
    WHILE (@loop < 300000)
      BEGIN
        SELECT @AccountKey = CAST (RAND()*10000000 as int);
        SELECT @AccountDescription = 'accountdesc ' + CONVERT(varchar(20), @AccountKey);
        SELECT @AccountType = 'AccountType ' + CONVERT(varchar(20), @AccountKey);
        SELECT @AccountCode =  CAST (RAND()*10000000 as int);

        INSERT INTO  staging VALUES (@AccountKey, @AccountDescription, @AccountType, @AccountCode);

        SELECT @loop = @loop + 1;
    END
COMMIT

-- Create a table for the clustered columnstore index

CREATE TABLE cci_target (
     AccountKey              int NOT NULL,
     AccountDescription      nvarchar (50),
     AccountType             nvarchar(50),
     AccountCodeAlternateKey int
     )

-- Convert the table to a clustered columnstore index named inxcci_cci_target;
CREATE CLUSTERED COLUMNSTORE INDEX idxcci_cci_target ON cci_target;