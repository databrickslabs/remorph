-- see https://docs.snowflake.com/en/sql-reference/functions/strtok_split_to_table

CREATE OR REPLACE TABLE splittable (v VARCHAR);
INSERT INTO splittable (v) VALUES ('a b'), ('cde'), ('f|g'), ('');