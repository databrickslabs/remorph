--Query type: DQL
WITH temp_result AS ( SELECT orderkey, custkey FROM ( VALUES (1, 10), (2, 20), (3, 30) ) AS orders (orderkey, custkey) ) SELECT orderkey, custkey FROM temp_result;
