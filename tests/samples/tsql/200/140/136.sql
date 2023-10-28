SELECT DepartmentNumber,
    DepartmentName,
    ManagerID,
    ParentDepartmentNumber
FROM DEPARTMENT
FOR SYSTEM_TIME AS OF '2014-01-01'
WHERE ManagerID = 5;