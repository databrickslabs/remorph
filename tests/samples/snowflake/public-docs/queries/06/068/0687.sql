-- see https://docs.snowflake.com/en/sql-reference/constructs/join

INSERT INTO t1 (col1) VALUES 
   (2),
   (3),
   (4);
INSERT INTO t2 (col1) VALUES 
   (1),
   (2),
   (2),
   (3);