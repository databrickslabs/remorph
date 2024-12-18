-- tsql sql:
SELECT *
FROM (
    VALUES
        (1, 'John'),
        (2, 'Jane'),
        (3, 'Bob')
) AS temp_data (ID, Name)
ORDER BY ID;
