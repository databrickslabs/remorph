--Query type: DQL
WITH TempResult AS ( SELECT 4 AS column1, 5 AS column2, NULL AS column3 UNION ALL SELECT 7, 8, 9 ) SELECT CASE WHEN EXISTS ( SELECT 1 FROM TempResult WHERE column1 = 4 AND column2 = 5 AND column3 IS NULL ) THEN 1 ELSE 0 END AS RESULT;
