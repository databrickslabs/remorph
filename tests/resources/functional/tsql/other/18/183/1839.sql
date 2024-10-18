--Query type: DML
DECLARE @mynewvar CHAR(20);
SET @mynewvar = 'This is another test';
SELECT *
FROM (
    VALUES (@mynewvar)
) AS mycte(myvalue);