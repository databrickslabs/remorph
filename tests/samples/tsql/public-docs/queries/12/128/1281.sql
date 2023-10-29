-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/logical-functions-least-transact-sql?view=azuresqldb-current

CREATE TABLE dbo.Studies (
    VarX VARCHAR(10) NOT NULL,
    Correlation DECIMAL(4, 3) NULL
    );

INSERT INTO dbo.Studies
VALUES ('Var1', 0.2),
    ('Var2', 0.825),
    ('Var3', 0.61);
GO

DECLARE @VarX DECIMAL(4, 3) = 0.59;

SELECT VarX,
    Correlation,
    LEAST(Correlation, 1.0, @VarX) AS LeastVar
FROM dbo.Studies;
GO