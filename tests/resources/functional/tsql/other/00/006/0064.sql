--Query type: DDL
CREATE PROCEDURE get_order_status_sp
AS
BEGIN
    SELECT *
    FROM get_order_status;
END;
EXEC get_order_status_sp;
-- REMORPH CLEANUP: DROP PROCEDURE get_order_status_sp;