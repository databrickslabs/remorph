--Query type: DCL
DECLARE @MyNewCursor CURSOR;
SET @MyNewCursor = CURSOR LOCAL SCROLL FOR
    SELECT *
    FROM (
        VALUES (1, 'USA'),
               (2, 'Canada')
    ) AS CustomerRegion(RegionID, RegionName);
DEALLOCATE @MyNewCursor;