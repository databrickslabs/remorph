--Query type: DQL
WITH temp_result AS ( SELECT * FROM ( VALUES ('value1'), ('value2') ) AS temp_table (c_custkey) ) SELECT * FROM temp_result ORDER BY c_custkey OFFSET 5 ROWS FETCH NEXT 10 ROWS ONLY
