-- see https://docs.snowflake.com/en/sql-reference/functions/date_part

SELECT TO_TIMESTAMP('2013-05-08T23:39:20.123-07:00') AS "TIME_STAMP1",
         DATE_PART(EPOCH_MILLISECOND, "TIME_STAMP1") AS "EXTRACTED EPOCH MILLISECOND";