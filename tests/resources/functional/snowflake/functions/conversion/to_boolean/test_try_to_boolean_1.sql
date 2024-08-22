-- snowflake sql:
select TRY_TO_BOOLEAN(1);

-- databricks sql:
SELECT

    CASE
       WHEN 1 IS NULL THEN NULL
       WHEN TYPEOF(1) = 'boolean' THEN BOOLEAN(1)
       WHEN TYPEOF(1) = 'string' THEN
           CASE
               WHEN LOWER(1) IN ('true', 't', 'yes', 'y', 'on', '1') THEN true
               WHEN LOWER(1) IN ('false', 'f', 'no', 'n', 'off', '0') THEN false
               ELSE RAISE_ERROR('Boolean value of x is not recognized by TO_BOOLEAN')
               END
       WHEN TRY_CAST(1 AS DOUBLE) IS NOT NULL THEN
           CASE
               WHEN ISNAN(CAST(1 AS DOUBLE)) OR CAST(1 AS DOUBLE) = DOUBLE('infinity') THEN
                    RAISE_ERROR('Invalid parameter type for TO_BOOLEAN')
               ELSE CAST(1 AS DOUBLE) != 0.0
               END
       ELSE NULL
       END;
