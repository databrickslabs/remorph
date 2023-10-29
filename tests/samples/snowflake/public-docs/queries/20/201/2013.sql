-- see https://docs.snowflake.com/en/sql-reference/constructs/with

create or replace view view_album_IDs_by_bands AS
 select album_ID, music_bands.band_id, band_name
  from music_albums inner join music_bands
  where music_albums.band_id = music_bands.band_ID;