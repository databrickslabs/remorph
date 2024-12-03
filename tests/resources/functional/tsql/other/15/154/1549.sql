--Query type: DML
DECLARE @d3 DATE, @dt3 DATETIME, @dt4 DATETIME2;
SET @d3 = '1999-12-31';
SET @dt4 = CAST(@d3 AS DATETIME2);
SET @dt3 = CAST(@d3 AS DATETIME);
WITH DateValues AS (
    SELECT @d3 AS DateValue, CAST(@d3 AS DATETIME) AS DateTimeValue, CAST(@d3 AS DATETIME2) AS DateTime2Value
)
SELECT * FROM DateValues;
