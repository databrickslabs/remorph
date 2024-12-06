-- tsql sql:
WITH temp_result AS (SELECT 'hello' AS spanish_phrase, 'hello' AS uncollated_phrase UNION ALL SELECT 'world', 'world') SELECT * FROM temp_result WHERE spanish_phrase COLLATE SQL_Latin1_General_CP1_CI_AS = uncollated_phrase COLLATE SQL_Latin1_General_CP1_CI_AS;
