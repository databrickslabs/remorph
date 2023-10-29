-- see https://docs.snowflake.com/en/sql-reference/functions/st_makeline

SELECT ST_MAKELINE(
                   TO_GEOGRAPHY('POINT(37.0 45.0)'),
                   TO_GEOGRAPHY('POINT(38.5 46.5)')
                  ) AS line_between_two_points;