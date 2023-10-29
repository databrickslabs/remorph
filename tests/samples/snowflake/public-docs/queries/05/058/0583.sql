-- see https://docs.snowflake.com/en/sql-reference/snowflake-scripting/for

CREATE or replace TABLE invoices (price NUMBER(12, 2));
INSERT INTO invoices (price) VALUES
    (11.11),
    (22.22);