--Query type: DQL
DECLARE @description VARCHAR(64);
SELECT @description = 'Regular bicycles are designed' + ' for riding on paved roads.';
WITH temp_result AS (
    SELECT 'Regular bicycles are designed' + ' for riding on paved roads.' AS description
)
SELECT CHARINDEX('riding', description, 5) AS [index]
FROM temp_result;
