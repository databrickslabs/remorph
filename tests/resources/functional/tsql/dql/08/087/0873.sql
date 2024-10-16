--Query type: DQL
SELECT
    *
FROM
    (
        VALUES
            ('{"a":1, "b":[77,88], "c": {"d":"X"}}')
    ) AS json_data (json_string)
CROSS APPLY
    OPENJSON(json_data.json_string)
    WITH (
        a INT '$.a',
        b NVARCHAR(MAX) '$.b' AS JSON,
        c NVARCHAR(MAX) '$.c' AS JSON
    ) AS flattened_json
CROSS APPLY
    OPENJSON(flattened_json.b)
    WITH (
        b_value INT '$'
    ) AS flattened_b
CROSS APPLY
    OPENJSON(flattened_json.c)
    WITH (
        c_d NVARCHAR(MAX) '$.d'
    ) AS flattened_c