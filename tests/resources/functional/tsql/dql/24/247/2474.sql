--Query type: DQL
WITH cte AS (
    SELECT SYSDATETIME() AS sysdt, CURRENT_TIMESTAMP AS ct, GETDATE() AS gd
)
SELECT CONVERT(time, sysdt) AS time_sysdt, CONVERT(time, ct) AS time_ct, CONVERT(time, gd) AS time_gd
FROM cte
