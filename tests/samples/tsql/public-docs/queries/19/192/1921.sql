-- see https://learn.microsoft.com/en-us/sql/t-sql/data-types/nondeterministic-convert-date-literals?view=sql-server-ver16

DECLARE @yourDateString NVARCHAR(10) = '12-09-2018';
PRINT @yourDateString + '  = the input.';

SET DATEFORMAT dmy;
SELECT CONVERT(DATE, @yourDateString) AS [DMY-Interpretation-of-input-format];

SET DATEFORMAT mdy;
SELECT CONVERT(DATE, @yourDateString) AS [MDY-Interpretation-of-input-format];

SET DATEFORMAT ymd;
SELECT CONVERT(DATE, @yourDateString) AS [YMD-Interpretation--?--NotGuaranteed];


/***  Actual output:
12-09-2018  = the input.

DMY-Interpretation-of-input-format
2018-09-12

MDY-Interpretation-of-input-format
2018-12-09

YMD-Interpretation--?--NotGuaranteed
2018-12-09
***/