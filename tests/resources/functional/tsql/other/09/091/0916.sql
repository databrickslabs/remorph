-- tsql sql:
CREATE DATABASE SCOPED CREDENTIAL SQLServerCredentials
WITH IDENTITY = 'username',
    SECRET = 'password';

WITH temp_result AS (
    SELECT 1001 AS suppkey,
           'Supplier#000000001' AS s_name,
           1000.00 AS s_acctbal,
           '25-989-741-2988' AS s_phone,
           'Comment for Supplier#000000001' AS s_comment,
           5 AS n_nationkey,
           'UNITED STATES' AS n_name
)
SELECT suppkey,
       s_name,
       SUM(s_acctbal) AS total_revenue,
       s_acctbal,
       n_name,
       s_phone,
       s_comment
FROM temp_result
GROUP BY suppkey,
         s_name,
         s_acctbal,
         n_name,
         s_phone,
         s_comment
ORDER BY total_revenue DESC;
