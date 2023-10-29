-- see https://docs.snowflake.com/en/sql-reference/functions/ilike_any

CREATE OR REPLACE TABLE ilike_example(subject varchar(20));
INSERT INTO ilike_example VALUES
    ('jane doe'),
    ('Jane Doe'),
    ('JANE DOE'),
    ('John Doe'),
    ('John Smith');