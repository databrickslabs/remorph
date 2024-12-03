--Query type: DQL
DECLARE @varname INT;
SET @varname = NULL;
WITH temp_result AS (
    SELECT c_custkey
    FROM customer
)
SELECT c_custkey
FROM temp_result
WHERE c_custkey = @varname;

SELECT c_custkey
FROM temp_result
WHERE c_custkey <> @varname;

SELECT c_custkey
FROM temp_result
WHERE c_custkey IS NULL;
