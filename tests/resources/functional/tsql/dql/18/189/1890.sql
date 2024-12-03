--Query type: DQL
DECLARE @categories NVARCHAR(400) = 'electronics,books,,sports,toys';
WITH categories AS (
    SELECT value
    FROM STRING_SPLIT(@categories, ',')
)
SELECT value AS category
FROM categories
WHERE RTRIM(value) <> '';
