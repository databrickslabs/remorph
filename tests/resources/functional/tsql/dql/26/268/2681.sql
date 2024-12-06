-- tsql sql:
SELECT NEXT VALUE FOR OrderSequence AS NextOrderID
FROM (
    VALUES (1), (2), (3)
) AS TempTable (ID);
