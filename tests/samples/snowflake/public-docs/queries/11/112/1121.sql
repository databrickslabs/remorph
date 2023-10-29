-- see https://docs.snowflake.com/en/sql-reference/functions/date_from_parts

SELECT DATE_FROM_PARTS(2004, -1, -1);  -- Two months and two days prior to DATE_FROM_PARTS(2004, 1, 1), so it's October 30, 2003.