-- tsql sql:
SELECT ID FROM (VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9)) AS T(ID) WHERE ID < 10
