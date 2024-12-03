--Query type: DDL
CREATE TABLE #mylogintable (date_in DATETIME, user_id INT, myuser_name AS USER_NAME());
WITH mylogintable AS (
    SELECT CAST('2022-01-01' AS DATETIME) AS date_in, 1 AS user_id
    UNION ALL
    SELECT CAST('2022-01-02' AS DATETIME), 2
)
INSERT INTO #mylogintable (date_in, user_id)
SELECT date_in, user_id
FROM mylogintable;
SELECT * FROM #mylogintable
