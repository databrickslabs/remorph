--Query type: DCL
DECLARE cursor1 CURSOR FOR
    WITH temp_result AS (
        SELECT 1 AS id, 'cursor1' AS name
        UNION ALL
        SELECT 2 AS id, 'cursor2' AS name
    )
    SELECT id, name
    FROM temp_result;

DEALLOCATE cursor1;
