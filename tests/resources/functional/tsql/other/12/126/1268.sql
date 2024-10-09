--Query type: DDL
CREATE TABLE #Globally_Unique_Data
(
    GUID UNIQUEIDENTIFIER DEFAULT (NEWSEQUENTIALID()),
    Employee_Name VARCHAR(50)
);

INSERT INTO #Globally_Unique_Data (Employee_Name)
VALUES ('Employee_Name');

ALTER TABLE #Globally_Unique_Data
ADD CONSTRAINT Guid_PK PRIMARY KEY (GUID);

SELECT *
FROM #Globally_Unique_Data;

-- REMORPH CLEANUP: DROP TABLE #Globally_Unique_Data;