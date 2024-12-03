--Query type: DQL
WITH DateCTE AS ( SELECT CAST('2022-01-01' AS DATE) AS DateValue ) SELECT DATEPART(year, DateValue), DATEPART(month, DateValue), DATEPART(day, DateValue) FROM DateCTE
