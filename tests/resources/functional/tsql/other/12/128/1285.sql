--Query type: DML
CREATE TABLE #T1
(
    column_1 AS ('Computed column ' + column_2),
    column_2 VARCHAR(30) CONSTRAINT default_name DEFAULT 'my column default',
    column_3 ROWVERSION,
    column_4 VARCHAR(40) NULL
);

WITH T2 AS
(
    SELECT 'Computed column ' + column_6 AS column_5, column_6, rowversion_column, column_8
    FROM (
        VALUES ('Explicit value2', 0, 'Explicit value2'),
               ('Explicit value2', 0, 'Explicit value2'),
               ('Explicit value2', 0, NULL),
               (NULL, 0, NULL)
    ) AS T (column_6, rowversion_column, column_8)
)
INSERT INTO #T1 (column_1, column_2, column_3, column_4)
SELECT column_5, column_6, rowversion_column, column_8
FROM T2;

INSERT INTO #T1 (column_2, column_3, column_4)
VALUES ('my column default', DEFAULT, NULL);

SELECT *
FROM #T1;
-- REMORPH CLEANUP: DROP TABLE #T1;
