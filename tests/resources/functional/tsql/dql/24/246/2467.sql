--Query type: DQL
WITH DateValues AS (
    SELECT
        CONVERT(DATE, SYSDATETIME()) AS DateValue1,
        CONVERT(DATE, SYSDATETIMEOFFSET()) AS DateValue2,
        CONVERT(DATE, SYSUTCDATETIME()) AS DateValue3,
        CONVERT(DATE, CURRENT_TIMESTAMP) AS DateValue4,
        CONVERT(DATE, GETDATE()) AS DateValue5,
        CONVERT(DATE, GETUTCDATE()) AS DateValue6
)
SELECT
    DateValue1,
    DateValue2,
    DateValue3,
    DateValue4,
    DateValue5,
    DateValue6
FROM DateValues