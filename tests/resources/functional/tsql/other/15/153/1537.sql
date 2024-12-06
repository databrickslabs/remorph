-- tsql sql:
DECLARE @a DECIMAL(10,2) = 75.123, @b FLOAT(53) = 75.123;
CREATE TABLE cte WITH (DISTRIBUTION = ROUND_ROBIN) AS
SELECT result
FROM (
VALUES (@a*@b)
) AS v(result);