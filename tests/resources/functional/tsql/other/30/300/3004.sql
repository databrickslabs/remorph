--Query type: DML
WITH DateValues AS (SELECT '12/31/2022' AS DateValue UNION ALL SELECT '01/01/2023' AS DateValue) SELECT TRY_CAST(DateValue AS DATETIME2) AS Result FROM DateValues;
