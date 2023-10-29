-- see https://docs.snowflake.com/en/sql-reference/functions/h3_point_to_cell

SELECT H3_POINT_TO_CELL(ST_POINT(13.377704, 52.516262), 18);