-- tsql sql:
WITH datetime_values AS (
    SELECT SYSDATETIME() AS sysdatetime,
           SYSDATETIMEOFFSET() AS sysdatetimeoffset,
           SYSUTCDATETIME() AS sysutcdatetime,
           CURRENT_TIMESTAMP AS current_timestamp_value,
           GETDATE() AS getdate,
           GETUTCDATE() AS getutcdatetime
)
SELECT CONVERT(time, sysdatetime) AS converted_sysdatetime,
       CONVERT(time, sysdatetimeoffset) AS converted_sysdatetimeoffset,
       CONVERT(time, sysutcdatetime) AS converted_sysutcdatetime,
       CONVERT(time, current_timestamp_value) AS converted_current_timestamp,
       CONVERT(time, getdate) AS converted_getdate,
       CONVERT(time, getutcdatetime) AS converted_getutcdatetime
FROM datetime_values
