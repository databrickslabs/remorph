-- tsql sql:
CREATE PARTITION FUNCTION myNewRangePF1 (int) AS RANGE RIGHT FOR VALUES (1, 2, 3);
CREATE PARTITION SCHEME myNewRangePS1 AS PARTITION myNewRangePF1 ALL TO ('PRIMARY');
-- REMORPH CLEANUP: DROP PARTITION FUNCTION myNewRangePF1;
-- REMORPH CLEANUP: DROP PARTITION SCHEME myNewRangePS1;
