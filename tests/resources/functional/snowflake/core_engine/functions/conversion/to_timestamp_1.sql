
-- snowflake sql:
SELECT to_timestamp(col1) AS to_timestamp_col1 FROM tabl;

-- databricks sql:
SELECT
  IFNULL(
    COALESCE(
      TRY_TO_TIMESTAMP(col1, 'yyyy-MM-dd' T 'HH:mmXXX'),
      TRY_TO_TIMESTAMP(col1, 'yyyy-MM-dd HH:mmXXX'),
      TRY_TO_TIMESTAMP(col1, 'EEE, dd MMM yyyy HH:mm:ss ZZZ'),
      TRY_TO_TIMESTAMP(col1, 'EEE, dd MMM yyyy HH:mm:ss.SSSSSSSSS ZZZ'),
      TRY_TO_TIMESTAMP(col1, 'EEE, dd MMM yyyy hh:mm:ss a ZZZ'),
      TRY_TO_TIMESTAMP(col1, 'EEE, dd MMM yyyy hh:mm:ss.SSSSSSSSS a ZZZ'),
      TRY_TO_TIMESTAMP(col1, 'EEE, dd MMM yyyy HH:mm:ss'),
      TRY_TO_TIMESTAMP(col1, 'EEE, dd MMM yyyy HH:mm:ss.SSSSSSSSS'),
      TRY_TO_TIMESTAMP(col1, 'EEE, dd MMM yyyy hh:mm:ss a'),
      TRY_TO_TIMESTAMP(col1, 'EEE, dd MMM yyyy hh:mm:ss.SSSSSSSSS a'),
      TRY_TO_TIMESTAMP(col1, 'MM/dd/yyyy HH:mm:ss'),
      TRY_TO_TIMESTAMP(col1, 'EEE MMM dd HH:mm:ss ZZZ yyyy')
    ),
    TO_TIMESTAMP(col1)
  ) AS to_timestamp_col1
FROM
  tabl;
