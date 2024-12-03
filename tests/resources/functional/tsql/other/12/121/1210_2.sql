--Query type: DML
INSERT INTO MyTest3 (myKey, myValue)
SELECT myKey, myValue
FROM (
    VALUES (2, 0), (3, 1), (4, 2)
) AS MyValues(myKey, myValue);
