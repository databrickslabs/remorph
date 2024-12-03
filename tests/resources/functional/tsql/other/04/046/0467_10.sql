--Query type: DCL
DECLARE my_cursor CURSOR FOR SELECT * FROM (VALUES (1, 'a'), (2, 'b')) AS t(id, name);
DEALLOCATE my_cursor;
