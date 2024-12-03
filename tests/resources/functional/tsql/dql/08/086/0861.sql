--Query type: DQL
SELECT * FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three')) AS T1 (c1, c2) WHERE T1.c1 IN (SELECT c1 FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three')) AS T2 (c1, c2) WHERE T2.c2 = 'two');
