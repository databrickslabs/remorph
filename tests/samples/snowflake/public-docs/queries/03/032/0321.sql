-- see https://docs.snowflake.com/en/sql-reference/functions/st_aswkb

CREATE OR REPLACE TABLE geometry_table (g GEOMETRY);
INSERT INTO geometry_table VALUES
  ('POINT(-122.35 37.55)'), ('LINESTRING(0.75 0.75, -10 20)');

SELECT ST_ASWKB(g) FROM geometry_table;