--Query type: DQL
DECLARE @var FLOAT = 10;
WITH temp AS (
    SELECT @var AS var
)
SELECT 'The LOG of the variable is: ' + CONVERT(VARCHAR, LOG(var))
FROM temp;