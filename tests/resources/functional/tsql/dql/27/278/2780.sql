-- tsql sql:
SELECT SUSER_SNAME(SID) FROM (VALUES (SUSER_SID('TestComputer\User', 0))) AS SID_CTE(SID);