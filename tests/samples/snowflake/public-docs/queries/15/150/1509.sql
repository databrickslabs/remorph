-- see https://docs.snowflake.com/en/sql-reference/functions/to_timestamp

SELECT TO_TIMESTAMP_NTZ(0), TO_TIMESTAMP_NTZ(PARSE_JSON(0)), TO_TIMESTAMP_NTZ(PARSE_JSON(0)::INT);