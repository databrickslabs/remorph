-- tsql sql:
CREATE PROCEDURE uspSupplierAllInfo
    @PartName VARCHAR(25)
AS
BEGIN
    SET NOCOUNT ON;

    WITH Supplier AS (
        SELECT S_SUPPKEY, S_NAME, S_CREDITRATING, S_ACTIVEFLAG
        FROM (
            VALUES (1, 'Supplier 1', 1, 1),
                   (2, 'Supplier 2', 2, 0),
                   (3, 'Supplier 3', 3, 1)
        ) AS s (S_SUPPKEY, S_NAME, S_CREDITRATING, S_ACTIVEFLAG)
    ),
    PartSupp AS (
        SELECT PS_SUPPKEY, PS_PARTKEY
        FROM (
            VALUES (1, 1),
                   (2, 2),
                   (3, 3)
        ) AS ps (PS_SUPPKEY, PS_PARTKEY)
    ),
    Part AS (
        SELECT P_PARTKEY, P_NAME
        FROM (
            VALUES (1, 'Part 1'),
                   (2, 'Part 2'),
                   (3, 'Part 3')
        ) AS p (P_PARTKEY, P_NAME)
    )
    SELECT LEFT(s.S_NAME, 25) AS Supplier,
           LEFT(p.P_NAME, 25) AS 'Part name',
           'Rating' = CASE s.S_CREDITRATING
                           WHEN 1 THEN 'Superior'
                           WHEN 2 THEN 'Excellent'
                           WHEN 3 THEN 'Above average'
                           WHEN 4 THEN 'Average'
                           WHEN 5 THEN 'Below average'
                           ELSE 'No rating'
                       END,
           Availability = CASE s.S_ACTIVEFLAG
                               WHEN 1 THEN 'Yes'
                               ELSE 'No'
                           END
    FROM Supplier s
    INNER JOIN PartSupp ps ON s.S_SUPPKEY = ps.PS_SUPPKEY
    INNER JOIN Part p ON ps.PS_PARTKEY = p.P_PARTKEY
    WHERE p.P_NAME LIKE @PartName
    ORDER BY s.S_NAME ASC;
END;
EXEC uspSupplierAllInfo 'Part%';
