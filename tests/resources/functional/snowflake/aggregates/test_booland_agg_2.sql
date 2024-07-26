
-- snowflake sql:
select s2, booland_agg(k) from bool_example group by s2;

-- databricks sql:
SELECT s2, BOOL_AND(k) FROM bool_example GROUP BY s2;
