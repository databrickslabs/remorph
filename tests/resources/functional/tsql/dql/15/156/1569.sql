--Query type: DQL
DECLARE @datetime DATETIME = '2016-10-23 12:45:37.333';
DECLARE @datetime2 DATETIME2 = @datetime;

WITH temp_result AS (
    SELECT @datetime2 AS [@datetime2], @datetime AS [@datetime]
)
SELECT * FROM temp_result;
