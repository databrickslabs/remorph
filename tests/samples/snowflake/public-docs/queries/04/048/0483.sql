-- see https://docs.snowflake.com/en/sql-reference/operators-logical

CREATE TABLE logical2 (x BOOLEAN);
INSERT INTO logical2 (x) VALUES 
    (False),
    (True),
    (NULL);