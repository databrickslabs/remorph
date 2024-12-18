-- tsql sql:
WITH dates AS (
    SELECT
        SYSDATETIME() AS sysdatetime,
        SYSDATETIMEOFFSET() AS sysdatetimeoffset,
        SYSUTCDATETIME() AS sysutcdatetime,
        GETDATE() AS getdate,
        GETUTCDATE() AS getutcdatetime,
        CURRENT_TIMESTAMP AS current_timestamp_value
)
SELECT
    'SYSDATETIME()      ',
    sysdatetime,
    'SYSDATETIMEOFFSET()',
    sysdatetimeoffset,
    'SYSUTCDATETIME()   ',
    sysutcdatetime,
    'CURRENT_TIMESTAMP  ',
    current_timestamp_value,
    'GETDATE()          ',
    getdate,
    'GETUTCDATE()       ',
    getutcdatetime
FROM dates
