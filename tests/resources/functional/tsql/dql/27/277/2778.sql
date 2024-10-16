--Query type: DQL
WITH temp_result AS (SELECT 0x01 AS sid)
SELECT SUSER_SNAME(sid)
FROM temp_result;