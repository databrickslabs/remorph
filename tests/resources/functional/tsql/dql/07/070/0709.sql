--Query type: DQL
WITH dates AS (
    SELECT '2022-01-01' AS event_date
    UNION ALL
    SELECT '2022-01-02' AS event_date
)
SELECT
    d.event_date AS [Date],
    t.city,
    t.temperature
FROM
    dates d
    CROSS APPLY (
        SELECT
            city,
            temperature
        FROM
            (
                VALUES
                    ('New York', 32, '2022-01-01'),
                    ('Los Angeles', 75, '2022-01-01'),
                    ('New York', 30, '2022-01-02'),
                    ('Los Angeles', 78, '2022-01-02')
            ) AS temperatures (city, temperature, event_date)
        WHERE
            temperatures.event_date = d.event_date
            AND temperature > 50
    ) AS t
ORDER BY
    d.event_date,
    t.city