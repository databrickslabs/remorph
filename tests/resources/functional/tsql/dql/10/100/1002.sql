--Query type: DQL
WITH temp_result AS ( SELECT TOP 1 * FROM ( VALUES ('1', 'John', 'Doe'), ('2', 'Jane', 'Doe') ) AS customer (c_custkey, c_name, c_address) ) SELECT * FROM temp_result;
