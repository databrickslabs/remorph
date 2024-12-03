--Query type: DML
DECLARE @dateFrom DATE = '2022-01-01';
DECLARE @dateTo DATE = '2022-01-31';

SELECT @dateFrom AS [date], @dateTo AS [date]
FROM (
    VALUES (@dateFrom, @dateTo)
) AS temp_result_set (dateFrom, dateTo);
