
-- snowflake sql:
select s2, bitor_agg(k) from bitwise_example group by s2;

-- databricks sql:
SELECT s2, BIT_OR(k) FROM bitwise_example GROUP BY s2;
