-- tsql sql:
DECLARE @g GEOGRAPHY = 'POINT(32 23)';
DECLARE @speed FLOAT = 10.5;

SELECT *
FROM (
    VALUES (@g, @speed)
) AS temp (g, speed);
