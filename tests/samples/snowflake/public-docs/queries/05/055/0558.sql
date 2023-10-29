-- see https://docs.snowflake.com/en/sql-reference/functions/to_xml

CREATE TABLE xml2 (x OBJECT);
INSERT INTO xml2 (x)
  SELECT PARSE_XML('<note> <body>Sample XML</body> </note>');