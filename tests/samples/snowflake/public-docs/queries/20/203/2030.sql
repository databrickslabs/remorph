-- see https://docs.snowflake.com/en/sql-reference/functions/st_asewkb

create table geospatial_table (id INTEGER, g GEOGRAPHY);
insert into geospatial_table values
    (1, 'POINT(-122.35 37.55)'), (2, 'LINESTRING(-124.20 42.00, -120.01 41.99)');