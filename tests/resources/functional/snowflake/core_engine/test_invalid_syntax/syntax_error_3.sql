-- snowflake sql:
* ;
SELECT 1 ;
SELECT A B FROM C ;

-- databricks sql:
/* The following issues were detected:

   Unparsed input - ErrorNode encountered
    Unparsable text: unexpected extra input '*' while parsing a Snowflake batch
    expecting one of: End of batch, Select Statement, Statement, '(', ';', 'CALL', 'COMMENT', 'DECLARE', 'GET', 'LET', 'START', 'WITH'...
    Unparsable text: *
 */
SELECT
  1;
SELECT
  A AS B
FROM
  C;
