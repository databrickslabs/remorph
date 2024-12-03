--Query type: DML
INSERT INTO orders (o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment)
VALUES
    (1, 1, 'O', 100.00, '1992-01-01', '1-URGENT', 'Clerk#000000001', 0, 'O comment'),
    (2, 2, 'O', 200.00, '1992-01-02', '2-HIGH', 'Clerk#000000002', 0, 'O comment'),
    (3, 3, 'O', 300.00, '1992-01-03', '3-MEDIUM', 'Clerk#000000003', 0, 'O comment'),
    (4, 4, 'O', 400.00, '1992-01-04', '4-NOT SPECIFIED', 'Clerk#000000004', 0, 'O comment'),
    (5, 5, 'O', 500.00, '1992-01-05', '5-LOW', 'Clerk#000000005', 0, 'O comment');

INSERT INTO customers (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment)
VALUES
    (1, 'Customer#000000001', 'Address#000000001', 1, 'Phone#000000001', 100.00, 'BUILDING', 'C comment'),
    (2, 'Customer#000000002', 'Address#000000002', 2, 'Phone#000000002', 200.00, 'AUTOMOBILE', 'C comment'),
    (3, 'Customer#000000003', 'Address#000000003', 3, 'Phone#000000003', 300.00, 'FURNITURE', 'C comment'),
    (4, 'Customer#000000004', 'Address#000000004', 4, 'Phone#000000004', 400.00, 'MACHINERY', 'C comment'),
    (5, 'Customer#000000005', 'Address#000000005', 5, 'Phone#000000005', 500.00, 'HOUSEHOLD', 'C comment');
