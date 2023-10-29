-- see https://docs.snowflake.com/en/sql-reference/functions/object_pick

SELECT OBJECT_PICK(
    OBJECT_CONSTRUCT(
        'a', 1,
        'b', 2,
        'c', 3
    ),
    'a', 'b'
) AS new_object;