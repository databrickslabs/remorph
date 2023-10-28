SELECT DeptID,
    DeptName,
    DeptMgrID,
    EmpID,
    EmpLastName,
    EmpSalary
FROM Departments d
OUTER APPLY dbo.GetReports(d.DeptMgrID);