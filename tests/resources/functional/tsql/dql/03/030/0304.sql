--Query type: DQL
SELECT TOP 1
    MONTH('2007-04-30T01:01:01.1234') AS month_value
FROM (
    VALUES ('2007-04-30T01:01:01.1234')
) AS customer_date (
    date_value
);
