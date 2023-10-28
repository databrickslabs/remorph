CREATE TABLE demo (v VARCHAR, b BINARY);
INSERT INTO demo (v, b) SELECT 'Hi', HEX_ENCODE('Hi');
INSERT INTO demo (v, b) SELECT '-123.00', HEX_ENCODE('-123.00');
INSERT INTO demo (v, b) SELECT 'Twelve Dollars', 
  TO_BINARY(HEX_ENCODE('Twelve Dollars'), 'HEX');