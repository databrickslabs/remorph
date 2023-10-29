-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/concat-transact-sql?view=sql-server-ver16

CREATE TABLE #temp (
    emp_name NVARCHAR(200) NOT NULL,
    emp_middlename NVARCHAR(200) NULL,
    emp_lastname NVARCHAR(200) NOT NULL
    );

INSERT INTO #temp
VALUES ('Name', NULL, 'Lastname');

SELECT CONCAT (emp_name, emp_middlename, emp_lastname) AS Result
FROM #temp;