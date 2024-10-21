--Query type: DCL
DECLARE @Rate DECIMAL(10, 2);
SET @Rate = 10.50;
SELECT Rate
FROM (
    VALUES (@Rate)
) AS RateCTE (Rate);