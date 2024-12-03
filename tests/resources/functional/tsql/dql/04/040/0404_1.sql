--Query type: DQL
WITH idx AS (
    SELECT 1 AS data_space_id, 'Index1' AS idx_name, 'CLUSTERED' AS idx_type, 1 AS obj_id
),
fg AS (
    SELECT 1 AS data_space_id, 'Filegroup1' AS fg_name
),
tbl AS (
    SELECT 1 AS obj_id, 'Table1' AS tbl_name
)
SELECT
    tbl.tbl_name AS [TableName],
    idx.idx_name AS [IndexName],
    idx.idx_type,
    idx.data_space_id,
    fg.fg_name AS [FilegroupName]
FROM
    idx
    JOIN fg ON idx.data_space_id = fg.data_space_id
    JOIN tbl ON idx.obj_id = tbl.obj_id
WHERE
    idx.obj_id = OBJECT_ID(N'Sales.Region', 'U');
