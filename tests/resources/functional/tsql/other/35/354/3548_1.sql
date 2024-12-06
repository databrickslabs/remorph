-- tsql sql:
EXEC sp_executesql N'SELECT * FROM ( VALUES (@param1, @param2) ) AS DemoTable(Column1, Column2);', N'@param1 INT, @param2 INT', @param1 = 1, @param2 = 2;
