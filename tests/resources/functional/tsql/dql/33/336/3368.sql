-- tsql sql:
SELECT P_Partkey, 3 + 4 FROM (VALUES (1, 'Part1'), (2, 'Part2')) AS Part (P_Partkey, P_Name);
