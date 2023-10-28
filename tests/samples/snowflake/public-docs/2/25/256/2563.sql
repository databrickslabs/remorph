SELECT OBJECT_PICK(
    OBJECT_CONSTRUCT(
        'a', 1,
        'b', 2,
        'c', 3
    ),
    ARRAY_CONSTRUCT('a', 'b')
) AS new_object;