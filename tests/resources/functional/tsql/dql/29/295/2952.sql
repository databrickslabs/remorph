--Query type: DQL
WITH temp_result AS ( SELECT orderkey, totalprice, orderstatus FROM ( VALUES (1, 100.0, 'O'), (2, 200.0, 'O'), (3, 300.0, 'O') ) AS orders (orderkey, totalprice, orderstatus) ) SELECT orderkey, totalprice, orderstatus FROM temp_result WHERE orderkey = 1
