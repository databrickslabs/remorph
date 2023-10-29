-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql?view=sql-server-ver16

SELECT DeptID,
    DeptName,
    DeptMgrID,
    EmpID,
    EmpLastName,
    EmpSalary
FROM Departments d
CROSS APPLY dbo.GetReports(d.DeptMgrID);