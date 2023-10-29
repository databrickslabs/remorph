-- see https://docs.snowflake.com/en/sql-reference/functions/conditional_true_event

CREATE OR REPLACE TABLE tbl
(p int, o int, i int, r int, s varchar(100));

INSERT INTO tbl VALUES
(100,1,1,70,'seventy'),(100,2,2,30, 'thirty'),(100,3,3,40,'fourty'),(100,4,NULL,90,'ninety'),(100,5,5,50,'fifty'),(100,6,6,30,'thirty'),
(200,7,7,40,'fourty'),(200,8,NULL,NULL,'n_u_l_l'),(200,9,NULL,NULL,'n_u_l_l'),(200,10,10,20,'twenty'),(200,11,NULL,90,'ninety'),
(300,12,12,30,'thirty'),
(400,13,NULL,20,'twenty');

SELECT * FROM tbl ORDER BY p, o, i;


SELECT p, o, CONDITIONAL_TRUE_EVENT(o>2) OVER (PARTITION BY p ORDER BY o) FROM tbl ORDER BY p, o;


SELECT p, o, CONDITIONAL_TRUE_EVENT(LAG(O) OVER (PARTITION BY P ORDER BY O) >1) OVER (PARTITION BY P ORDER BY O) FROM tbl ORDER BY p, o;
