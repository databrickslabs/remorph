--Query type: DQL
WITH temp_result AS ( SELECT * FROM ( VALUES ('QID58286', 1), ('QID58287', 0) ) AS t (request_id, result_cache_hit) ) SELECT result_cache_hit FROM temp_result WHERE request_id = 'QID58286'
