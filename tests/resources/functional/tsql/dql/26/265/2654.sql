-- tsql sql:
SELECT KEY_ID('#NewKey')
FROM (
    VALUES ('#NewKey')
) AS T(key_value);
