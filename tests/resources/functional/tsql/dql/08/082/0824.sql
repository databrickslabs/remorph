--Query type: DQL
SELECT d1.ID AS d1_ID, d1.Name, d2.ID AS d2_ID, d2.Value
FROM (
    SELECT *
    FROM (
        VALUES (1, 'a'), (2, 'b')
    ) AS d1 (ID, Name)
) d1
FULL OUTER JOIN (
    SELECT *
    FROM (
        VALUES (1, 'x'), (3, 'y')
    ) AS d2 (ID, Value)
) d2
    ON d1.ID = d2.ID
ORDER BY d1.ID;