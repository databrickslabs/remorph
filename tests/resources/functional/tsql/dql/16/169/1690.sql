-- tsql sql:
DECLARE @geom geometry = 'CIRCULARSTRING(2 2, 2 2, 2 2);
SELECT @geom.MakeValid().ToString();
