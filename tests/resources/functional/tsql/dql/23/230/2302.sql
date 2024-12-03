--Query type: DQL
WITH TempResult AS (
    SELECT '2006-04-25T15:50:59.997' AS OriginalText
)
SELECT
    OriginalText AS UnconvertedText,
    CAST(OriginalText AS DATETIME) AS UsingCast,
    CONVERT(DATETIME, OriginalText, 126) AS UsingConvertFrom_ISO8601
FROM TempResult;
