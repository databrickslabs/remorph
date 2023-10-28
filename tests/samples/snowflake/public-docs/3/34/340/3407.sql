-- Evaluates using "English case-insensitive" collation:
SELECT * FROM t1 WHERE COLLATE(col1 , 'en-ci') = 'Tango';

-- Sorts the results using German (Deutsch) collation.
SELECT * FROM t1 ORDER BY COLLATE(col1 , 'de');

-- Creates a table with a column using French collation.
CREATE TABLE t2 AS SELECT COLLATE(col1, 'fr') AS col1 FROM t1;

-- Creates a table with a column using French collation.
CREATE TABLE t2 AS SELECT col1 COLLATE 'fr' AS col1 FROM t1;