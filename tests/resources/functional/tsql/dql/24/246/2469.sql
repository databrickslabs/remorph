--Query type: DQL
WITH DateValues AS (
    SELECT CONVERT(date, SYSDATETIME()) AS DateValue1,
           CONVERT(date, CURRENT_TIMESTAMP) AS DateValue2,
           CONVERT(date, GETDATE()) AS DateValue3
)
SELECT DateValue1,
       DateValue2,
       DateValue3
FROM DateValues
