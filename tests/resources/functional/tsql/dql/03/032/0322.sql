--Query type: DQL
SELECT c.FirstName, c.LastName, s.Rate
FROM (
    VALUES (1, 'John', 'Doe'),
           (2, 'Jane', 'Doe'),
           (3, 'Bob', 'Smith')
) AS c (CustomerID, FirstName, LastName)
JOIN (
    VALUES (1, 25.0),
           (2, 30.0),
           (3, 35.0)
) AS s (CustomerID, Rate)
    ON c.CustomerID = s.CustomerID
WHERE s.Rate NOT BETWEEN 27 AND 30
ORDER BY s.Rate;
