-- see https://docs.snowflake.com/en/sql-reference/functions/dynamic_table_refresh_history

SELECT
  name,
  state,
  state_code,
  state_message,
  query_id,
  data_timestamp,
  refresh_start_time,
  refresh_end_time
FROM
  TABLE (
    INFORMATION_SCHEMA.DYNAMIC_TABLE_REFRESH_HISTORY (
      NAME_PREFIX => 'MYDB.MYSCHEMA.', ERROR_ONLY => TRUE
    )
  )
ORDER BY
  name,
  data_timestamp;