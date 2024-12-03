--Query type: DQL
DECLARE @new_date DATETIME2 = '2022-01-01 12:00:00';
WITH buckets AS (
    SELECT
        DATE_BUCKET(WEEK, 2, @new_date) AS bucket_2,
        DATE_BUCKET(WEEK, 3, @new_date) AS bucket_3,
        DATE_BUCKET(WEEK, 4, @new_date) AS bucket_4,
        DATE_BUCKET(WEEK, 6, @new_date) AS bucket_6
)
SELECT * FROM buckets;
