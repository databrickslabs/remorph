-- tsql sql:
DECLARE my_cursor_name CURSOR FOR SELECT * FROM (VALUES (1, 'a'), (2, 'b')) AS my_table (id, name);
OPEN my_cursor_name;
CLOSE my_cursor_name;
