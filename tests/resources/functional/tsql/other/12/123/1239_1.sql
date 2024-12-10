-- tsql sql:
CREATE TABLE region (regionkey INT, name NVARCHAR(25), comment NVARCHAR(100));
INSERT INTO region (regionkey, name, comment)
VALUES (1, 'North', 'This is the north region'), (2, 'South', 'This is the south region');
CREATE PRIMARY XML INDEX pxi_region ON region (name);
CREATE SELECTIVE XML INDEX sxi_region ON region (name)
FOR (
    pathregionkey = '/region/regionkey' AS XQUERY 'xs:integer',
    pathname = '/region/name' AS XQUERY 'xs:string' MAXLENGTH(25) SINGLETON,
    pathcomment = '/region/comment' AS SQL NVARCHAR(100)
);
SELECT * FROM region;
-- REMORPH CLEANUP: DROP TABLE region;
-- REMORPH CLEANUP: DROP INDEX sxi_region ON region;
-- REMORPH CLEANUP: DROP INDEX pxi_region ON region;
