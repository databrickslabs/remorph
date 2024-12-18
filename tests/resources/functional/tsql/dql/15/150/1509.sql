-- tsql sql:
DECLARE @x INT = 50, @y INT = 60; SELECT IIF ( @x < @y, 'TRUE', 'FALSE' ) AS Result FROM (VALUES (1)) AS temp_table(temp_column);
