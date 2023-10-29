-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/create-database-transact-sql?view=sql-server-ver16

USE master;
GO
--Detach the AdventureWorks2022 database
sp_detach_db AdventureWorks2022;
GO
-- Physically move the full text catalog to the new location.
--Attach the AdventureWorks2022 database and specify the new location of the full-text catalog.
CREATE DATABASE AdventureWorks2022 ON
    (FILENAME = 'c:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\Data\AdventureWorks2022_data.mdf'),
    (FILENAME = 'c:\Program Files\Microsoft SQL Server\MSSQL13.MSSQLSERVER\MSSQL\Data\AdventureWorks2022_log.ldf'),
    (FILENAME = 'c:\myFTCatalogs\AdvWksFtCat')
FOR ATTACH;
GO