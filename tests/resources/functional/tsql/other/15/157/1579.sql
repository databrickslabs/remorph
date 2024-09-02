--Query type: DML
DECLARE @datetimeoffset datetimeoffset(4) = '1968-10-23 12:45:37.1234 +10:0';
DECLARE @datetime datetime = @datetimeoffset;

SELECT @datetime AS '@datetime', @datetimeoffset AS '@datetimeoffset';

-- Create a temporary result set using a Table Value Constructor (VALUES) subquery
SELECT * FROM (VALUES ('1968-10-23 12:45:37.1234 +10:0')) AS datetimeoffsets(datetimeoffset);

-- REMORPH CLEANUP: DROP TABLE datetimeoffsets;