-- tsql sql:
CREATE TABLE #myNewTable
(
    id INT,
    lastName VARCHAR(50),
    zipCode VARCHAR(10)
);

INSERT INTO #myNewTable
(
    id,
    lastName,
    zipCode
)
VALUES
(
    1,
    'Doe',
    '12345'
),
(
    2,
    'Smith',
    '67890'
);

SELECT *
FROM #myNewTable;

-- REMORPH CLEANUP: DROP TABLE #myNewTable;
