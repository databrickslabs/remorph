-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/with-common-table-expression-transact-sql?view=sql-server-ver16

DECLARE @t1 TABLE (itmID INT, itmIDComp INT);
INSERT @t1 VALUES (1,10), (2,10);

DECLARE @t2 TABLE (itmID INT, itmIDComp INT);
INSERT @t2 VALUES (3,10), (4,10);

WITH vw AS
(
    SELECT itmIDComp, itmID
    FROM @t1

    UNION ALL

    SELECT itmIDComp, itmID
    FROM @t2
)
, r AS
(
    SELECT t.itmID AS itmIDComp
           , NULL AS itmID
           , CAST(0 AS BIGINT) AS N
           , 1 AS Lvl
    FROM (SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4) AS t (itmID)

UNION ALL

SELECT t.itmIDComp
    , t.itmID
    , ROW_NUMBER() OVER(PARTITION BY t.itmIDComp ORDER BY t.itmIDComp, t.itmID) AS N
    , Lvl + 1
FROM r
    JOIN vw AS t ON t.itmID = r.itmIDComp
)

SELECT Lvl, N FROM r;