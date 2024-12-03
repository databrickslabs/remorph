--Query type: DQL
DECLARE @order_date datetime2 = '1995-03-01 00:00:00.0000000';
SELECT 'Week-1',
       DATETRUNC(week, @order_date) AS truncated_date
FROM   (
       VALUES (1)
       ) AS temp_table(column_name);
