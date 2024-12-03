--Query type: Unknown
DECLARE @result INT;

BEGIN TRY
    WITH temp AS (
        SELECT 1 AS order_id, '2022-01-01' AS order_date
    )
    SELECT @result = CASE
        WHEN order_id = 1 THEN 123
        WHEN order_id = 2 THEN 4
        ELSE 99
    END
    FROM temp;

END TRY

BEGIN CATCH
    IF ERROR_NUMBER() = 1205 OR ERROR_NUMBER() = 1222 OR ERROR_NUMBER() = 1204
        SET @result = 123;
    ELSE IF ERROR_NUMBER() = 1206
        SET @result = 4;
    ELSE
        SET @result = 99;

END CATCH

SELECT @result AS result;
