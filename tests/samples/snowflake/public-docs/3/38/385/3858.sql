create or replace view view_musicians_in_bands AS
 select distinct musicians.musician_id, musician_name, band_name
  from musicians inner join musicians_and_albums inner join view_album_IDs_by_bands
  where musicians.musician_ID = musicians_and_albums.musician_ID
    and musicians_and_albums.album_ID = view_album_IDS_by_bands.album_ID;