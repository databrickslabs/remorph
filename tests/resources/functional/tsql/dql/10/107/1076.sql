-- tsql sql:
WITH temp_result AS (
    SELECT n_name, COUNT(*) AS count
    FROM (
        VALUES ('name1'), ('name2'), ('name3')
    ) AS temp_table(n_name)
    GROUP BY n_name
)
SELECT
    $PARTITION.RangePF1(n_name) AS Partition,
    COUNT(*) AS [COUNT]
FROM temp_result
GROUP BY $PARTITION.RangePF1(n_name)
ORDER BY Partition;
