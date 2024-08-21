-- snowflake sql:
select IS_INTEGER(col);

-- databricks sql:
SELECT

      CASE
         WHEN col IS NULL THEN NULL
         WHEN col RLIKE '^-?[0-9]+$' AND TRY_CAST(col AS INT) IS NOT NULL THEN TRUE
         ELSE FALSE
         END
