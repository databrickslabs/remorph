-- tsql sql:
DECLARE @MyCrsrRef1 CURSOR;

SET @MyCrsrRef1 = CURSOR FOR
    SELECT *
    FROM (
        VALUES (1, 'John'),
               (2, 'Jane')
    ) AS MyCTE (ID, Name);

OPEN @MyCrsrRef1;

DECLARE @ID INT,
        @Name VARCHAR(50);

FETCH NEXT FROM @MyCrsrRef1 INTO @ID, @Name;

SELECT @ID, @Name;

DEALLOCATE @MyCrsrRef1;
