-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/string-comparison-assignment?view=sql-server-ver16

CREATE TABLE #tmp (c1 VARCHAR(10));
GO

INSERT INTO #tmp VALUES ('abc ');

INSERT INTO #tmp VALUES ('abc');
GO

SELECT DATALENGTH(c1) AS 'EqualWithSpace', * FROM #tmp
WHERE c1 = 'abc ';

SELECT DATALENGTH(c1) AS 'EqualNoSpace  ', * FROM #tmp
WHERE c1 = 'abc';

SELECT DATALENGTH(c1) AS 'GTWithSpace   ', * FROM #tmp
WHERE c1 > 'ab ';

SELECT DATALENGTH(c1) AS 'GTNoSpace     ', * FROM #tmp
WHERE c1 > 'ab';

SELECT DATALENGTH(c1) AS 'LTWithSpace   ', * FROM #tmp
WHERE c1 < 'abd ';

SELECT DATALENGTH(c1) AS 'LTNoSpace     ', * FROM #tmp
WHERE c1 < 'abd';

SELECT DATALENGTH(c1) AS 'LikeWithSpace ', * FROM #tmp
WHERE c1 LIKE 'abc %';

SELECT DATALENGTH(c1) AS 'LikeNoSpace   ', * FROM #tmp
WHERE c1 LIKE 'abc%';
GO

DROP TABLE #tmp;
GO