DECLARE @AsOfFrom DATETIME2 = DATEADD(month, -12, SYSUTCDATETIME());
DECLARE @AsOfTo DATETIME2 = DATEADD(month, -6, SYSUTCDATETIME());

SELECT DepartmentNumber,
    DepartmentName,
    ManagerID,
    ParentDepartmentNumber
FROM DEPARTMENT
FOR SYSTEM_TIME
FROM @AsOfFrom TO @AsOfTo
WHERE ManagerID = 5;