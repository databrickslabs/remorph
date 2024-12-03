--Query type: DML
DECLARE @date DATETIME = '2022-01-01';
DECLARE @time TIME = '12:00:00';

SELECT @date AS [date], @time AS [time],
       CAST(@date AS DATETIME2) AS [datetime2],
       CAST(@date AS DATETIMEOFFSET) AS [datetimeoffset],
       CAST(@date AS SMALLDATETIME) AS [smalldatetime];

-- Create a temporary result set using a Table Value Constructor (VALUES) subquery
SELECT * FROM (VALUES ('2022-01-01', '12:00:00'), ('2022-01-02', '13:00:00')) AS dates ([date], [time]);
