
-- source:
select TO_BOOLEAN(col1);

-- databricks_sql:
SELECT
CASE
   WHEN col1 IS NULL THEN NULL
   WHEN TYPEOF(col1) = 'boolean' THEN BOOLEAN(col1)
   WHEN TYPEOF(col1) = 'string' THEN
       CASE
           WHEN LOWER(col1) IN ('true', 't', 'yes', 'y', 'on', '1') THEN TRUE
           WHEN LOWER(col1) IN ('false', 'f', 'no', 'n', 'off', '0') THEN FALSE
           ELSE RAISE_ERROR('Boolean value of x is not recognized by TO_BOOLEAN')
           END
   WHEN ISNOTNULL(TRY_CAST(col1 AS DOUBLE)) THEN
       CASE
           WHEN ISNAN(CAST(col1 AS DOUBLE)) OR CAST(col1 AS DOUBLE) = DOUBLE('infinity') THEN
                RAISE_ERROR('Invalid parameter type for TO_BOOLEAN')
           ELSE CAST(col1 AS DOUBLE) != 0.0
           END
   ELSE RAISE_ERROR('Invalid parameter type for TO_BOOLEAN')
   END;
