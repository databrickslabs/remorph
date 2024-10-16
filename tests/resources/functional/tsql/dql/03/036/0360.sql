--Query type: DQL
DECLARE @altstartdate DATETIME;
SET @altstartdate = (
    SELECT date
    FROM (
        VALUES (
            CONVERT(DATETIME, 'January 10, 1900 3:00 AM', 101)
        )
    ) AS temp_result(date)
);
SELECT @altstartdate - 1.5 AS 'Subtract Date';