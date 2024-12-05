-- snowflake sql:
SELECT t.col1, t.col2, t.col3 AS ca FROM table1 t WHERE ca in ('v1', 'v2');

-- databricks sql:
SELECT t.col1, t.col2, t.col3 AS ca FROM table1 AS t WHERE t.col3 in ('v1', 'v2');
