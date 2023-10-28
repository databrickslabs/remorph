SELECT * FROM TABLE(FLATTEN(input => parse_json('[]'))) f;


SELECT * FROM TABLE(FLATTEN(input => parse_json('[]'), outer => true)) f;
