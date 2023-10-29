-- see https://docs.snowflake.com/en/sql-reference/functions/st_distance

SELECT ST_DISTANCE(TO_GEOMETRY('POINT(0 0)'), TO_GEOMETRY('POINT(1 1)')) AS geometry_distance,
       ST_DISTANCE(TO_GEOGRAPHY('POINT(0 0)'), TO_GEOGRAPHY('POINT(1 1)')) AS geography_distance;