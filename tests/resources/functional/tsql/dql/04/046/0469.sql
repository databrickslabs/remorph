--Query type: DQL
WITH temp_result AS (
    SELECT 'Bearing Ball' AS cs_Pname, 'Bearing Ball' AS Name
    UNION ALL
    SELECT 'Bearing Ball 2', 'Bearing Ball 2'
)
SELECT *
FROM temp_result
WHERE CHECKSUM(N'Bearing Ball 3') = cs_Pname
    AND Name = N'Bearing Ball 3';