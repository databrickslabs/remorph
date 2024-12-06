-- tsql sql:
SELECT c_custkey FROM ( SELECT 1 AS c_custkey, 25.0 AS c_acctbal, '25-989-741-2988' AS c_phone, 1 AS c_nationkey ) AS temp_result WHERE c_nationkey = 1 AND c_phone = '25-989-741-2988;
