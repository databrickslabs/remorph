-- tsql sql:
SELECT c_acctbal FROM (VALUES (100.0), (200.0), (300.0)) AS Temp_Result(c_acctbal) ORDER BY c_acctbal;
