-- tsql sql:
SET LANGUAGE French;
WITH CurrentDate AS (
    SELECT @@DATEFIRST AS DateFirst
)
SELECT DateFirst
FROM CurrentDate;
