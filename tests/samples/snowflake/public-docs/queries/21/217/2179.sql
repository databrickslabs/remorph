-- see https://docs.snowflake.com/en/sql-reference/functions/st_geographyfromwkt

select ST_GEOGRAPHYFROMEWKT('SRID=4326;POINT(-122.35 37.55)');