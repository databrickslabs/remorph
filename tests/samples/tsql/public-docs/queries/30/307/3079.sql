-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/at-time-zone-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

DECLARE @ASOF DATETIMEOFFSET;

SET @ASOF = DATEADD(month, -1, GETDATE()) AT TIME ZONE 'UTC';

-- Query state of the table a month ago projecting period
-- columns as Pacific Standard Time
SELECT BusinessEntityID,
    PersonType,
    NameStyle,
    Title,
    FirstName,
    MiddleName,
    ValidFrom AT TIME ZONE 'Pacific Standard Time'
FROM Person.Person_Temporal
FOR SYSTEM_TIME AS OF @ASOF;