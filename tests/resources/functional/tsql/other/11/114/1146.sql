-- tsql sql:
CREATE SEQUENCE OrderSeq AS integer;
SELECT NEXT VALUE FOR OrderSeq AS OrderId
FROM (
    VALUES (1)
) AS TempTable(T);
