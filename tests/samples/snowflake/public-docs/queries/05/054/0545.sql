-- see https://docs.snowflake.com/en/sql-reference/functions/concat

CREATE TABLE table1 (s1 VARCHAR, s2 VARCHAR, s3 VARCHAR);
INSERT INTO table1 (s1, s2, s3) VALUES 
    ('co', 'd', 'e'),
    ('Colorado ', 'River ', NULL);