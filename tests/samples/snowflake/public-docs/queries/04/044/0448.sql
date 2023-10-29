-- see https://docs.snowflake.com/en/sql-reference/functions/decode

CREATE TABLE d (column1 INTEGER);
INSERT INTO d (column1) VALUES 
    (1),
    (2),
    (NULL),
    (4);