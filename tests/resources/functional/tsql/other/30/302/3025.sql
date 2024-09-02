--Query type: DCL
SET QUOTED_IDENTIFIER OFF;
SELECT *
FROM (
    VALUES ('Customer', 1),
           ('Supplier', 2)
) AS CustomerType (
    Type,
    ID
);