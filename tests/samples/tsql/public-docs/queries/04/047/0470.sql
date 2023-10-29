-- see https://learn.microsoft.com/en-us/sql/t-sql/functions/char-transact-sql?view=sql-server-ver16

; WITH uni(c) AS (
    -- BMP character
    SELECT NCHAR(9835)
    UNION ALL
    -- non-BMP supplementary character or, under downlevel collation, NULL
    SELECT NCHAR(127925)
  ),
  enc(u16c, u8c) AS (
    SELECT c, CONVERT(VARCHAR(4), c COLLATE Latin1_General_100_CI_AI_SC_UTF8)
    FROM uni
  )
  SELECT u16c AS [Music note]
    , u8c AS [Music note (UTF-8)]
    , UNICODE(u16c) AS [Code Point]
    , CONVERT(VARBINARY(4), u16c) AS [UTF-16LE bytes]
    , CONVERT(VARBINARY(4), u8c)  AS [UTF-8 bytes]
  FROM enc