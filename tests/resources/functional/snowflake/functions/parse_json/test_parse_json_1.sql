-- snowflake sql:
SELECT tt.id, PARSE_JSON(tt.details) FROM prod.public.table tt;

-- databricks sql:
SELECT tt.id, FROM_JSON(tt.details, {TT.DETAILS_SCHEMA}) FROM prod.public.table AS tt;

-- experimental sql:
SELECT tt.id, PARSE_JSON(tt.details) FROM prod.public.table AS tt;