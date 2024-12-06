-- tsql sql:
WITH temp_result AS (
    SELECT '2022-01-01' AS date_string
)
SELECT TRY_PARSE(date_string AS datetime2 USING 'en-US') AS parsed_date
FROM temp_result;
