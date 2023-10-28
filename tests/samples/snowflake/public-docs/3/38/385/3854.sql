create or replace view view_musicians_in_bands AS
  select distinct musicians.musician_id, musician_name, band_name
    from musicians inner join musicians_and_albums inner join music_albums inner join music_bands
    where musicians.musician_ID = musicians_and_albums.musician_ID
      and musicians_and_albums.album_ID = music_albums.album_ID
      and music_albums.band_ID = music_bands.band_ID;