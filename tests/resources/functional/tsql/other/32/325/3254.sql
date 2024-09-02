--Query type: DDL
CREATE PROCEDURE NotifyALTER_T2_Proc
AS
BEGIN
    SELECT *
    FROM (
        VALUES ('NotifyService2', '123e4567-e89b-12d3-a456-426614174000')
    ) AS temp(service_name, service_id);
END;
EXEC NotifyALTER_T2_Proc;
-- REMORPH CLEANUP: DROP PROCEDURE NotifyALTER_T2_Proc;