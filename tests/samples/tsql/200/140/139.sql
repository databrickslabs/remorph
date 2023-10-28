SELECT DepartmentNumber,
    DepartmentName,
    ManagerID,
    ParentDepartmentNumber
FROM DEPARTMENT
FOR SYSTEM_TIME CONTAINED IN ('2013-01-01', '2014-01-01')
WHERE ManagerID = 5;