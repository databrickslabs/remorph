--Query type: DQL
WITH DateValues AS (
    SELECT CONVERT(DATE, '2022-01-01') AS OrderDate
)
SELECT CONVERT(DATE, OrderDate) AS OrderDateConverted
FROM DateValues;
