-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/merge-transact-sql?view=sql-server-ver16

IF object_id('[repair_table_temp]', 'U') IS NOT NULL
    DROP TABLE [repair_table_temp];
GO

IF object_id('[repair_table]', 'U') IS NOT NULL
    DROP TABLE [repair_table];
GO

CREATE TABLE [repair_table_temp]
    WITH (DISTRIBUTION = ROUND_ROBIN) AS

SELECT *
FROM <MERGE_TABLE>;
GO

-- [repair_table] will hold the repaired table generated from <MERGE_TABLE>
CREATE TABLE [repair_table]
    WITH (DISTRIBUTION = HASH (<DISTRIBUTION_COLUMN>)) AS

SELECT *
FROM [repair_table_temp];
GO

IF object_id('[repair_table_temp]', 'U') IS NOT NULL
    DROP TABLE [repair_table_temp];
GO