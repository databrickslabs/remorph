-- tsql sql:
SELECT 'true' WHERE 1.35 BETWEEN ( SELECT c1 FROM ( VALUES (1, 2, 3), (4, 5, 6) ) AS t (c1, c2, c3) ) AND ( SELECT c2 FROM ( VALUES (7, 8, 9), (10, 11, 12) ) AS t (c1, c2, c3) );
