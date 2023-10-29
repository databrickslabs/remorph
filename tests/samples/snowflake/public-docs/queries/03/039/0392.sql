-- see https://docs.snowflake.com/en/sql-reference/functions/equal_null

CREATE OR REPLACE TABLE x (i number);
INSERT INTO x values
    (1), 
    (2), 
    (null);