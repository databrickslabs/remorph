
-- snowflake sql:
SELECT to_timestamp(col1) AS to_timestamp_col1 FROM tabl;

-- databricks sql:
SELECT
  CASE
    TYPEOF(col1)
    WHEN 'string' THEN IFNULL(
      COALESCE(
        TRY_TO_TIMESTAMP(TRY_CAST(col1 AS INT)),
        TRY_TO_TIMESTAMP(col1, 'yyyy-MM-dd\'T\'HH:mmXXX'),
    	TRY_TO_TIMESTAMP(col1, 'yyyy-MM-dd HH:mmXXX'),
        TRY_TO_TIMESTAMP(SUBSTR(col1, 4), ', dd MMM yyyy HH:mm:ss ZZZ'),
    	TRY_TO_TIMESTAMP(SUBSTR(col1, 4), ', dd MMM yyyy HH:mm:ss.SSSSSSSSS ZZZ'),
        TRY_TO_TIMESTAMP(SUBSTR(col1, 4), ', dd MMM yyyy hh:mm:ss a ZZZ'),
        TRY_TO_TIMESTAMP(SUBSTR(col1, 4), ', dd MMM yyyy hh:mm:ss.SSSSSSSSS a ZZZ'),
        TRY_TO_TIMESTAMP(SUBSTR(col1, 4), ', dd MMM yyyy HH:mm:ss'),
        TRY_TO_TIMESTAMP(SUBSTR(col1, 4), ', dd MMM yyyy HH:mm:ss.SSSSSSSSS'),
        TRY_TO_TIMESTAMP(SUBSTR(col1, 4), ', dd MMM yyyy hh:mm:ss a'),
        TRY_TO_TIMESTAMP(SUBSTR(col1, 4), ', dd MMM yyyy hh:mm:ss.SSSSSSSSS a'),
        TRY_TO_TIMESTAMP(col1, 'M/dd/yyyy HH:mm:ss'),
        TRY_TO_TIMESTAMP(SUBSTR(col1, 4), ' MMM dd HH:mm:ss ZZZ yyyy')
      ),
      TO_TIMESTAMP(col1)
    )
    ELSE CAST(col1 AS TIMESTAMP)
  END AS to_timestamp_col1
FROM
  tabl;
