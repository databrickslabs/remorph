-- see https://docs.snowflake.com/en/sql-reference/functions/st_makeline

SELECT ST_MAKELINE(
                   TO_GEOGRAPHY('MULTIPOINT((-122.32328 37.561801), (-122.325879 37.586852))'),
                   TO_GEOGRAPHY('LINESTRING(-122.306067 37.55412, -122.496691 37.495627)')
                  ) AS line_between_multipoint_and_linestring;