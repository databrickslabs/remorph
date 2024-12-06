-- tsql sql:
SELECT COUNT(*) AS [Number of rows]
FROM (
    VALUES (1, 'Value1'),
           (2, 'Value2')
) AS #Test (
    Column1,
    Column2
);
