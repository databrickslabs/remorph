--Query type: DML
DECLARE @new_string VARCHAR(60);
SET @new_string = 'Four spaces are after the period in this sentence.    ';
SELECT @new_string + ' Next string.' AS original_string, RTRIM(@new_string) + ' Next string.' AS trimmed_string;
WITH cte AS (
    SELECT 'This is a string.' AS string
)
SELECT * FROM cte;