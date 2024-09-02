--Query type: DCL
SELECT c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment
FROM (
    VALUES
        (1, 'Customer1', 100.00, 'Address1', 'Phone1', 'Comment1'),
        (2, 'Customer2', 200.00, 'Address2', 'Phone2', 'Comment2')
) AS temp_customer (c_custkey, c_name, c_acctbal, c_address, c_phone, c_comment)
WHERE c_acctbal > 0.00
ORDER BY c_acctbal DESC;