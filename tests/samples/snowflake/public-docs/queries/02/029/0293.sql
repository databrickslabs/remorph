-- see https://docs.snowflake.com/en/sql-reference/functions/avg

CREATE OR REPLACE TABLE avg_example(int_col int, d decimal(10,5), s1 varchar(10), s2 varchar(10));
INSERT INTO avg_example VALUES
    (1, 1.1, '1.1','one'), 
    (1, 10, '10','ten'),
    (2, 2.4, '2.4','two'), 
    (2, NULL, NULL, 'NULL'),
    (3, NULL, NULL, 'NULL'),
    (NULL, 9.9, '9.9','nine');