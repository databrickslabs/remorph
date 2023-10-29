-- see https://docs.snowflake.com/en/sql-reference/functions/st_asewkt

CREATE OR REPLACE TABLE geometry_table (g GEOMETRY);
INSERT INTO geometry_table VALUES
  ('SRID=4326;POINT(-122.35 37.55)'),
  ('SRID=0;LINESTRING(0.75 0.75, -10 20)');

ALTER SESSION SET GEOMETRY_OUTPUT_FORMAT='EWKT';
SELECT ST_ASEWKT(g) FROM geometry_table;