--Query type: DCL
WITH TempResult AS (
    SELECT 'WanidaBenshoof' AS UserName, 'AdvWorks\YoonM' AS Grantor
    UNION ALL
    SELECT 'AnotherUser', 'AnotherGrantor'
)
SELECT *
FROM TempResult;