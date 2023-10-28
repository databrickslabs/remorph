SELECT * FROM TABLE(FLATTEN(input => parse_json('[1, ,77]'))) f;
