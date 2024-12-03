--Query type: DQL
DECLARE @a INT = 45, @b INT = 40; SELECT IIF ( @a > @b, 'TRUE', 'FALSE' ) AS Result FROM (VALUES (1)) AS temp_result(column_name);
