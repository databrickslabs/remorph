-- tsql sql:
WITH TempResult AS ( SELECT * FROM ( VALUES (1, 'a'), (2, 'b'), (3, 'c') ) AS T (a1, b1) ) SELECT * FROM TempResult AS TR1 WHERE 3 = ( SELECT COUNT(*) FROM ( SELECT b1 FROM ( VALUES (1, 'a'), (2, 'b'), (3, 'c') ) AS T2 (b1, c1) WHERE T2.b1 = TR1.a1 ) X );
