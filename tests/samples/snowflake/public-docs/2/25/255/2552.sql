SELECT GET_IGNORE_CASE(TO_OBJECT(PARSE_JSON('{"aa":1, "aA":2, "Aa":3}')),'AA') as output;
