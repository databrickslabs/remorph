-- tsql sql:
CREATE PARTITION FUNCTION myRangePF3 (INT) AS RANGE LEFT FOR VALUES (5, 50, 500);
CREATE PARTITION SCHEME myRangePS3 AS PARTITION myRangePF3 ALL TO ([PRIMARY]);
-- REMORPH CLEANUP: DROP PARTITION FUNCTION myRangePF3;
-- REMORPH CLEANUP: DROP PARTITION SCHEME myRangePS3;