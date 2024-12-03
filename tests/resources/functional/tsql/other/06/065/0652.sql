--Query type: DML
INSERT INTO orders (o_orderkey, o_custkey, o_orderstatus)
SELECT *
FROM (
    VALUES (1, 1, 'O'),
           (2, 2, 'O'),
           (3, 3, NULL)
) AS temp (o_orderkey, o_custkey, o_orderstatus);
