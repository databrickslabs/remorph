--Query type: DQL
WITH DateValues AS (
    SELECT CONVERT(date, SYSDATETIME()) AS DateValue1,
           CONVERT(date, SYSDATETIMEOFFSET()) AS DateValue2,
           CONVERT(date, SYSUTCDATETIME()) AS DateValue3,
           CONVERT(date, CURRENT_TIMESTAMP) AS DateValue4,
           CONVERT(date, GETDATE()) AS DateValue5,
           CONVERT(date, GETUTCDATE()) AS DateValue6
)
SELECT DateValue1, DateValue2, DateValue3, DateValue4, DateValue5, DateValue6
FROM DateValues