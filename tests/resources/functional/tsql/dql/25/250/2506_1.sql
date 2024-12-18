-- tsql sql:
SELECT totalprice + discount + 10 AS result FROM (VALUES (100, 0.1), (200, 0.2), (300, 0.3)) AS temp_result (totalprice, discount) GROUP BY totalprice, discount;
