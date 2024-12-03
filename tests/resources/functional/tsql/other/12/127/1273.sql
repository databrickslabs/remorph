--Query type: DDL
CREATE TABLE Marketing.Territory
(
    TerritoryID INT,
    TerritoryName VARCHAR(50)
);

INSERT INTO Marketing.Territory
(
    TerritoryID,
    TerritoryName
)
SELECT TerritoryID, TerritoryName
FROM (
    VALUES
    (
        1,
        'Territory1'
    ),
    (
        2,
        'Territory2'
    )
) AS Territory
(
    TerritoryID,
    TerritoryName
);

SELECT *
FROM Marketing.Territory;

-- REMORPH CLEANUP: DROP TABLE Marketing.Territory;
