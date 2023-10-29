-- see https://docs.snowflake.com/en/sql-reference/collation

CREATE TABLE collation_demo2 (c1 VARCHAR COLLATE 'fr', c2 VARCHAR COLLATE '');
INSERT INTO collation_demo2 (c1, c2) VALUES
    ('a', 'a'),
    ('b', 'b');