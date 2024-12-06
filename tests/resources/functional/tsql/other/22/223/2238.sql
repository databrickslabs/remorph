-- tsql sql:
DECLARE @trancount INT;
SET @trancount = @@TRANCOUNT;
PRINT @trancount;
WITH temp_result AS (
    SELECT @trancount AS trancount
)
SELECT * FROM temp_result;
