
-- snowflake sql:
select DATE_TRUNC('month', TRY_TO_DATE(COLUMN1)) from table;

-- databricks sql:
SELECT DATE_TRUNC('MONTH', DATE(TRY_TO_TIMESTAMP(COLUMN1))) FROM table;
