-- tsql sql:
SELECT * FROM (VALUES (1, 'a'), (2, 'b'), (3, 'c')) AS board(v, d), (VALUES (1, 'x'), (2, 'y'), (3, 'z')) AS bored(v, e) WHERE board.v = bored.v;
