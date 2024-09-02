--Query type: DQL
DECLARE @date_exp NVARCHAR(30) = '2007-04-21 01:01:01.1234567';
WITH temp_result AS (
    SELECT @date_exp AS date_exp
)
SELECT {fn DAYNAME(date_exp)} AS DAYNAME,
       {fn DAYOFMONTH(date_exp)} AS DAYOFMONTH,
       {fn DAYOFWEEK(date_exp)} AS DAYOFWEEK,
       {fn HOUR(date_exp)} AS HOUR,
       {fn MINUTE(date_exp)} AS MINUTE,
       {fn SECOND(date_exp)} AS SECOND,
       {fn MONTHNAME(date_exp)} AS MONTHNAME,
       {fn QUARTER(date_exp)} AS QUARTER,
       {fn WEEK(date_exp)} AS WEEK
FROM temp_result;