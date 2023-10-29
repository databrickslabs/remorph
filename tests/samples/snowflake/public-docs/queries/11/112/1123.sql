-- see https://docs.snowflake.com/en/sql-reference/functions/date_from_parts

SELECT DATE_FROM_PARTS(2004, 2, 1),   -- February 1, 2004, as expected.
       DATE_FROM_PARTS(2004, 2, 0),   -- This is one day prior to DATE_FROM_PARTS(2004, 2, 1), so it's January 31, 2004.
       DATE_FROM_PARTS(2004, 2, -1);  -- Two days prior to DATE_FROM_PARTS(2004, 2, 1) so it's January 30, 2004.