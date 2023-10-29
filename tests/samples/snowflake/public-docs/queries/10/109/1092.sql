-- see https://docs.snowflake.com/en/sql-reference/functions/previous_day

SELECT CURRENT_DATE() AS "Today's Date",
       PREVIOUS_DAY("Today's Date", 'Friday ') AS "Previous Friday";
