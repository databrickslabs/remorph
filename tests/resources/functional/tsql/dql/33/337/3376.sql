-- tsql sql:
SELECT RTRIM(c_last) + ',' + SPACE(2) + LTRIM(c_first) AS customer_name
FROM (
    VALUES ('Smith', 'John'),
           ('Johnson', 'Mary')
) AS customers (c_last, c_first)
ORDER BY c_last, c_first;
