--Query type: DDL
CREATE PROCEDURE dbo.usp_TPCHDemo
    WITH EXECUTE AS 'SqlUser2'
AS
BEGIN
    SELECT user_name() AS current_username
    FROM (
        VALUES (1),
               (2),
               (3)
    ) AS temp_result(id);

    EXECUTE AS CALLER;

    SELECT user_name() AS current_username
    FROM (
        VALUES (4),
               (5),
               (6)
    ) AS temp_result(id);

    REVERT;

    SELECT user_name() AS current_username
    FROM (
        VALUES (7),
               (8),
               (9)
    ) AS temp_result(id);
END;

EXECUTE dbo.usp_TPCHDemo;
-- REMORPH CLEANUP: DROP PROCEDURE dbo.usp_TPCHDemo;
