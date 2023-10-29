-- see https://docs.snowflake.com/en/sql-reference/functions/like_all

CREATE OR REPLACE TABLE like_all_example(subject varchar(20));
INSERT INTO like_all_example VALUES
    ('John  Dddoe'),
    ('Joe   Doe'),
    ('John_do%wn'),
    ('Joe down'),
    ('Tom   Doe'),
    ('Tim down'),
    (null);