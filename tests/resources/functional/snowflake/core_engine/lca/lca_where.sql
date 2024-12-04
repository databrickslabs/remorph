-- snowflake sql:
SELECT column_a as alias_a FROM table_a where alias_a = '123';

-- databricks sql:
SELECT column_a as alias_a FROM table_a where column_a = '123';
