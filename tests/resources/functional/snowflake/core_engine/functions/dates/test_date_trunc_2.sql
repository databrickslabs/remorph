
-- snowflake sql:
DELETE FROM table1 WHERE cre_at >= DATE_TRUNC('month', TRY_TO_DATE('2022-01-15'));

-- databricks sql:
DELETE FROM table1 WHERE cre_at >= DATE_TRUNC('MONTH', DATE(TRY_TO_TIMESTAMP('2022-01-15')));
