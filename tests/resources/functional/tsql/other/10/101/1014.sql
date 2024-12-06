-- tsql sql:
CREATE PROCEDURE dbo.GetWeekNumber
    @DATE datetime
AS
BEGIN
    DECLARE @ISOweek int;

    WITH temp_result AS (
        SELECT DATEPART(wk, date) + 1 - DATEPART(wk, CAST(DATEPART(yy, date) AS CHAR(4)) + '0104') AS ISOweek
        FROM (
            VALUES (@DATE)
        ) AS temp_result(date)
    )
    SELECT @ISOweek = ISOweek
    FROM temp_result;

    IF (@ISOweek = 0)
        SET @ISOweek = 1;

    IF ((DATEPART(mm, @DATE) = 12) AND ((DATEPART(dd, @DATE) - DATEPART(dw, @DATE)) >= 28))
        SET @ISOweek = 1;

    SELECT @ISOweek AS WeekNumber;
END;
EXEC dbo.GetWeekNumber '2023-03-15';
-- REMORPH CLEANUP: DROP PROCEDURE dbo.GetWeekNumber;
