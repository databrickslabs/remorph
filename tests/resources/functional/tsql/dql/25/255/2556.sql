--Query type: DQL
WITH temp_result AS ( SELECT DB_ID() AS database_id ) SELECT database_id FROM temp_result;