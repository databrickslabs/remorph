--Query type: DQL
DECLARE cursor1 CURSOR FOR
    SELECT *
    FROM (
        VALUES ('customer', 1, 10, 0.5),
               ('orders', 2, 20, 0.7)
    ) AS t1(tablename, objectid, indexid, frag);

DECLARE @tablename nvarchar(50),
        @objectid int,
        @indexid int,
        @frag float;

OPEN cursor1;

FETCH NEXT FROM cursor1 INTO @tablename, @objectid, @indexid, @frag;

WHILE @@FETCH_STATUS = 0
BEGIN
    PRINT @tablename + ' ' + CONVERT(nvarchar, @objectid) + ' ' + CONVERT(nvarchar, @indexid) + ' ' + CONVERT(nvarchar, @frag);

    FETCH NEXT FROM cursor1 INTO @tablename, @objectid, @indexid, @frag;
END;

CLOSE cursor1;

DEALLOCATE cursor1;