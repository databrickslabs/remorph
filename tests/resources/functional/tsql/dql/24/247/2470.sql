--Query type: DQL
WITH cte AS (
    SELECT
        SYSDATETIME() AS sysdatetime,
        SYSDATETIMEOFFSET() AS sysdatetimeoffset,
        SYSUTCDATETIME() AS sysutcdatetime,
        CURRENT_TIMESTAMP AS current_timestamp_value,
        GETDATE() AS getdate,
        GETUTCDATE() AS getutcdatetime
)
SELECT
    CONVERT(date, sysdatetime) AS converted_sysdatetime,
    CONVERT(date, sysdatetimeoffset) AS converted_sysdatetimeoffset,
    CONVERT(date, sysutcdatetime) AS converted_sysutcdatetime,
    CONVERT(date, current_timestamp_value) AS converted_current_timestamp,
    CONVERT(date, getdate) AS converted_getdate,
    CONVERT(date, getutcdatetime) AS converted_getutcdatetime
FROM cte
