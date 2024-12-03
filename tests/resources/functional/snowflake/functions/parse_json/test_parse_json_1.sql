-- snowflake sql:
SELECT tt.id, PARSE_JSON(tt.details) FROM prod.public.table tt;

-- databricks sql:
SELECT tt.id, PARSE_JSON(tt.details) FROM prod.public.table AS tt;
