-- tsql sql:
CREATE TABLE check_table_2
WITH (DISTRIBUTION = ROUND_ROBIN)
AS
SELECT c_custkey AS x
FROM (
    VALUES (1, 'Customer#000000001'),
           (2, 'Customer#000000002'),
           (3, 'Customer#000000003')
) AS customer (c_custkey, c_name)
GROUP BY c_custkey;
