-- tsql sql:
CREATE TABLE #myNewTable
(
    ColumnA uniqueidentifier DEFAULT (NEWSEQUENTIALID())
);

INSERT INTO #myNewTable (ColumnA)
DEFAULT VALUES;

SELECT *
FROM #myNewTable;

-- REMORPH CLEANUP: DROP TABLE #myNewTable;
