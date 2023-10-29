-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/logical-functions-greatest-transact-sql?view=azuresqldb-current

CREATE TABLE dbo.Studies (
    VarX VARCHAR(10) NOT NULL,
    Correlation DECIMAL(4, 3) NULL
    );

INSERT INTO dbo.Studies
VALUES ('Var1', 0.2),
    ('Var2', 0.825),
    ('Var3', 0.61);
GO

DECLARE @PredictionA DECIMAL(2, 1) = 0.7;
DECLARE @PredictionB DECIMAL(3, 1) = 0.65;

SELECT VarX,
    Correlation
FROM dbo.Studies
WHERE Correlation > GREATEST(@PredictionA, @PredictionB);
GO