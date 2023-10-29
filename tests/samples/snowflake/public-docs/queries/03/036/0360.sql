-- see https://docs.snowflake.com/en/sql-reference/functions/regexp

CREATE OR REPLACE TABLE strings (v VARCHAR(50));
INSERT INTO strings (v) VALUES
    ('San Francisco'),
    ('San Jose'),
    ('Santa Clara'),
    ('Sacramento');