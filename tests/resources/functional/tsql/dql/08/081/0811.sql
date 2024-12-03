--Query type: DQL
SELECT CASE WHEN EXISTS ( SELECT 1 FROM ( VALUES (1, 2, 3), (4, 5, 6), (7, 8, 9) ) AS temp_table (col_1, col_2, col_3) WHERE col_1 = 1 AND col_2 = 2 AND col_3 = 3 ) THEN 'TRUE' ELSE 'FALSE' END AS RESULT;
