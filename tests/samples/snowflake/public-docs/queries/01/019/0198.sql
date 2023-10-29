-- see https://docs.snowflake.com/en/sql-reference/sql/delete

BEGIN WORK;
DELETE FROM leased_bicycles 
    USING returned_bicycles
    WHERE leased_bicycles.bicycle_ID = returned_bicycles.bicycle_ID;
TRUNCATE TABLE returned_bicycles;
COMMIT WORK;