-- tsql sql:
WITH temp_result AS (SELECT @@SPID AS ID, @@SPID AS [Control ID], SYSTEM_USER AS [Login Name], USER AS [User Name]) SELECT ID, [Control ID], [Login Name], [User Name] FROM temp_result
