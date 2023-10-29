-- see https://docs.snowflake.com/en/sql-reference/functions/to_timestamp

SELECT 0::TIMESTAMP_NTZ, PARSE_JSON(0)::TIMESTAMP_NTZ, PARSE_JSON(0)::INT::TIMESTAMP_NTZ;