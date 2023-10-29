-- see https://learn.microsoft.com/en-us/sql/t-sql/language-elements/declare-local-variable-transact-sql?view=sql-server-ver16

DECLARE @MyTableVar TABLE (
    EmpID INT NOT NULL,
    PRIMARY KEY CLUSTERED (EmpID),
    UNIQUE NONCLUSTERED (EmpID),
    INDEX CustomNonClusteredIndex NONCLUSTERED (EmpID)
);
GO