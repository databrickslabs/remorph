-- see https://docs.snowflake.com/en/sql-reference/functions/parse_xml

CREATE TABLE xtab (v OBJECT);

INSERT INTO xtab SELECT PARSE_XML(column1) AS v
  FROM VALUES ('<a/>'), ('<a attr="123">text</a>'), ('<a><b>X</b><b>Y</b></a>');

SELECT * FROM xtab;