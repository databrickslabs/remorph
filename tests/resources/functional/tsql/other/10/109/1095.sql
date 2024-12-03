--Query type: DDL
CREATE PROCEDURE dbo.uspNationCursor
    @NationCursor CURSOR VARYING OUTPUT
AS
    SET NOCOUNT ON;
    SET @NationCursor = CURSOR FORWARD_ONLY STATIC FOR
      SELECT n_nationkey, n_name
      FROM (VALUES (1, 'USA'), (2, 'Canada'), (3, 'Mexico')) AS n (n_nationkey, n_name);
    OPEN @NationCursor;
-- REMORPH CLEANUP: DROP PROCEDURE dbo.uspNationCursor;
