
-- snowflake sql:
SELECT tabb.col_a, tabb.col_b, last_value( CASE WHEN tabb.col_c IN (‘xyz’, ‘abc’) THEN tabb.col_d END) ignore nulls OVER (partition BY tabb.col_e ORDER BY tabb.col_f RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS derived_col_a FROM schema_a.table_a taba LEFT JOIN schema_b.table_b AS tabb ON taba.col_e = tabb.col_e;

-- databricks sql:
SELECT tabb.col_a, tabb.col_b, LAST_VALUE(CASE WHEN tabb.col_c IN (‘xyz’, ‘abc’) THEN tabb.col_d END) IGNORE NULLS OVER (PARTITION BY tabb.col_e ORDER BY tabb.col_f NULLS LAST RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS derived_col_a FROM schema_a.table_a AS taba LEFT JOIN schema_b.table_b AS tabb ON taba.col_e = tabb.col_e;
