--Query type: DML
CREATE PROCEDURE get_current_date_and_database_id
AS
BEGIN
    WITH current_info AS (
        SELECT GETDATE() AS [current_date],
               DB_ID() AS database_id
    )
    SELECT *
    FROM current_info;
END;
EXEC get_current_date_and_database_id;