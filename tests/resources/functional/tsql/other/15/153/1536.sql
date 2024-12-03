--Query type: DML
DECLARE @a DECIMAL(10,3) = 75.123, @b FLOAT(53) = 75.123;
WITH result_set AS (
    SELECT @a * @b AS result
)
SELECT * FROM result_set
