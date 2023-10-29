-- see https://docs.snowflake.com/en/sql-reference/functions/to_timestamp

ALTER SESSION SET TIMESTAMP_OUTPUT_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF9 TZH:TZM';
SELECT TO_TIMESTAMP_NTZ(40 * 365.25 * 86400 * 1000 + 456, 3);