SELECT DeptID,
    DeptName,
    DeptMgrID,
    EmpID,
    EmpLastName,
    EmpSalary
FROM Departments d
CROSS APPLY dbo.GetReports(d.DeptMgrID);