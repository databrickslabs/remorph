--Query type: DML
DECLARE @a DECIMAL(10, 3) = 75.123, @b FLOAT(53) = 90.789;
CREATE TABLE result2 (
    result2 DECIMAL(10, 3) NOT NULL
)
WITH (
    DISTRIBUTION = ROUND_ROBIN
);

WITH temp_result AS (
    SELECT @a + @b AS result
)
INSERT INTO result2
SELECT result
FROM temp_result;