--Query type: DQL
SELECT CAST((d_length * d_width) AS VARCHAR) + ' square meters' AS area FROM (VALUES (10, 5), (20, 10), (30, 15)) AS dimensions(d_length, d_width);