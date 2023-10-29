-- see https://docs.snowflake.com/en/sql-reference/functions-analytic

CREATE TABLE example_sliding
  (p INT, o INT, i INT, r INT, s VARCHAR(100));

INSERT INTO example_sliding VALUES
  (100,1,1,70,'seventy'),(100,2,2,30, 'thirty'),(100,3,3,40,'forty'),(100,4,NULL,90,'ninety'),
  (100,5,5,50,'fifty'),(100,6,6,30,'thirty'),
  (200,7,7,40,'forty'),(200,8,NULL,NULL,'n_u_l_l'),(200,9,NULL,NULL,'n_u_l_l'),(200,10,10,20,'twenty'),
  (200,11,NULL,90,'ninety'),
  (300,12,12,30,'thirty'),
  (400,13,NULL,20,'twenty');