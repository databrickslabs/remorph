-- tsql sql:
SELECT * FROM ( SELECT c_custkey, c_nationkey, c_acctbal, ROW_NUMBER() OVER ( PARTITION BY c_nationkey ORDER BY c_acctbal ) AS row_num FROM customer ) AS temp_result WHERE row_num = 1;
