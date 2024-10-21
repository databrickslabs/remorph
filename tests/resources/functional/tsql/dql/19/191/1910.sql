--Query type: DQL
DECLARE @y NVARCHAR(4) = 'ef' + NCHAR(0x10002);
WITH temp_result AS (
    SELECT @y AS temp_column
)
SELECT CAST(temp_column AS NVARCHAR(3)) AS result_column
FROM temp_result;