-- tsql sql:
WITH temp_result AS (
    SELECT 'column1' AS column_name, 'type1' AS data_type
    UNION ALL
    SELECT 'column2', 'type2'
)
SELECT STUFF(
    CONVERT(nvarchar(max), (
        SELECT ', ' + column_name + ' ' + data_type
        FROM temp_result
        FOR XML PATH('')
    )), 1, 2, ''
) AS COLUMNS;
