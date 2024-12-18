-- tsql sql:
WITH temp_result AS ( SELECT * FROM customer WHERE c_acctbal IS NULL ) SELECT * FROM temp_result ORDER BY c_custkey;
