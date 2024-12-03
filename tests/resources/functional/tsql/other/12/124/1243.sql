--Query type: DDL
CREATE TABLE TestTab
(
    PrimaryKey INT PRIMARY KEY,
    CharCol CHAR(10) COLLATE French_CI_AS
);

WITH CTE AS
(
    SELECT *
    FROM (
        VALUES (1, 'abc')
    ) AS TestTab(PrimaryKey, CharCol)
)
SELECT *
FROM CTE
WHERE CharCol LIKE N'abc';
