SELECT DepartmentNumber,
    DepartmentName,
    ManagerID,
    ParentDepartmentNumber
FROM DEPARTMENT
FOR SYSTEM_TIME FROM '2013-01-01' TO '2014-01-01'
WHERE ManagerID = 5;