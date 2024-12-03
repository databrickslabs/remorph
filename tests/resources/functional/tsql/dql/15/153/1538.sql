--Query type: DQL
DECLARE @d date = '2050-04-04';
SELECT 'Input', @d
FROM (
    VALUES (1)
) AS x(a);

SELECT 'Truncated', DATETRUNC(day, @d)
FROM (
    VALUES (1)
) AS x(a);
