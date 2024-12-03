--Query type: DML
DECLARE my_cursor CURSOR FOR SELECT * FROM (VALUES (1, 'John'), (2, 'Alice'), (3, 'Bob')) AS users (id, name);
OPEN my_cursor;
CLOSE my_cursor;
-- REMORPH CLEANUP: DEALLOCATE my_cursor;
