-- tsql sql:
WITH temp_result AS ( SELECT DATABASEPROPERTYEX('clone_database_name', 'IsVerifiedClone') AS is_verified_clone ) SELECT is_verified_clone FROM temp_result
