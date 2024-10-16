--Query type: DCL
SET QUOTED_IDENTIFIER ON;
SELECT [Customer Name]
FROM (
    VALUES ('John Doe'), ('Jane Doe')
) AS Customers ([Customer Name]);