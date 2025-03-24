WITH column_info AS (
    SELECT
        TABLE_CATALOG,
        TABLE_SCHEMA,
        TABLE_NAME,
        STRING_AGG(
                CONCAT(
                        column_name,
                        '§',
                        CASE
                            WHEN numeric_precision IS NOT NULL AND numeric_scale IS NOT NULL THEN CONCAT(data_type, '(', numeric_precision, ',', numeric_scale, ')')
                            WHEN LOWER(data_type) = 'text' THEN CONCAT('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')
                            ELSE data_type
                            END,
                        '§',
                        CASE
                            WHEN cis.IS_NULLABLE = 'YES' THEN 'true'
                            ELSE 'false'
                            END,
                        '§',
                        ISNULL(CAST(ep_col.value AS NVARCHAR(MAX)), '')
                ),
                '‡'
        ) WITHIN GROUP (ORDER BY ordinal_position) AS DERIVED_SCHEMA
FROM
    sys.tables t
    INNER JOIN sys.columns c ON t.object_id = c.object_id
    INNER JOIN INFORMATION_SCHEMA.COLUMNS cis ON t.name = cis.TABLE_NAME AND c.name = cis.COLUMN_NAME
    OUTER APPLY (
    SELECT TOP 1 value
    FROM sys.extended_properties
    WHERE major_id = t.object_id AND minor_id = 0
    ORDER BY name DESC
    ) ep_tbl
    OUTER APPLY (
    SELECT TOP 1 value
    FROM sys.extended_properties
    WHERE major_id = c.object_id AND minor_id = c.column_id
    ORDER BY name DESC
    ) ep_col
GROUP BY
    TABLE_CATALOG,
    TABLE_SCHEMA,
    TABLE_NAME
    ),
    table_file_info AS (
SELECT
    s.name AS TABLE_SCHEMA,
    t.name AS TABLE_NAME,
    f.physical_name AS location,
    f.type_desc AS TABLE_FORMAT,
    CAST(ROUND(SUM(a.used_pages) * 8.0 / 1024, 2) AS DECIMAL(18, 2)) AS SIZE_GB
FROM
    sys.tables t
    INNER JOIN sys.indexes i ON t.object_id = i.object_id
    INNER JOIN sys.partitions p ON i.object_id = p.object_id AND i.index_id = p.index_id
    INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
    INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
    INNER JOIN sys.database_files f ON a.data_space_id = f.data_space_id
    LEFT JOIN sys.extended_properties ep ON ep.major_id = t.object_id AND ep.minor_id = 0
GROUP BY
    s.name,
    t.name,
    f.name,
    f.physical_name,
    f.type_desc
    ),
    table_comment_info AS (
SELECT
    s.name AS TABLE_SCHEMA,
    t.name AS TABLE_NAME,
    CAST(ep.value AS NVARCHAR(MAX)) AS TABLE_COMMENT
FROM
    sys.tables t
    INNER JOIN sys.schemas s ON t.schema_id = s.schema_id
    OUTER APPLY (
    SELECT TOP 1 value
    FROM sys.extended_properties
    WHERE major_id = t.object_id AND minor_id = 0
    ORDER BY name DESC
    ) ep
    ),
    table_pk_info AS (
SELECT
    TC.TABLE_CATALOG,
    TC.TABLE_SCHEMA,
    TC.TABLE_NAME,
    STRING_AGG(KU.COLUMN_NAME,':') as PK_COLUMN_NAME
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC
    JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KU
ON TC.CONSTRAINT_NAME = KU.CONSTRAINT_NAME
    AND TC.TABLE_NAME = KU.TABLE_NAME
WHERE TC.CONSTRAINT_TYPE = 'PRIMARY KEY' group by TC.TABLE_CATALOG, TC.TABLE_SCHEMA, TC.TABLE_NAME)
SELECT
    sft.TABLE_CATALOG,
    sft.TABLE_SCHEMA,
    sft.TABLE_NAME,
    tfi.location,
    tfi.TABLE_FORMAT,
    '' as view_definition,
    column_info.DERIVED_SCHEMA,
    tfi.SIZE_GB,
    tci.TABLE_COMMENT,
    tpK.PK_COLUMN_NAME
FROM
    column_info
        JOIN INFORMATION_SCHEMA.TABLES sft ON column_info.TABLE_CATALOG = sft.TABLE_CATALOG AND column_info.TABLE_SCHEMA = sft.TABLE_SCHEMA AND column_info.TABLE_NAME = sft.TABLE_NAME
    LEFT JOIN table_file_info tfi ON column_info.TABLE_SCHEMA = tfi.TABLE_SCHEMA AND column_info.TABLE_NAME = tfi.TABLE_NAME
    LEFT JOIN table_comment_info tci ON column_info.TABLE_SCHEMA = tci.TABLE_SCHEMA AND column_info.TABLE_NAME = tci.TABLE_NAME
    LEFT JOIN table_pk_info tpK ON column_info.TABLE_SCHEMA = tpK.TABLE_SCHEMA AND column_info.TABLE_NAME = tpK.TABLE_NAME


UNION ALL
SELECT
    sfv.TABLE_CATALOG,
    sfv.TABLE_SCHEMA,
    sfv.TABLE_NAME,
    '' location,
    '' TABLE_FORMAT,
    sfv.view_definition,
    '' DERIVED_SCHEMA,
    0 SIZE_GB,
    '' TABLE_COMMENT,
    '' PK_COLUMN_NAME
FROM INFORMATION_SCHEMA.VIEWS sfv