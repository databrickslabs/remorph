-- tsql sql:
CREATE TABLE #T1 (c1 INT, c2 XML) WITH (XML_COMPRESSION = ON);
SELECT c1, c2
FROM (VALUES (1, '<root><a>1</a><b>2</b></root>'), (2, '<root><a>3</a><b>4</b></root>')) AS T2(c1, c2);
