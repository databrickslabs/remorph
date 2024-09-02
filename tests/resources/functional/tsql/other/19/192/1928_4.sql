--Query type: DML
WHILE (@@FETCH_STATUS <> -1)
BEGIN
    WITH LoopData AS (
        SELECT ID, Value
        FROM (
            VALUES (1, 10),
                   (2, 20),
                   (3, 30)
        ) AS LoopData (ID, Value)
    )
    SELECT ID, Value
    FROM LoopData;
END;