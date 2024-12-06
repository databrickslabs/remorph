-- tsql sql:
DECLARE @x INT = 50, @y INT = 30; SELECT [Result] = IIF(@x > @y, 'TRUE', 'FALSE') FROM (VALUES (1)) AS temp_table(column_name);
