-- snowflake sql:
SELECT
tt.id
, PARSE_JSON(tt.details)
FROM prod.public.table tt
,  LATERAL FLATTEN (input=> PARSE_JSON(PARSE_JSON(tt.resp):items)) AS lit
,  LATERAL FLATTEN (input=> parse_json(lit.value:"details")) AS ltd;

-- databricks sql:
SELECT
  tt.id, FROM_JSON(tt.details, {TT.DETAILS_SCHEMA}) FROM prod.public.table AS tt
  LATERAL VIEW EXPLODE(FROM_JSON(FROM_JSON(tt.resp, {TT.RESP_SCHEMA}).items, {JSON_COLUMN_SCHEMA})) AS lit
  LATERAL VIEW EXPLODE(FROM_JSON(lit.value.details, {JSON_COLUMN_SCHEMA})) AS ltd;

-- experimental sql:
SELECT
  tt.id, PARSE_JSON(tt.details) FROM prod.public.table AS tt
  LATERAL VIEW EXPLODE(PARSE_JSON(PARSE_JSON(tt.resp).items)) AS lit
  LATERAL VIEW EXPLODE(PARSE_JSON(lit.value.details)) AS ltd;
