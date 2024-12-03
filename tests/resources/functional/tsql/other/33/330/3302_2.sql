--Query type: DML
DECLARE @A TABLE (PostalCode VARCHAR(5), City VARCHAR(50));
INSERT INTO @A (PostalCode, City)
VALUES ('12345', 'New York'), ('67890', 'Los Angeles');
UPDATE @A
SET PostalCode = '99999'
WHERE PostalCode = '12345';
SELECT * FROM @A;
