-- see https://docs.snowflake.com/en/sql-reference/functions/get_ddl

create view view_t1
    -- GET_DDL() removes this comment.
    AS
    select * from t1;