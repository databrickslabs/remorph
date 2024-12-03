--Query type: DML
DECLARE @v2 VARCHAR(80);

WITH temp_result AS (
    SELECT 'This is the original.' AS original_text
)

SELECT @v2 = original_text FROM temp_result;

SET @v2 += ' More text.';

PRINT @v2;

-- REMORPH CLEANUP: None
