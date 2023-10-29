-- see https://docs.snowflake.com/en/sql-reference/session-variables

SELECT album_title
  FROM albums
  WHERE artist = $VAR_ARTIST_NAME;