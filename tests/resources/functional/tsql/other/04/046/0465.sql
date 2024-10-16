--Query type: DML
SET DATEFORMAT mdy;
WITH dates AS (
    SELECT '15/04/2008' AS date_str
    UNION ALL
    SELECT '15/2008/04'
    UNION ALL
    SELECT '2008/15/04'
    UNION ALL
    SELECT '2008/04/15'
)
SELECT ISDATE(date_str) AS is_valid_date
FROM dates;