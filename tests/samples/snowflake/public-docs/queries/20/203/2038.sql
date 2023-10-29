-- see https://docs.snowflake.com/en/sql-reference/functions/st_dimension

create table geospatial_table_02 (id INTEGER, g GEOGRAPHY);
insert into geospatial_table_02 values
    (1, 'POINT(-122.35 37.55)'),
    (2, 'MULTIPOINT((-122.35 37.55), (0.00 -90.0))'),
    (3, 'LINESTRING(-124.20 42.00, -120.01 41.99)'),
    (4, 'LINESTRING(-124.20 42.00, -120.01 41.99, -122.5 42.01)'),
    (5, 'MULTILINESTRING((-124.20 42.00, -120.01 41.99, -122.5 42.01), (10.0 0.0, 20.0 10.0, 30.0 0.0))'),
    (6, 'POLYGON((-124.20 42.00, -120.01 41.99, -121.1 42.01, -124.20 42.00))'),
    (7, 'MULTIPOLYGON(((-124.20 42.00, -120.01 41.99, -121.1 42.01, -124.20 42.0)), ((20.0 20.0, 40.0 20.0, 40.0 40.0, 20.0 40.0, 20.0 20.0)))')
    ;