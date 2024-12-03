--Query type: DDL
SELECT col2, col3, col4, col5
FROM (
    VALUES ('value1', 'value2', 10, 20.5),
           ('value3', 'value4', 30, 40.5)
) AS mynewtable (col2, col3, col4, col5)
WHERE col4 > 15 AND col3 > 20
ORDER BY col2, col3, col4, col5;
