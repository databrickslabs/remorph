-- tsql sql:
CREATE TABLE #EmployeeSales
(
    EmployeeID INT,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    YearlySales DECIMAL(10, 2)
);

WITH SalesPersonCTE AS
(
    SELECT
        s_businessentityid,
        s_lastname,
        s_firstname,
        s_salesytd
    FROM
    (
        VALUES
        (
            1,
            'Smith',
            'John',
            300000.00
        ),
        (
            2,
            'Johnson',
            'Mike',
            250000.00
        ),
        (
            3,
            'Williams',
            'Emma',
            200000.00
        ),
        (
            4,
            'Jones',
            'David',
            150000.00
        ),
        (
            5,
            'Brown',
            'Sophia',
            100000.00
        )
    ) AS SalesPerson (s_businessentityid, s_lastname, s_firstname, s_salesytd)
),
CustomerCTE AS
(
    SELECT
        c_businessentityid,
        c_lastname,
        c_firstname
    FROM
    (
        VALUES
        (
            1,
            'Smith',
            'John'
        ),
        (
            2,
            'Johnson',
            'Mike'
        ),
        (
            3,
            'Williams',
            'Emma'
        ),
        (
            4,
            'Jones',
            'David'
        ),
        (
            5,
            'Brown',
            'Sophia'
        )
    ) AS Customer (c_businessentityid, c_lastname, c_firstname)
)
INSERT INTO #EmployeeSales
OUTPUT inserted.EmployeeID, inserted.FirstName, inserted.LastName, inserted.YearlySales
SELECT
    sp.s_businessentityid,
    c.c_firstname,
    c.c_lastname,
    sp.s_salesytd
FROM
    SalesPersonCTE sp
INNER JOIN CustomerCTE c ON sp.s_businessentityid = c.c_businessentityid
WHERE
    sp.s_salesytd > 250000.00
ORDER BY
    sp.s_salesytd DESC;

SELECT * FROM #EmployeeSales;
-- REMORPH CLEANUP: DROP TABLE #EmployeeSales;
