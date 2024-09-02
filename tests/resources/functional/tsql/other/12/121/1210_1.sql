--Query type: DML
INSERT INTO MyTest2 (myKey, myValue)
SELECT myKey, myValue
FROM (
    VALUES (1, 0),
           (2, 10),
           (3, 20)
) AS temp (myKey, myValue);