-- see https://docs.snowflake.com/en/sql-reference/sql/create-sequence

SELECT COUNT(i), COUNT(DISTINCT i) FROM sequence_demo;