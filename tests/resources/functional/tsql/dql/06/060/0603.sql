--Query type: DQL
WITH columns AS (
    SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, NUMERIC_SCALE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'emp'
)
SELECT COLUMN_NAME,
    CASE DATA_TYPE
        WHEN 'bigint' THEN 'bigint'
        WHEN 'binary' THEN 'binary'
        WHEN 'bit' THEN 'bit'
        WHEN 'char' THEN 'char'
        WHEN 'date' THEN 'date'
        WHEN 'datetime' THEN 'datetime'
        WHEN 'datetime2' THEN 'datetime2'
        WHEN 'datetimeoffset' THEN 'datetimeoffset'
        WHEN 'decimal' THEN 'decimal'
        WHEN 'float' THEN 'float'
        WHEN 'geography' THEN 'geography'
        WHEN 'geometry' THEN 'geometry'
        WHEN 'hierarchyid' THEN 'hierarchyid'
        WHEN 'image' THEN 'image'
        WHEN 'int' THEN 'int'
        WHEN 'money' THEN 'money'
        WHEN 'nchar' THEN 'nchar'
        WHEN 'ntext' THEN 'ntext'
        WHEN 'numeric' THEN 'numeric'
        WHEN 'nvarchar' THEN 'nvarchar'
        WHEN 'real' THEN 'real'
        WHEN 'smalldatetime' THEN 'smalldatetime'
        WHEN 'smallint' THEN 'smallint'
        WHEN 'smallmoney' THEN 'smallmoney'
        WHEN 'sql_variant' THEN 'sql_variant'
        WHEN 'text' THEN 'text'
        WHEN 'time' THEN 'time'
        WHEN 'timestamp' THEN 'timestamp'
        WHEN 'tinyint' THEN 'tinyint'
        WHEN 'uniqueidentifier' THEN 'uniqueidentifier'
        WHEN 'varbinary' THEN 'varbinary'
        WHEN 'varchar' THEN 'varchar'
        ELSE 'unknown'
    END AS DATA_TYPE,
    CHARACTER_MAXIMUM_LENGTH,
    NUMERIC_PRECISION,
    NUMERIC_SCALE
FROM columns