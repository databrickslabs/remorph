--Query type: DCL
DECLARE @g1 datetime;
SELECT date AS date_value
FROM (
    VALUES (GETDATE())
) AS current_date_table(date);
