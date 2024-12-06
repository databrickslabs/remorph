-- tsql sql:
CREATE TABLE #WorkloadGroupConfig
(
    WorkloadGroupName sysname,
    Importance nvarchar(10),
    RequestMaxMemoryGrantPercent tinyint,
    RequestMaxCPUTimeSec smallint
);

INSERT INTO #WorkloadGroupConfig
(
    WorkloadGroupName,
    Importance,
    RequestMaxMemoryGrantPercent,
    RequestMaxCPUTimeSec
)
VALUES
(
    'WGAdmin',
    'MEDIUM',
    20,
    100
);

SELECT *
FROM #WorkloadGroupConfig;

-- REMORPH CLEANUP: DROP TABLE #WorkloadGroupConfig;
