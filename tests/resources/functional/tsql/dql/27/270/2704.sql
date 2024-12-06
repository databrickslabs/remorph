-- tsql sql:
WITH temp_result AS (SELECT 'abcdef' AS GreekCol, 'xyzabc' AS LatinCol, 5 AS id UNION ALL SELECT 'abcxyz', 'defabc', 15) SELECT PATINDEX((CASE WHEN id > 10 THEN GreekCol ELSE LatinCol END), 'a') FROM temp_result
