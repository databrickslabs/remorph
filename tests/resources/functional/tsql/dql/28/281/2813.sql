-- tsql sql:
SELECT TOP (1) '2010-07-25T13:50:38.544' AS OriginalText, CAST('2010-07-25T13:50:38.544' AS DATETIME) AS UsingCastFunction, CONVERT(DATETIME, '2010-07-25T13:50:38.544', 126) AS UsingConvertFunctionFrom_ISO8601 FROM (VALUES ('2010-07-25T13:50:38.544')) AS Customer (SalesDate);