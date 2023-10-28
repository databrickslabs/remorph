CREATE TABLE union_test(a array);

INSERT INTO union_test
    SELECT PARSE_JSON('[ 1, 1, 2]')
    UNION ALL
    SELECT PARSE_JSON('[ 1, 2, 3]');

SELECT ARRAY_UNION_AGG(a) FROM union_test;