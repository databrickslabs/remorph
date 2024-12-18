-- tsql sql:
DECLARE new_cursor CURSOR FOR SELECT * FROM (VALUES (1, 'John'), (2, 'Doe')) AS temp_table(id, name);
CLOSE new_cursor;
