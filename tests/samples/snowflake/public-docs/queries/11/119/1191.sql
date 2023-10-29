-- see https://docs.snowflake.com/en/sql-reference/functions/h3_point_to_cell_string

SELECT H3_POINT_TO_CELL_STRING(ST_POINT(13.377704, 52.516262), 18);