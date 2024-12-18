-- tsql sql:
SELECT name, ISNUMERIC(name) AS IsNameANumber, database_id, ISNUMERIC(database_id) AS IsIdANumber FROM (VALUES ('database1', 1), ('database2', 2), ('database3', 3)) AS databases (name, database_id);
