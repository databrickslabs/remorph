-- see https://docs.snowflake.com/en/sql-reference/functions/object_agg

CREATE OR REPLACE TABLE objectagg_example(g NUMBER, k VARCHAR(30), v VARIANT);
    INSERT INTO objectagg_example SELECT 0, 'name', 'Joe'::variant;
    INSERT INTO objectagg_example SELECT 0, 'age', 21::variant;
    INSERT INTO objectagg_example SELECT 1, 'name', 'Sue'::variant;
    INSERT INTO objectagg_example SELECT 1, 'zip', 94401::variant;

SELECT * FROM objectagg_example;
