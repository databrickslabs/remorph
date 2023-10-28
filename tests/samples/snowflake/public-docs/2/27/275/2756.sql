SELECT
    TO_JSON(PARSE_JSON('{"b":1,"a":2}')),
    TO_JSON(PARSE_JSON('{"b":1,"a":2}')) = '{"b":1,"a":2}',
    TO_JSON(PARSE_JSON('{"b":1,"a":2}')) = '{"a":2,"b":1}'
    ;