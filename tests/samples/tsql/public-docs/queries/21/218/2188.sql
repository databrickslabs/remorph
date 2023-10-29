-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/merge-transact-sql?view=sql-server-ver16

IF object_id('[check_table_1]', 'U') IS NOT NULL
    DROP TABLE [check_table_1]
GO

IF object_id('[check_table_2]', 'U') IS NOT NULL
    DROP TABLE [check_table_2]
GO

CREATE TABLE [check_table_1]
    WITH (DISTRIBUTION = ROUND_ROBIN) AS

SELECT <DISTRIBUTION_COLUMN> AS x
FROM <MERGE_TABLE>
GROUP BY <DISTRIBUTION_COLUMN>;
GO

CREATE TABLE [check_table_2]
    WITH (DISTRIBUTION = HASH (x)) AS

SELECT x
FROM [check_table_1];
GO

IF NOT EXISTS (
        SELECT TOP 1 *
        FROM (
            SELECT <DISTRIBUTION_COLUMN> AS x
            FROM <MERGE_TABLE>

            EXCEPT

            SELECT x
            FROM [check_table_2]
            ) AS tmp
        )
    SELECT 'no need for repair' AS result
ELSE
    SELECT 'needs repair' AS result
GO

IF object_id('[check_table_1]', 'U') IS NOT NULL
    DROP TABLE [check_table_1]
GO

IF object_id('[check_table_2]', 'U') IS NOT NULL
    DROP TABLE [check_table_2]
GO