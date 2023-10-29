-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/approx-percentile-disc-transact-sql?view=sql-server-ver16

SET NOCOUNT ON
GO
DROP TABLE IF EXISTS tblEmployee
GO
CREATE TABLE tblEmployee (
EmplId INT IDENTITY(1,1) PRIMARY KEY CLUSTERED,
DeptId INT,
Salary int);
GO
INSERT INTO tblEmployee
VALUES (1, 31),(1, 33), (1, 18), (2, 25),(2, 35),(2, 10), (2, 10),(3,1), (3,NULL), (4,NULL), (4,NULL)
GO
SELECT DeptId,
APPROX_PERCENTILE_DISC(0.10) WITHIN GROUP(ORDER BY Salary) AS 'P10',
APPROX_PERCENTILE_DISC(0.90) WITHIN GROUP(ORDER BY Salary) AS 'P90'
FROM tblEmployee
GROUP BY DeptId