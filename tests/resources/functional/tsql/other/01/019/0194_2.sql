--Query type: TCL
BEGIN TRANSACTION;
INSERT INTO customer (c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment)
VALUES (1, 'Customer#000000001', '7716.36.3961', 5, '25-989-741-2988', 711.56, 'BUILDING', 'regular future accounts deposit');
COMMIT;
