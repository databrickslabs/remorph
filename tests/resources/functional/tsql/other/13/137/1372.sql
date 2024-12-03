--Query type: DDL
CREATE TABLE WorkloadClassifiers
(
    ClassifierName nvarchar(255),
    WorkloadGroup nvarchar(255),
    MemberName nvarchar(255),
    StartTime time,
    EndTime time
);

INSERT INTO WorkloadClassifiers
(
    ClassifierName,
    WorkloadGroup,
    MemberName,
    StartTime,
    EndTime
)
VALUES
(
    'wcReportingLoads',
    'wgReporting',
    'ReportingRole',
    '08:00',
    '18:00'
);

SELECT *
FROM WorkloadClassifiers;

-- REMORPH CLEANUP: DROP TABLE WorkloadClassifiers;
