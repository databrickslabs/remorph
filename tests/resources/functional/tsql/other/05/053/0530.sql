-- tsql sql:
DECLARE @plan_handle VARBINARY(64) = 0x06000500F443610F003B7CD12C02000001000000000000000000000000000000000000000000000000000000;
WITH temp_result AS (
    SELECT @plan_handle AS plan_handle
)
SELECT plan_handle
FROM temp_result;
DBCC FREEPROCCACHE (@plan_handle);