-- see https://docs.snowflake.com/en/sql-reference/functions/st_y

SELECT
    ST_X(ST_MAKEPOINT(NULL, NULL)), ST_X(NULL),
    ST_Y(ST_MAKEPOINT(NULL, NULL)), ST_Y(NULL)
    ;