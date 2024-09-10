-- snowflake sql:
SELECT tt.id, PARSE_JSON(tt.details) FROM prod.public.table tt;

-- databricks sql:
SELECT tt.id, FROM_JSON ( tt.details, SCHEMA_OF_JSON ( '{tt.details}' )  ) FROM prod.public.table as tt;

-- experimental sql:
SELECT tt.id, PARSE_JSON(tt.details) FROM prod.public.table AS tt;