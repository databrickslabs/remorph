--Query type: DML
SELECT Name AS MyName
FROM (
    VALUES (1, 'John'),
           (2, 'Jane')
) AS MyCTE (ID, Name)
WHERE ID = 1;
