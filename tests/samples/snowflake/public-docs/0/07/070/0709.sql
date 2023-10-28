CREATE OR REPLACE TABLE test_boolean(
   b BOOLEAN,
   n NUMBER,
   s STRING);

INSERT INTO test_boolean VALUES (true, 1, 'yes'), (false, 0, 'no'), (null, null, null);

SELECT * FROM test_boolean;
