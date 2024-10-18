--Query type: DQL
DECLARE @date_exp NVARCHAR(30) = '2007-04-21 01:01:01.1234567';
WITH dates AS (
    SELECT @date_exp AS date_value
)
SELECT
    {fn DAYNAME(date_value)} AS day_name,
    {fn DAYOFMONTH(date_value)} AS day_of_month,
    {fn DAYOFWEEK(date_value)} AS day_of_week,
    {fn HOUR(date_value)} AS hour_value,
    {fn MINUTE(date_value)} AS minute_value,
    {fn SECOND(date_value)} AS second_value,
    {fn MONTHNAME(date_value)} AS month_name,
    {fn QUARTER(date_value)} AS quarter_value,
    {fn WEEK(date_value)} AS week_value
FROM dates;