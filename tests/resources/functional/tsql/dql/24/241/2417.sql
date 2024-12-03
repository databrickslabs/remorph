--Query type: DQL
SELECT ATAN(o_totalprice) AS atanCalc1, ATAN(-l_discount) AS atanCalc2, ATAN(0) AS atanCalc3, ATAN(c_acctbal) AS atanCalc4, ATAN(ps_supplycost) AS atanCalc5 FROM (VALUES (100, 0.1, 1000, 1000.50), (200, 0.2, 2000, 2000.25), (300, 0.3, 3000, 3000.10)) AS t (o_totalprice, l_discount, c_acctbal, ps_supplycost);
