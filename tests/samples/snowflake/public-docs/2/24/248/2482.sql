CREATE TABLE xml2 (x OBJECT);
INSERT INTO xml2 (x)
  SELECT PARSE_XML('<note> <body>Sample XML</body> </note>');