-- see https://docs.snowflake.com/en/sql-reference/functions/h3_polygon_to_cells_strings

SELECT H3_POLYGON_TO_CELLS_STRINGS(
  TO_GEOGRAPHY(
    'POLYGON((-122.481889 37.826683,-122.479487 37.808548,-122.474150 37.808904,-122.476510 37.826935,-122.481889 37.826683))'),
  9) AS h3_cells_in_polygon;