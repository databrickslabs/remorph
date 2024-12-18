-- tsql sql:
DECLARE cur CURSOR FOR SELECT * FROM (VALUES (1, 'a'), (2, 'b')) AS t(id, name);
OPEN cur;
