-- TODO: Fix this test, it's currently incorrect because RANDOM() can't be simply passed through as-is.
-- See: https://github.com/databrickslabs/remorph/issues/1280
-- Reference: https://docs.snowflake.com/en/sql-reference/functions/random.html

-- snowflake sql:
SELECT random(), random(col1) FROM tabl;

-- databricks sql:
SELECT RANDOM(), RANDOM(col1) FROM tabl;
