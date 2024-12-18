-- tsql sql:
DECLARE @find VARCHAR(30);
SET @find = '%Special%';
SELECT T1.l_name, T1.c_name, T2.phone
FROM (
    VALUES ('Smith', 'Customer#000000001', '25-989-741-2988'),
         ('Jones', 'Customer#000000002', '25-989-741-2989')
) AS T1 (l_name, c_name, phone)
JOIN (
    VALUES ('Smith', '25-989-741-2988'),
         ('Jones', '25-989-741-2989')
) AS T2 (l_name, phone)
ON T1.l_name = T2.l_name
WHERE T1.c_name LIKE @find;
