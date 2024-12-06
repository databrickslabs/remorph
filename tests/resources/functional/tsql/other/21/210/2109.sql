-- tsql sql:
WITH TempResult AS ( SELECT 'dummy' AS dummy_value )
SELECT *
FROM TempResult;

GRANT CREATE TABLE TO [john@tpc.com];

GRANT ALTER ON SCHEMA::SALES TO [john@tpc.com];
