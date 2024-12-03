--Query type: DQL
WITH datetime_values AS (
    SELECT SYSDATETIME() AS sysdatetime,
           SYSDATETIMEOFFSET() AS sysdatetimeoffset,
           SYSUTCDATETIME() AS sysutcdatetime,
           CURRENT_TIMESTAMP AS [current_timestamp],
           GETDATE() AS getdate,
           GETUTCDATE() AS getutcdatetime
)
SELECT CONVERT(time, sysdatetime) AS [SYSDATETIME()],
       CONVERT(time, sysdatetimeoffset) AS [SYSDATETIMEOFFSET()],
       CONVERT(time, sysutcdatetime) AS [SYSUTCDATETIME()],
       CONVERT(time, [current_timestamp]) AS [CURRENT_TIMESTAMP],
       CONVERT(time, getdate) AS [GETDATE()],
       CONVERT(time, getutcdatetime) AS [GETUTCDATE()]
FROM datetime_values;
