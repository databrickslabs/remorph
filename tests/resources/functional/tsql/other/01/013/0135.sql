-- tsql sql:
DECLARE @datefirst INT = (SELECT datefirst FROM (VALUES (7)) AS options(datefirst));
SET DATEFIRST @datefirst;
