--Query type: DML
CREATE TABLE #lineitem
(
    l_linename VARCHAR(50),
    l_mfgr VARCHAR(50)
);

INSERT INTO #lineitem (l_linename, l_mfgr)
VALUES
    ('LARGE ANODIZED STEEL', 'INITIAL_MFGR'),
    ('STANDARD POLISHED STEEL', 'INITIAL_MFGR'),
    ('SMALL POLISHED STEEL', 'INITIAL_MFGR');

DECLARE @SummaryOfChanges TABLE
(
    Change VARCHAR(20)
);

MERGE INTO #lineitem AS Target
USING (
    VALUES
        ('LARGE ANODIZED STEEL', 'ECONOMY ANODIZED STEEL'),
        ('STANDARD POLISHED STEEL', 'STANDARD POLISHED COPPER'),
        ('SMALL POLISHED STEEL', 'SMALL POLISHED STEEL')
) AS Source (NewName, NewMfgr)
ON Target.l_linename = Source.NewName
WHEN MATCHED THEN
    UPDATE SET l_mfgr = Source.NewMfgr
WHEN NOT MATCHED BY TARGET THEN
    INSERT (l_linename, l_mfgr)
    VALUES (NewName, NewMfgr)
OUTPUT $action INTO @SummaryOfChanges;

SELECT Change, COUNT(*) AS CountPerChange
FROM @SummaryOfChanges
GROUP BY Change;

SELECT *
FROM #lineitem;

-- REMORPH CLEANUP: DROP TABLE #lineitem;
-- REMORPH CLEANUP: DROP TABLE @SummaryOfChanges;