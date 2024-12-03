--Query type: DML
INSERT INTO orders (o_orderkey, o_custkey, o_orderstatus)
VALUES
    (1, 10, 'O'),
    (1, 10, 'O'),
    (1, 10, 'O'),
    (1, 20, 'P'),
    (1, 21, 'F'),
    (1, 10, 'O');
