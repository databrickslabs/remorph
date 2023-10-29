-- see https://docs.snowflake.com/en/sql-reference/functions/date_from_parts

SELECT DATE_FROM_PARTS(2010, 1, 100), DATE_FROM_PARTS(2010, 1 + 24, 1);