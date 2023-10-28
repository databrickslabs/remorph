CREATE TABLE hex (v VARCHAR, hex_string VARCHAR, garbage VARCHAR);
INSERT INTO hex (v, hex_string, garbage) 
  SELECT 'AaBb', HEX_ENCODE('AaBb'), '127';