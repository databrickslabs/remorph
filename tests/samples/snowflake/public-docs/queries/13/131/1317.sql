-- see https://docs.snowflake.com/en/sql-reference/functions/soundex

SELECT SOUNDEX('I love rock and roll music.'),
       SOUNDEX('I love rocks and gemstones.'),
       SOUNDEX('I leave a rock wherever I go.');