-- see https://docs.snowflake.com/en/sql-reference/functions/soundex_p123

SELECT SOUNDEX('Pfister'),
       SOUNDEX_P123('Pfister'),
       SOUNDEX('LLoyd'),
       SOUNDEX_P123('Lloyd');