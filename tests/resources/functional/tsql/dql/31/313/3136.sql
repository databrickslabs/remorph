--Query type: DQL
WITH temp_result AS ( SELECT TOP (10) p_partkey, p_size, p_type FROM part ) SELECT p_partkey, p_size, p_type FROM temp_result