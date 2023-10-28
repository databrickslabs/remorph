SELECT column1,
    ARRAY_TO_STRING(PARSE_JSON(column1), '') AS no_separation,
    ARRAY_TO_STRING(PARSE_JSON(column1), ', ') AS comma_separated
  FROM VALUES
    (NULL),
    ('[]'),
    ('[1]'),
    ('[1, 2]'),
    ('[true, 1, -1.2e-3, "Abc", ["x","y"], {"a":1}]'),
    ('[, 1]'),
    ('[1, ]'),
    ('[1, , ,2]');