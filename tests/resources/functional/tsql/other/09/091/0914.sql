-- tsql sql:
SELECT * FROM (VALUES (1001, 'Supplier#000000001', 1000.00, '25-989-741-2988', 'Comment for Supplier#000000001', 5, 'UNITED STATES'), (1002, 'Supplier#000000002', 2000.00, '25-989-741-2999', 'Comment for Supplier#000000002', 5, 'UNITED STATES')) AS temp_result (s_suppkey, s_name, s_acctbal, s_phone, s_comment, n_nationkey, n_name);
