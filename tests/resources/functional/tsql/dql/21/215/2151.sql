--Query type: DQL
IF 3 < ALL (SELECT ORDERKEY FROM (VALUES (1), (2), (3), (4), (5)) AS T2(ORDERKEY))
PRINT 'TRUE'
ELSE
PRINT 'FALSE';
