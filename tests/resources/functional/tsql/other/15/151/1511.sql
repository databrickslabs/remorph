--Query type: DML
DECLARE @addvalue INT;
SET @addvalue = 20;
SELECT id, value + @addvalue AS new_value
FROM (
    VALUES (1, '100'),
           (2, '200'),
           (3, '300')
) AS result (id, value);
