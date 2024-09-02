--Query type: DCL
CREATE TABLE #CustomerCTE
(
    CustomerID INT,
    CustomerName VARCHAR(255)
);

INSERT INTO #CustomerCTE
(
    CustomerID,
    CustomerName
)
VALUES
(
    1,
    'John Doe'
),
(
    2,
    'Jane Doe'
);

SELECT
    CASE
        WHEN HAS_PERMS_BY_NAME('#CustomerCTE', 'OBJECT', 'INSERT') = 1
        THEN 'INSERT on #CustomerCTE is grantable.'
        ELSE 'You may not GRANT INSERT permissions on #CustomerCTE.'
    END AS PermissionStatus;

SELECT
    *
FROM
    #CustomerCTE;

-- REMORPH CLEANUP: DROP TABLE #CustomerCTE;