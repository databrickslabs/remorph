-- see https://learn.microsoft.com/en-us/sql/t-sql/database-console-commands/dbcc-cleantable-transact-sql?view=sql-server-ver16

USE AdventureWorks2022;
GO

IF OBJECT_ID('dbo.CleanTableTest', 'U') IS NOT NULL
    DROP TABLE dbo.CleanTableTest;
GO

CREATE TABLE dbo.CleanTableTest (
    FileName NVARCHAR(4000)
    , DocumentSummary NVARCHAR(max)
    , Document VARBINARY(max)
    );
GO

-- Populate the table with data from the Production.Document table.
INSERT INTO dbo.CleanTableTest
SELECT REPLICATE(FileName, 1000), DocumentSummary, Document
FROM Production.Document;
GO

-- Verify the current page counts and average space used in the dbo.CleanTableTest table.
DECLARE @db_id SMALLINT;
DECLARE @object_id INT;

SET @db_id = DB_ID(N'AdventureWorks2022');
SET @object_id = OBJECT_ID(N'AdventureWorks2022.dbo.CleanTableTest');

SELECT alloc_unit_type_desc
    , page_count
    , avg_page_space_used_in_percent
    , record_count
FROM sys.dm_db_index_physical_stats(@db_id, @object_id, NULL, NULL, 'Detailed');
GO

-- Drop two variable-length columns from the table.
ALTER TABLE dbo.CleanTableTest

DROP COLUMN FileName, Document;
GO

-- Verify the page counts and average space used in the dbo.CleanTableTest table
-- Notice that the values have not changed.
DECLARE @db_id SMALLINT;
DECLARE @object_id INT;

SET @db_id = DB_ID(N'AdventureWorks2022');
SET @object_id = OBJECT_ID(N'AdventureWorks2022.dbo.CleanTableTest');

SELECT alloc_unit_type_desc
    , page_count
    , avg_page_space_used_in_percent
    , record_count
FROM sys.dm_db_index_physical_stats(@db_id, @object_id, NULL, NULL, 'Detailed');
GO

-- Run DBCC CLEANTABLE.
DBCC CLEANTABLE (AdventureWorks2022, 'dbo.CleanTableTest');
GO

-- Verify the values in the dbo.CleanTableTest table after the DBCC CLEANTABLE command.
DECLARE @db_id SMALLINT;
DECLARE @object_id INT;

SET @db_id = DB_ID(N'AdventureWorks2022');
SET @object_id = OBJECT_ID(N'AdventureWorks2022.dbo.CleanTableTest');

SELECT alloc_unit_type_desc
    , page_count
    , avg_page_space_used_in_percent
    , record_count
FROM sys.dm_db_index_physical_stats(@db_id, @object_id, NULL, NULL, 'Detailed');
GO