SELECT DepartmentNumber,
    DepartmentName,
    ManagerID,
    ParentDepartmentNumber
FROM DEPARTMENT
FOR SYSTEM_TIME BETWEEN '2013-01-01' AND '2014-01-01'
WHERE ManagerID = 5;