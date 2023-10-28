ALTER SESSION SET WEEK_START = 0;

SELECT d "Date", DAYNAME(d) "Day",
       DAYOFWEEK(d) "DOW",
       DATE_TRUNC('week', d) "Trunc Date",
       DAYNAME("Trunc Date") "Trunc Day",
       LAST_DAY(d, 'week') "Last DOW Date",
       DAYNAME("Last DOW Date") "Last DOW Day",
       DATEDIFF('week', '2017-01-01', d) "Weeks Diff from 2017-01-01 to Date"
FROM week_examples;


ALTER SESSION SET WEEK_START = 1;

SELECT d "Date", DAYNAME(d) "Day",
       DAYOFWEEK(d) "DOW",
       DATE_TRUNC('week', d) "Trunc Date",
       DAYNAME("Trunc Date") "Trunc Day",
       LAST_DAY(d, 'week') "Last DOW Date",
       DAYNAME("Last DOW Date") "Last DOW Day",
       DATEDIFF('week', '2017-01-01', d) "Weeks Diff from 2017-01-01 to Date"
FROM week_examples;
