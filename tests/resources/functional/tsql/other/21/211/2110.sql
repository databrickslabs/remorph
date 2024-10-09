--Query type: DCL
CREATE ROLE SalesTeam;
GO
CREATE VIEW temp_result
AS
    SELECT *
    FROM (
        VALUES (1)
    ) AS temp;
GO
GRANT SELECT ON temp_result TO SalesTeam;
GO
SELECT *
FROM temp_result;