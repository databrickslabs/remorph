-- see https://docs.snowflake.com/en/sql-reference/functions/as_timestamp

SELECT AS_TIMESTAMP_NTZ(timestamp1) AS "Timestamp" FROM multiple_types;