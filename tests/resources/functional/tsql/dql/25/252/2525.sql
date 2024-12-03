--Query type: DQL
SELECT DATEADD(year, 2147483647, date_column) AS new_date
FROM (
    VALUES ('20060731')
) AS date_table (date_column);

SELECT DATEADD(year, -2147483647, date_column) AS new_date
FROM (
    VALUES ('20060731')
) AS date_table (date_column);
