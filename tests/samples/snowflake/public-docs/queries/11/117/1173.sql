-- see https://docs.snowflake.com/en/sql-reference/functions/h3_coverage_strings

SELECT H3_COVERAGE_STRINGS(
  TO_GEGGRAPHY(
    'POLYGON((-122.481889 37.826683,-122.479487 37.808548,-122.474150 37.808904,-122.476510 37.826935,-122.481889 37.826683))'),
  8) AS set_of_h3_cells_covering_polygon;