-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/merge-transact-sql?view=sql-server-ver16

-- Case 1
SELECT a.name,
    c.distribution_policy_desc,
    b.type
FROM sys.tables a
INNER JOIN sys.indexes b
    ON a.object_id = b.object_id
INNER JOIN sys.pdw_table_distribution_properties c
    ON a.object_id = c.object_id
WHERE b.type = 2
    AND c.distribution_policy_desc = 'HASH';

-- Subject to Case 2, if distribution key value is updated in MERGE statement
SELECT a.name,
    c.distribution_policy_desc
FROM sys.tables a
INNER JOIN sys.pdw_table_distribution_properties c
    ON a.object_id = c.object_id
WHERE c.distribution_policy_desc = 'HASH';