-- see https://docs.snowflake.com/en/sql-reference/functions/st_simplify

SELECT ST_NUMPOINTS(geom) AS numpoints_before,
  ST_NUMPOINTS(ST_Simplify(geom, 0.5)) AS numpoints_simplified_05,
  ST_NUMPOINTS(ST_Simplify(geom, 1)) AS numpoints_simplified_1
  FROM
  (SELECT ST_BUFFER(to_geometry('LINESTRING(0 0, 1 1)'), 10) As geom);
