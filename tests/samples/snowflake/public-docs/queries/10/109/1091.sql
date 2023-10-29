-- see https://docs.snowflake.com/en/sql-reference/functions/next_day

SELECT CURRENT_DATE() AS "Today's Date",
       NEXT_DAY("Today's Date", 'Friday ') AS "Next Friday";
