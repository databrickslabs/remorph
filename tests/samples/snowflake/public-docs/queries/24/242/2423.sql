-- see https://docs.snowflake.com/en/sql-reference/constructs/with

with
  albums_1976 as (select * from music_albums where album_year = 1976)
select album_name from albums_1976 order by album_name;