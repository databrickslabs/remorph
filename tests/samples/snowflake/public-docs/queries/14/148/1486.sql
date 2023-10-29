-- see https://docs.snowflake.com/en/sql-reference/functions/last_day

SELECT TO_DATE('2015-05-08T23:39:20.123-07:00') AS "DATE",
       LAST_DAY("DATE", 'year') AS "LAST DAY OF YEAR";