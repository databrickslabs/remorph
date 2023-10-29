-- see https://docs.snowflake.com/en/sql-reference/functions/is_null_value

SELECT v, v:a, IS_NULL_VALUE(v:a), IS_NULL_VALUE(v:no_such_field)
    FROM
        (SELECT parse_json(column1) AS v
         FROM VALUES
             ('{"a": null}'),
             ('{"a": "foo"}'),
             (NULL)
        );