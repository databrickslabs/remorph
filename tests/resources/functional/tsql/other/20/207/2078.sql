-- tsql sql:
EXEC sp_executesql N'SELECT * FROM (VALUES (1, ''Form1''), (2, ''Form2'')) AS FormLocks (FormId, FormName);'
