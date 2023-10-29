-- see https://docs.snowflake.com/en/sql-reference/constructs/with

with
  album_IDs_by_bands as (select album_ID, music_bands.band_id, band_name
                          from music_albums inner join music_bands
                          where music_albums.band_id = music_bands.band_ID),
  musicians_in_bands as (select distinct musicians.musician_id, musician_name, band_name
                          from musicians inner join musicians_and_albums inner join album_IDs_by_bands
                          where musicians.musician_ID = musicians_and_albums.musician_ID
                            and musicians_and_albums.album_ID = album_IDS_by_bands.album_ID)
select musician_ID, musician_name from musicians_in_bands where band_name = 'Santana'
intersect
select musician_ID, musician_name from musicians_in_bands where band_name = 'Journey'
order by musician_ID
  ;