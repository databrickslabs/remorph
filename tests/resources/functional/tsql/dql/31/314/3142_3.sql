--Query type: DQL
WITH CustomerCTE AS (
    SELECT 'Smith' AS CLastName, 'John' AS CFirstName, 'Salesman' AS CJobTitle
    UNION ALL
    SELECT 'Johnson' AS CLastName, 'Mike' AS CFirstName, 'Salesman' AS CJobTitle
),
OrdersCTE AS (
    SELECT 'Smith' AS OLastName, 'John' AS OFirstName, 'Clerk' AS OJobTitle
    UNION
    SELECT 'Williams' AS OLastName, 'David' AS OFirstName, 'Clerk' AS OJobTitle
)
SELECT CLastName, CFirstName, CJobTitle
FROM CustomerCTE
UNION ALL
(
    SELECT OLastName, OFirstName, OJobTitle
    FROM OrdersCTE
    UNION
    SELECT 'Jones' AS NLastName, 'Mary' AS NFirstName, 'Manager' AS NJobTitle
    FROM (
        VALUES ('Jones', 'Mary', 'Manager')
    ) AS NamesTable(NLastName, NFirstName, NJobTitle)
)