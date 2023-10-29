-- see https://docs.snowflake.com/en/sql-reference/functions/hour-minute-second

SELECT '2013-05-08T23:39:20.123-07:00'::TIMESTAMP AS TSTAMP,
         HOUR(tstamp) AS "HOUR",
         MINUTE(tstamp) AS "MINUTE",
         SECOND(tstamp) AS "SECOND";