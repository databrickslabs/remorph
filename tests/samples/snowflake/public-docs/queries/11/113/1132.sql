-- see https://docs.snowflake.com/en/sql-reference/functions/st_azimuth

SELECT DEGREES(ST_AZIMUTH(
    TO_GEOGRAPHY('POINT(0 1)'),
    TO_GEOGRAPHY('POINT(1 2)')
));